"""Adjudicate whether Pineau 2024's publisher supplementary source repeats a GitHub
Fig5A copy/label conflict (l1 Day40 / s1 Day40: 164 identical values).

One original paper and one supplementary file. This script does not
download full articles, use unlicensed rehosts, or mirror original XLSX
bytes. It compares numeric source identities only. The publisher version
may be unavailable; that is an explicit result, not a success.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import pathlib
import zipfile
from collections import Counter
from scripts.audit_bita_pineau2024_f2_workbook import (
    verify_author_bytes,
    get_workbook_sheets,
    get_shared_strings,
    read_cells,
)
from scripts.analyze_bita_pineau2024_f5_replay import (
    audit_exact_source_column_duplicates,
)

PMCID="PMC11090753"
DOI="10.1038/s41559-024-02367-y"
SUPPLEMENT_NAME="NIHMS1986110-supplement-Source_data.xlsx"
ORIGINAL_PUBLISHER_PAGE="https://pmc.ncbi.nlm.nih.gov/articles/PMC11090753/"
SOURCE_DOI_GITHUB_COMMIT="071affa79f16f0a469f099058372a7488c35c0c2"
KNOWN_AUTHOR_F5A_DUPLICATE=[6,24]
XLSX_MAX_BYTES=8_000_000


def is_xlsx(raw:bytes)->bool:
    if not raw.startswith(b"PK\x03\x04") or len(raw)>XLSX_MAX_BYTES:
        return False
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as f:
            names=f.namelist()
            return "xl/workbook.xml" in names and "xl/_rels/workbook.xml.rels" in names
    except (zipfile.BadZipFile,ValueError):
        return False


def find_named_publisher_xlsx(raw:bytes, origin_name:str)->tuple[bytes|None,str]:
    """Only a direct named XLSX or one named article supplementary ZIP member."""
    if origin_name.endswith(".xlsx") and is_xlsx(raw):
        return raw,origin_name
    if not raw.startswith(b"PK\x03\x04"):
        return None,"not_an_xlsx_or_zip"
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            targets=[
                x for x in z.infolist()
                if pathlib.PurePosixPath(x.filename).name.lower()==SUPPLEMENT_NAME.lower()
            ]
            if len(targets)!=1:
                return None,"supplementary_archive_ambiguous_or_named_source_absent"
            info=targets[0]
            if info.file_size>XLSX_MAX_BYTES:
                return None,"supplementary_source_exceeds_size_limit"
            output=z.read(info)
            if not is_xlsx(output):
                return None,"publisher_source_entry_not_valid_xlsx"
            return output,info.filename
    except (zipfile.BadZipFile,ValueError,RuntimeError,KeyError):
        return None,"malformed_supplementary_zip"


def source_numeric_vectors(workbook:bytes)->dict:
    if not is_xlsx(workbook):
        raise ValueError("publisher candidate must be valid XLSX")
    with zipfile.ZipFile(io.BytesIO(workbook)) as z:
        sheetnames=get_workbook_sheets(z)
        if "Fig5A" not in sheetnames:
            return {"fig5a_found":False,"available_sheet_names":list(sheetnames)}
        rows=read_cells(z,sheetnames["Fig5A"],get_shared_strings(z))
    if len(rows)<5 or rows[1]["cells"].get(0)!="Line1_large_area":
        raise ValueError("publisher candidate Fig5A does not match source figure identities")
    if rows[1]["cells"].get(18)!="Line1_small_area":
        raise ValueError("publisher source Fig5A changed Small population header")
    vectors={}
    for col in range(42):
        pairs=tuple((r["excel_row"],float(r["cells"][col]))
                    for r in rows[3:]
                    if col in r["cells"] and type(r["cells"][col]) in (int,float))
        if not pairs:
            raise ValueError("publisher Fig5A has empty expected source column")
        vectors[col+1]=pairs
    duplications=audit_exact_source_column_duplicates(rows)
    return {
        "fig5a_found":True,
        "fig5a_original_numeric_rows":len(rows)-3,
        "source_numeric_columns":42,
        "source_columns_have_identified_names":True,
        "source_vector_row_and_value_pairs":vectors,
        "exact_duplicate_audit":duplications,
    }


def column_fingerprint(pairs:tuple)->str:
    canonical=json.dumps(pairs,separators=(",",":"),allow_nan=False).encode("utf8")
    return hashlib.sha256(canonical).hexdigest()


def audit(author_bytes:bytes, publisher_bytes:bytes|None,
          publisher_url:str|None, fetch_receipts:list[dict], archive_member:str|None)->dict:
    author_identity=verify_author_bytes(author_bytes)
    auth=source_numeric_vectors(author_bytes)
    if not auth["fig5a_found"]:
        raise ValueError("known author workbook Fig5A source unexpectedly missing")
    duplicates=auth["exact_duplicate_audit"]
    if (duplicates["cross_population_duplicate_pairs"]!=1
        or duplicates["cross_population_suspect_excel_columns_1indexed"]!=KNOWN_AUTHOR_F5A_DUPLICATE):
        raise ValueError("registered 164-cell source data anomaly changed")
    first=duplicates["exact_duplicate_source_column_pairs"][0]
    if first["identical_excel_row_and_numeric_value_pairs"]!=164:
        raise ValueError("exact original source overlap count is not 164")
    out={
        "source_doi":DOI, "publisher_article_pmcid":PMCID,
        "original_publisher_supplement_name":SUPPLEMENT_NAME,
        "original_publisher_article_url":ORIGINAL_PUBLISHER_PAGE,
        "original_author_source_receipt":author_identity,
        "publisher_source_attempts":fetch_receipts,
        "publisher_source_downloaded":publisher_bytes is not None,
        "publisher_source_url":publisher_url,
        "publisher_source_archive_member":archive_member,
        "original_author_Fig5A_exact_cross_population_duplicate":duplicates,
        "original_author_Fig5A_source_column_sha256":{
            str(col):column_fingerprint(pairs)
            for col,pairs in sorted(auth["source_vector_row_and_value_pairs"].items())
        },
    }
    if publisher_bytes is None:
        out["publisher_comparison"]={
            "status":"publisher_independent_raw_bytes_not_retrieved",
            "can_decide_whether_publisher_copy_corrected_the_duplicate":False,
            "quarantine_author_l1_and_s1_day40_retained":True,
        }
    else:
        pub=source_numeric_vectors(publisher_bytes)
        compare={
            "status":"publisher_independent_distribution_retrieved",
            "publisher_workbook_bytes":len(publisher_bytes),
            "publisher_workbook_sha256":hashlib.sha256(publisher_bytes).hexdigest(),
            "same_raw_xlsx_bytes_as_author_GitHub":publisher_bytes==author_bytes,
            "publisher_fig5a_found":pub["fig5a_found"],
        }
        if pub["fig5a_found"]:
            same=[
                col for col in range(1,43)
                if auth["source_vector_row_and_value_pairs"][col]==pub["source_vector_row_and_value_pairs"][col]
            ]
            compare.update({
                "original_Fig5A_source_columns_identical_to_author_count":len(same),
                "source_column_numbers_identical":[int(i) for i in same],
                "source_column_numbers_changed":[i for i in range(1,43) if i not in same],
                "publisher_original_Fig5A_exact_cross_population_duplicate":pub["exact_duplicate_audit"],
                "publisher_has_exact_same_l1_and_s1_day40_duplicate":(
                    pub["source_vector_row_and_value_pairs"][6]==
                    pub["source_vector_row_and_value_pairs"][24]
                ),
                "publisher_l1_day40_matches_GitHub_l1_day40":(
                    pub["source_vector_row_and_value_pairs"][6]==
                    auth["source_vector_row_and_value_pairs"][6]
                ),
                "publisher_s1_day40_matches_GitHub_s1_day40":(
                    pub["source_vector_row_and_value_pairs"][24]==
                    auth["source_vector_row_and_value_pairs"][24]
                ),
            })
            if not compare["publisher_has_exact_same_l1_and_s1_day40_duplicate"]:
                compare["publication_revisions_may_enable_resolution"]=True
                compare["which_original_micrograph_is_correct_still_unverified"]=True
            else:
                compare["publisher_source_mirrors_duplicate_not_independent_biological_validation"]=True
                compare["quarantine_author_l1_and_s1_day40_retained"]=True
        else:
            compare["quarantine_author_l1_and_s1_day40_retained"]=True
            compare["other_source_is_not_original_Fig5A_measurements"]=True
        out["publisher_comparison"]=compare
    out["interpretation_ceiling"]={
        "same_original_Pineau2024_research_programme":True,
        "duplicate_source_column_not_two_independent_day40_measurements":True,
        "publisher_distribution_identity_not_independent_raw_microscopy_verification":True,
        "cannot_infer_gene_module_split_or_historical_origin_rate":True,
        "do_not_promote_unadjudicated_l1_s1_day40_results":True,
        "no_published_xlsx_or_original_measurement_vectors_committed":True,
    }
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--author",required=True,type=pathlib.Path)
    p.add_argument("--publisher",type=pathlib.Path)
    p.add_argument("--publisher-url")
    p.add_argument("--archive-member")
    p.add_argument("--fetch-receipts",required=True,type=pathlib.Path)
    p.add_argument("--output",required=True,type=pathlib.Path)
    a=p.parse_args()
    doc=audit(a.author.read_bytes(),
              a.publisher.read_bytes() if a.publisher and a.publisher.is_file() else None,
              a.publisher_url,
              json.loads(a.fetch_receipts.read_text(encoding="utf8")),
              a.archive_member)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf8")
    m=doc["publisher_comparison"]
    print("BITA_PINEAU_PUBLISHER_SOURCE_AUDIT:"+json.dumps({
        "status":m["status"],
        "attempts":doc["publisher_source_attempts"],
        "duplicate_in_author":doc["original_author_Fig5A_exact_cross_population_duplicate"]["cross_population_duplicate_pairs"],
        "compared_columns":m.get("original_Fig5A_source_columns_identical_to_author_count"),
        "publisher_has_original_duplicate":m.get("publisher_has_exact_same_l1_and_s1_day40_duplicate"),
        "publisher_sha256":m.get("publisher_workbook_sha256"),
    },sort_keys=True),flush=True)


if __name__=="__main__":
    main()
