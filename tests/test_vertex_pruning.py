import pytest

from trait_architecture.vertex_pruning import (
    dominates,
    pareto_maximal_vertex_indices,
    pareto_maximal_vertices,
)


def test_box_has_unique_pareto_maximal_vertex():
    vertices = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
    ]
    assert pareto_maximal_vertices(vertices) == ((1.0, 1.0),)


def test_simplex_keeps_budget_tradeoff_vertices():
    vertices = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
    ]
    assert set(pareto_maximal_vertices(vertices)) == {(1.0, 0.0), (0.0, 1.0)}


def test_monotone_convex_maximum_is_preserved_after_pruning():
    vertices = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
    ]

    def recovery(x):
        return x[0] ** 2 + 2.0 * x[1] ** 2

    all_max = max(recovery(v) for v in vertices)
    kept = pareto_maximal_vertices(vertices)
    kept_max = max(recovery(v) for v in kept)
    assert kept_max == pytest.approx(all_max)


def test_dominated_vertex_cannot_outperform_its_dominator_under_monotone_example():
    weak = (0.4, 0.3)
    strong = (0.8, 0.3)
    assert dominates(strong, weak)

    def recovery(x):
        return 3.0 * x[0] + x[1] + 0.5 * (x[0] ** 2 + x[1] ** 2)

    assert recovery(strong) >= recovery(weak)


def test_indices_preserve_original_order():
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    assert pareto_maximal_vertex_indices(vertices) == (1, 2)


def test_invalid_vertex_dimensions_fail_closed():
    with pytest.raises(ValueError):
        pareto_maximal_vertex_indices([])
    with pytest.raises(ValueError):
        pareto_maximal_vertex_indices([(0.0,), (0.0, 1.0)])
