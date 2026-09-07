from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from statistics import mean

from trait_architecture.dimensional_release import _fit_quadratic


def _grid(n_levels: int, xmin: float = -1.0, xmax: float = 1.0) -> list[float]:
    if n_levels < 3:
        raise ValueError("n_levels must be >=3")
    if n_levels == 1:
        return [(xmin + xmax) / 2]
    step = (xmax - xmin) / (n_levels - 1)
    return [xmin + i * step for i in range(n_levels)]


def _simulate_one(cfg: dict, rng: random.Random) -> dict:
    n_plants = int(cfg["n_plants"])
    n_levels = int(cfg["n_x_levels"])
    flowers_per_cell = int(cfg.get("flowers_per_plant_cell", 1))
    residual_sd = float(cfg["residual_sd"])
    plant_sd = float(cfg.get("plant_sd", 0.0))
    curvature = float(cfg.get("curvature", 1.0))
    z_ref = float(cfg.get("sch_reference", 1.0))
    x0_true = float(cfg.get("x0_true", 0.0))
    x1_true = float(cfg["x1_true"])
    y_gain = float(cfg.get("y1_peak_gain", 0.0))
    xs = _grid(n_levels, float(cfg.get("x_min", -1.0)), float(cfg.get("x_max", 1.0)))

    cell_values: dict[tuple[int, float], list[float]] = {(y, x): [] for y in (0, 1) for x in xs}
    for _plant in range(n_plants):
        plant_effect = rng.gauss(0.0, plant_sd)
        for y in (0, 1):
            optimum = x0_true if y == 0 else x1_true
            peak = 0.0 if y == 0 else y_gain
            for x in xs:
                mu = peak - curvature * (x - optimum) ** 2 + plant_effect
                for _ in range(flowers_per_cell):
                    cell_values[(y, x)].append(mu + rng.gauss(0.0, residual_sd))

    fits = {}
    for y in (0, 1):
        points = [(x, mean(cell_values[(y, x)])) for x in xs]
        fits[y] = _fit_quadratic(points)

    x0_hat = float(fits[0]["primary_optimum"])
    x1_hat = float(fits[1]["primary_optimum"])
    release = abs(x0_hat - z_ref) - abs(x1_hat - z_ref)
    true_release = abs(x0_true - z_ref) - abs(x1_true - z_ref)
    return {
        "estimated_release": release,
        "true_release": true_release,
        "x0_hat": x0_hat,
        "x1_hat": x1_hat,
        "y0_interior": fits[0]["optimum_class"] == "INTERIOR_CONCAVE",
        "y1_interior": fits[1]["optimum_class"] == "INTERIOR_CONCAVE",
    }


def evaluate_scenario(cfg: dict) -> dict:
    reps = int(cfg.get("simulation_reps", 1000))
    if reps < 100:
        raise ValueError("simulation_reps must be >=100")
    rng = random.Random(int(cfg.get("random_seed", 20260907)))
    runs = [_simulate_one(cfg, rng) for _ in range(reps)]
    true_release = float(runs[0]["true_release"])
    estimated = [float(r["estimated_release"]) for r in runs]
    same_sign = [1.0 if (r["estimated_release"] > 0) == (true_release > 0) else 0.0 for r in runs]
    both_interior = [1.0 if r["y0_interior"] and r["y1_interior"] else 0.0 for r in runs]
    within_quarter = [1.0 if abs(r["estimated_release"] - true_release) <= max(0.05, abs(true_release) * 0.25) else 0.0 for r in runs]
    return {
        "n_plants": int(cfg["n_plants"]),
        "n_x_levels": int(cfg["n_x_levels"]),
        "flowers_per_plant_cell": int(cfg.get("flowers_per_plant_cell", 1)),
        "residual_sd": float(cfg["residual_sd"]),
        "plant_sd": float(cfg.get("plant_sd", 0.0)),
        "true_release": true_release,
        "mean_estimated_release": mean(estimated),
        "sign_recovery_frequency": mean(same_sign),
        "both_optima_interior_frequency": mean(both_interior),
        "within_25pct_or_0p05_frequency": mean(within_quarter),
        "simulation_reps": reps,
    }


def run_grid(config: dict) -> dict:
    base = dict(config.get("base", {}))
    grid = config.get("grid", {})
    if not isinstance(base, dict) or not isinstance(grid, dict):
        raise ValueError("config requires base and grid objects")
    plants = list(grid.get("n_plants", []))
    levels = list(grid.get("n_x_levels", []))
    residuals = list(grid.get("residual_sd", []))
    if not plants or not levels or not residuals:
        raise ValueError("grid must provide non-empty n_plants, n_x_levels, residual_sd")
    results = []
    for n_plants in plants:
        for n_levels in levels:
            for residual_sd in residuals:
                cfg = dict(base)
                cfg.update({"n_plants": n_plants, "n_x_levels": n_levels, "residual_sd": residual_sd})
                results.append(evaluate_scenario(cfg))
    return {
        "analysis": "pedicularis_focal_design_sensitivity",
        "status": "DESIGN_SENSITIVITY_ONLY_NOT_EMPIRICAL_EVIDENCE",
        "results": results,
        "interpretation_guard": (
            "Recovery frequencies depend on declared synthetic effect sizes and noise. "
            "They may guide prospective field allocation but are not empirical evidence and cannot be reported as biological evidence, "
            "and they do not justify changing thresholds after focal outcomes are observed."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate prospective Pedicularis focal x-by-y design recovery")
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    result = run_grid(config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
