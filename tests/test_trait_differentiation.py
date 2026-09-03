from math import isclose

import pytest

from trait_architecture.differentiation import (
    compare_architectures,
    differentiated_axis_optimum,
    differentiation_threshold,
    shared_axis_optimum,
)


def test_equal_weight_shared_axis_is_midpoint():
    result = shared_axis_optimum(0.0, 1.0)
    assert isclose(result.trait, 0.5)
    assert isclose(result.conflict_loss, 0.5)
    assert isclose(result.fitness, -0.5)


def test_full_decoupling_recovers_both_functional_optima():
    result = differentiated_axis_optimum(0.0, 1.0, coupling=0.0)
    assert isclose(result.trait_1, 0.0)
    assert isclose(result.trait_2, 1.0)
    assert isclose(result.residual_conflict_loss, 0.0)
    assert isclose(result.separation, 1.0)
    assert isclose(result.fitness, 0.0)


def test_architecture_gain_equals_threshold_minus_fixed_cost():
    threshold = differentiation_threshold(0.0, 1.0, coupling=1.0)
    comparison = compare_architectures(
        0.0,
        1.0,
        coupling=1.0,
        architecture_cost=0.1,
    )
    assert isclose(threshold, 1.0 / 6.0)
    assert isclose(comparison.architecture_gain, threshold - 0.1)
    assert comparison.preferred_architecture == "differentiated"


def test_large_architecture_cost_retains_shared_compromise():
    comparison = compare_architectures(
        0.0,
        1.0,
        coupling=0.0,
        architecture_cost=0.6,
    )
    assert isclose(comparison.differentiation_threshold, 0.5)
    assert isclose(comparison.architecture_gain, -0.1)
    assert comparison.preferred_architecture == "shared"


def test_no_functional_conflict_gives_no_differentiation_gain():
    comparison = compare_architectures(
        0.25,
        0.25,
        coupling=0.0,
        architecture_cost=0.0,
    )
    assert isclose(comparison.differentiation_threshold, 0.0)
    assert isclose(comparison.architecture_gain, 0.0)
    assert comparison.preferred_architecture == "indifferent"


def test_residual_coupling_reduces_differentiation_threshold():
    low = differentiation_threshold(0.0, 1.0, coupling=0.1)
    high = differentiation_threshold(0.0, 1.0, coupling=10.0)
    assert low > high > 0.0


def test_invalid_parameters_are_rejected():
    with pytest.raises(ValueError):
        shared_axis_optimum(0.0, 1.0, weight_1=0.0)
    with pytest.raises(ValueError):
        differentiated_axis_optimum(0.0, 1.0, coupling=-0.1)
    with pytest.raises(ValueError):
        compare_architectures(0.0, 1.0, architecture_cost=-0.1)
