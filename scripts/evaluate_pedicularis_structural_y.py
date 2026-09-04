from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev


REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "unit_id",
    "measurement_round",
    "realized_exsertion",
    "retention_capacity_ml",
    "retention_duration_hours",
    "bract_top_width_mm",
    "bract_bottom_width_mm",
    "bract_height_mm",
    "pollen_grains",
    "pollinator_visits",
    "initiated_seed_count",
    "undamaged_seed_count",
    "early_predator_attack_present",
    "mechanical_damage",
)

ALLOWED_Y_FIELDS = {"retention_capacity_ml", "retention_duration_hours"}
RECEIPT_SCHEMA = "BITA_PEDICULARIS_STRUCTURAL_Y_V1"


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
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        key = f"{row['unit_id']}::{row['measurement_round']}"
        if key in seen:
            raise ValueError(f"duplicate unit/round key {key!r}")
        seen.add(key)
        for field in (
            "realized_exsertion",
            "retention_capacity_ml",
            "retention_duration_hours",
            "bract_top_width_mm",
            "bract_bottom_width_mm",
            "bract_height_mm",
            "pollen_grains",
            "pollinator_visits",
            "initiated_seed_count",
            "undamaged_seed_count",
        ):
            _num(row, field)
        _binary(row, "early_predator_attack_present")
        _binary(row, "mechanical_damage")
        initiated = _num(row, "initiated_seed_count")
        undamaged = _num(row, "undamaged_seed_count")
        if initiated <= 0:
            raise ValueError("initiated_seed_count must be > 0")
        if undamaged < 0 or undamaged > initiated:
            raise ValueError("undamaged_seed_count must be between 0 and initiated_seed_count")
    return rows


def _context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one structural-y package must contain exactly one population and season")
    return next(iter(populations)), next(iter(seasons))


def _plant_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["plant_id"]].append(row)
    return groups


def _survival(row: dict[str, str]) -> float:
    return _num(row, "undamaged_seed_count") / _num(row, "initiated_seed_count")


def _plant_summary(rows: list[dict[str, str]], y_field: str) -> list[dict[str, float]]:
    groups = _plant_rows(rows)
    out: list[dict[str, float]] = []
    for plant, group in sorted(groups.items()):
        out.append(
            {
                "plant_id": plant,
                "x": mean(_num(row, "realized_exsertion") for row in group),
                "y": mean(_num(row, y_field) for row in group),
                "f1": mean(_num(row, "pollen_grains") for row in group),
                "f2": mean(_survival(row) for row in group),
                "visits": mean(_num(row, "pollinator_visits") for row in group),
                "attack": mean(_binary(row, "early_predator_attack_present") for row in group),
                "damage": mean(_binary(row, "mechanical_damage") for row in group),
                "top_width": mean(_num(row, "bract_top_width_mm") for row in group),
                "bottom_width": mean(_num(row, "bract_bottom_width_mm") for row in group),
                "bract_height": mean(_num(row, "bract_height_mm") for row in group),
                "retention_capacity_ml": mean(_num(row, "retention_capacity_ml") for row in group),
                "retention_duration_hours": mean(_num(row, "retention_duration_hours") for row in group),
            }
        )
    return out


def _standardize(values: list[float]) -> list[float]:
    sd = pstdev(values)
    if sd <= 1e-12:
        raise ValueError("cannot standardize a constant variable")
    center = mean(values)
    return [(value - center) / sd for value in values]


def _two_predictor_standardized_beta(summary: list[dict[str, float]], outcome: str) -> tuple[float, float]:
    x = _standardize([float(row["x"]) for row in summary])
    y = _standardize([float(row["y"]) for row in summary])
    o = _standardize([float(row[outcome]) for row in summary])

    sxx = sum(v * v for v in x)
    syy = sum(v * v for v in y)
    sxy = sum(a * b for a, b in zip(x, y))
    sxo = sum(a * b for a, b in zip(x, o))
    syo = sum(a * b for a, b in zip(y, o))
    det = sxx * syy - sxy * sxy
    if abs(det) < 1e-10:
        raise ValueError("x and y are too collinear to estimate partial standardized effects")
    beta_x = (sxo * syy - syo * sxy) / det
    beta_y = (syo * sxx - sxo * sxy) / det
    return beta_x, beta_y


def _correlation(a: list[float], b: list[float]) -> float:
    za = _standardize(a)
    zb = _standardize(b)
    return sum(x * y for x, y in zip(za, zb)) / len(za)


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of empty values")
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    weight = pos - lo
    return values[lo] * (1 - weight) + values[hi] * weight


def _within_plant_y_spread(rows: list[dict[str, str]], y_field: str) -> tuple[float, dict[str, float]]:
    spreads: dict[str, float] = {}
    for plant, group in _plant_rows(rows).items():
        values = [_num(row, y_field) for row in group]
        center = mean(values)
        spreads[plant] = (max(values) - min(values)) / max(abs(center), 1e-12)
    return max(spreads.values()), spreads


def _among_plant_y_range(summary: list[dict[str, float]]) -> float:
    values = [float(row["y"]) for row in summary]
    center = mean(values)
    return (max(values) - min(values)) / max(abs(center), 1e-12)


def _bootstrap_betas(summary: list[dict[str, float]], reps: int, rng: random.Random) -> dict[str, list[float]]:
    if len(summary) < 3:
        raise ValueError("at least three plants are required")
    out = {"y_f1": [], "y_f2": [], "xy_corr": []}
    for _ in range(reps):
        sample = rng.choices(summary, k=len(summary))
        try:
            _, y_f1 = _two_predictor_standardized_beta(sample, "f1")
            _, y_f2 = _two_predictor_standardized_beta(sample, "f2")
            xy = _correlation([float(row["x"]) for row in sample], [float(row["y"]) for row in sample])
        except ValueError:
            continue
        out["y_f1"].append(y_f1)
        out["y_f2"].append(y_f2)
        out["xy_corr"].append(xy)
    valid = len(out["y_f1"])
    if valid < max(50, reps // 5):
        raise ValueError("too few valid structural-y bootstrap replicates")
    return out


def evaluate(rows: list[dict[str, str]], config: dict) -> dict:
    population, season = _context(rows)
    y_field = str(config.get("primary_y_field", "retention_capacity_ml"))
    if y_field not in ALLOWED_Y_FIELDS:
        raise ValueError(f"primary_y_field must be one of {sorted(ALLOWED_Y_FIELDS)}")
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")

    groups = _plant_rows(rows)
    min_repeats = int(config["min_repeats_per_plant"])
    summary = _plant_summary(rows, y_field)
    max_spread, spreads = _within_plant_y_spread(rows, y_field)
    y_range = _among_plant_y_range(summary)
    beta_x_f1, beta_y_f1 = _two_predictor_standardized_beta(summary, "f1")
    beta_x_f2, beta_y_f2 = _two_predictor_standardized_beta(summary, "f2")
    xy_corr = _correlation([float(row["x"]) for row in summary], [float(row["y"]) for row in summary])

    rng = random.Random(int(config.get("random_seed", 20260904)))
    boot = _bootstrap_betas(summary, reps, rng)
    f1_ci = [_quantile(boot["y_f1"], 0.025), _quantile(boot["y_f1"], 0.975)]
    f2_ci = [_quantile(boot["y_f2"], 0.025), _quantile(boot["y_f2"], 0.975)]
    xy_ci = [_quantile(boot["xy_corr"], 0.025), _quantile(boot["xy_corr"], 0.975)]

    min_plants = int(config["min_plants"])
    min_y_beta = float(config["min_y_to_function2_standardized_beta"])
    max_cross = float(config["max_abs_y_to_function1_standardized_beta"])
    max_damage = float(config["max_mechanical_damage_rate"])
    low_coupling_threshold = float(config["max_abs_xy_correlation_for_low_coupling"])

    gates = {
        "minimum_plants": len(summary) >= min_plants,
        "minimum_repeats_per_plant": all(len(group) >= min_repeats for group in groups.values()),
        "repeatable_y_performance": max_spread <= float(config["max_within_plant_y_relative_spread"]),
        "adequate_y_range": y_range >= float(config["min_among_plant_y_relative_range"]),
        "y_targets_function2_after_x": f2_ci[0] >= min_y_beta,
        "y_cross_effect_on_function1_bounded": f1_ci[0] >= -max_cross and f1_ci[1] <= max_cross,
        "mechanical_damage_low": max(float(row["damage"]) for row in summary) <= max_damage,
    }

    base_identified = all(gates.values())
    low_coupling = max(abs(xy_ci[0]), abs(xy_ci[1])) <= low_coupling_threshold
    if base_identified and low_coupling:
        status = "STRUCTURAL_Y_TRAIT_IDENTIFIED_LOW_COUPLING"
    elif base_identified:
        status = "STRUCTURAL_Y_TRAIT_IDENTIFIED_PARTIAL_COUPLING"
    else:
        status = "STRUCTURAL_Y_TRAIT_NOT_IDENTIFIED"

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "pedicularis_structural_y_promotion",
        "population_id": population,
        "season_id": season,
        "primary_y_field": y_field,
        "n_rows": len(rows),
        "n_plants": len(summary),
        "observed_estimands": {
            "max_within_plant_y_relative_spread": max_spread,
            "within_plant_y_relative_spread_by_plant": spreads,
            "among_plant_y_relative_range": y_range,
            "x_y_correlation": xy_corr,
            "x_to_function1_standardized_beta": beta_x_f1,
            "y_to_function1_standardized_beta": beta_y_f1,
            "x_to_function2_standardized_beta": beta_x_f2,
            "y_to_function2_standardized_beta": beta_y_f2,
        },
        "bootstrap_95_ci": {
            "y_to_function1_standardized_beta": f1_ci,
            "y_to_function2_standardized_beta": f2_ci,
            "x_y_correlation": xy_ci,
        },
        "gates": gates,
        "coupling_classification": "LOW_COUPLING" if low_coupling else "PARTIAL_COUPLING",
        "status": status,
        "claim_ceiling": (
            "contemporary_repeatable_structural_or_performance_y_coordinate_with_preferential_loading; "
            "not heritability; not genetic/developmental independence; not historical modularization"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Pedicularis structural water-retention y as a second trait/performance coordinate")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = evaluate(rows, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
