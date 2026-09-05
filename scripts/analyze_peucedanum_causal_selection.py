from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from trait_architecture.ols_hc3 import fit_ols_hc3


REQUIRED_FIELDS = (
    "plant_id",
    "block_id",
    "g_state",
    "perfect_flowers",
    "male_flowers",
    "total_flowers",
    "q_perfect",
    "flower_height",
    "flowering_day",
    "eggs_before",
    "initial_fruits",
    "final_intact_fruits",
    "predated_fruits",
    "male_fitness",
)

RECEIPT_SCHEMA = "BITA_PEUCEDANUM_CAUSAL_SELECTION_STAGE_A_V1"
G_REMOVED = "EGGS_REMOVED"
G_RETAINED = "EGGS_RETAINED"
MODEL_TERMS = (
    "Intercept",
    "q_z",
    "G",
    "q_z:G",
    "total_flower_z",
    "flower_height_z",
    "flowering_day_z",
)
PLACEHOLDER = "REQUIRED_BEFORE_USE"


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError, TypeError) as exc:
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

    seen_plants: set[str] = set()
    block_states: dict[str, set[int]] = defaultdict(set)
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        plant_id = row["plant_id"].strip()
        if plant_id in seen_plants:
            raise ValueError(f"duplicate plant_id {plant_id!r}")
        seen_plants.add(plant_id)
        block_states[row["block_id"].strip()].add(_g(row))

        numeric_fields = REQUIRED_FIELDS[3:]
        for field in numeric_fields:
            _num(row, field)

        perfect = _num(row, "perfect_flowers")
        male = _num(row, "male_flowers")
        total = _num(row, "total_flowers")
        q = _num(row, "q_perfect")
        eggs = _num(row, "eggs_before")
        initial = _num(row, "initial_fruits")
        intact = _num(row, "final_intact_fruits")
        predated = _num(row, "predated_fruits")
        male_fit = _num(row, "male_fitness")

        if perfect < 0 or male < 0 or total <= 0:
            raise ValueError("flower counts must be non-negative and total_flowers must be > 0")
        if abs((perfect + male) - total) > max(1e-6, 1e-6 * total):
            raise ValueError("total_flowers must equal perfect_flowers + male_flowers")
        expected_q = perfect / total
        if not 0 <= q <= 1 or abs(q - expected_q) > 1e-6:
            raise ValueError("q_perfect must equal perfect_flowers / total_flowers on [0,1]")
        if eggs < 0 or initial < 0 or intact < 0 or predated < 0 or male_fit < 0:
            raise ValueError("egg, fruit and male-fitness outcomes must be non-negative")
        if initial > perfect + 1e-6:
            raise ValueError("initial_fruits cannot exceed perfect_flowers")
        if intact + predated > initial + 1e-6:
            raise ValueError("final_intact_fruits + predated_fruits cannot exceed initial_fruits")

    bad_blocks = [block for block, states in block_states.items() if states != {0, 1}]
    if bad_blocks:
        raise ValueError(
            "within-block design requires both egg-removal and retained states in every block; "
            f"invalid blocks include {bad_blocks[:5]}"
        )
    return rows


def _require_config(config: dict) -> dict:
    if config.get("randomization_scheme") != "WITHIN_BLOCK_EGG_REMOVAL_VS_RETENTION":
        raise ValueError("config must declare WITHIN_BLOCK_EGG_REMOVAL_VS_RETENTION")
    numeric_keys = (
        "bootstrap_reps",
        "bootstrap_seed",
        "min_blocks",
        "min_units_per_g_state",
        "min_valid_predation_units_per_g_state",
        "max_abs_pretreatment_smd",
        "min_negative_delta_beta_q",
        "min_predation_relief",
        "initial_effect_tolerance_z",
        "male_effect_tolerance_z",
    )
    out = dict(config)
    for key in numeric_keys:
        value = out.get(key)
        if value is None or value == PLACEHOLDER:
            raise ValueError(f"config field {key!r} must be preregistered before analysis")
        try:
            out[key] = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"config field {key!r} must be numeric") from exc
    for key in ("bootstrap_reps", "bootstrap_seed", "min_blocks", "min_units_per_g_state", "min_valid_predation_units_per_g_state"):
        if out[key] < 1:
            raise ValueError(f"config field {key!r} must be >= 1")
        out[key] = int(out[key])
    for key in ("max_abs_pretreatment_smd", "min_negative_delta_beta_q", "min_predation_relief", "initial_effect_tolerance_z", "male_effect_tolerance_z"):
        if out[key] < 0:
            raise ValueError(f"config field {key!r} must be >= 0")
    return out


def _zscore(values: list[float]) -> list[float]:
    if len(values) < 2:
        raise ValueError("standardization requires at least two values")
    center = mean(values)
    variance = sum((value - center) ** 2 for value in values) / len(values)
    if variance <= 1e-15:
        raise ValueError("standardization is undefined for a constant variable")
    scale = math.sqrt(variance)
    return [(value - center) / scale for value in values]


def _coefficient_map(result) -> dict[str, dict[str, float]]:
    return {
        coefficient.term: {
            "estimate": coefficient.estimate,
            "hc3_se": coefficient.hc3_se,
            "z_value": coefficient.z_value,
            "p_value_normal": coefficient.p_value_normal,
            "ci95_lower": coefficient.ci95_lower,
            "ci95_upper": coefficient.ci95_upper,
        }
        for coefficient in result.coefficients
    }


def _fit_selection_model(rows: list[dict[str, str]], response_field: str) -> dict:
    q_z = _zscore([_num(row, "q_perfect") for row in rows])
    total_z = _zscore([_num(row, "total_flowers") for row in rows])
    height_z = _zscore([_num(row, "flower_height") for row in rows])
    day_z = _zscore([_num(row, "flowering_day") for row in rows])
    response_z = _zscore([_num(row, response_field) for row in rows])
    g = [_g(row) for row in rows]
    design = [
        [1.0, q, float(state), q * state, total, height, day]
        for q, state, total, height, day in zip(q_z, g, total_z, height_z, day_z)
    ]
    result = fit_ols_hc3(response_z, design, MODEL_TERMS)
    return {
        "response": response_field,
        "standardization": "global_z_score_for_response_and_continuous_predictors",
        "n": result.n,
        "r_squared": result.r_squared,
        "coefficients": _coefficient_map(result),
    }


def _fit_oviposition_model(rows: list[dict[str, str]]) -> dict:
    terms = ("Intercept", "q_z", "total_flower_z", "flower_height_z", "flowering_day_z")
    q_z = _zscore([_num(row, "q_perfect") for row in rows])
    total_z = _zscore([_num(row, "total_flowers") for row in rows])
    height_z = _zscore([_num(row, "flower_height") for row in rows])
    day_z = _zscore([_num(row, "flowering_day") for row in rows])
    eggs_z = _zscore([_num(row, "eggs_before") for row in rows])
    design = [[1.0, q, total, height, day] for q, total, height, day in zip(q_z, total_z, height_z, day_z)]
    result = fit_ols_hc3(eggs_z, design, terms)
    return {
        "response": "eggs_before",
        "observational_with_respect_to_q": True,
        "n": result.n,
        "r_squared": result.r_squared,
        "coefficients": _coefficient_map(result),
    }


def _sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return math.sqrt(sum((value - center) ** 2 for value in values) / (len(values) - 1))


def _smd(rows: list[dict[str, str]], field: str) -> float:
    removed = [_num(row, field) for row in rows if _g(row) == 0]
    retained = [_num(row, field) for row in rows if _g(row) == 1]
    s0, s1 = _sample_sd(removed), _sample_sd(retained)
    pooled = math.sqrt((s0 * s0 + s1 * s1) / 2.0)
    difference = mean(retained) - mean(removed)
    if pooled <= 1e-15:
        return 0.0 if abs(difference) <= 1e-15 else math.copysign(math.inf, difference)
    return difference / pooled


def _balance_summary(rows: list[dict[str, str]]) -> dict:
    fields = (
        "q_perfect",
        "perfect_flowers",
        "male_flowers",
        "total_flowers",
        "flower_height",
        "flowering_day",
        "eggs_before",
    )
    smd = {field: _smd(rows, field) for field in fields}
    return {
        "standardized_mean_differences_retained_minus_removed": smd,
        "max_abs_smd": max(abs(value) for value in smd.values()),
    }


def _predation_rates(rows: list[dict[str, str]]) -> dict[int, list[float]]:
    rates: dict[int, list[float]] = {0: [], 1: []}
    for row in rows:
        initial = _num(row, "initial_fruits")
        if initial > 0:
            rates[_g(row)].append(_num(row, "predated_fruits") / initial)
    return rates


def _predation_relief(rows: list[dict[str, str]]) -> tuple[float, dict[int, int], dict[int, float]]:
    rates = _predation_rates(rows)
    if not rates[0] or not rates[1]:
        raise ValueError("predation relief requires initial_fruits > 0 in both G states")
    means = {state: mean(values) for state, values in rates.items()}
    return means[1] - means[0], {state: len(values) for state, values in rates.items()}, means


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of an empty list")
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return ordered[lo]
    weight = position - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight


def _core_metrics(rows: list[dict[str, str]]) -> dict:
    final_model = _fit_selection_model(rows, "final_intact_fruits")
    initial_model = _fit_selection_model(rows, "initial_fruits")
    male_model = _fit_selection_model(rows, "male_fitness")
    oviposition_model = _fit_oviposition_model(rows)
    relief, predation_n, predation_means = _predation_relief(rows)
    return {
        "delta_beta_q": final_model["coefficients"]["q_z:G"]["estimate"],
        "predation_relief": relief,
        "initial_G": initial_model["coefficients"]["G"]["estimate"],
        "initial_qG": initial_model["coefficients"]["q_z:G"]["estimate"],
        "male_q": male_model["coefficients"]["q_z"]["estimate"],
        "male_G": male_model["coefficients"]["G"]["estimate"],
        "male_qG": male_model["coefficients"]["q_z:G"]["estimate"],
        "oviposition_q": oviposition_model["coefficients"]["q_z"]["estimate"],
        "models": {
            "female_final": final_model,
            "initial_female_opportunity": initial_model,
            "male_fitness": male_model,
            "pre_treatment_oviposition": oviposition_model,
        },
        "predation": {
            "valid_n_by_g": {G_REMOVED: predation_n[0], G_RETAINED: predation_n[1]},
            "mean_rate_by_g": {G_REMOVED: predation_means[0], G_RETAINED: predation_means[1]},
            "retained_minus_removed": relief,
        },
    }


def _bootstrap(rows: list[dict[str, str]], reps: int, seed: int) -> dict:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["block_id"]].append(row)
    blocks = sorted(grouped)
    rng = random.Random(seed)
    collected = {key: [] for key in (
        "delta_beta_q",
        "predation_relief",
        "initial_G",
        "initial_qG",
        "male_q",
        "male_G",
        "male_qG",
        "oviposition_q",
    )}
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
        for key in collected:
            value = metrics[key]
            if math.isfinite(value):
                collected[key].append(value)
    effective = min(len(values) for values in collected.values())
    minimum_effective = max(20, int(math.ceil(reps * 0.8)))
    if effective < minimum_effective:
        raise ValueError(
            f"too many failed block-bootstrap replicates: effective={effective}, required>={minimum_effective}, failures={failures}"
        )
    intervals = {
        key: {
            "lower_95": _quantile(values, 0.025),
            "median": _quantile(values, 0.5),
            "upper_95": _quantile(values, 0.975),
        }
        for key, values in collected.items()
    }
    return {
        "resampling_unit": "block_id",
        "requested_reps": reps,
        "effective_reps": effective,
        "failed_reps": failures,
        "intervals": intervals,
    }


def _inside_equivalence(interval: dict[str, float], tolerance: float) -> bool:
    return interval["lower_95"] >= -tolerance and interval["upper_95"] <= tolerance


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    config = _require_config(config)
    n_blocks = len({row["block_id"] for row in rows})
    n_by_g = {
        G_REMOVED: sum(_g(row) == 0 for row in rows),
        G_RETAINED: sum(_g(row) == 1 for row in rows),
    }
    core = _core_metrics(rows)
    balance = _balance_summary(rows)
    bootstrap = _bootstrap(rows, config["bootstrap_reps"], config["bootstrap_seed"])
    ci = bootstrap["intervals"]

    coverage_gate = (
        n_blocks >= config["min_blocks"]
        and n_by_g[G_REMOVED] >= config["min_units_per_g_state"]
        and n_by_g[G_RETAINED] >= config["min_units_per_g_state"]
        and core["predation"]["valid_n_by_g"][G_REMOVED] >= config["min_valid_predation_units_per_g_state"]
        and core["predation"]["valid_n_by_g"][G_RETAINED] >= config["min_valid_predation_units_per_g_state"]
    )
    balance_gate = balance["max_abs_smd"] <= config["max_abs_pretreatment_smd"]

    delta_gate = core["delta_beta_q"] <= -config["min_negative_delta_beta_q"]
    if config.get("require_delta_beta_bootstrap_upper_below_zero", True):
        delta_gate = delta_gate and ci["delta_beta_q"]["upper_95"] < 0.0

    relief_gate = core["predation_relief"] >= config["min_predation_relief"]
    if config.get("require_predation_relief_bootstrap_lower_above_minimum", True):
        relief_gate = relief_gate and ci["predation_relief"]["lower_95"] > config["min_predation_relief"]

    initial_tol = config["initial_effect_tolerance_z"]
    male_tol = config["male_effect_tolerance_z"]
    if config.get("require_equivalence_ci_inside_tolerance", True):
        initial_gate = _inside_equivalence(ci["initial_G"], initial_tol) and _inside_equivalence(ci["initial_qG"], initial_tol)
        male_gate = (
            _inside_equivalence(ci["male_q"], male_tol)
            and _inside_equivalence(ci["male_G"], male_tol)
            and _inside_equivalence(ci["male_qG"], male_tol)
        )
    else:
        initial_gate = abs(core["initial_G"]) <= initial_tol and abs(core["initial_qG"]) <= initial_tol
        male_gate = (
            abs(core["male_q"]) <= male_tol
            and abs(core["male_G"]) <= male_tol
            and abs(core["male_qG"]) <= male_tol
        )

    gates = {
        "coverage": coverage_gate,
        "pretreatment_randomization_balance": balance_gate,
        "predation_relief": relief_gate,
        "negative_antagonism_dependent_selection_shift": delta_gate,
        "initial_female_opportunity_equivalence": initial_gate,
        "male_function_equivalence": male_gate,
    }
    supported = all(gates.values())

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "randomized_antagonism_dependent_selection_on_natural_peucedanum_sex_allocation",
        "randomization_scheme": config["randomization_scheme"],
        "n_plants": len(rows),
        "n_blocks": n_blocks,
        "n_by_g": n_by_g,
        "primary_estimand": {
            "name": "Delta_beta_q",
            "definition": "beta_q_retained_minus_beta_q_removed_equals_q_by_G_interaction_on_standardized_final_intact_fruits",
            "estimate": core["delta_beta_q"],
            "block_bootstrap_ci95": ci["delta_beta_q"],
            "prediction": "negative",
        },
        "predation_relief": {
            **core["predation"],
            "block_bootstrap_ci95": ci["predation_relief"],
        },
        "pretreatment_balance": balance,
        "equivalence_estimands": {
            "initial_female_opportunity": {
                "G": {"estimate": core["initial_G"], "block_bootstrap_ci95": ci["initial_G"]},
                "q_by_G": {"estimate": core["initial_qG"], "block_bootstrap_ci95": ci["initial_qG"]},
                "tolerance_z": initial_tol,
            },
            "male_function": {
                "q": {"estimate": core["male_q"], "block_bootstrap_ci95": ci["male_q"]},
                "G": {"estimate": core["male_G"], "block_bootstrap_ci95": ci["male_G"]},
                "q_by_G": {"estimate": core["male_qG"], "block_bootstrap_ci95": ci["male_qG"]},
                "tolerance_z": male_tol,
            },
        },
        "secondary_oviposition_association": {
            "q_z_coefficient": core["oviposition_q"],
            "block_bootstrap_ci95": ci["oviposition_q"],
            "causal_with_respect_to_q": False,
        },
        "models": core["models"],
        "bootstrap": bootstrap,
        "gates": gates,
        "status": (
            "CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_ON_SEX_ALLOCATION"
            if supported
            else "CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_NOT_FULLY_RECOVERED"
        ),
        "claim_ceiling": (
            "randomized_antagonist_context_changes_the_fitness_landscape_over_natural_sex_allocation; "
            "q_itself_not_randomized; not_canonical_R_state; not_complete_modularity; not_historical_origin_of_andromonoecy"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Peucedanum Stage-A randomized egg-removal causal-selection data")
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
