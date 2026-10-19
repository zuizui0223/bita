"""Hypothesis and falsifier checks for the SCH–BITA evolutionary access model.

All values are synthetic parameter configurations, never biological effect sizes.
"""
from __future__ import annotations

import json
from math import sqrt

import pytest

from trait_architecture.differentiation import compare_architectures
from trait_architecture.evolutionary_accessibility import (
    deterministic_uphill_walk,
    example_readout,
    gain_at_fraction,
    initial_gradient,
    landscape,
)


def test_no_function_conflict_with_activation_cost_preserves_shared_optimum():
    r = landscape(distance=0.0)
    assert r.selected_separation_fraction == 0.0
    assert r.maximum_relative_fitness == 0.0
    assert r.classification == "SHARED_GLOBAL_OPTIMUM"


def test_zero_activation_cost_exactly_recovers_existing_bita_quadratic_model():
    for w1, w2, coupling, d in (
        (1, 1, 0.5, 1), (0.4, 2, 1, 1.2), (3, 0.7, 0, 0.3),
    ):
        analytic = compare_architectures(
            0, d, weight_1=w1, weight_2=w2,
            coupling=coupling, architecture_cost=0,
        )
        new = landscape(
            distance=d, weight_1=w1, weight_2=w2,
            coupling=coupling, activation_cost_cap=0,
        )
        assert new.selected_separation_fraction == pytest.approx(
            analytic.decoupling_fraction, abs=1e-9,
        )
        assert new.maximum_relative_fitness == pytest.approx(
            analytic.recoverable_conflict_loss, abs=1e-9,
        )
        assert new.classification == "SMALL_STEPS_CAN_INVADE"


def test_tradeoff_can_remain_balanced_with_positive_cost():
    assert landscape(distance=0.5).classification == "SHARED_GLOBAL_OPTIMUM"
    assert landscape(
        distance=1.0, activation_cost_cap=0.4,
    ).classification == "SHARED_GLOBAL_OPTIMUM"


def test_global_fitness_advantage_does_not_guarantee_local_invasion():
    r = landscape(distance=1)
    assert r.classification == "GLOBAL_GAIN_BUT_LOCAL_TRAP"
    assert r.initial_selection_gradient == pytest.approx(-2)
    assert r.maximum_relative_fitness == pytest.approx(0.1000068136, abs=2e-8)
    assert r.first_positive_invasion_fraction == pytest.approx(
        0.176958854, abs=1e-8,
    )
    assert r.selected_separation_fraction == pytest.approx(.5, abs=1e-3)
    assert gain_at_fraction(.1, distance=1) < 0
    assert gain_at_fraction(.25, distance=1) > 0
    assert deterministic_uphill_walk(
        maximum_step=.1, distance=1,
    ) == (0.0,)
    larger = deterministic_uphill_walk(maximum_step=.25, distance=1)
    assert larger[0] == 0.0
    assert larger[-1] == pytest.approx(.5, abs=.01)
    assert len(larger) > 1


def test_conflict_distance_splits_three_architecture_regimes():
    labels = [landscape(distance=d).classification for d in
              (.5, .8, 1, 1.5, 2)]
    assert labels == [
        "SHARED_GLOBAL_OPTIMUM",
        "GLOBAL_GAIN_BUT_LOCAL_TRAP",
        "GLOBAL_GAIN_BUT_LOCAL_TRAP",
        "GLOBAL_GAIN_BUT_LOCAL_TRAP",
        "SMALL_STEPS_CAN_INVADE",
    ]
    h, s, k, tau = .5, .5, .15, .05
    assert sqrt(k/(s*h)) < 1 < sqrt(k/(2*h*tau))
    assert initial_gradient(
        distance=sqrt(k/(2*h*tau)),
    ) == pytest.approx(0, abs=1e-12)


def test_fitness_rescaling_preserves_gain_sign_optimum_and_jump_threshold():
    r = landscape(distance=1)
    for factor in (1e-3, 1e3):
        rr = landscape(
            distance=1, weight_1=factor, weight_2=factor,
            coupling=.5*factor, activation_cost_cap=.15*factor,
        )
        assert rr.classification == r.classification
        assert rr.selected_separation_fraction == pytest.approx(
            r.selected_separation_fraction, abs=1e-8,
        )
        assert rr.first_positive_invasion_fraction == pytest.approx(
            r.first_positive_invasion_fraction, abs=1e-8,
        )
        assert rr.maximum_relative_fitness == pytest.approx(
            r.maximum_relative_fitness*factor, rel=1e-10,
        )


@pytest.mark.parametrize("changes", [
    {"distance": -1}, {"coupling": -1}, {"weight_1": 0},
    {"activation_cost_cap": -1}, {"activation_scale": 0},
])
def test_invalid_parameters_fail_closed(changes):
    with pytest.raises(ValueError):
        landscape(**dict({"distance": 1}, **changes))


def test_readout_is_explicitly_synthetic_and_not_an_empirical_confirmation():
    result = example_readout()
    assert result["data_level"] == "THEORY_SIMULATION_ONLY"
    assert len(result["scenarios"]) == 5
    assert "source_dataset" not in json.dumps(result)
