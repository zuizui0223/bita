from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "simulate_pedicularis_focal_design_sensitivity.py"
CONFIG = ROOT / "empirical" / "identification_design" / "PEDICULARIS_FOCAL_DESIGN_SENSITIVITY_CONFIG_V1.json"

SPEC = importlib.util.spec_from_file_location("pedicularis_design_sensitivity", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_small_grid_returns_design_only_guard() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    cfg["base"]["simulation_reps"] = 100
    cfg["grid"] = {"n_plants": [10], "n_x_levels": [5], "residual_sd": [1.0]}
    result = MODULE.run_grid(cfg)
    assert result["status"] == "DESIGN_SENSITIVITY_ONLY_NOT_EMPIRICAL_EVIDENCE"
    assert len(result["results"]) == 1
    row = result["results"][0]
    assert row["n_plants"] == 10
    assert row["n_x_levels"] == 5
    assert 0.0 <= row["sign_recovery_frequency"] <= 1.0
    assert 0.0 <= row["both_optima_interior_frequency"] <= 1.0


def test_more_replication_is_not_encoded_as_biological_evidence() -> None:
    cfg = {
        "base": {
            "simulation_reps": 100,
            "random_seed": 7,
            "flowers_per_plant_cell": 1,
            "plant_sd": 0.0,
            "curvature": 1.0,
            "sch_reference": 1.0,
            "x0_true": 0.0,
            "x1_true": 0.5,
            "y1_peak_gain": 0.2,
            "x_min": -1.0,
            "x_max": 1.0
        },
        "grid": {"n_plants": [10, 40], "n_x_levels": [5], "residual_sd": [1.0]}
    }
    result = MODULE.run_grid(cfg)
    assert "not empirical evidence" in result["interpretation_guard"].lower()
    assert {row["n_plants"] for row in result["results"]} == {10, 40}
