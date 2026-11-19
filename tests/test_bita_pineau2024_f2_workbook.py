"""Only author source workbook and competition-series inference units are allowed."""
import io
import json
import math
import zipfile
from pathlib import Path

import pytest

from scripts.audit_bita_pineau2024_f2_workbook import (
    XLSX_BLOB_SHA1, XLSX_SHA256, WORKBOOK_ORIGINAL_BYTES,
    AUTHOR_COMMIT, verify_author_bytes, col_index, fit_ols,
    numeric_matrix, f2_reanalysis, get_shared_strings, get_workbook_sheets,
    read_cells,
)


def test_author_identity_and_sha256_are_frozen():
    assert AUTHOR_COMMIT == "071affa79f16f0a469f099058372a7488c35c0c2"
    assert XLSX_BLOB_SHA1 == "8f7d01b388489374aba210db96495f387d4338e2"
    assert XLSX_SHA256 == "b6bc44d5085344292b5b33cac81369652b25e56f0947c1057f4c00ae4947057f"
    assert WORKBOOK_ORIGINAL_BYTES == 1535384
    with pytest.raises(ValueError, match="untrusted"):
        verify_author_bytes(b"fake workbook")


def test_column_addresses_and_no_risk_of_column_aliasing():
    assert col_index("A1") == 0
    assert col_index("H6") == 7
    assert col_index("AA1") == 26
    with pytest.raises(ValueError):
        col_index("NotACell")


def test_fitted_frequency_change_uses_complete_independent_competitions_only():
    starting = [0.1, 0.3, 0.5, 0.7]
    changes = [0.2-0.5*x for x in starting]
    fit=fit_ols(starting,changes)
    assert fit["n_paired_trajectories"] == 4
    assert fit["slope"] == pytest.approx(-0.5)
    assert fit["intercept"] == pytest.approx(.2)
    assert fit["equilibrium_if_slope_nonzero"] == pytest.approx(.4)
    with pytest.raises(ValueError, match="minimum three"):
        fit_ols([.1,.2],[.2,.1])


def test_sheet_extraction_and_missing_competition_series_are_separate():
    rows=[
        {"excel_row":1,"cells":{0:"C1",1:"C2",2:"C3",3:"C4"},"formula_count":0},
        {"excel_row":2,"cells":{0:.1,1:.3,2:.5,3:.7},"formula_count":0},
        {"excel_row":3,"cells":{0:.15,1:.35,2:None,3:.55},"formula_count":0},
        {"excel_row":4,"cells":{0:.2,1:.4,2:.4,3:.5},"formula_count":0},
        {"excel_row":5,"cells":{0:.25,1:.45,2:.35,3:.45},"formula_count":0},
    ]
    sheet=numeric_matrix(rows,"F2A")
    assert sheet["summary"]["active_column_count"] == 4
    assert sheet["summary"]["numeric_row_count"] == 4
    audit=f2_reanalysis(sheet,8)
    assert audit["original_sheet_active_series"] == 4
    assert audit["complete_trajectory_count"] == 3
    assert audit["incomplete_active_excel_columns"] == [3]
    assert audit["first_last_fit"]["n_paired_trajectories"] == 3


def test_xml_relationships_and_numeric_table_are_not_excel_formulas():
    workbook=(
        '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships"><sheets>'
        '<sheet name="F2A" sheetId="1" r:id="rId1"/>'
        '<sheet name="F2C" sheetId="2" r:id="rId2"/>'
        '</sheets></workbook>'
    )
    relations=(
        '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/'
        'package/2006/relationships">'
        '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Target="worksheets/sheet2.xml"/>'
        '</Relationships>'
    )
    sheet=(
        '<worksheet xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main"><sheetData>'
        '<row r="1"><c r="A1" t="inlineStr"><is><t>C1</t></is></c></row>'
        '<row r="2"><c r="A2"><v>0.1</v></c></row>'
        '</sheetData></worksheet>'
    )
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        z.writestr("xl/workbook.xml",workbook)
        z.writestr("xl/_rels/workbook.xml.rels",relations)
        z.writestr("xl/worksheets/sheet1.xml",sheet)
        z.writestr("xl/worksheets/sheet2.xml",sheet)
    with zipfile.ZipFile(io.BytesIO(b.getvalue())) as z:
        names=get_workbook_sheets(z)
        assert names=={"F2A":"xl/worksheets/sheet1.xml","F2C":"xl/worksheets/sheet2.xml"}
        cells=read_cells(z,names["F2A"],get_shared_strings(z))
        assert cells[0]["cells"][0]=="C1"
        assert cells[1]["cells"][0]==.1
        assert not cells[0]["formula_count"]
