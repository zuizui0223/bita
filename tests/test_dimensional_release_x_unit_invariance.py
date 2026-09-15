from __future__ import annotations

import math

from trait_architecture.dimensional_release import _fit_quadratic, analyze_dimensional_release


def _quadratic_points(scale: float) -> list[tuple[float, float]]:
    return [
        (scale * x, 10.0 - (x - 0.5) ** 2)
        for x in (-2.0, -1.0, 0.0, 1.0, 2.0)
    ]


def test_quadratic_fit_is_invariant_to_measured_x_units() -> None:
    for scale in (1e-100, 1e-13, 1.0, 1e13, 1e100):
        fit = _fit_quadratic(_quadratic_points(scale))
        assert fit["optimum_class"] == "INTERIOR_CONCAVE"
        assert math.isclose(fit["primary_optimum"], 0.5 * scale, rel_tol=2e-12, abs_tol=0.0)
        assert math.isclose(fit["optimum_value"], 10.0, rel_tol=2e-13, abs_tol=1e-13)
        assert math.isclose(fit["a"], 9.75, rel_tol=2e-12, abs_tol=1e-12)
        assert math.isclose(fit["b"], 1.0 / scale, rel_tol=2e-12, abs_tol=0.0)
        assert math.isclose(fit["c"], -1.0 / (scale * scale), rel_tol=3e-12, abs_tol=0.0)


def test_tiny_distinct_x_values_are_not_collapsed_by_decimal_rounding() -> None:
    fit = _fit_quadratic(_quadratic_points(1e-13))
    assert fit["optimum_class"] == "INTERIOR_CONCAVE"
    assert math.isclose(fit["primary_optimum"], 5e-14, rel_tol=2e-12, abs_tol=0.0)


def test_large_x_units_do_not_materialize_x_fourth_powers() -> None:
    fit = _fit_quadratic(_quadratic_points(1e100))
    assert math.isfinite(fit["primary_optimum"])
    assert math.isfinite(fit["optimum_value"])
    assert math.isclose(fit["primary_optimum"], 5e99, rel_tol=2e-12, abs_tol=0.0)


def test_duplicate_represented_x_values_still_fail_closed() -> None:
    points = [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0), (1.0, 4.0)]
    try:
        _fit_quadratic(points)
    except ValueError as error:
        assert "three distinct measured x values" in str(error)
    else:
        raise AssertionError("duplicate x levels should fail closed")


def _sch_receipt() -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "optimum_semantics": {
            "z_pollinator_context": "STATE_SPECIFIC_P1G0_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F1",
            "z_antagonist_context": "STATE_SPECIFIC_P0G1_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F2",
            "z_combined": "STATE_SPECIFIC_P1G1_COMBINED_REPRODUCTIVE_OPTIMUM",
            "pure_function_optima_identified_by_default": False,
        },
        "observed_estimands": {
            "z_pollinator_context": 2.0,
            "z_antagonist_context": -2.0,
            "z_combined": 0.0,
        },
    }


def _config(scale: float) -> dict:
    return {
        "bootstrap_reps": 200,
        "random_seed": 5,
        "min_x_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "sch_reference_mode": "state_specific",
        "min_dimensional_release": 0.5,
        "min_within_bita_fitness_gain": 1.0,
        "min_y_function2_gain": 1.0,
        "max_y_function1_penalty": 0.5,
        "min_y1_interior_bootstrap_fraction": 0.9,
        "x_to_sch_multiplier": 1.0 / scale,
        "x_to_sch_offset": 0.0,
    }


def _rows(scale: float) -> list[dict[str, str]]:
    rows = []
    y1_optimum = 1.5
    for plant in range(16):
        plant_effect = (plant % 4) * 0.05
        for x in (-2, -1, 0, 1, 2):
            for y in (0, 1):
                if y == 0:
                    fitness = 40.0 - x**2
                else:
                    fitness = 45.0 - (x - y1_optimum) ** 2
                function1 = 30.0 - (x - 2.0) ** 2
                function2 = 20.0 - 0.2 * x + 5.0 * y
                rows.append(
                    {
                        "plant_id": f"P{plant:02d}",
                        "unit_id": f"P{plant:02d}_X{x:+d}_Y{y}",
                        "x_level": f"X{x:+d}",
                        "x_measured": repr(float(x) * scale),
                        "y_state": str(y),
                        "function1_value": f"{function1 + plant_effect:.4f}",
                        "function2_value": f"{function2 + plant_effect:.4f}",
                        "fitness_value": f"{fitness + plant_effect:.4f}",
                    }
                )
    return rows


def test_end_to_end_dimensional_release_is_x_unit_invariant() -> None:
    baseline = analyze_dimensional_release(_rows(1.0), _sch_receipt(), _config(1.0))
    base_est = baseline["observed_estimands"]

    for scale in (1e-13, 1.0, 1e13):
        result = analyze_dimensional_release(_rows(scale), _sch_receipt(), _config(scale))
        est = result["observed_estimands"]
        assert result["status"] == baseline["status"]
        assert result["decisions"] == baseline["decisions"]
        assert math.isclose(est["x_optimum_y0"], base_est["x_optimum_y0"] * scale, rel_tol=1e-10, abs_tol=1e-30)
        assert math.isclose(est["x_optimum_y1"], base_est["x_optimum_y1"] * scale, rel_tol=1e-10, abs_tol=0.0)
        for key in (
            "x_optimum_y0_on_sch_scale",
            "x_optimum_y1_on_sch_scale",
            "distance_to_sch_reference_y0",
            "distance_to_sch_reference_y1",
            "dimensional_release",
            "within_bita_optimum_fitness_gain",
            "y_effect_function1",
            "y_effect_function2",
        ):
            assert math.isclose(est[key], base_est[key], rel_tol=1e-10, abs_tol=1e-10)
        assert result["bootstrap"]["valid_reps"] == baseline["bootstrap"]["valid_reps"]
        assert math.isclose(
            result["bootstrap"]["y1_interior_fraction"],
            baseline["bootstrap"]["y1_interior_fraction"],
            rel_tol=0.0,
            abs_tol=0.0,
        )
