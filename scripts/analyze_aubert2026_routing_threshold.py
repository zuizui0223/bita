"""Frozen plant-species routing-threshold analysis for Aubert / EPHI.

The script is committed before the real threshold result is opened. It uses the same
259 plant-species aggregation as the robust cross-network routing analysis.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from scripts.analyze_joint_access_routing_species_robust import (
    aggregate_aubert_by_plant,
    build_public_inputs,
)

SEED = 20261003
BOOTSTRAPS = 999
PERMUTATIONS = 9999
K_MIN = 0.25
K_MAX = 20.0
MIN_AMPLITUDE = 0.10
PROXIMITY_MARGIN = math.log(1.25)
MIN_BOOTSTRAP_FRACTION = 0.90


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires values")
    return sum(values) / len(values)


def _quantile(values: list[float], p: float) -> float:
    if not values:
        raise ValueError("quantile requires values")
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0,1]")
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = p * (len(xs) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def _sigmoid(z: float) -> float:
    if z >= 0:
        e = math.exp(-z)
        return 1.0 / (1.0 + e)
    e = math.exp(z)
    return e / (1.0 + e)


def _sse(values: list[float], fitted: list[float]) -> float:
    return sum((y - f) ** 2 for y, f in zip(values, fitted))


def _best_bounds(q: list[float], y: list[float]) -> tuple[float, float, float]:
    # yhat = L*(1-q) + U*q, constrained to 0 <= L <= U <= 1.
    one_minus = [1.0 - v for v in q]
    s00 = sum(v * v for v in one_minus)
    s11 = sum(v * v for v in q)
    s01 = sum(a * b for a, b in zip(one_minus, q))
    t0 = sum(a * yy for a, yy in zip(one_minus, y))
    t1 = sum(b * yy for b, yy in zip(q, y))
    det = s00 * s11 - s01 * s01

    candidates: list[tuple[float, float]] = []
    if abs(det) > 1e-14:
        lower = (t0 * s11 - t1 * s01) / det
        upper = (t1 * s00 - t0 * s01) / det
        if 0.0 <= lower <= upper <= 1.0:
            candidates.append((lower, upper))

    if s11 > 0:
        upper = min(1.0, max(0.0, t1 / s11))
        candidates.append((0.0, upper))

    if s00 > 0:
        lower = min(
            1.0,
            max(
                0.0,
                sum(a * (yy - qq) for a, yy, qq in zip(one_minus, y, q)) / s00,
            ),
        )
        candidates.append((lower, 1.0))

    const = min(1.0, max(0.0, _mean(y)))
    candidates.append((const, const))
    candidates.append((0.0, 1.0))

    best = None
    for lower, upper in candidates:
        if lower > upper:
            continue
        fitted = [lower * (1.0 - qq) + upper * qq for qq in q]
        value = _sse(y, fitted)
        if best is None or value < best[0]:
            best = (value, lower, upper)
    assert best is not None
    return best


def _evaluate_sigmoid(
    x: list[float],
    y: list[float],
    xstar: float,
    logk: float,
) -> dict[str, float]:
    k = math.exp(logk)
    q = [_sigmoid(k * (xx - xstar)) for xx in x]
    sse, lower, upper = _best_bounds(q, y)
    return {
        "sse": sse,
        "lower": lower,
        "upper": upper,
        "amplitude": upper - lower,
        "xstar": xstar,
        "k": k,
        "logk": logk,
    }


def _pattern_refine(
    x: list[float],
    y: list[float],
    *,
    start_x: float,
    start_logk: float,
    x_low: float,
    x_high: float,
    iterations: int = 36,
) -> dict[str, float]:
    logk_low = math.log(K_MIN)
    logk_high = math.log(K_MAX)
    current = _evaluate_sigmoid(x, y, start_x, start_logk)
    step_x = max((x_high - x_low) / 8.0, 1e-4)
    step_k = (logk_high - logk_low) / 8.0

    for _ in range(iterations):
        candidates = [current]
        for dx in (-step_x, 0.0, step_x):
            for dk in (-step_k, 0.0, step_k):
                if dx == 0 and dk == 0:
                    continue
                xx = min(x_high, max(x_low, current["xstar"] + dx))
                lk = min(logk_high, max(logk_low, current["logk"] + dk))
                candidates.append(_evaluate_sigmoid(x, y, xx, lk))
        best = min(candidates, key=lambda item: item["sse"])
        if best["sse"] + 1e-14 < current["sse"]:
            current = best
        else:
            step_x *= 0.5
            step_k *= 0.5
        if step_x < 1e-6 and step_k < 1e-5:
            break
    return current


def fit_sigmoid_threshold(x: list[float], y: list[float]) -> dict[str, float | bool]:
    if len(x) != len(y) or len(x) < 20:
        raise ValueError("threshold fit requires >=20 paired values")
    x_low = _quantile(x, 0.05)
    x_high = _quantile(x, 0.95)
    if not x_high > x_low:
        raise ValueError("insufficient mismatch range")

    logk_low = math.log(K_MIN)
    logk_high = math.log(K_MAX)
    best = None
    nx = 61
    nk = 51
    for i in range(nx):
        xx = x_low + (x_high - x_low) * i / (nx - 1)
        for j in range(nk):
            lk = logk_low + (logk_high - logk_low) * j / (nk - 1)
            candidate = _evaluate_sigmoid(x, y, xx, lk)
            if best is None or candidate["sse"] < best["sse"]:
                best = candidate
    assert best is not None

    refined = _pattern_refine(
        x,
        y,
        start_x=float(best["xstar"]),
        start_logk=float(best["logk"]),
        x_low=x_low,
        x_high=x_high,
    )
    boundary_tol = max(1e-6, (x_high - x_low) * 1e-4)
    refined["x_search_low"] = x_low
    refined["x_search_high"] = x_high
    refined["at_search_boundary"] = (
        float(refined["xstar"]) <= x_low + boundary_tol
        or float(refined["xstar"]) >= x_high - boundary_tol
    )
    return refined


def _linear_fit(x: list[float], y: list[float]) -> dict[str, float]:
    mx = _mean(x)
    my = _mean(y)
    sxx = sum((xx - mx) ** 2 for xx in x)
    if sxx <= 0:
        raise ValueError("linear fit requires x variation")
    slope = sum((xx - mx) * (yy - my) for xx, yy in zip(x, y)) / sxx
    intercept = my - slope * mx
    fitted = [intercept + slope * xx for xx in x]
    return {"intercept": intercept, "slope": slope, "sse": _sse(y, fitted)}


def _solve3(a: list[list[float]], b: list[float]) -> list[float]:
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    n = 3
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-12:
            raise ValueError("singular quadratic design")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [value / scale for value in m[col]]
        for row in range(n):
            if row == col:
                continue
            factor = m[row][col]
            m[row] = [
                m[row][j] - factor * m[col][j]
                for j in range(n + 1)
            ]
    return [m[i][n] for i in range(n)]


def _quadratic_fit(x: list[float], y: list[float]) -> dict[str, float | None]:
    n = float(len(x))
    sx = sum(x)
    sx2 = sum(xx * xx for xx in x)
    sx3 = sum(xx**3 for xx in x)
    sx4 = sum(xx**4 for xx in x)
    sy = sum(y)
    sxy = sum(xx * yy for xx, yy in zip(x, y))
    sx2y = sum(xx * xx * yy for xx, yy in zip(x, y))
    intercept, linear, quadratic = _solve3(
        [
            [n, sx, sx2],
            [sx, sx2, sx3],
            [sx2, sx3, sx4],
        ],
        [sy, sxy, sx2y],
    )
    fitted = [
        intercept + linear * xx + quadratic * xx * xx
        for xx in x
    ]
    vertex = (
        -linear / (2.0 * quadratic)
        if quadratic < 0
        else None
    )
    return {
        "intercept": intercept,
        "linear": linear,
        "quadratic": quadratic,
        "vertex": vertex,
        "sse": _sse(y, fitted),
    }


def bootstrap_threshold(
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

    estimates: list[float] = []
    amplitudes: list[float] = []
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
        if math.isfinite(float(fit["xstar"])):
            estimates.append(float(fit["xstar"]))
            amplitudes.append(float(fit["amplitude"]))

    fraction = len(estimates) / replicates if replicates else 0.0
    if not estimates:
        return {
            "finite_replicates": 0,
            "finite_fraction": 0.0,
            "ci90_xstar": None,
            "median_xstar": None,
            "median_amplitude": None,
        }
    return {
        "finite_replicates": len(estimates),
        "finite_fraction": fraction,
        "ci90_xstar": [
            _quantile(estimates, 0.05),
            _quantile(estimates, 0.95),
        ],
        "median_xstar": _quantile(estimates, 0.50),
        "median_amplitude": _quantile(amplitudes, 0.50),
    }


def classify_threshold(
    fit: dict[str, float | bool],
    bootstrap: dict[str, object],
) -> str:
    if float(fit["amplitude"]) < MIN_AMPLITUDE:
        return "NO_MEANINGFUL_SIGMOID_TRANSITION"
    if bool(fit["at_search_boundary"]):
        return "THRESHOLD_AT_SUPPORT_BOUNDARY"
    if float(bootstrap["finite_fraction"]) < MIN_BOOTSTRAP_FRACTION:
        return "BOOTSTRAP_THRESHOLD_UNSTABLE"
    ci = bootstrap["ci90_xstar"]
    if not isinstance(ci, list):
        return "BOOTSTRAP_THRESHOLD_UNSTABLE"
    lo, hi = float(ci[0]), float(ci[1])
    if lo >= -PROXIMITY_MARGIN and hi <= PROXIMITY_MARGIN:
        return "THRESHOLD_NEAR_EQUALITY"
    if hi < -PROXIMITY_MARGIN:
        return "THRESHOLD_BELOW_EQUALITY"
    if lo > PROXIMITY_MARGIN:
        return "THRESHOLD_ABOVE_EQUALITY"
    return "THRESHOLD_LOCATION_UNRESOLVED"


def upper_turnover_diagnostic(
    x: list[float],
    y: list[float],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    linear = _linear_fit(x, y)
    quadratic = _quadratic_fit(x, y)
    improvement = float(linear["sse"]) - float(quadratic["sse"])

    rng = random.Random(seed)
    extreme = 0
    shuffled = list(y)
    for _ in range(permutations):
        rng.shuffle(shuffled)
        lp = _linear_fit(x, shuffled)
        qp = _quadratic_fit(x, shuffled)
        perm_improvement = float(lp["sse"]) - float(qp["sse"])
        if perm_improvement >= improvement - 1e-15:
            extreme += 1
    p = (extreme + 1) / (permutations + 1)

    q10 = _quantile(x, 0.10)
    q90 = _quantile(x, 0.90)
    curvature = float(quadratic["quadratic"])
    linear_term = float(quadratic["linear"])
    vertex = quadratic["vertex"]
    derivative_q90 = linear_term + 2.0 * curvature * q90

    interior = (
        vertex is not None
        and q10 <= float(vertex) <= q90
    )
    if curvature < 0 and p < 0.05 and interior and derivative_q90 < 0:
        classification = "INTERIOR_UPPER_TURNOVER_SUPPORTED"
    elif p < 0.05:
        classification = "CURVATURE_WITHOUT_INTERIOR_TURNOVER"
    else:
        classification = "NO_DETECTED_UPPER_TURNOVER"

    return {
        "classification": classification,
        "linear_sse": linear["sse"],
        "quadratic_sse": quadratic["sse"],
        "sse_improvement": improvement,
        "curvature_permutation_p": p,
        "quadratic": quadratic,
        "q10_mismatch": q10,
        "q90_mismatch": q90,
        "derivative_at_q90": derivative_q90,
        "permutations": permutations,
    }


def analyze_points(
    points: list[dict[str, float]],
    *,
    bootstraps: int = BOOTSTRAPS,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> dict[str, object]:
    if len(points) < 30:
        raise ValueError("too few plant-species points")
    x = [float(row["mismatch"]) for row in points]
    y = [float(row["robbery_rate"]) for row in points]
    if not all(math.isfinite(v) for v in x + y):
        raise ValueError("non-finite threshold inputs")

    sigmoid = fit_sigmoid_threshold(x, y)
    bootstrap = bootstrap_threshold(
        x,
        y,
        sigmoid,
        replicates=bootstraps,
        seed=seed,
    )
    threshold_class = classify_threshold(sigmoid, bootstrap)
    turnover = upper_turnover_diagnostic(
        x,
        y,
        permutations=permutations,
        seed=seed + 1,
    )

    linear = _linear_fit(x, y)
    n = len(x)
    sse_sig = max(float(sigmoid["sse"]), 1e-15)
    sse_lin = max(float(linear["sse"]), 1e-15)
    aic_sig = n * math.log(sse_sig / n) + 2 * 4
    aic_lin = n * math.log(sse_lin / n) + 2 * 2

    return {
        "analysis_name": "aubert_ephi_plant_species_routing_threshold",
        "status": "FIT",
        "n_plant_species": n,
        "primary_sigmoid": sigmoid,
        "bootstrap": bootstrap,
        "threshold_classification": threshold_class,
        "proximity_margin_abs_log_mismatch": PROXIMITY_MARGIN,
        "equivalent_tube_bill_ratio": [0.8, 1.25],
        "model_diagnostics": {
            "linear_sse": sse_lin,
            "sigmoid_sse": sse_sig,
            "working_aic_linear": aic_lin,
            "working_aic_sigmoid": aic_sig,
            "delta_aic_sigmoid_minus_linear": aic_sig - aic_lin,
            "claim_boundary": (
                "Working Gaussian AIC on species-level robbery proportions is a "
                "descriptive adequacy diagnostic, not the threshold decision rule."
            ),
        },
        "upper_turnover": turnover,
        "bootstraps": bootstraps,
        "permutations": permutations,
        "seed": seed,
        "claim_boundary": (
            "Observational shape analysis at the plant-species grain. Threshold "
            "location does not establish a causal morphology switch."
        ),
    }


def run(
    output: str | Path,
    *,
    bootstraps: int = BOOTSTRAPS,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> dict[str, object]:
    _sakh, aubert_rows, _audit = build_public_inputs()
    points = aggregate_aubert_by_plant(aubert_rows)
    result = analyze_points(
        points,
        bootstraps=bootstraps,
        permutations=permutations,
        seed=seed,
    )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--bootstraps", type=int, default=BOOTSTRAPS)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output,
                bootstraps=args.bootstraps,
                permutations=args.permutations,
                seed=args.seed,
            ),
            indent=2,
            sort_keys=True,
        )
    )
