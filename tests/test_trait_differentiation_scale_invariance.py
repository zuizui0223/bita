from __future__ import annotations

import math

from trait_architecture.differentiation import (
    compare_architectures,
    differentiation_threshold,
)


def _close(left: float, right: float, rel_tol: float = 2e-11) -> None:
    assert math.isclose(left, right, rel_tol=rel_tol, abs_tol=0.0)


def test_trait_coordinate_units_preserve_quadratic_architecture_geometry() -> None:
    base = compare_architectures(
        -0.5,
        1.5,
        weight_1=0.4,
        weight_2=2.0,
        coupling=0.7,
        architecture_cost=0.01,
    )

    for q in (1e-150, 1e-75, 1.0, 1e75, 1e150):
        q2 = q * q
        result = compare_architectures(
            -0.5 * q,
            1.5 * q,
            weight_1=0.4 / q2,
            weight_2=2.0 / q2,
            coupling=0.7 / q2,
            architecture_cost=0.01,
        )
        assert result.preferred_architecture == base.preferred_architecture
        _close(result.decoupling_fraction, base.decoupling_fraction)
        _close(result.shared.trait / q, base.shared.trait)
        _close(result.differentiated.trait_1 / q, base.differentiated.trait_1)
        _close(result.differentiated.trait_2 / q, base.differentiated.trait_2)
        _close(result.shared.conflict_loss, base.shared.conflict_loss)
        _close(result.differentiated.residual_conflict_loss, base.differentiated.residual_conflict_loss)
        _close(result.recoverable_conflict_loss, base.recoverable_conflict_loss)
        _close(result.differentiation_threshold, base.differentiation_threshold)
        _close(result.architecture_gain, base.architecture_gain)


def test_fitness_units_scale_losses_costs_and_gain_but_not_trait_geometry() -> None:
    base = compare_architectures(
        -0.5,
        1.5,
        weight_1=0.4,
        weight_2=2.0,
        coupling=0.7,
        architecture_cost=0.01,
    )

    for scale in (1e-300, 1.0, 1e300):
        result = compare_architectures(
            -0.5,
            1.5,
            weight_1=0.4 * scale,
            weight_2=2.0 * scale,
            coupling=0.7 * scale,
            architecture_cost=0.01 * scale,
        )
        assert result.preferred_architecture == base.preferred_architecture
        _close(result.decoupling_fraction, base.decoupling_fraction)
        _close(result.shared.trait, base.shared.trait)
        _close(result.differentiated.trait_1, base.differentiated.trait_1)
        _close(result.differentiated.trait_2, base.differentiated.trait_2)
        _close(result.shared.conflict_loss / scale, base.shared.conflict_loss)
        _close(
            result.differentiated.residual_conflict_loss / scale,
            base.differentiated.residual_conflict_loss,
        )
        _close(result.recoverable_conflict_loss / scale, base.recoverable_conflict_loss)
        _close(result.differentiation_threshold / scale, base.differentiation_threshold)
        _close(result.architecture_gain / scale, base.architecture_gain)


def test_default_preference_does_not_hide_tiny_strict_gain() -> None:
    result = compare_architectures(
        0.0,
        1.0,
        weight_1=1e-13,
        weight_2=1e-13,
        coupling=1e-13,
        architecture_cost=1e-14,
    )
    assert 0.0 < result.architecture_gain < 1e-12
    assert result.preferred_architecture == "differentiated"


def test_explicit_absolute_neutral_band_keeps_historical_semantics() -> None:
    result = compare_architectures(
        0.0,
        1.0,
        weight_1=1e-13,
        weight_2=1e-13,
        coupling=1e-13,
        architecture_cost=1e-14,
        neutral_tolerance=1e-12,
    )
    assert 0.0 < result.architecture_gain < 1e-12
    assert result.preferred_architecture == "indifferent"


def test_exact_architecture_boundary_remains_indifferent_by_default() -> None:
    threshold = differentiation_threshold(
        0.0,
        1.0,
        weight_1=0.4,
        weight_2=2.0,
        coupling=0.7,
    )
    result = compare_architectures(
        0.0,
        1.0,
        weight_1=0.4,
        weight_2=2.0,
        coupling=0.7,
        architecture_cost=threshold,
    )
    assert result.architecture_gain == 0.0
    assert result.preferred_architecture == "indifferent"
