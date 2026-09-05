from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from scripts.evaluate_peucedanum_stage_b_manipulation import (
    analyze as validate_stage_b_manipulation,
    read_rows as read_stage_b_validation_rows,
)


G_REMOVED = "EGGS_REMOVED"
G_RETAINED = "EGGS_RETAINED"
RECEIPT_SCHEMA = "BITA_PEUCEDANUM_STAGE_B_CAUSAL_FITNESS_V1"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
EXTRA_REQUIRED_FIELDS = (
    "g_state",
    "eggs_before_g_treatment",
    "initial_fruits",
    "final_intact_fruits",
    "predated_fruits",
    "male_fitness",
)


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _g(row: dict[str, str]) -> int:
    value = row["g_state"].strip()
    if value == G_REMOVED:
        return 0
    if value == G_RETAINED:
        return 1
    raise ValueError(f"g_state must be {G_REMOVED!r} or {G_RETAINED!r}, got {value!r}")


def read_rows(path: Path) -> list[dict[str, str]]:
    rows = read_stage_b_validation_rows(path)
    missing = [field for field in EXTRA_REQUIRED_FIELDS if field not in rows[0]]
    if missing:
        raise ValueError(f"missing required Stage-B outcome columns: {', '.join(missing)}")

    q_levels = sorted({_num(row, "q_target") for row in rows})
    expected = {(q, g) for q in q_levels for g in (0, 1)}
    by_block: dict[str, Counter[tuple[float, int]]] = defaultdict(Counter)

    for i, row in enumerate(rows, start=2):
        for field in EXTRA_REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        g = _g(row)
        q = _num(row, "q_target")
        by_block[row["block_id"]][(q, g)] += 1

        eggs = _num(row, "eggs_before_g_treatment")
        initial = _num(row, "initial_fruits")
        intact = _num(row, "final_intact_fruits")
        predated = _num(row, "predated_fruits")
        male = _num(row, "male_fitness")
        perfect = _num(row, "perfect_retained")
        if eggs < 0 or initial < 0 or intact < 0 or predated < 0 or male < 0:
            raise ValueError("Stage-B egg, fruit and male-fitness outcomes must be non-negative")
        if initial > perfect + 1e-6:
            raise ValueError("initial_fruits cannot exceed perfect_retained")
        if intact + predated > initial + 1e-6:
            raise ValueError("final_intact_fruits + predated_fruits cannot exceed initial_fruits")

    for block, counts in by_block.items():
        if set(counts) != expected or any(count != 1 for count in counts.values()):
            raise ValueError(
                "each Stage-B block must contain exactly one unit for every q_target x G combination; "
                f"block {block!r} is incomplete or duplicated"
            )
    return rows


def _require_config(config: dict) -> dict:
    if config.get("design") != "WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL":
        raise ValueError("fitness config must declare WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL")
    numeric_keys = (
        "bootstrap_reps",
        "bootstrap_seed",
        "min_blocks",
        "min_q_levels",
        "min_units_per_q_by_g_cell",
        "min_valid_predation_fraction_per_cell",
        "min_negative_optimum_shift_q",
        "min_initial_high_vs_low_gain_z",
        "min_positive_q_oviposition_gain_z",
        "min_predation_relief",
        "min_positive_q_predation_interaction",
        "initial_g_effect_tolerance_z",
        "male_cell_range_tolerance_z",
    )
    out = dict(config)
    for key in numeric_keys:
        value = out.get(key)
        if value is None or value == PLACEHOLDER:
            raise ValueError(f"fitness config field {key!r} must be preregistered before analysis")
        try:
            out[key] = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"fitness config field {key!r} must be numeric") from exc
    for key in ("bootstrap_reps", "bootstrap_seed", "min_blocks", "min_q_levels", "min_units_per_q_by_g_cell"):
        if out[key] < 1:
            raise ValueError(f"fitness config field {key!r} must be >= 1")
        out[key] = int(out[key])
    for key in numeric_keys[5:]:
        if out[key] < 0:
            raise ValueError(f"fitness config field {key!r} must be >= 0")
    if out["min_valid_predation_fraction_per_cell"] > 1:
        raise ValueError("min_valid_predation_fraction_per_cell must be <= 1")
    return out


def _solve3(matrix: list[list[float]], rhs: list[float]) -> tuple[float, float, float]:
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("quadratic fit is singular")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(3):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [a - factor * b for a, b in zip(aug[row], aug[col])]
    return aug[0][3], aug[1][3], aug[2][3]


def _fit_quadratic(points: list[tuple[float, float]]) -> dict:
    if len(points) < 3 or len({round(x, 12) for x, _ in points}) < 3:
        raise ValueError("quadratic surface requires at least three distinct q levels")
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    n = float(len(points))
    s1 = sum(xs)
    s2 = sum(x * x for x in xs)
    s3 = sum(x**3 for x in xs)
    s4 = sum(x**4 for x in xs)
    t0 = sum(ys)
    t1 = sum(x * y for x, y in points)
    t2 = sum((x * x) * y for x, y in points)
    a, b, c = _solve3([[n, s1, s2], [s1, s2, s3], [s2, s3, s4]], [t0, t1, t2])
    q_min, q_max = min(xs), max(xs)
    discrete_q = points[max(range(len(points)), key=lambda i: points[i][1])][0]
    vertex = None
    if c < 0:
        candidate = -b / (2 * c)
        if q_min <= candidate <= q_max:
            vertex = candidate
    optimum = vertex if vertex is not None else discrete_q
    return {
        "a": a,
        "b": b,
        "c": c,
        "q_min": q_min,
        "q_max": q_max,
        "primary_optimum": optimum,
        "optimum_class": "INTERIOR_CONCAVE" if vertex is not None else "BOUNDARY_OR_NONCONCAVE",
        "points": [{"q": q, "mean": y} for q, y in sorted(points)],
    }


def _population_sd(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError("standardized contrast requires at least two observations")
    center = mean(values)
    variance = sum((value - center) ** 2 for value in values) / len(values)
    if variance <= 1e-15:
        raise ValueError("standardized contrast is undefined for a constant outcome")
    return math.sqrt(variance)


def _cell_rows(rows: list[dict[str, str]]) -> dict[tuple[float, int], list[dict[str, str]]]:
    groups: dict[tuple[float, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(_num(row, "q_target"), _g(row))].append(row)
    return groups


def _cell_mean(groups: dict[tuple[float, int], list[dict[str, str]]], q: float, g: int, field: str) -> float:
    return mean(_num(row, field) for row in groups[(q, g)])


def _predation_cell_rates(groups: dict[tuple[float, int], list[dict[str, str]]]) -> tuple[dict[tuple[float, int], float], dict[tuple[float, int], float]]:
    means: dict[tuple[float, int], float] = {}
    valid_fraction: dict[tuple[float, int], float] = {}
    for key, group in groups.items():
        rates = []
        for row in group:
            initial = _num(row, "initial_fruits")
            if initial > 0:
                rates.append(_num(row, "predated_fruits") / initial)
        valid_fraction[key] = len(rates) / len(group)
        if not rates:
            raise ValueError(f"predation rate undefined in cell {key}")
        means[key] = mean(rates)
    return means, valid_fraction


def _core_metrics(rows: list[dict[str, str]]) -> dict:
    groups = _cell_rows(rows)
    q_levels = sorted({q for q, _ in groups})
    q_low, q_high = q_levels[0], q_levels[-1]

    final_surfaces = {}
    for g in (0, 1):
        final_surfaces[g] = _fit_quadratic(
            [(q, _cell_mean(groups, q, g, "final_intact_fruits")) for q in q_levels]
        )
    optimum_shift = final_surfaces[1]["primary_optimum"] - final_surfaces[0]["primary_optimum"]

    initial_sd = _population_sd([_num(row, "initial_fruits") for row in rows])
    initial_low = mean(_cell_mean(groups, q_low, g, "initial_fruits") for g in (0, 1))
    initial_high = mean(_cell_mean(groups, q_high, g, "initial_fruits") for g in (0, 1))
    initial_gain_z = (initial_high - initial_low) / initial_sd
    initial_g_effects_z = {
        q: abs(_cell_mean(groups, q, 1, "initial_fruits") - _cell_mean(groups, q, 0, "initial_fruits")) / initial_sd
        for q in q_levels
    }
    initial_g_max_abs_z = max(initial_g_effects_z.values())

    egg_sd = _population_sd([_num(row, "eggs_before_g_treatment") for row in rows])
    egg_low = mean(_cell_mean(groups, q_low, g, "eggs_before_g_treatment") for g in (0, 1))
    egg_high = mean(_cell_mean(groups, q_high, g, "eggs_before_g_treatment") for g in (0, 1))
    oviposition_gain_z = (egg_high - egg_low) / egg_sd

    predation_means, predation_valid_fraction = _predation_cell_rates(groups)
    removed_all = [predation_means[(q, 0)] for q in q_levels]
    retained_all = [predation_means[(q, 1)] for q in q_levels]
    predation_relief = mean(retained_all) - mean(removed_all)
    q_predation_interaction = (
        predation_means[(q_high, 1)] - predation_means[(q_low, 1)]
        - predation_means[(q_high, 0)] + predation_means[(q_low, 0)]
    )

    male_values = [_num(row, "male_fitness") for row in rows]
    male_sd = _population_sd(male_values)
    male_cell_means = {key: mean(_num(row, "male_fitness") for row in group) for key, group in groups.items()}
    male_cell_range_z = (max(male_cell_means.values()) - min(male_cell_means.values())) / male_sd

    return {
        "q_levels": q_levels,
        "final_surfaces": {G_REMOVED: final_surfaces[0], G_RETAINED: final_surfaces[1]},
        "q_optimum_removed": final_surfaces[0]["primary_optimum"],
        "q_optimum_retained": final_surfaces[1]["primary_optimum"],
        "optimum_shift_q": optimum_shift,
        "initial_high_vs_low_gain_z": initial_gain_z,
        "initial_g_max_abs_z": initial_g_max_abs_z,
        "initial_g_abs_effect_z_by_q": {str(q): initial_g_effects_z[q] for q in q_levels},
        "oviposition_high_vs_low_gain_z": oviposition_gain_z,
        "predation_relief": predation_relief,
        "q_predation_interaction": q_predation_interaction,
        "predation_rate_by_cell": {f"q={q}|g={G_RETAINED if g else G_REMOVED}": value for (q, g), value in predation_means.items()},
        "predation_valid_fraction_by_cell": {f"q={q}|g={G_RETAINED if g else G_REMOVED}": value for (q, g), value in predation_valid_fraction.items()},
        "male_cell_range_z": male_cell_range_z,
        "male_cell_means": {f"q={q}|g={G_RETAINED if g else G_REMOVED}": value for (q, g), value in male_cell_means.items()},
    }


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of empty values")
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return ordered[lo]
    weight = position - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def _bootstrap(rows: list[dict[str, str]], reps: int, seed: int) -> dict:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["block_id"]].append(row)
    blocks = sorted(grouped)
    rng = random.Random(seed)
    keys = (
        "optimum_shift_q",
        "initial_high_vs_low_gain_z",
        "initial_g_max_abs_z",
        "oviposition_high_vs_low_gain_z",
        "predation_relief",
        "q_predation_interaction",
        "male_cell_range_z",
    )
    collected = {key: [] for key in keys}
    failures = 0
    for _ in range(reps):
        sampled: list[dict[str, str]] = []
        for block in (rng.choice(blocks) for _ in blocks):
            sampled.extend(grouped[block])
        try:
            metrics = _core_metrics(sampled)
        except ValueError:
            failures += 1
            continue
        for key in keys:
            value = metrics[key]
            if math.isfinite(value):
                collected[key].append(value)
    effective = min(len(values) for values in collected.values())
    minimum_effective = max(20, int(math.ceil(reps * 0.8)))
    if effective < minimum_effective:
        raise ValueError(
            f"too many failed Stage-B block-bootstrap replicates: effective={effective}, required>={minimum_effective}"
        )
    return {
        "resampling_unit": "block_id",
        "requested_reps": reps,
        "effective_reps": effective,
        "failed_reps": failures,
        "intervals": {
            key: {
                "lower_95": _quantile(values, 0.025),
                "median": _quantile(values, 0.5),
                "upper_95": _quantile(values, 0.975),
            }
            for key, values in collected.items()
        },
    }


def analyze(rows: list[dict[str, str]], validation_config: dict, fitness_config: dict) -> dict:
    validation_receipt = validate_stage_b_manipulation(rows, validation_config)
    if validation_receipt["status"] != "PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED":
        return {
            "receipt_schema_version": RECEIPT_SCHEMA,
            "status": "BLOCKED_BY_INVALID_STAGE_B_MANIPULATION",
            "validation_receipt": validation_receipt,
            "claim_ceiling": "no_fitness_inference_permitted_until_stage_b_manipulation_validation_passes",
        }

    config = _require_config(fitness_config)
    core = _core_metrics(rows)
    bootstrap = _bootstrap(rows, config["bootstrap_reps"], config["bootstrap_seed"])
    ci = bootstrap["intervals"]
    groups = _cell_rows(rows)
    n_blocks = len({row["block_id"] for row in rows})
    q_levels = core["q_levels"]
    cell_counts = {key: len(group) for key, group in groups.items()}

    coverage_gate = (
        n_blocks >= config["min_blocks"]
        and len(q_levels) >= config["min_q_levels"]
        and all(count >= config["min_units_per_q_by_g_cell"] for count in cell_counts.values())
        and all(
            fraction >= config["min_valid_predation_fraction_per_cell"]
            for fraction in core["predation_valid_fraction_by_cell"].values()
        )
    )

    optimum_gate = core["optimum_shift_q"] <= -config["min_negative_optimum_shift_q"]
    if config.get("require_optimum_shift_bootstrap_upper_below_zero", True):
        optimum_gate = optimum_gate and ci["optimum_shift_q"]["upper_95"] < 0

    initial_gain_gate = core["initial_high_vs_low_gain_z"] >= config["min_initial_high_vs_low_gain_z"]
    if config.get("require_initial_gain_bootstrap_lower_above_minimum", True):
        initial_gain_gate = initial_gain_gate and ci["initial_high_vs_low_gain_z"]["lower_95"] > config["min_initial_high_vs_low_gain_z"]

    oviposition_gate = core["oviposition_high_vs_low_gain_z"] >= config["min_positive_q_oviposition_gain_z"]
    if config.get("require_oviposition_gain_bootstrap_lower_above_minimum", True):
        oviposition_gate = oviposition_gate and ci["oviposition_high_vs_low_gain_z"]["lower_95"] > config["min_positive_q_oviposition_gain_z"]

    predation_relief_gate = core["predation_relief"] >= config["min_predation_relief"]
    predation_interaction_gate = core["q_predation_interaction"] >= config["min_positive_q_predation_interaction"]
    if config.get("require_predation_interaction_bootstrap_lower_above_minimum", True):
        predation_interaction_gate = predation_interaction_gate and ci["q_predation_interaction"]["lower_95"] > config["min_positive_q_predation_interaction"]

    if config.get("require_equivalence_bootstrap_upper_below_tolerance", True):
        initial_g_gate = ci["initial_g_max_abs_z"]["upper_95"] <= config["initial_g_effect_tolerance_z"]
        male_gate = ci["male_cell_range_z"]["upper_95"] <= config["male_cell_range_tolerance_z"]
    else:
        initial_g_gate = core["initial_g_max_abs_z"] <= config["initial_g_effect_tolerance_z"]
        male_gate = core["male_cell_range_z"] <= config["male_cell_range_tolerance_z"]

    gates = {
        "same_dataset_stage_b_manipulation_validated": True,
        "factorial_coverage": coverage_gate,
        "female_opportunity_increases_with_q": initial_gain_gate,
        "G_does_not_change_initial_female_opportunity": initial_g_gate,
        "randomized_q_increases_predator_oviposition": oviposition_gate,
        "egg_removal_reduces_predation": predation_relief_gate,
        "predation_cost_increases_with_q_under_G": predation_interaction_gate,
        "female_fitness_optimum_shifts_to_lower_q_under_antagonism": optimum_gate,
        "male_function_preserved_across_q_by_G_cells": male_gate,
    }
    supported = all(gates.values())

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "validated_randomized_q_by_antagonist_factorial_in_peucedanum",
        "design": config["design"],
        "validation_receipt": validation_receipt,
        "n_units": len(rows),
        "n_blocks": n_blocks,
        "q_levels": q_levels,
        "n_by_q_by_g_cell": {
            f"q={q}|g={G_RETAINED if g else G_REMOVED}": count for (q, g), count in cell_counts.items()
        },
        "primary_estimand": {
            "name": "Delta_q_star",
            "definition": "q_star_retained_minus_q_star_removed_on_final_intact_fruit_surface",
            "q_star_removed": core["q_optimum_removed"],
            "q_star_retained": core["q_optimum_retained"],
            "estimate": core["optimum_shift_q"],
            "block_bootstrap_ci95": ci["optimum_shift_q"],
            "prediction": "negative",
        },
        "female_final_surfaces": core["final_surfaces"],
        "mechanism_estimands": {
            "initial_high_vs_low_gain_z": {
                "estimate": core["initial_high_vs_low_gain_z"],
                "block_bootstrap_ci95": ci["initial_high_vs_low_gain_z"],
            },
            "initial_g_max_abs_z": {
                "estimate": core["initial_g_max_abs_z"],
                "block_bootstrap_ci95": ci["initial_g_max_abs_z"],
            },
            "oviposition_high_vs_low_gain_z": {
                "estimate": core["oviposition_high_vs_low_gain_z"],
                "block_bootstrap_ci95": ci["oviposition_high_vs_low_gain_z"],
                "causal_interpretation": "q is randomized and eggs are counted before G treatment",
            },
            "predation_relief": {
                "estimate": core["predation_relief"],
                "block_bootstrap_ci95": ci["predation_relief"],
            },
            "q_predation_interaction": {
                "estimate": core["q_predation_interaction"],
                "block_bootstrap_ci95": ci["q_predation_interaction"],
            },
            "male_cell_range_z": {
                "estimate": core["male_cell_range_z"],
                "block_bootstrap_ci95": ci["male_cell_range_z"],
            },
        },
        "predation_rate_by_cell": core["predation_rate_by_cell"],
        "predation_valid_fraction_by_cell": core["predation_valid_fraction_by_cell"],
        "male_cell_means": core["male_cell_means"],
        "bootstrap": bootstrap,
        "gates": gates,
        "status": (
            "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_SUPPORTED"
            if supported
            else "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_NOT_FULLY_RECOVERED"
        ),
        "claim_ceiling": (
            "contemporary_causal_partial_functional_differentiation_in_a_validated_post_male_phase_manipulation; "
            "does_not_establish_natural_developmental_origin; not_complete_modularity; not_historical_origin_of_andromonoecy"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze validated Peucedanum Stage-B randomized q x antagonist fitness data")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("validation_config_path", type=Path)
    parser.add_argument("fitness_config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    validation_config = json.loads(args.validation_config_path.read_text(encoding="utf-8"))
    fitness_config = json.loads(args.fitness_config_path.read_text(encoding="utf-8"))
    result = analyze(rows, validation_config, fitness_config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
