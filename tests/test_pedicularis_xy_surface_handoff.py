from __future__ import annotations

import math
import pytest

from scripts.export_pedicularis_xy_surface_handoff import export_xy_handoff


def _conflict(context_id: str = "PEDICULARIS_POP_A_2027") -> dict:
    return {
        "receipt_schema_version": "THREE_WORLD_CONFLICT_HANDOFF_V1",
        "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
        "context_id": context_id,
        "system": "Pedicularis rex",
        "population_id": "POP_A",
        "season_id": "2027",
        "fitness_scale_id": "UNDAMAGED_SEEDS_PER_FOCAL_FLOWER",
        "conflict_load": {"point": 0.4, "lower_95": 0.3, "upper_95": 0.5},
    }


def _result(population: str = "POP_A", season: str = "2027", gap: float = -0.1) -> dict:
    ws = 10.0
    wd = ws + gap
    return {
        "analysis": "bita_empirical_dimensional_release",
        "status": "FUNCTIONAL_DIFFERENTIATION_OUTCOME_NOT_SUPPORTED",
        "system_wrapper_schema_version": "BITA_PEDICULARIS_DIMENSIONAL_RELEASE_WRAPPER_V2",
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "pedicularis_mapping": {
            "y0": "DRAINED_WATER_DEFENCE_DISABLED",
            "y1": "PROTECTED_WATER_DEFENCE_ACTIVE",
            "fitness_value": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
        },
        "sch_reference": {
            "reference_value": 2.0,
            "reference_type": "STATE_SPECIFIC_P1G0_OPTIMUM",
        },
        "observed_estimands": {
            "x_optimum_y0": 0.0,
            "x_optimum_y1": 0.5,
            "dimensional_release": 0.5,
            "within_bita_optimum_fitness_gain": gap,
            "y_effect_function1": 0.0,
            "y_effect_function2": 0.2,
            "fitness_fit_y0": {"optimum_value": ws},
            "fitness_fit_y1": {"optimum_value": wd},
        },
        "bootstrap": {
            "dimensional_release_95_ci": [0.2, 0.8],
            "within_bita_optimum_fitness_gain_95_ci": [-0.2, -0.02] if gap < 0 else [0.02, 0.2],
            "y_effect_function1_95_ci": [-0.05, 0.05],
            "y_effect_function2_95_ci": [0.1, 0.3],
        },
        "decisions": {
            "y_targets_function2": True,
            "y_preserves_function1": True,
            "x_optimum_released_toward_sch_reference": True,
            "within_bita_joint_fitness_improves": gap > 0,
            "released_surface_has_interior_optimum": True,
        },
    }


def _config() -> dict:
    return {
        "context_id": "PEDICULARIS_POP_A_2027",
        "fitness_scale_id": "UNDAMAGED_SEEDS_PER_FOCAL_FLOWER",
        "fitness_value_semantics": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
    }


def test_exports_surface_even_when_bita_positive_gate_fails() -> None:
    out = export_xy_handoff(_result(gap=-0.1), _conflict(), _config())
    assert out["receipt_schema_version"] == "PEDICULARIS_XY_SURFACE_HANDOFF_V1"
    assert out["status"] == "PEDICULARIS_XY_SURFACE_ANALYZED"
    assert out["context_id"] == "PEDICULARIS_POP_A_2027"
    assert out["bita_surface_status"] == "FUNCTIONAL_DIFFERENTIATION_OUTCOME_NOT_SUPPORTED"
    assert math.isclose(out["worldlines"]["gap_y1_minus_y0"]["point"], -0.1)
    assert out["worldlines"]["gap_y1_minus_y0"]["upper_95"] < 0
    assert math.isclose(out["dimensional_release"]["point"], 0.5)


def test_positive_surface_is_exported_without_changing_schema() -> None:
    out = export_xy_handoff(_result(gap=0.1), _conflict(), _config())
    assert out["receipt_schema_version"] == "PEDICULARIS_XY_SURFACE_HANDOFF_V1"
    assert out["worldlines"]["gap_y1_minus_y0"]["lower_95"] > 0


def test_population_or_season_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="population and season"):
        export_xy_handoff(_result(season="2028"), _conflict(), _config())


def test_context_or_scale_mismatch_fails_closed() -> None:
    config = _config()
    config["context_id"] = "OTHER"
    with pytest.raises(ValueError, match="context_id"):
        export_xy_handoff(_result(), _conflict(), config)
    config = _config()
    config["fitness_scale_id"] = "OTHER_SCALE"
    with pytest.raises(ValueError, match="fitness_scale_id"):
        export_xy_handoff(_result(), _conflict(), config)


def test_fitness_semantics_must_be_explicitly_frozen() -> None:
    config = _config()
    config["fitness_value_semantics"] = "OTHER"
    with pytest.raises(ValueError, match="fitness semantics"):
        export_xy_handoff(_result(), _conflict(), config)
