import random

from scripts.extract_pedicularis_experiment_b_pilot_parameters import extract
from scripts.simulate_pedicularis_experiment_b_power import generate_rows


def _model() -> dict:
    return {
        "x_levels": [-2, -1, 0, 1, 2],
        "sch_pollinator_reference": 2.0,
        "sch_combined_reference": 0.0,
        "fitness_peak_y0": 60.0,
        "fitness_peak_y1": 65.0,
        "fitness_optimum_y0": 0.0,
        "fitness_optimum_y1": 1.0,
        "fitness_curvature_y0": 1.0,
        "fitness_curvature_y1": 1.0,
        "between_plant_sd": 2.0,
        "residual_sd": 3.0,
        "ovule_count": 100.0,
        "damaged_seed_mean_y0": 20.0,
        "damaged_seed_mean_y1": 3.0,
        "damaged_seed_sd": 1.0,
        "pollen_peak": 100.0,
        "pollen_optimum": 2.0,
        "pollen_curvature": 1.0,
        "y_cross_effect_on_pollen": 0.0,
        "water_depth_y1": 10.0,
        "water_depth_sd": 0.3,
        "mechanical_damage_rate": 0.0,
    }


def test_pilot_receipt_is_descriptive_and_power_only() -> None:
    rows = generate_rows(_model(), 8, random.Random(13))
    result = extract(rows)
    assert result["receipt_schema_version"] == "PEDICULARIS_EXPERIMENT_B_PILOT_PARAMETERS_V1"
    assert result["status"] == "DESCRIPTIVE_PILOT_ONLY_NOT_BIOLOGICAL_TEST"
    assert result["n_plants"] == 8
    assert len(result["realized_x_by_assigned_level"]) == 5
    assert result["pooled_within_cell_fitness_variance"] > 0
    assert result["manipulation_performance"]["water_depth_separation"] > 5
    assert result["manipulation_performance"]["mean_damaged_seeds_y1"] < result["manipulation_performance"]["mean_damaged_seeds_y0"]
    assert result["power_config_draft"]["effect_geometry_status"].startswith("REQUIRES_")
    assert "do not test BALANCE/BITA biology" in result["claim_ceiling"]


def test_residualized_cluster_component_is_available_for_complete_block() -> None:
    rows = generate_rows(_model(), 8, random.Random(17))
    result = extract(rows)
    components = result["residualized_cluster_components"]
    assert components["balanced_cluster_estimate_available"] is True
    assert components["rows_per_plant"] == 10
    assert components["between_plant_variance_component"] is not None
    assert components["within_plant_residual_variance"] is not None
