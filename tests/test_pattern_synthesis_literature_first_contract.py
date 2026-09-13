from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / "docs" / "THEORY_TO_REALITY_PATTERN_RECOVERY_V1.md"
CONCORDANCE = ROOT / "docs" / "THREE_CHAPTER_PATTERN_SYNTHESIS_CONCORDANCE_V1.md"
PROMOTION = ROOT / "empirical" / "mechanism_pattern_synthesis" / "BITA_META_ANALYSIS_PROMOTION_RULE_V1.md"
REGISTRY = ROOT / "empirical" / "mechanism_pattern_synthesis" / "BITA_QUANTITATIVE_LANE_REGISTRY_V1.csv"
COMPLETION = ROOT / "empirical" / "mechanism_pattern_synthesis" / "COMPLETION_STATUS_V2.md"


def test_current_pattern_universe_is_the_primary_empirical_spine() -> None:
    recovery = RECOVERY.read_text(encoding="utf-8")
    completion = COMPLETION.read_text(encoding="utf-8")
    assert "56 directional route records from 25 independent biological clusters" in recovery
    assert "Fourteen clusters contain more than one route" in recovery
    assert "17 show context- or state-dependent switching" in recovery
    assert "17 high-information systems" in recovery
    assert "route-ledger records:               56" in completion
    assert "independent biological clusters:    25" in completion
    assert "same-system multi-route clusters:   14" in completion
    assert "context/sign-switch clusters:       17" in completion


def test_route_meta_analysis_is_not_promoted_to_mechanism_allocation() -> None:
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        rows = {row["lane_id"]: row for row in csv.DictReader(handle)}
    assert len(rows) == 5
    assert rows["BITA_Q1_larceny_female"]["independent_clusters"] == "48"
    assert rows["BITA_Q2_larceny_visitation"]["independent_clusters"] == "22"
    assert rows["BITA_Q3_larceny_reward"]["independent_clusters"] == "28"
    assert float(rows["BITA_Q1_larceny_female"]["pooled_effect"]) < 0
    assert float(rows["BITA_Q2_larceny_visitation"]["pooled_effect"]) < 0
    assert float(rows["BITA_Q3_larceny_reward"]["pooled_effect"]) < 0
    assert float(rows["BITA_Q4_larceny_male"]["ci_low"]) < 0 < float(rows["BITA_Q4_larceny_male"]["ci_high"])
    strict = rows["BITA_Q5_complete_mechanism_allocation"]
    assert strict["independent_clusters"] == "0"
    assert strict["analysis_status"] == "NOT_AVAILABLE"


def test_promotion_rule_keeps_identification_fail_closed() -> None:
    text = PROMOTION.read_text(encoding="utf-8")
    assert "Route-level pooling does not identify the ecological allocation of a trait interaction" in text
    assert "An unmeasured residual is not called joint cost by subtraction" in text
    assert "conditional on that admission" in text
    assert "not an unbiased mean across all design-eligible systems" in text
    assert "The focal experiment is not the empirical entry point" in text


def test_three_paper_order_places_focal_experiments_last() -> None:
    text = CONCORDANCE.read_text(encoding="utf-8")
    assert "SCH" in text and "BALANCE" in text and "BITA" in text
    assert "design the strongest focal causal experiment last" in text
    assert "A focal experiment is therefore a final identification upgrade" in text
    assert "## Remaining direct-identification gaps" in text
    for heading in ("### SCH final gap", "### BALANCE final gap", "### BITA final gap"):
        assert heading in text


def test_focal_bita_experiment_is_not_a_current_submission_blocker() -> None:
    recovery = RECOVERY.read_text(encoding="utf-8")
    completion = COMPLETION.read_text(encoding="utf-8")
    assert "It is not a prerequisite for the current theory + literature-synthesis paper" in recovery
    assert "Scientific evidence hunting, Pattern saturation, quantitative robustness" in completion
    assert "The remaining blockers are genuinely author/release controlled" in completion
