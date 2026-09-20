"""Small dependency-free numerical helpers shared across BITA analyses."""
from __future__ import annotations

import math
import statistics
from typing import Literal, Sequence


def _gauss_jordan_inverse(
    rows: list[list[float]],
    *,
    tol: float,
    singular_message: str,
    ridge: float,
) -> list[list[float]]:
    """Invert an already equilibrated matrix.

    Ridge is applied in the equilibrated coordinate system. This makes the
    regularization dimensionless and invariant to harmless changes of units.
    """

    n = len(rows)
    work = [
        row[:] + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(rows)
    ]
    if ridge:
        for i in range(n):
            work[i][i] += ridge

    scale = max(abs(value) for row in rows for value in row)
    if scale == 0.0:
        raise ValueError(singular_message)
    threshold = tol * max(1.0, scale)

    for column in range(n):
        pivot_row = max(range(column, n), key=lambda r: abs(work[r][column]))
        if abs(work[pivot_row][column]) <= threshold:
            raise ValueError(singular_message)
        work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            factor = work[row][column]
            if factor == 0.0:
                continue
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[column])
            ]
    return [row[n:] for row in work]


def invert_matrix(
    matrix: Sequence[Sequence[float]],
    *,
    tol: float = 1e-12,
    ridge: float = 0.0,
    singular_message: str = "matrix is singular or numerically rank deficient",
) -> list[list[float]]:
    """Invert a square matrix after row/column equilibration.

    The previous implementation compared every pivot with a threshold based on
    the single largest entry in the matrix. With an intercept, that made the
    rank decision depend on the units of a much smaller slope column.

    For symmetric matrices (the dominant BITA use: X'X, X'WX, covariance
    blocks), diagonal equilibration maps A to a unit-diagonal scale before
    pivoting. Rescaling one design column rescales the corresponding row and
    column of its Gram matrix but leaves the equilibrated matrix unchanged.

    A nonsymmetric fallback performs explicit row and column max-norm
    equilibration. Ridge is dimensionless because it is added only after
    equilibration; it therefore cannot become stronger or weaker merely
    because a predictor is measured in different units.
    """

    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    rows = [list(map(float, row)) for row in matrix]
    if any(not math.isfinite(value) for row in rows for value in row):
        raise ValueError("matrix values must be finite")
    if tol <= 0 or not math.isfinite(tol):
        raise ValueError("tol must be positive and finite")
    if ridge < 0 or not math.isfinite(ridge):
        raise ValueError("ridge must be non-negative and finite")

    overall = max(abs(value) for row in rows for value in row)
    if overall == 0.0:
        raise ValueError(singular_message)

    symmetry_tol = 100.0 * math.ulp(overall)
    symmetric = all(
        abs(rows[i][j] - rows[j][i]) <= symmetry_tol
        for i in range(n)
        for j in range(i + 1, n)
    )

    if symmetric and all(rows[i][i] != 0.0 for i in range(n)):
        scales = [math.sqrt(abs(rows[i][i])) for i in range(n)]
        if all(math.isfinite(scale) and scale > 0.0 for scale in scales):
            balanced = [
                [rows[i][j] / (scales[i] * scales[j]) for j in range(n)]
                for i in range(n)
            ]
            inverse_balanced = _gauss_jordan_inverse(
                balanced,
                tol=tol,
                singular_message=singular_message,
                ridge=ridge,
            )
            return [
                [
                    inverse_balanced[i][j] / (scales[i] * scales[j])
                    for j in range(n)
                ]
                for i in range(n)
            ]

    row_scales = [max(abs(value) for value in row) for row in rows]
    if any(scale == 0.0 for scale in row_scales):
        raise ValueError(singular_message)
    row_balanced = [
        [rows[i][j] / row_scales[i] for j in range(n)]
        for i in range(n)
    ]
    col_scales = [
        max(abs(row_balanced[i][j]) for i in range(n))
        for j in range(n)
    ]
    if any(scale == 0.0 for scale in col_scales):
        raise ValueError(singular_message)
    balanced = [
        [row_balanced[i][j] / col_scales[j] for j in range(n)]
        for i in range(n)
    ]
    inverse_balanced = _gauss_jordan_inverse(
        balanced,
        tol=tol,
        singular_message=singular_message,
        ridge=ridge,
    )
    return [
        [
            inverse_balanced[i][j] / (col_scales[i] * row_scales[j])
            for j in range(n)
        ]
        for i in range(n)
    ]


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


def pearson(
    x: Sequence[float],
    y: Sequence[float],
    *,
    mean_method: Literal["sum", "fmean"] = "sum",
    denominator_method: Literal["separate", "joint"] = "separate",
    zero_variance: Literal["zero", "nan"] = "zero",
) -> float:
    """Pearson correlation with explicit floating-point evaluation contract.

    The options preserve exact historical BITA receipts while centralizing the
    implementation. Mathematically equivalent evaluation orders can differ by
    one ULP, which matters for frozen-result reproducibility checks.
    """

    if len(x) != len(y) or len(x) < 2:
        raise ValueError("pearson requires equal-length vectors with at least two values")
    if mean_method == "fmean":
        mx, my = statistics.fmean(x), statistics.fmean(y)
    else:
        mx, my = mean(x), mean(y)

    dx_values = [a - mx for a in x]
    dy_values = [b - my for b in y]
    numerator = sum(a * b for a, b in zip(dx_values, dy_values))
    ssx = sum(value * value for value in dx_values)
    ssy = sum(value * value for value in dy_values)
    if ssx == 0.0 or ssy == 0.0:
        return math.nan if zero_variance == "nan" else 0.0

    if denominator_method == "joint":
        denominator = math.sqrt(ssx * ssy)
    else:
        denominator = math.sqrt(ssx) * math.sqrt(ssy)

    value = numerator / denominator
    if math.isclose(value, 1.0, rel_tol=0.0, abs_tol=1e-15):
        return 1.0
    if math.isclose(value, -1.0, rel_tol=0.0, abs_tol=1e-15):
        return -1.0
    return value


def spearman(
    x: Sequence[float],
    y: Sequence[float],
    *,
    mean_method: Literal["sum", "fmean"] = "sum",
    denominator_method: Literal["separate", "joint"] = "separate",
    zero_variance: Literal["zero", "nan"] = "zero",
) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("spearman requires equal-length vectors with at least two values")
    return pearson(
        rankdata(x),
        rankdata(y),
        mean_method=mean_method,
        denominator_method=denominator_method,
        zero_variance=zero_variance,
    )
