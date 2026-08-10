from __future__ import annotations

import math

import pytest

from trait_architecture.empirical_leverage import (
    cost_from_log_response_ratio,
    evaluate_interval,
    leverage_grid,
    load_config,
    required_precision,
    sign_boundary,
)
from trait_architecture.model import Architecture, InteractionRegime, ModelParameters, fitness


CONFIG = load_config("configs/part_i_robustness_grid.json")


def mixed_partial(a: float, d: float, r: float, p: float, h: float, params: ModelParameters) -> float:
    """Independent finite-difference mixed partial of the declared score surface."""

    eps = 1e-5

    def w(attraction: float, defence: float) -> float:
        return fitness(Architecture(attraction, defence, r), InteractionRegime(p, h), params).total

    return (w(a + eps, d + eps) - w(a + eps, d - eps) - w(a - eps, d + eps) + w(a - eps, d - eps)) / (4 * eps * eps)


def test_closed_form_boundary_matches_finite_difference_sign_everywhere_tested() -> None:
    """The boundary is derived analytically; this checks it against the model itself."""

    mismatches = []
    for cost in (0.05, 0.2, 0.45, 0.9, 2.0, 5.0, 12.0):
        params = ModelParameters(defence_pollinator_cost=cost)
        for defence in (0.2, 0.5, 0.8):
            for assurance in (0.0, 0.5):
                for service in (0.2, 0.5, 0.8):
                    for pressure in (0.2, 0.5, 0.8):
                        boundary = sign_boundary(
                            Architecture(0.5, defence, assurance),
                            InteractionRegime(service, pressure),
                            params,
                        )
                        predicted = boundary.is_complementary(cost)
                        actual = mixed_partial(0.5, defence, assurance, service, pressure, params) > 0
                        if predicted != actual:
                            mismatches.append((cost, defence, assurance, service, pressure))
    assert not mismatches


def test_boundary_recovers_the_two_sided_window_of_the_corollary() -> None:
    """A large enough pollinator cost shuts the mutualist channel off and the
    interaction returns to complementary. That upper branch is a property of the
    exponential access term, so it is reported rather than truncated away."""

    params = ModelParameters(
        attraction_tracking=1.1, floral_defence_efficacy=0.75,
        attraction_defence_shared_cost=0.10, attraction_gain=1.2,
    )
    boundary = sign_boundary(Architecture(0.5, 0.8, 0.0), InteractionRegime(0.8, 0.5), params)

    assert boundary.boundary_type == "two_sided_window"
    assert 0 < boundary.lower < boundary.upper
    assert boundary.is_complementary(boundary.lower * 0.5)
    assert not boundary.is_complementary(0.5 * (boundary.lower + boundary.upper))
    assert boundary.is_complementary(boundary.upper * 1.5)


def test_extreme_regimes_are_insensitive_to_the_measured_parameter() -> None:
    high_relief = sign_boundary(
        Architecture(0.5, 0.2, 0.0), InteractionRegime(0.2, 0.8),
        ModelParameters(attraction_tracking=1.6, floral_defence_efficacy=0.9,
                        attraction_defence_shared_cost=0.03),
    )
    assert high_relief.boundary_type == "always_complementary"

    high_cost = sign_boundary(
        Architecture(0.5, 0.5, 0.0), InteractionRegime(0.8, 0.2),
        ModelParameters(attraction_tracking=0.8, floral_defence_efficacy=0.6,
                        attraction_defence_shared_cost=0.25),
    )
    assert high_cost.boundary_type == "always_substitutable"
    assert not high_cost.is_complementary(0.0)


def test_cost_recovery_from_an_oriented_route_effect() -> None:
    assert math.isclose(cost_from_log_response_ratio(-0.60, 0.5), 1.2, rel_tol=1e-12)
    # A positive route effect falsifies the orientation gate; it is clamped to
    # zero rather than reported as a negative pollinator cost.
    assert cost_from_log_response_ratio(0.40, 0.5) == 0.0
    with pytest.raises(ValueError, match="trait_contrast must be positive"):
        cost_from_log_response_ratio(-0.6, 0.0)


def test_interval_verdicts_separate_settled_from_unsettled_points() -> None:
    boundary = sign_boundary(
        Architecture(0.5, 0.5, 0.0), InteractionRegime(0.5, 0.5), ModelParameters()
    )
    assert boundary.boundary_type == "two_sided_window"
    inside = 0.5 * (boundary.lower + boundary.upper)

    _, _, straddling = evaluate_interval(boundary, boundary.lower * 0.5, inside)
    assert straddling == "unsettled_interval_spans_boundary"

    _, _, settled = evaluate_interval(boundary, inside * 0.9, inside * 1.1)
    assert settled == "settled_substitutable"

    with pytest.raises(ValueError, match="interval_low must not exceed"):
        evaluate_interval(boundary, 1.0, 0.5)


def test_interval_spanning_the_whole_window_is_not_reported_as_settled() -> None:
    """Both endpoints agree here, but the sign flips twice in between."""

    boundary = sign_boundary(
        Architecture(0.5, 0.5, 0.0), InteractionRegime(0.5, 0.5), ModelParameters()
    )
    _, _, verdict = evaluate_interval(boundary, boundary.lower * 0.5, boundary.upper * 2.0)

    assert verdict == "unsettled_interval_spans_boundary"


def test_leverage_grid_omits_the_attraction_axis_and_covers_every_scenario() -> None:
    rows, summaries = leverage_grid(CONFIG, 0.2, 0.7)

    grid = CONFIG["phenotype_and_regime_grid"]
    expected = (
        len(CONFIG["parameter_scenarios"]) * len(grid["defence"]) * len(grid["assurance"])
        * len(grid["pollinator_service"]) * len(grid["floral_damage_pressure"])
    )
    assert len(rows) == expected
    assert "attraction" not in rows[0]
    assert len(summaries) == len(CONFIG["parameter_scenarios"])
    for summary in summaries:
        counted = (
            summary["settled_complementary"] + summary["settled_substitutable"]
            + summary["unsettled_by_interval"] + summary["always_substitutable"]
            + summary["always_complementary"]
        )
        assert counted == summary["grid_points"]


def test_tighter_intervals_never_settle_fewer_points() -> None:
    rows = required_precision(CONFIG, centre=0.45)
    fractions = [float(row["settled_fraction"]) for row in rows]

    assert rows[0]["half_width"] == "0.05"
    assert all(earlier >= later for earlier, later in zip(fractions, fractions[1:]))
