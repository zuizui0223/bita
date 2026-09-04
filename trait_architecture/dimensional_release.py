"""Empirical SCH -> BITA dimensional-release analysis.

This module tests whether adding a second functional coordinate y moves the
optimum of the retained x coordinate toward the function-1 optimum identified
in SCH.  It deliberately separates within-BITA fitness improvement from a true
architecture-level Delta_mod comparison.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from statistics import mean


REQUIRED_FIELDS = (
    "plant_id",
    "unit_id",
    "x_level",
    "x_measured",
    "y_state",
    "function1_value",
    "function2_value",
    "fitness_value",
)


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _ystate(row: dict[str, str]) -> int:
    raw = row["y_state"].strip()
    if raw not in {"0", "1"}:
        raise ValueError(f"y_state must be 0/1, got {raw!r}")
    return int(raw)


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of empty values")
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    w = pos - lo
    return values[lo] * (1 - w) + values[hi] * w


def _solve3(matrix: list[list[float]], rhs: list[float]) -> tuple[float, float, float]:
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("quadratic fit is singular")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(3):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [a - factor * b for a, b in zip(aug[row], aug[col])]
    return aug[0][3], aug[1][3], aug[2][3]


def _fit_quadratic(points: list[tuple[float, float]]) -> dict:
    if len(points) < 3:
        raise ValueError("quadratic fit requires at least three x levels")
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    if len({round(x, 12) for x in xs}) < 3:
        raise ValueError("quadratic fit requires at least three distinct measured x values")
    n = float(len(points))
    s1 = sum(xs)
    s2 = sum(x * x for x in xs)
    s3 = sum(x**3 for x in xs)
    s4 = sum(x**4 for x in xs)
    t0 = sum(ys)
    t1 = sum(x * y for x, y in points)
    t2 = sum((x * x) * y for x, y in points)
    a, b, c = _solve3(
        [[n, s1, s2], [s1, s2, s3], [s2, s3, s4]],
        [t0, t1, t2],
    )
    zmin, zmax = min(xs), max(xs)
    discrete = points[max(range(len(points)), key=lambda i: points[i][1])][0]
    vertex = None
    if c < 0:
        candidate = -b / (2 * c)
        if zmin <= candidate <= zmax:
            vertex = candidate
    optimum = vertex if vertex is not None else discrete
    optimum_value = a + b * optimum + c * optimum * optimum
    return {
        "a": a,
        "b": b,
        "c": c,
        "x_min": zmin,
        "x_max": zmax,
        "primary_optimum": optimum,
        "optimum_value": optimum_value,
        "optimum_class": "INTERIOR_CONCAVE" if vertex is not None else "BOUNDARY_OR_NONCONCAVE",
        "points": [{"x": x, "mean_fitness": y} for x, y in points],
    }


def _cell_means(rows: list[dict[str, str]], field: str) -> dict[tuple[str, int], tuple[float, float]]:
    groups: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["x_level"], _ystate(row))].append(row)
    out = {}
    for key, group in groups.items():
        out[key] = (
            mean(_num(row, "x_measured") for row in group),
            mean(_num(row, field) for row in group),
        )
    return out


def _fitness_fit(rows: list[dict[str, str]], y_state: int, min_levels: int) -> dict:
    cells = _cell_means(rows, "fitness_value")
    points = [value for (level, y), value in cells.items() if y == y_state]
    if len(points) < min_levels:
        raise ValueError(f"y={y_state} has {len(points)} x levels; requires >= {min_levels}")
    return _fit_quadratic(sorted(points))


def _equal_level_y_effect(rows: list[dict[str, str]], field: str, min_levels: int) -> float:
    cells = _cell_means(rows, field)
    levels = sorted({level for level, _ in cells})
    diffs = []
    for level in levels:
        if (level, 0) in cells and (level, 1) in cells:
            diffs.append(cells[(level, 1)][1] - cells[(level, 0)][1])
    if len(diffs) < min_levels:
        raise ValueError(f"field {field} has only {len(diffs)} matched x levels across y states")
    return mean(diffs)


def _x_range(rows: list[dict[str, str]], field: str, y_state: int, min_levels: int) -> float:
    cells = _cell_means(rows, field)
    values = [value[1] for (level, y), value in cells.items() if y == y_state]
    if len(values) < min_levels:
        raise ValueError(f"field {field}, y={y_state} lacks enough x levels")
    return max(values) - min(values)


def _metrics(rows: list[dict[str, str]], sch_z1: float, config: dict) -> dict:
    min_levels = int(config.get("min_x_levels", 5))
    fit0 = _fitness_fit(rows, 0, min_levels)
    fit1 = _fitness_fit(rows, 1, min_levels)
    multiplier = float(config.get("x_to_sch_multiplier", 1.0))
    offset = float(config.get("x_to_sch_offset", 0.0))
    if multiplier == 0:
        raise ValueError("x_to_sch_multiplier must be non-zero")

    x0 = fit0["primary_optimum"]
    x1 = fit1["primary_optimum"]
    x0_sch = offset + multiplier * x0
    x1_sch = offset + multiplier * x1
    d0 = abs(x0_sch - sch_z1)
    d1 = abs(x1_sch - sch_z1)

    return {
        "x_optimum_y0": x0,
        "x_optimum_y1": x1,
        "x_optimum_y0_on_sch_scale": x0_sch,
        "x_optimum_y1_on_sch_scale": x1_sch,
        "distance_to_sch_z1_y0": d0,
        "distance_to_sch_z1_y1": d1,
        "dimensional_release": d0 - d1,
        "within_bita_optimum_fitness_gain": fit1["optimum_value"] - fit0["optimum_value"],
        "y_effect_function1": _equal_level_y_effect(rows, "function1_value", min_levels),
        "y_effect_function2": _equal_level_y_effect(rows, "function2_value", min_levels),
        "x_range_function1_y0": _x_range(rows, "function1_value", 0, min_levels),
        "x_range_function2_y0": _x_range(rows, "function2_value", 0, min_levels),
        "y0_interior": fit0["optimum_class"] == "INTERIOR_CONCAVE",
        "y1_interior": fit1["optimum_class"] == "INTERIOR_CONCAVE",
        "fitness_fit_y0": fit0,
        "fitness_fit_y1": fit1,
    }


def _bootstrap_rows(rows: list[dict[str, str]], rng: random.Random) -> list[dict[str, str]]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clusters[row["plant_id"]].append(row)
    ids = list(clusters)
    if len(ids) < 2:
        raise ValueError("at least two plant_id clusters are required")
    sampled = []
    for plant_id in rng.choices(ids, k=len(ids)):
        sampled.extend(clusters[plant_id])
    return sampled


def analyze_dimensional_release(rows: list[dict[str, str]], sch_receipt: dict, config: dict) -> dict:
    if sch_receipt.get("status") != "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE":
        raise ValueError("SCH receipt must contain a positive causal-compromise candidate before BITA release testing")
    try:
        sch_z1 = float(sch_receipt["observed_estimands"]["z_pollinator_context"])
        sch_zc = float(sch_receipt["observed_estimands"]["z_combined"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("SCH receipt lacks required observed z optima") from exc

    min_levels = int(config.get("min_x_levels", 5))
    if min_levels < 3:
        raise ValueError("min_x_levels must be >= 3")
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")

    observed = _metrics(rows, sch_z1, config)
    rng = random.Random(int(config.get("random_seed", 20260904)))
    boot = []
    interior_y1 = 0
    for _ in range(reps):
        sample = _bootstrap_rows(rows, rng)
        try:
            item = _metrics(sample, sch_z1, config)
        except ValueError:
            continue
        boot.append(item)
        interior_y1 += int(item["y1_interior"])

    min_valid = float(config.get("min_valid_bootstrap_fraction", 0.5))
    if len(boot) < max(50, int(reps * min_valid)):
        raise ValueError("too few valid bootstrap replicates")

    def ci(key: str) -> list[float]:
        values = [float(item[key]) for item in boot]
        return [_quantile(values, 0.025), _quantile(values, 0.975)]

    release_ci = ci("dimensional_release")
    gain_ci = ci("within_bita_optimum_fitness_gain")
    f1_ci = ci("y_effect_function1")
    f2_ci = ci("y_effect_function2")
    interior_fraction = interior_y1 / len(boot)

    min_release = float(config.get("min_dimensional_release", 0.0))
    min_gain = float(config.get("min_within_bita_fitness_gain", 0.0))
    min_target = float(config.get("min_y_function2_gain", 0.0))
    max_cross_penalty = float(config.get("max_y_function1_penalty", 0.0))
    min_interior = float(config.get("min_y1_interior_bootstrap_fraction", 0.5))

    decisions = {
        "y_targets_function2": f2_ci[0] >= min_target,
        "y_preserves_function1": f1_ci[0] >= -max_cross_penalty,
        "x_optimum_released_toward_sch_function1": release_ci[0] >= min_release,
        "within_bita_joint_fitness_improves": gain_ci[0] >= min_gain,
        "released_surface_has_interior_optimum": observed["y1_interior"] and interior_fraction >= min_interior,
    }

    return {
        "analysis": "bita_empirical_dimensional_release",
        "sch_reference": {
            "z_function1": sch_z1,
            "z_shared_combined": sch_zc,
            "receipt_status": sch_receipt["status"],
        },
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "x_levels": sorted({row["x_level"] for row in rows}),
        "observed_estimands": observed,
        "bootstrap": {
            "requested_reps": reps,
            "valid_reps": len(boot),
            "dimensional_release_95_ci": release_ci,
            "within_bita_optimum_fitness_gain_95_ci": gain_ci,
            "y_effect_function1_95_ci": f1_ci,
            "y_effect_function2_95_ci": f2_ci,
            "y1_interior_fraction": interior_fraction,
        },
        "decisions": decisions,
        "status": "FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED"
        if all(decisions.values())
        else "FUNCTIONAL_DIFFERENTIATION_OUTCOME_NOT_FULLY_RECOVERED",
        "claim_ceiling": "outcome_level_dimensional_release_only_mechanism_allocation_requires_selective_crossed_design",
        "delta_mod_status": "NOT_IDENTIFIED_UNLESS_SHARED_AND_DIFFERENTIATED_FITNESS_SCALES_ARE_EXPLICITLY_COMMENSURABLE",
    }
