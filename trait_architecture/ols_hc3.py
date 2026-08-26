"""Narrow dependency-free OLS with HC3 covariance for registered retrofits.

This helper exists so source-audited public-data reanalyses do not depend on a
large numerical stack. It fits only caller-declared complete-case linear models;
it performs no model selection or transformation search.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import erf, isfinite, sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class OlsCoefficient:
    term: str
    estimate: float
    hc3_se: float
    z_value: float
    p_value_normal: float
    ci95_lower: float
    ci95_upper: float


@dataclass(frozen=True)
class OlsResult:
    n: int
    parameter_count: int
    residual_df: int
    r_squared: float
    coefficients: tuple[OlsCoefficient, ...]


def _identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _transpose(m: Sequence[Sequence[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*m)]


def _matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> list[list[float]]:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("matrix dimensions do not align")
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _matvec(m: Sequence[Sequence[float]], v: Sequence[float]) -> list[float]:
    if not m or len(m[0]) != len(v):
        raise ValueError("matrix/vector dimensions do not align")
    return [sum(row[i] * v[i] for i in range(len(v))) for row in m]


def _invert(m: Sequence[Sequence[float]], *, tol: float = 1e-12) -> list[list[float]]:
    n = len(m)
    if n == 0 or any(len(row) != n for row in m):
        raise ValueError("matrix must be non-empty and square")
    aug = [list(map(float, row)) + identity for row, identity in zip(m, _identity(n))]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) <= tol:
            raise ValueError("design matrix is singular or numerically rank deficient")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def _p_two_sided_normal(z: float) -> float:
    return max(0.0, min(1.0, 1.0 - erf(abs(z) / sqrt(2.0))))


def fit_ols_hc3(y: Iterable[float], design: Iterable[Iterable[float]], terms: Sequence[str]) -> OlsResult:
    response = [float(x) for x in y]
    x = [list(map(float, row)) for row in design]
    if not response or len(response) != len(x):
        raise ValueError("response and design must contain the same non-zero number of rows")
    if not terms or any(len(row) != len(terms) for row in x):
        raise ValueError("design rows must match terms")
    if any(not isfinite(v) for v in response) or any(not isfinite(v) for row in x for v in row):
        raise ValueError("all values must be finite")
    n = len(response)
    p = len(terms)
    if n <= p:
        raise ValueError("OLS requires more observations than parameters")

    xt = _transpose(x)
    xtx_inv = _invert(_matmul(xt, x))
    beta = _matvec(xtx_inv, _matvec(xt, response))
    fitted = _matvec(x, beta)
    residuals = [obs - pred for obs, pred in zip(response, fitted)]
    mean_y = sum(response) / n
    tss = sum((v - mean_y) ** 2 for v in response)
    rss = sum(e * e for e in residuals)
    r2 = 1.0 - rss / tss if tss > 0 else 0.0

    meat = [[0.0 for _ in range(p)] for _ in range(p)]
    for row, residual in zip(x, residuals):
        h = sum(row[i] * xtx_inv[i][j] * row[j] for i in range(p) for j in range(p))
        denom = max(1e-12, 1.0 - h)
        weight = (residual / denom) ** 2
        for i in range(p):
            for j in range(p):
                meat[i][j] += weight * row[i] * row[j]
    cov = _matmul(_matmul(xtx_inv, meat), xtx_inv)

    coefficients = []
    for i, term in enumerate(terms):
        se = sqrt(max(0.0, cov[i][i]))
        z = beta[i] / se if se > 0 else float("nan")
        p_value = _p_two_sided_normal(z) if isfinite(z) else float("nan")
        coefficients.append(OlsCoefficient(
            term=term,
            estimate=beta[i],
            hc3_se=se,
            z_value=z,
            p_value_normal=p_value,
            ci95_lower=beta[i] - 1.96 * se,
            ci95_upper=beta[i] + 1.96 * se,
        ))
    return OlsResult(
        n=n,
        parameter_count=p,
        residual_df=n - p,
        r_squared=r2,
        coefficients=tuple(coefficients),
    )
