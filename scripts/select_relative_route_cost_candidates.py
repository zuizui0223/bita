"""Deterministically select candidate low/high path lengths before freeze validation."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from itertools import product
from pathlib import Path

ROUTES = ("legitimate", "bypass")
MIN_BEES_PER_ROUTE = 12
MIN_ATTEMPTS_PER_DISTANCE_PER_BEE = 3
MIN_SUCCESS_RATE_SCREEN = 0.80
MIN_LOG_INCREMENT = 0.20
RATIO_LOW = 0.80
RATIO_HIGH = 1.25

REQUIRED = {
    "bee_id", "colony_id", "route", "distance_mm", "trial_id",
    "trial_order", "reward_acquired", "handling_time_s",
    "failure_code", "geometry_version",
}

def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("candidate sweep CSV is empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise ValueError(f"candidate sweep missing columns: {sorted(missing)}")
    return rows

def _bool(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"invalid boolean: {value!r}")

def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires data")
    return sum(values) / len(values)

def select_candidate_pair(rows: list[dict[str, str]]) -> dict[str, object]:
    versions = {str(row["geometry_version"]).strip() for row in rows}
    if len(versions) != 1 or "" in versions:
        raise ValueError("candidate sweep must contain one geometry_version")
    version = next(iter(versions))

    attempts: dict[tuple[str, str, float], int] = defaultdict(int)
    successes: dict[tuple[str, str, float], list[float]] = defaultdict(list)
    bees_by_route: dict[str, set[str]] = defaultdict(set)
    distances_by_route: dict[str, set[float]] = defaultdict(set)

    for row in rows:
        bee = str(row["bee_id"]).strip()
        route = str(row["route"]).strip().lower()
        if not bee or route not in ROUTES:
            raise ValueError("invalid bee_id or route")
        try:
            distance = float(str(row["distance_mm"]).strip())
        except ValueError as exc:
            raise ValueError("distance_mm must be numeric") from exc
        if not math.isfinite(distance) or distance <= 0:
            raise ValueError("distance_mm must be positive and finite")
        key = (bee, route, distance)
        attempts[key] += 1
        bees_by_route[route].add(bee)
        distances_by_route[route].add(distance)
        if _bool(row["reward_acquired"]):
            try:
                time_s = float(str(row["handling_time_s"]).strip())
            except ValueError as exc:
                raise ValueError("successful trial requires numeric handling_time_s") from exc
            if not math.isfinite(time_s) or time_s <= 0:
                raise ValueError("handling_time_s must be positive")
            successes[key].append(math.log(time_s))

    for route in ROUTES:
        if len(bees_by_route[route]) < MIN_BEES_PER_ROUTE:
            raise ValueError(f"{route} sweep requires at least {MIN_BEES_PER_ROUTE} bees")
        if len(distances_by_route[route]) < 2:
            raise ValueError(f"{route} sweep requires at least two distances")

    route_candidates: dict[str, list[dict[str, float]]] = {}
    for route in ROUTES:
        distances = sorted(distances_by_route[route])
        candidates: list[dict[str, float]] = []
        for low_i, low in enumerate(distances[:-1]):
            for high in distances[low_i + 1:]:
                eligible = []
                total_low_attempts = total_low_success = 0
                total_high_attempts = total_high_success = 0
                for bee in sorted(bees_by_route[route]):
                    low_attempts = attempts[(bee, route, low)]
                    high_attempts = attempts[(bee, route, high)]
                    total_low_attempts += low_attempts
                    total_high_attempts += high_attempts
                    total_low_success += len(successes[(bee, route, low)])
                    total_high_success += len(successes[(bee, route, high)])
                    if (
                        low_attempts >= MIN_ATTEMPTS_PER_DISTANCE_PER_BEE
                        and high_attempts >= MIN_ATTEMPTS_PER_DISTANCE_PER_BEE
                        and successes[(bee, route, low)]
                        and successes[(bee, route, high)]
                    ):
                        eligible.append(bee)
                if len(eligible) < MIN_BEES_PER_ROUTE:
                    continue
                low_rate = total_low_success / total_low_attempts if total_low_attempts else 0.0
                high_rate = total_high_success / total_high_attempts if total_high_attempts else 0.0
                if min(low_rate, high_rate) < MIN_SUCCESS_RATE_SCREEN:
                    continue
                diffs = [
                    _mean(successes[(bee, route, high)])
                    - _mean(successes[(bee, route, low)])
                    for bee in eligible
                ]
                delta = _mean(diffs)
                if delta < MIN_LOG_INCREMENT:
                    continue
                candidates.append({
                    "low_mm": low,
                    "high_mm": high,
                    "delta_log_time": delta,
                    "min_success_rate": min(low_rate, high_rate),
                    "eligible_bees": float(len(eligible)),
                })
        if not candidates:
            raise ValueError(f"no {route} low/high pair passes candidate-screen gates")
        route_candidates[route] = candidates

    joint = []
    for leg, bypass in product(route_candidates["legitimate"], route_candidates["bypass"]):
        ratio = leg["delta_log_time"] / bypass["delta_log_time"]
        if not (RATIO_LOW <= ratio <= RATIO_HIGH):
            continue
        joint.append({
            "legitimate": leg,
            "bypass": bypass,
            "ratio": ratio,
            "match_error": abs(math.log(ratio)),
            "min_success_rate": min(leg["min_success_rate"], bypass["min_success_rate"]),
            "total_high_distance_mm": leg["high_mm"] + bypass["high_mm"],
        })
    if not joint:
        raise ValueError("no cross-route candidate pair satisfies matched-increment ratio")

    joint.sort(key=lambda item: (
        item["match_error"],
        -item["min_success_rate"],
        item["total_high_distance_mm"],
        item["legitimate"]["low_mm"],
        item["legitimate"]["high_mm"],
        item["bypass"]["low_mm"],
        item["bypass"]["high_mm"],
    ))
    selected = joint[0]
    return {
        "analysis_name": "relative_route_cost_stage0a_candidate_selection",
        "geometry_version": version,
        "selection_rule": [
            "minimize absolute log matched-increment ratio",
            "maximize minimum success rate",
            "minimize total high-distance burden",
            "lexicographic distance tie-break",
        ],
        "selected": selected,
        "candidate_counts": {route: len(route_candidates[route]) for route in ROUTES},
        "next_gate": (
            "Selected distances are engineering candidates only. Re-test exactly these four "
            "states on fresh Stage-0B bees with validate_relative_route_cost_calibration.py."
        ),
    }

def run(input_csv: str | Path, output_json: str | Path) -> dict[str, object]:
    result = select_candidate_pair(_read(input_csv))
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
