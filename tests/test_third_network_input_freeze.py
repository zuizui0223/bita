from __future__ import annotations

import csv
import hashlib
import json

import pytest

from scripts.build_third_access_routing_units import run as build_units_run
from scripts.freeze_third_network_confirmatory_inputs import (
    freeze_inputs,
    write_manifest,
)
from scripts.evaluate_third_network_route_reliability import expected_double_code_ids


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _freeze_receipt() -> dict:
    return {
        "receipt": "BITA_THIRD_NETWORK_CONFIRMATORY_FREEZE_V1",
        "status": "REQUIRED_BEFORE_CONFIRMATORY_VIDEO_OPEN",
        "parent_prereg_commit": "ae98e496a99fa7f5b333bbe7881025d13a8d8768",
        "design_system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "site_selection": {
            "final_sites": ["S1"],
            "final_plant_species": ["P0", "P1", "P2", "P3", "P4"],
            "route_outcome_blind": True,
            "pilot_B_or_L_presence_used_for_selection": False,
            "selection_basis": "route-blind presurvey",
        },
        "visitor_identification": {
            "protocol_version": "ID_V1",
            "minimum_confidence": "MEDIUM",
        },
        "morphology": {
            "plant_protocol_version": "PLANT_V1",
            "mammal_protocol_version": "MAMMAL_V1",
            "plant_primary_trait": "legitimate_nectar_access_depth_mm",
            "mammal_primary_trait": "functional_rostral_reach_mm",
        },
        "route_coding": {
            "manual": "THIRD_NETWORK_ROUTE_CODING_MANUAL_V1",
            "coders_blind_to_P_V_M": True,
            "double_code_fraction_minimum": 0.2,
            "target_kappa_LBAN": 0.8,
        },
        "camera_effort": {
            "rule": "fixed effort v1",
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
        "claim": "test",
    }


def _fixture(tmp_path):
    events = tmp_path / "events.csv"
    plants = tmp_path / "plant_traits.csv"
    mammals = tmp_path / "mammal_traits.csv"
    cameras = tmp_path / "camera_deployment.csv"
    freeze = tmp_path / "confirmatory_freeze.json"
    field = tmp_path / "field_readiness.json"
    manifest = tmp_path / "input_freeze.json"
    units = tmp_path / "units.csv"
    audit = tmp_path / "audit.json"

    event_rows = []
    event = 0
    for p in range(5):
        for m in range(5):
            event += 1
            event_rows.append(
                {
                    "event_id": f"E{event:03d}",
                    "dataset_role": "CONFIRMATORY",
                    "site_id": "S1",
                    "plant_species": f"P{p}",
                    "mammal_species": f"M{m}",
                    "timestamp": "2027-03-01T00:00:00Z",
                    "camera_id": f"C{p}",
                    "route_code": "B" if p > m else "L",
                    "visitor_id_confidence": "HIGH",
                    "clip_quality": "PASS",
                }
            )
    selected = expected_double_code_ids(event_rows)
    for row in event_rows:
        row["coder_id"] = "PRIMARY"
        row["double_coded"] = "true" if row["event_id"] in selected else "false"
        row["second_route_code"] = row["route_code"] if row["event_id"] in selected else ""

    _write_csv(
        events,
        [
            "event_id",
            "dataset_role",
            "site_id",
            "plant_species",
            "mammal_species",
            "timestamp",
            "camera_id",
            "route_code",
            "visitor_id_confidence",
            "clip_quality",
            "coder_id",
            "double_coded",
            "second_route_code",
        ],
        event_rows,
    )

    plant_rows = []
    for p in range(5):
        for rep in (1, 2):
            plant_rows.append(
                {
                    "site_id": "S1",
                    "plant_species": f"P{p}",
                    "inflorescence_id": f"I{p}",
                    "access_depth_mm": str(20 + p + rep / 10),
                    "repeat_index": str(rep),
                }
            )
    _write_csv(
        plants,
        [
            "site_id",
            "plant_species",
            "inflorescence_id",
            "access_depth_mm",
            "repeat_index",
        ],
        plant_rows,
    )

    mammal_rows = []
    for m in range(5):
        for rep in (1, 2):
            mammal_rows.append(
                {
                    "mammal_species": f"M{m}",
                    "individual_id": f"IND{m}",
                    "rostral_reach_mm": str(12 + m + rep / 10),
                    "repeat_index": str(rep),
                }
            )
    _write_csv(
        mammals,
        [
            "mammal_species",
            "individual_id",
            "rostral_reach_mm",
            "repeat_index",
        ],
        mammal_rows,
    )

    camera_rows = []
    for p in range(5):
        camera_rows.append(
            {
                "deployment_id": f"D{p}",
                "site_id": "S1",
                "plant_species": f"P{p}",
                "camera_id": f"C{p}",
                "planned_start_utc": "2027-03-01T00:00:00Z",
                "planned_end_utc": "2027-03-06T00:00:00Z",
                "planned_camera_hours": "120",
                "camera_angle": "PRIMARY",
                "dataset_role": "CONFIRMATORY",
                "effort_rule_version": "EFFORT_V1",
                "route_outcome_adaptive": "false",
            }
        )
    _write_csv(
        cameras,
        [
            "deployment_id",
            "site_id",
            "plant_species",
            "camera_id",
            "planned_start_utc",
            "planned_end_utc",
            "planned_camera_hours",
            "camera_angle",
            "dataset_role",
            "effort_rule_version",
            "route_outcome_adaptive",
        ],
        camera_rows,
    )

    freeze.write_text(json.dumps(_freeze_receipt()), encoding="utf-8")
    freeze_sha = _sha(freeze)
    field.write_text(
        json.dumps(
            {
                "receipt_schema_version": "BITA_THIRD_NETWORK_FIELD_READINESS_V1",
                "system": "CAPE_SMALL_MAMMAL_X_PROTEA",
                "status": "THIRD_NETWORK_FIELD_EXECUTION_READY",
                "gates": {
                "site_locations_verified_privately": True,
                "route_blind_presurvey_checksum_matches": True,
                "route_blind_presurvey_ready": True,
                "route_and_morphology_fields_absent_from_presurvey": True,
                "final_sites_supported_by_route_blind_presurvey": True,
                "confirmatory_freeze_receipt_checksum_matches": True,
                "confirmatory_freeze_receipt_ready": True,
                "land_site_access_resolved": True,
                "camera_deployment_resolved": True,
                "plant_morphology_measurement_resolved": True,
                "plant_tissue_collection_resolved_or_not_planned": True,
                "mammal_capture_or_handling_resolved_or_not_planned": True,
                "animal_ethics_or_institutional_review_resolved": True,
                "mammal_morphology_mode_predeclared": True,
                "mammal_morphology_same_regional_assemblage_supported": True,
                "other_required_authorizations_checked": True,
            },
                "confirmatory_freeze_receipt": {
                    "expected_sha256": freeze_sha,
                    "actual_sha256": freeze_sha,
                    "validator_status": "READY_FOR_CONFIRMATORY_VIDEO_OPEN",
                    "validator_failures": [],
                    "final_sites": ["S1"],
                },
            }
        ),
        encoding="utf-8",
    )

    return {
        "events": events,
        "plants": plants,
        "mammals": mammals,
        "cameras": cameras,
        "freeze": freeze,
        "field": field,
        "manifest": manifest,
        "units": units,
        "audit": audit,
    }


def _freeze(paths):
    manifest = freeze_inputs(
        events_csv=paths["events"],
        plant_traits_csv=paths["plants"],
        mammal_traits_csv=paths["mammals"],
        camera_deployment_csv=paths["cameras"],
        confirmatory_freeze_json=paths["freeze"],
        field_readiness_json=paths["field"],
    )
    write_manifest(paths["manifest"], manifest)
    return manifest


def test_frozen_inputs_can_be_joined_only_with_matching_manifest(tmp_path) -> None:
    paths = _fixture(tmp_path)
    manifest = _freeze(paths)
    assert manifest["status"] == "INPUTS_FROZEN_READY_FOR_JOIN"

    audit = build_units_run(
        paths["events"],
        paths["plants"],
        paths["mammals"],
        paths["manifest"],
        paths["units"],
        paths["audit"],
    )
    assert audit["analysis_units"] == 25
    assert "input_freeze" in audit
    assert paths["units"].exists()


def test_postfreeze_event_edit_blocks_join(tmp_path) -> None:
    paths = _fixture(tmp_path)
    _freeze(paths)

    with paths["events"].open("a", encoding="utf-8") as handle:
        handle.write("\n")

    with pytest.raises(ValueError, match="FROZEN_INPUT_HASH_MISMATCH: events"):
        build_units_run(
            paths["events"],
            paths["plants"],
            paths["mammals"],
            paths["manifest"],
            paths["units"],
            paths["audit"],
        )


def test_outcome_adaptive_camera_effort_is_rejected_before_freeze(tmp_path) -> None:
    paths = _fixture(tmp_path)
    text = paths["cameras"].read_text(encoding="utf-8")
    paths["cameras"].write_text(text.replace(",false\n", ",true\n", 1), encoding="utf-8")

    with pytest.raises(ValueError, match="OUTCOME_ADAPTIVE_CAMERA_EFFORT_FORBIDDEN"):
        _freeze(paths)


def test_field_readiness_must_be_ready_before_input_freeze(tmp_path) -> None:
    paths = _fixture(tmp_path)
    field = json.loads(paths["field"].read_text(encoding="utf-8"))
    field["status"] = "THIRD_NETWORK_FIELD_EXECUTION_BLOCKED"
    paths["field"].write_text(json.dumps(field), encoding="utf-8")

    with pytest.raises(ValueError, match="FIELD_READINESS_NOT_READY"):
        _freeze(paths)


def test_status_only_field_readiness_receipt_is_rejected(tmp_path) -> None:
    paths = _fixture(tmp_path)
    paths["field"].write_text(
        json.dumps({"status": "THIRD_NETWORK_FIELD_EXECUTION_READY"}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="INVALID_THIRD_NETWORK_FIELD_READINESS_RECEIPT"):
        _freeze(paths)


def test_field_readiness_must_bind_exact_confirmatory_freeze(tmp_path) -> None:
    paths = _fixture(tmp_path)
    field = json.loads(paths["field"].read_text(encoding="utf-8"))
    field["confirmatory_freeze_receipt"]["actual_sha256"] = "0" * 64
    paths["field"].write_text(json.dumps(field), encoding="utf-8")

    with pytest.raises(ValueError, match="FIELD_READINESS_FREEZE_HASH_MISMATCH"):
        _freeze(paths)


def test_camera_deployment_must_cover_every_frozen_plant(tmp_path) -> None:
    paths = _fixture(tmp_path)
    rows = list(csv.DictReader(paths["cameras"].open(encoding="utf-8")))
    rows = rows[:-1]
    _write_csv(paths["cameras"], list(rows[0]), rows)

    with pytest.raises(ValueError, match="does not cover every frozen plant species"):
        _freeze(paths)



def test_double_code_subset_cannot_be_selected_posthoc(tmp_path) -> None:
    paths = _fixture(tmp_path)
    rows = list(csv.DictReader(paths["events"].open(encoding="utf-8")))
    selected = [row for row in rows if row["double_coded"] == "true"]
    unselected = [row for row in rows if row["double_coded"] == "false"]
    assert selected and unselected

    selected[0]["double_coded"] = "false"
    selected[0]["second_route_code"] = ""
    unselected[0]["double_coded"] = "true"
    unselected[0]["second_route_code"] = unselected[0]["route_code"]
    _write_csv(paths["events"], list(rows[0]), rows)

    with pytest.raises(ValueError, match="DOUBLE_CODE_SUBSET_MISMATCH"):
        _freeze(paths)


def test_low_route_coder_reliability_blocks_input_freeze(tmp_path) -> None:
    paths = _fixture(tmp_path)
    rows = list(csv.DictReader(paths["events"].open(encoding="utf-8")))
    flipped = 0
    for row in rows:
        if row["double_coded"] == "true":
            row["second_route_code"] = "B" if row["route_code"] != "B" else "L"
            flipped += 1
    assert flipped > 0
    _write_csv(paths["events"], list(rows[0]), rows)

    with pytest.raises(ValueError, match="ROUTE_RELIABILITY_NOT_READY"):
        _freeze(paths)
