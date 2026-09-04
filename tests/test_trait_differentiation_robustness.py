import math

import pytest

from trait_architecture.differentiation import compare_architectures
from trait_architecture.differentiation_robustness import compare_power_architectures


def test_quadratic_power_family_matches_closed_form_baseline():
    cases = [
        (0.0, 1.0, 1.0, 1.0, 0.0, 0.1),
        (-0.5, 1.5, 2.0, 0.7, 0.4, 0.05),
        (0.2, 0.9, 0.4, 3.0, 2.0, 0.01),
    ]
    for theta1, theta2, w1, w2, coupling, cost in cases:
        analytic = compare_architectures(
            theta1,
            theta2,
            weight_1=w1,
            weight_2=w2,
            coupling=coupling,
            architecture_cost=cost,
        )
        numeric = compare_power_architectures(
            theta1,
            theta2,
            weight_1=w1,
            weight_2=w2,
            coupling=coupling,
            architecture_cost=cost,
            functional_power=2.0,
            coupling_power=2.0,
        )
        assert numeric.shared.trait == pytest.approx(analytic.shared.trait, abs=2e-6)
        assert numeric.differentiated.trait_1 == pytest.approx(
            analytic.differentiated.trait_1, abs=2e-6
        )
        assert numeric.differentiated.trait_2 == pytest.approx(
            analytic.differentiated.trait_2, abs=2e-6
        )
        assert numeric.architecture_gain == pytest.approx(
            analytic.architecture_gain, abs=2e-6
        )


def test_zero_conflict_has_no_recoverable_gain_before_architecture_cost():
    for power in (1.5, 2.0, 3.0, 4.0):
        result = compare_power_architectures(
            0.75,
            0.75,
            weight_1=0.6,
            weight_2=2.3,
            coupling=1.7,
            architecture_cost=0.08,
            functional_power=power,
        )
        assert result.recoverable_conflict_loss == pytest.approx(0.0, abs=1e-8)
        assert result.architecture_gain == pytest.approx(-0.08, abs=1e-8)
        assert result.preferred_architecture == "shared"


def test_nonquadratic_differentiation_recovers_some_conflict_loss():
    for power in (1.5, 2.0, 3.0, 4.0):
        for w1, w2 in ((1.0, 1.0), (0.4, 2.0), (3.0, 0.7)):
            for coupling in (0.0, 0.2, 1.0, 5.0):
                result = compare_power_architectures(
                    0.0,
                    1.0,
                    weight_1=w1,
                    weight_2=w2,
                    coupling=coupling,
                    architecture_cost=0.0,
                    functional_power=power,
                )
                assert result.recoverable_conflict_loss > 0.0
                assert result.architecture_gain > 0.0
                assert result.preferred_architecture == "differentiated"
                assert result.differentiated.separation > 0.0


def test_fixed_architecture_cost_subtracts_one_for_one_from_gain():
    base = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7,
        weight_2=1.4,
        coupling=0.6,
        architecture_cost=0.0,
        functional_power=3.0,
    )
    costly = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7,
        weight_2=1.4,
        coupling=0.6,
        architecture_cost=0.123,
        functional_power=3.0,
    )
    assert costly.architecture_gain == pytest.approx(
        base.architecture_gain - 0.123, abs=1e-8
    )


def test_more_residual_coupling_never_increases_recoverable_gain_in_declared_grid():
    for power in (1.5, 2.0, 3.0, 4.0):
        gains = [
            compare_power_architectures(
                0.0,
                1.0,
                weight_1=0.8,
                weight_2=1.6,
                coupling=coupling,
                architecture_cost=0.0,
                functional_power=power,
            ).recoverable_conflict_loss
            for coupling in (0.0, 0.1, 0.5, 2.0, 10.0)
        ]
        assert all(a >= b - 1e-8 for a, b in zip(gains, gains[1:]))


def test_stronger_optimum_conflict_increases_recoverable_gain_for_matched_powers():
    for power in (1.5, 2.0, 3.0, 4.0):
        gains = [
            compare_power_architectures(
                0.0,
                distance,
                weight_1=1.3,
                weight_2=0.9,
                coupling=0.7,
                architecture_cost=0.0,
                functional_power=power,
                coupling_power=power,
            ).recoverable_conflict_loss
            for distance in (0.1, 0.25, 0.5, 1.0, 2.0)
        ]
        assert all(a < b for a, b in zip(gains, gains[1:]))


def test_mismatched_function_and_coupling_curvature_preserves_cost_threshold_logic():
    for functional_power, coupling_power in ((1.5, 2.0), (2.0, 4.0), (4.0, 2.0)):
        no_cost = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=0.0,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        threshold = no_cost.recoverable_conflict_loss
        below = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=0.9 * threshold,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        above = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=1.1 * threshold,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        assert below.preferred_architecture == "differentiated"
        assert above.preferred_architecture == "shared"
