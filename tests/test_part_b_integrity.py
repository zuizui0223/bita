import csv

from scripts.validate_part_b_integrity import check_verified_effects

EFFECTS = "empirical/broad_reality_evidence/part_b_arrow_effects.csv"


def test_repo_part_b_effects_are_clean() -> None:
    assert check_verified_effects(EFFECTS) == []


def test_verified_effects_reject_candidate_basis(tmp_path) -> None:
    from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION

    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": "e1", "study_id": "s", "study_cluster_id": "s",
        "route": "A_to_antagonism", "trait_role": "A", "trait_class": "scent",
        "outcome_class": "floral_damage_proportion", "design_class": "observational",
        "effect_input_type": "reported_effect", "effect_metric": "log_odds_ratio",
        "effect_value": "0.3", "standard_error": "0.1", "effect_orientation": ORIENTATION,
        "is_primary_effect": "true", "analysis_status": "eligible_for_quantitative_synthesis",
        "source_basis": "candidate_unverified_lead", "source_locator": "doi:x",
    })
    bad = tmp_path / "effects.csv"
    with bad.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    violations = check_verified_effects(bad)
    assert any("unverified/candidate basis" in v for v in violations)


def test_verified_effects_require_source_locator(tmp_path) -> None:
    from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION

    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": "e2", "study_id": "s", "study_cluster_id": "s",
        "route": "B_to_pollination", "trait_role": "B", "trait_class": "chemistry",
        "outcome_class": "pollinator_visitation", "design_class": "observational",
        "effect_input_type": "reported_effect", "effect_metric": "log_rate_ratio",
        "effect_value": "-0.2", "standard_error": "0.1", "effect_orientation": ORIENTATION,
        "is_primary_effect": "true", "analysis_status": "eligible_for_quantitative_synthesis",
        "source_basis": "reported_model_table", "source_locator": "",
    })
    bad = tmp_path / "effects.csv"
    with bad.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    violations = check_verified_effects(bad)
    assert any("source_locator" in v for v in violations)
