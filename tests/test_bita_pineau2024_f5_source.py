"""Pineau 2024 Fig5 source-provenance / independent monoculture replay units."""
import json
import pytest

from scripts.audit_bita_pineau2024_f5_source import (
    LOAD_DATA_BLOB, PLOT_CODE_BLOB, AUTHOR_COMMIT,
    validate_author_scripts, summarize_sheet, analyze_original_workbook,
)


def test_source_hashes_and_independent_biological_unit_contract():
    assert AUTHOR_COMMIT=="071affa79f16f0a469f099058372a7488c35c0c2"
    assert LOAD_DATA_BLOB=="77844c9c336d01ea264a0b2b30229f61191a7ff7"
    assert PLOT_CODE_BLOB=="9ec49af81ba1805277223149644c9fe35ab47f0f"
    with pytest.raises(ValueError, match="Git blob"):
        validate_author_scripts(b"changed",b"changed")
    with pytest.raises(ValueError,match="untrusted"):
        analyze_original_workbook(b"not an xlsx",b"not a script",b"not a script")


def test_compact_worksheet_inventory_counts_numeric_and_text_without_cell_duplication():
    rows=[
        {"excel_row":1,"formula_count":0,"cells":{0:"Fig5A original data"}},
        {"excel_row":2,"formula_count":0,"cells":{0:"small_1",1:"small_2",2:"large_1"}},
        {"excel_row":3,"formula_count":0,"cells":{0:12.0,1:15.0,2:45.0}},
        {"excel_row":4,"formula_count":0,"cells":{0:16.0,1:19.0,2:43.0}},
    ]
    info=summarize_sheet(rows,"Fig5A")
    assert info["nonempty_excel_rows"]==4
    assert info["nonempty_excel_columns"]==3
    assert info["cell_type_count"]["numeric"]==6
    assert info["cell_type_count"]["strings"]==4
    assert info["source_numeric_row_count"]==2
    assert info["source_numeric_value_range"]==[12.0,45.0]
    assert info["first_six_source_header_tokens"][1]["text"]==[
        "small_1","small_2","large_1",
    ]


def test_empty_figure_worksheet_rejected():
    with pytest.raises(ValueError,match="empty"):
        summarize_sheet([],"Fig5A")
