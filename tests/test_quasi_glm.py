from __future__ import annotations

from math import isfinite

import pytest

from trait_architecture.quasi_glm import fit_quasi_glm


def test_poisson_log_recovers_positive_linear_signal() -> None:
    design = [[1.0, value] for value in (-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5)]
    response = [0.0, 1.0, 1.0, 2.0, 3.0, 5.0, 7.0, 12.0]
    result = fit_quasi_glm(response, design, ["Intercept", "x"], family="poisson_log")
    assert result.converged
    assert result.n == len(response)
    assert result.cluster_count == len(response)
    slope = result.coefficients[1]
    assert slope.estimate > 0
    assert slope.exp_estimate > 1
    assert isfinite(result.pearson_dispersion)


def test_fractional_logit_supports_zeroes_and_clustered_scores() -> None:
    design = [[1.0, value] for value in (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0)]
    response = [0.0, 0.02, 0.05, 0.15, 0.34, 0.58, 0.75, 0.90]
    clusters = ["a", "a", "b", "b", "c", "c", "d", "d"]
    result = fit_quasi_glm(response, design, ["Intercept", "x"], family="fractional_logit", clusters=clusters)
    assert result.converged
    assert result.cluster_count == 4
    assert result.coefficients[1].estimate > 0
    assert result.coefficients[1].robust_se > 0


def test_invalid_fractional_response_is_rejected() -> None:
    with pytest.raises(ValueError, match="responses in \[0, 1\]"):
        fit_quasi_glm([0.1, 1.2, 0.4], [[1.0], [1.0], [1.0]], ["Intercept"], family="fractional_logit")
