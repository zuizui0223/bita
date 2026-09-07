from __future__ import annotations

from typing import Iterable, Sequence


def dominates(a: Sequence[float], b: Sequence[float], *, tol: float = 1e-12) -> bool:
    """Return True when intervention ``a`` componentwise dominates ``b``."""
    if len(a) != len(b) or not a:
        raise ValueError("vertices must have the same nonzero dimension")
    ge_all = all(x + tol >= y for x, y in zip(a, b))
    gt_any = any(x > y + tol for x, y in zip(a, b))
    return ge_all and gt_any


def pareto_maximal_vertex_indices(vertices: Iterable[Sequence[float]]) -> tuple[int, ...]:
    points = tuple(tuple(float(x) for x in v) for v in vertices)
    if not points:
        raise ValueError("at least one vertex is required")
    dim = len(points[0])
    if dim == 0 or any(len(v) != dim for v in points):
        raise ValueError("all vertices must have the same nonzero dimension")

    maximal: list[int] = []
    for i, vertex in enumerate(points):
        if not any(
            j != i and dominates(other, vertex)
            for j, other in enumerate(points)
        ):
            maximal.append(i)
    return tuple(maximal)


def pareto_maximal_vertices(vertices: Iterable[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    points = tuple(tuple(float(x) for x in v) for v in vertices)
    indices = pareto_maximal_vertex_indices(points)
    return tuple(points[i] for i in indices)
