import math

import pytest

from trait_architecture.model import ModelParameters
from trait_architecture.robustness import RobustnessCase, mixed_partial
from trait_architecture.sign_criterion import (
    OrientedSignCriterion,
    RegimeDerivativeBalance,
    RegimeScaledCriterion,
    SeparableLocalRegimeCriterion,
)


def test_antagonist_relief_can_make_traits_locally_complementary() -> None:
    criterion = OrientedSignCriterion(1.2, 0.5, 0.2)
    assert criterion.mixed_partial == pytest.approx(0.5)
    assert criterion.classify() == "locally_complementary"


def test_mutualist_interference_and_cross_cost_can_make_traits_substitutable() -> None:
    criterion = OrientedSignCriterion(0.4, 0.5, 0.2)
    assert criterion.mixed_partial == pytest.approx(-0.3)
    assert criterion.classify() == "locally_substitutable"


def test_break_even_boundary_is_explicit() -> None:
    criterion = OrientedSignCriterion(0.7, 0.5, 0.2)
    assert criterion.break_even_antagonist_relief == pytest.approx(0.7)
    assert criterion.classify() == "locally_neutral"


def test_baseline_result_is_a_corollary_of_oriented_local_criterion() -> None:
    case = RobustnessCase("baseline_corollary", 0.4, 0.3, 0.2, 0.6, 0.7)
    result = mixed_partial(case, ModelParameters())
    criterion = OrientedSignCriterion(
        result.antagonism_term,
        result.pollination_obstruction_term,
        result.joint_cost_curvature_term,
    )
    assert criterion.mixed_partial == pytest.approx(result.mixed_partial)


def test_oriented_channel_magnitudes_must_be_nonnegative_and_finite() -> None:
    with pytest.raises(ValueError, match="finite and non-negative"):
        OrientedSignCriterion(-0.1, 0.2, 0.1)
    with pytest.raises(ValueError, match="finite and non-negative"):
        OrientedSignCriterion(math.nan, 0.2, 0.1)


def test_general_regime_derivative_balance_keeps_cross_environment_effects() -> None:
    balance = RegimeDerivativeBalance(
        relief_h_slope=0.7,
        interference_h_slope=0.9,
        joint_cost_curvature_h_slope=-0.1,
        relief_p_slope=0.4,
        interference_p_slope=0.2,
        joint_cost_curvature_p_slope=0.05,
    )
    assert balance.d_mixed_partial_d_antagonist_pressure == pytest.approx(-0.1)
    assert balance.d_mixed_partial_d_pollinator_service == pytest.approx(0.15)


def test_cross_environment_effect_can_reverse_naive_antagonist_prediction() -> None:
    balance = RegimeDerivativeBalance(
        relief_h_slope=0.5,
        interference_h_slope=0.8,
        joint_cost_curvature_h_slope=0.0,
        relief_p_slope=0.0,
        interference_p_slope=0.0,
        joint_cost_curvature_p_slope=0.0,
    )
    assert balance.d_mixed_partial_d_antagonist_pressure < 0


def test_linear_separable_scaling_is_a_restricted_derivative_balance() -> None:
    criterion = RegimeScaledCriterion(0.6, 0.8, 1.0, 0.5, 0.1)
    assert criterion.d_mixed_partial_d_antagonist_pressure == pytest.approx(1.0)
    assert criterion.d_mixed_partial_d_pollinator_service == pytest.approx(-0.5)
    assert criterion.derivative_balance.interference_h_slope == 0.0
    assert criterion.derivative_balance.relief_p_slope == 0.0


def test_linear_break_even_requires_positive_relief_rate() -> None:
    criterion = RegimeScaledCriterion(0.5, 0.0, 0.8, 0.6, 0.1)
    assert criterion.break_even_antagonist_pressure == pytest.approx(0.5)
    no_unique_threshold = RegimeScaledCriterion(0.5, 0.0, 0.0, 0.6, 0.1)
    assert no_unique_threshold.break_even_antagonist_pressure is None


def test_separable_nonlinear_scaling_can_preserve_direction() -> None:
    criterion = SeparableLocalRegimeCriterion(
        antagonist_scale=0.7,
        mutualist_scale=0.8,
        antagonist_scale_slope=0.3,
        mutualist_scale_slope=0.4,
        relief_rate=1.2,
        interference_rate=0.5,
        joint_cost_curvature=0.1,
    )
    assert criterion.d_mixed_partial_d_antagonist_pressure == pytest.approx(0.36)
    assert criterion.d_mixed_partial_d_pollinator_service == pytest.approx(-0.2)


def test_regime_dependent_cross_cost_can_reverse_separable_prediction() -> None:
    criterion = SeparableLocalRegimeCriterion(
        antagonist_scale=0.7,
        mutualist_scale=0.8,
        antagonist_scale_slope=0.3,
        mutualist_scale_slope=0.4,
        relief_rate=1.2,
        interference_rate=0.5,
        joint_cost_curvature=0.1,
        joint_cost_curvature_h_slope=0.5,
    )
    assert criterion.d_mixed_partial_d_antagonist_pressure == pytest.approx(-0.14)
