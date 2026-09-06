import math

import pytest


def recovery_after_decoupling(lambda0, x):
    return sum(math.exp(-(lam - dx)) for lam, dx in zip(lambda0, x))


def test_symmetric_convex_recovery_prefers_extreme_over_equal_split():
    lambda0 = (1.0, 1.0)
    budget = 0.8
    extreme = recovery_after_decoupling(lambda0, (budget, 0.0))
    split = recovery_after_decoupling(lambda0, (budget / 2.0, budget / 2.0))
    assert extreme > split


def test_dense_two_channel_grid_has_a_vertex_maximizer_under_l1_budget():
    lambda0 = (1.0, 1.0)
    budget = 0.8
    best = (-math.inf, None)
    step = 0.01
    for i in range(81):
        x1 = i * step
        for j in range(81 - i):
            x2 = j * step
            if x1 <= 1.0 and x2 <= 1.0 and x1 + x2 <= budget + 1e-12:
                value = recovery_after_decoupling(lambda0, (x1, x2))
                if value > best[0]:
                    best = (value, (x1, x2))

    value, x = best
    vertex_values = [
        recovery_after_decoupling(lambda0, (0.0, 0.0)),
        recovery_after_decoupling(lambda0, (budget, 0.0)),
        recovery_after_decoupling(lambda0, (0.0, budget)),
    ]
    assert value == pytest.approx(max(vertex_values))
    assert x in {(budget, 0.0), (0.0, budget)}


def test_weighted_budget_extreme_has_at_most_one_partial_coordinate():
    caps = (0.4, 0.7, 0.9)
    costs = (1.0, 2.0, 3.0)
    budget = 1.4

    # One feasible extreme pattern: first channel saturated, second partial,
    # third untouched. Only one coordinate lies strictly inside its box.
    x1 = caps[0]
    x2 = (budget - costs[0] * x1) / costs[1]
    x3 = 0.0
    x = (x1, x2, x3)
    partial = sum(0.0 < xi < cap for xi, cap in zip(x, caps))
    assert partial == 1
    assert sum(a * xi for a, xi in zip(costs, x)) == pytest.approx(budget)
