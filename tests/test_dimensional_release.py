from __future__ import annotations

import pytest

from trait_architecture.dimensional_release import analyze_dimensional_release


def _sch_receipt() -> dict:
    return {
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "observed_estimands": {
            "z_pollinator_context": 2.0,
            "z_antagonist_context": -2.0,
            "z_combined": 0.0,
        },
    }


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 5,
        "min_x_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "sch_reference_mode": "state_specific",
        "min_dimensional_release": 0.5,
        "min_within_bita_fitness_gain": 1.0,
        "min_y_function2_gain": 1.0,
        "max_y_function1_penalty": 0.5,
        "min_y1_interior_bootstrap_fraction": 0.9,
        "x_to_sch_multiplier": 1.0,
        "x_to_sch_offset": 0.0,
    }


def _rows(released: bool = True) -> list[dict[str, str]]:
    rows = []
    y1_optimum = 1.5 if released else -1.0
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
                        "x_measured": str(float(x)),
                        "y_state": str(y),
                        "function1_value": f"{function1 + plant_effect:.4f}",
                        "function2_value": f"{function2 + plant_effect:.4f}",
                        "fitness_value": f"{fitness + plant_effect:.4f}",
                    }
                )
    return rows


def test_positive_dimensional_release_uses_state_specific_reference_by_default() -> None:
    result = analyze_dimensional_release(_rows(True), _sch_receipt(), _config())
    assert result["status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED"
    assert all(result["decisions"].values())
    assert result["sch_reference"]["reference_type"] == "STATE_SPECIFIC_P1G0_OPTIMUM"
    assert result["sch_reference"]["source_field"] == "observed_estimands.z_pollinator_context"
    assert "not automatically pure z_F1*" in result["sch_reference"]["interpretation"]
    est = result["observed_estimands"]
    assert abs(est["x_optimum_y0"]) < 1e-8
    assert abs(est["x_optimum_y1"] - 1.5) < 1e-8
    assert est["dimensional_release"] > 1.0
    assert est["within_bita_optimum_fitness_gain"] > 4.0
    assert est["y_effect_function2"] > 4.0
    assert abs(est["y_effect_function1"]) < 1e-8
    assert result["delta_mod_status"].startswith("NOT_IDENTIFIED")


def test_shift_away_from_sch_reference_is_not_called_functional_release() -> None:
    result = analyze_dimensional_release(_rows(False), _sch_receipt(), _config())
    assert result["decisions"]["x_optimum_released_toward_sch_reference"] is False
    assert result["status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_NOT_FULLY_RECOVERED"


def test_sch_positive_receipt_is_required() -> None:
    receipt = _sch_receipt()
    receipt["status"] = "COMPROMISE_CRITERIA_NOT_ALL_RECOVERED"
    with pytest.raises(ValueError, match="positive causal-compromise"):
        analyze_dimensional_release(_rows(True), receipt, _config())


def test_pure_function_mode_fails_closed_without_independent_sch_optimum() -> None:
    config = _config()
    config["sch_reference_mode"] = "pure_function"
    with pytest.raises(ValueError, match="identified_pure_function_optima.z_F1"):
        analyze_dimensional_release(_rows(True), _sch_receipt(), config)


def test_pure_function_mode_uses_explicit_independent_reference() -> None:
    config = _config()
    config["sch_reference_mode"] = "pure_function"
    receipt = _sch_receipt()
    receipt["identified_pure_function_optima"] = {"z_F1": 2.0}
    result = analyze_dimensional_release(_rows(True), receipt, config)
    assert result["sch_reference"]["reference_type"] == "PURE_FUNCTION_F1_OPTIMUM_INDEPENDENTLY_IDENTIFIED"
    assert result["sch_reference"]["source_field"] == "identified_pure_function_optima.z_F1"
    assert result["status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED"
