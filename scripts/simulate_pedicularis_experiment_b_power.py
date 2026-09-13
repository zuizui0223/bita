from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from scripts.analyze_pedicularis_dimensional_release import analyze as analyze_pedicularis_release


REQUIRED_GENERATING_FIELDS = (
    "x_levels",
    "sch_pollinator_reference",
    "sch_combined_reference",
    "fitness_peak_y0",
    "fitness_peak_y1",
    "fitness_optimum_y0",
    "fitness_optimum_y1",
    "fitness_curvature_y0",
    "fitness_curvature_y1",
    "between_plant_sd",
    "residual_sd",
    "ovule_count",
    "damaged_seed_mean_y0",
    "damaged_seed_mean_y1",
    "damaged_seed_sd",
    "pollen_peak",
    "pollen_optimum",
    "pollen_curvature",
    "y_cross_effect_on_pollen",
    "water_depth_y1",
    "water_depth_sd",
    "mechanical_damage_rate",
)


def _require_frozen(value: object, name: str) -> object:
    if value == "REQUIRED_BEFORE_USE" or value is None:
        raise ValueError(f"{name} must be prospectively frozen before power simulation")
    return value


def _number(value: object, name: str, *, nonnegative: bool = False) -> float:
    _require_frozen(value, name)
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    if nonnegative and out < 0:
        raise ValueError(f"{name} must be non-negative")
    return out


def _prob(value: object, name: str) -> float:
    out = _number(value, name, nonnegative=True)
    if out > 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return out


def _read_config(config: dict) -> tuple[list[int], int, float, str, dict, dict]:
    if "DO_NOT_RUN" in str(config.get("status", "")):
        raise ValueError("power template must be copied and fully frozen before use")
    raw_candidates = _require_frozen(config.get("candidate_plants_per_cell"), "candidate_plants_per_cell")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise ValueError("candidate_plants_per_cell must be a non-empty list")
    candidates = sorted({int(value) for value in raw_candidates})
    if candidates[0] < 2:
        raise ValueError("candidate plants per cell must be >=2")
    reps = int(_require_frozen(config.get("simulation_reps"), "simulation_reps"))
    if reps < 1:
        raise ValueError("simulation_reps must be >=1")
    target = _number(config.get("target_joint_power"), "target_joint_power", nonnegative=True)
    if target > 1:
        raise ValueError("target_joint_power must lie in [0,1]")
    target_state = str(_require_frozen(config.get("target_worldline_state"), "target_worldline_state"))
    if target_state not in {"BALANCE", "BITA"}:
        raise ValueError("target_worldline_state must be BALANCE or BITA")

    model = config.get("generating_model")
    if not isinstance(model, dict):
        raise ValueError("generating_model must be an object")
    for field in REQUIRED_GENERATING_FIELDS:
        _require_frozen(model.get(field), f"generating_model.{field}")
    x_levels = model["x_levels"]
    if not isinstance(x_levels, list) or len(x_levels) < 5:
        raise ValueError("generating_model.x_levels must contain at least five levels")
    if len({float(value) for value in x_levels}) != len(x_levels):
        raise ValueError("x levels must be distinct")

    production = config.get("production_bita_config")
    if not isinstance(production, dict) or not isinstance(production.get("bita_release"), dict):
        raise ValueError("production_bita_config.bita_release is required")
    return candidates, reps, target, target_state, model, production


def _sch_receipt(model: dict) -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "analysis": "sch_multilevel_causal_compromise_surface",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "system": "Pedicularis rex",
        "population_id": "PEDICULARIS_POWER_SIM",
        "season_id": "SIM_SEASON",
        "pedicularis_state_mapping": {
            "P0": "SUPPLEMENTED_OPEN_POLLINATION_DEPENDENCE_NEUTRALIZED",
            "P1": "NATURAL_OPEN_POLLINATION_DEPENDENCE_ACTIVE",
            "G0": "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED",
            "G1": "SEED_PREDATOR_EXPOSED",
            "water_y": "HELD_FIXED_ACROSS_ALL_SCH_CELLS",
            "fitness_value": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
        },
        "readiness_reference": {
            "schema": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
            "status": "PEDICULARIS_FULL_SURFACE_READY",
            "population_id": "PEDICULARIS_POWER_SIM",
            "season_id": "SIM_SEASON",
            "g_schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V3",
            "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
        },
        "optimum_semantics": {
            "z_pollinator_context": "STATE_SPECIFIC_P1G0_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F1",
            "z_antagonist_context": "STATE_SPECIFIC_P0G1_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F2",
            "z_combined": "STATE_SPECIFIC_P1G1_COMBINED_REPRODUCTIVE_OPTIMUM",
            "pure_function_optima_identified_by_default": False,
        },
        "observed_estimands": {
            "z_pollinator_context": float(model["sch_pollinator_reference"]),
            "z_antagonist_context": float(model["sch_combined_reference"]) - 1.0,
            "z_combined": float(model["sch_combined_reference"]),
        },
    }


def _curve(x: float, peak: float, optimum: float, curvature: float) -> float:
    return peak - curvature * (x - optimum) ** 2


def generate_rows(model: dict, plants_per_cell: int, rng: random.Random) -> list[dict[str, str]]:
    x_levels = [float(value) for value in model["x_levels"]]
    fit_peak0 = _number(model["fitness_peak_y0"], "fitness_peak_y0")
    fit_peak1 = _number(model["fitness_peak_y1"], "fitness_peak_y1")
    fit_opt0 = _number(model["fitness_optimum_y0"], "fitness_optimum_y0")
    fit_opt1 = _number(model["fitness_optimum_y1"], "fitness_optimum_y1")
    fit_curv0 = _number(model["fitness_curvature_y0"], "fitness_curvature_y0", nonnegative=True)
    fit_curv1 = _number(model["fitness_curvature_y1"], "fitness_curvature_y1", nonnegative=True)
    plant_sd = _number(model["between_plant_sd"], "between_plant_sd", nonnegative=True)
    residual_sd = _number(model["residual_sd"], "residual_sd", nonnegative=True)
    ovules = _number(model["ovule_count"], "ovule_count", nonnegative=True)
    dmg0 = _number(model["damaged_seed_mean_y0"], "damaged_seed_mean_y0", nonnegative=True)
    dmg1 = _number(model["damaged_seed_mean_y1"], "damaged_seed_mean_y1", nonnegative=True)
    dmg_sd = _number(model["damaged_seed_sd"], "damaged_seed_sd", nonnegative=True)
    pollen_peak = _number(model["pollen_peak"], "pollen_peak")
    pollen_opt = _number(model["pollen_optimum"], "pollen_optimum")
    pollen_curv = _number(model["pollen_curvature"], "pollen_curvature", nonnegative=True)
    pollen_cross = _number(model["y_cross_effect_on_pollen"], "y_cross_effect_on_pollen")
    water_y1 = _number(model["water_depth_y1"], "water_depth_y1", nonnegative=True)
    water_sd = _number(model["water_depth_sd"], "water_depth_sd", nonnegative=True)
    damage_rate = _prob(model["mechanical_damage_rate"], "mechanical_damage_rate")
    if ovules <= 0 or fit_curv0 <= 0 or fit_curv1 <= 0 or pollen_curv <= 0:
        raise ValueError("ovule_count and all curvatures must be >0")

    rows: list[dict[str, str]] = []
    plant_effects = [rng.gauss(0.0, plant_sd) for _ in range(plants_per_cell)]
    for plant, plant_effect in enumerate(plant_effects):
        for xi, x in enumerate(x_levels):
            for y in (0, 1):
                fit_peak = fit_peak1 if y else fit_peak0
                fit_opt = fit_opt1 if y else fit_opt0
                fit_curv = fit_curv1 if y else fit_curv0
                mu = _curve(x, fit_peak, fit_opt, fit_curv) + plant_effect
                undamaged = max(0.0, min(ovules, rng.gauss(mu, residual_sd)))
                damaged_mean = dmg1 if y else dmg0
                damaged = max(0.0, rng.gauss(damaged_mean, dmg_sd))
                damaged = min(damaged, max(0.0, ovules - undamaged))
                undamaged = min(undamaged, ovules - damaged)
                pollen = max(0.0, _curve(x, pollen_peak, pollen_opt, pollen_curv) + y * pollen_cross + rng.gauss(0.0, max(1e-9, residual_sd * 0.25)))
                water_depth = max(0.0, (water_y1 if y else 0.0) + rng.gauss(0.0, water_sd))
                rows.append(
                    {
                        "population_id": "PEDICULARIS_POWER_SIM",
                        "season_id": "SIM_SEASON",
                        "plant_id": f"P{plant:04d}",
                        "flower_id": f"P{plant:04d}_X{xi}_Y{y}",
                        "assigned_x_level": f"X{xi}",
                        "realized_exsertion": f"{x:.8f}",
                        "water_treatment": "PROTECTED" if y else "DRAINED",
                        "ovule_count": f"{ovules:.8f}",
                        "undamaged_seed_count": f"{undamaged:.8f}",
                        "damaged_seed_count": f"{damaged:.8f}",
                        "pollen_grains": f"{pollen:.8f}",
                        "pollinator_visits": f"{max(0.0, 10.0 + x):.8f}",
                        "water_depth": f"{water_depth:.8f}",
                        "mechanical_damage": str(1 if rng.random() < damage_rate else 0),
                    }
                )
    return rows


def _worldline_resolved(gain_ci: list[float], target_state: str) -> bool:
    lo, hi = map(float, gain_ci)
    if target_state == "BALANCE":
        return hi < 0.0
    if target_state == "BITA":
        return lo > 0.0
    raise ValueError("unknown target state")


def simulate_power(config: dict) -> dict:
    candidates, reps, target, target_state, model, production = _read_config(config)
    master = random.Random(int(config.get("simulation_seed", 20260906)))
    results = []
    for n in candidates:
        release_success = 0
        loading_success = 0
        interior_success = 0
        worldline_success = 0
        joint_success = 0
        registered_bita_success = 0
        failures = 0
        for _ in range(reps):
            rng = random.Random(master.randrange(1, 2**31 - 1))
            rows = generate_rows(model, n, rng)
            try:
                result = analyze_pedicularis_release(rows, _sch_receipt(model), production)
                decisions = result["decisions"]
                release_ok = bool(decisions["x_optimum_released_toward_sch_reference"])
                loading_ok = bool(decisions["y_targets_function2"] and decisions["y_preserves_function1"])
                interior_ok = bool(decisions["released_surface_has_interior_optimum"])
                gain_ci = result["bootstrap"]["within_bita_optimum_fitness_gain_95_ci"]
                worldline_ok = _worldline_resolved(gain_ci, target_state)
                bita_ok = all(bool(value) for value in decisions.values())
            except (ValueError, KeyError, TypeError):
                failures += 1
                release_ok = loading_ok = interior_ok = worldline_ok = bita_ok = False
            release_success += int(release_ok)
            loading_success += int(loading_ok)
            interior_success += int(interior_ok)
            worldline_success += int(worldline_ok)
            joint_success += int(release_ok and loading_ok and interior_ok and worldline_ok)
            registered_bita_success += int(bita_ok)
        row = {
            "plants_per_cell": n,
            "simulation_reps": reps,
            "release_gate_power": release_success / reps,
            "preferential_loading_power": loading_success / reps,
            "released_surface_interior_power": interior_success / reps,
            "direct_worldline_order_power": worldline_success / reps,
            "joint_primary_gate_power": joint_success / reps,
            "registered_bita_positive_gate_power": registered_bita_success / reps,
            "analysis_failure_fraction": failures / reps,
        }
        results.append(row)

    eligible = [row["plants_per_cell"] for row in results if row["joint_primary_gate_power"] >= target]
    return {
        "analysis": "pedicularis_experiment_b_full_pipeline_power",
        "target_worldline_state": target_state,
        "design_assumption": "balanced complete-block planning model; one focal flower per x-by-y cell per independent plant cluster",
        "target_joint_power": target,
        "candidate_results": results,
        "minimum_candidate_meeting_target": min(eligible) if eligible else None,
        "claim_ceiling": (
            "planning simulation conditional on frozen pilot parameters and thresholds; BALANCE power is direct worldline-order resolution, "
            "BITA power additionally concerns release/loading; no biological result is implied"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = simulate_power(config)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
