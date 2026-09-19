from __future__ import annotations

import json
from pathlib import Path

from scripts.run_effective_domain_state_recovery import (
    classify_outcome_family,
    domain_prediction,
    exact_alignment_probability,
    summarize_state_recovery,
)
from trait_architecture.floral_defence_selectivity import load_csv_rows


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "empirical" / "floral_defence_selectivity"


def _row(domain: str, state: str, modality: str, cohort: str = "derivation") -> dict[str, str]:
    return {
        "study_cluster_id": f"{domain}-{state}-{modality}-{cohort}",
        "pre_outcome_domain_code": domain,
        "pollinator_cost_state_derived": state,
        "defence_modality": modality,
        "derivation_or_holdout": cohort,
    }


def test_outcome_family_preserves_null_as_no_interference_detected() -> None:
    assert classify_outcome_family("PRESERVED_OR_IMPROVED") == "NO_INTERFERENCE_OBSERVED"
    assert classify_outcome_family("NO_DETECTED_CHANGE") == "NO_INTERFERENCE_OBSERVED"
    assert classify_outcome_family("MIXED") == "MIXED"
    assert classify_outcome_family("IMPAIRED") == "IMPAIRED"
    assert classify_outcome_family("UNRESOLVED") is None


def test_domain_rule_is_fixed_before_outcome_scoring() -> None:
    assert domain_prediction("SEPARATED") == "NO_INTERFERENCE_OBSERVED"
    assert domain_prediction("TRANSITIONAL") == "MIXED"
    assert domain_prediction("OVERLAPPED") == "IMPAIRED"
    assert domain_prediction("UNCLEAR") is None
    assert domain_prediction("BYPASS_TOLERANCE") is None


def test_exact_perfect_alignment_probability_uses_fixed_margins() -> None:
    # 4 separated / 4 transitional / 1 overlapped with matching outcome counts.
    assert exact_alignment_probability([4, 4, 1]) == 1 / 630
    # 6 separated / 4 transitional / 1 overlapped in the pooled scored set.
    assert exact_alignment_probability([6, 4, 1]) == 1 / 2310


def test_summary_separates_derivation_expansion_and_holdout() -> None:
    rows = [
        _row("SEPARATED", "NO_DETECTED_CHANGE", "chemical"),
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("TRANSITIONAL", "MIXED", "chemical"),
        _row("OVERLAPPED", "IMPAIRED", "chemical"),
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical", "systematic_expansion"),
        _row("SEPARATED", "UNRESOLVED", "physical", "holdout"),
    ]
    result = summarize_state_recovery(rows)

    assert result["derivation"]["scored_n"] == 4
    assert result["derivation"]["domain_rule_correct"] == 4
    assert result["systematic_expansion"]["scored_n"] == 1
    assert result["systematic_expansion"]["domain_rule_correct"] == 1
    assert result["holdout"]["scored_n"] == 0
    assert result["holdout"]["unscored_n"] == 1
    assert result["null_compatible_is_not_equivalence"] is True


def test_current_corpus_state_recovery_is_frozen() -> None:
    rows = load_csv_rows(MODULE / "results" / "analysis_ready_matched_systems.csv")
    result = summarize_state_recovery(rows)

    assert result["derivation"]["scored_n"] == 9
    assert result["derivation"]["domain_rule_correct"] == 9
    assert result["derivation"]["domain_rule_accuracy"] == 1.0
    assert result["derivation"]["exact_perfect_alignment_probability"] == 1 / 630

    assert result["systematic_expansion"]["scored_n"] == 2
    assert result["systematic_expansion"]["domain_rule_correct"] == 2
    assert result["systematic_expansion"]["domain_rule_accuracy"] == 1.0

    assert result["holdout"]["scored_n"] == 0
    assert result["holdout"]["unscored_n"] == 1

    assert result["pooled_scored"]["scored_n"] == 11
    assert result["pooled_scored"]["domain_rule_correct"] == 11
    assert result["pooled_scored"]["exact_perfect_alignment_probability"] == 1 / 2310

    # Coarse modality is a weaker descriptive classifier in the derivation set.
    assert result["derivation"]["modality_loo_correct"] == 6
    assert result["derivation"]["modality_loo_accuracy"] == 6 / 9

    # Using the derivation modality rule prospectively on the two expansion systems:
    # Caryopteris physical is recovered, Phlox chemical is not.
    assert result["systematic_expansion"]["modality_from_derivation_correct"] == 1
    assert result["systematic_expansion"]["modality_from_derivation_accuracy"] == 0.5


def test_committed_result_matches_current_corpus_when_present() -> None:
    result_path = MODULE / "results" / "effective_domain_state_recovery.json"
    if not result_path.exists():
        return
    rows = load_csv_rows(MODULE / "results" / "analysis_ready_matched_systems.csv")
    observed = summarize_state_recovery(rows)
    committed = json.loads(result_path.read_text(encoding="utf-8"))
    assert committed == observed
