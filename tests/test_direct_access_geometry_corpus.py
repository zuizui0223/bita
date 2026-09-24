from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.summarize_direct_access_geometry_corpus import (
    DEFAULT_CORPUS,
    REQUIRED_COLUMNS,
    summarize,
)


def test_committed_direct_corpus_is_support_only_and_does_not_change_k() -> None:
    result = summarize(DEFAULT_CORPUS)
    assert result["status"] == "DISCOVERY_SUPPORT_ONLY_NOT_NETWORK_K"
    assert result["study_programs"] == 23
    assert result["direction_counts"] == {
        "POSITIVE": 15,
        "NULL": 5,
        "OPPOSITE": 1,
        "MIXED": 2,
    }
    assert result["network_k_contribution"] == 0
    assert result["primary_joint_network_k_remains"] == 2
    assert result["formal_recurrence_test_permitted"] is False


def test_validator_rejects_attempt_to_promote_discovery_row_into_network_k(
    tmp_path: Path,
) -> None:
    row = {key: "x" for key in REQUIRED_COLUMNS}
    row.update(
        {
            "study_id": "example",
            "year": "2026",
            "direction": "POSITIVE",
            "network_k_eligible": "YES",
            "reason_not_k": "none",
        }
    )
    path = tmp_path / "corpus.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(row)

    with pytest.raises(ValueError, match="DIRECT_CORPUS_CANNOT_PROMOTE_NETWORK_K"):
        summarize(path)


def test_validator_rejects_invalid_direction(tmp_path: Path) -> None:
    row = {key: "x" for key in REQUIRED_COLUMNS}
    row.update(
        {
            "study_id": "example",
            "year": "2026",
            "direction": "SUPPORTIVE",
            "network_k_eligible": "NO",
            "reason_not_k": "not a network",
        }
    )
    path = tmp_path / "corpus.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(row)

    with pytest.raises(ValueError, match="DIRECT_CORPUS_INVALID_DIRECTION"):
        summarize(path)
