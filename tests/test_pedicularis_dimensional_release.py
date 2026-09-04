from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_pedicularis_dimensional_release import RAW_FIELDS, analyze, to_bita_rows


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEDICULARIS_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "identification_design" / "PEDICULARIS_DIMENSIONAL_RELEASE_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "BITA_PEDICULARIS_DIMENSIONAL_RELEASE_CONTRACT_V1.md"


def _sch_receipt(population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "analysis": "sch_multilevel_causal_compromise_surface",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
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


def _config() -> dict:
    return {
        "bita_release": {
            "bootstrap_reps": 300,
            "random_seed": 41,
            "min_x_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "sch_reference_mode": "state_specific",
            "min_dimensional_release": 0.5,
            "min_within_bita_fitness_gain": 3.0,
            "min_y_function2_gain": 0.1,
            "max_y_function1_penalty": 0.1,
            "min_y1_interior_bootstrap_fraction": 0.9,
            "x_to_sch_multiplier": 1.0,
            "x_to_sch_offset": 0.0,
        }
    }


def _rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(16):
        for x in (-2, -1, 0, 1, 2):
            for y in (0, 1):
                if y == 0:
                    undamaged = 60 - x**2
                    damaged = 20
                    water = "DRAINED"
                    water_depth = 0
                else:
                    undamaged = 65 - (x - 1) ** 2
                    damaged = 3
                    water = "PROTECTED"
                    water_depth = 10
                pollen = 100 - (x - 2) ** 2
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": "S1",
                        "plant_id": f"P{plant:02d}",
                        "flower_id": f"P{plant:02d}_X{x:+d}_Y{y}",
                        "assigned_x_level": f"X{x:+d}",
                        "realized_exsertion": str(float(x)),
                        "water_treatment": water,
                        "ovule_count": "100",
                        "undamaged_seed_count": str(undamaged),
                        "damaged_seed_count": str(damaged),
                        "pollen_grains": str(pollen),
                        "pollinator_visits": str(10 + x),
                        "water_depth": str(water_depth),
                        "mechanical_damage": "0",
                    }
                )
    return rows


def test_template_and_config_are_registered_fail_closed_inputs() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == RAW_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["bita_release"]["min_dimensional_release"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_pedicularis_water_defence_releases_exsertion_toward_sch_reference() -> None:
    result = analyze(_rows(), _sch_receipt(), _config())
    assert result["status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED"
    assert result["system"] == "Pedicularis rex"
    assert result["system_wrapper_schema_version"] == "BITA_PEDICULARIS_DIMENSIONAL_RELEASE_WRAPPER_V1"
    assert result["pedicularis_mapping"]["y0"].startswith("DRAINED")
    assert result["pedicularis_mapping"]["y1"].startswith("PROTECTED")
    est = result["observed_estimands"]
    assert abs(est["x_optimum_y0"]) < 1e-8
    assert abs(est["x_optimum_y1"] - 1.0) < 1e-8
    assert abs(est["dimensional_release"] - 1.0) < 1e-8
    assert est["within_bita_optimum_fitness_gain"] >= 5.0
    assert est["y_effect_function2"] > 0.1
    assert abs(est["y_effect_function1"]) < 1e-8
    assert all(result["decisions"].values())
    assert result["delta_mod_status"].startswith("NOT_IDENTIFIED")


def test_conversion_orients_both_functions_as_larger_is_better() -> None:
    rows = _rows()[:2]
    converted = to_bita_rows(rows)
    by_y = {row["y_state"]: row for row in converted}
    assert set(by_y) == {"0", "1"}
    assert float(by_y["1"]["function2_value"]) > float(by_y["0"]["function2_value"])
    assert float(by_y["1"]["function1_value"]) == float(by_y["0"]["function1_value"])


def test_sch_context_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="match the population and season"):
        analyze(_rows(), _sch_receipt(season="S2"), _config())


def test_contract_keeps_dimensional_release_below_delta_mod_and_history() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "R_state = |x0* - z_P*| - |x1* - z_P*|" in text
    assert "not as `Delta_mod`" in text
    assert "historical modularization" in text
