import csv

from scripts.validate_part_b_integrity import (
    check_candidates,
    check_coding_queue,
    check_part_b_integrity,
    check_verified_effects,
)

EFFECTS = "empirical/broad_reality_evidence/part_b_arrow_effects.csv"
CANDIDATES = "empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv"
QUEUE = "empirical/broad_reality_evidence/d_A_moderator_coding_queue.csv"


def test_repo_part_b_files_are_clean() -> None:
    assert check_part_b_integrity(EFFECTS, CANDIDATES, QUEUE) == []


def test_candidate_with_effect_size_column_is_flagged(tmp_path) -> None:
    bad = tmp_path / "candidates.csv"
    with bad.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "verification_status", "effect_value"])
        writer.writeheader()
        writer.writerow({"candidate_id": "c1", "verification_status": "candidate_unverified", "effect_value": "0.5"})
    violations = check_candidates(bad)
    assert any("effect_value" in v for v in violations)


def test_candidate_claiming_verified_status_is_flagged(tmp_path) -> None:
    bad = tmp_path / "candidates.csv"
    with bad.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "verification_status"])
        writer.writeheader()
        writer.writerow({"candidate_id": "c1", "verification_status": "verified"})
    violations = check_candidates(bad)
    assert any("verification_status" in v for v in violations)


def test_screened_context_only_candidate_is_allowed_but_remains_non_effect(tmp_path) -> None:
    candidate = tmp_path / "candidates.csv"
    with candidate.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "verification_status", "extraction_todo"])
        writer.writeheader()
        writer.writerow({
            "candidate_id": "c_context_only",
            "verification_status": "candidate_screened_context_only",
            "extraction_todo": "retain as context only; do not extract as d_A",
        })
    assert check_candidates(candidate) == []


def test_queue_blank_level_needs_coding_flag(tmp_path) -> None:
    from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION

    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": "q1", "study_id": "s", "study_cluster_id": "s",
        "route": "A_to_antagonism", "trait_role": "A", "trait_class": "scent",
        "outcome_class": "floral_damage_proportion", "design_class": "observational",
        "effect_input_type": "reported_effect", "effect_metric": "log_odds_ratio",
        "effect_value": "0.3", "standard_error": "0.1", "effect_orientation": ORIENTATION,
        "is_primary_effect": "true", "analysis_status": "eligible_for_quantitative_synthesis",
    })
    row["moderator_variable"] = "pollination_generalization"
    row["moderator_level"] = ""
    row["coding_status"] = "done"
    bad = tmp_path / "queue.csv"
    with bad.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    violations = check_coding_queue(bad)
    assert any("needs_moderator_level_coding" in v for v in violations)


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
