from __future__ import annotations

import math

from trait_architecture.differentiation_robustness import compare_power_architectures


def _close(left: float, right: float, rel_tol: float = 2e-7) -> None:
    assert math.isclose(left, right, rel_tol=rel_tol, abs_tol=0.0)


def _base():
    return compare_power_architectures(
        -0.5,
        1.2,
        weight_1=0.6,
        weight_2=2.2,
        coupling=0.9,
        architecture_cost=0.02,
        functional_power=1.5,
        coupling_power=2.5,
    )


def test_nonquadratic_trait_units_leave_dimensionless_optimization_unchanged() -> None:
    base = _base()
    p = 1.5
    q_power = 2.5

    for scale in (1e-120, 1e-60, 1.0, 1e60, 1e120):
        functional_scale = scale**p
        coupling_scale = scale**q_power
        result = compare_power_architectures(
            -0.5 * scale,
            1.2 * scale,
            weight_1=0.6 / functional_scale,
            weight_2=2.2 / functional_scale,
            coupling=0.9 / coupling_scale,
            architecture_cost=0.02,
            functional_power=p,
            coupling_power=q_power,
        )
        assert result.preferred_architecture == base.preferred_architecture
        _close(result.shared.trait / scale, base.shared.trait)
        _close(result.differentiated.trait_1 / scale, base.differentiated.trait_1)
        _close(result.differentiated.trait_2 / scale, base.differentiated.trait_2)
        _close(result.shared.loss, base.shared.loss)
        _close(
            result.differentiated.loss_before_fixed_cost,
            base.differentiated.loss_before_fixed_cost,
        )
        _close(result.recoverable_conflict_loss, base.recoverable_conflict_loss)
        _close(result.architecture_gain, base.architecture_gain)


def test_common_fitness_units_scale_losses_without_moving_optima() -> None:
    base = _base()
    for scale in (1e-250, 1.0, 1e250):
        result = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6 * scale,
            weight_2=2.2 * scale,
            coupling=0.9 * scale,
            architecture_cost=0.02 * scale,
            functional_power=1.5,
            coupling_power=2.5,
        )
        assert result.preferred_architecture == base.preferred_architecture
        _close(result.shared.trait, base.shared.trait)
        _close(result.differentiated.trait_1, base.differentiated.trait_1)
        _close(result.differentiated.trait_2, base.differentiated.trait_2)
        _close(result.shared.loss / scale, base.shared.loss)
        _close(
            result.differentiated.loss_before_fixed_cost / scale,
            base.differentiated.loss_before_fixed_cost,
        )
        _close(result.recoverable_conflict_loss / scale, base.recoverable_conflict_loss)
        _close(result.architecture_gain / scale, base.architecture_gain)


def test_default_preference_does_not_hide_tiny_nonquadratic_gain() -> None:
    no_cost = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7,
        weight_2=1.4,
        coupling=0.6,
        architecture_cost=0.0,
        functional_power=3.0,
    )
    scale = 1e-13
    cost = 0.5 * no_cost.recoverable_conflict_loss * scale
    result = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7 * scale,
        weight_2=1.4 * scale,
        coupling=0.6 * scale,
        architecture_cost=cost,
        functional_power=3.0,
    )
    assert 0.0 < result.architecture_gain < 1e-9
    assert result.preferred_architecture == "differentiated"


def test_explicit_nonquadratic_neutral_band_keeps_absolute_semantics() -> None:
    no_cost = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7,
        weight_2=1.4,
        coupling=0.6,
        architecture_cost=0.0,
        functional_power=3.0,
    )
    scale = 1e-13
    cost = 0.5 * no_cost.recoverable_conflict_loss * scale
    result = compare_power_architectures(
        0.0,
        1.0,
        weight_1=0.7 * scale,
        weight_2=1.4 * scale,
        coupling=0.6 * scale,
        architecture_cost=cost,
        functional_power=3.0,
        neutral_tolerance=1e-9,
    )
    assert 0.0 < result.architecture_gain < 1e-9
    assert result.preferred_architecture == "indifferent"


def test_zero_conflict_remains_exact_under_normalized_optimizer() -> None:
    result = compare_power_architectures(
        0.75,
        0.75,
        weight_1=1e200,
        weight_2=2e200,
        coupling=3e200,
        architecture_cost=0.08,
        functional_power=3.0,
        coupling_power=2.0,
    )
    assert result.shared.loss == 0.0
    assert result.differentiated.loss_before_fixed_cost == 0.0
    assert result.recoverable_conflict_loss == 0.0
    assert result.architecture_gain == -0.08
    assert result.preferred_architecture == "shared"
