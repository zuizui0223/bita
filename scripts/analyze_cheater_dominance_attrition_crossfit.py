#!/usr/bin/env python3
"""Cross-fitted cheater-dominance / mutualism-attrition test.

Frozen before outcome in:
empirical/mutualism_attrition/CHEATER_DOMINANCE_ATTRITION_CROSSFIT_PREREG_V1.md

Key design:
- deterministic FNV-1a split of raw clean waypoint IDs into folds A/B;
- conditional robbery share estimated in the predictor fold;
- absolute feeding flux estimated from the disjoint outcome fold;
- plant species is the inferential unit;
- equal-fold Fisher-z statistic;
- 99,999 independent predictor-label permutations.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES,
    _as_float,
    _download,
    _read,
)
from scripts.audit_aubert2026_participation_denominator import (
    _camera_is_clean,
    _date_in_any_interval,
    _parse_date,
    _primary_route_status,
)

SEED = 20261007
PERMUTATIONS = 99_999
BOOTSTRAPS = 9_999

PRIMARY_MIN_WAYPOINTS = 2
PRIMARY_MIN_EVENTS = 5
SENS_MIN_EVENTS = 10
SENS_MIN_WAYPOINTS = 3
MIN_DIRECTION_PLANTS = 20


@dataclass(frozen=True)
class Waypoint:
    waypoint: str
    site: str
    plant: str
    intervals: tuple[tuple[date, date], ...]
    sampling_hours: float
    flower_hours: float | None
    fold: str


@dataclass
class FoldPlant:
    waypoints: set[str]
    sampling_hours: float
    flower_hours: float
    flower_hours_complete: bool
    robbery: int
    legitimate: int

    @property
    def total(self) -> int:
        return self.robbery + self.legitimate


def fnv1a32(text: str) -> int:
    h = 2166136261
    for byte in text.encode("utf-8"):
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def fold_of_waypoint(waypoint: str) -> str:
    return "A" if fnv1a32(waypoint) % 2 == 0 else "B"


def _is_target(row: dict[str, str], mode: str) -> bool:
    family = str(row.get("hummingbird_family", "")).strip()
    genus = str(row.get("hummingbird_genus", "")).strip()
    species = str(row.get("hummingbird_species", "")).strip()
    if not species:
        return False
    if mode == "all_target":
        return family == "Trochilidae" or genus == "Diglossa"
    if mode == "hummingbird_only":
        return family == "Trochilidae" and genus != "Diglossa"
    raise ValueError(mode)


def _route_status(value: object, route_policy: str) -> str | None:
    raw = str(value or "").strip().lower()
    if route_policy == "primary":
        return _primary_route_status(value)
    if route_policy == "explicit":
        return raw if raw in {"yes", "no"} else None
    raise ValueError(route_policy)


def build_waypoints(cameras: list[dict[str, str]]) -> dict[str, Waypoint]:
    by_wp: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in cameras:
        waypoint = str(row.get("waypoint", "")).strip()
        site = str(row.get("site", "")).strip()
        plant = str(row.get("plant_species", "")).strip()
        start = _parse_date(row.get("start_date"))
        end = _parse_date(row.get("end_date"))
        duration = _as_float(row.get("duration_sampling_hours"))
        flowers = _as_float(row.get("camera_flowers_count"))
        if (
            not waypoint
            or not site
            or not plant
            or start is None
            or end is None
            or duration is None
            or duration <= 0
            or not _camera_is_clean(row.get("camera_problem"))
        ):
            continue
        by_wp[waypoint].append(
            {
                "site": site,
                "plant": plant,
                "start": start,
                "end": end,
                "duration": float(duration),
                "flowers": flowers,
            }
        )

    out: dict[str, Waypoint] = {}
    for waypoint, rows in by_wp.items():
        site_plant = {(str(r["site"]), str(r["plant"])) for r in rows}
        if len(site_plant) != 1:
            continue
        site, plant = next(iter(site_plant))
        intervals = tuple(
            (r["start"], r["end"])
            for r in rows
            if isinstance(r["start"], date) and isinstance(r["end"], date)
        )
        hours = sum(float(r["duration"]) for r in rows)
        flower_values = [
            float(r["duration"]) * float(r["flowers"])
            for r in rows
            if r["flowers"] is not None and float(r["flowers"]) > 0
        ]
        complete = len(flower_values) == len(rows)
        out[waypoint] = Waypoint(
            waypoint=waypoint,
            site=site,
            plant=plant,
            intervals=intervals,
            sampling_hours=hours,
            flower_hours=sum(flower_values) if complete else None,
            fold=fold_of_waypoint(waypoint),
        )
    return out


def build_fold_plants(
    interactions: list[dict[str, str]],
    waypoints: dict[str, Waypoint],
    *,
    consumer_mode: str,
    route_policy: str,
) -> dict[tuple[str, str], FoldPlant]:
    grouped: dict[tuple[str, str], FoldPlant] = {}
    for wp in waypoints.values():
        key = (wp.plant, wp.fold)
        item = grouped.get(key)
        if item is None:
            item = FoldPlant(
                waypoints=set(),
                sampling_hours=0.0,
                flower_hours=0.0,
                flower_hours_complete=True,
                robbery=0,
                legitimate=0,
            )
            grouped[key] = item
        item.waypoints.add(wp.waypoint)
        item.sampling_hours += wp.sampling_hours
        if wp.flower_hours is None:
            item.flower_hours_complete = False
        else:
            item.flower_hours += wp.flower_hours

    for row in interactions:
        waypoint = str(row.get("waypoint", "")).strip()
        wp = waypoints.get(waypoint)
        if wp is None or not _is_target(row, consumer_mode):
            continue
        d = _parse_date(row.get("date"))
        if d is None or not _date_in_any_interval(d, list(wp.intervals)):
            continue
        if str(row.get("feeding_activity", "")).strip().lower() == "no_feeding":
            continue
        route = _route_status(row.get("piercing"), route_policy)
        if route not in {"yes", "no"}:
            continue
        item = grouped[(wp.plant, wp.fold)]
        if route == "yes":
            item.robbery += 1
        else:
            item.legitimate += 1
    return grouped


def _rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        r = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = r
        i = j
    return ranks


def _pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 3:
        return float("nan")
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    den = math.sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    if den <= 0:
        return float("nan")
    return sum(a*b for a, b in zip(dx, dy)) / den


def spearman(x: list[float], y: list[float]) -> float:
    return _pearson(_rank(x), _rank(y))


def fisher_mean(r1: float, r2: float) -> float:
    eps = 1e-12
    r1 = max(-1 + eps, min(1 - eps, r1))
    r2 = max(-1 + eps, min(1 - eps, r2))
    return math.tanh((math.atanh(r1) + math.atanh(r2)) / 2.0)


def directional_rows(
    grouped: dict[tuple[str, str], FoldPlant],
    predictor_fold: str,
    outcome_fold: str,
    *,
    min_events: int,
    min_waypoints: int,
    require_flower_hours: bool = False,
) -> list[dict[str, float | str]]:
    plants = sorted({plant for plant, _ in grouped})
    rows: list[dict[str, float | str]] = []
    for plant in plants:
        p = grouped.get((plant, predictor_fold))
        o = grouped.get((plant, outcome_fold))
        if p is None or o is None:
            continue
        if len(p.waypoints) < min_waypoints or len(o.waypoints) < min_waypoints:
            continue
        if p.total < min_events or o.sampling_hours <= 0:
            continue
        if p.total <= 0:
            continue
        if require_flower_hours and (
            not o.flower_hours_complete or o.flower_hours <= 0
        ):
            continue
        effort = o.flower_hours if require_flower_hours else o.sampling_hours
        rows.append(
            {
                "plant": plant,
                "share": p.robbery / p.total,
                "total_flux": o.total / effort,
                "legitimate_flux": o.legitimate / effort,
                "robbery_flux": o.robbery / effort,
                "predictor_events": float(p.total),
                "predictor_waypoints": float(len(p.waypoints)),
                "outcome_waypoints": float(len(o.waypoints)),
            }
        )
    return rows


def summarize_direction(rows: list[dict[str, float | str]]) -> dict[str, object]:
    x = [float(r["share"]) for r in rows]
    total = [math.log1p(float(r["total_flux"])) for r in rows]
    legit = [math.log1p(float(r["legitimate_flux"])) for r in rows]
    robbery = [math.log1p(float(r["robbery_flux"])) for r in rows]
    return {
        "n": len(rows),
        "rho_total": spearman(x, total),
        "rho_legitimate": spearman(x, legit),
        "rho_robbery": spearman(x, robbery),
    }


def _combine(d1: dict[str, object], d2: dict[str, object], key: str) -> float:
    return fisher_mean(float(d1[key]), float(d2[key]))


def permutation_test(
    rows_ab: list[dict[str, float | str]],
    rows_ba: list[dict[str, float | str]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    if len(rows_ab) < MIN_DIRECTION_PLANTS or len(rows_ba) < MIN_DIRECTION_PLANTS:
        return {"status": "INSUFFICIENT_DIRECTIONAL_PLANTS"}

    def vectors(rows):
        x = _rank([float(r["share"]) for r in rows])
        y = _rank([math.log1p(float(r["total_flux"])) for r in rows])
        return x, y

    xa, ya = vectors(rows_ab)
    xb, yb = vectors(rows_ba)
    obs_a = _pearson(xa, ya)
    obs_b = _pearson(xb, yb)
    obs = fisher_mean(obs_a, obs_b)

    rng = random.Random(seed)
    lower = 0
    two = 0
    pa = list(xa)
    pb = list(xb)
    for _ in range(permutations):
        rng.shuffle(pa)
        rng.shuffle(pb)
        stat = fisher_mean(_pearson(pa, ya), _pearson(pb, yb))
        if stat <= obs + 1e-15:
            lower += 1
        if abs(stat) >= abs(obs) - 1e-15:
            two += 1

    return {
        "status": "FIT",
        "rho_AtoB": obs_a,
        "rho_BtoA": obs_b,
        "rho_X": obs,
        "permutations": permutations,
        "p_one_sided_lower": (lower + 1) / (permutations + 1),
        "p_two_sided": (two + 1) / (permutations + 1),
    }


def bootstrap_ci(
    rows_ab: list[dict[str, float | str]],
    rows_ba: list[dict[str, float | str]],
    *,
    bootstraps: int,
    seed: int,
) -> dict[str, object]:
    map_ab = {str(r["plant"]): r for r in rows_ab}
    map_ba = {str(r["plant"]): r for r in rows_ba}
    universe = sorted(set(map_ab) | set(map_ba))
    rng = random.Random(seed)
    stats = []

    for _ in range(bootstraps):
        sample = [rng.choice(universe) for _ in universe]
        a = [map_ab[p] for p in sample if p in map_ab]
        b = [map_ba[p] for p in sample if p in map_ba]
        if len(a) < 3 or len(b) < 3:
            continue
        da = summarize_direction(a)
        db = summarize_direction(b)
        ra = float(da["rho_total"])
        rb = float(db["rho_total"])
        if math.isfinite(ra) and math.isfinite(rb):
            stats.append(fisher_mean(ra, rb))

    stats.sort()
    if not stats:
        return {"status": "NO_FINITE_BOOTSTRAPS"}
    lo_i = int(math.floor(0.025 * (len(stats) - 1)))
    hi_i = int(math.ceil(0.975 * (len(stats) - 1)))
    return {
        "status": "FIT",
        "bootstraps_requested": bootstraps,
        "finite_bootstraps": len(stats),
        "ci95": [stats[lo_i], stats[hi_i]],
    }


def evaluate_config(
    interactions: list[dict[str, str]],
    waypoints: dict[str, Waypoint],
    *,
    name: str,
    consumer_mode: str,
    route_policy: str,
    min_events: int,
    min_waypoints: int,
    permutations: int,
    seed: int,
    do_inference: bool,
    flower_hours: bool = False,
) -> dict[str, object]:
    grouped = build_fold_plants(
        interactions,
        waypoints,
        consumer_mode=consumer_mode,
        route_policy=route_policy,
    )
    ab = directional_rows(
        grouped, "A", "B",
        min_events=min_events,
        min_waypoints=min_waypoints,
        require_flower_hours=flower_hours,
    )
    ba = directional_rows(
        grouped, "B", "A",
        min_events=min_events,
        min_waypoints=min_waypoints,
        require_flower_hours=flower_hours,
    )
    d_ab = summarize_direction(ab)
    d_ba = summarize_direction(ba)
    summary = {
        "name": name,
        "consumer_mode": consumer_mode,
        "route_policy": route_policy,
        "min_events": min_events,
        "min_waypoints": min_waypoints,
        "effort": "flower_hours" if flower_hours else "camera_hours",
        "A_to_B": d_ab,
        "B_to_A": d_ba,
        "rho_X_total": (
            _combine(d_ab, d_ba, "rho_total")
            if len(ab) >= 3 and len(ba) >= 3 else None
        ),
        "rho_X_legitimate": (
            _combine(d_ab, d_ba, "rho_legitimate")
            if len(ab) >= 3 and len(ba) >= 3 else None
        ),
        "rho_X_robbery": (
            _combine(d_ab, d_ba, "rho_robbery")
            if len(ab) >= 3 and len(ba) >= 3 else None
        ),
    }
    if do_inference:
        summary["permutation"] = permutation_test(
            ab, ba, permutations=permutations, seed=seed
        )
        summary["bootstrap"] = bootstrap_ci(
            ab, ba, bootstraps=BOOTSTRAPS, seed=seed + 1
        )
    return summary


def promotion_decision(primary: dict[str, object], min10: dict[str, object]) -> dict[str, object]:
    p = primary.get("permutation", {})
    enough = (
        int(primary["A_to_B"]["n"]) >= MIN_DIRECTION_PLANTS
        and int(primary["B_to_A"]["n"]) >= MIN_DIRECTION_PLANTS
    )
    directions_negative = (
        float(primary["A_to_B"]["rho_total"]) < 0
        and float(primary["B_to_A"]["rho_total"]) < 0
    )
    total_negative = primary.get("rho_X_total") is not None and float(primary["rho_X_total"]) < 0
    legitimate_selective = (
        primary.get("rho_X_legitimate") is not None
        and primary.get("rho_X_robbery") is not None
        and float(primary["rho_X_legitimate"]) < 0
        and float(primary["rho_X_legitimate"]) < float(primary["rho_X_robbery"])
    )
    min10_negative = (
        min10.get("rho_X_total") is not None
        and float(min10["rho_X_total"]) < 0
    )
    promote = (
        enough
        and total_negative
        and directions_negative
        and legitimate_selective
        and min10_negative
    )
    return {
        "eligible_directional_n": enough,
        "primary_rho_X_negative": total_negative,
        "both_directional_total_rho_negative": directions_negative,
        "legitimate_more_negative_than_robbery": legitimate_selective,
        "min10_rho_X_negative": min10_negative,
        "promotion_gate_pass": promote,
        "permutation_p_one_sided": p.get("p_one_sided_lower"),
    }


def analyze(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    *,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> dict[str, object]:
    waypoints = build_waypoints(cameras)
    fold_counts = Counter(w.fold for w in waypoints.values())

    primary = evaluate_config(
        interactions, waypoints,
        name="primary",
        consumer_mode="all_target",
        route_policy="primary",
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
        permutations=permutations,
        seed=seed,
        do_inference=True,
    )
    min10 = evaluate_config(
        interactions, waypoints,
        name="min10_events",
        consumer_mode="all_target",
        route_policy="primary",
        min_events=SENS_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
        permutations=0,
        seed=seed + 100,
        do_inference=False,
    )
    min3wp = evaluate_config(
        interactions, waypoints,
        name="min3_waypoints",
        consumer_mode="all_target",
        route_policy="primary",
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=SENS_MIN_WAYPOINTS,
        permutations=0,
        seed=seed + 200,
        do_inference=False,
    )
    hb = evaluate_config(
        interactions, waypoints,
        name="hummingbird_only",
        consumer_mode="hummingbird_only",
        route_policy="primary",
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
        permutations=0,
        seed=seed + 300,
        do_inference=False,
    )
    explicit = evaluate_config(
        interactions, waypoints,
        name="explicit_yes_no_only",
        consumer_mode="all_target",
        route_policy="explicit",
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
        permutations=0,
        seed=seed + 400,
        do_inference=False,
    )
    flower = evaluate_config(
        interactions, waypoints,
        name="flower_hours",
        consumer_mode="all_target",
        route_policy="primary",
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
        permutations=0,
        seed=seed + 500,
        do_inference=False,
        flower_hours=True,
    )

    decision = promotion_decision(primary, min10)

    return {
        "analysis_name": "cheater_dominance_attrition_crossfit",
        "status": "FIT",
        "freeze": "empirical/mutualism_attrition/CHEATER_DOMINANCE_ATTRITION_CROSSFIT_PREREG_V1.md",
        "seed": seed,
        "permutations": permutations,
        "bootstraps": BOOTSTRAPS,
        "waypoint_split": {
            "eligible_clean_waypoints": len(waypoints),
            "fold_A": fold_counts["A"],
            "fold_B": fold_counts["B"],
            "algorithm": "FNV1a32(raw_waypoint_utf8) mod 2",
        },
        "primary": primary,
        "sensitivities": {
            "min10_events": min10,
            "min3_waypoints": min3wp,
            "hummingbird_only": hb,
            "explicit_yes_no_only": explicit,
            "flower_hours": flower,
        },
        "decision": decision,
        "claim_boundary": (
            "Cross-fitted observational association. Predictor and outcome waypoints "
            "are disjoint, removing same-sample algebraic coupling, but the result is "
            "not a causal effect of cheating on interaction flux or plant fitness."
        ),
    }


def run(output: str | Path, *, permutations: int = PERMUTATIONS) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    result = analyze(
        tables["interactions"],
        tables["cameras"],
        permutations=permutations,
    )
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--permutations", type=int, default=PERMUTATIONS)
    args = ap.parse_args()
    print(json.dumps(run(args.output, permutations=args.permutations), indent=2, sort_keys=True))
