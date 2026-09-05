from __future__ import annotations

import pytest

from scripts.evaluate_peucedanum_field_admin_readiness import (
    BLOCKED_STATUS,
    READY_STATUS,
    SCHEMA,
    evaluate,
)


def _config() -> dict:
    return {
        "schema_version": SCHEMA,
        "site_code": "HA",
        "exact_site_coordinates_verified": True,
        "municipality": "Higashikawa",
        "national_park_zone": "SPECIAL_AREA_EXACT_CLASS_VERIFIED",
        "responsible_environment_office": "Higashikawa Ranger Office",
        "planned_field_start": "2027-07-05",
        "planned_field_end": "2027-08-20",
        "plant_q_manipulation": {
            "planned": True,
            "regulatory_status": "PERMITTED",
            "authorization_id": "PLANT-001",
            "authorization_valid_from": "2027-07-01",
            "authorization_valid_until": "2027-08-31",
        },
        "leaf_sampling_for_genotyping": {
            "planned": True,
            "regulatory_status": "PERMITTED",
            "authorization_id": "LEAF-001",
            "authorization_valid_from": "2027-07-01",
            "authorization_valid_until": "2027-08-31",
        },
        "predator_egg_removal": {
            "planned": True,
            "regulatory_status": "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY",
            "authorization_id": "OFFICE-CONFIRMATION-001",
            "authorization_valid_from": "2027-07-01",
            "authorization_valid_until": "2027-08-31",
        },
        "land_manager_or_site_owner": {
            "identified": True,
            "access_and_research_status": "PERMITTED",
            "authorization_id": "LAND-001",
        },
        "other_required_authorizations_checked": True,
    }


def test_resolved_permissions_promote_administrative_readiness() -> None:
    receipt = evaluate(_config())
    assert receipt["status"] == READY_STATUS
    assert all(receipt["gates"].values())
    assert receipt["action_authorizations"]["predator_egg_removal"]["regulatory_status"] == "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY"
    assert "not legal advice" in receipt["claim_boundary"]


def test_expired_plant_authorization_blocks_field_readiness() -> None:
    config = _config()
    config["plant_q_manipulation"]["authorization_valid_until"] = "2027-07-20"
    receipt = evaluate(config)
    assert receipt["status"] == BLOCKED_STATUS
    assert receipt["gates"]["plant_q_manipulation_authorized_for_field_window"] is False


def test_unresolved_action_status_does_not_get_inferred_from_zone() -> None:
    config = _config()
    config["predator_egg_removal"]["regulatory_status"] = "UNKNOWN_BUT_PROBABLY_NOT_REQUIRED"
    receipt = evaluate(config)
    assert receipt["status"] == BLOCKED_STATUS
    assert receipt["gates"]["predator_egg_removal_authorized_for_field_window"] is False


def test_unverified_coordinates_fail_closed() -> None:
    config = _config()
    config["exact_site_coordinates_verified"] = False
    receipt = evaluate(config)
    assert receipt["status"] == BLOCKED_STATUS
    assert receipt["gates"]["exact_site_coordinates_verified"] is False


def test_template_placeholders_raise_before_readiness_is_evaluated() -> None:
    config = _config()
    config["municipality"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="must be resolved"):
        evaluate(config)


def test_unplanned_leaf_sampling_does_not_require_leaf_authorization() -> None:
    config = _config()
    config["leaf_sampling_for_genotyping"] = {"planned": False}
    receipt = evaluate(config)
    assert receipt["status"] == READY_STATUS
    assert receipt["action_authorizations"]["leaf_sampling_for_genotyping"]["regulatory_status"] == "NOT_PLANNED"
