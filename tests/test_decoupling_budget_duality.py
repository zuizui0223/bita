import math

from trait_architecture.optimal_decoupling import (
    optimal_l1_decoupling,
    optimal_l2_decoupling,
    optimal_linf_decoupling,
)


def test_l1_budget_is_sparse_on_largest_penalty_channel():
    plan = optimal_l1_decoupling((1.0, 3.0, 2.0), budget=2.0)
    assert plan.direction == (0.0, -2.0, 0.0)
    assert math.isclose(plan.first_order_gain, 6.0, rel_tol=1e-12)


def test_l2_budget_distributes_proportionally_to_penalties():
    plan = optimal_l2_decoupling((3.0, 4.0), budget=2.0)
    assert math.isclose(plan.direction[0], -1.2, rel_tol=1e-12)
    assert math.isclose(plan.direction[1], -1.6, rel_tol=1e-12)
    assert math.isclose(plan.first_order_gain, 10.0, rel_tol=1e-12)
    assert math.isclose(math.sqrt(sum(x * x for x in plan.direction)), 2.0, rel_tol=1e-12)


def test_linf_budget_weakens_all_positive_penalty_channels():
    plan = optimal_linf_decoupling((1.0, 3.0, 0.0, 2.0), budget=0.5)
    assert plan.direction == (-0.5, -0.5, 0.0, -0.5)
    assert math.isclose(plan.first_order_gain, 3.0, rel_tol=1e-12)
