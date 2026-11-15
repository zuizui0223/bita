"""Reanalyse Nature Microbiology 2018 original evolutionary mutation supplement.

Input is official Nature XLSX bytes SHA-pinned. Reading OOXML using only
Python stdlib avoids depending on a spreadsheet-application engine.
Mutation presence ≠ viable architecture, phenotype, functional rescue,
or an independently evolved new trait. Clones within a line are dependent.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

SOURCE_DOI = "10.1038/s41564-018-0263-y"
SOURCE_URL = (
    "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-018-0263-y/"
    "MediaObjects/41564_2018_263_MOESM3_ESM.xlsx"
)
SOURCE_SHA256 = "ec916667dbd7a288246737979e3b0d2e4336acfcc8dd98d641339973361d9a43"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
MIXES = ("Mix1", "Mix3", "Mix4")
TRANSFERS = (5, 14, 24)


def F_TO_R2(F: float, predictors: int, residual_df: int) -> dict:
    """Compare reported Figure 3 'R2' with raw vs adjusted conventional R2."""
    if not math.isfinite(F) or F <= 0 or predictors <= 0 or residual_df <= 0:
        raise ValueError("invalid regression F/df")
    r2 = (F*predictors) / (F*predictors + residual_df)
    adj = 1-(1-r2)*(residual_df+predictors)/residual_df
    return {"F":F,"numerator_df":predictors,"residual_df":residual_df,
            "r2_raw":r2,"r2_adjusted":adj}


def _read_sheet(z: zipfile.ZipFile, sheet_id: int, shared: list[str]) -> list[dict]:
    xml=ET.fromstring(z.read(f"xl/worksheets/sheet{sheet_id}.xml"))
    result=[]
    for row in xml.iter(NS+"row"):
        cells={}
        for cell in row.findall(NS+"c"):
            reference=cell.attrib.get("r")
            m=re.fullmatch(r"([A-Z]+)(\d+)",reference or "")
            if m is None:
                raise ValueError("unexpected Excel cell reference")
            column=m.group(1)
            val=cell.find(NS+"v")
            if cell.get("t")=="inlineStr":
                inline=cell.find(NS+"is")
                v="".join(t.text or "" for t in inline.iter(NS+"t")) if inline is not None else None
            elif val is None:
                continue
            elif cell.get("t")=="s":
                v=shared[int(val.text)]
            else:
                v=val.text
            cells[column]=v
        if cells:
            result.append(cells)
    return result


def _shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    xml=ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in node.iter(NS+"t"))
            for node in xml.findall(NS+"si")]


def _column_label(n: int) -> str:
    s=""
    while n:
        n,a=divmod(n-1,26)
        s=chr(65+a)+s
    return s


def analyze_source_xlsx(data: bytes) -> dict:
    if hashlib.sha256(data).hexdigest()!=SOURCE_SHA256:
        raise ValueError("original Nature XLSX sha256 mismatch")
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("source is not XLSX ZIP")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        shared=_shared_strings(z)
        evolved=_read_sheet(z,3,shared)  # Original tab: 'unique for eps'
        mixed=_read_sheet(z,6,shared)    # Original tab: 'resequenced populations (mix)'
    if len(evolved)<3 or evolved[0].get("Q")!="Gene name":
        raise ValueError("unique-for-eps original-source gene column changed")
    if len(mixed)<10 or mixed[1].get("Y")!="Gene name":
        raise ValueError("source mixed-population headers changed")
    # The original 'unique for eps' tab refers to delta-eps isolates:
    # e4A/e4B/e4C are three isolates FROM e4, not independent lineages.
    col_names={_column_label(i):evolved[0].get(_column_label(i))
               for i in range(7,17)}
    alleles=[]
    for row in evolved[1:]:
        if row.get("Q")!="tasA":
            continue
        clone_ids=[sample for col,sample in col_names.items()
                   if sample and row.get(col)=="X"]
        if not clone_ids:
            continue
        parents=sorted({re.match(r"^(e\d+)",sample).group(1)
                        for sample in clone_ids
                        if re.match(r"^e\d+",sample)})
        if len(parents)!=1:
            raise ValueError("mixed independent clone origins for a variant")
        alleles.append({
            "gene":"tasA",
            "position":int(row["A"]),
            "amino_acid":row.get("F"),
            "clonal_lineage":parents[0],
            "clone_ids":sorted(clone_ids),
        })
    alleles.sort(key=lambda r:r["clonal_lineage"])
    if [(r["position"],r["amino_acid"],r["clonal_lineage"],
         r["clone_ids"]) for r in alleles]!=[
        (2552702,"Tyr124Cys","e4",["e4A","e4B","e4C"]),
        (2552526,"Gly183Cys","e6",["e6A","e6B","e6C"]),
    ]:
        raise ValueError("source TasA cysteine mutation coding drift")
    # Original mix headers carry two classes each with three independent
    # mixed-population IDs (Mix1, Mix3, Mix4), each at 3 transfers.
    h=mixed[1]
    backgrounds = {
        "delta_eps": [_column_label(i) for i in range(7,16)],
        "delta_tasA":[_column_label(i) for i in range(16,25)],
    }
    if sorted(h[c] for cols in backgrounds.values() for c in cols)!=sorted(
        [f"{mix}_tr.{transfer}" for mix in MIXES for transfer in TRANSFERS]*2
    ):
        raise ValueError("unexpected original sample/transfer labels")
    original_rows=mixed[2:]
    # Record positions/alleles. The workbook has a non-"X" numeric cell,
    # which must not be treated as mutation presence or as explicit absence.
    profiles=[]
    unexpected=[]
    for row in original_rows:
        if row.get("A") is None:
            continue
        key={
            "position":int(row["A"]),
            "type":row.get("B") or None,
            "reference":row.get("C") or None,
            "allele":row.get("D") or None,
            "gene":row.get("Y") or "(unannotated)",
            "amino_acid":row.get("F") or None,
        }
        if any(not item["position"] or item["allele"] is None
               for item in [key]):
            raise ValueError("missing source locus information")
        marks={}
        for genotype,cols in backgrounds.items():
            marks[genotype]={}
            for c in cols:
                v=row.get(c)
                if v not in (None,""," ","X"):
                    unexpected.append({"mutation":key,"genotype":genotype,
                                       "sample":h[c],"cell_value":v})
                if v=="X":
                    marks[genotype][h[c]]=True
        profiles.append({"mutation":key,"calls":marks})
    if len(profiles)!=13:
        raise ValueError("unexpected original time-resolved locus count")
    stable_baseline={}
    series=[]
    for genotype,cols in backgrounds.items():
        stable_baseline[genotype]=[
            {"position":p["mutation"]["position"],"gene":p["mutation"]["gene"]}
            for p in profiles
            if all(p["calls"][genotype].get(h[col]) is True for col in cols)
        ]
        for mix in MIXES:
            sets={}
            for t in TRANSFERS:
                name=f"{mix}_tr.{t}"
                observed={
                    p["mutation"]["position"]
                    for p in profiles
                    if p["calls"][genotype].get(name) is True
                }
                sets[t]=observed
            novel=sets[24]-sets[5]
            absent_late=sets[5]-sets[24]
            series.append({
                "background":genotype,"mixed_population":mix,
                "count_X_by_transfer":{str(t):len(sets[t]) for t in TRANSFERS},
                "newly_detected_by_24_not_5":[
                    {"position":p["mutation"]["position"],"gene":p["mutation"]["gene"]}
                    for p in profiles if p["mutation"]["position"] in novel
                ],
                "detected_5_not_24":[
                    {"position":p["mutation"]["position"],"gene":p["mutation"]["gene"]}
                    for p in profiles if p["mutation"]["position"] in absent_late
                ],
            })
    if (len(unexpected)!=0
        or stable_baseline!={"delta_eps":[
           {"position":375887,"gene":"hxlA"},
           {"position":3502519,"gene":"ganA"}],
           "delta_tasA":[
           {"position":3509522,"gene":"(unannotated)"},
           {"position":3517700,"gene":"epsK"}],
        }):
        raise ValueError("source first-transfer/shared-variant coding drift")
    return {
        "source_doi":SOURCE_DOI,
        "source_url":SOURCE_URL,
        "original_supplement_sha256":SOURCE_SHA256,
        "source_file_size":len(data),
        "data_level":"NATURE_AUTHOR_MUTATION_XLSX_NOT_GROWTH_RAW_DATA",
        "original_gene_sheet":"unique for eps",
        "original_mix_time_sheet":"resequenced populations (mix)",
        "evolved_eps_deficient_tasa_cysteine_alleles":alleles,
        "genetically_independent_tasa_cys_lineages_lower_bound":len({
            r["clonal_lineage"] for r in alleles}),
        "distinct_mutant_clones_not_independent_lineages":sum(len(r["clone_ids"]) for r in alleles),
        "mixed_population_groups":len(series),
        "mixed_population_transfer_records":len(series)*len(TRANSFERS),
        "first_observed_transfer":min(TRANSFERS),
        "last_observed_transfer":max(TRANSFERS),
        "mixed_mutations_newly_detected_at_24_vs_5":sum(
            len(r["newly_detected_by_24_not_5"]) for r in series),
        "mixed_mutations_not_detected_at_24_but_detected_at_5":sum(
            len(r["detected_5_not_24"]) for r in series),
        "n_ambiguous_or_non_X_cells":len(unexpected),
        "ambiguous_cells":unexpected,
        "mixed_mutations_present_in_all_9_within_genotype":stable_baseline,
        "original_mutation_calls":profiles,
        "mixed_population_time_summaries":series,
        "identical_baseline_markers_coded_as_independent_recurrent_mutations":False,
        "mixed_populations_collapsed_from_genotypes":False,
        "phenotypic_productivity_effect_from_supplement_estimated":False,
        "evolutionary_origin_of_division_identified":False,
        "reported_initial_bacillus_fig3":{
            "source_doi":"10.1016/j.cub.2018.04.046",
            "source_grade":"PUBLICLY_INDEXED_ORIGINAL_TEXT_NOT_DOWNLOADED_JATS",
            "productivity_model":F_TO_R2(54.9,3,68),
            "within_mix_frequency_model":F_TO_R2(94.7,3,46),
            "paper_displayed_R2":[.695,.852],
            "interpretation":"Reported R2 matches adjusted rather than raw R2 under the conventional F-to-R2 transformation; these are source-reported model fits, not WT effect-size estimates.",
        },
        "claim_boundary":(
            "The 2018 Nature follow-up source proves data availability and "
            "records specific mutation calls in evolved lines. Three clone "
            "isolates from one e4 or e6 lineage are NOT three independent "
            "mutation-origin events. Mixed samples at transfers 5/14/24 "
            "supply mutation detection snapshots, not complete first-fixation "
            "times: X absent at a sample is not molecular proof of mutation "
            "absence or ancestral genotype. Common group-specific variants "
            "present at the first transfer are not counted as independent "
            "parallel origins. The original supplement has NO matched "
            "pellicle productivity/fitness measurements. Experimentally "
            "reported collapse is qualitative original-paper evidence, not "
            "recalculated from mutation-only observations. No K(u), "
            "independent evolutionary architecture origin, cost curvature, "
            "or cross-study meta effect is identified."
        ),
    }


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xlsx",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=analyze_source_xlsx(args.xlsx.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("BITA_BACILLUS_MUTATIONS_JSON:"+json.dumps({
        "source_sha256":result["original_supplement_sha256"],
        "tasa_alleles":result["evolved_eps_deficient_tasa_cysteine_alleles"],
        "mix_groups":result["mixed_population_groups"],
        "mixed_variants_newly_detected":result["mixed_mutations_newly_detected_at_24_vs_5"],
        "mixed_variants_lost_detection":result["mixed_mutations_not_detected_at_24_but_detected_at_5"],
        "baseline":result["mixed_mutations_present_in_all_9_within_genotype"],
        "r2_checks":result["reported_initial_bacillus_fig3"]
    },ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
