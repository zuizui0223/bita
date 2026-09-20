"""Narrow dependency-free OLS with HC3 covariance for registered retrofits.

This helper exists so source-audited public-data reanalyses do not depend on a
large numerical stack. It fits only caller-declared complete-case linear models;
it performs no model selection or transformation search.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import erf, isfinite, sqrt
from typing import Iterable, Sequence

from trait_architecture.distributions import student_t_quantile_975, student_t_two_sided_p
from trait_architecture.numerics import invert_matrix


@dataclass(frozen=True)
class OlsCoefficient:
    term: str
    estimate: float
    hc3_se: float
    t_value: float
    p_value_t: float
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


def _invert(m: Sequence[Sequence[float]], *, tol: float = 1e-12) -> list[list[float]]:
    return invert_matrix(
        m,
        tol=tol,
        singular_message="design matrix is singular or numerically rank deficient",
    )

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

    residual_df = n - p
    critical = student_t_quantile_975(float(residual_df))

    coefficients = []
    for i, term in enumerate(terms):
        se = sqrt(max(0.0, cov[i][i]))
        t_value = beta[i] / se if se > 0 else float("nan")
        p_value_t = student_t_two_sided_p(t_value, float(residual_df)) if isfinite(t_value) else float("nan")
        # Legacy normal-reference fields are retained for backward-compatible
        # serialized outputs. HC3 inference now uses residual-df Student t.
        z_value = t_value
        p_value_normal = _p_two_sided_normal(z_value) if isfinite(z_value) else float("nan")
        coefficients.append(OlsCoefficient(
            term=term,
            estimate=beta[i],
            hc3_se=se,
            t_value=t_value,
            p_value_t=p_value_t,
            z_value=z_value,
            p_value_normal=p_value_normal,
            ci95_lower=beta[i] - critical * se,
            ci95_upper=beta[i] + critical * se,
        ))
    return OlsResult(
        n=n,
        parameter_count=p,
        residual_df=residual_df,
        r_squared=r2,
        coefficients=tuple(coefficients),
    )
