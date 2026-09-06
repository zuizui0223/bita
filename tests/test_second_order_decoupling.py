import math

import pytest

from trait_architecture.second_order_decoupling import (
    euclidean_crossing_budget_bracket,
    robust_uncertain_budget_bracket,
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
    c0 = 2.0
    x = 0.3
    beta = 4.0
    exact_gain = c0 * x + 0.5 * beta * x * x
    lower, upper = scalar_finite_gain_bounds(
        linear_gain=c0 * x,
        squared_norm=x * x,
        curvature_lower=beta,
        curvature_upper=beta,
    )
    assert lower == pytest.approx(exact_gain)
    assert upper == pytest.approx(exact_gain)


def test_budget_bracket_matches_affine_case():
    bracket = euclidean_crossing_budget_bracket(
        deficit=1.5,
        penalty_norm=3.0,
        curvature_upper=0.0,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(0.5)
    assert bracket.sufficient_above == pytest.approx(0.5)


def test_exact_quadratic_curvature_collapses_budget_band():
    deficit = 1.0
    c = 2.0
    beta = 3.0
    exact_threshold = (math.sqrt(c * c + 2.0 * beta * deficit) - c) / beta
    bracket = euclidean_crossing_budget_bracket(
        deficit=deficit,
        penalty_norm=c,
        curvature_lower=beta,
        curvature_upper=beta,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(exact_threshold)
    assert bracket.sufficient_above == pytest.approx(exact_threshold)


def test_partial_curvature_information_brackets_true_threshold():
    deficit = 1.0
    c = 2.0
    true_beta = 2.0
    lower_beta = 1.0
    upper_beta = 3.0
    exact_threshold = (
        math.sqrt(c * c + 2.0 * true_beta * deficit) - c
    ) / true_beta
    bracket = euclidean_crossing_budget_bracket(
        deficit=deficit,
        penalty_norm=c,
        curvature_lower=lower_beta,
        curvature_upper=upper_beta,
    )
    assert bracket.no_cross_below_or_at <= exact_threshold
    assert exact_threshold <= bracket.sufficient_above
    assert bracket.no_cross_below_or_at < bracket.sufficient_above


def test_zero_current_gradient_can_have_curvature_only_sufficient_budget():
    bracket = euclidean_crossing_budget_bracket(
        deficit=1.0,
        penalty_norm=0.0,
        curvature_lower=1.0,
        curvature_upper=2.0,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(1.0)
    assert bracket.sufficient_above == pytest.approx(math.sqrt(2.0))


def test_zero_gradient_and_zero_lower_curvature_has_no_finite_guarantee():
    bracket = euclidean_crossing_budget_bracket(
        deficit=1.0,
        penalty_norm=0.0,
        curvature_upper=2.0,
    )
    assert bracket.no_cross_below_or_at == pytest.approx(1.0)
    assert math.isinf(bracket.sufficient_above)


def test_uncertain_parameter_band_contains_all_corner_exact_bands():
    robust = robust_uncertain_budget_bracket(
        deficit_lower=0.8,
        deficit_upper=1.2,
        penalty_norm_lower=1.5,
        penalty_norm_upper=2.5,
        curvature_lower=0.5,
        curvature_upper=3.0,
    )
    for deficit in (0.8, 1.2):
        for penalty in (1.5, 2.5):
            for curvature in (0.5, 3.0):
                exact = euclidean_crossing_budget_bracket(
                    deficit=deficit,
                    penalty_norm=penalty,
                    curvature_lower=curvature,
                    curvature_upper=curvature,
                )
                assert robust.robust_no_cross_below_or_at <= exact.no_cross_below_or_at
                assert exact.sufficient_above <= robust.robust_sufficient_above


def test_tightening_parameter_uncertainty_cannot_widen_band_in_example():
    wide = robust_uncertain_budget_bracket(
        deficit_lower=0.8,
        deficit_upper=1.2,
        penalty_norm_lower=1.5,
        penalty_norm_upper=2.5,
        curvature_lower=0.5,
        curvature_upper=3.0,
    )
    tight = robust_uncertain_budget_bracket(
        deficit_lower=0.9,
        deficit_upper=1.1,
        penalty_norm_lower=1.8,
        penalty_norm_upper=2.2,
        curvature_lower=1.0,
        curvature_upper=2.5,
    )
    wide_width = wide.robust_sufficient_above - wide.robust_no_cross_below_or_at
    tight_width = tight.robust_sufficient_above - tight.robust_no_cross_below_or_at
    assert tight_width <= wide_width


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        euclidean_crossing_budget_bracket(
            deficit=0.0,
            penalty_norm=1.0,
            curvature_upper=1.0,
        )
    with pytest.raises(ValueError):
        euclidean_crossing_budget_bracket(
            deficit=1.0,
            penalty_norm=1.0,
            curvature_lower=2.0,
            curvature_upper=1.0,
        )
    with pytest.raises(ValueError):
        scalar_finite_gain_bounds(
            linear_gain=1.0,
            squared_norm=1.0,
            curvature_lower=2.0,
            curvature_upper=1.0,
        )
    with pytest.raises(ValueError):
        robust_uncertain_budget_bracket(
            deficit_lower=1.2,
            deficit_upper=1.0,
            penalty_norm_lower=1.0,
            penalty_norm_upper=2.0,
            curvature_lower=0.0,
            curvature_upper=1.0,
        )
