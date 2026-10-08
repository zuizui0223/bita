#!/usr/bin/env python3
"""Zero-inclusive bypass rescue-window test.

Frozen by:
empirical/bypass_rescue_window/BYPASS_RESCUE_WINDOW_PREREG_V1.md

Primary population: hummingbirds only, excluding Diglossa.
Primary mismatch: log(tube / (1.8 * culmen)).
States:
  accessible: m <= 0
  moderate:   0 < m <= log(1.25)
  severe:     m > log(1.25)

The response is fitted separately for legitimate, robbing, and pooled feeding
counts on the existing clean-waypoint x locally-available-bird opportunity
matrix with waypoint and bird fixed effects.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path

from scripts.analyze_aubert2026_participation_route_decomposition import (
    FILES,
    Edge,
    _download,
    _read,
    build_opportunity_edges,
    _prune_positive_margin_support,
)
from scripts.analyze_aubert2026_route_specific_participation_postopen import (
    split_route_counts,
)
from scripts.analyze_aubert2026_hummingbird_reach_sensitivity import (
    _hummingbird_species,
)

REACH_MULTIPLIER = 1.8
MARGIN = math.log(1.25)
Z95 = 1.96
MIN_TOTAL_EDGES = 10_000
MIN_STATE_EDGES = 200
MIN_BIRDS = 20
MIN_PLANTS = 30
MIN_FINITE_JACKKNIFE_FRACTION = 0.90

STATE_ACCESSIBLE = 0
STATE_MODERATE = 1
STATE_SEVERE = 2
STATE_NAMES = {
    STATE_ACCESSIBLE: "ACCESSIBLE",
    STATE_MODERATE: "MODERATE_MISMATCH",
    STATE_SEVERE: "SEVERE_MISMATCH",
}


@dataclass(frozen=True)
class WindowEdge:
    edge: Edge
    state: int


def _mean(xs: list[float]) -> float:
    if not xs:
        raise ValueError("mean requires values")
    return sum(xs) / len(xs)


def _state(mismatch: float) -> int:
    if mismatch <= 0.0:
        return STATE_ACCESSIBLE
    if mismatch <= MARGIN:
        return STATE_MODERATE
    return STATE_SEVERE


def _shift_hummingbird_edges(
    edges: list[Edge],
    hummingbirds: set[str],
    multiplier: float,
) -> list[Edge]:
    shift = math.log(multiplier)
    return [
        replace(
            edge,
            mismatch=edge.mismatch - shift,
            barrier=1 if edge.mismatch - shift > 0.0 else 0,
        )
        for edge in edges
        if edge.bird in hummingbirds
    ]


def _support_gate(edges: list[Edge]) -> dict[str, object]:
    states = [_state(edge.mismatch) for edge in edges]
    state_edges = {
        STATE_NAMES[k]: sum(s == k for s in states)
        for k in STATE_NAMES
    }
    checks = {
        "total_edges_ge_10000": len(edges) >= MIN_TOTAL_EDGES,
        "each_state_ge_200": all(v >= MIN_STATE_EDGES for v in state_edges.values()),
        "bird_species_ge_20": len({e.bird for e in edges}) >= MIN_BIRDS,
        "plant_species_ge_30": len({e.plant for e in edges}) >= MIN_PLANTS,
        "all_three_states_present": len(set(states)) == 3,
    }
    return {
        "passes": all(checks.values()),
        "checks": checks,
        "state_edges": state_edges,
        "total_edges": len(edges),
        "birds": len({e.bird for e in edges}),
        "plants": len({e.plant for e in edges}),
        "waypoints": len({e.waypoint for e in edges}),
    }


def _fit_three_state_ipf(
    edges: list[Edge],
    *,
    count_field: str = "primary_count",
    max_iter: int = 10000,
    tol: float = 1e-10,
) -> dict[str, object]:
    supported, pruning = _prune_positive_margin_support(edges, count_field)
    if not supported:
        return {"status": "NO_POSITIVE_MARGIN_SUPPORT", **pruning}

    rows = sorted({e.waypoint for e in supported})
    cols = sorted({e.bird for e in supported})
    rix = {x: i for i, x in enumerate(rows)}
    cix = {x: i for i, x in enumerate(cols)}

    rr = [rix[e.waypoint] for e in supported]
    cc = [cix[e.bird] for e in supported]
    kk = [_state(e.mismatch) for e in supported]
    yy = [int(getattr(e, count_field)) for e in supported]

    edge_support = [sum(k == j for k in kk) for j in range(3)]
    cat_total = [0.0, 0.0, 0.0]
    row_total = [0.0] * len(rows)
    col_total = [0.0] * len(cols)
    for ri, ci, ki, yi in zip(rr, cc, kk, yy):
        row_total[ri] += yi
        col_total[ci] += yi
        cat_total[ki] += yi

    if any(n == 0 for n in edge_support):
        return {
            "status": "STATE_WITHOUT_OPPORTUNITY_SUPPORT",
            "state_edge_support": {
                STATE_NAMES[i]: edge_support[i] for i in range(3)
            },
            **pruning,
        }

    zero_count_states = [
        STATE_NAMES[i] for i, total in enumerate(cat_total) if total <= 0
    ]
    if zero_count_states:
        return {
            "status": "RATE_SEPARATED_AT_ZERO",
            "zero_count_states": zero_count_states,
            "state_edge_support": {
                STATE_NAMES[i]: edge_support[i] for i in range(3)
            },
            "state_observed_counts": {
                STATE_NAMES[i]: cat_total[i] for i in range(3)
            },
            **pruning,
        }

    a = [1.0] * len(rows)
    b = [1.0] * len(cols)
    theta = [1.0, 1.0, 1.0]
    converged = False
    max_error = math.inf

    for iteration in range(1, max_iter + 1):
        row_den = [0.0] * len(rows)
        for ri, ci, ki in zip(rr, cc, kk):
            row_den[ri] += b[ci] * theta[ki]
        for i, den in enumerate(row_den):
            if den <= 0:
                raise ValueError("zero row denominator in three-state IPF")
            a[i] = row_total[i] / den

        col_den = [0.0] * len(cols)
        for ri, ci, ki in zip(rr, cc, kk):
            col_den[ci] += a[ri] * theta[ki]
        for i, den in enumerate(col_den):
            if den <= 0:
                raise ValueError("zero column denominator in three-state IPF")
            b[i] = col_total[i] / den

        cat_base = [0.0, 0.0, 0.0]
        for ri, ci, ki in zip(rr, cc, kk):
            cat_base[ki] += a[ri] * b[ci]
        new_theta = [
            cat_total[i] / cat_base[i]
            for i in range(3)
        ]

        # ACCESSIBLE is the reference. Rescale a to preserve every fitted mu.
        scale = new_theta[STATE_ACCESSIBLE]
        if scale <= 0:
            raise ValueError("accessible state scale collapsed")
        theta = [x / scale for x in new_theta]
        a = [x * scale for x in a]

        fit_row = [0.0] * len(rows)
        fit_col = [0.0] * len(cols)
        fit_cat = [0.0, 0.0, 0.0]
        for ri, ci, ki in zip(rr, cc, kk):
            mu = a[ri] * b[ci] * theta[ki]
            fit_row[ri] += mu
            fit_col[ci] += mu
            fit_cat[ki] += mu

        row_err = max(
            abs(fit_row[i] - row_total[i]) / max(1.0, row_total[i])
            for i in range(len(rows))
        )
        col_err = max(
            abs(fit_col[i] - col_total[i]) / max(1.0, col_total[i])
            for i in range(len(cols))
        )
        cat_err = max(
            abs(fit_cat[i] - cat_total[i]) / max(1.0, cat_total[i])
            for i in range(3)
        )
        max_error = max(row_err, col_err, cat_err)

        # Check one-cycle stability of the category factors.
        next_cat_base = [0.0, 0.0, 0.0]
        for ri, ci, ki in zip(rr, cc, kk):
            next_cat_base[ki] += a[ri] * b[ci]
        implied = [cat_total[i] / next_cat_base[i] for i in range(3)]
        implied_scale = implied[0]
        implied = [x / implied_scale for x in implied]
        delta = max(abs(math.log(implied[i] / theta[i])) for i in range(3))

        if delta < tol and max_error < 1e-8:
            converged = True
            break

    if not converged:
        raise ValueError(
            f"three-state IPF failed to converge: error={max_error}"
        )

    t0, t1, t2 = theta
    return {
        "status": "FIT",
        "iterations": iteration,
        "max_margin_relative_error": max_error,
        "supported_edges": len(supported),
        "supported_waypoints": len(rows),
        "supported_birds": len(cols),
        "state_edge_support": {
            STATE_NAMES[i]: edge_support[i] for i in range(3)
        },
        "state_observed_counts": {
            STATE_NAMES[i]: cat_total[i] for i in range(3)
        },
        "state_rate_ratio_vs_accessible": {
            "ACCESSIBLE": 1.0,
            "MODERATE_MISMATCH": t1,
            "SEVERE_MISMATCH": t2,
        },
        "log_contrasts": {
            "moderate_vs_accessible": math.log(t1 / t0),
            "severe_vs_accessible": math.log(t2 / t0),
            "severe_vs_moderate": math.log(t2 / t1),
        },
        "rate_ratio_contrasts": {
            "moderate_vs_accessible": t1 / t0,
            "severe_vs_accessible": t2 / t0,
            "severe_vs_moderate": t2 / t1,
        },
        **pruning,
    }


def _jackknife(
    edges: list[Edge],
    *,
    count_field: str = "primary_count",
) -> dict[str, object]:
    full = _fit_three_state_ipf(edges, count_field=count_field)
    if full.get("status") != "FIT":
        return {
            "status": str(full.get("status")),
            "full_fit": full,
            "jackknife": None,
        }

    plants = sorted({e.plant for e in edges})
    leave: dict[str, list[float]] = {
        "moderate_vs_accessible": [],
        "severe_vs_accessible": [],
        "severe_vs_moderate": [],
    }
    intermediate_max = 0
    failures = []

    for plant in plants:
        subset = [e for e in edges if e.plant != plant]
        fit = _fit_three_state_ipf(subset, count_field=count_field)
        if fit.get("status") != "FIT":
            failures.append({"plant": plant, "status": fit.get("status")})
            continue
        lc = fit["log_contrasts"]
        for key in leave:
            leave[key].append(float(lc[key]))

        rr = fit["state_rate_ratio_vs_accessible"]
        if (
            float(rr["MODERATE_MISMATCH"]) > 1.0
            and float(rr["MODERATE_MISMATCH"]) > float(rr["SEVERE_MISMATCH"])
        ):
            intermediate_max += 1

    finite_n = min(len(v) for v in leave.values()) if leave else 0
    finite_fraction = finite_n / len(plants) if plants else 0.0
    intervals = {}
    for key, vals in leave.items():
        if not vals:
            intervals[key] = None
            continue
        mean_leave = _mean(vals)
        n = len(vals)
        var = (n - 1) / n * sum((x - mean_leave) ** 2 for x in vals)
        se = math.sqrt(max(0.0, var))
        beta = float(full["log_contrasts"][key])
        intervals[key] = {
            "beta": beta,
            "rate_ratio": math.exp(beta),
            "jackknife_se_beta": se,
            "ci95_rate_ratio": [
                math.exp(beta - Z95 * se),
                math.exp(beta + Z95 * se),
            ],
            "finite_leave_one": n,
        }

    return {
        "status": (
            "FIT"
            if finite_fraction >= MIN_FINITE_JACKKNIFE_FRACTION
            else "JACKKNIFE_UNSTABLE"
        ),
        "full_fit": full,
        "plant_clusters": len(plants),
        "finite_leave_one_fraction": finite_fraction,
        "failed_leave_one": failures,
        "contrasts": intervals,
        "intermediate_max_leave_one_fraction": (
            intermediate_max / finite_n if finite_n else None
        ),
    }


def _ci_entirely_above_one(result: dict[str, object], key: str) -> bool:
    obj = result.get("contrasts", {}).get(key)
    return bool(obj and float(obj["ci95_rate_ratio"][0]) > 1.0)


def _ci_entirely_below_one(result: dict[str, object], key: str) -> bool:
    obj = result.get("contrasts", {}).get(key)
    return bool(obj and float(obj["ci95_rate_ratio"][1]) < 1.0)


def _point_intermediate_max(result: dict[str, object]) -> bool:
    full = result.get("full_fit", {})
    if full.get("status") != "FIT":
        return False
    rr = full["state_rate_ratio_vs_accessible"]
    return (
        float(rr["MODERATE_MISMATCH"]) > 1.0
        and float(rr["MODERATE_MISMATCH"]) > float(rr["SEVERE_MISMATCH"])
    )


def _decision(
    robbery: dict[str, object],
    legitimate: dict[str, object],
) -> dict[str, object]:
    robust_order = float(
        robbery.get("intermediate_max_leave_one_fraction") or 0.0
    ) >= 0.90
    full = (
        robbery.get("status") == "FIT"
        and legitimate.get("status") == "FIT"
        and _ci_entirely_above_one(robbery, "moderate_vs_accessible")
        and _ci_entirely_below_one(robbery, "severe_vs_moderate")
        and (
            _ci_entirely_below_one(legitimate, "moderate_vs_accessible")
            or _ci_entirely_below_one(legitimate, "severe_vs_moderate")
        )
        and robust_order
    )
    directional = _point_intermediate_max(robbery)

    if full:
        label = "FULL_BYPASS_RESCUE_WINDOW"
    elif directional:
        label = "DIRECTIONAL_WINDOW_ONLY"
    else:
        label = "NO_BYPASS_RESCUE_WINDOW"

    return {
        "classification": label,
        "promotion_eligible": full,
        "robbery_moderate_vs_accessible_ci_above_one": (
            _ci_entirely_above_one(robbery, "moderate_vs_accessible")
        ),
        "robbery_severe_vs_moderate_ci_below_one": (
            _ci_entirely_below_one(robbery, "severe_vs_moderate")
        ),
        "legitimate_any_step_ci_below_one": (
            _ci_entirely_below_one(legitimate, "moderate_vs_accessible")
            or _ci_entirely_below_one(legitimate, "severe_vs_moderate")
        ),
        "robbery_intermediate_max_leave_one_fraction": (
            robbery.get("intermediate_max_leave_one_fraction")
        ),
    }


def analyze_tables(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> dict[str, object]:
    hummingbirds = _hummingbird_species(interactions)

    pooled, base_audit = build_opportunity_edges(
        interactions, cameras, plants, birds
    )
    robbery, legitimate, route_audit = split_route_counts(
        interactions, cameras, plants, birds
    )

    pooled = _shift_hummingbird_edges(pooled, hummingbirds, REACH_MULTIPLIER)
    robbery = _shift_hummingbird_edges(robbery, hummingbirds, REACH_MULTIPLIER)
    legitimate = _shift_hummingbird_edges(legitimate, hummingbirds, REACH_MULTIPLIER)

    if not (len(pooled) == len(robbery) == len(legitimate)):
        raise ValueError("route edge sets do not align after hummingbird restriction")

    gate = _support_gate(pooled)
    if not gate["passes"]:
        return {
            "analysis": "bypass_rescue_window",
            "status": "SUPPORT_GATE_FAILED_RESULT_NOT_INTERPRETED",
            "support_gate": gate,
        }

    robbery_fit = _jackknife(robbery)
    legitimate_fit = _jackknife(legitimate)
    pooled_fit = _jackknife(pooled)
    decision = _decision(robbery_fit, legitimate_fit)

    return {
        "analysis": "bypass_rescue_window",
        "status": "FIT",
        "analysis_timing": "NEW_POST_OPEN_HYPOTHESIS_FROZEN_BEFORE_THIS_OUTCOME",
        "freeze": "empirical/bypass_rescue_window/BYPASS_RESCUE_WINDOW_PREREG_V1.md",
        "reach_multiplier": REACH_MULTIPLIER,
        "excess_margin_ratio": 1.25,
        "excess_margin_log": MARGIN,
        "hummingbird_species": len(hummingbirds),
        "support_gate": gate,
        "source_audit": {
            "base": base_audit,
            "route_split": route_audit,
        },
        "robbery": robbery_fit,
        "legitimate": legitimate_fit,
        "pooled": pooled_fit,
        "decision": decision,
        "claim_boundary": (
            "Observational zero-inclusive route-rate shape test. A supported window "
            "would establish a route-specific intermediate-mismatch pattern, not "
            "causal induction of robbery by morphology or adaptation of the bypass."
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
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    args = ap.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
