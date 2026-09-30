"""Frozen participation-versus-routing analysis for EPHI Ecuador.

Primary participation model:
    log(mu_wb) = alpha_waypoint + gamma_bird + beta * barrier_wb

The opportunity matrix contains zero-count bird x waypoint dyads only when the bird
was locally available in the same site during a clean-camera interval. Opportunity
edges outside that frozen local pool are structural zeros and are absent.

This file is committed before the real mismatch-participation effect is opened.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES,
    _as_float,
    _download,
    _read,
)
from scripts.audit_aubert2026_participation_denominator import (
    _camera_is_clean,
    _date_in_any_interval,
    _is_target_bird,
    _parse_date,
    _primary_route_status,
)

EQ_LOW = 0.80
EQ_HIGH = 1.25
Z95 = 1.96
Z90 = 1.6448536269514722
MIN_EDGES = 10_000
MIN_POSITIVE = 3_000
MIN_ZERO = 3_000
MIN_WAYPOINTS = 1_000
MIN_BIRDS = 20
MIN_PLANTS = 30

EXPLICIT_FEEDING = {"hoverflying", "perching", "perching,hoverflying"}


@dataclass(frozen=True)
class Edge:
    waypoint: str
    bird: str
    plant: str
    site: str
    barrier: int
    mismatch: float
    primary_count: int
    strict_count: int
    broad_count: int


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires values")
    return sum(values) / len(values)


def _raw_piercing(value: object) -> str:
    return str(value or "").strip().lower()


def build_opportunity_edges(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> tuple[list[Edge], dict[str, object]]:
    plant_values: dict[tuple[str, str], list[float]] = defaultdict(list)
    plant_global: dict[str, list[float]] = defaultdict(list)
    for row in plants:
        if str(row.get("Country", "")).strip().lower() not in {"ecuador", ""}:
            continue
        species = str(row.get("plant_species", "")).strip()
        site = str(row.get("site", "")).strip()
        tube = _as_float(row.get("Tubelength"))
        if species and tube is not None and tube > 0:
            plant_global[species].append(tube)
            if site:
                plant_values[(site, species)].append(tube)

    bird_values: dict[str, list[float]] = defaultdict(list)
    for row in birds:
        species = str(row.get("hummingbird_species", "")).strip()
        culmen = _as_float(row.get("culmen_length"))
        if species and culmen is not None and culmen > 0:
            bird_values[species].append(culmen)

    camera_by_waypoint: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in cameras:
        waypoint = str(row.get("waypoint", "")).strip()
        site = str(row.get("site", "")).strip()
        plant = str(row.get("plant_species", "")).strip()
        start = _parse_date(row.get("start_date"))
        end = _parse_date(row.get("end_date"))
        duration = _as_float(row.get("duration_sampling_hours"))
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
        camera_by_waypoint[waypoint].append(
            {
                "site": site,
                "plant": plant,
                "start": start,
                "end": end,
                "duration": duration,
            }
        )

    waypoint_units: dict[str, dict[str, object]] = {}
    inconsistent_waypoints = 0
    for waypoint, rows in camera_by_waypoint.items():
        site_plant = {(str(r["site"]), str(r["plant"])) for r in rows}
        if len(site_plant) != 1:
            inconsistent_waypoints += 1
            continue
        site, plant = next(iter(site_plant))
        intervals = [
            (r["start"], r["end"])
            for r in rows
            if isinstance(r["start"], date) and isinstance(r["end"], date)
        ]
        waypoint_units[waypoint] = {
            "site": site,
            "plant": plant,
            "intervals": intervals,
            "sampling_hours": sum(float(r["duration"]) for r in rows),
        }

    clean_waypoints = set(waypoint_units)

    by_site: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_waypoint_bird: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in interactions:
        waypoint = str(row.get("waypoint", "")).strip()
        if waypoint not in clean_waypoints or not _is_target_bird(row):
            continue
        d = _parse_date(row.get("date"))
        if d is None:
            continue
        unit = waypoint_units[waypoint]
        intervals = list(unit["intervals"])
        if not _date_in_any_interval(d, intervals):
            continue
        species = str(row.get("hummingbird_species", "")).strip()
        site = str(unit["site"])
        obs = {
            "waypoint": waypoint,
            "site": site,
            "species": species,
            "date": d,
            "feeding": str(row.get("feeding_activity", "")).strip().lower(),
            "piercing_raw": _raw_piercing(row.get("piercing")),
            "route_status": _primary_route_status(row.get("piercing")),
        }
        by_site[site].append(obs)
        by_waypoint_bird[(waypoint, species)].append(obs)

    edges: list[Edge] = []
    nonempty_pool_waypoints = 0
    for waypoint, unit in waypoint_units.items():
        site = str(unit["site"])
        plant = str(unit["plant"])
        intervals = list(unit["intervals"])
        local_birds = {
            str(obs["species"])
            for obs in by_site.get(site, [])
            if _date_in_any_interval(obs["date"], intervals)
        }
        if local_birds:
            nonempty_pool_waypoints += 1

        tube_vals = plant_values.get((site, plant)) or plant_global.get(plant)
        if not tube_vals:
            continue
        tube_cm = _mean(tube_vals)
        if tube_cm <= 0:
            continue

        for species in sorted(local_birds):
            bill_vals = bird_values.get(species)
            if not bill_vals:
                continue
            bill_cm = _mean(bill_vals) / 10.0
            if bill_cm <= 0:
                continue
            mismatch = math.log(tube_cm / bill_cm)
            focal = [
                obs
                for obs in by_waypoint_bird.get((waypoint, species), [])
                if _date_in_any_interval(obs["date"], intervals)
            ]

            primary = 0
            strict = 0
            broad = 0
            for obs in focal:
                feeding = str(obs["feeding"])
                raw = str(obs["piercing_raw"])
                route = obs["route_status"]

                if feeding != "no_feeding" and route in {"yes", "no"}:
                    primary += 1
                    if feeding in EXPLICIT_FEEDING:
                        strict += 1

                if feeding != "no_feeding" and raw != "not_interacting":
                    broad += 1

            edges.append(
                Edge(
                    waypoint=waypoint,
                    bird=species,
                    plant=plant,
                    site=site,
                    barrier=1 if mismatch > 0 else 0,
                    mismatch=mismatch,
                    primary_count=primary,
                    strict_count=strict,
                    broad_count=broad,
                )
            )

    audit = {
        "clean_waypoints": len(waypoint_units),
        "inconsistent_waypoints_excluded": inconsistent_waypoints,
        "waypoints_with_nonempty_local_pool": nonempty_pool_waypoints,
        "trait_matched_opportunity_edges": len(edges),
        "bird_species": len({edge.bird for edge in edges}),
        "plant_species": len({edge.plant for edge in edges}),
        "sites": len({edge.site for edge in edges}),
        "primary_positive_edges": sum(edge.primary_count > 0 for edge in edges),
        "primary_zero_edges": sum(edge.primary_count == 0 for edge in edges),
        "primary_interaction_records": sum(edge.primary_count for edge in edges),
        "strict_interaction_records": sum(edge.strict_count for edge in edges),
        "broad_interaction_records": sum(edge.broad_count for edge in edges),
        "barrier_edges": sum(edge.barrier == 1 for edge in edges),
        "accessible_edges": sum(edge.barrier == 0 for edge in edges),
    }
    return edges, audit


def _prune_positive_margin_support(
    edges: list[Edge],
    count_field: str,
) -> tuple[list[Edge], dict[str, int]]:
    current = list(edges)
    removed_waypoints: set[str] = set()
    removed_birds: set[str] = set()

    while True:
        row_totals: dict[str, int] = defaultdict(int)
        col_totals: dict[str, int] = defaultdict(int)
        for edge in current:
            y = int(getattr(edge, count_field))
            row_totals[edge.waypoint] += y
            col_totals[edge.bird] += y
        zero_rows = {key for key, value in row_totals.items() if value <= 0}
        zero_cols = {key for key, value in col_totals.items() if value <= 0}
        if not zero_rows and not zero_cols:
            break
        removed_waypoints.update(zero_rows)
        removed_birds.update(zero_cols)
        new_current = [
            edge
            for edge in current
            if edge.waypoint not in zero_rows and edge.bird not in zero_cols
        ]
        if len(new_current) == len(current):
            break
        current = new_current

    return current, {
        "zero_margin_waypoints_removed": len(removed_waypoints),
        "zero_margin_birds_removed": len(removed_birds),
    }


def fit_two_way_poisson(
    edges: list[Edge],
    *,
    count_field: str,
    max_iter: int = 5000,
    tol: float = 1e-10,
) -> dict[str, object]:
    supported, pruning = _prune_positive_margin_support(edges, count_field)
    if not supported:
        raise ValueError("no positive-margin support remains")
    if not any(edge.barrier == 1 for edge in supported):
        raise ValueError("no barrier support remains")
    if not any(edge.barrier == 0 for edge in supported):
        raise ValueError("no accessible support remains")

    rows = sorted({edge.waypoint for edge in supported})
    cols = sorted({edge.bird for edge in supported})
    row_index = {key: i for i, key in enumerate(rows)}
    col_index = {key: i for i, key in enumerate(cols)}

    r = [row_index[e.waypoint] for e in supported]
    c = [col_index[e.bird] for e in supported]
    x = [int(e.barrier) for e in supported]
    y = [int(getattr(e, count_field)) for e in supported]

    row_total = [0.0] * len(rows)
    col_total = [0.0] * len(cols)
    barrier_total = 0.0
    total_y = 0.0
    for ri, ci, xi, yi in zip(r, c, x, y):
        row_total[ri] += yi
        col_total[ci] += yi
        total_y += yi
        if xi:
            barrier_total += yi

    if barrier_total <= 0 or barrier_total >= total_y:
        raise ValueError("barrier coefficient is separated by observed counts")

    a = [1.0] * len(rows)
    b = [1.0] * len(cols)
    beta = 0.0
    converged = False
    margin_error = math.inf

    for iteration in range(1, max_iter + 1):
        exp_beta = math.exp(beta)

        row_den = [0.0] * len(rows)
        for ri, ci, xi in zip(r, c, x):
            row_den[ri] += b[ci] * (exp_beta if xi else 1.0)
        for i in range(len(rows)):
            if row_den[i] <= 0:
                raise ValueError("zero row denominator during IPF")
            a[i] = row_total[i] / row_den[i]

        col_den = [0.0] * len(cols)
        for ri, ci, xi in zip(r, c, x):
            col_den[ci] += a[ri] * (exp_beta if xi else 1.0)
        for i in range(len(cols)):
            if col_den[i] <= 0:
                raise ValueError("zero column denominator during IPF")
            b[i] = col_total[i] / col_den[i]

        positive_b = [value for value in b if value > 0]
        if not positive_b:
            raise ValueError("all bird fixed effects collapsed")
        scale = math.exp(_mean([math.log(value) for value in positive_b]))
        b = [value / scale for value in b]
        a = [value * scale for value in a]

        base_barrier = 0.0
        for ri, ci, xi in zip(r, c, x):
            if xi:
                base_barrier += a[ri] * b[ci]
        if base_barrier <= 0:
            raise ValueError("barrier base intensity is zero")
        beta_new = math.log(barrier_total / base_barrier)

        exp_new = math.exp(beta_new)
        fitted_row = [0.0] * len(rows)
        fitted_col = [0.0] * len(cols)
        for ri, ci, xi in zip(r, c, x):
            mu = a[ri] * b[ci] * (exp_new if xi else 1.0)
            fitted_row[ri] += mu
            fitted_col[ci] += mu

        row_error = max(
            abs(fitted_row[i] - row_total[i]) / max(1.0, row_total[i])
            for i in range(len(rows))
        )
        col_error = max(
            abs(fitted_col[i] - col_total[i]) / max(1.0, col_total[i])
            for i in range(len(cols))
        )
        margin_error = max(row_error, col_error)

        if abs(beta_new - beta) < tol and margin_error < 1e-8:
            beta = beta_new
            converged = True
            break
        beta = beta_new

    if not converged:
        raise ValueError(
            f"IPF did not converge; beta={beta}, margin_error={margin_error}"
        )

    return {
        "beta_log_rate_ratio": beta,
        "rate_ratio": math.exp(beta),
        "iterations": iteration,
        "max_margin_relative_error": margin_error,
        "supported_edges": len(supported),
        "supported_waypoints": len(rows),
        "supported_birds": len(cols),
        **pruning,
    }


def plant_cluster_jackknife(
    edges: list[Edge],
    *,
    count_field: str,
) -> dict[str, object]:
    supported, _ = _prune_positive_margin_support(edges, count_field)
    plants = sorted({edge.plant for edge in supported})
    if len(plants) < MIN_PLANTS:
        raise ValueError("too few plant clusters for jackknife")

    full = fit_two_way_poisson(supported, count_field=count_field)
    estimates: list[float] = []
    for plant in plants:
        subset = [edge for edge in supported if edge.plant != plant]
        estimate = fit_two_way_poisson(subset, count_field=count_field)
        estimates.append(float(estimate["beta_log_rate_ratio"]))

    mean_leave_one = _mean(estimates)
    n = len(estimates)
    variance = (n - 1) / n * sum(
        (value - mean_leave_one) ** 2
        for value in estimates
    )
    se = math.sqrt(max(0.0, variance))
    beta = float(full["beta_log_rate_ratio"])

    ci95_beta = [beta - Z95 * se, beta + Z95 * se]
    ci90_beta = [beta - Z90 * se, beta + Z90 * se]

    return {
        "fit": full,
        "plant_clusters": len(plants),
        "jackknife_se_beta": se,
        "ci95_rate_ratio": [math.exp(ci95_beta[0]), math.exp(ci95_beta[1])],
        "ci90_rate_ratio": [math.exp(ci90_beta[0]), math.exp(ci90_beta[1])],
        "leave_one_estimate_min": min(estimates),
        "leave_one_estimate_max": max(estimates),
    }


def classify_participation(primary: dict[str, object]) -> dict[str, object]:
    rr = float(primary["fit"]["rate_ratio"])
    ci95 = [float(x) for x in primary["ci95_rate_ratio"]]
    ci90 = [float(x) for x in primary["ci90_rate_ratio"]]

    equivalent = ci90[0] >= EQ_LOW and ci90[1] <= EQ_HIGH
    reduced = ci95[1] < 1.0
    increased = ci95[0] > 1.0

    if equivalent:
        classification = "ROUTING_WITHOUT_MATERIAL_PARTICIPATION_LOSS"
    elif reduced:
        classification = "PARTICIPATION_REDUCTION_PLUS_ROUTING"
    elif increased:
        classification = "PARTICIPATION_INCREASE_PLUS_ROUTING"
    else:
        classification = "PARTICIPATION_UNRESOLVED_ROUTING_ESTABLISHED"

    return {
        "classification": classification,
        "rate_ratio": rr,
        "ci95_rate_ratio": ci95,
        "ci90_rate_ratio": ci90,
        "equivalence_margin": [EQ_LOW, EQ_HIGH],
        "equivalence_supported": equivalent,
        "participation_reduction_supported": reduced,
        "participation_increase_supported": increased,
        "material_suppression_supported": ci95[1] < EQ_LOW,
        "material_enhancement_supported": ci95[0] > EQ_HIGH,
    }


def support_gate(audit: dict[str, object], edges: list[Edge]) -> dict[str, object]:
    checks = {
        "trait_matched_edges_ge_10000": len(edges) >= MIN_EDGES,
        "positive_edges_ge_3000": int(audit["primary_positive_edges"]) >= MIN_POSITIVE,
        "zero_edges_ge_3000": int(audit["primary_zero_edges"]) >= MIN_ZERO,
        "clean_waypoints_ge_1000": int(audit["clean_waypoints"]) >= MIN_WAYPOINTS,
        "bird_species_ge_20": int(audit["bird_species"]) >= MIN_BIRDS,
        "plant_species_clusters_ge_30": int(audit["plant_species"]) >= MIN_PLANTS,
        "contains_barrier_edges": int(audit["barrier_edges"]) > 0,
        "contains_accessible_edges": int(audit["accessible_edges"]) > 0,
    }
    return {"checks": checks, "passes": all(checks.values())}


def analyze_tables(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> dict[str, object]:
    edges, audit = build_opportunity_edges(interactions, cameras, plants, birds)
    gate = support_gate(audit, edges)
    if not gate["passes"]:
        return {
            "analysis_name": "aubert_ephi_participation_route_decomposition",
            "status": "RESULT_NOT_OPENED_SUPPORT_GATE_FAILED",
            "audit": audit,
            "support_gate": gate,
            "participation_effect": None,
        }

    primary = plant_cluster_jackknife(edges, count_field="primary_count")
    strict = fit_two_way_poisson(edges, count_field="strict_count")
    broad = fit_two_way_poisson(edges, count_field="broad_count")
    decision = classify_participation(primary)

    return {
        "analysis_name": "aubert_ephi_participation_route_decomposition",
        "status": "FIT",
        "audit": audit,
        "support_gate": gate,
        "primary_participation": primary,
        "decision": decision,
        "sensitivities": {
            "strict_feeding_rate_ratio": strict["rate_ratio"],
            "broad_feeding_rate_ratio": broad["rate_ratio"],
        },
        "model": {
            "formula": (
                "log(mu_waypoint,bird) = alpha_waypoint + gamma_bird "
                "+ beta * I[tube > culmen]"
            ),
            "estimand": (
                "exp(beta) barrier/access total route-resolved exploitation rate ratio"
            ),
            "uncertainty": "delete-one-plant-species jackknife",
        },
        "claim_boundary": (
            "Observational participation analysis. Waypoint and bird fixed effects "
            "control their main effects, but the result does not establish that floral "
            "geometry causally changed visitation or evolved as defence."
        ),
    }


def run(output: str | Path) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    result = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
    )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
