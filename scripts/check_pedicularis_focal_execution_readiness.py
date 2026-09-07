from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_THRESHOLDS = (
    "min_dimensional_release",
    "min_within_bita_fitness_gain",
    "min_y_function2_gain",
    "max_y_function1_penalty",
    "min_y1_interior_bootstrap_fraction",
)

REQUIRED_RAW_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "assigned_x_level",
    "realized_exsertion",
    "water_treatment",
    "ovule_count",
    "undamaged_seed_count",
    "damaged_seed_count",
    "pollen_grains",
    "pollinator_visits",
    "water_depth",
    "mechanical_damage",
)

SCH_SCHEMA = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"
SCH_STATUS = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
SCH_WRAPPER = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
SCH_G_SCHEMA = "SCH_PEDICULARIS_PREDATOR_METHOD_V3"
FROZEN_CONFIG_STATUS = "FROZEN_BEFORE_FOCAL_OUTCOME_ANALYSIS"


def _config_gate(path: Path, raw_contexts: list[list[str]]) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    release = config.get("bita_release")
    reasons: list[str] = []
    if not isinstance(release, dict):
        return {"pass": False, "reasons": ["missing bita_release object"]}

    for key in REQUIRED_THRESHOLDS:
        value = release.get(key)
        if value is None:
            reasons.append(f"missing threshold: {key}")
            continue
        if isinstance(value, str) and "REQUIRED_BEFORE_USE" in value:
            reasons.append(f"unfrozen threshold: {key}")
            continue
        try:
            float(value)
        except (TypeError, ValueError):
            reasons.append(f"non-numeric threshold: {key}")

    if config.get("status") != FROZEN_CONFIG_STATUS:
        reasons.append(f"config status must be {FROZEN_CONFIG_STATUS}")

    provenance = config.get("freeze_provenance")
    if not isinstance(provenance, dict):
        reasons.append("missing freeze_provenance")
    else:
        if provenance.get("system") != "Pedicularis rex":
            reasons.append("freeze provenance system is not Pedicularis rex")
        if provenance.get("focal_data_inspected") is not False:
            reasons.append("freeze provenance does not certify pre-focal freezing")
        if not str(provenance.get("freeze_date", "")).strip():
            reasons.append("freeze provenance lacks freeze_date")
        digest = str(provenance.get("calibration_receipt_sha256", ""))
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest.lower()):
            reasons.append("freeze provenance lacks valid calibration receipt SHA-256")
        if len(raw_contexts) == 1:
            population, season = raw_contexts[0]
            if provenance.get("population_id") != population or provenance.get("season_id") != season:
                reasons.append("frozen threshold context does not match BITA raw data")

    return {"pass": not reasons, "reasons": reasons}


def _raw_gate(path: Path) -> dict:
    reasons: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        rows = list(reader)

    missing = [field for field in REQUIRED_RAW_FIELDS if field not in fields]
    if missing:
        reasons.append("missing raw fields: " + ", ".join(missing))
    if not rows:
        reasons.append("raw CSV has zero observation rows")

    contexts = sorted({(row.get("population_id", ""), row.get("season_id", "")) for row in rows})
    if rows and len(contexts) != 1:
        reasons.append("raw CSV must contain exactly one population-season context")

    levels_by_y: dict[str, set[str]] = {"DRAINED": set(), "PROTECTED": set()}
    for row in rows:
        y = row.get("water_treatment", "")
        if y in levels_by_y:
            levels_by_y[y].add(row.get("assigned_x_level", ""))
    if rows:
        for y, levels in levels_by_y.items():
            clean = {level for level in levels if level != ""}
            if len(clean) < 5:
                reasons.append(f"{y} has {len(clean)} assigned x levels; requires >=5")

    return {
        "pass": not reasons,
        "reasons": reasons,
        "n_rows": len(rows),
        "contexts": [list(item) for item in contexts],
        "x_level_counts": {key: len({x for x in value if x != ""}) for key, value in levels_by_y.items()},
    }


def _sch_gate(path: Path | None, raw_contexts: list[list[str]]) -> dict:
    if path is None:
        return {"pass": False, "reasons": ["same-context SCH receipt path not supplied"]}
    receipt = json.loads(path.read_text(encoding="utf-8"))
    reasons: list[str] = []

    if receipt.get("receipt_schema_version") != SCH_SCHEMA:
        reasons.append("wrong SCH receipt schema")
    if receipt.get("status") != SCH_STATUS:
        reasons.append("SCH causal-compromise status not positive")
    if receipt.get("system") != "Pedicularis rex":
        reasons.append("SCH receipt system is not Pedicularis rex")
    if receipt.get("system_wrapper_schema_version") != SCH_WRAPPER:
        reasons.append("SCH receipt is not non-circular Pedicularis wrapper V2")

    mapping = receipt.get("pedicularis_state_mapping")
    if not isinstance(mapping, dict):
        reasons.append("missing pedicularis_state_mapping")
    else:
        if mapping.get("G0") != "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED":
            reasons.append("SCH G0 is not independent seed-predator exclusion")
        if mapping.get("G1") != "SEED_PREDATOR_EXPOSED":
            reasons.append("SCH G1 is not seed-predator exposure")
        if mapping.get("water_y") != "HELD_FIXED_ACROSS_ALL_SCH_CELLS":
            reasons.append("SCH water-y was not held fixed")

    readiness = receipt.get("readiness_reference")
    if not isinstance(readiness, dict):
        reasons.append("missing SCH readiness_reference")
    else:
        if readiness.get("g_schema") != SCH_G_SCHEMA:
            reasons.append("SCH predator method is not V3")
        if "POLLINATOR_ACCESS_PRESERVED" not in str(readiness.get("predator_method_requirement", "")):
            reasons.append("SCH predator intervention lacks pollinator-access-preserved provenance")

    if len(raw_contexts) == 1:
        population, season = raw_contexts[0]
        if receipt.get("population_id") != population or receipt.get("season_id") != season:
            reasons.append("SCH receipt population-season does not match BITA raw data")

    return {"pass": not reasons, "reasons": reasons}


def evaluate(raw_csv: Path, config_json: Path, sch_receipt: Path | None = None) -> dict:
    raw_gate = _raw_gate(raw_csv)
    config_gate = _config_gate(config_json, raw_gate["contexts"])
    sch_gate = _sch_gate(sch_receipt, raw_gate["contexts"])
    gates = {
        "E0_thresholds_frozen": config_gate,
        "E1_non_circular_sch_handoff": sch_gate,
        "E2_registered_xy_surface_present": raw_gate,
    }
    all_ready = all(item["pass"] for item in gates.values())
    return {
        "analysis": "pedicularis_focal_execution_readiness",
        "gates": gates,
        "status": "READY_FOR_FOCAL_C1_C3_ANALYSIS" if all_ready else "NOT_READY_FOR_FOCAL_C1_C3_ANALYSIS",
        "next_action": (
            "run scripts/analyze_pedicularis_dimensional_release.py"
            if all_ready
            else "resolve listed gate failures without changing focal outcomes"
        ),
        "claim_ceiling": "readiness_only_not_empirical_support",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether the Pedicularis focal BITA chain is ready for confirmatory C1-C3 analysis")
    parser.add_argument("raw_csv", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--sch-receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = evaluate(args.raw_csv, args.config_json, args.sch_receipt)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
