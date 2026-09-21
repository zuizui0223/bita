from __future__ import annotations

import hashlib
import json

import pytest

from scripts.evaluate_third_network_field_readiness import (
    BLOCKED_STATUS,
    READY_STATUS,
    SCHEMA,
    evaluate,
)
from scripts.evaluate_third_network_route_blind_presurvey import evaluate_rows


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ready_freeze() -> dict:
    return {
        "receipt": "BITA_THIRD_NETWORK_CONFIRMATORY_FREEZE_V1",
        "status": "REQUIRED_BEFORE_CONFIRMATORY_VIDEO_OPEN",
        "parent_prereg_commit": "ae98e496a99fa7f5b333bbe7881025d13a8d8768",
        "design_system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "site_selection": {
            "final_sites": ["S1"],
            "final_plant_species": ["P0", "P1", "P2", "P3", "P4"],
            "final_mammal_species": ["M0", "M1", "M2", "M3", "M4"],
            "final_site_plant_pairs": [
                {"site_id": "S1", "plant_species": f"P{i}"} for i in range(5)
            ],
            "route_outcome_blind": True,
            "pilot_B_or_L_presence_used_for_selection": False,
            "selection_basis": "route-blind presurvey + permits + flowering",
        },
        "visitor_identification": {
            "protocol_version": "ID_V1",
            "minimum_confidence": "MEDIUM",
        },
        "morphology": {
            "plant_protocol_version": "PLANT_MORPH_V1",
            "mammal_protocol_version": "MAMMAL_MORPH_V1",
            "plant_primary_trait": "legitimate_nectar_access_depth_mm",
            "mammal_primary_trait": "functional_rostral_reach_mm",
        },
        "route_coding": {
            "manual": "THIRD_NETWORK_ROUTE_CODING_MANUAL_V1",
            "coders_blind_to_P_V_M": True,
            "double_code_fraction_minimum": 0.2,
            "target_kappa_LBAN": 0.8,
            "double_code_subset_seed": 20260922,
            "double_code_selection_method": "SEEDED_RANDOM_SAMPLE_OF_NON_N_EVENT_IDS",
        },
        "camera_effort": {
            "rule": "fixed 120 camera-hours per plant x site",
            "rule_version": "EFFORT_V1",
            "may_extend_based_on_route_outcomes": False,
        },
        "analysis": {
            "third_network_seed": 20260921,
            "k3_joint_seed": 20260921,
            "permutations": 9999,
            "minimum_units": 30,
            "minimum_mammal_species": 5,
            "minimum_plant_species": 5,
            "planning_target_units": 70,
        },
        "permissions": {
            "land_access": "RESOLVED",
            "animal_capture_or_handling": "NOT_PLANNED",
            "plant_measurement_or_collection": "RESOLVED",
        },
        "freeze_time_utc": "2027-01-01T00:00:00Z",
        "frozen_by": "author",
        "claim": "test fixture",
    }


def _presurvey_rows() -> list[dict[str, str]]:
    rows = []
    for p in range(5):
        rows.append(
            {
                "record_id": f"P{p}",
                "site_id": "S1",
                "record_type": "PLANT",
                "plant_species": f"P{p}",
                "mammal_species": "",
                "evidence_method": "route-blind flowering survey",
                "flowering_available": "YES",
                "camera_operable": "NA",
            }
        )
    for m in range(5):
        rows.append(
            {
                "record_id": f"M{m}",
                "site_id": "S1",
                "record_type": "MAMMAL",
                "plant_species": "",
                "mammal_species": f"M{m}",
                "evidence_method": "independent mammal survey",
                "flowering_available": "NA",
                "camera_operable": "NA",
            }
        )
    rows.append(
        {
            "record_id": "C1",
            "site_id": "S1",
            "record_type": "CAMERA",
            "plant_species": "",
            "mammal_species": "",
            "evidence_method": "camera test",
            "flowering_available": "NA",
            "camera_operable": "YES",
        }
    )
    return rows


def _action(planned: bool = True) -> dict:
    if not planned:
        return {"planned": False}
    return {
        "planned": True,
        "regulatory_status": "PERMITTED",
        "evidence_reference": "AUTH-001",
        "authorization_valid_from": "2027-01-01",
        "authorization_valid_until": "2027-12-31",
    }


def _config(tmp_path) -> dict:
    freeze_path = tmp_path / "freeze.json"
    freeze_path.write_text(json.dumps(_ready_freeze()), encoding="utf-8")

    presurvey_path = tmp_path / "presurvey_receipt.json"
    presurvey_path.write_text(
        json.dumps(evaluate_rows(_presurvey_rows())),
        encoding="utf-8",
    )

    return {
        "schema_version": SCHEMA,
        "system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "planned_field_start": "2027-03-01",
        "planned_field_end": "2027-05-31",
        "site_locations_verified_privately": True,
        "site_location_receipt_reference": "PRIVATE-SITE-RECEIPT-001",
        "route_blind_presurvey": {
            "receipt_path": presurvey_path.name,
            "sha256": _sha(presurvey_path),
        },
        "confirmatory_freeze_receipt": {
            "path": freeze_path.name,
            "sha256": _sha(freeze_path),
        },
        "land_site_access": _action(),
        "camera_deployment": _action(),
        "plant_morphology_measurement": _action(),
        "plant_tissue_collection": _action(False),
        "mammal_capture_or_handling": _action(False),
        "mammal_morphology_source": {
            "mode": "INDEPENDENT_MORPHOMETRIC_DATA",
            "evidence_reference": "MORPH-001",
            "same_regional_assemblage_supported": True,
        },
        "animal_ethics_or_institutional_review": _action(),
        "other_required_authorizations_checked": True,
    }


def test_all_resolved_route_blind_inputs_promote_field_execution(tmp_path) -> None:
    config = _config(tmp_path)
    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == READY_STATUS
    assert all(result["gates"].values())


def test_freeze_site_must_be_supported_by_route_blind_presurvey(tmp_path) -> None:
    config = _config(tmp_path)
    freeze_path = tmp_path / config["confirmatory_freeze_receipt"]["path"]
    freeze = json.loads(freeze_path.read_text())
    freeze["site_selection"]["final_sites"] = ["S2"]
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
    config["confirmatory_freeze_receipt"]["sha256"] = _sha(freeze_path)

    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == BLOCKED_STATUS
    assert result["gates"]["final_sites_supported_by_route_blind_presurvey"] is False


def test_presurvey_checksum_mismatch_blocks_execution(tmp_path) -> None:
    config = _config(tmp_path)
    config["route_blind_presurvey"]["sha256"] = "0" * 64
    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == BLOCKED_STATUS
    assert result["gates"]["route_blind_presurvey_checksum_matches"] is False


def test_expired_camera_authorization_blocks_execution(tmp_path) -> None:
    config = _config(tmp_path)
    config["camera_deployment"]["authorization_valid_until"] = "2027-03-15"
    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == BLOCKED_STATUS
    assert result["gates"]["camera_deployment_resolved"] is False


def test_capture_can_be_not_planned_without_weakening_morphology_gate(tmp_path) -> None:
    config = _config(tmp_path)
    result = evaluate(config, base_dir=tmp_path)
    assert result["action_authorizations"]["mammal_capture_or_handling"]["regulatory_status"] == "NOT_PLANNED"
    assert result["gates"]["mammal_morphology_mode_predeclared"] is True
    assert result["gates"]["mammal_morphology_same_regional_assemblage_supported"] is True


def test_template_like_placeholder_fails_closed(tmp_path) -> None:
    config = _config(tmp_path)
    config["planned_field_start"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="must be resolved"):
        evaluate(config, base_dir=tmp_path)



def test_final_plant_and_mammal_lists_must_come_from_route_blind_presurvey(tmp_path) -> None:
    config = _config(tmp_path)
    freeze_path = tmp_path / config["confirmatory_freeze_receipt"]["path"]
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    freeze["site_selection"]["final_plant_species"] = ["P0", "P1", "P2", "P3", "P_OUTSIDE"]
    freeze["site_selection"]["final_mammal_species"] = ["M0", "M1", "M2", "M3", "M_OUTSIDE"]
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
    config["confirmatory_freeze_receipt"]["sha256"] = _sha(freeze_path)

    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == BLOCKED_STATUS
    assert result["gates"]["final_plants_supported_by_route_blind_presurvey"] is False
    assert result["gates"]["final_mammals_supported_by_route_blind_presurvey"] is False



def test_final_site_plant_pairs_must_be_route_blind_presurvey_pairs(tmp_path) -> None:
    config = _config(tmp_path)
    freeze_path = tmp_path / config["confirmatory_freeze_receipt"]["path"]
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    freeze["site_selection"]["final_plant_species"] = ["P0", "P1", "P2", "P3", "P_OUTSIDE"]
    freeze["site_selection"]["final_site_plant_pairs"] = [
        {"site_id": "S1", "plant_species": value}
        for value in freeze["site_selection"]["final_plant_species"]
    ]
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
    config["confirmatory_freeze_receipt"]["sha256"] = _sha(freeze_path)

    result = evaluate(config, base_dir=tmp_path)
    assert result["status"] == BLOCKED_STATUS
    assert result["gates"]["final_site_plant_pairs_supported_by_route_blind_presurvey"] is False
