"""Post-open audit of bootstrap boundary stickiness for Aubert routing threshold.

The frozen first-open result is left untouched. This audit reruns the same
plant-species bootstrap with the same seed and search bounds, then reports how
often the fitted sigmoid midpoint lands on the lower or upper search boundary.
"""
from __future__ import annotations

import argparse
import json
import sys
import math
import random
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_routing_threshold import (
    BOOTSTRAPS,
    SEED,
    _pattern_refine,
    _quantile,
    fit_sigmoid_threshold,
)
from scripts.analyze_joint_access_routing_species_robust import (
    aggregate_aubert_by_plant,
    build_public_inputs,
)


def boundary_stickiness(
    x: list[float],
    y: list[float],
    full_fit: dict[str, float | bool],
    *,
    replicates: int,
    seed: int,
) -> dict[str, object]:
    rng = random.Random(seed)
    n = len(x)
    x_low = float(full_fit["x_search_low"])
    x_high = float(full_fit["x_search_high"])
    start_x = float(full_fit["xstar"])
    start_logk = math.log(float(full_fit["k"]))
    boundary_tol = max(1e-6, (x_high - x_low) * 1e-4)

    estimates: list[float] = []
    upper = 0
    lower = 0
    interior = 0

    for _ in range(replicates):
        idx = [rng.randrange(n) for _ in range(n)]
        bx = [x[i] for i in idx]
        by = [y[i] for i in idx]
        fit = _pattern_refine(
            bx,
            by,
            start_x=start_x,
            start_logk=start_logk,
            x_low=x_low,
            x_high=x_high,
            iterations=30,
        )
        xstar = float(fit["xstar"])
        if not math.isfinite(xstar):
            continue
        estimates.append(xstar)
        if xstar >= x_high - boundary_tol:
            upper += 1
        elif xstar <= x_low + boundary_tol:
            lower += 1
        else:
            interior += 1

    finite = len(estimates)
    if finite == 0:
        raise ValueError("no finite bootstrap threshold estimates")

    return {
        "replicates_requested": replicates,
        "finite_replicates": finite,
        "finite_fraction": finite / replicates if replicates else 0.0,
        "search_low": x_low,
        "search_high": x_high,
        "boundary_tolerance": boundary_tol,
        "upper_boundary_replicates": upper,
        "upper_boundary_fraction": upper / finite,
        "lower_boundary_replicates": lower,
        "lower_boundary_fraction": lower / finite,
        "interior_replicates": interior,
        "interior_fraction": interior / finite,
        "median_xstar": _quantile(estimates, 0.50),
        "ci90_xstar": [
            _quantile(estimates, 0.05),
            _quantile(estimates, 0.95),
        ],
    }


def analyze(
    *,
    replicates: int = BOOTSTRAPS,
    seed: int = SEED,
) -> dict[str, object]:
    _sakh, aubert_rows, _audit = build_public_inputs()
    points = aggregate_aubert_by_plant(aubert_rows)
    x = [float(row["mismatch"]) for row in points]
    y = [float(row["robbery_rate"]) for row in points]
    full_fit = fit_sigmoid_threshold(x, y)
    stickiness = boundary_stickiness(
        x,
        y,
        full_fit,
        replicates=replicates,
        seed=seed,
    )

    return {
        "analysis_name": "aubert_ephi_threshold_bootstrap_boundary_audit",
        "status": "FIT",
        "analysis_timing": "POST_OPEN_DIAGNOSTIC",
        "n_plant_species": len(points),
        "seed": seed,
        "primary_xstar": float(full_fit["xstar"]),
        "primary_at_search_boundary": bool(full_fit["at_search_boundary"]),
        "bootstrap_boundary": stickiness,
        "interpretation_rule": (
            "When a large share of finite bootstrap fits land on the search boundary, "
            "report that boundary mass directly rather than interpreting the percentile "
            "interval as ordinary interior threshold uncertainty."
        ),
        "claim_boundary": (
            "This audit quantifies optimizer/search-boundary stickiness in the already "
            "opened observational threshold analysis; it does not identify an external "
            "causal threshold."
        ),
    }


def run(output: str | Path) -> dict[str, object]:
    result = analyze()
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
