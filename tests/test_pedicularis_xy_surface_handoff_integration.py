from __future__ import annotations

from scripts.analyze_pedicularis_dimensional_release import analyze
from scripts.export_pedicularis_xy_surface_handoff import export_xy_handoff


def _sch_receipt() -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "analysis": "sch_multilevel_causal_compromise_surface",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "system": "Pedicularis rex",
        "population_id": "POP_A",
        "season_id": "2027",
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
            "population_id": "POP_A",
            "season_id": "2027",
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
            "z_pollinator_context": 2.0,
            "z_antagonist_context": -2.0,
            "z_combined": 0.0,
        },
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(12):
        for x in (-2, -1, 0, 1, 2):
            for y in (0, 1):
                if y == 0:
                    undamaged, damaged, water, depth = 60 - x**2, 20, "DRAINED", 0
                else:
                    undamaged, damaged, water, depth = 65 - (x - 1) ** 2, 3, "PROTECTED", 10
                pollen = 100 - (x - 2) ** 2
                rows.append({
                    "population_id": "POP_A",
                    "season_id": "2027",
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P{plant:02d}_X{x:+d}_Y{y}",
                    "assigned_x_level": f"X{x:+d}",
                    "realized_exsertion": str(float(x)),
                    "water_treatment": water,
                    "ovule_count": "100",
                    "undamaged_seed_count": str(undamaged),
                    "damaged_seed_count": str(damaged),
                    "pollen_grains": str(pollen),
                    "pollinator_visits": str(10 + x),
                    "water_depth": str(depth),
                    "mechanical_damage": "0",
                })
    return rows


def _analysis_config() -> dict:
    return {"bita_release": {
        "bootstrap_reps": 200,
        "random_seed": 41,
        "min_x_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "sch_reference_mode": "state_specific",
        "min_dimensional_release": 0.5,
        "min_within_bita_fitness_gain": 3.0,
        "min_y_function2_gain": 0.1,
        "max_y_function1_penalty": 0.1,
        "min_y1_interior_bootstrap_fraction": 0.9,
        "x_to_sch_multiplier": 1.0,
        "x_to_sch_offset": 0.0,
    }}


def _conflict() -> dict:
    return {
        "receipt_schema_version": "THREE_WORLD_CONFLICT_HANDOFF_V1",
        "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
        "context_id": "PEDICULARIS_POP_A_2027",
        "system": "Pedicularis rex",
        "population_id": "POP_A",
        "season_id": "2027",
        "fitness_scale_id": "UNDAMAGED_SEEDS_PER_FOCAL_FLOWER",
        "conflict_load": {"point": 0.4, "lower_95": 0.3, "upper_95": 0.5},
    }


def test_real_pedicularis_analyzer_exports_shared_surface() -> None:
    analyzed = analyze(_rows(), _sch_receipt(), _analysis_config())
    out = export_xy_handoff(
        analyzed,
        _conflict(),
        {
            "context_id": "PEDICULARIS_POP_A_2027",
            "fitness_scale_id": "UNDAMAGED_SEEDS_PER_FOCAL_FLOWER",
            "fitness_value_semantics": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
        },
    )
    assert out["status"] == "PEDICULARIS_XY_SURFACE_ANALYZED"
    assert out["bita_surface_status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED"
    assert out["worldlines"]["gap_y1_minus_y0"]["point"] > 0
    assert out["worldlines"]["gap_y1_minus_y0"]["lower_95"] > 0
    assert out["dimensional_release"]["point"] > 0
    assert out["functional_loading"]["y_effect_function2"]["lower_95"] > 0
