#!/usr/bin/env python3
"""Post-outcome sorting-only diagnostic using the fixed EPHI opportunity universe.

The companion protocol is frozen at:
empirical/route_retention_composition/ROUTE_RETENTION_COMPOSITION_DIAGNOSTIC_FREEZE_V1.md

This is NOT an individual switching or causal inference design.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_participation_route_decomposition import (
    FILES, _download, _read, build_opportunity_edges, Edge,
)
from scripts.analyze_aubert2026_route_specific_participation_postopen import split_route_counts
from scripts.analyze_aubert2026_hummingbird_reach_sensitivity import _hummingbird_species
from scripts.analyze_bypass_rescue_window import (
    REACH_MULTIPLIER, MARGIN, _shift_hummingbird_edges,
    _state, _support_gate, _fit_three_state_ipf, STATE_NAMES,
)

Z95 = 1.96


def bird_site_fe(edges: list[Edge]) -> list[Edge]:
    return [replace(e, bird=e.bird + "@@" + e.site) for e in edges]


def route_sorting_expectation(edges: list[Edge]) -> dict:
    grouped = defaultdict(lambda: [[0, 0] for _ in range(3)])
    for e in edges:
        x = grouped[(e.bird, e.site)][_state(e.mismatch)]
        x[0] += 1
        x[1] += int(e.primary_count)

    def aggregate(only_informative: bool) -> dict:
        obs = [0.0] * 3
        expected = [0.0] * 3
        ns = [0] * 3
        strata = 0
        for counts in grouped.values():
            if only_informative and (counts[0][0] <= 0 or counts[2][0] <= 0):
                continue
            N = sum(x[0] for x in counts)
            Y = sum(x[1] for x in counts)
            if N <= 0:
                continue
            strata += 1
            for g in range(3):
                ns[g] += counts[g][0]
                obs[g] += counts[g][1]
                expected[g] += Y * counts[g][0] / N
        return {
            "strata": strata,
            "state_edge_count": {STATE_NAMES[i]: ns[i] for i in range(3)},
            "observed_counts": {STATE_NAMES[i]: obs[i] for i in range(3)},
            "expected_sorting_only_counts": {STATE_NAMES[i]: expected[i] for i in range(3)},
            "observed_to_expected": {
                STATE_NAMES[i]: obs[i] / expected[i] if expected[i] > 0 else None
                for i in range(3)
            },
        }
    return {
        "total_bird_site_strata": len(grouped),
        "all_strata": aggregate(False),
        "accessible_and_severe_support_strata": aggregate(True),
        "interpretation": (
            "Expected counts condition on each bird x site total count and available "
            "opportunity-edge proportions, not on waypoint-specific floral rewards, "
            "camera sampling hours or detectability; descriptive null only."
        ),
    }


def fit_safe(edges: list[Edge]) -> dict:
    try:
        return _fit_three_state_ipf(edges)
    except (ArithmeticError, ValueError, OverflowError, ZeroDivisionError) as exc:
        return {"status": "FIT_ERROR", "detail": str(exc)}


def jackknife_site_fe(edges: list[Edge], full: dict) -> dict:
    if full.get("status") != "FIT":
        return {"status": "NOT_RUN_M2_NOT_FIT"}
    plants = sorted({e.plant for e in edges})
    values = defaultdict(list)
    failures = []
    for plant in plants:
        sample = [e for e in edges if e.plant != plant]
        f = fit_safe(sample)
        if f.get("status") != "FIT":
            failures.append({"plant": plant, "status": f.get("status")})
            continue
        for key, beta in f["log_contrasts"].items():
            values[key].append(float(beta))
    result = {}
    for key in ("moderate_vs_accessible", "severe_vs_accessible", "severe_vs_moderate"):
        arr = values[key]
        if not arr:
            result[key] = None
            continue
        mean = sum(arr) / len(arr)
        var = (len(arr)-1)/len(arr) * sum((v-mean)**2 for v in arr)
        se = math.sqrt(max(0, var))
        beta = float(full["log_contrasts"][key])
        result[key] = {
            "beta": beta,
            "rate_ratio": math.exp(beta),
            "ci95_rate_ratio": [math.exp(beta-Z95*se), math.exp(beta+Z95*se)],
            "jackknife_se_beta": se,
            "fraction_leave_one_below_one": sum(v < 0 for v in arr)/len(arr),
            "successful_leave_one": len(arr),
        }
    return {
        "status": "FIT" if len(failures) <= 0.1*len(plants) else "JACKKNIFE_UNSTABLE",
        "plant_clusters": len(plants),
        "failed_leave_one": failures,
        "contrasts": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--mode", choices=("point", "full"), default="point")
    args = parser.parse_args()

    data = {key: _read(_download(name)) for key, name in FILES.items()}
    allowed = _hummingbird_species(data["interactions"])
    base, audit = build_opportunity_edges(
        data["interactions"], data["cameras"], data["plants"], data["birds"]
    )
    rob, leg, route_audit = split_route_counts(
        data["interactions"], data["cameras"], data["plants"], data["birds"]
    )
    base = _shift_hummingbird_edges(base, allowed, REACH_MULTIPLIER)
    rob = _shift_hummingbird_edges(rob, allowed, REACH_MULTIPLIER)
    leg = _shift_hummingbird_edges(leg, allowed, REACH_MULTIPLIER)
    if not (len(base) == len(rob) == len(leg)):
        raise RuntimeError("ROUTE_EDGE_COUNTS_MISMATCH")
    if route_audit["route_specific_reconstruction_mismatches"] != 0:
        raise RuntimeError("ROUTE_COUNTS_NOT_RECONSTRUCTED")
    if any(b.primary_count != r.primary_count + l.primary_count
           for b, r, l in zip(base, rob, leg)):
        raise RuntimeError("EDGE_ROUTE_SUM_MISMATCH")
    gate = _support_gate(base)
    if not gate["passes"]:
        raise RuntimeError("OPPORTUNITY_SUPPORT_FAILED:" + json.dumps(gate))

    results = {}
    for name, edges in (("robbing", rob), ("legitimate", leg)):
        m1 = fit_safe(edges)
        m2edges = bird_site_fe(edges)
        m2 = fit_safe(m2edges)
        results[name] = {
            "sorting_only_expectation": route_sorting_expectation(edges),
            "model_bird_and_waypoint_FE": m1,
            "model_bird_site_and_waypoint_FE": m2,
            "m2_plant_cluster_jackknife": (
                jackknife_site_fe(m2edges, m2) if args.mode == "full"
                else {"status": "NOT_RUN_POINT_MODE"}
            ),
        }

    m2l = results["legitimate"]["model_bird_site_and_waypoint_FE"]
    m2r = results["robbing"]["model_bird_site_and_waypoint_FE"]
    m1r = results["robbing"]["model_bird_and_waypoint_FE"]
    if m2l.get("status") != "FIT" or m2r.get("status") != "FIT":
        decision = "M2_NOT_IDENTIFIABLE"
    else:
        severe_l = float(m2l["rate_ratio_contrasts"]["severe_vs_accessible"])
        severe_r = float(m2r["rate_ratio_contrasts"]["severe_vs_accessible"])
        if 0.8 <= severe_l <= 1.25 and 0.8 <= severe_r <= 1.25:
            decision = "SORTING_COMPATIBLE"
        else:
            decision = "CONTEXT_ASSOCIATION_ONLY"
        lj = results["legitimate"]["m2_plant_cluster_jackknife"]
        if args.mode == "full" and lj.get("status") == "FIT":
            severe_ci = lj["contrasts"]["severe_vs_accessible"]
            if (severe_ci is not None
                and severe_ci["ci95_rate_ratio"][1] < 1
                and severe_ci["fraction_leave_one_below_one"] >= 0.8
                and severe_r >= float(m1r["rate_ratio_contrasts"]["severe_vs_accessible"])):
                decision = "CONTEXT_DIFFERENTIATION_STRONG"

    out = {
        "analysis_name": "route_retention_species_sorting_vs_pair_context",
        "analysis_timing": "POST_OPEN_DIAGNOSTIC_ON_EXISTING_EPHI_DATA",
        "protocol": "empirical/route_retention_composition/ROUTE_RETENTION_COMPOSITION_DIAGNOSTIC_FREEZE_V1.md",
        "mode": args.mode,
        "population": "Trochilidae excluding Diglossa",
        "mismatch_scale": "log(tube/(1.8*culmen))",
        "category_cut": [0.0, MARGIN],
        "support_gate": gate,
        "source_route_reconstruction": route_audit["route_specific_reconstruction_mismatches"],
        "route_specific": results,
        "diagnostic_decision": decision,
        "claim_ceiling": (
            "A mismatch association remaining after bird x site and waypoint "
            "fixed effects rules out only a strict fixed bird-site baseline "
            "account. It cannot identify individual tactic switching, causal "
            "mismatch effects, fitness benefit, or community-level adaptation."
        ),
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    for route in ("robbing", "legitimate"):
        item = results[route]
        print(route, "sorting O/E", item["sorting_only_expectation"]["accessible_and_severe_support_strata"]["observed_to_expected"])
        for model in ("model_bird_and_waypoint_FE", "model_bird_site_and_waypoint_FE"):
            fit = item[model]
            print(route, model, fit.get("status"), fit.get("rate_ratio_contrasts"),
                  "pruned", (fit.get("zero_margin_waypoints_removed"), fit.get("zero_margin_birds_removed")))
        if args.mode == "full":
            print(route, "jackknife", item["m2_plant_cluster_jackknife"]["status"],
                  item["m2_plant_cluster_jackknife"].get("contrasts"))
    print("DECISION", decision)

if __name__ == "__main__":
    main()
