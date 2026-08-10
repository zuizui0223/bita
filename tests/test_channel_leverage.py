from __future__ import annotations

import math

import pytest

from trait_architecture.channel_leverage import (
    DECLARED_PRIOR_RANGES,
    GridPoint,
    channel_leverage,
    rank_parameters,
    sign_change_points,
)
from trait_architecture.empirical_leverage import load_config, sign_boundary
from trait_architecture.model import Architecture, InteractionRegime, ModelParameters
from trait_architecture.robustness import BASELINE_FORM, RobustnessCase, default_functional_forms


CONFIG = load_config("configs/part_i_robustness_grid.json")


def baseline_point(defence: float, service: float, pressure: float, assurance: float = 0.0) -> GridPoint:
    return GridPoint(
        RobustnessCase(
            case_id="case",
            attraction=0.5,
            defence=defence,
            assurance=assurance,
            pollinator_service=service,
            floral_damage_pressure=pressure,
        ),
        BASELINE_FORM,
    )


def test_root_search_agrees_with_the_independent_closed_form_boundary() -> None:
    """Two modules derive the c_D boundary differently; they must agree.

    ``empirical_leverage`` solves it analytically for the baseline corollary;
    this module finds it by scanning the deployed mixed partial. Agreement is a
    check on both.
    """

    low, high = DECLARED_PRIOR_RANGES["defence_pollinator_cost"]
    for defence in (0.2, 0.5, 0.8):
        for service in (0.2, 0.5, 0.8):
            for pressure in (0.2, 0.5, 0.8):
                point = baseline_point(defence, service, pressure)
                roots = sign_change_points(
                    point, ModelParameters(), "defence_pollinator_cost", low, high
                )
                closed = sign_boundary(
                    Architecture(0.5, defence, 0.0),
                    InteractionRegime(service, pressure),
                    ModelParameters(),
                )
                expected = [
                    value for value in (closed.lower, closed.upper)
                    if value is not None and low < value < high
                ]
                assert len(roots) == len(expected), (defence, service, pressure)
                for found, predicted in zip(sorted(roots), sorted(expected)):
                    assert math.isclose(found, predicted, rel_tol=1e-6, abs_tol=1e-9)


def test_root_search_recovers_both_sides_of_a_two_sided_window() -> None:
    point = baseline_point(0.8, 0.8, 0.5)
    roots = sign_change_points(point, ModelParameters(), "defence_pollinator_cost", 0.0, 3.0)

    assert len(roots) == 2
    assert roots[0] < roots[1]


def test_unknown_parameter_and_empty_range_are_rejected() -> None:
    with pytest.raises(ValueError, match="no declared prior range"):
        channel_leverage(CONFIG, parameters_of_interest=["not_a_parameter"])
    with pytest.raises(ValueError, match="prior range must be increasing"):
        sign_change_points(baseline_point(0.5, 0.5, 0.5), ModelParameters(), "attraction_gain", 1.0, 1.0)


def test_leverage_rows_are_internally_consistent() -> None:
    config = {**CONFIG, "parameter_scenarios": CONFIG["parameter_scenarios"][1:2]}
    rows = channel_leverage(
        config,
        parameters_of_interest=["attraction_tracking", "defence_pollinator_cost"],
        relative_half_widths=(0.25,),
        forms=list(default_functional_forms())[:1],
    )

    assert len(rows) == 2
    for row in rows:
        total = int(row["grid_points"])
        assert 0 <= int(row["settled_points"]) <= total
        assert 0 <= int(row["prior_sensitive_points"]) <= total
        insensitive = (total - int(row["prior_sensitive_points"])) / total
        expected = max(0.0, float(row["settled_fraction"]) - insensitive)
        # Both fields are written rounded to six decimals.
        assert math.isclose(float(row["value_of_information"]), expected, abs_tol=1e-6)


def test_wider_intervals_never_settle_more_points() -> None:
    config = {**CONFIG, "parameter_scenarios": CONFIG["parameter_scenarios"][1:2]}
    rows = channel_leverage(
        config,
        parameters_of_interest=["defence_pollinator_cost"],
        relative_half_widths=(0.10, 0.25, 0.50),
        forms=list(default_functional_forms())[:1],
    )
    fractions = [float(row["settled_fraction"]) for row in rows]

    assert all(earlier >= later for earlier, later in zip(fractions, fractions[1:]))


def test_ranking_orders_by_value_of_information_and_assigns_dense_ranks() -> None:
    config = {**CONFIG, "parameter_scenarios": CONFIG["parameter_scenarios"][1:2]}
    rows = channel_leverage(
        config, relative_half_widths=(0.25,), forms=list(default_functional_forms())[:1]
    )
    ranking = rank_parameters(rows, 0.25)

    scores = [float(row["value_of_information"]) for row in ranking]
    assert scores == sorted(scores, reverse=True)
    assert [row["rank"] for row in ranking] == list(range(1, len(ranking) + 1))
    assert {row["parameter"] for row in ranking} == set(DECLARED_PRIOR_RANGES)


def test_ranking_requires_a_half_width_present_in_the_rows() -> None:
    config = {**CONFIG, "parameter_scenarios": CONFIG["parameter_scenarios"][1:2]}
    rows = channel_leverage(
        config,
        parameters_of_interest=["attraction_gain"],
        relative_half_widths=(0.25,),
        forms=list(default_functional_forms())[:1],
    )

    with pytest.raises(ValueError, match="no rows at relative half-width"):
        rank_parameters(rows, 0.9)
