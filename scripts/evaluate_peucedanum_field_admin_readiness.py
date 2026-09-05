from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


SCHEMA = "BITA_PEUCEDANUM_FIELD_ADMIN_READINESS_V1"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
READY_STATUS = "PEUCEDANUM_FIELD_ADMINISTRATIVELY_READY"
BLOCKED_STATUS = "PEUCEDANUM_FIELD_ADMINISTRATIVELY_BLOCKED"
ALLOWED_ACTION_STATUSES = {"PERMITTED", "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY"}
ALLOWED_ACCESS_STATUSES = {"PERMITTED", "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY"}


def _required_text(payload: dict, key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"field {key!r} must be resolved before administrative readiness evaluation")
    return value.strip()


def _boolish(payload: dict, key: str) -> bool:
    value = payload.get(key)
    if value is True:
        return True
    if value is False:
        return False
    if value == PLACEHOLDER or value is None:
        raise ValueError(f"field {key!r} must be resolved to true/false")
    raise ValueError(f"field {key!r} must be boolean")


def _date(value: str, field: str) -> dt.date:
    if value == PLACEHOLDER:
        raise ValueError(f"field {field!r} must be resolved")
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"field {field!r} must be ISO date YYYY-MM-DD") from exc


def _action_gate(action: dict, *, field_start: dt.date, field_end: dt.date, label: str) -> dict:
    planned = action.get("planned")
    if planned is not True and planned is not False:
        raise ValueError(f"{label}.planned must be boolean")
    if not planned:
        return {
            "planned": False,
            "status_resolved": True,
            "authorization_covers_field_window": True,
            "gate": True,
            "regulatory_status": "NOT_PLANNED",
        }

    regulatory_status = _required_text(action, "regulatory_status")
    if regulatory_status not in ALLOWED_ACTION_STATUSES:
        return {
            "planned": True,
            "status_resolved": False,
            "authorization_covers_field_window": False,
            "gate": False,
            "regulatory_status": regulatory_status,
        }

    authorization_id = _required_text(action, "authorization_id")
    valid_from = _date(_required_text(action, "authorization_valid_from"), f"{label}.authorization_valid_from")
    valid_until = _date(_required_text(action, "authorization_valid_until"), f"{label}.authorization_valid_until")
    if valid_until < valid_from:
        raise ValueError(f"{label} authorization validity dates are reversed")
    covers = valid_from <= field_start and valid_until >= field_end
    return {
        "planned": True,
        "status_resolved": True,
        "authorization_id": authorization_id,
        "authorization_valid_from": valid_from.isoformat(),
        "authorization_valid_until": valid_until.isoformat(),
        "authorization_covers_field_window": covers,
        "gate": covers,
        "regulatory_status": regulatory_status,
    }


def evaluate(config: dict) -> dict:
    if config.get("schema_version") != SCHEMA:
        raise ValueError(f"config must use schema {SCHEMA}")

    site_code = _required_text(config, "site_code")
    coordinates_verified = _boolish(config, "exact_site_coordinates_verified")
    municipality = _required_text(config, "municipality")
    zone = _required_text(config, "national_park_zone")
    office = _required_text(config, "responsible_environment_office")
    field_start = _date(_required_text(config, "planned_field_start"), "planned_field_start")
    field_end = _date(_required_text(config, "planned_field_end"), "planned_field_end")
    if field_end < field_start:
        raise ValueError("planned_field_end precedes planned_field_start")

    action_results = {
        "plant_q_manipulation": _action_gate(
            config.get("plant_q_manipulation", {}), field_start=field_start, field_end=field_end, label="plant_q_manipulation"
        ),
        "leaf_sampling_for_genotyping": _action_gate(
            config.get("leaf_sampling_for_genotyping", {}), field_start=field_start, field_end=field_end, label="leaf_sampling_for_genotyping"
        ),
        "predator_egg_removal": _action_gate(
            config.get("predator_egg_removal", {}), field_start=field_start, field_end=field_end, label="predator_egg_removal"
        ),
    }

    land = config.get("land_manager_or_site_owner", {})
    land_identified = _boolish(land, "identified")
    access_status = _required_text(land, "access_and_research_status")
    access_status_ok = access_status in ALLOWED_ACCESS_STATUSES
    access_id = _required_text(land, "authorization_id") if access_status_ok else None

    other_checked = _boolish(config, "other_required_authorizations_checked")

    gates = {
        "exact_site_coordinates_verified": coordinates_verified,
        "municipality_and_park_zone_resolved": bool(municipality and zone),
        "responsible_environment_office_resolved": bool(office),
        "plant_q_manipulation_authorized_for_field_window": action_results["plant_q_manipulation"]["gate"],
        "leaf_sampling_authorized_for_field_window": action_results["leaf_sampling_for_genotyping"]["gate"],
        "predator_egg_removal_authorized_for_field_window": action_results["predator_egg_removal"]["gate"],
        "land_manager_identified": land_identified,
        "site_access_and_research_authorized": access_status_ok,
        "other_required_authorizations_checked": other_checked,
    }
    ready = all(gates.values())

    return {
        "receipt_schema_version": SCHEMA,
        "site_code": site_code,
        "site_resolution": {
            "exact_coordinates_verified": coordinates_verified,
            "municipality": municipality,
            "national_park_zone": zone,
            "responsible_environment_office": office,
            "planned_field_start": field_start.isoformat(),
            "planned_field_end": field_end.isoformat(),
        },
        "action_authorizations": action_results,
        "land_manager_or_site_owner": {
            "identified": land_identified,
            "access_and_research_status": access_status,
            "authorization_id": access_id,
        },
        "gates": gates,
        "status": READY_STATUS if ready else BLOCKED_STATUS,
        "claim_boundary": (
            "This receipt records resolved administrative permissions supplied by the researcher or authority. "
            "It is not legal advice and does not infer that a permit is unnecessary from ecological or zoning assumptions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Peucedanum field administrative readiness")
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    receipt = evaluate(config)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
