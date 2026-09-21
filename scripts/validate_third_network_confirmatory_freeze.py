"""Validate the prospective third-network pre-video freeze receipt."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = "REQUIRED_BEFORE_USE"


def validate(receipt: dict[str, object]) -> dict[str, object]:
    failures: list[str] = []

    if receipt.get("receipt") != "BITA_THIRD_NETWORK_CONFIRMATORY_FREEZE_V1":
        failures.append("wrong_receipt_type")

    site = receipt.get("site_selection", {})
    if not isinstance(site, dict):
        failures.append("site_selection_missing")
        site = {}
    if site.get("route_outcome_blind") is not True:
        failures.append("site_selection_not_route_blind")
    if site.get("pilot_B_or_L_presence_used_for_selection") is not False:
        failures.append("pilot_route_used_for_selection")
    if not site.get("final_sites"):
        failures.append("final_sites_not_frozen")
    if not site.get("final_plant_species"):
        failures.append("final_plant_species_not_frozen")
    if site.get("selection_basis") in {None, "", REQUIRED}:
        failures.append("selection_basis_not_frozen")

    visitor = receipt.get("visitor_identification", {})
    if not isinstance(visitor, dict) or visitor.get("protocol_version") in {None, "", REQUIRED}:
        failures.append("visitor_identification_not_frozen")

    morphology = receipt.get("morphology", {})
    if not isinstance(morphology, dict):
        failures.append("morphology_missing")
        morphology = {}
    for key in ("plant_protocol_version", "mammal_protocol_version"):
        if morphology.get(key) in {None, "", REQUIRED}:
            failures.append(f"{key}_not_frozen")

    route = receipt.get("route_coding", {})
    if not isinstance(route, dict) or route.get("coders_blind_to_P_V_M") is not True:
        failures.append("route_coder_blinding_not_frozen")

    camera = receipt.get("camera_effort", {})
    if not isinstance(camera, dict):
        failures.append("camera_effort_missing")
        camera = {}
    if camera.get("rule") in {None, "", REQUIRED}:
        failures.append("camera_effort_rule_not_frozen")
    if camera.get("may_extend_based_on_route_outcomes") is not False:
        failures.append("outcome_adaptive_camera_effort_forbidden")

    permissions = receipt.get("permissions", {})
    if not isinstance(permissions, dict):
        failures.append("permissions_missing")
        permissions = {}
    for key in ("land_access", "animal_capture_or_handling", "plant_measurement_or_collection"):
        if permissions.get(key) in {None, "", REQUIRED}:
            failures.append(f"{key}_unresolved")

    for key in ("freeze_time_utc", "frozen_by"):
        if receipt.get(key) in {None, "", REQUIRED}:
            failures.append(f"{key}_missing")

    status = "READY_FOR_CONFIRMATORY_VIDEO_OPEN" if not failures else "BLOCKED"
    return {
        "status": status,
        "failures": failures,
        "claim_boundary": (
            "READY means design/admin fields are frozen before route-video opening; "
            "it does not imply that the future confirmatory data pass the biological eligibility gate."
        ),
    }


def run(path: str | Path) -> dict[str, object]:
    receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate(receipt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_json")
    args = parser.parse_args()
    result = run(args.receipt_json)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "READY_FOR_CONFIRMATORY_VIDEO_OPEN":
        raise SystemExit(2)
