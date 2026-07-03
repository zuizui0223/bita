import pytest

from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION
from trait_architecture.model import ModelParameters
from trait_architecture.part_b_arrow_evidence import (
    arrow_regime_leverage,
    prioritise_arrows,
    synthesise_arrow_evidence,
)
from trait_architecture.robustness import cartesian_cases


def _row(effect_id, cluster, route, role, trait_class, outcome_class, metric, value, design="observational"):
    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": effect_id,
        "study_id": cluster,
        "study_cluster_id": cluster,
        "route": route,
        "trait_role": role,
        "trait_class": trait_class,
        "outcome_class": outcome_class,
        "design_class": design,
        "effect_input_type": "reported_effect",
        "effect_metric": metric,
        "effect_value": str(value),
        "standard_error": "0.2",
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "true",
        "analysis_status": "eligible_for_quantitative_synthesis",
    })
    return row


def _cross_stratum_d_A_rows():
    # The current Impatiens vs Gymnadenia situation: opposite signs, but different
    # trait and metric strata. This is heterogeneity, not a direct sign conflict.
    return [
        _row("dA1", "impatiens", "A_to_antagonism", "A", "visual_signal", "floral_damage_proportion", "standardized_beta", -0.1),
        _row("dA2", "gymnadenia", "A_to_antagonism", "A", "scent", "floral_damage_proportion", "log_odds_ratio", 0.57),
        _row("eF1", "impatiens", "B_to_antagonism", "B", "chemical_barrier", "floral_damage_proportion", "standardized_beta", 0.09),
    ]


def _within_stratum_conflict_rows():
    return [
        _row("dA1", "study-1", "A_to_antagonism", "A", "visual_signal", "floral_damage_proportion", "standardized_beta", -0.1),
        _row("dA2", "study-2", "A_to_antagonism", "A", "visual_signal", "floral_damage_proportion", "standardized_beta", 0.2),
    ]


def test_cross_stratum_opposition_is_heterogeneity_not_sign_conflict() -> None:
    evidence = synthesise_arrow_evidence(_cross_stratum_d_A_rows())
    d_a = evidence["A_to_antagonism"]
    assert d_a.independent_clusters == 2
    assert d_a.positive_signs == 1 and d_a.negative_signs == 1
    assert d_a.distinct_strata == 2
    assert d_a.sign_state == "cross_stratum_heterogeneity"
    assert d_a.mixed_partial_role == "complementarity_driver"

    e_f = evidence["B_to_antagonism"]
    assert e_f.sign_state == "single_anchor"
    assert e_f.clusters_needed_to_pool == 2

    absent = evidence["A_to_pollination"]
    assert absent.sign_state == "absent"
    assert absent.clusters_needed_to_pool == 3


def test_opposite_signs_in_same_compatibility_stratum_are_a_conflict() -> None:
    evidence = synthesise_arrow_evidence(_within_stratum_conflict_rows())
    d_a = evidence["A_to_antagonism"]
    assert d_a.distinct_strata == 1
    assert d_a.sign_state == "within_stratum_conflict"


def test_regime_leverage_positive_for_tracking() -> None:
    cases = cartesian_cases(
        attraction=(0.2, 0.5, 0.8),
        defence=(0.2, 0.5, 0.8),
        assurance=(0.0,),
        pollinator_service=(0.2, 0.5, 0.8),
        floral_damage_pressure=(0.2, 0.5, 0.8),
    )
    envelopes = {
        "low": {"attraction_gain": 1.2, "attraction_tracking": 0.4, "floral_defence_efficacy": 0.5, "defence_pollinator_cost": 0.6},
        "baseline": {"attraction_gain": 1.2, "attraction_tracking": 1.1, "floral_defence_efficacy": 0.75, "defence_pollinator_cost": 0.45},
        "high": {"attraction_gain": 1.2, "attraction_tracking": 1.6, "floral_defence_efficacy": 0.9, "defence_pollinator_cost": 0.3},
    }
    leverage = arrow_regime_leverage(cases, envelopes, shared_cost=0.1)
    # Stronger antagonist tracking (d_A) raises the complementary fraction.
    assert leverage["A_to_antagonism"] > 0
    # b_A is held constant across the envelope, so it has no leverage here.
    assert leverage["A_to_pollination"] == 0.0

    # With a declared range, b_A becomes comparable: more attraction gain feeds the
    # obstruction term, so its leverage is negative (fewer complementary cases).
    ranged = arrow_regime_leverage(
        cases, envelopes, shared_cost=0.1,
        param_ranges={"attraction_gain": (0.6, 1.8)},
    )
    assert ranged["A_to_pollination"] < 0


def test_priority_ranks_heterogeneity_without_calling_a_moderator() -> None:
    evidence = synthesise_arrow_evidence(_cross_stratum_d_A_rows())
    leverage = {
        "A_to_antagonism": 0.66,
        "B_to_antagonism": 0.37,
        "B_to_pollination": -0.22,
        "A_to_pollination": 0.0,
    }
    ranked = prioritise_arrows(evidence, leverage)
    assert ranked[0].route == "A_to_antagonism"
    assert ranked[0].priority_rank == 1
    assert ranked[0].sign_state == "cross_stratum_heterogeneity"
    assert "strata" in ranked[0].recommended_action
    assert "moderator" not in ranked[0].recommended_action
    # Every arrow gets a rank and a carried-through leverage value.
    assert {item.priority_rank for item in ranked} == {1, 2, 3, 4}
    assert ranked[0].regime_leverage == pytest.approx(0.66)


def test_priority_sends_genuine_within_stratum_conflict_to_moderator() -> None:
    evidence = synthesise_arrow_evidence(_within_stratum_conflict_rows())
    ranked = prioritise_arrows(evidence, {route: 0.0 for route in evidence})
    d_a = next(item for item in ranked if item.route == "A_to_antagonism")
    assert d_a.priority_rank == 1
    assert "moderator" in d_a.recommended_action
    assert "within-stratum" in d_a.recommended_action
