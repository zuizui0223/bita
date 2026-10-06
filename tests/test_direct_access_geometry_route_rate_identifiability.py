from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAME = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "formal_bibliographic_frame_v2"
)
LEDGER = FRAME / "DIRECT_ACCESS_GEOMETRY_ROUTE_RATE_IDENTIFIABILITY_AUDIT_V1.csv"
SUMMARY = FRAME / "DIRECT_ACCESS_GEOMETRY_ROUTE_RATE_IDENTIFIABILITY_SUMMARY_V1.json"
FREEZE = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "ROUTE_RATE_IDENTIFIABILITY_AUDIT_FREEZE_V1.md"
)

ALLOWED = {
    "ZERO_INCLUSIVE_BOTH_ROUTE_RATES",
    "BOTH_ROUTE_COUNTS_NO_ZERO_INCLUSIVE_DENOMINATOR",
    "CONDITIONAL_ROUTE_CHOICE_ONLY",
    "ROBBERY_PREVALENCE_ONLY",
    "OTHER_ROUTE_RESOLVED_NOT_RATE_IDENTIFIABLE",
    "UNRESOLVED_SOURCE",
}

EXPECTED_STRICT = {
    "Adler_Leege_Irwin_2016",
    "Bhandari_Das_Karmakar_2024",
    "Lara_Ornelas_2001",
    "Newman_Thomson_2005_Linaria",
    "Tie_et_al_2023",
    "Wang_et_al_2013_Impatiens",
    "Wu_Gao_2024_Thunia_alba",
}


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_route_rate_audit_is_frozen_and_complete() -> None:
    assert FREEZE.is_file()
    rows = _rows()
    assert len(rows) == 33
    assert all(row["identifiability_class"] in ALLOWED for row in rows)
    assert all(row["identifiability_class"] != "PENDING" for row in rows)
    assert all(row["source_basis"].strip() for row in rows)
    assert all(row["rationale"].strip() for row in rows)


def test_route_rate_audit_counts_match_frozen_summary() -> None:
    rows = _rows()
    observed = Counter(row["identifiability_class"] for row in rows)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert summary["status"] == "POST_HOC_DESIGN_AUDIT_COMPLETE"
    assert summary["source_frame_programs"] == 33
    assert summary["class_counts"] == dict(sorted(observed.items()))
    assert summary["strict_zero_inclusive_both_route_programs"] == 7
    assert summary["not_strict_zero_inclusive_both_route_programs"] == 26


def test_strict_zero_inclusive_program_set_is_exact() -> None:
    rows = _rows()
    strict = {
        row["program_id"]
        for row in rows
        if row["identifiability_class"] == "ZERO_INCLUSIVE_BOTH_ROUTE_RATES"
    }
    assert strict == EXPECTED_STRICT

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert set(summary["strict_program_ids"]) == EXPECTED_STRICT
    assert abs(summary["strict_zero_inclusive_both_route_fraction"] - 7 / 33) < 1e-15


def test_strict_class_requires_both_routes_and_common_zero_denominator() -> None:
    rows = _rows()
    for row in rows:
        if row["identifiability_class"] != "ZERO_INCLUSIVE_BOTH_ROUTE_RATES":
            continue
        assert row["legitimate_route_separate"] == "YES"
        assert row["robbery_route_separate"] == "YES"
        assert row["zero_interaction_state"] == "YES"
        assert row["common_effort_denominator"] == "YES"


def test_claim_boundary_prevents_prevalence_or_replication_overclaim() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    claim = summary["claim"].lower()
    assert "frozen 33-program" in claim
    assert "7/33" in claim
    assert "post-hoc finite-frame design audit" in claim
    assert "not an estimate of the prevalence" in claim

    boundaries = set(summary["claim_boundaries"])
    assert "does_not_change_effect_direction_counts" in boundaries
    assert "does_not_increment_standardized_network_k" in boundaries
