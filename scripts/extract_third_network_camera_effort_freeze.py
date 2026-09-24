"""Extract a frozen camera-effort block from a route-blind planner receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

MIN_TARGET_SUCCESS = 0.80


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _number(value: object, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def extract_camera_effort(plan_path: str | Path) -> dict[str, object]:
    path = Path(plan_path)
    plan = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict):
        raise ValueError("camera effort plan must be a JSON object")

    if plan.get("receipt") != "BITA_THIRD_NETWORK_CAMERA_EFFORT_PLAN_V1":
        raise ValueError("WRONG_CAMERA_EFFORT_PLAN_RECEIPT")
    if plan.get("status") != "PLANNING_TARGET_EFFORT_IDENTIFIED":
        raise ValueError("CAMERA_EFFORT_PLAN_NOT_READY")

    route_blind = plan.get("route_blind_contract", {})
    if not isinstance(route_blind, dict):
        raise ValueError("CAMERA_EFFORT_ROUTE_BLIND_CONTRACT_MISSING")
    if any(
        route_blind.get(key) is not False
        for key in ("uses_route_outcome", "uses_access_mismatch", "uses_morphology")
    ):
        raise ValueError("CAMERA_EFFORT_PLAN_NOT_ROUTE_BLIND")
    if route_blind.get("effort_allocation") != "uniform_camera_hours_per_plant_x_site":
        raise ValueError("CAMERA_EFFORT_ALLOCATION_NOT_UNIFORM")

    model = plan.get("model", {})
    recommended = plan.get("recommended_uniform_effort")
    structure = plan.get("candidate_structure", {})
    if (
        not isinstance(model, dict)
        or not isinstance(recommended, dict)
        or not isinstance(structure, dict)
    ):
        raise ValueError("CAMERA_EFFORT_PLAN_FIELDS_MISSING")

    q = _number(model.get("qualifying_fraction"), "qualifying_fraction")
    target = _number(
        model.get("target_success_probability"),
        "target_success_probability",
    )
    hours = _number(
        recommended.get("uniform_camera_hours_per_plant_site"),
        "uniform_camera_hours_per_plant_site",
    )
    achieved = _number(
        recommended.get("planning_target_success_probability"),
        "planning_target_success_probability",
    )
    deployment_count = int(structure.get("distinct_plant_site_deployments", 0))
    deployment_sha = str(
        structure.get("plant_site_deployment_set_sha256", "")
    ).strip().lower()

    if deployment_count <= 0:
        raise ValueError("CAMERA_EFFORT_DEPLOYMENT_COUNT_INVALID")
    if len(deployment_sha) != 64:
        raise ValueError("CAMERA_EFFORT_DEPLOYMENT_DIGEST_INVALID")
    try:
        int(deployment_sha, 16)
    except ValueError as exc:
        raise ValueError("CAMERA_EFFORT_DEPLOYMENT_DIGEST_INVALID") from exc

    if not (0 < q <= 1):
        raise ValueError("CAMERA_EFFORT_QUALIFYING_FRACTION_INVALID")
    if not (MIN_TARGET_SUCCESS <= target <= 1):
        raise ValueError("CAMERA_EFFORT_TARGET_SUCCESS_BELOW_FROZEN_MINIMUM")
    if hours <= 0:
        raise ValueError("CAMERA_EFFORT_HOURS_INVALID")
    if not (target <= achieved <= 1):
        raise ValueError("CAMERA_EFFORT_RECOMMENDATION_DOES_NOT_MEET_TARGET")

    return {
        "rule": (
            f"uniform {hours:g} camera-hours per plant x site; "
            "no route-outcome-adaptive extension"
        ),
        "planner_receipt_sha256": _sha256(path),
        "planner_status": "PLANNING_TARGET_EFFORT_IDENTIFIED",
        "uniform_camera_hours_per_plant_site": hours,
        "qualifying_fraction": q,
        "planner_target_success_probability": target,
        "planner_achieved_success_probability": achieved,
        "planned_plant_site_deployments": deployment_count,
        "planned_plant_site_deployment_set_sha256": deployment_sha,
        "effort_rule_version": f"CAMERA_EFFORT_PLAN:{_sha256(path)}",
        "may_extend_based_on_route_outcomes": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_effort_plan_json")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = extract_camera_effort(args.camera_effort_plan_json)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
