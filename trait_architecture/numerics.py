"""Small dependency-free numerical helpers shared across BITA analyses."""
from __future__ import annotations

import math
from typing import Sequence


def invert_matrix(
    matrix: Sequence[Sequence[float]],
    *,
    tol: float = 1e-12,
    singular_message: str = "matrix is singular or numerically rank deficient",
) -> list[list[float]]:
    """Invert a square matrix with scale-relative pivot rejection.

    The tolerance is interpreted relative to the largest absolute entry in the
    original coefficient matrix, so multiplying the entire design by a constant
    does not change the singular/rank-deficient decision.
    """

    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    rows = [list(map(float, row)) for row in matrix]
    if any(not math.isfinite(value) for row in rows for value in row):
        raise ValueError("matrix values must be finite")
    scale = max(abs(value) for row in rows for value in row)
    if scale == 0.0:
        raise ValueError(singular_message)
    threshold = tol * scale

    augmented = [
        row + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(rows)
    ]
    for column in range(n):
        pivot_row = max(range(column, n), key=lambda r: abs(augmented[r][column]))
        if abs(augmented[pivot_row][column]) <= threshold:
            raise ValueError(singular_message)
        augmented[column], augmented[pivot_row] = augmented[pivot_row], augmented[column]
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0.0:
                continue
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [row[n:] for row in augmented]


def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def rankdata(values: Sequence[float]) -> list[float]:
    """Average ranks for ties, using 1-based ranks."""

    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = rank
        i = j
    return ranks


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("pearson requires equal-length vectors with at least two values")
    mx, my = mean(x), mean(y)
    numerator = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    if dx == 0.0 or dy == 0.0:
        return 0.0
    value = numerator / (dx * dy)
    if math.isclose(value, 1.0, rel_tol=0.0, abs_tol=1e-15):
        return 1.0
    if math.isclose(value, -1.0, rel_tol=0.0, abs_tol=1e-15):
        return -1.0
    return value


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("spearman requires equal-length vectors with at least two values")
    return pearson(rankdata(x), rankdata(y))
