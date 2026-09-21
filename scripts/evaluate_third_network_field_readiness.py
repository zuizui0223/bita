"""Evaluate prospective third-network field execution readiness.

This module deliberately contains no legal inference engine. It accepts only
resolved authorization/review statuses supplied by the researcher or relevant
authority, verifies the route-blind presurvey receipt, and verifies the
pre-video confirmatory freeze receipt before field execution can be promoted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

from scripts.validate_third_network_confirmatory_freeze import validate as validate_freeze

SCHEMA = "BITA_THIRD_NETWORK_FIELD_READINESS_V1"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
READY_STATUS = "THIRD_NETWORK_FIELD_EXECUTION_READY"
BLOCKED_STATUS = "THIRD_NETWORK_FIELD_EXECUTION_BLOCKED"
ALLOWED_STATUSES = {"PERMITTED", "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY"}
ALLOWED_MORPH_MODES = {
    "LIVE_CAPTURE",
    "EXISTING_SPECIMENS",
    "INDEPENDENT_MORPHOMETRIC_DATA",
}
PRESURVEY_READY = "PRESURVEY_ROUTE_BLIND_ELIGIBLE_SITES_PRESENT"


def _required_text(payload: dict, key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"field {key!r} must be resolved before field readiness evaluation")
    return value.strip()


def _bool(payload: dict, key: str) -> bool:
    value = payload.get(key)
    if value is True:
        return True
    if value is False:
        return False
    raise ValueError(f"field {key!r} must be resolved to true/false")


def _date(value: str, field: str) -> dt.date:
    if value == PLACEHOLDER:
        raise ValueError(f"field {field!r} must be resolved")
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"field {field!r} must be ISO date YYYY-MM-DD") from exc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_hashed_json(
    payload: dict,
    *,
    base_dir: str | Path,
    label: str,
) -> tuple[Path, str, str, dict]:
    rel = _required_text(payload, "receipt_path" if "receipt_path" in payload else "path")
    expected = _required_text(payload, "sha256").lower()
    path = Path(base_dir) / rel
    if not path.exists():
        raise ValueError(f"{label} receipt not found: {path}")
    actual = _sha256(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return path, expected, actual, data


def _action_gate(action: dict, *, field_start: dt.date, field_end: dt.date, label: str) -> dict:
    planned = action.get("planned")
    if planned is not True and planned is not False:
        raise ValueError(f"{label}.planned must be boolean")

    if not planned:
        return {
            "planned": False,
            "regulatory_status": "NOT_PLANNED",
            "status_resolved": True,
            "authorization_covers_field_window": True,
            "gate": True,
        }

    status = _required_text(action, "regulatory_status")
    if status not in ALLOWED_STATUSES:
        return {
            "planned": True,
            "regulatory_status": status,
            "status_resolved": False,
            "authorization_covers_field_window": False,
            "gate": False,
        }

    evidence = _required_text(action, "evidence_reference")
    valid_from = _date(
        _required_text(action, "authorization_valid_from"),
        f"{label}.authorization_valid_from",
    )
    valid_until = _date(
        _required_text(action, "authorization_valid_until"),
        f"{label}.authorization_valid_until",
    )
    if valid_until < valid_from:
        raise ValueError(f"{label} authorization validity dates are reversed")

    covers = valid_from <= field_start and valid_until >= field_end
    return {
        "planned": True,
        "regulatory_status": status,
        "evidence_reference": evidence,
        "authorization_valid_from": valid_from.isoformat(),
        "authorization_valid_until": valid_until.isoformat(),
        "status_resolved": True,
        "authorization_covers_field_window": covers,
        "gate": covers,
    }


def evaluate(
    config: dict,
    *,
    base_dir: str | Path = ".",
) -> dict:
    if config.get("schema_version") != SCHEMA:
        raise ValueError(f"config must use schema {SCHEMA}")

    field_start = _date(_required_text(config, "planned_field_start"), "planned_field_start")
    field_end = _date(_required_text(config, "planned_field_end"), "planned_field_end")
    if field_end < field_start:
        raise ValueError("planned_field_end precedes planned_field_start")

    sites_verified = _bool(config, "site_locations_verified_privately")
    site_receipt = _required_text(config, "site_location_receipt_reference")

    presurvey_cfg = config.get("route_blind_presurvey", {})
    if not isinstance(presurvey_cfg, dict):
        raise ValueError("route_blind_presurvey must be an object")
    presurvey_path, presurvey_expected_sha, presurvey_actual_sha, presurvey_payload = _load_hashed_json(
        presurvey_cfg,
        base_dir=base_dir,
        label="route-blind presurvey",
    )
    presurvey_sha_ok = presurvey_actual_sha == presurvey_expected_sha
    presurvey_status = str(presurvey_payload.get("status", ""))
    presurvey_ready = presurvey_status == PRESURVEY_READY
    presurvey_route_fields_absent = (
        presurvey_payload.get("route_outcome_fields_present") is False
        and presurvey_payload.get("morphology_fields_present") is False
    )
    presurvey_sites = {
        str(site) for site in presurvey_payload.get("eligible_sites", [])
        if str(site).strip()
    }

    freeze_cfg = config.get("confirmatory_freeze_receipt", {})
    if not isinstance(freeze_cfg, dict):
        raise ValueError("confirmatory_freeze_receipt must be an object")
    freeze_path, freeze_expected_sha, freeze_actual_sha, freeze_payload = _load_hashed_json(
        freeze_cfg,
        base_dir=base_dir,
        label="confirmatory freeze",
    )
    freeze_sha_ok = freeze_actual_sha == freeze_expected_sha
    freeze_result = validate_freeze(freeze_payload)
    freeze_ready = freeze_result["status"] == "READY_FOR_CONFIRMATORY_VIDEO_OPEN"

    site_cfg = freeze_payload.get("site_selection", {})
    final_sites = {
        str(site) for site in site_cfg.get("final_sites", [])
        if str(site).strip()
    } if isinstance(site_cfg, dict) else set()
    final_sites_supported_by_presurvey = bool(final_sites) and final_sites.issubset(presurvey_sites)

    actions = {
        "land_site_access": _action_gate(
            config.get("land_site_access", {}),
            field_start=field_start,
            field_end=field_end,
            label="land_site_access",
        ),
        "camera_deployment": _action_gate(
            config.get("camera_deployment", {}),
            field_start=field_start,
            field_end=field_end,
            label="camera_deployment",
        ),
        "plant_morphology_measurement": _action_gate(
            config.get("plant_morphology_measurement", {}),
            field_start=field_start,
            field_end=field_end,
            label="plant_morphology_measurement",
        ),
        "plant_tissue_collection": _action_gate(
            config.get("plant_tissue_collection", {}),
            field_start=field_start,
            field_end=field_end,
            label="plant_tissue_collection",
        ),
        "mammal_capture_or_handling": _action_gate(
            config.get("mammal_capture_or_handling", {}),
            field_start=field_start,
            field_end=field_end,
            label="mammal_capture_or_handling",
        ),
        "animal_ethics_or_institutional_review": _action_gate(
            config.get("animal_ethics_or_institutional_review", {}),
            field_start=field_start,
            field_end=field_end,
            label="animal_ethics_or_institutional_review",
        ),
    }

    morph = config.get("mammal_morphology_source", {})
    if not isinstance(morph, dict):
        raise ValueError("mammal_morphology_source must be an object")
    morph_mode = _required_text(morph, "mode")
    morph_ref = _required_text(morph, "evidence_reference")
    same_assemblage = _bool(morph, "same_regional_assemblage_supported")
    morph_mode_ok = morph_mode in ALLOWED_MORPH_MODES

    other_checked = _bool(config, "other_required_authorizations_checked")

    gates = {
        "site_locations_verified_privately": sites_verified,
        "route_blind_presurvey_checksum_matches": presurvey_sha_ok,
        "route_blind_presurvey_ready": presurvey_ready,
        "route_and_morphology_fields_absent_from_presurvey": presurvey_route_fields_absent,
        "final_sites_supported_by_route_blind_presurvey": final_sites_supported_by_presurvey,
        "confirmatory_freeze_receipt_checksum_matches": freeze_sha_ok,
        "confirmatory_freeze_receipt_ready": freeze_ready,
        "land_site_access_resolved": actions["land_site_access"]["gate"],
        "camera_deployment_resolved": actions["camera_deployment"]["gate"],
        "plant_morphology_measurement_resolved": actions["plant_morphology_measurement"]["gate"],
        "plant_tissue_collection_resolved_or_not_planned": actions["plant_tissue_collection"]["gate"],
        "mammal_capture_or_handling_resolved_or_not_planned": actions["mammal_capture_or_handling"]["gate"],
        "animal_ethics_or_institutional_review_resolved": actions["animal_ethics_or_institutional_review"]["gate"],
        "mammal_morphology_mode_predeclared": morph_mode_ok,
        "mammal_morphology_same_regional_assemblage_supported": same_assemblage,
        "other_required_authorizations_checked": other_checked,
    }
    ready = all(gates.values())

    return {
        "receipt_schema_version": SCHEMA,
        "system": config.get("system"),
        "field_window": {
            "start": field_start.isoformat(),
            "end": field_end.isoformat(),
        },
        "site_location_receipt_reference": site_receipt,
        "route_blind_presurvey": {
            "path": str(presurvey_path),
            "expected_sha256": presurvey_expected_sha,
            "actual_sha256": presurvey_actual_sha,
            "status": presurvey_status,
            "eligible_sites": sorted(presurvey_sites),
        },
        "confirmatory_freeze_receipt": {
            "path": str(freeze_path),
            "expected_sha256": freeze_expected_sha,
            "actual_sha256": freeze_actual_sha,
            "validator_status": freeze_result["status"],
            "validator_failures": freeze_result["failures"],
            "final_sites": sorted(final_sites),
        },
        "action_authorizations": actions,
        "mammal_morphology_source": {
            "mode": morph_mode,
            "evidence_reference": morph_ref,
            "same_regional_assemblage_supported": same_assemblage,
        },
        "gates": gates,
        "status": READY_STATUS if ready else BLOCKED_STATUS,
        "claim_boundary": (
            "This is an operational readiness receipt, not legal advice. "
            "PERMITTED/NOT_REQUIRED statuses must come from the researcher, institution, land manager, "
            "or relevant authority; the evaluator never infers them from prior studies or site ecology. "
            "READY authorizes only the frozen field protocol to begin, not any k=3 scientific claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate third-network field readiness")
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    receipt = evaluate(config, base_dir=args.config_json.parent)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
