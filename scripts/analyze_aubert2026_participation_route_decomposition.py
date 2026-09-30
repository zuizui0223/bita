"""Pre-registered participation-versus-routing decomposition for EPHI Ecuador.

The real-data effect analysis is fail-closed behind the denominator audit. This file
may be tested on synthetic data before the audit is accepted; no real mismatch effect
should be opened until the audit gate passes.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES,
    _as_float,
    _download,
    _read,
)
from scripts.audit_aubert2026_participation_denominator import (
    _date_in_any_interval,
    _is_target_bird,
    _parse_date,
    _primary_route_status,
)

SEED = 20260930
PERMUTATIONS = 9999
ALPHA = 0.05

KNOWN_CAMERA_OK = {"", "na", "n/a", "nan", "none", "no"}
KNOWN_CAMERA_BAD = {"yes", "maybe", "flower_problem"}


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires data")
    return sum(values) / len(values)


def _median(values: list[float]) -> float:
    if not values:
        raise ValueError("median requires data")
    values = sorted(values)
    n = len(values)
    m = n // 2
    return values[m] if n % 2 else (values[m - 1] + values[m]) / 2


def _rankdata(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    out = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[indexed[k][0]] = rank
        i = j
    return out


def _pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    mx = _mean(x)
    my = _mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    sx = math.sqrt(sum(v * v for v in dx))
    sy = math.sqrt(sum(v * v for v in dy))
    if sx == 0 or sy == 0:
        return float("nan")
    return sum(a * b for a, b in zip(dx, dy)) / (sx * sy)


def _binomial_two_sided_sign_p(positive: int, total: int) -> float | None:
    if total <= 0:
        return None
    k = min(positive, total - positive)
    tail = sum(math.comb(total, i) for i in range(k + 1)) / (2 ** total)
    return min(1.0, 2 * tail)


def _sign_flip_p(values: list[float], *, permutations: int, seed: int) -> float | None:
    if not values:
        return None
    observed = _mean(values)
    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        permuted = [v if rng.getrandbits(1) else -v for v in values]
        stat = _mean(permuted)
        if abs(stat) >= abs(observed) - 1e-15:
            extreme += 1
    return (extreme + 1) / (permutations + 1)


def _normalize_camera_problem(value: object) -> str:
    return str(value or "").strip().lower()


def _camera_row_primary_eligible(row: dict[str, str]) -> bool:
    problem = _normalize_camera_problem(row.get("camera_problem"))
    if problem in KNOWN_CAMERA_BAD:
        return False
    if problem not in KNOWN_CAMERA_OK:
        raise ValueError(f"unrecognized camera_problem state: {problem!r}")
    return True


def _strict_feeding_event(row: dict[str, str]) -> tuple[str | None, bool]:
    status = _primary_route_status(row.get("piercing"))
    if status is None:
        return None, False
    feeding = str(row.get("feeding_activity", "")).strip().lower()
    if feeding == "no_feeding":
        return status, False
    return status, True


def _build_waypoints(
    cameras: list[dict[str, str]],
    *,
    strict_camera_problem: bool = False,
) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in cameras:
        waypoint = str(row.get("waypoint", "")).strip()
        if waypoint:
            grouped[waypoint].append(row)

    out: list[dict[str, object]] = []
    for waypoint, rows in grouped.items():
        site_plant = {
            (
                str(row.get("site", "")).strip(),
                str(row.get("plant_species", "")).strip(),
            )
            for row in rows
            if str(row.get("site", "")).strip()
            and str(row.get("plant_species", "")).strip()
        }
        if len(site_plant) != 1:
            continue
        site, plant = next(iter(site_plant))
        valid = []
        for row in rows:
            start = _parse_date(row.get("start_date"))
            end = _parse_date(row.get("end_date"))
            hours = _as_float(row.get("duration_sampling_hours"))
            problem = _normalize_camera_problem(row.get("camera_problem"))
            if strict_camera_problem:
                problem_ok = problem == "no"
            else:
                problem_ok = _camera_row_primary_eligible(row)
            if (
                start is None
                or end is None
                or hours is None
                or hours <= 0
                or not problem_ok
            ):
                continue
            valid.append((start, end, hours))
        if not valid:
            continue
        out.append(
            {
                "waypoint": waypoint,
                "site": site,
                "plant": plant,
                "intervals": [(a, b) for a, b, _h in valid],
                "hours": sum(h for _a, _b, h in valid),
            }
        )
    return out


def build_opportunity_rows(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
    *,
    exclude_no_feeding: bool = True,
    strict_camera_problem: bool = False,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    plant_values: dict[tuple[str, str], list[float]] = defaultdict(list)
    plant_global: dict[str, list[float]] = defaultdict(list)
    for row in plants:
        if str(row.get("Country", "")).strip().lower() not in {"ecuador", ""}:
            continue
        plant = str(row.get("plant_species", "")).strip()
        site = str(row.get("site", "")).strip()
        tube = _as_float(row.get("Tubelength"))
        if plant and tube is not None and tube > 0:
            plant_global[plant].append(tube)
            if site:
                plant_values[(site, plant)].append(tube)

    bird_values: dict[str, list[float]] = defaultdict(list)
    for row in birds:
        species = str(row.get("hummingbird_species", "")).strip()
        culmen = _as_float(row.get("culmen_length"))
        if species and culmen is not None and culmen > 0:
            bird_values[species].append(culmen)

    target_obs: list[dict[str, object]] = []
    by_site: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_waypoint_species: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in interactions:
        if not _is_target_bird(row):
            continue
        species = str(row.get("hummingbird_species", "")).strip()
        site = str(row.get("site", "")).strip()
        waypoint = str(row.get("waypoint", "")).strip()
        d = _parse_date(row.get("date"))
        status, strict_event = _strict_feeding_event(row)
        event = status is not None and (strict_event if exclude_no_feeding else True)
        obs = {
            "species": species,
            "site": site,
            "waypoint": waypoint,
            "date": d,
            "route_status": status,
            "counted_event": event,
        }
        target_obs.append(obs)
        if site:
            by_site[site].append(obs)
        if waypoint:
            by_waypoint_species[(waypoint, species)].append(obs)

    waypoints = _build_waypoints(cameras, strict_camera_problem=strict_camera_problem)

    rows_out: list[dict[str, object]] = []
    for unit in waypoints:
        waypoint = str(unit["waypoint"])
        site = str(unit["site"])
        plant = str(unit["plant"])
        intervals = list(unit["intervals"])
        hours = float(unit["hours"])
        available = {
            str(obs["species"])
            for obs in by_site.get(site, [])
            if _date_in_any_interval(obs["date"], intervals)
        }
        tube_vals = plant_values.get((site, plant)) or plant_global.get(plant)
        if not tube_vals:
            continue
        tube_cm = _mean(tube_vals)

        for species in available:
            bill_vals = bird_values.get(species)
            if not bill_vals:
                continue
            bill_cm = _mean(bill_vals) / 10.0
            if tube_cm <= 0 or bill_cm <= 0:
                continue
            mismatch = math.log(tube_cm / bill_cm)
            rob = 0
            leg = 0
            for obs in by_waypoint_species.get((waypoint, species), []):
                if not _date_in_any_interval(obs["date"], intervals):
                    continue
                if not bool(obs["counted_event"]):
                    continue
                if obs["route_status"] == "yes":
                    rob += 1
                elif obs["route_status"] == "no":
                    leg += 1
            total = rob + leg
            rows_out.append(
                {
                    "waypoint": waypoint,
                    "site": site,
                    "bird_species": species,
                    "plant_species": plant,
                    "hours": hours,
                    "total_count": total,
                    "robbery_count": rob,
                    "legitimate_count": leg,
                    "mismatch_log_t_over_b": mismatch,
                    "trait_barrier": mismatch > 0,
                }
            )

    return rows_out, {
        "waypoints_used": len({str(r["waypoint"]) for r in rows_out}),
        "potential_waypoint_bird_rows": len(rows_out),
        "positive_waypoint_bird_rows": sum(int(r["total_count"]) > 0 for r in rows_out),
        "zero_waypoint_bird_rows": sum(int(r["total_count"]) == 0 for r in rows_out),
        "strict_camera_problem": strict_camera_problem,
        "exclude_no_feeding": exclude_no_feeding,
    }


def aggregate_site_dyads(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = (
            str(row["site"]),
            str(row["bird_species"]),
            str(row["plant_species"]),
        )
        grouped[key].append(row)

    out = []
    for (site, bird, plant), sub in grouped.items():
        hours = sum(float(r["hours"]) for r in sub)
        total = sum(int(r["total_count"]) for r in sub)
        rob = sum(int(r["robbery_count"]) for r in sub)
        leg = sum(int(r["legitimate_count"]) for r in sub)
        mismatch = _mean([float(r["mismatch_log_t_over_b"]) for r in sub])
        out.append(
            {
                "site": site,
                "bird_species": bird,
                "plant_species": plant,
                "hours": hours,
                "total_count": total,
                "robbery_count": rob,
                "legitimate_count": leg,
                "total_rate_per_hour": total / hours,
                "robbery_rate_per_hour": rob / hours,
                "legitimate_rate_per_hour": leg / hours,
                "robbery_proportion": rob / total if total > 0 else None,
                "mismatch_log_t_over_b": mismatch,
                "trait_barrier": mismatch > 0,
            }
        )
    return out


def aggregate_bird_plant_dyads(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["bird_species"]), str(row["plant_species"]))].append(row)

    out = []
    for (bird, plant), sub in grouped.items():
        hours = sum(float(r["hours"]) for r in sub)
        total = sum(int(r["total_count"]) for r in sub)
        rob = sum(int(r["robbery_count"]) for r in sub)
        leg = sum(int(r["legitimate_count"]) for r in sub)
        out.append(
            {
                "bird_species": bird,
                "plant_species": plant,
                "site_rows": len(sub),
                "hours": hours,
                "total_count": total,
                "robbery_count": rob,
                "legitimate_count": leg,
                "total_rate_per_hour": total / hours,
                "robbery_rate_per_hour": rob / hours,
                "legitimate_rate_per_hour": leg / hours,
                "robbery_proportion": rob / total if total > 0 else None,
                "mismatch_log_t_over_b": _mean(
                    [float(r["mismatch_log_t_over_b"]) for r in sub]
                ),
            }
        )
    return out


def within_bird_centered_rank_summary(
    rows: list[dict[str, object]],
    *,
    response_key: str,
    require_positive_total: bool,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    by_bird: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for row in rows:
        if require_positive_total and int(row["total_count"]) <= 0:
            continue
        response = row.get(response_key)
        if response is None:
            continue
        by_bird[str(row["bird_species"])].append(
            (float(row["mismatch_log_t_over_b"]), float(response))
        )

    groups = []
    bird_rhos: list[float] = []
    spans: list[float] = []
    for points in by_bird.values():
        if len(points) < 3:
            continue
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        spans.append(max(x) - min(x))
        if len(set(x)) < 2 or len(set(y)) < 2:
            continue
        xr = _rankdata(x)
        yr = _rankdata(y)
        xmean = _mean(xr)
        ymean = _mean(yr)
        xc = [v - xmean for v in xr]
        yc = [v - ymean for v in yr]
        rho = _pearson(xr, yr)
        if math.isfinite(rho):
            bird_rhos.append(rho)
        groups.append((xc, yc))

    pooled_x = [v for x, _y in groups for v in x]
    pooled_y = [v for _x, y in groups for v in y]
    observed = _pearson(pooled_x, pooled_y)
    if not math.isfinite(observed):
        p = None
    else:
        rng = random.Random(seed)
        extreme = 0
        for _ in range(permutations):
            perm_y = []
            for _x, y in groups:
                local = list(y)
                rng.shuffle(local)
                perm_y.extend(local)
            stat = _pearson(pooled_x, perm_y)
            if math.isfinite(stat) and abs(stat) >= abs(observed) - 1e-15:
                extreme += 1
        p = (extreme + 1) / (permutations + 1)

    nonzero = [rho for rho in bird_rhos if rho != 0]
    positive = sum(rho > 0 for rho in nonzero)
    return {
        "response": response_key,
        "bird_species_total": len(by_bird),
        "eligible_bird_species": len(groups),
        "bird_plant_dyads_in_pooled_test": len(pooled_x),
        "pooled_within_bird_rank_rho": (
            observed if math.isfinite(observed) else None
        ),
        "within_bird_permutation_p_two_sided": p,
        "bird_specific_rho_count": len(bird_rhos),
        "bird_specific_positive_rho_count": positive,
        "bird_specific_median_rho": _median(bird_rhos) if bird_rhos else None,
        "bird_specific_sign_test_p": _binomial_two_sided_sign_p(
            positive, len(nonzero)
        ),
        "median_within_bird_mismatch_span": _median(spans) if spans else None,
        "permutations": permutations,
    }


def barrier_rate_decomposition(
    site_rows: list[dict[str, object]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    by_bird: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in site_rows:
        by_bird[str(row["bird_species"])].append(row)

    total_diffs: list[float] = []
    leg_diffs: list[float] = []
    rob_diffs: list[float] = []
    for rows in by_bird.values():
        barrier = [r for r in rows if bool(r["trait_barrier"])]
        accessible = [r for r in rows if not bool(r["trait_barrier"])]
        if not barrier or not accessible:
            continue
        total_diffs.append(
            _mean([float(r["total_rate_per_hour"]) for r in barrier])
            - _mean([float(r["total_rate_per_hour"]) for r in accessible])
        )
        leg_diffs.append(
            _mean([float(r["legitimate_rate_per_hour"]) for r in barrier])
            - _mean([float(r["legitimate_rate_per_hour"]) for r in accessible])
        )
        rob_diffs.append(
            _mean([float(r["robbery_rate_per_hour"]) for r in barrier])
            - _mean([float(r["robbery_rate_per_hour"]) for r in accessible])
        )

    mean_total = _mean(total_diffs) if total_diffs else None
    mean_leg = _mean(leg_diffs) if leg_diffs else None
    mean_rob = _mean(rob_diffs) if rob_diffs else None
    compensation = None
    if (
        mean_leg is not None
        and mean_rob is not None
        and mean_leg < 0
        and mean_rob > 0
    ):
        compensation = mean_rob / abs(mean_leg)

    return {
        "eligible_bird_species": len(total_diffs),
        "mean_total_rate_difference_per_hour": mean_total,
        "median_total_rate_difference_per_hour": (
            _median(total_diffs) if total_diffs else None
        ),
        "total_rate_sign_flip_p_two_sided": _sign_flip_p(
            total_diffs, permutations=permutations, seed=seed
        ),
        "mean_legitimate_rate_difference_per_hour": mean_leg,
        "mean_robbery_rate_difference_per_hour": mean_rob,
        "descriptive_robbery_compensation_ratio": compensation,
        "claim_boundary": (
            "Legitimate and robbery rate differences are a descriptive decomposition. "
            "The compensation ratio is not causal mediation."
        ),
    }


def classify(participation: dict[str, object], routing: dict[str, object]) -> str:
    prho = participation["pooled_within_bird_rank_rho"]
    pp = participation["within_bird_permutation_p_two_sided"]
    rrho = routing["pooled_within_bird_rank_rho"]
    rp = routing["within_bird_permutation_p_two_sided"]
    part_negative = (
        prho is not None and pp is not None and float(prho) < 0 and float(pp) < ALPHA
    )
    route_positive = (
        rrho is not None and rp is not None and float(rrho) > 0 and float(rp) < ALPHA
    )
    if route_positive and not part_negative:
        return "ROUTING_WITHOUT_DETECTED_PARTICIPATION_LOSS"
    if route_positive and part_negative:
        return "SUPPRESSION_PLUS_REROUTING"
    if (not route_positive) and part_negative:
        return "FILTERING_DOMINANT"
    return "MIXED_OR_UNRESOLVED"


def analyze_tables(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
    *,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
    exclude_no_feeding: bool = True,
    strict_camera_problem: bool = False,
) -> dict[str, object]:
    opportunities, audit = build_opportunity_rows(
        interactions,
        cameras,
        plants,
        birds,
        exclude_no_feeding=exclude_no_feeding,
        strict_camera_problem=strict_camera_problem,
    )
    site_dyads = aggregate_site_dyads(opportunities)
    dyads = aggregate_bird_plant_dyads(site_dyads)

    participation = within_bird_centered_rank_summary(
        dyads,
        response_key="total_rate_per_hour",
        require_positive_total=False,
        permutations=permutations,
        seed=seed,
    )
    routing = within_bird_centered_rank_summary(
        dyads,
        response_key="robbery_proportion",
        require_positive_total=True,
        permutations=permutations,
        seed=seed + 1,
    )
    decomposition = barrier_rate_decomposition(
        site_dyads,
        permutations=permutations,
        seed=seed + 2,
    )

    return {
        "analysis_name": "aubert_ephi_participation_route_decomposition",
        "status": "OBSERVATIONAL_TWO_PART_DECOMPOSITION",
        "opportunity_audit": audit,
        "site_bird_plant_rows": len(site_dyads),
        "bird_plant_dyads": len(dyads),
        "participation": participation,
        "routing_reconstructed": routing,
        "barrier_rate_decomposition": decomposition,
        "outcome_classification": classify(participation, routing),
        "policy": {
            "exclude_no_feeding": exclude_no_feeding,
            "strict_camera_problem": strict_camera_problem,
            "effort": "positive duration_sampling_hours only; no duration_from_pics fallback",
            "camera_flowers_count": "unused; source metadata says unavailable for Ecuador",
        },
        "claim_boundary": (
            "The participation denominator uses locally available birds and camera "
            "effort to add zero opportunities. The analysis is observational; failure "
            "to detect a negative participation association is not equivalence."
        ),
        "permutations": permutations,
        "seed": seed,
    }


def _require_denominator_gate(audit: dict[str, object]) -> None:
    decision = audit.get("decision_inputs")
    if not isinstance(decision, dict):
        raise ValueError("denominator audit lacks decision_inputs")
    if decision.get("waypoint_temporal_denominator_is_possible") is not True:
        raise ValueError("waypoint temporal denominator audit did not pass")
    if not audit.get("camera_metadata_matches"):
        raise ValueError("camera metadata definitions were not captured")


def run(
    audit_json: str | Path,
    output: str | Path,
    *,
    permutations: int = PERMUTATIONS,
) -> dict[str, object]:
    audit = json.loads(Path(audit_json).read_text(encoding="utf-8"))
    _require_denominator_gate(audit)
    tables = {key: _read(_download(name)) for key, name in FILES.items()}

    primary = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        permutations=permutations,
        seed=SEED,
        exclude_no_feeding=True,
        strict_camera_problem=False,
    )
    letter_aligned = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        permutations=permutations,
        seed=SEED + 1000,
        exclude_no_feeding=False,
        strict_camera_problem=False,
    )
    strict_camera = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        permutations=permutations,
        seed=SEED + 2000,
        exclude_no_feeding=True,
        strict_camera_problem=True,
    )

    result = {
        "analysis_name": "aubert_ephi_participation_route_decomposition_bundle",
        "preregistration": (
            "empirical/floral_defence_selectivity/"
            "PARTICIPATION_ROUTE_DECOMPOSITION_PREREG_V1.md"
        ),
        "denominator_audit": str(audit_json),
        "primary": primary,
        "sensitivities": {
            "letter_aligned_feeding_policy": letter_aligned,
            "camera_problem_no_only": strict_camera,
        },
        "guardrail": (
            "First real-data effect opening must be retained regardless of sign. "
            "Do not redefine zero opportunities, effort, feeding inclusion, or outcome "
            "classification after this file is generated."
        ),
    }
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_json")
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.audit_json, args.output, permutations=args.permutations),
            indent=2,
            sort_keys=True,
        )
    )
