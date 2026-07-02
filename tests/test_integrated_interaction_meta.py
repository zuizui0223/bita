import math

import pytest

from trait_architecture.integrated_interaction_meta import (
    IntegratedInteractionMetaError,
    build_balance_dashboard,
    build_candidate_ledger,
    harmonize_effect_rows,
    make_effect_ledger,
)


def candidate(candidate_id, routes):
    return {
        "candidate_id": candidate_id,
        "doi": f"10.test/{candidate_id}",
        "title": candidate_id,
        "publication_year": "2024",
        "work_type": "journal-article",
        "container_title": "Test Journal",
        "publisher": "Test Publisher",
        "route_memberships": routes,
        "source_bucket": "empirical_nonreview",
        "screening_priority": "tier_1_direct_effect_candidate",
        "crossref_abstract_text": "A test abstract.",
        "full_text_screen_status": "unreviewed",
        "full_text_screen_note": "",
        "source_queries": "test",
    }


def included_effect(
    metric="hedges_g",
    estimate="0.5",
    variance="0.04",
    *,
    route="A_to_pollinator",
    outcome="consumer_use",
    design="direct_experiment",
    effect_id="effect_1",
):
    trait, partner = {
        "A_to_pollinator": ("A_flower", "pollinator"),
        "A_to_antagonist": ("A_flower", "floral_antagonist"),
        "B_to_antagonist": ("B_flower", "floral_antagonist"),
        "B_to_pollinator": ("B_flower", "pollinator"),
    }[route]
    return {
        "candidate_route_id": f"candidate::{route}",
        "candidate_id": "candidate",
        "doi": "10.test/candidate",
        "title": "candidate",
        "study_id": "study_1",
        "independent_study_id": "panel_1",
        "effect_id": effect_id,
        "species": "Testus floralis",
        "trait_role": trait,
        "partner_role": partner,
        "route": route,
        "trait_name": "test trait",
        "mechanism_class": "chemical",
        "organ_match": "nectar",
        "trait_contrast_or_predictor": "high vs low",
        "outcome_construct": outcome,
        "study_design": design,
        "dose_relation": "within_natural_range",
        "consumer_specialization": "unknown",
        "alternative_resource_context": "unknown",
        "source_effect_metric": metric,
        "source_effect_estimate": estimate,
        "source_effect_variance": variance,
        "sample_size_total": "40",
        "direction_is_higher_trait": "true",
        "full_text_inclusion": "included",
        "source_locator": "p. 3",
        "extractor_id": "test",
        "extraction_note": "",
        "is_primary_effect": "true",
        "harmonization_status": "",
        "harmonization_method": "",
        "common_effect_fisher_z": "",
        "common_effect_variance": "",
        "metric_specific_analysis_lane": "",
        "model_inclusion_status": "",
        "exclusion_reason": "",
        "effect_boundary": "",
    }


def test_candidate_ledger_keeps_all_four_channels_in_one_table():
    ledger = build_candidate_ledger([
        candidate("both", "A_to_pollinator;B_to_pollinator"),
        candidate("enemy", "A_to_antagonist;B_to_antagonist"),
    ])
    assert len(ledger) == 4
    assert {(row["trait_role"], row["partner_role"]) for row in ledger} == {
        ("A_flower", "pollinator"),
        ("B_flower", "pollinator"),
        ("A_flower", "floral_antagonist"),
        ("B_flower", "floral_antagonist"),
    }
    blank = make_effect_ledger(ledger)
    assert len(blank) == 4
    assert {row["full_text_inclusion"] for row in blank} == {"pending_full_text"}


def test_common_scale_conversions_are_documented_and_positive_variance():
    g = harmonize_effect_rows([included_effect("hedges_g")])[0]
    assert g["harmonization_status"] == "common_scale_ready"
    assert g["harmonization_method"] == "fisher_z_from_hedges_g"
    assert float(g["common_effect_fisher_z"]) > 0
    assert float(g["common_effect_variance"]) > 0

    odds = harmonize_effect_rows([included_effect("log_odds_ratio", estimate="0.7", effect_id="effect_2")])[0]
    assert odds["harmonization_method"] == "fisher_z_from_log_odds_ratio_via_standardized_mean_difference"
    assert math.isfinite(float(odds["common_effect_fisher_z"]))

    correlation = harmonize_effect_rows([included_effect("correlation_r", estimate="0.3", variance="0.02", effect_id="effect_3")])[0]
    assert correlation["harmonization_method"] == "fisher_z_from_correlation_r"


def test_log_ratios_stay_in_master_ledger_without_forced_conversion():
    row = harmonize_effect_rows([included_effect("log_response_ratio")])[0]
    assert row["harmonization_status"] == "native_metric_retained"
    assert row["model_inclusion_status"] == "metric_specific_layer"
    assert row["common_effect_fisher_z"] == ""


def test_dashboard_distinguishes_candidate_capacity_from_numeric_effects():
    candidates = build_candidate_ledger([
        candidate("ap", "A_to_pollinator"),
        candidate("bp", "B_to_pollinator"),
    ])
    dashboard = build_balance_dashboard(candidates, [included_effect()])
    by_route = {row["route"]: row for row in dashboard}
    assert by_route["A_to_pollinator"]["candidate_route_rows"] == "1"
    assert by_route["A_to_pollinator"]["common_scale_effect_rows"] == "1"
    assert by_route["B_to_pollinator"]["candidate_route_rows"] == "1"
    assert by_route["B_to_pollinator"]["common_scale_effect_rows"] == "0"


def test_included_effect_cannot_reverse_the_shared_orientation():
    bad = included_effect()
    bad["direction_is_higher_trait"] = "false"
    with pytest.raises(IntegratedInteractionMetaError):
        harmonize_effect_rows([bad])
