from __future__ import annotations

import json

import pytest

from scripts.extract_third_network_camera_effort_freeze import (
    extract_camera_effort,
)


def _plan() -> dict[str, object]:
    return {
        "receipt": "BITA_THIRD_NETWORK_CAMERA_EFFORT_PLAN_V1",
        "status": "PLANNING_TARGET_EFFORT_IDENTIFIED",
        "route_blind_contract": {
            "uses_route_outcome": False,
            "uses_access_mismatch": False,
            "uses_morphology": False,
            "effort_allocation": "uniform_camera_hours_per_plant_x_site",
        },
        "model": {
            "qualifying_fraction": 0.5,
            "target_success_probability": 0.8,
        },
        "recommended_uniform_effort": {
            "uniform_camera_hours_per_plant_site": 168.0,
            "planning_target_success_probability": 0.87,
        },
    }


def _write(tmp_path, payload):
    path = tmp_path / "plan.json"
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def test_extract_camera_effort_freezes_exact_planner_values(tmp_path) -> None:
    path = _write(tmp_path, _plan())
    block = extract_camera_effort(path)

    assert block["planner_status"] == "PLANNING_TARGET_EFFORT_IDENTIFIED"
    assert block["uniform_camera_hours_per_plant_site"] == 168.0
    assert block["qualifying_fraction"] == 0.5
    assert block["planner_target_success_probability"] == 0.8
    assert block["planner_achieved_success_probability"] == 0.87
    assert block["may_extend_based_on_route_outcomes"] is False
    assert len(block["planner_receipt_sha256"]) == 64


def test_extract_camera_effort_rejects_non_route_blind_plan(tmp_path) -> None:
    plan = _plan()
    plan["route_blind_contract"]["uses_route_outcome"] = True
    path = _write(tmp_path, plan)

    with pytest.raises(ValueError, match="CAMERA_EFFORT_PLAN_NOT_ROUTE_BLIND"):
        extract_camera_effort(path)


def test_extract_camera_effort_rejects_sub_80_percent_target(tmp_path) -> None:
    plan = _plan()
    plan["model"]["target_success_probability"] = 0.79
    path = _write(tmp_path, plan)

    with pytest.raises(
        ValueError,
        match="CAMERA_EFFORT_TARGET_SUCCESS_BELOW_FROZEN_MINIMUM",
    ):
        extract_camera_effort(path)


def test_extract_camera_effort_rejects_recommendation_below_target(tmp_path) -> None:
    plan = _plan()
    plan["recommended_uniform_effort"]["planning_target_success_probability"] = 0.75
    path = _write(tmp_path, plan)

    with pytest.raises(
        ValueError,
        match="CAMERA_EFFORT_RECOMMENDATION_DOES_NOT_MEET_TARGET",
    ):
        extract_camera_effort(path)


def test_extract_camera_effort_rejects_structurally_unready_plan(tmp_path) -> None:
    plan = _plan()
    plan["status"] = "PLANNING_TARGET_STRUCTURALLY_IMPOSSIBLE"
    path = _write(tmp_path, plan)

    with pytest.raises(ValueError, match="CAMERA_EFFORT_PLAN_NOT_READY"):
        extract_camera_effort(path)
