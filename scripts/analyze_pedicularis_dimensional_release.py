from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from trait_architecture.dimensional_release import analyze_dimensional_release


RAW_FIELDS = (
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

Y_MAP = {"DRAINED": 0, "PROTECTED": 1}
SCH_SCHEMA = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"
SCH_STATUS = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
SCH_PEDICULARIS_WRAPPER_V2 = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
SCH_PREDATOR_G_SCHEMA = "SCH_PEDICULARIS_PREDATOR_WEIGHT_V2"
WRAPPER_SCHEMA = "BITA_PEDICULARIS_DIMENSIONAL_RELEASE_WRAPPER_V2"


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _binary(row: dict[str, str], field: str) -> int:
    raw = row[field].strip()
    if raw not in {"0", "1"}:
        raise ValueError(f"{field} must be coded 0/1, got {raw!r}")
    return int(raw)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in RAW_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in RAW_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        if row["flower_id"] in seen:
            raise ValueError(f"duplicate flower_id {row['flower_id']!r}")
        seen.add(row["flower_id"])
        if row["water_treatment"] not in Y_MAP:
            raise ValueError("water_treatment must be DRAINED or PROTECTED")
        for field in (
            "realized_exsertion",
            "ovule_count",
            "undamaged_seed_count",
            "damaged_seed_count",
            "pollen_grains",
            "pollinator_visits",
            "water_depth",
        ):
            _num(row, field)
        _binary(row, "mechanical_damage")
        ovules = _num(row, "ovule_count")
        undamaged = _num(row, "undamaged_seed_count")
        damaged = _num(row, "damaged_seed_count")
        if ovules <= 0:
            raise ValueError("ovule_count must be > 0")
        if undamaged < 0 or damaged < 0:
            raise ValueError("seed counts must be >= 0")
        if undamaged + damaged > ovules:
            raise ValueError("undamaged_seed_count + damaged_seed_count cannot exceed ovule_count")
        if undamaged + damaged <= 0:
            raise ValueError("at least one initiated seed is required to define the function-2 survival metric")
    return rows


def _context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one Pedicularis BITA package must contain exactly one population and season")
    return next(iter(populations)), next(iter(seasons))


def _validate_sch_receipt(sch_receipt: dict, population: str, season: str) -> None:
    if sch_receipt.get("receipt_schema_version") != SCH_SCHEMA:
        raise ValueError("Pedicularis BITA requires the registered SCH state-optimum receipt schema")
    if sch_receipt.get("status") != SCH_STATUS:
        raise ValueError("Pedicularis BITA requires a positive SCH causal-compromise receipt")
    if sch_receipt.get("system") != "Pedicularis rex":
        raise ValueError("Pedicularis BITA requires a Pedicularis rex SCH receipt")
    if sch_receipt.get("population_id") != population or sch_receipt.get("season_id") != season:
        raise ValueError("BITA raw data must match the population and season of the SCH reference receipt")

    if sch_receipt.get("system_wrapper_schema_version") != SCH_PEDICULARIS_WRAPPER_V2:
        raise ValueError(
            "Pedicularis BITA requires the non-circular SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2 receipt; "
            "legacy water-as-G SCH receipts are rejected"
        )
    mapping = sch_receipt.get("pedicularis_state_mapping")
    if not isinstance(mapping, dict):
        raise ValueError("Pedicularis SCH V2 receipt lacks pedicularis_state_mapping")
    if mapping.get("G0") != "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED" or mapping.get("G1") != "SEED_PREDATOR_EXPOSED":
        raise ValueError("Pedicularis SCH receipt does not use independent seed-predator G states")
    if mapping.get("water_y") != "HELD_FIXED_ACROSS_ALL_SCH_CELLS":
        raise ValueError("Pedicularis SCH receipt did not hold the Chapter-2 water-y axis fixed")
    readiness = sch_receipt.get("readiness_reference")
    if not isinstance(readiness, dict) or readiness.get("g_schema") != SCH_PREDATOR_G_SCHEMA:
        raise ValueError("Pedicularis SCH receipt is not grounded in SCH_PEDICULARIS_PREDATOR_WEIGHT_V2")


def _seed_survival(row: dict[str, str]) -> float:
    undamaged = _num(row, "undamaged_seed_count")
    damaged = _num(row, "damaged_seed_count")
    return undamaged / (undamaged + damaged)


def to_bita_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    converted: list[dict[str, str]] = []
    for row in rows:
        converted.append(
            {
                "plant_id": row["plant_id"],
                "unit_id": row["flower_id"],
                "x_level": row["assigned_x_level"],
                "x_measured": row["realized_exsertion"],
                "y_state": str(Y_MAP[row["water_treatment"]]),
                "function1_value": row["pollen_grains"],
                "function2_value": str(_seed_survival(row)),
                "fitness_value": row["undamaged_seed_count"],
            }
        )
    return converted


def analyze(rows: list[dict[str, str]], sch_receipt: dict, config: dict) -> dict:
    population, season = _context(rows)
    _validate_sch_receipt(sch_receipt, population, season)
    release_config = config.get("bita_release")
    if not isinstance(release_config, dict):
        raise ValueError("config must contain a bita_release object with frozen thresholds")

    result = analyze_dimensional_release(to_bita_rows(rows), sch_receipt, release_config)
    result["system_wrapper_schema_version"] = WRAPPER_SCHEMA
    result["system"] = "Pedicularis rex"
    result["population_id"] = population
    result["season_id"] = season
    result["sch_reference_provenance"] = {
        "system_wrapper_schema_version": sch_receipt["system_wrapper_schema_version"],
        "independent_predator_g_schema": sch_receipt["readiness_reference"]["g_schema"],
        "water_y_was_fixed_during_sch": True,
    }
    result["pedicularis_mapping"] = {
        "x": "REALIZED_COROLLA_EXSERTION",
        "y0": "DRAINED_WATER_DEFENCE_DISABLED",
        "y1": "PROTECTED_WATER_DEFENCE_ACTIVE",
        "function1_value": "POLLEN_GRAINS_RECEIVED",
        "function2_value": "UNDAMAGED_FRACTION_OF_INITIATED_SEEDS",
        "fitness_value": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
    }
    result["pedicularis_claim_ceiling"] = (
        "contemporary_non_circular_functional_state_dimensional_release_only; "
        "structural trait differentiation requires the separate retention-performance promotion gate; "
        "mechanism allocation requires crossed P/G intervention; "
        "historical modularization not identified"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run non-circular Pedicularis x-y release using an SCH V2 independent-predator reference")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("sch_receipt", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    sch_receipt = json.loads(args.sch_receipt.read_text(encoding="utf-8"))
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze(rows, sch_receipt, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
