"""Small dependency-free quasi-GLM engine for predeclared response-scale models.

Supported canonical-link models:

- ``poisson_log`` for non-negative count/rate responses;
- ``fractional_logit`` for responses on [0, 1], including exact zeros and ones.

Inference uses a sandwich covariance matrix. Repeated observations can be clustered
(e.g. flower or fruit records within a plant) with a finite-cluster correction. This
is deliberately a narrowly scoped analysis utility: it does not select models,
search transformations, estimate random effects, or convert associations into causal
claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, erf, isfinite, log, sqrt
from typing import Iterable, Sequence

from trait_architecture.standardized_ols import _invert, _matmul, _matvec, _transpose


EPSILON = 1e-12
MAX_ETA = 30.0


@dataclass(frozen=True)
class QuasiGlmCoefficient:
    term: str
    estimate: float
    robust_se: float
    z_value: float
    p_value_normal: float
    ci95_lower: float
    ci95_upper: float
    exp_estimate: float
    exp_ci95_lower: float
    exp_ci95_upper: float


@dataclass(frozen=True)
class QuasiGlmResult:
    family: str
    n: int
    parameter_count: int
    residual_df: int
    cluster_count: int
    iterations: int
    converged: bool
    mean_response: float
    pearson_dispersion: float
    coefficients: tuple[QuasiGlmCoefficient, ...]


def _normal_two_sided_p(z_value: float) -> float:
    return max(0.0, min(1.0, 1.0 - erf(abs(z_value) / sqrt(2.0))))


def _validate_inputs(
    y: Iterable[float],
    design: Iterable[Iterable[float]],
    terms: Sequence[str],
    clusters: Iterable[str] | None,
) -> tuple[list[float], list[list[float]], list[str], list[str] | None]:
    response = [float(value) for value in y]
    matrix = [list(map(float, row)) for row in design]
    labels = list(terms)
    cluster_labels = list(clusters) if clusters is not None else None
    if not response or len(response) != len(matrix):
        raise ValueError("response and design must contain the same non-zero number of rows")
    if not labels or any(len(row) != len(labels) for row in matrix):
        raise ValueError("every design row must match supplied terms")
    if len(response) <= len(labels):
        raise ValueError("GLM requires more rows than parameters")
    if any(not isfinite(value) for value in response) or any(
        not isfinite(value) for row in matrix for value in row
    ):
        raise ValueError("response and design must be finite")
    if cluster_labels is not None and len(cluster_labels) != len(response):
        raise ValueError("clusters must be omitted or match response length")
    return response, matrix, labels, cluster_labels


def _mean_and_weight(family: str, eta: float) -> tuple[float, float, float]:
    eta = min(MAX_ETA, max(-MAX_ETA, eta))
    if family == "poisson_log":
        mean = max(EPSILON, exp(eta))
        derivative = mean
        weight = mean
    elif family == "fractional_logit":
        mean = 1.0 / (1.0 + exp(-eta))
        mean = min(1.0 - EPSILON, max(EPSILON, mean))
        derivative = mean * (1.0 - mean)
        weight = derivative
    else:
        raise ValueError("family must be poisson_log or fractional_logit")
    return mean, derivative, weight


def _initial_beta(family: str, response: list[float], parameter_count: int) -> list[float]:
    mean = sum(response) / len(response)
    if family == "poisson_log":
        intercept = log(max(EPSILON, mean))
    elif family == "fractional_logit":
        bounded = min(1.0 - EPSILON, max(EPSILON, mean))
        intercept = log(bounded / (1.0 - bounded))
    else:
        raise ValueError("family must be poisson_log or fractional_logit")
    return [intercept] + [0.0] * (parameter_count - 1)


def _weighted_crossproduct(matrix: list[list[float]], weights: list[float]) -> list[list[float]]:
    parameter_count = len(matrix[0])
    result = [[0.0 for _ in range(parameter_count)] for _ in range(parameter_count)]
    for row, weight in zip(matrix, weights):
        for left in range(parameter_count):
            for right in range(parameter_count):
                result[left][right] += weight * row[left] * row[right]
    return result


def _weighted_response(matrix: list[list[float]], weights: list[float], adjusted: list[float]) -> list[float]:
    return [
        sum(weight * row[column] * value for row, weight, value in zip(matrix, weights, adjusted))
        for column in range(len(matrix[0]))
    ]


def _cluster_meat(matrix: list[list[float]], residuals: list[float], clusters: list[str] | None) -> tuple[list[list[float]], int]:
    parameter_count = len(matrix[0])
    if clusters is None:
        grouped = {str(index): [index] for index in range(len(matrix))}
    else:
        grouped: dict[str, list[int]] = {}
        for index, label in enumerate(clusters):
            grouped.setdefault(str(label), []).append(index)
    meat = [[0.0 for _ in range(parameter_count)] for _ in range(parameter_count)]
    for indices in grouped.values():
        score = [0.0 for _ in range(parameter_count)]
        for index in indices:
            for column in range(parameter_count):
                score[column] += matrix[index][column] * residuals[index]
        for left in range(parameter_count):
            for right in range(parameter_count):
                meat[left][right] += score[left] * score[right]
    return meat, len(grouped)


def _correction(n: int, parameter_count: int, cluster_count: int) -> float:
    if n <= parameter_count:
        return 1.0
    base = (n - 1.0) / (n - parameter_count)
    if cluster_count > 1:
        return base * cluster_count / (cluster_count - 1.0)
    return base


def fit_quasi_glm(
    y: Iterable[float],
    design: Iterable[Iterable[float]],
    terms: Sequence[str],
    *,
    family: str,
    clusters: Iterable[str] | None = None,
    max_iterations: int = 100,
    tolerance: float = 1e-9,
) -> QuasiGlmResult:
    """Fit a declared canonical-link quasi-GLM with robust sandwich covariance."""

    response, matrix, labels, cluster_labels = _validate_inputs(y, design, terms, clusters)
    if family == "poisson_log" and any(value < 0 for value in response):
        raise ValueError("poisson_log requires non-negative responses")
    if family == "fractional_logit" and any(value < 0 or value > 1 for value in response):
        raise ValueError("fractional_logit requires responses in [0, 1]")

    beta = _initial_beta(family, response, len(labels))
    converged = False
    final_bread: list[list[float]] | None = None
    final_means: list[float] = []
    for iteration in range(1, max_iterations + 1):
        means: list[float] = []
        derivatives: list[float] = []
        weights: list[float] = []
        eta_values: list[float] = []
        for row in matrix:
            eta = sum(value * coefficient for value, coefficient in zip(row, beta))
            mean, derivative, weight = _mean_and_weight(family, eta)
            eta_values.append(min(MAX_ETA, max(-MAX_ETA, eta)))
            means.append(mean)
            derivatives.append(derivative)
            weights.append(weight)
        adjusted = [eta + (observed - mean) / derivative for eta, observed, mean, derivative in zip(eta_values, response, means, derivatives)]
        bread = _invert(_weighted_crossproduct(matrix, weights))
        beta_new = _matvec(bread, _weighted_response(matrix, weights, adjusted))
        if max(abs(after - before) for after, before in zip(beta_new, beta)) < tolerance:
            beta = beta_new
            final_bread = bread
            final_means = means
            converged = True
            break
        beta = beta_new
    if not converged or final_bread is None:
        raise RuntimeError(f"{family} IRLS did not converge within {max_iterations} iterations")

    # Recompute means and expected information at final beta.
    final_means = []
    final_weights = []
    for row in matrix:
        eta = sum(value * coefficient for value, coefficient in zip(row, beta))
        mean, _derivative, weight = _mean_and_weight(family, eta)
        final_means.append(mean)
        final_weights.append(weight)
    bread = _invert(_weighted_crossproduct(matrix, final_weights))
    residuals = [observed - mean for observed, mean in zip(response, final_means)]
    meat, cluster_count = _cluster_meat(matrix, residuals, cluster_labels)
    correction = _correction(len(response), len(labels), cluster_count)
    covariance = _matmul(_matmul(bread, meat), bread)
    for left in range(len(labels)):
        for right in range(len(labels)):
            covariance[left][right] *= correction

    pearson = 0.0
    for observed, mean in zip(response, final_means):
        variance = mean if family == "poisson_log" else mean * (1.0 - mean)
        pearson += (observed - mean) ** 2 / max(EPSILON, variance)
    residual_df = len(response) - len(labels)
    coefficients: list[QuasiGlmCoefficient] = []
    for index, term in enumerate(labels):
        variance = max(0.0, covariance[index][index])
        se = sqrt(variance)
        z_value = beta[index] / se if se > 0 else float("nan")
        p_value = _normal_two_sided_p(z_value) if isfinite(z_value) else float("nan")
        lower = beta[index] - 1.96 * se
        upper = beta[index] + 1.96 * se
        coefficients.append(QuasiGlmCoefficient(
            term=term,
            estimate=beta[index],
            robust_se=se,
            z_value=z_value,
            p_value_normal=p_value,
            ci95_lower=lower,
            ci95_upper=upper,
            exp_estimate=exp(beta[index]),
            exp_ci95_lower=exp(lower),
            exp_ci95_upper=exp(upper),
        ))
    return QuasiGlmResult(
        family=family,
        n=len(response),
        parameter_count=len(labels),
        residual_df=residual_df,
        cluster_count=cluster_count,
        iterations=iteration,
        converged=True,
        mean_response=sum(response) / len(response),
        pearson_dispersion=pearson / residual_df if residual_df > 0 else float("nan"),
        coefficients=tuple(coefficients),
    )
