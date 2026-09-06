import pytest

from trait_architecture.box_constrained_decoupling import (
    diagonal_l2_box_plan,
    weighted_l1_box_plan,
)


def test_weighted_l1_allocates_by_gain_per_cost_and_saturates():
    plan = weighted_l1_box_plan(
        active_penalties=[4.0, 3.0, 1.0],
        coupling_available=[1.0, 2.0, 5.0],
        unit_costs=[2.0, 1.0, 1.0],
        budget=3.0,
    )
    # efficiencies: channel1=3, channel0=2, channel2=1.
    assert plan.allocation == pytest.approx((0.5, 2.0, 0.0))
    assert plan.certified_linear_gain == pytest.approx(8.0)
    assert plan.budget_used == pytest.approx(3.0)
    assert plan.saturated_channels == (1,)


def test_weighted_l1_full_budget_need_not_be_spent_on_zero_gain_channel():
    plan = weighted_l1_box_plan(
        active_penalties=[1.0, 0.0],
        coupling_available=[1.0, 10.0],
        unit_costs=[1.0, 1.0],
        budget=5.0,
    )
    assert plan.allocation == pytest.approx((1.0, 0.0))
    assert plan.budget_used == pytest.approx(1.0)


def test_diagonal_l2_matches_unconstrained_proportional_rule_before_saturation():
    plan = diagonal_l2_box_plan(
        active_penalties=[2.0, 1.0],
        coupling_available=[10.0, 10.0],
        quadratic_costs=[1.0, 1.0],
        budget=1.0,
    )
    # x is proportional to c and has Euclidean norm 1.
    assert plan.allocation[0] / plan.allocation[1] == pytest.approx(2.0)
    assert plan.budget_used == pytest.approx(1.0)
    assert plan.saturated_channels == ()


def test_diagonal_l2_caps_saturated_high_value_channel_then_reallocates():
    plan = diagonal_l2_box_plan(
        active_penalties=[4.0, 1.0],
        coupling_available=[0.2, 10.0],
        quadratic_costs=[1.0, 1.0],
        budget=1.0,
    )
    assert plan.allocation[0] == pytest.approx(0.2)
    assert plan.allocation[1] == pytest.approx((1.0 - 0.2**2) ** 0.5)
    assert plan.budget_used == pytest.approx(1.0)
    assert plan.saturated_channels == (0,)


def test_diagonal_l2_returns_full_positive_gain_decoupling_if_budget_is_large():
    plan = diagonal_l2_box_plan(
        active_penalties=[2.0, 1.0, 0.0],
        coupling_available=[0.5, 1.0, 5.0],
        quadratic_costs=[4.0, 1.0, 1.0],
        budget=10.0,
    )
    assert plan.allocation == pytest.approx((0.5, 1.0, 0.0))
    assert plan.saturated_channels == (0, 1)


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        weighted_l1_box_plan([1.0], [1.0], [0.0], 1.0)
    with pytest.raises(ValueError):
        diagonal_l2_box_plan([1.0], [-1.0], [1.0], 1.0)
    with pytest.raises(ValueError):
        diagonal_l2_box_plan([1.0], [1.0], [1.0], -1.0)
