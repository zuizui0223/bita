import math

import pytest


def recovery(lambda0, x):
    return sum(math.exp(-(lam - dx)) for lam, dx in zip(lambda0, x))


def test_vertex_values_dominate_dense_interior_grid_for_convex_recovery():
    lambda0 = (1.0, 1.0)
    budget = 0.8
    vertices = [(0.0, 0.0), (budget, 0.0), (0.0, budget)]
    vertex_max = max(recovery(lambda0, v) for v in vertices)

    step = 0.02
    grid_max = -math.inf
    for i in range(int(budget / step) + 1):
        x1 = i * step
        for j in range(int((budget - x1) / step) + 1):
            x2 = j * step
            grid_max = max(grid_max, recovery(lambda0, (x1, x2)))

    assert grid_max == pytest.approx(vertex_max)


def test_if_all_vertices_are_below_cost_dense_interior_cannot_cross():
    lambda0 = (1.0, 1.0)
    budget = 0.4
    vertices = [(0.0, 0.0), (budget, 0.0), (0.0, budget)]
    vertex_max = max(recovery(lambda0, v) for v in vertices)
    k_cost = vertex_max + 0.05
    assert all(recovery(lambda0, v) - k_cost < 0 for v in vertices)

    step = 0.02
    for i in range(int(budget / step) + 1):
        x1 = i * step
        for j in range(int((budget - x1) / step) + 1):
            x2 = j * step
            assert recovery(lambda0, (x1, x2)) - k_cost <= 1e-12


def test_interior_convexity_chord_audit():
    lambda0 = (1.0, 1.0)
    v1 = (0.8, 0.0)
    v2 = (0.0, 0.8)
    theta = 0.3
    x = (
        theta * v1[0] + (1.0 - theta) * v2[0],
        theta * v1[1] + (1.0 - theta) * v2[1],
    )
    lhs = recovery(lambda0, x)
    rhs = theta * recovery(lambda0, v1) + (1.0 - theta) * recovery(lambda0, v2)
    assert lhs <= rhs + 1e-12
