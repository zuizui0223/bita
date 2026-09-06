import math

import pytest

from trait_architecture.second_order_decoupling import (
    euclidean_crossing_budget_bracket,
    scalar_finite_gain_bounds,
)


def test_scalar_bounds_collapse_when_curvature_is_zero():
    lower, upper = scalar_finite_gain_bounds(
        linear_gain=0.6,
        squared_norm=0.25,
        curvature_upper=0.0,
    )
    assert lower == pytest.approx(0.6)
    assert upper == pytest.approx(0.6)


def test_scalar_bounds_include_quadratic_exact_gain():
    # R(lambda) = const - c0*x +?  Along decoupling, exact gain is
    # c0*x + 0.5*beta*x^2 when Hessian is exactly beta.
    c0 = 2.0
    x = 0.3
    beta = 4.0
    exact_gain = c0 * x + 0.5 * beta * x * x
    lower, upper = scalar_finite_gain_bounds(
        linear_gain=c0 * x,
        squared_norm=x * x,
        curvature_upper=beta,
    )
    assert lower <= exact_gain <= upper
    assert upper == pytest.approx(exact_gain)


def test_budget_bracket_matches_affine_case():
    bracket = euclidean_crossing_budget_bracket(
        deficit=1.5,
        penalty_norm=3.0,
        curvature_upper=0.0,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(0.5)
    assert bracket.sufficient_above == pytest.approx(0.5)


def test_true_quadratic_threshold_lies_inside_bracket():
    # Exact gain(epsilon) = c*epsilon + 0.5*beta*epsilon^2.
    deficit = 1.0
    c = 2.0
    beta = 3.0
    exact_threshold = (math.sqrt(c * c + 2.0 * beta * deficit) - c) / beta
    bracket = euclidean_crossing_budget_bracket(
        deficit=deficit,
        penalty_norm=c,
        curvature_upper=beta,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(exact_threshold)
    assert exact_threshold <= bracket.sufficient_above


def test_zero_current_gradient_has_no_first_order_sufficient_budget():
    bracket = euclidean_crossing_budget_bracket(
        deficit=1.0,
        penalty_norm=0.0,
        curvature_upper=2.0,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(1.0)
    assert math.isinf(bracket.sufficient_above)


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        euclidean_crossing_budget_bracket(
            deficit=0.0,
            penalty_norm=1.0,
            curvature_upper=1.0,
        )
    with pytest.raises(ValueError):
        scalar_finite_gain_bounds(
            linear_gain=1.0,
            squared_norm=1.0,
            curvature_lower=2.0,
            curvature_upper=1.0,
        )
