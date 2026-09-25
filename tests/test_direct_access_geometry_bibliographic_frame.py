from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_direct_access_geometry_bibliographic_frame import (
    REQUIRED_COLUMNS,
    build,
)


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _row(q: str, rid: str, title: str, year: int, doi: str = "") -> dict[str, str]:
    return {
        "source_db": "ExampleDB",
        "query_id": q,
        "record_id": rid,
        "doi": doi,
        "title": title,
        "year": str(year),
        "authors": "A. Author",
        "publication": "Example Journal",
        "url": "https://example.org/" + rid,
        "search_date": "2026-09-25",
    }


def test_builds_complete_outcome_blind_frame_and_deduplicates_doi(tmp_path: Path) -> None:
    rows = [_row(f"Q{i}", str(i), f"Title {i}", 2020 + (i % 5)) for i in range(1, 9)]
    rows.append(_row("Q2", "dup", "Different title formatting", 2021, "https://doi.org/10.1/test"))
    rows.append(_row("Q3", "dup2", "Same work", 2021, "10.1/test"))
    path = tmp_path / "raw.csv"
    _write(path, rows)

    frame, receipt = build([path])
    assert receipt["input_rows"] == 10
    assert receipt["unique_bibliographic_records"] == 9
    assert receipt["duplicate_rows_collapsed"] == 1
    assert receipt["outcome_direction_coded"] is False
    assert receipt["formal_recurrence_result_open"] is False
    assert receipt["primary_standardized_network_k"] == 2
    assert any(row["doi"] == "10.1/test" and row["raw_rows_collapsed"] == "2" for row in frame)


def test_requires_all_frozen_queries(tmp_path: Path) -> None:
    path = tmp_path / "raw.csv"
    _write(path, [_row("Q1", "1", "Only one query", 2020)])
    with pytest.raises(ValueError, match="BIB_FRAME_MISSING_FROZEN_QUERIES"):
        build([path])


def test_rejects_out_of_window_year(tmp_path: Path) -> None:
    rows = [_row(f"Q{i}", str(i), f"Title {i}", 2020) for i in range(1, 9)]
    rows[0]["year"] = "1999"
    path = tmp_path / "raw.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="BIB_FRAME_YEAR_OUT_OF_RANGE"):
        build([path])


def test_rejects_unknown_query_id(tmp_path: Path) -> None:
    rows = [_row(f"Q{i}", str(i), f"Title {i}", 2020) for i in range(1, 9)]
    rows[0]["query_id"] = "Q9"
    path = tmp_path / "raw.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="BIB_FRAME_INVALID_QUERY_ID"):
        build([path])
