"""Structural and negative-control tests for original-source Kinsler intake."""
import pytest
from scripts.audit_bita_kinsler2024_source import (
    SOURCE_COMMIT, EXPECTED_S3_COLUMNS, verify_git_source,
    read_csv, describe_rows, audit_files,
)


def test_pinned_source_and_expected_selected_s3_schema():
    assert SOURCE_COMMIT == "0de5873c853e08e78541cec4f50988f41327af47"
    assert EXPECTED_S3_COLUMNS[:5] == [
        "barcode", "ancestor", "evolution_condition", "class_new", "gene"
    ]


def test_any_changed_raw_source_fails_closed():
    with pytest.raises(ValueError, match="blob"):
        verify_git_source(b"not the original data", "S1_Data.csv")
    with pytest.raises(ValueError, match="blob"):
        verify_git_source(b"not the original data", "S3_Data.csv")


def test_csv_parser_handles_missing_metadata_without_inventing_values():
    head, rows = read_csv(
        b"barcode,ancestor,evolution_condition,ResPerHour\n"
        b"a,IRA1_MIS,Evo2D,0.01\n"
        b"b,IRA1_NON,Evo2D,\n"
    )
    summary = describe_rows(head, rows)
    assert summary["rows"] == 2
    assert summary["distinct_barcode_count"] == 2
    assert summary["columns_with_missing"]["ResPerHour"] == 1
    assert summary["category_counts"]["ancestor"] == {"IRA1_MIS": 1, "IRA1_NON": 1}


def test_duplicate_headers_and_malformed_source_fail_closed():
    with pytest.raises(ValueError, match="duplicated"):
        read_csv(b"barcode,barcode\na,b\n")
    with pytest.raises(ValueError, match="empty"):
        read_csv(b"barcode,ancestor\n")
    with pytest.raises(ValueError, match="surplus"):
        read_csv(b"barcode,ancestor\na,IRA1,CYR1\n")


def test_wrong_original_files_cannot_enter_biological_audit():
    with pytest.raises(ValueError, match="blob"):
        audit_files(b"barcode,ancestor\na,CYR1\n", b"barcode,class_new\na,x\n")
