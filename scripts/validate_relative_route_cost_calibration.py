"""Validate Stage-0 relative-route-cost engineering calibration.

The calibration is outcome-blind with respect to route choice because only one route
is available per calibration flower. It freezes a geometry version only when both
high-cost manipulations increase isolated-route handling cost, access remains
successful, and the two cost increments are approximately matched.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

MIN_BEES = 20
MIN_SUCCESSFUL_TRIALS_PER_STATE = 5
MIN_SUCCESS_RATE = 0.90
RATIO_LOW = 0.80
RATIO_HIGH = 1.25

REQUIRED_COLUMNS = {
    "bee_id",
    "colony_id",
    "geometry_version",
    "route",
    "cost_level",
    "trial_id",
    "handling_time_s",
    "reward_acquired",
    "failure_code",
}

ROUTES = {"legitimate", "bypass"}
LEVELS = {"low", "high"}
INVALID_HARDWARE_CODES = {"mechanical_failure", "reward_failure"}


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
        raise ValueError("calibration CSV is empty")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(f"missing calibration columns: {sorted(missing)}")
    return rows


def validate_calibration(rows: list[dict[str, str]]) -> dict[str, object]:
    versions = {str(row["geometry_version"]).strip() for row in rows}
    if len(versions) != 1 or "" in versions:
        raise ValueError("calibration input must contain exactly one geometry_version")
    version = next(iter(versions))

    attempts: dict[tuple[str, str], int] = defaultdict(int)
    successes: dict[tuple[str, str], int] = defaultdict(int)
    handling: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    invalid_hardware = 0

    for row in rows:
        bee = str(row["bee_id"]).strip()
        route = str(row["route"]).strip().lower()
        level = str(row["cost_level"]).strip().lower()
        if not bee:
            raise ValueError("blank bee_id")
        if route not in ROUTES:
            raise ValueError(f"invalid route: {route!r}")
        if level not in LEVELS:
            raise ValueError(f"invalid cost_level: {level!r}")

        failure_code = str(row.get("failure_code", "")).strip().lower()
        if failure_code in INVALID_HARDWARE_CODES:
            invalid_hardware += 1
            continue

        state = (route, level)
        attempts[state] += 1
        acquired = _as_bool(row["reward_acquired"])
        if not acquired:
            continue

        try:
            time_s = float(row["handling_time_s"])
        except (TypeError, ValueError) as exc:
            raise ValueError("successful calibration trial lacks numeric handling_time_s") from exc
        if not math.isfinite(time_s) or time_s <= 0:
            raise ValueError("handling_time_s must be positive and finite")

        successes[state] += 1
        handling[(bee, route, level)].append(math.log(time_s))

    states = [(route, level) for route in sorted(ROUTES) for level in sorted(LEVELS)]
    success_rates: dict[str, float] = {}
    for route, level in states:
        key = (route, level)
        if attempts[key] <= 0:
            raise ValueError(f"no valid calibration attempts for {route}/{level}")
        success_rates[f"{route}_{level}"] = successes[key] / attempts[key]

    bees = sorted({key[0] for key in handling})
    eligible: list[str] = []
    for bee in bees:
        if all(
            len(handling[(bee, route, level)]) >= MIN_SUCCESSFUL_TRIALS_PER_STATE
            for route, level in states
        ):
            eligible.append(bee)

    if not eligible:
        delta_l = None
        delta_b = None
        ratio = None
    else:
        bee_delta_l = [
            _mean(handling[(bee, "legitimate", "high")])
            - _mean(handling[(bee, "legitimate", "low")])
            for bee in eligible
        ]
        bee_delta_b = [
            _mean(handling[(bee, "bypass", "high")])
            - _mean(handling[(bee, "bypass", "low")])
            for bee in eligible
        ]
        delta_l = _mean(bee_delta_l)
        delta_b = _mean(bee_delta_b)
        ratio = delta_l / delta_b if delta_b > 0 else None

    gates = {
        "eligible_bees_ge_20": len(eligible) >= MIN_BEES,
        "delta_legitimate_positive": delta_l is not None and delta_l > 0,
        "delta_bypass_positive": delta_b is not None and delta_b > 0,
        "all_state_success_rates_ge_0_90": all(
            value >= MIN_SUCCESS_RATE for value in success_rates.values()
        ),
        "matched_increment_ratio_0_80_to_1_25": (
            ratio is not None and RATIO_LOW <= ratio <= RATIO_HIGH
        ),
    }

    return {
        "analysis_name": "relative_route_cost_stage0_calibration",
        "geometry_version": version,
        "raw_rows": len(rows),
        "invalid_hardware_trials_excluded": invalid_hardware,
        "eligible_bees": len(eligible),
        "minimum_completed_bees": MIN_BEES,
        "minimum_successful_trials_per_state_per_bee": MIN_SUCCESSFUL_TRIALS_PER_STATE,
        "state_success_rates": success_rates,
        "delta_legitimate_log_handling_time": delta_l,
        "delta_bypass_log_handling_time": delta_b,
        "delta_ratio_legitimate_over_bypass": ratio,
        "gates": gates,
        "passes_freeze_gate": all(gates.values()),
        "claim_boundary": (
            "This is an engineering calibration only. No route-choice outcome is "
            "available because each calibration flower exposes one route."
        ),
    }


def run(input_csv: str | Path, output_json: str | Path) -> dict[str, object]:
    result = validate_calibration(_read(input_csv))
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_json")
    args = parser.parse_args()
    print(json.dumps(run(args.input_csv, args.output_json), indent=2, sort_keys=True))
