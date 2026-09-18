from __future__ import annotations

import json
from pathlib import Path

from scripts.run_floral_defence_selectivity_models import summarize_stage2_model_gate
from trait_architecture.floral_defence_selectivity import load_csv_rows


def _row(domain: str, state: str, modality: str) -> dict[str, str]:
    return {
        "study_cluster_id": f"{domain}-{state}-{modality}",
        "defence_efficacy_state": "EFFECTIVE",
        "pre_outcome_domain_code": domain,
        "pollinator_cost_state_derived": state,
        "defence_modality": modality,
    }


def test_strict_gate_uses_only_direction_supported_stage2_states() -> None:
    rows = [
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("OVERLAPPED", "IMPAIRED", "chemical"),
        _row("SEPARATED", "NO_DETECTED_CHANGE", "chemical"),
        _row("TRANSITIONAL", "MIXED", "chemical"),
    ]

    result = summarize_stage2_model_gate(rows)

    assert result["strict_stage2_n"] == 3
    assert result["strict_table"] == {
        "SEPARATED": {"compatible": 2, "impaired": 0},
        "OVERLAPPED": {"compatible": 0, "impaired": 1},
    }
    assert result["strict_fisher_two_sided_p"] == 1 / 3
    assert result["model_decision"] == "DESCRIPTIVE_EXACT_ONLY"


def test_null_compatible_rows_enter_sensitivity_not_strict_table() -> None:
    rows = [
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("SEPARATED", "NO_DETECTED_CHANGE", "chemical"),
        _row("SEPARATED", "NO_DETECTED_CHANGE", "physical"),
        _row("SEPARATED", "NO_DETECTED_CHANGE", "reward_access"),
        _row("SEPARATED", "NO_DETECTED_CHANGE", "chemical"),
        _row("OVERLAPPED", "IMPAIRED", "chemical"),
    ]

    result = summarize_stage2_model_gate(rows)

    assert result["strict_stage2_n"] == 3
    assert result["compatibility_sensitivity_n"] == 7
    assert result["compatibility_sensitivity_table"]["SEPARATED"]["compatible_or_null"] == 6
    assert result["compatibility_sensitivity_fisher_two_sided_p"] == 1 / 7
    assert result["null_compatible_is_not_equivalence"] is True


def test_strict_domain_modality_confounding_blocks_competing_model_claim() -> None:
    rows = [
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("SEPARATED", "PRESERVED_OR_IMPROVED", "physical"),
        _row("OVERLAPPED", "IMPAIRED", "chemical"),
    ]

    result = summarize_stage2_model_gate(rows)

    assert result["strict_domain_modality_confounding"] == "PERFECT_IN_CURRENT_STRICT_SET"
    assert result["can_compare_domain_vs_modality"] is False


def test_committed_stage2_gate_matches_current_analysis_ready_data() -> None:
    root = Path(__file__).resolve().parents[1]
    module = root / "empirical" / "floral_defence_selectivity"
    rows = load_csv_rows(module / "results" / "analysis_ready_matched_systems.csv")
    expected = summarize_stage2_model_gate(rows)
    committed = json.loads(
        (module / "results" / "stage2_model_gate.json").read_text(encoding="utf-8")
    )
    assert committed == expected
    assert expected["strict_stage2_n"] == 3
    assert expected["model_decision"] == "DESCRIPTIVE_EXACT_ONLY"
    assert expected["strict_domain_modality_confounding"] == "PERFECT_IN_CURRENT_STRICT_SET"
