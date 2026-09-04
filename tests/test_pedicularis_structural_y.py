from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_structural_y import REQUIRED_FIELDS, evaluate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEDICULARIS_STRUCTURAL_Y_TEMPLATE_V1.csv"
CONFIG = ROOT / "empirical" / "identification_design" / "PEDICULARIS_STRUCTURAL_Y_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "BITA_PEDICULARIS_STRUCTURAL_Y_PROMOTION_V1.md"


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 53,
        "primary_y_field": "retention_capacity_ml",
        "min_plants": 20,
        "min_repeats_per_plant": 2,
        "max_within_plant_y_relative_spread": 0.05,
        "min_among_plant_y_relative_range": 0.4,
        "min_y_to_function2_standardized_beta": 0.25,
        "max_abs_y_to_function1_standardized_beta": 0.15,
        "max_abs_xy_correlation_for_low_coupling": 0.65,
        "max_mechanical_damage_rate": 0.05,
    }


def _rows(cross_effect: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    plant = 0
    for i, x in enumerate((-2, -1, 0, 1, 2)):
        for j in range(5):
            capacity = 10.0 + 2.0 * j
            duration = 4.0 + 0.8 * j
            for round_id, jitter in ((1, -0.01), (2, 0.01)):
                y = capacity * (1.0 + jitter)
                pollen = 100.0 + 8.0 * x + (4.0 * j if cross_effect else 0.0)
                initiated = 100
                undamaged = 48 - 2 * x + 7 * j
                rows.append(
                    {
                        "population_id": "P_REX_STRUCT",
                        "season_id": "S1",
                        "plant_id": f"P{plant:02d}",
                        "unit_id": f"P{plant:02d}_R{round_id}",
                        "measurement_round": str(round_id),
                        "realized_exsertion": str(float(x)),
                        "retention_capacity_ml": f"{y:.5f}",
                        "retention_duration_hours": f"{duration * (1.0 + jitter):.5f}",
                        "bract_top_width_mm": f"{12.0 + 0.4 * j:.4f}",
                        "bract_bottom_width_mm": f"{8.0 + 0.3 * j:.4f}",
                        "bract_height_mm": f"{15.0 + 0.1 * i:.4f}",
                        "pollen_grains": f"{pollen:.4f}",
                        "pollinator_visits": f"{10.0 + x:.4f}",
                        "initiated_seed_count": str(initiated),
                        "undamaged_seed_count": str(undamaged),
                        "early_predator_attack_present": "0" if j >= 3 else "1",
                        "mechanical_damage": "0",
                    }
                )
            plant += 1
    return rows


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert cfg["min_plants"] == "REQUIRED_BEFORE_USE"
    assert cfg["min_y_to_function2_standardized_beta"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in cfg["status"]


def test_repeatable_retention_coordinate_with_preferential_loading_is_promoted() -> None:
    result = evaluate(_rows(False), _config())
    assert result["status"] == "STRUCTURAL_Y_TRAIT_IDENTIFIED_LOW_COUPLING"
    assert all(result["gates"].values())
    assert result["coupling_classification"] == "LOW_COUPLING"
    est = result["observed_estimands"]
    assert est["max_within_plant_y_relative_spread"] < 0.05
    assert est["among_plant_y_relative_range"] > 0.4
    assert abs(est["x_y_correlation"]) < 1e-8
    assert est["y_to_function2_standardized_beta"] > 0.25
    assert abs(est["y_to_function1_standardized_beta"]) < 1e-8


def test_large_pollination_cross_effect_blocks_structural_y_promotion() -> None:
    result = evaluate(_rows(True), _config())
    assert result["gates"]["y_cross_effect_on_function1_bounded"] is False
    assert result["status"] == "STRUCTURAL_Y_TRAIT_NOT_IDENTIFIED"


def test_contract_separates_functional_state_structural_trait_and_history() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "FUNCTIONAL_Y_STATE" in text
    assert "STRUCTURAL_Y_TRAIT" in text
    assert "HISTORICAL_MODULE" in text
    assert "water-holding capacity / retention performance" in text
