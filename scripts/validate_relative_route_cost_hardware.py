"""Validate artificial-flower hardware and bench QC before Stage 0."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

TARGETS = {
    "top_disc_diameter_mm": (50.0, 0.5),
    "visible_tube_length_mm": (20.0, 0.5),
    "top_aperture_diameter_mm": (2.5, 0.1),
    "lateral_aperture_diameter_mm": (2.5, 0.1),
    "lateral_aperture_offset_below_top_mm": (5.0, 0.2),
}
MIN_BODIES = 4
MIN_LOADS_PER_ASSEMBLY = 20
INSERT_MIN_MM = 2.0
INSERT_MAX_MM = 10.0

MANIFEST_REQUIRED = {
    "module_id", "module_type", "manufacturing_batch", "geometry_version",
    "top_disc_diameter_mm", "visible_tube_length_mm",
    "top_aperture_diameter_mm", "lateral_aperture_diameter_mm",
    "lateral_aperture_offset_below_top_mm", "route",
    "insert_effective_distance_mm", "material", "surface_finish",
    "inspection_date", "dimension_tolerance_pass",
}
QC_REQUIRED = {
    "qc_run_id", "module_id", "legitimate_insert_id", "bypass_insert_id",
    "reward_volume_ul", "reward_concentration", "load_number",
    "delay_to_inspection_s", "top_entrance_wet", "lateral_entrance_wet",
    "overflow", "cross_route_leakage", "shared_reservoir_confirmed",
    "shutter_legitimate_pass", "shutter_bypass_pass",
    "external_cue_identity_pass", "cleaning_compatibility_pass",
}

def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    return rows

def _bool(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"invalid boolean: {value!r}")

def _float(value: object, name: str) -> float:
    try:
        out = float(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out

def _check_columns(rows: list[dict[str, str]], required: set[str], label: str) -> None:
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"{label} missing columns: {sorted(missing)}")

def validate_hardware(
    manifest_rows: list[dict[str, str]],
    qc_rows: list[dict[str, str]],
) -> dict[str, object]:
    _check_columns(manifest_rows, MANIFEST_REQUIRED, "manifest")
    _check_columns(qc_rows, QC_REQUIRED, "bench QC")

    modules: dict[str, dict[str, str]] = {}
    body_ids: list[str] = []
    inserts_by_route: dict[str, list[str]] = defaultdict(list)
    manifest_failures: list[str] = []

    for row in manifest_rows:
        module_id = str(row["module_id"]).strip()
        if not module_id or module_id in modules:
            raise ValueError("module_id values must be nonblank and unique")
        modules[module_id] = row
        module_type = str(row["module_type"]).strip().lower()
        declared_pass = _bool(row["dimension_tolerance_pass"])

        if module_type == "body":
            body_ids.append(module_id)
            for field, (target, tol) in TARGETS.items():
                observed = _float(row[field], field)
                if abs(observed - target) > tol + 1e-12:
                    manifest_failures.append(f"{module_id}:{field}")
            if not declared_pass:
                manifest_failures.append(f"{module_id}:declared_dimension_fail")
        elif module_type == "insert":
            route = str(row["route"]).strip().lower()
            if route not in {"legitimate", "bypass"}:
                raise ValueError(f"invalid insert route for {module_id}")
            distance = _float(
                row["insert_effective_distance_mm"], "insert_effective_distance_mm"
            )
            if not (INSERT_MIN_MM <= distance <= INSERT_MAX_MM):
                manifest_failures.append(f"{module_id}:insert_distance")
            if not declared_pass:
                manifest_failures.append(f"{module_id}:declared_dimension_fail")
            inserts_by_route[route].append(module_id)
        else:
            raise ValueError(f"invalid module_type for {module_id}: {module_type!r}")

    assembly_rows: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in qc_rows:
        key = (
            str(row["qc_run_id"]).strip(),
            str(row["module_id"]).strip(),
            str(row["legitimate_insert_id"]).strip(),
            str(row["bypass_insert_id"]).strip(),
        )
        if not all(key):
            raise ValueError("QC assembly identifiers must be nonblank")
        if key[1] not in modules or str(modules[key[1]]["module_type"]).lower() != "body":
            raise ValueError(f"unknown body in QC: {key[1]}")
        if key[2] not in modules or str(modules[key[2]]["route"]).lower() != "legitimate":
            raise ValueError(f"invalid legitimate insert in QC: {key[2]}")
        if key[3] not in modules or str(modules[key[3]]["route"]).lower() != "bypass":
            raise ValueError(f"invalid bypass insert in QC: {key[3]}")
        assembly_rows[key].append(row)

    qc_failures: list[str] = []
    assembly_summaries: dict[str, object] = {}
    for key, rows in sorted(assembly_rows.items()):
        label = "|".join(key)
        loads = sorted(int(str(row["load_number"]).strip()) for row in rows)
        load_count_pass = (
            len(rows) >= MIN_LOADS_PER_ASSEMBLY
            and set(range(1, MIN_LOADS_PER_ASSEMBLY + 1)).issubset(loads)
        )
        reward_volumes = {
            _float(row["reward_volume_ul"], "reward_volume_ul") for row in rows
        }
        reward_concentrations = {
            str(row["reward_concentration"]).strip() for row in rows
        }
        delay_values = {
            _float(row["delay_to_inspection_s"], "delay_to_inspection_s")
            for row in rows
        }
        no_wetting = all(
            not _bool(row["top_entrance_wet"])
            and not _bool(row["lateral_entrance_wet"])
            for row in rows
        )
        no_overflow = all(not _bool(row["overflow"]) for row in rows)
        no_leak = all(not _bool(row["cross_route_leakage"]) for row in rows)
        shared = all(_bool(row["shared_reservoir_confirmed"]) for row in rows)
        shutters = all(
            _bool(row["shutter_legitimate_pass"])
            and _bool(row["shutter_bypass_pass"])
            for row in rows
        )
        cue_identity = all(_bool(row["external_cue_identity_pass"]) for row in rows)
        cleaning = all(_bool(row["cleaning_compatibility_pass"]) for row in rows)
        consistent_reward = (
            len(reward_volumes) == 1 and len(reward_concentrations) == 1
        )
        consistent_delay = len(delay_values) == 1

        checks = {
            "loads_ge_20_with_first_20_present": load_count_pass,
            "no_entrance_wetting": no_wetting,
            "no_overflow": no_overflow,
            "no_cross_route_leakage": no_leak,
            "shared_reservoir_confirmed": shared,
            "both_shutters_pass": shutters,
            "external_cue_identity_pass": cue_identity,
            "cleaning_compatibility_pass": cleaning,
            "reward_constant_within_assembly": consistent_reward,
            "inspection_delay_constant_within_assembly": consistent_delay,
        }
        if not all(checks.values()):
            qc_failures.append(label)
        assembly_summaries[label] = {
            "rows": len(rows),
            "reward_volume_ul": (
                next(iter(reward_volumes)) if len(reward_volumes) == 1 else None
            ),
            "reward_concentration": (
                next(iter(reward_concentrations))
                if len(reward_concentrations) == 1 else None
            ),
            "delay_to_inspection_s": (
                next(iter(delay_values)) if len(delay_values) == 1 else None
            ),
            "checks": checks,
            "passes": all(checks.values()),
        }

    gates = {
        "at_least_four_bodies": len(body_ids) >= MIN_BODIES,
        "has_legitimate_inserts": bool(inserts_by_route["legitimate"]),
        "has_bypass_inserts": bool(inserts_by_route["bypass"]),
        "manifest_dimensions_pass": not manifest_failures,
        "at_least_one_qc_assembly": bool(assembly_rows),
        "all_tested_assemblies_pass_bench_qc": (
            not qc_failures and bool(assembly_rows)
        ),
    }

    return {
        "analysis_name": "relative_route_cost_hardware_bench_qc",
        "body_count": len(body_ids),
        "legitimate_insert_count": len(inserts_by_route["legitimate"]),
        "bypass_insert_count": len(inserts_by_route["bypass"]),
        "tested_assembly_count": len(assembly_rows),
        "manifest_failures": manifest_failures,
        "qc_failures": qc_failures,
        "assemblies": assembly_summaries,
        "gates": gates,
        "passes_stage0_hardware_gate": all(gates.values()),
        "claim_boundary": (
            "This validator certifies engineering readiness only. Passing bench QC "
            "does not establish matched biological route costs; Stage-0 bee "
            "calibration remains required."
        ),
    }

def run(
    manifest_csv: str | Path,
    qc_csv: str | Path,
    output_json: str | Path,
) -> dict[str, object]:
    result = validate_hardware(_read(manifest_csv), _read(qc_csv))
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_csv")
    parser.add_argument("qc_csv")
    parser.add_argument("output_json")
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.manifest_csv, args.qc_csv, args.output_json),
            indent=2,
            sort_keys=True,
        )
    )
