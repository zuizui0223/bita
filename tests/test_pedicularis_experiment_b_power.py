import json
from pathlib import Path

import pytest

from scripts.simulate_pedicularis_experiment_b_power import _worldline_resolved, generate_rows, simulate_power


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEDICULARIS_EXPERIMENT_B_POWER_CONFIG_TEMPLATE_V1.json"


def _config() -> dict:
    return {
        "status": "FROZEN_SYNTHETIC_TEST_ONLY",
        "candidate_plants_per_cell": [6],
        "simulation_reps": 1,
        "simulation_seed": 29,
        "target_joint_power": 0.8,
        "target_worldline_state": "BITA",
        "generating_model": {
            "x_levels": [-2, -1, 0, 1, 2],
            "sch_pollinator_reference": 2.0,
            "sch_combined_reference": 0.0,
            "fitness_peak_y0": 60.0,
            "fitness_peak_y1": 65.0,
            "fitness_optimum_y0": 0.0,
            "fitness_optimum_y1": 1.0,
            "fitness_curvature_y0": 1.0,
            "fitness_curvature_y1": 1.0,
            "between_plant_sd": 0.0,
            "residual_sd": 0.0,
            "ovule_count": 100.0,
            "damaged_seed_mean_y0": 20.0,
            "damaged_seed_mean_y1": 3.0,
            "damaged_seed_sd": 0.0,
            "pollen_peak": 100.0,
            "pollen_optimum": 2.0,
            "pollen_curvature": 1.0,
            "y_cross_effect_on_pollen": 0.0,
            "water_depth_y1": 10.0,
            "water_depth_sd": 0.0,
            "mechanical_damage_rate": 0.0
        },
        "production_bita_config": {
            "bita_release": {
                "bootstrap_reps": 200,
                "random_seed": 31,
                "min_x_levels": 5,
                "min_valid_bootstrap_fraction": 0.8,
                "sch_reference_mode": "state_specific",
                "min_dimensional_release": 0.5,
                "min_within_bita_fitness_gain": 3.0,
                "min_y_function2_gain": 0.1,
                "max_y_function1_penalty": 0.1,
                "min_y1_interior_bootstrap_fraction": 0.8,
                "x_to_sch_multiplier": 1.0,
                "x_to_sch_offset": 0.0
            }
        }
    }


def test_template_is_fail_closed() -> None:
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["target_worldline_state"] == "REQUIRED_BEFORE_USE"


def test_generator_preserves_ten_cell_complete_block() -> None:
    import random

    config = _config()
    rows = generate_rows(config["generating_model"], 3, random.Random(1))
    assert len(rows) == 3 * 5 * 2
    assert len({row["plant_id"] for row in rows}) == 3
    assert {row["water_treatment"] for row in rows} == {"DRAINED", "PROTECTED"}


def test_strong_synthetic_bita_scenario_passes_joint_production_pipeline() -> None:
    result = simulate_power(_config())
    row = result["candidate_results"][0]
    assert row["release_gate_power"] == 1.0
    assert row["preferential_loading_power"] == 1.0
    assert row["released_surface_interior_power"] == 1.0
    assert row["direct_worldline_order_power"] == 1.0
    assert row["joint_primary_gate_power"] == 1.0
    assert row["registered_bita_positive_gate_power"] == 1.0
    assert result["minimum_candidate_meeting_target"] == 6


def test_worldline_resolution_supports_balance_and_bita_planning_scenarios() -> None:
    assert _worldline_resolved([-3.0, -1.0], "BALANCE")
    assert not _worldline_resolved([-3.0, 1.0], "BALANCE")
    assert _worldline_resolved([1.0, 3.0], "BITA")
    assert not _worldline_resolved([-1.0, 3.0], "BITA")


def test_unfrozen_template_is_rejected() -> None:
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="fully frozen"):
        simulate_power(config)
