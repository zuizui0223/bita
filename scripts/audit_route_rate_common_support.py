#!/usr/bin/env python3
"""Post-outcome risk-set audit for separate route-specific Poisson effects.

Critically, route-specific positive-margin pruning conditions on each response.
A shared-support re-fit therefore also conditions on outcomes and is a
descriptive sensitivity, not a remedy that recovers the original population
estimand. Do NOT use its jackknife as confirmatory evidence.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from scripts.diagnose_route_retention_poisson_mle_existence import (
    _read_frozen_archive,
)
from scripts.analyze_route_retention_extended_mle import (
    fit_extended,
)


def prune_route(cells, route):
    """Repeatedly delete zero-count waypoint and bird x site margins."""
    current = list(cells)
    while True:
        rows, cols = Counter(), Counter()
        for cell in current:
            count = int(getattr(cell, route))
            rows[cell.waypoint] += count
            cols[(cell.bird, cell.site)] += count
        kept = [
            cell for cell in current
            if rows[cell.waypoint] > 0 and cols[(cell.bird, cell.site)] > 0
        ]
        if len(kept) == len(current):
            return current
        current = kept


def prune_joint(cells):
    """Fixed point of the intersection of BOTH route-specific margins."""
    current = list(cells)
    for k in range(50):
        rob, legit = Counter(), Counter()
        rcol, lcol = Counter(), Counter()
        for c in current:
            rob[c.waypoint] += c.robbery
            legit[c.waypoint] += c.legitimate
            rcol[(c.bird, c.site)] += c.robbery
            lcol[(c.bird, c.site)] += c.legitimate
        kept = [
            c for c in current
            if min(rob[c.waypoint], legit[c.waypoint],
                   rcol[(c.bird, c.site)], lcol[(c.bird, c.site)]) > 0
        ]
        if len(kept) == len(current):
            return current, k + 1
        current = kept
    raise RuntimeError("JOINT_MARGIN_PRUNING_NOT_STABLE")


def fit_route(cells, route):
    tuples = [
        (c.waypoint, c.bird + "@@" + c.site, c.category,
         int(getattr(c, route)), c.plant)
        for c in cells
    ]
    return fit_extended(tuples)


def category_counts(cells):
    return {str(i): sum(c.category == i for c in cells) for i in range(3)}


def run(source, output, *, jackknife=True):
    cells, audit = _read_frozen_archive(source)
    r = prune_route(cells, "robbery")
    l = prune_route(cells, "legitimate")
    rid, lid = set(map(id, r)), set(map(id, l))
    intersection = rid & lid
    common, iterations = prune_joint(cells)
    plants = sorted({c.plant for c in common})
    if len(cells) != 19903 or len(r) != 2563 or len(l) != 15352:
        raise RuntimeError("ORIGINAL_ROUTE_SPECIFIC_SUPPORT_DRIFT")
    if len(intersection) != 2195 or len(common) != 1986 or len(plants) != 126:
        raise RuntimeError("COMMON_POSITIVE_MARGIN_SUPPORT_DRIFT")

    rb = fit_route(common, "robbery")
    lg = fit_route(common, "legitimate")
    if rb["status"] != "FIT" or lg["status"] != "FIT":
        raise RuntimeError("SHARED_SUPPORT_RATE_FIT_FAILED")

    labels = ("moderate_accessible", "severe_accessible", "severe_moderate")
    relative = {
        label: rb["rate_ratios"][label] / lg["rate_ratios"][label]
        for label in labels
    }
    receipt = {
        "analysis": "POST_OUTCOME_ROUTE_SPECIFIC_POSITIVE_MARGIN_SUPPORT_AUDIT",
        "source": audit,
        "route_support": {
            "total_eligible_opportunities": len(cells),
            "robbery_positive_margin_support": len(r),
            "legitimate_positive_margin_support": len(l),
            "initial_intersection": len(intersection),
            "robbery_only": len(rid - lid),
            "legitimate_only": len(lid - rid),
            "neither": len(cells) - len(rid | lid),
            "initial_intersection_fraction": len(intersection) / len(cells),
            "joint_iteratively_pruned_cells": len(common),
            "joint_pruning_iterations": iterations,
            "joint_support_plants": len(plants),
            "joint_support_categories": category_counts(common),
        },
        "common_positive_margin_sensitivity": {
            "method": "outcome-dependent joint positive-margin subset; full maximal face recomputed per route",
            "robbery_fit": rb,
            "legitimate_fit": lg,
            "cross_route_rr_ratio_on_joint_margin_support": relative,
        },
        "claim_boundary": (
            "Route-specific positive-margin pruning changes which opportunities "
            "inform each Poisson fixed-effect estimator. Dividing their RRs is "
            "not a single-population relative-rate estimand. A common-support "
            "sensitivity conditions on post-outcome route counts and cannot "
            "restore the original zero-inclusive population estimand; do not "
            "promote to confirmatory effect, causal switch or equivalent denominators."
        ),
    }
    if jackknife:
        refits = []
        for p in plants:
            subset, _ = prune_joint([c for c in cells if c.plant != p])
            rr = fit_route(subset, "robbery")
            ll = fit_route(subset, "legitimate")
            if rr["status"] != "FIT" or ll["status"] != "FIT":
                raise RuntimeError("PLANT_JACKKNIFE_FIT_FAILED:" + p)
            refits.append({
                "plant": p, "shared_opportunities": len(subset),
                "ratio_log": {
                    label: math.log(rr["rate_ratios"][label]) -
                           math.log(ll["rate_ratios"][label])
                    for label in labels
                }
            })
        if len(refits) != len(plants):
            raise RuntimeError("JACKKNIFE_PLANT_COUNT_DRIFT")
        summary = {}
        for label in labels:
            leave = np.array([row["ratio_log"][label] for row in refits])
            point = math.log(relative[label])
            n = len(leave)
            se = math.sqrt(float((n-1)/n * np.sum((leave - leave.mean())**2)))
            summary[label] = {
                "relative_rate_ratio": math.exp(point),
                "plant_jackknife_95_working_interval": [
                    math.exp(point-1.96*se), math.exp(point+1.96*se)
                ],
                "successful_plant_refits": n,
                "leave_one_min_ratio": math.exp(float(leave.min())),
                "leave_one_max_ratio": math.exp(float(leave.max())),
            }
        receipt["common_positive_margin_sensitivity"]["paired_plant_jackknife"] = summary
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(json.dumps({
        "support": receipt["route_support"],
        "robbery_rr": rb["rate_ratios"],
        "legitimate_rr": lg["rate_ratios"],
        "relative": relative,
        "jackknife": receipt["common_positive_margin_sensitivity"].get("paired_plant_jackknife"),
    }, indent=2))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--no-jackknife", action="store_true")
    args = parser.parse_args()
    run(args.source_zip, args.output_json, jackknife=not args.no_jackknife)
