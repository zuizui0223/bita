import pytest

from trait_architecture.joint_intervention_allocation import (
    allocate_joint_linear_budget,
    minimum_certified_joint_budget,
)


def test_high_efficiency_coupling_is_used_before_cost_relief():
    out = allocate_joint_linear_budget(
        active_penalties=[4.0, 1.0],
        decoupling_costs=[1.0, 1.0],
        coupling_caps=[0.5, 1.0],
        cost_relief_price=1.0,  # efficiency 1
        budget=0.4,
    )
    assert out.decoupling[0] == pytest.approx(0.4)
    assert out.cost_relief == 0.0
    assert out.certified_margin_gain == pytest.approx(1.6)


def test_cost_relief_is_used_first_when_it_is_more_efficient():
    out = allocate_joint_linear_budget(
        active_penalties=[0.5, 0.2],
        decoupling_costs=[2.0, 1.0],
        coupling_caps=[1.0, 1.0],
        cost_relief_price=1.0,  # efficiency 1 > .25 and .2
        budget=0.7,
    )
    assert out.decoupling == pytest.approx((0.0, 0.0))
    assert out.cost_relief == pytest.approx(0.7)
    assert out.certified_margin_gain == pytest.approx(0.7)


def test_schedule_switches_to_cost_after_best_coupling_saturates():
    out = allocate_joint_linear_budget(
        active_penalties=[3.0, 0.5],
        decoupling_costs=[1.0, 1.0],
        coupling_caps=[0.2, 1.0],
        cost_relief_price=1.0,
        budget=0.5,
    )
    assert out.decoupling[0] == pytest.approx(0.2)
    assert out.decoupling[1] == pytest.approx(0.0)
    assert out.cost_relief == pytest.approx(0.3)
    assert out.certified_margin_gain == pytest.approx(0.9)


def test_minimum_certified_budget_follows_efficiency_order():
    crossing = minimum_certified_joint_budget(
        deficit=1.0,
        active_penalties=[3.0, 0.5],
        decoupling_costs=[1.0, 1.0],
        coupling_caps=[0.2, 1.0],
        cost_relief_price=1.0,
    )
    # First spend .2 for .6 gain on coupling 0, then .4 on K relief.
    assert crossing.budget == pytest.approx(0.6)
    assert crossing.last_lane == "cost"


def test_invalid_budget_fails_closed():
    with pytest.raises(ValueError):
        allocate_joint_linear_budget(
            active_penalties=[1.0],
            decoupling_costs=[1.0],
            coupling_caps=[1.0],
            cost_relief_price=1.0,
            budget=-1.0,
        )
