"""Confirmatory Stage-1 analysis for the relative-route-cost 2 x 2 experiment.

Primary inference is bee-level. Event rows are never treated as independent
replicates. Two predeclared directional contrasts test sign reversal:

  C_L = p(HL) - p(LL) > 0
  C_B = p(LH) - p(LL) < 0

Each is tested by bee-level sign-flip randomization with Bonferroni alpha 0.025.
The HH-vs-LL contrast is a secondary equivalence diagnostic.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path

TARGET_BEES = 60
TRIALS_PER_CONDITION = 10
PERMUTATIONS = 9999
PRIMARY_ALPHA = 0.025
EQUIVALENCE_MARGIN = 0.10
BOOTSTRAPS = 9999
SEED = 20260929

CONDITIONS = ("LL", "HL", "LH", "HH")
REQUIRED_COLUMNS = {
    "bee_id",
    "colony_id",
    "trial_id",
    "trial_order",
    "condition",
    "legitimate_cost_level",
    "bypass_cost_level",
    "successful_route",
    "reward_acquired",
    "trial_valid",
}

EXPECTED_LEVELS = {
    "LL": ("low", "low"),
    "HL": ("high", "low"),
    "LH": ("low", "high"),
    "HH": ("high", "high"),
}


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires data")
    return sum(values) / len(values)


def _as_bool(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("choice-event CSV is empty")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(f"missing choice-event columns: {sorted(missing)}")
    return rows


def _one_sided_sign_flip_p(
    differences: list[float],
    *,
    direction: str,
    permutations: int,
    seed: int,
) -> float:
    if not differences:
        raise ValueError("sign-flip test requires differences")
    observed = _mean(differences)
    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        value = _mean([
            diff if rng.getrandbits(1) else -diff
            for diff in differences
        ])
        if direction == "greater":
            if value >= observed - 1e-15:
                extreme += 1
        elif direction == "less":
            if value <= observed + 1e-15:
                extreme += 1
        else:
            raise ValueError("direction must be greater or less")
    return (extreme + 1) / (permutations + 1)


def _bootstrap_mean_ci(
    values: list[float],
    *,
    bootstraps: int,
    seed: int,
) -> tuple[float, float]:
    if not values:
        raise ValueError("bootstrap requires values")
    rng = random.Random(seed)
    n = len(values)
    estimates = []
    for _ in range(bootstraps):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        estimates.append(_mean(sample))
    estimates.sort()
    lo_i = max(0, math.floor(0.025 * (bootstraps - 1)))
    hi_i = min(bootstraps - 1, math.ceil(0.975 * (bootstraps - 1)))
    return estimates[lo_i], estimates[hi_i]


def analyze_choice_events(
    rows: list[dict[str, str]],
    *,
    permutations: int = PERMUTATIONS,
    bootstraps: int = BOOTSTRAPS,
    seed: int = SEED,
) -> dict[str, object]:
    valid: dict[tuple[str, str], list[int]] = defaultdict(list)
    colony_by_bee: dict[str, str] = {}
    invalid_rows = 0

    for row in rows:
        bee = str(row["bee_id"]).strip()
        colony = str(row["colony_id"]).strip()
        condition = str(row["condition"]).strip().upper()
        if not bee or not colony:
            raise ValueError("bee_id and colony_id are required")
        if condition not in CONDITIONS:
            raise ValueError(f"invalid condition: {condition!r}")

        l_level = str(row["legitimate_cost_level"]).strip().lower()
        b_level = str(row["bypass_cost_level"]).strip().lower()
        if (l_level, b_level) != EXPECTED_LEVELS[condition]:
            raise ValueError(
                f"condition/level mismatch for {condition}: {(l_level, b_level)}"
            )

        prior_colony = colony_by_bee.setdefault(bee, colony)
        if prior_colony != colony:
            raise ValueError(f"bee {bee} appears in multiple colonies")

        if not _as_bool(row["trial_valid"]):
            invalid_rows += 1
            continue

        if not _as_bool(row["reward_acquired"]):
            raise ValueError("valid choice trial must end in reward acquisition")

        route = str(row["successful_route"]).strip().lower()
        if route not in {"legitimate", "bypass"}:
            raise ValueError("valid choice trial must resolve legitimate or bypass route")

        valid[(bee, condition)].append(1 if route == "bypass" else 0)

    bees = sorted(colony_by_bee)
    completed = []
    incomplete: dict[str, dict[str, int]] = {}
    for bee in bees:
        counts = {condition: len(valid[(bee, condition)]) for condition in CONDITIONS}
        if all(count == TRIALS_PER_CONDITION for count in counts.values()):
            completed.append(bee)
        else:
            incomplete[bee] = counts

    if len(completed) != TARGET_BEES:
        raise ValueError(
            f"confirmatory dataset must contain exactly {TARGET_BEES} completed bees; "
            f"found {len(completed)}"
        )

    p: dict[str, dict[str, float]] = {}
    for bee in completed:
        p[bee] = {
            condition: _mean([float(x) for x in valid[(bee, condition)]])
            for condition in CONDITIONS
        }

    d_l = [p[bee]["HL"] - p[bee]["LL"] for bee in completed]
    d_b = [p[bee]["LH"] - p[bee]["LL"] for bee in completed]
    d_hh = [p[bee]["HH"] - p[bee]["LL"] for bee in completed]

    c_l = _mean(d_l)
    c_b = _mean(d_b)
    c_hh = _mean(d_hh)

    p_l = _one_sided_sign_flip_p(
        d_l,
        direction="greater",
        permutations=permutations,
        seed=seed,
    )
    p_b = _one_sided_sign_flip_p(
        d_b,
        direction="less",
        permutations=permutations,
        seed=seed + 1,
    )
    ci_hh = _bootstrap_mean_ci(
        d_hh,
        bootstraps=bootstraps,
        seed=seed + 2,
    )

    route_share = {
        condition: _mean([p[bee][condition] for bee in completed])
        for condition in CONDITIONS
    }

    by_colony: dict[str, list[str]] = defaultdict(list)
    for bee in completed:
        by_colony[colony_by_bee[bee]].append(bee)

    colony_sensitivity = {}
    for colony, colony_bees in sorted(by_colony.items()):
        colony_sensitivity[colony] = {
            "n_bees": len(colony_bees),
            "C_L": _mean([p[bee]["HL"] - p[bee]["LL"] for bee in colony_bees]),
            "C_B": _mean([p[bee]["LH"] - p[bee]["LL"] for bee in colony_bees]),
            "C_HH": _mean([p[bee]["HH"] - p[bee]["LL"] for bee in colony_bees]),
        }

    primary_pass = (
        c_l > 0
        and p_l < PRIMARY_ALPHA
        and c_b < 0
        and p_b < PRIMARY_ALPHA
    )
    compensation_pass = (
        ci_hh[0] >= -EQUIVALENCE_MARGIN
        and ci_hh[1] <= EQUIVALENCE_MARGIN
    )

    return {
        "analysis_name": "relative_route_cost_factorial_confirmatory",
        "primary_unit": "individual_bee",
        "completed_bees": len(completed),
        "valid_trials": sum(
            len(valid[(bee, condition)])
            for bee in completed
            for condition in CONDITIONS
        ),
        "invalid_trials_retained_in_audit": invalid_rows,
        "trials_per_condition_per_bee": TRIALS_PER_CONDITION,
        "condition_mean_bypass_proportion": route_share,
        "primary_contrasts": {
            "C_L_HL_minus_LL": {
                "estimate": c_l,
                "prediction": "positive",
                "one_sided_sign_flip_p": p_l,
                "alpha": PRIMARY_ALPHA,
                "passes": c_l > 0 and p_l < PRIMARY_ALPHA,
            },
            "C_B_LH_minus_LL": {
                "estimate": c_b,
                "prediction": "negative",
                "one_sided_sign_flip_p": p_b,
                "alpha": PRIMARY_ALPHA,
                "passes": c_b < 0 and p_b < PRIMARY_ALPHA,
            },
        },
        "primary_relative_route_cost_support": primary_pass,
        "compensation_diagnostic": {
            "C_HH_HH_minus_LL": c_hh,
            "bootstrap_95_ci": [ci_hh[0], ci_hh[1]],
            "equivalence_margin": [-EQUIVALENCE_MARGIN, EQUIVALENCE_MARGIN],
            "supported": compensation_pass,
        },
        "colony_sensitivity_descriptive": colony_sensitivity,
        "permutations": permutations,
        "bootstraps": bootstraps,
        "seed": seed,
        "claim_boundary": (
            "A primary pass supports causal relative-route-cost control of route choice "
            "in this artificial-flower bumblebee system. It does not establish a "
            "universal law across taxa or interaction types."
        ),
    }


def run(
    input_csv: str | Path,
    output_json: str | Path,
    *,
    permutations: int = PERMUTATIONS,
    bootstraps: int = BOOTSTRAPS,
    seed: int = SEED,
) -> dict[str, object]:
    result = analyze_choice_events(
        _read(input_csv),
        permutations=permutations,
        bootstraps=bootstraps,
        seed=seed,
    )
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_json")
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--bootstraps", type=int, default=BOOTSTRAPS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.input_csv,
                args.output_json,
                permutations=args.permutations,
                bootstraps=args.bootstraps,
                seed=args.seed,
            ),
            indent=2,
            sort_keys=True,
        )
    )
