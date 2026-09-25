from __future__ import annotations

import csv
import zipfile
from pathlib import Path

import pytest

from scripts.ingest_direct_access_geometry_bibliographic_export_zip import ingest


def _scopus(q: int) -> str:
    return (
        "EID,DOI,Title,Year,Authors,Source title,Link\n"
        f"2-s2.0-{q},,Title {q},202{q % 5},Author {q},Journal {q},https://example/{q}\n"
    )


def _counts() -> str:
    rows = ["query_id,source_db,reported_total_rows,search_date"]
    rows.extend(f"Q{q},Scopus,1,2026-09-25" for q in range(1, 9))
    return "\n".join(rows) + "\n"


def _packet(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for q in range(1, 9):
            zf.writestr(f"Q{q}.csv", _scopus(q))
        zf.writestr("QUERY_COUNTS.csv", _counts())


def test_ingests_one_complete_q1_q8_zip(tmp_path: Path) -> None:
    archive = tmp_path / "exports.zip"
    _packet(archive)
    out = tmp_path / "out"

    result = ingest(
        archive,
        out,
        search_date="2026-09-25",
    )
    assert result["status"] == "Q1_Q8_ZIP_INGESTED_OUTCOME_BLIND"
    assert result["source_db"] == "Scopus"
    assert result["all_query_export_counts_verified"] is True
    assert result["input_rows"] == 8
    assert result["unique_bibliographic_records"] == 8
    assert result["formal_recurrence_result_open"] is False
    assert result["primary_standardized_network_k"] == 2
    assert (
        out / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_ZIP_INTAKE_RECEIPT_V1.json"
    ).exists()


def test_rejects_path_traversal(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("../Q1.csv", _scopus(1))
        for q in range(2, 9):
            zf.writestr(f"Q{q}.csv", _scopus(q))
        zf.writestr("QUERY_COUNTS.csv", _counts())

    with pytest.raises(ValueError, match="BIB_ZIP_UNSAFE_PATH"):
        ingest(archive, tmp_path / "out", search_date="2026-09-25")


def test_rejects_missing_count_manifest(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        for q in range(1, 9):
            zf.writestr(f"Q{q}.csv", _scopus(q))
        zf.writestr("EXTRA.csv", "x\n")

    with pytest.raises(ValueError, match="BIB_ZIP_MISSING_COUNT_MANIFEST"):
        ingest(archive, tmp_path / "out", search_date="2026-09-25")
