from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

REQUIRED_THRESHOLDS = {
    "min_dimensional_release": (0.0, None),
    "min_within_bita_fitness_gain": (0.0, None),
    "min_y_function2_gain": (0.0, 1.0),
    "max_y_function1_penalty": (0.0, None),
    "min_y1_interior_bootstrap_fraction": (0.0, 1.0),
}
REQUIRED_META = ("value", "unit", "source_type", "source_reference", "biological_interpretation")


def _finite(value: object, name: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def validate_receipt(receipt: dict) -> dict[str, float]:
    if receipt.get("system") != "Pedicularis rex":
        raise ValueError("system must be 'Pedicularis rex'")
    for field in ("population_id", "season_id", "freeze_date"):
        if not str(receipt.get(field, "")).strip():
            raise ValueError(f"missing {field}")
    if receipt.get("focal_data_inspected") is not False:
        raise ValueError("thresholds must be frozen before focal outcome data are inspected")
    sources = receipt.get("calibration_sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("at least one calibration source is required")

    raw = receipt.get("thresholds")
    if not isinstance(raw, dict):
        raise ValueError("thresholds must be an object")

    out: dict[str, float] = {}
    for name, (lower, upper) in REQUIRED_THRESHOLDS.items():
        record = raw.get(name)
        if not isinstance(record, dict):
            raise ValueError(f"missing threshold record {name}")
        for meta in REQUIRED_META:
            if meta == "value":
                continue
            if not str(record.get(meta, "")).strip():
                raise ValueError(f"{name}.{meta} is required")
        value = _finite(record.get("value"), name)
        if value < lower:
            raise ValueError(f"{name} must be >= {lower}")
        if upper is not None and value > upper:
            raise ValueError(f"{name} must be <= {upper}")
        out[name] = value
    return out


def freeze(receipt: dict) -> dict:
    thresholds = validate_receipt(receipt)
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "bita_release": {
            "bootstrap_reps": 2000,
            "random_seed": 20260904,
            "min_x_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "sch_reference_mode": "state_specific",
            **thresholds,
            "x_to_sch_multiplier": 1.0,
            "x_to_sch_offset": 0.0,
        },
        "freeze_provenance": {
            "system": receipt["system"],
            "population_id": receipt["population_id"],
            "season_id": receipt["season_id"],
            "freeze_date": receipt["freeze_date"],
            "focal_data_inspected": False,
            "calibration_receipt_sha256": digest,
        },
        "status": "FROZEN_BEFORE_FOCAL_OUTCOME_ANALYSIS",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Freeze Pedicularis BITA focal thresholds prospectively")
    parser.add_argument("calibration_receipt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = json.loads(args.calibration_receipt.read_text(encoding="utf-8"))
    payload = json.dumps(freeze(receipt), indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
