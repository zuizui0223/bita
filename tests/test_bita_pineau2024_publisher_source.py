"""Publisher source availability is separate from biological identity verification."""
import hashlib
import io
import zipfile
import pytest

from scripts.audit_bita_pineau2024_publisher_source import (
    PMCID, DOI, SUPPLEMENT_NAME, find_named_publisher_xlsx,
    is_xlsx, source_numeric_vectors, column_fingerprint,
)


def fixture_xlsx(duplicate=True):
    """Minimal, synthetic, non-publisher 42-source-column Fig5A."""
    main_ns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    wb=(f'<workbook xmlns="{main_ns}" xmlns:r="{rel_ns}"><sheets>'
        '<sheet name="Fig5A" sheetId="1" r:id="rId1"/>'
        '<sheet name="F2A" sheetId="2" r:id="rId2"/>'
        '<sheet name="F2C" sheetId="3" r:id="rId3"/></sheets></workbook>')
    rel=('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
         '<Relationship Id="rId2" Target="worksheets/sheet2.xml"/>'
         '<Relationship Id="rId3" Target="worksheets/sheet3.xml"/>'
         '</Relationships>')
    def a1(index):
        s=""
        while index:
            index, rem=divmod(index-1,26)
            s=chr(65+rem)+s
        return s
    row2='<row r="2">'
    names={0:"Line1_large_area",6:"Line3_large_area",12:"Line4_large_area",
           18:"Line1_small_area",24:"Line2_small_area",30:"Line3_small_area",36:"Line4_small_area"}
    for i,name in names.items():
        row2+=f'<c r="{a1(i+1)}2" t="inlineStr"><is><t>{name}</t></is></c>'
    row2+='</row>'
    dayrow='<row r="3">' + ''.join(
        f'<c r="{a1(i+1)}3" t="inlineStr"><is><t>Day{[1,5,10,15,20,40][i%6]}</t></is></c>'
        for i in range(42)) + '</row>'
    rows=[]
    for excelrow in range(4,10):
        cells=[]
        for c in range(42):
            val=1000*c+excelrow
            if duplicate and c==23:
                val=1000*5+excelrow
            cells.append(f'<c r="{a1(c+1)}{excelrow}"><v>{val}</v></c>')
        rows.append(f'<row r="{excelrow}">'+''.join(cells)+'</row>')
    sheet=(f'<worksheet xmlns="{main_ns}"><sheetData><row r="1">'
           '<c r="A1" t="inlineStr"><is><t>Figure 5A</t></is></c></row>'
           +row2+dayrow+''.join(rows)+'</sheetData></worksheet>')
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('xl/workbook.xml',wb)
        z.writestr('xl/_rels/workbook.xml.rels',rel)
        z.writestr('xl/worksheets/sheet1.xml',sheet)
        z.writestr('xl/worksheets/sheet2.xml',sheet)
        z.writestr('xl/worksheets/sheet3.xml',sheet)
    return mem.getvalue()


def test_only_original_article_named_supplement_is_considered():
    assert DOI=="10.1038/s41559-024-02367-y"
    assert PMCID=="PMC11090753"
    assert SUPPLEMENT_NAME=="NIHMS1986110-supplement-Source_data.xlsx"
    raw=fixture_xlsx()
    assert is_xlsx(raw)
    direct,member=find_named_publisher_xlsx(raw,SUPPLEMENT_NAME)
    assert direct==raw
    assert member==SUPPLEMENT_NAME
    direct,why=find_named_publisher_xlsx(b'<html>Cloudflare</html>',SUPPLEMENT_NAME)
    assert direct is None and why=="not_an_xlsx_or_zip"


def test_supplier_zip_can_contain_several_other_supplemental_files():
    raw=fixture_xlsx()
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w') as z:
        z.writestr('Unrelated_readme.txt','other')
        z.writestr('supplements/'+SUPPLEMENT_NAME,raw)
        z.writestr('Supplementary_data_1.xlsx',b'other')
    direct,member=find_named_publisher_xlsx(mem.getvalue(),"supplementary.zip")
    assert direct==raw
    assert member=='supplements/'+SUPPLEMENT_NAME
    assert find_named_publisher_xlsx(b'bad','x.zip')[0] is None


def test_source_numeric_column_comparison_detects_complete_cross_population_clone():
    raw=fixture_xlsx()
    parsed=source_numeric_vectors(raw)
    assert parsed["fig5a_found"]
    assert parsed["source_numeric_columns"]==42
    assert parsed["exact_duplicate_audit"]["cross_population_duplicate_pairs"]==1
    assert parsed["exact_duplicate_audit"]["cross_population_suspect_excel_columns_1indexed"]==[6,24]
    assert parsed["source_vector_row_and_value_pairs"][6] == parsed["source_vector_row_and_value_pairs"][24]
    assert parsed["source_vector_row_and_value_pairs"][6] != parsed["source_vector_row_and_value_pairs"][12]
    another=source_numeric_vectors(fixture_xlsx(duplicate=False))
    assert another["exact_duplicate_audit"]["cross_population_duplicate_pairs"]==0
    assert another["source_vector_row_and_value_pairs"][6]!=another["source_vector_row_and_value_pairs"][24]
    assert column_fingerprint(parsed["source_vector_row_and_value_pairs"][6]) == column_fingerprint(parsed["source_vector_row_and_value_pairs"][24])
    assert column_fingerprint(parsed["source_vector_row_and_value_pairs"][6]) != column_fingerprint(another["source_vector_row_and_value_pairs"][24])


def test_source_digest_not_a_new_evolution_study():
    data=((4,10.0),(5,20.0))
    expected=hashlib.sha256(b'[[4,10.0],[5,20.0]]').hexdigest()
    assert column_fingerprint(data)==expected


def test_frozen_official_access_gate_keeps_day40_quarantine():
    import json
    from pathlib import Path
    base=Path(__file__).resolve().parents[1]
    readout=json.loads((base/"empirical/trait_architecture_history/"
                        "pineau2024_publisher_source_adjudication.json").read_text())
    gate=readout["publisher_comparison"]
    assert readout["source_doi"]==DOI
    assert readout["publisher_article_pmcid"]==PMCID
    assert readout["publisher_source_downloaded"] is False
    assert gate["status"]=="publisher_independent_raw_bytes_not_retrieved"
    assert gate["can_decide_whether_publisher_copy_corrected_the_duplicate"] is False
    assert gate["quarantine_author_l1_and_s1_day40_retained"] is True
    attempts=readout["publisher_source_attempts"]
    assert len(attempts)==2
    assert attempts[0]["provider"]=="PMC_author_manuscript_source_data"
    assert attempts[1]["provider"]=="Europe_PMC_official_supplementary_archive"
    for attempt in attempts:
        assert attempt["recognized_source"] is False
        assert attempt["source_grade"]=="no_valid_workbook"
        assert "http_status" not in attempt
        assert "received_bytes" not in attempt
        assert "verified_publisher_xlsx_bytes" not in attempt
    assert attempts[1]["recognized_source"] is False
    src=readout["original_author_source_receipt"]
    assert src["git_blob_sha1"]=="8f7d01b388489374aba210db96495f387d4338e2"
    assert src["sha256"]=="b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f"
    assert src["source_bytes"]==1535384
    duplications=readout["original_author_Fig5A_exact_cross_population_duplicate"]
    assert duplications["cross_population_duplicate_pairs"]==1
    assert duplications["cross_population_suspect_excel_columns_1indexed"]==[6,24]
    assert duplications["exact_duplicate_source_column_pairs"][0][
        "identical_excel_row_and_numeric_value_pairs"]==164
    signatures=readout["original_author_Fig5A_source_column_sha256"]
    assert len(signatures)==42
    assert signatures["6"]==signatures["24"]
    assert signatures["6"] != signatures["5"]
    assert signatures["6"] != signatures["25"]
    assert all(readout["interpretation_ceiling"].values())
