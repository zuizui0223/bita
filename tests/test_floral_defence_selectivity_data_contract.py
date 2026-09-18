from __future__ import annotations

from trait_architecture.floral_defence_selectivity import (
    validate_architecture_codes,
    validate_outcome_codes,
    validate_registry,
)


def _valid_registry_row() -> dict[str, str]:
    return {
        "study_cluster_id": "Catalpa_1982",
        "publication_id": "Stephenson_1982",
        "plant_taxon": "Catalpa speciosa",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
        "derivation_or_holdout": "derivation",
        "source_provenance_path": "empirical/mechanism_pattern_synthesis/CATALPA_1982_MATCHED_SELECTIVITY_EFFECTS_V1.md",
    }


def _valid_architecture_row() -> dict[str, str]:
    return {
        "study_cluster_id": "Catalpa_1982",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
        "pre_outcome_domain_code": "SEPARATED",
        "separating_coordinate": "susceptibility",
        "defence_modality": "chemical",
        "antagonist_guild": "nectar_thieves",
        "pollinator_guild": "legitimate_bees",
        "observational_or_experimental": "experimental",
        "architecture_basis_path": "empirical/mechanism_pattern_synthesis/CATALPA_1982_NECTAR_DEFENCE_AUDIT_V1.md",
    }


def _valid_outcome_row() -> dict[str, str]:
    return {
        "study_cluster_id": "Catalpa_1982",
        "D_axis_id": "nectar_iridoid_glycosides",
        "context_id": "thieves_vs_legitimate_pollinators",
        "antagonist_outcome_type": "reward_consumption",
        "antagonist_effect_direction": "suppressed",
        "antagonist_uncertainty_class": "DIRECTION_SUPPORTED",
        "pollinator_outcome_type": "reward_consumption",
        "pollinator_response_stage": "consumption",
        "pollinator_effect_direction": "no_detected_change",
        "pollinator_uncertainty_class": "NULL_COMPATIBLE",
        "pollinator_cost_state": "NO_DETECTED_CHANGE",
        "source_supported_preservation": "false",
        "source_inference": "antagonists suppressed; legitimate pollinator consumption null-compatible",
        "outcome_basis_path": "empirical/mechanism_pattern_synthesis/CATALPA_1982_MATCHED_SELECTIVITY_EFFECTS_V1.md",
    }


def test_registry_requires_study_cluster_id() -> None:
    row = _valid_registry_row()
    row.pop("study_cluster_id")
    errors = validate_registry([row])
    assert any("study_cluster_id" in error for error in errors)


def test_architecture_rejects_unknown_domain_code() -> None:
    row = _valid_architecture_row()
    row["pre_outcome_domain_code"] = "MAGIC"
    errors = validate_architecture_codes([row])
    assert any("pre_outcome_domain_code" in error for error in errors)


def test_null_compatible_pollinator_result_cannot_be_promoted_to_preserved() -> None:
    row = _valid_outcome_row()
    row["pollinator_cost_state"] = "PRESERVED_OR_IMPROVED"
    errors = validate_outcome_codes([row])
    assert any("PRESERVED_OR_IMPROVED" in error for error in errors)


def test_source_supported_preservation_can_license_preserved_state() -> None:
    row = _valid_outcome_row()
    row["pollinator_cost_state"] = "PRESERVED_OR_IMPROVED"
    row["source_supported_preservation"] = "true"
    errors = validate_outcome_codes([row])
    assert errors == []


def test_valid_minimal_rows_pass() -> None:
    assert validate_registry([_valid_registry_row()]) == []
    assert validate_architecture_codes([_valid_architecture_row()]) == []
    assert validate_outcome_codes([_valid_outcome_row()]) == []


def test_registry_accepts_systematic_expansion_cohort() -> None:
    row = _valid_registry_row()
    row["derivation_or_holdout"] = "systematic_expansion"
    assert validate_registry([row]) == []
