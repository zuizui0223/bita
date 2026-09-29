from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAME = ROOT / "empirical" / "floral_defence_selectivity" / "formal_bibliographic_frame_v2"
AUDIT = FRAME / "DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_AUDIT_V1.csv"
NOTE = FRAME / "DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_AUDIT_V1.md"
SUMMARY = FRAME / "DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1.json"
BOUNDARY_SUMMARY = FRAME / "DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_SUMMARY_V1.json"


def _rows():
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_boundary_audit_covers_exact_nonpositive_programs() -> None:
    rows = _rows()
    assert len(rows) == 6
    assert sum(row["direction"] == "OPPOSITE" for row in rows) == 4
    assert sum(row["direction"] == "MIXED" for row in rows) == 2
    assert len({row["program_id"] for row in rows}) == 6


def test_direct_bypass_hardening_is_not_overgeneralized() -> None:
    rows = _rows()
    direct = [row for row in rows if row["mechanism_code"] == "BYPASS_HARDENED_DIRECT"]
    assert {row["program_id"] for row in direct} == {
        "Wu_Gao_2024_Thunia_alba",
        "Hattori_Nagano_Itino_2015_Meehania",
    }
    assert all(row["direction"] == "OPPOSITE" for row in direct)

    note = NOTE.read_text(encoding="utf-8")
    assert "post hoc mechanistic audit" in note
    assert "not a preregistered or independently" in note
    assert "the theory predicts all reversals" in note
    assert "all 33 programs" in note


def test_formal_search_added_disproportionately_more_reverse_cases_descriptively() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["preexisting_direct_programs_recovered"] == 23
    assert summary["new_eligible_programs_from_formal_frame"] == 10
    assert summary["direction_counts"]["OPPOSITE"] == 4
    assert summary["new_eligible_direction_counts"]["OPPOSITE"] == 3
    preexisting_opposite = (
        summary["direction_counts"]["OPPOSITE"]
        - summary["new_eligible_direction_counts"]["OPPOSITE"]
    )
    assert preexisting_opposite == 1


def test_boundary_summary_freezes_descriptive_claim_ceiling() -> None:
    summary = json.loads(BOUNDARY_SUMMARY.read_text(encoding="utf-8"))
    assert summary["audited_nonpositive_programs"] == 6
    assert summary["opposite_mechanism_partition"]["BYPASS_HARDENED_DIRECT"] == 2
    assert summary["formal_search_asymmetry"]["preexisting_opposite_programs"] == 1
    assert summary["formal_search_asymmetry"]["new_opposite_programs"] == 3
    assert summary["formal_search_asymmetry"]["inference"] == "DESCRIPTIVE_ONLY_NO_BIAS_TEST"
    assert "cannot estimate predictive accuracy" in summary["claim_boundary"]
