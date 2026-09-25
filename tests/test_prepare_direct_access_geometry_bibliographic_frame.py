from __future__ import annotations

from pathlib import Path

import pytest

from scripts.prepare_direct_access_geometry_bibliographic_frame import prepare


def _write_scopus(path: Path, q: int, doi: str = "") -> None:
    path.write_text(
        "EID,DOI,Title,Year,Authors,Source title,Link\n"
        f"2-s2.0-{q},{doi},Title {q},202{q % 5},Author {q},Journal {q},https://example/{q}\n",
        encoding="utf-8",
    )


def test_prepares_q1_q8_frame_from_one_source(tmp_path: Path) -> None:
    input_dir = tmp_path / "exports"
    output_dir = tmp_path / "prepared"
    input_dir.mkdir()
    for q in range(1, 9):
        _write_scopus(input_dir / f"Q{q}.csv", q)

    result = prepare(
        input_dir,
        output_dir,
        search_date="2026-09-25",
    )
    assert result["status"] == "OUTCOME_BLIND_Q1_Q8_FRAME_PREPARED"
    assert result["source_db"] == "Scopus"
    assert result["input_rows"] == 8
    assert result["unique_bibliographic_records"] == 8
    assert result["duplicate_rows_collapsed"] == 0
    assert result["formal_recurrence_result_open"] is False
    assert result["primary_standardized_network_k"] == 2

    assert (output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv").exists()
    assert (
        output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_RECEIPT_V1.json"
    ).exists()
    assert (
        output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_INTAKE_RECEIPT_V1.json"
    ).exists()
    assert len(list((output_dir / "normalized_raw").glob("Q*.csv"))) == 8


def test_rejects_missing_query_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "exports"
    input_dir.mkdir()
    for q in range(1, 8):
        _write_scopus(input_dir / f"Q{q}.csv", q)

    with pytest.raises(ValueError, match="BIB_INTAKE_MISSING_QUERY_FILE:Q8"):
        prepare(input_dir, tmp_path / "out", search_date="2026-09-25")


def test_rejects_multiple_files_for_same_query(tmp_path: Path) -> None:
    input_dir = tmp_path / "exports"
    input_dir.mkdir()
    for q in range(1, 9):
        _write_scopus(input_dir / f"Q{q}.csv", q)
    (input_dir / "Q1.tsv").write_text(
        "UT\tDI\tTI\tPY\tAU\tSO\tURL\n"
        "WOS:1\t\tOther\t2020\tA\tJ\thttps://example/other\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="BIB_INTAKE_MULTIPLE_QUERY_FILES:Q1"):
        prepare(input_dir, tmp_path / "out", search_date="2026-09-25")
