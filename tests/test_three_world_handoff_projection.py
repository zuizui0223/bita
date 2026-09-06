import pytest

from scripts.project_three_world_handoff_into_bita import project_handoff


def _handoff():
    return {
        "receipt_schema_version": "THREE_WORLD_CONFLICT_HANDOFF_V1",
        "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
        "context_id": "PEDICULARIS_POP_A_2027",
        "system": "Pedicularis rex",
        "population_id": "POP_A",
        "season_id": "2027",
        "fitness_scale_id": "INTACT_SEEDS_PER_FLOWER",
        "conflict_load": {"point": 0.4, "lower_95": 0.3, "upper_95": 0.5},
        "source": {"repository": "sch"},
    }


def _config():
    return {
        "context_id": "PEDICULARIS_POP_A_2027",
        "fitness_scale_id": "INTACT_SEEDS_PER_FLOWER",
        "cost_semantics": "FUNCTIONAL_STATE_DEPLOYMENT_COST",
        "cost_source": "registered water-defence deployment manipulation",
        "decoupling_fraction": 0.5,
        "decoupling_fraction_95_ci": [0.4, 0.6],
        "architecture_cost": 0.3,
        "architecture_cost_95_ci": [0.25, 0.35],
    }


def test_matching_context_projects_to_bita():
    result = project_handoff(_handoff(), _config())
    assert result["three_world_handoff"]["context_id"] == "PEDICULARIS_POP_A_2027"
    assert result["three_world_handoff"]["fitness_scale_id"] == "INTACT_SEEDS_PER_FLOWER"
    assert result["inputs"]["L_S_component"] == 0.4
    assert result["claim_level"] == "FUNCTIONAL_STATE_C2_PROJECTION_ONLY"


def test_context_mismatch_fails_closed():
    config = _config()
    config["context_id"] = "OTHER_CONTEXT"
    with pytest.raises(ValueError, match="context_id"):
        project_handoff(_handoff(), config)


def test_fitness_scale_mismatch_fails_closed():
    config = _config()
    config["fitness_scale_id"] = "RELATIVE_FITNESS"
    with pytest.raises(ValueError, match="fitness_scale_id"):
        project_handoff(_handoff(), config)


def test_kappa_is_still_rejected_by_underlying_projection():
    config = _config()
    config["cost_source"] = "kappa_delta"
    with pytest.raises(ValueError, match="kappa"):
        project_handoff(_handoff(), config)
