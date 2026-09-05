from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean


REQUIRED_FIELDS = (
    "dataset_id",
    "source_doi",
    "year",
    "population_id",
    "mean_flowering_day",
    "male_flower_mean",
    "perfect_flower_mean",
    "male_fraction",
    "fruit_set_mean",
    "seed_predation_rate",
    "n_plants",
)
RECEIPT_SCHEMA = "BITA_PEUCEDANUM_POPULATION_PATTERN_V1"


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


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

    seen: set[tuple[str, str, str]] = set()
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        key = (row["dataset_id"], row["year"], row["population_id"])
        if key in seen:
            raise ValueError(f"duplicate dataset/year/population row: {key}")
        seen.add(key)
        for field in (
            "mean_flowering_day",
            "male_flower_mean",
            "perfect_flower_mean",
            "male_fraction",
            "fruit_set_mean",
            "seed_predation_rate",
            "n_plants",
        ):
            _num(row, field)
        for field in ("male_fraction", "fruit_set_mean", "seed_predation_rate"):
            value = _num(row, field)
            if not 0 <= value <= 1:
                raise ValueError(f"{field} must be on [0,1]")
        if _num(row, "male_flower_mean") < 0 or _num(row, "perfect_flower_mean") < 0:
            raise ValueError("flower means must be >= 0")
        if _num(row, "n_plants") <= 0:
            raise ValueError("n_plants must be > 0")
    return rows


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


def _pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("correlation requires paired vectors of length >= 2")
    mx, my = mean(x), mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    sx = math.sqrt(sum(v * v for v in dx))
    sy = math.sqrt(sum(v * v for v in dy))
    if sx == 0 or sy == 0:
        raise ValueError("correlation is undefined for a constant vector")
    return sum(a * b for a, b in zip(dx, dy)) / (sx * sy)


def _spearman(x: list[float], y: list[float]) -> float:
    return _pearson(_ranks(x), _ranks(y))


def _dataset_summary(rows: list[dict[str, str]], config: dict) -> dict:
    n = len(rows)
    min_n = int(config["min_populations_per_dataset"])
    if n < 2:
        raise ValueError("each dataset requires at least two population rows")

    def values(field: str) -> list[float]:
        return [_num(row, field) for row in rows]

    pred = values("seed_predation_rate")
    estimands = {
        "rho_male_fraction_vs_predation": _spearman(values("male_fraction"), pred),
        "rho_flowering_day_vs_predation": _spearman(values("mean_flowering_day"), pred),
        "rho_perfect_flowers_vs_predation": _spearman(values("perfect_flower_mean"), pred),
        "rho_male_flowers_vs_predation": _spearman(values("male_flower_mean"), pred),
        "mean_seed_predation_rate": mean(pred),
        "mean_male_fraction": mean(values("male_fraction")),
    }
    gates = {
        "minimum_population_coverage": n >= min_n,
        "male_fraction_tracks_predation": estimands["rho_male_fraction_vs_predation"] >= float(
            config["min_positive_male_fraction_predation_rho"]
        ),
        "later_flowering_tracks_lower_predation": estimands["rho_flowering_day_vs_predation"] <= float(
            config["max_negative_flowering_predation_rho"]
        ),
    }
    return {
        "n_population_year_rows": n,
        "source_dois": sorted({row["source_doi"] for row in rows}),
        "years": sorted({row["year"] for row in rows}),
        "estimands": estimands,
        "gates": gates,
        "status": "DIRECTIONALLY_CONSISTENT" if all(gates.values()) else "NOT_DIRECTIONALLY_CONSISTENT",
    }


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    by_dataset: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_dataset[row["dataset_id"]].append(row)

    summaries = {dataset: _dataset_summary(group, config) for dataset, group in sorted(by_dataset.items())}
    n_supported = sum(summary["status"] == "DIRECTIONALLY_CONSISTENT" for summary in summaries.values())
    all_supported = n_supported == len(summaries)
    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "peucedanum_population_level_observational_partial_differentiation_pattern",
        "n_datasets": len(summaries),
        "n_directionally_consistent_datasets": n_supported,
        "dataset_results": summaries,
        "status": (
            "OBSERVATIONAL_GEOGRAPHIC_PARTIAL_DIFFERENTIATION_PATTERN_SUPPORTED"
            if all_supported
            else "OBSERVATIONAL_PATTERN_NOT_FULLY_RECOVERED"
        ),
        "claim_ceiling": (
            "population_level_observational_pattern_only; not_R_state; not_causal_dimensional_release; "
            "not_preferential_loading_from_intervention; not_historical_origin_of_andromonoecy"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze normalized Peucedanum population-level Dryad data")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze(rows, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
