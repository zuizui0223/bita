from __future__ import annotations

import math

import pytest

from trait_architecture.context_dependence import _invert as context_invert
from trait_architecture.numerics import invert_matrix, rankdata, spearman
from trait_architecture.ols_hc3 import _invert as ols_invert, fit_ols_hc3


def _assert_matrix_close(a: list[list[float]], b: list[list[float]], tol: float = 1e-9) -> None:
    assert len(a) == len(b)
    for row_a, row_b in zip(a, b):
        assert len(row_a) == len(row_b)
        for x, y in zip(row_a, row_b):
            assert math.isclose(x, y, rel_tol=tol, abs_tol=tol)


def test_inversion_rank_decision_is_scale_relative() -> None:
    matrix = [[4.0, 1.0], [2.0, 3.0]]
    scale = 1e-18
    base = invert_matrix(matrix)
    scaled = invert_matrix([[scale * value for value in row] for row in matrix])
    expected = [[value / scale for value in row] for row in base]
    _assert_matrix_close(scaled, expected, tol=1e-8)

    _assert_matrix_close(ols_invert(matrix), base)
    _assert_matrix_close(context_invert(matrix), base)



def test_inversion_is_invariant_to_tiny_slope_units_with_intercept() -> None:
    base_x = [[1.0, value] for value in [0.0, 1.0, 2.0, 3.0, 4.0]]
    tiny = 1e-10
    tiny_x = [[row[0], tiny * row[1]] for row in base_x]

    def gram(x: list[list[float]]) -> list[list[float]]:
        return [
            [sum(row[i] * row[j] for row in x) for j in range(2)]
            for i in range(2)
        ]

    base_inv = invert_matrix(gram(base_x))
    tiny_inv = invert_matrix(gram(tiny_x))

    assert tiny_inv[0][0] == pytest.approx(base_inv[0][0], rel=1e-12)
    assert tiny_inv[0][1] == pytest.approx(base_inv[0][1] / tiny, rel=1e-12)
    assert tiny_inv[1][0] == pytest.approx(base_inv[1][0] / tiny, rel=1e-12)
    assert tiny_inv[1][1] == pytest.approx(base_inv[1][1] / (tiny * tiny), rel=1e-12)


def test_equilibrated_ridge_is_unit_invariant() -> None:
    base = [[5.0, 10.0], [10.0, 30.0]]
    tiny = 1e-9
    scaled = [
        [base[0][0], tiny * base[0][1]],
        [tiny * base[1][0], tiny * tiny * base[1][1]],
    ]
    ridge = 1e-9
    base_inv = invert_matrix(base, ridge=ridge)
    scaled_inv = invert_matrix(scaled, ridge=ridge)

    assert scaled_inv[0][0] == pytest.approx(base_inv[0][0], rel=1e-10)
    assert scaled_inv[0][1] == pytest.approx(base_inv[0][1] / tiny, rel=1e-10)
    assert scaled_inv[1][0] == pytest.approx(base_inv[1][0] / tiny, rel=1e-10)
    assert scaled_inv[1][1] == pytest.approx(base_inv[1][1] / (tiny * tiny), rel=1e-10)

def test_inversion_rejects_rank_deficiency_independent_of_scale() -> None:
    singular = [[1.0, 2.0], [2.0, 4.0]]
    for scale in (1.0, 1e-18, 1e18):
        matrix = [[scale * value for value in row] for row in singular]
        try:
            invert_matrix(matrix)
        except ValueError:
            pass
        else:
            raise AssertionError("scaled singular matrix must remain singular")


def test_shared_rankdata_and_spearman_preserve_tie_handling() -> None:
    assert rankdata([10.0, 10.0, 20.0, 30.0]) == [1.5, 1.5, 3.0, 4.0]
    assert math.isclose(spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
    assert math.isclose(spearman([1, 2, 3, 4], [40, 30, 20, 10]), -1.0)


def test_hc3_primary_inference_uses_residual_df_student_t() -> None:
    y = [1.0, 2.1, 2.9, 4.2, 5.1, 5.8]
    x = [[1.0, value] for value in [0, 1, 2, 3, 4, 5]]
    result = fit_ols_hc3(y, x, ["intercept", "x"])
    assert result.residual_df == 4
    slope = result.coefficients[1]
    assert math.isclose(slope.t_value, slope.z_value)
    assert slope.p_value_t >= slope.p_value_normal
    half_width = slope.ci95_upper - slope.estimate
    assert half_width > 1.96 * slope.hc3_se
