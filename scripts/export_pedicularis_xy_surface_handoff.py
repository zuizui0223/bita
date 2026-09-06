"""Export one Pedicularis x-y surface into the shared Chapter-2/3 handoff.

The surface is exported regardless of whether BITA's positive differentiation gates pass.
This prevents circularly defining BALANCE only from already-positive BITA cases.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

XY_SCHEMA = "PEDICULARIS_XY_SURFACE_HANDOFF_V1"
CONFLICT_SCHEMA = "THREE_WORLD_CONFLICT_HANDOFF_V1"
BITA_WRAPPER = "BITA_PEDICULARIS_DIMENSIONAL_RELEASE_WRAPPER_V2"
EXPECTED_FITNESS_SEMANTICS = "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER"


def _finite(value: object, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _interval(value: object, name: str) -> list[float]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must be a two-element list")
    lo = _finite(value[0], f"{name}[0]")
    hi = _finite(value[1], f"{name}[1]")
    if lo > hi:
        raise ValueError(f"{name} lower bound exceeds upper bound")
    return [lo, hi]


def export_xy_handoff(result: dict, conflict_handoff: dict, config: dict) -> dict:
    if result.get("system_wrapper_schema_version") != BITA_WRAPPER:
        raise ValueError(f"BITA result must use {BITA_WRAPPER}")
    if result.get("system") != "Pedicularis rex":
        raise ValueError("BITA result must be Pedicularis rex")
    if conflict_handoff.get("receipt_schema_version") != CONFLICT_SCHEMA:
        raise ValueError(f"conflict handoff must use {CONFLICT_SCHEMA}")
    if conflict_handoff.get("status") != "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED":
        raise ValueError("conflict handoff is not positive")
    if conflict_handoff.get("system") != "Pedicularis rex":
        raise ValueError("conflict handoff must be Pedicularis rex")

    population = str(result.get("population_id", "")).strip()
    season = str(result.get("season_id", "")).strip()
    if population != conflict_handoff.get("population_id") or season != conflict_handoff.get("season_id"):
        raise ValueError("BITA x-y surface must match the SCH handoff population and season")

    expected_context = str(config.get("context_id", "")).strip()
    expected_scale = str(config.get("fitness_scale_id", "")).strip()
    if not expected_context or expected_context == "REQUIRED_BEFORE_USE":
        raise ValueError("context_id must be prospectively frozen")
    if not expected_scale or expected_scale == "REQUIRED_BEFORE_USE":
        raise ValueError("fitness_scale_id must be prospectively frozen")
    if expected_context != conflict_handoff.get("context_id"):
        raise ValueError("config context_id must exactly match SCH handoff")
    if expected_scale != conflict_handoff.get("fitness_scale_id"):
        raise ValueError("config fitness_scale_id must exactly match SCH handoff")

    mapping = result.get("pedicularis_mapping")
    if not isinstance(mapping, dict) or mapping.get("fitness_value") != EXPECTED_FITNESS_SEMANTICS:
        raise ValueError("BITA result does not use the registered common fitness outcome")
    if str(config.get("fitness_value_semantics", "")).strip() != EXPECTED_FITNESS_SEMANTICS:
        raise ValueError("config must explicitly freeze the registered common fitness semantics")

    observed = result.get("observed_estimands")
    bootstrap = result.get("bootstrap")
    if not isinstance(observed, dict) or not isinstance(bootstrap, dict):
        raise ValueError("BITA result lacks observed_estimands/bootstrap")

    y0_fit = observed.get("fitness_fit_y0")
    y1_fit = observed.get("fitness_fit_y1")
    if not isinstance(y0_fit, dict) or not isinstance(y1_fit, dict):
        raise ValueError("BITA result lacks optimized y0/y1 fitness fits")
    ws = _finite(y0_fit.get("optimum_value"), "W_S point")
    wd = _finite(y1_fit.get("optimum_value"), "W_D point")
    gap = _finite(observed.get("within_bita_optimum_fitness_gain"), "worldline gap")
    if abs((wd - ws) - gap) > 1e-8:
        raise ValueError("optimized fitness difference does not equal registered worldline gap")

    gap_ci = _interval(bootstrap.get("within_bita_optimum_fitness_gain_95_ci"), "worldline gap 95% CI")
    release = _finite(observed.get("dimensional_release"), "R_state")
    release_ci = _interval(bootstrap.get("dimensional_release_95_ci"), "R_state 95% CI")
    y1_effect = _finite(observed.get("y_effect_function1"), "y effect function1")
    y2_effect = _finite(observed.get("y_effect_function2"), "y effect function2")
    y1_ci = _interval(bootstrap.get("y_effect_function1_95_ci"), "y effect function1 95% CI")
    y2_ci = _interval(bootstrap.get("y_effect_function2_95_ci"), "y effect function2 95% CI")

    sch_ref = result.get("sch_reference")
    if not isinstance(sch_ref, dict):
        raise ValueError("BITA result lacks SCH reference")

    return {
        "receipt_schema_version": XY_SCHEMA,
        "status": "PEDICULARIS_XY_SURFACE_ANALYZED",
        "context_id": expected_context,
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "fitness_scale_id": expected_scale,
        "fitness_value_semantics": EXPECTED_FITNESS_SEMANTICS,
        "functional_state_level": True,
        "worldlines": {
            "shared_or_y_disabled": {"label": mapping.get("y0"), "optimum_fitness_point": ws},
            "y_enabled": {"label": mapping.get("y1"), "optimum_fitness_point": wd},
            "gap_y1_minus_y0": {"point": gap, "lower_95": gap_ci[0], "upper_95": gap_ci[1]},
        },
        "dimensional_release": {
            "point": release,
            "lower_95": release_ci[0],
            "upper_95": release_ci[1],
            "x_optimum_y0": _finite(observed.get("x_optimum_y0"), "x optimum y0"),
            "x_optimum_y1": _finite(observed.get("x_optimum_y1"), "x optimum y1"),
            "sch_reference_value": _finite(sch_ref.get("reference_value"), "SCH reference"),
            "sch_reference_type": sch_ref.get("reference_type"),
        },
        "functional_loading": {
            "y_effect_function1": {"point": y1_effect, "lower_95": y1_ci[0], "upper_95": y1_ci[1]},
            "y_effect_function2": {"point": y2_effect, "lower_95": y2_ci[0], "upper_95": y2_ci[1]},
        },
        "bita_surface_status": result.get("status"),
        "bita_decisions": result.get("decisions"),
        "source": {
            "repository": "bita",
            "analysis": result.get("analysis"),
            "system_wrapper_schema_version": BITA_WRAPPER,
            "sch_conflict_handoff_schema": CONFLICT_SCHEMA,
        },
        "claim_ceiling": (
            "single matched contemporary x-by-water-y functional-state surface; usable by BALANCE for direct worldline ordering "
            "and by BITA for dimensional release/loading; not structural architecture cost and not historical modularization"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bita_result_json", type=Path)
    parser.add_argument("sch_conflict_handoff_json", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.bita_result_json.read_text(encoding="utf-8"))
    handoff = json.loads(args.sch_conflict_handoff_json.read_text(encoding="utf-8"))
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    out = export_xy_handoff(result, handoff, config)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
