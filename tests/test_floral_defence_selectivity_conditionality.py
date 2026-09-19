from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "floral_defence_selectivity" / "d_side_conditionality_registry.csv"


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def test_d_side_conditionality_registry_contains_eight_independent_clusters() -> None:
    rows = _rows()
    assert len(rows) == 8
    assert len({row["study_cluster_id"] for row in rows}) == 8
    assert all(row["route"].startswith("D_to_") for row in rows)


def test_conditionality_registry_preserves_multiple_mechanistic_axes() -> None:
    axes = {row["macro_axis"] for row in _rows()}
    assert {
        "dose_or_expression",
        "exposure_or_reward_context",
        "consumer_identity",
        "response_stage",
        "temporal_expression",
    }.issubset(axes)


def test_conditionality_rows_trace_back_to_legacy_bita() -> None:
    for row in _rows():
        assert row["legacy_switch_id"].startswith("SS")
        assert row["source_provenance_path"] == (
            "empirical/mechanism_pattern_synthesis/SIGN_SWITCH_LEDGER_V1.csv"
        )
