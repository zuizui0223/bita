import math

import pytest

from scripts.project_sch_conflict_budget_into_bita import project


def _receipt(load=0.5, lo=0.48, hi=0.52):
    return {
        "receipt_schema_version": "SCH_COMPONENT_CONFLICT_BUDGET_V1",
        "status": "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED",
        "fitness_scale_id": "INTACT_SEEDS_COMPONENT_SCALE",
        "criticality_export": {
            "L_S_component": load,
            "L_S_component_95_ci": [lo, hi],
        },
    }


def _config(s=0.2, k=0.1, semantics="STRUCTURAL_ARCHITECTURE_MAINTENANCE_COST"):
    return {
        "fitness_scale_id": "INTACT_SEEDS_COMPONENT_SCALE",
        "decoupling_fraction": s,
        "decoupling_fraction_95_ci": [s, s],
        "architecture_cost": k,
        "architecture_cost_95_ci": [k, k],
        "cost_semantics": semantics,
        "cost_source": "independent architecture assay",
    }


def test_reference_point_lands_on_common_surface() -> None:
    result = project(_receipt(0.5, 0.5, 0.5), _config(0.2, 0.1))
    assert math.isclose(result["derived"]["recoverable_component_loss"], 0.1)
    assert math.isclose(result["derived"]["architecture_margin"], 0.0)
    assert math.isclose(result["derived"]["critical_shared_conflict_load"], 0.5)
    assert result["classification"] == "CRITICAL_SURFACE_NOT_RESOLVED_WITH_CURRENT_INTERVALS"
    assert result["claim_level"] == "ARCHITECTURE_LEVEL_C2_PROJECTION"


def test_interval_entirely_above_zero_supports_differentiated_side() -> None:
    result = project(_receipt(0.8, 0.75, 0.85), _config(0.5, 0.2))
    assert result["derived"]["architecture_margin_conservative_95_bounds"][0] > 0
    assert result["classification"] == "DIFFERENTIATED_SIDE_SUPPORTED_ON_DECLARED_SCALE"


def test_interval_entirely_below_zero_supports_shared_side() -> None:
    result = project(_receipt(0.2, 0.18, 0.22), _config(0.5, 0.2))
    assert result["derived"]["architecture_margin_conservative_95_bounds"][1] < 0
    assert result["classification"] == "SHARED_SIDE_SUPPORTED_ON_DECLARED_SCALE"


def test_functional_state_cost_is_not_promoted_to_structural_architecture() -> None:
    result = project(_receipt(), _config(0.5, 0.1, "FUNCTIONAL_STATE_DEPLOYMENT_COST"))
    assert result["claim_level"] == "FUNCTIONAL_STATE_C2_PROJECTION_ONLY"


def test_mismatched_fitness_scale_fails_closed() -> None:
    config = _config()
    config["fitness_scale_id"] = "OTHER_SCALE"
    with pytest.raises(ValueError, match="exactly match"):
        project(_receipt(), config)


def test_kappa_cannot_be_used_as_architecture_cost() -> None:
    config = _config()
    config["cost_source"] = "kappa_delta from local joint-channel assay"
    with pytest.raises(ValueError, match="kappa"):
        project(_receipt(), config)
