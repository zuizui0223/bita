from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "freeze_pedicularis_focal_thresholds.py"
SPEC = importlib.util.spec_from_file_location("freeze_pedicularis", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def receipt():
    thresholds = {}
    values = {
        "min_dimensional_release": 0.2,
        "min_within_bita_fitness_gain": 1.0,
        "min_y_function2_gain": 0.05,
        "max_y_function1_penalty": 10.0,
        "min_y1_interior_bootstrap_fraction": 0.8,
    }
    for name, value in values.items():
        thresholds[name] = {
            "value": value,
            "unit": "registered_unit",
            "source_type": "independent_pilot",
            "source_reference": "pilot_receipt_v1",
            "biological_interpretation": "prospectively declared meaningful threshold",
        }
    return {
        "system": "Pedicularis rex",
        "population_id": "POP1",
        "season_id": "2027",
        "freeze_date": "2027-01-15",
        "focal_data_inspected": False,
        "calibration_sources": [{"source_type": "independent_pilot", "source_reference": "pilot_receipt_v1", "scope": "pre-focal"}],
        "thresholds": thresholds,
    }


def test_freeze_emits_runnable_numeric_config_with_hash():
    out = MODULE.freeze(receipt())
    assert out["status"] == "FROZEN_BEFORE_FOCAL_OUTCOME_ANALYSIS"
    assert out["bita_release"]["min_x_levels"] == 5
    assert out["bita_release"]["min_dimensional_release"] == 0.2
    assert len(out["freeze_provenance"]["calibration_receipt_sha256"]) == 64


def test_rejects_posthoc_freeze():
    item = receipt()
    item["focal_data_inspected"] = True
    with pytest.raises(ValueError, match="before focal outcome data"):
        MODULE.freeze(item)


def test_rejects_missing_provenance():
    item = receipt()
    item["thresholds"]["min_y_function2_gain"]["source_reference"] = ""
    with pytest.raises(ValueError, match="source_reference"):
        MODULE.freeze(item)


def test_rejects_invalid_fraction():
    item = receipt()
    item["thresholds"]["min_y1_interior_bootstrap_fraction"]["value"] = 1.1
    with pytest.raises(ValueError, match="must be <= 1.0"):
        MODULE.freeze(item)
