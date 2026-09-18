from __future__ import annotations

from trait_architecture.floral_defence_selectivity import registry_key, validate_no_outcome_leakage


def test_registry_key_uses_cluster_axis_and_context() -> None:
    row = {
        "study_cluster_id": "Catalpa_1982",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
    }
    assert registry_key(row) == (
        "Catalpa_1982",
        "nectar_iridoid_glycosides",
        "thieves_vs_legitimate_pollinators",
    )


def test_architecture_rejects_observed_outcome_columns() -> None:
    row = {
        "study_cluster_id": "Catalpa_1982",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
        "pre_outcome_domain_code": "SEPARATED",
        "observed_state_for_validation": "strong_thief_reduction__pollinator_null",
    }
    errors = validate_no_outcome_leakage([row])
    assert any("observed_state_for_validation" in error for error in errors)


def test_architecture_rejects_effect_and_validation_columns() -> None:
    row = {
        "study_cluster_id": "X",
        "D_axis_id": "D",
        "context_id": "C",
        "effect_value": "1.2",
        "validation_result": "PASS",
    }
    errors = validate_no_outcome_leakage([row])
    assert any("effect_value" in error for error in errors)
    assert any("validation_result" in error for error in errors)


def test_clean_architecture_row_has_no_leakage() -> None:
    row = {
        "study_cluster_id": "Catalpa_1982",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
        "pre_outcome_domain_code": "SEPARATED",
        "pre_outcome_basis": "consumer guilds differ in tolerance and exposure",
    }
    assert validate_no_outcome_leakage([row]) == []
