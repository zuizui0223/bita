from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts.analyze_pedicularis_dimensional_release import read_rows


def _num(row: dict[str, str], field: str) -> float:
    value = float(row[field])
    if not math.isfinite(value):
        raise ValueError(f"non-finite {field}")
    return value


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sum((value - m) ** 2 for value in values) / (len(values) - 1)


def _sample_sd(values: list[float]) -> float:
    return math.sqrt(max(0.0, _sample_variance(values)))


def _pooled_within_cell_variance(rows: list[dict[str, str]], field: str) -> tuple[float, int]:
    cells: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        cells[(row["assigned_x_level"], row["water_treatment"])].append(_num(row, field))
    ss = 0.0
    df = 0
    for values in cells.values():
        if len(values) < 2:
            continue
        ss += (len(values) - 1) * _sample_variance(values)
        df += len(values) - 1
    return (ss / df if df else 0.0), df


def _residualized_variance_components(rows: list[dict[str, str]]) -> dict:
    cells: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        cells[(row["assigned_x_level"], row["water_treatment"])].append(row)
    cell_means = {
        key: mean(_num(row, "undamaged_seed_count") for row in group)
        for key, group in cells.items()
    }
    by_plant: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        key = (row["assigned_x_level"], row["water_treatment"])
        by_plant[row["plant_id"]].append(_num(row, "undamaged_seed_count") - cell_means[key])

    sizes = {len(values) for values in by_plant.values()}
    if len(by_plant) < 2 or len(sizes) != 1 or next(iter(sizes)) < 2:
        return {
            "balanced_cluster_estimate_available": False,
            "rows_per_plant": None,
            "between_plant_variance_component": None,
            "within_plant_residual_variance": None,
            "residualized_icc": None,
        }

    k = next(iter(sizes))
    plant_means = {plant: mean(values) for plant, values in by_plant.items()}
    grand = mean(plant_means.values())
    n = len(by_plant)
    ss_between = k * sum((value - grand) ** 2 for value in plant_means.values())
    ms_between = ss_between / (n - 1)
    ss_within = sum(
        sum((value - plant_means[plant]) ** 2 for value in values)
        for plant, values in by_plant.items()
    )
    ms_within = ss_within / (n * (k - 1))
    between_component = max(0.0, (ms_between - ms_within) / k)
    denom = ms_between + (k - 1) * ms_within
    icc = (ms_between - ms_within) / denom if denom > 0 else 0.0
    return {
        "balanced_cluster_estimate_available": True,
        "rows_per_plant": k,
        "between_plant_variance_component": between_component,
        "within_plant_residual_variance": ms_within,
        "residualized_icc": icc,
    }


def _matched_y_difference(rows: list[dict[str, str]], field: str) -> float | None:
    cells: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        cells[(row["assigned_x_level"], row["water_treatment"])].append(_num(row, field))
    levels = sorted({level for level, _ in cells})
    diffs = []
    for level in levels:
        key0 = (level, "DRAINED")
        key1 = (level, "PROTECTED")
        if key0 in cells and key1 in cells:
            diffs.append(mean(cells[key1]) - mean(cells[key0]))
    return mean(diffs) if diffs else None


def extract(rows: list[dict[str, str]]) -> dict:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("pilot receipt requires one population and season")

    levels: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        levels[row["assigned_x_level"]].append(_num(row, "realized_exsertion"))
    level_summary = {
        level: {
            "n": len(values),
            "mean_realized_exsertion": mean(values),
            "sd_realized_exsertion": _sample_sd(values),
            "min": min(values),
            "max": max(values),
        }
        for level, values in sorted(levels.items())
    }

    y0 = [row for row in rows if row["water_treatment"] == "DRAINED"]
    y1 = [row for row in rows if row["water_treatment"] == "PROTECTED"]
    if not y0 or not y1:
        raise ValueError("pilot requires both DRAINED and PROTECTED water states")

    fitness_var, fitness_df = _pooled_within_cell_variance(rows, "undamaged_seed_count")
    pollen_var, pollen_df = _pooled_within_cell_variance(rows, "pollen_grains")
    components = _residualized_variance_components(rows)
    water0 = [_num(row, "water_depth") for row in y0]
    water1 = [_num(row, "water_depth") for row in y1]
    damaged0 = [_num(row, "damaged_seed_count") for row in y0]
    damaged1 = [_num(row, "damaged_seed_count") for row in y1]
    all_damaged = damaged0 + damaged1
    damage = [int(row["mechanical_damage"]) for row in rows]

    planning_draft = {
        "between_plant_sd": (
            math.sqrt(components["between_plant_variance_component"])
            if components["between_plant_variance_component"] is not None
            else None
        ),
        "residual_sd": math.sqrt(max(0.0, fitness_var)),
        "damaged_seed_mean_y0": mean(damaged0),
        "damaged_seed_mean_y1": mean(damaged1),
        "damaged_seed_sd": _sample_sd(all_damaged),
        "y_cross_effect_on_pollen_descriptive": _matched_y_difference(rows, "pollen_grains"),
        "water_depth_y1": mean(water1),
        "water_depth_sd": _sample_sd(water1),
        "mechanical_damage_rate": mean(damage),
        "effect_geometry_status": "REQUIRES_PROSPECTIVE_SENSITIVITY_SCENARIOS_OR_EXTERNAL_PILOT",
    }

    return {
        "receipt_schema_version": "PEDICULARIS_EXPERIMENT_B_PILOT_PARAMETERS_V1",
        "status": "DESCRIPTIVE_PILOT_ONLY_NOT_BIOLOGICAL_TEST",
        "system": "Pedicularis rex",
        "population_id": next(iter(populations)),
        "season_id": next(iter(seasons)),
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "realized_x_by_assigned_level": level_summary,
        "pooled_within_cell_fitness_variance": fitness_var,
        "pooled_within_cell_fitness_df": fitness_df,
        "pooled_within_cell_pollen_variance": pollen_var,
        "pooled_within_cell_pollen_df": pollen_df,
        "residualized_cluster_components": components,
        "manipulation_performance": {
            "mean_water_depth_y0": mean(water0),
            "mean_water_depth_y1": mean(water1),
            "water_depth_separation": mean(water1) - mean(water0),
            "mechanical_damage_rate": mean(damage),
            "mean_damaged_seeds_y0": mean(damaged0),
            "mean_damaged_seeds_y1": mean(damaged1),
            "matched_y_pollen_difference_descriptive": _matched_y_difference(rows, "pollen_grains"),
        },
        "power_config_draft": planning_draft,
        "claim_ceiling": (
            "descriptive planning moments only; do not test BALANCE/BITA biology, choose thresholds, or infer differentiation from this receipt"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pilot_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = read_rows(args.pilot_csv)
    result = extract(rows)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
