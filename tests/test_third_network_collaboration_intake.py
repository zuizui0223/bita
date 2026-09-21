from __future__ import annotations

import csv

import pytest

from scripts.evaluate_third_network_collaboration_intake import evaluate, run


def _intake(
    response_id: str = "R1",
    site: str = "S1",
    received: str = "2026-09-21T03:00:00Z",
    exposed: str = "NONE",
) -> dict[str, str]:
    return {
        "response_id": response_id,
        "contact_id": "C1",
        "received_utc": received,
        "candidate_site_id": site,
        "region": "Western Cape",
        "flowering_plant_species_count": "6",
        "mammal_species_count": "6",
        "flowering_window": "March-May",
        "camera_feasible": "YES",
        "plant_access_depth_feasible": "YES",
        "mammal_rostral_morphometrics_feasible": "YES",
        "land_permit_ethics_path_identified": "YES",
        "collaboration_interest": "YES",
        "outcome_exposure_flag": exposed,
    }


def _site_exposure(response_id: str = "R1", site: str = "S1") -> dict[str, str]:
    return {
        "exposure_id": "E1",
        "response_id": response_id,
        "exposure_level": "SITE",
        "site_id": site,
        "plant_species": "",
        "mammal_species": "",
        "recorded_without_direction": "true",
        "required_action": "QUARANTINE_SITE",
    }


def test_first_route_blind_feasible_reply_is_selected() -> None:
    later = _intake("R2", "S2", "2026-09-21T04:00:00Z")
    earlier = _intake("R1", "S1", "2026-09-21T03:00:00Z")
    result = evaluate([later, earlier], [])
    assert result["status"] == "ROUTE_BLIND_COLLABORATION_SELECTED"
    assert result["selected_response"]["response_id"] == "R1"
    assert "historically more favorable" in result["stopping_rule"]


def test_site_specific_outcome_exposure_quarantines_site() -> None:
    exposed = _intake("R1", "S1", exposed="EXPOSED")
    clean = _intake("R2", "S2", "2026-09-21T04:00:00Z")
    result = evaluate([exposed, clean], [_site_exposure()])
    assert result["site_quarantine"] == ["S1"]
    assert result["selected_response"]["response_id"] == "R2"
    r1 = next(row for row in result["responses"] if row["response_id"] == "R1")
    assert r1["site_quarantined"] is True
    assert r1["route_blind_feasible"] is False


def test_taxon_exposure_forces_no_cherry_picking_without_quarantining_site() -> None:
    intake = _intake("R1", "S1", exposed="EXPOSED")
    exposure = {
        "exposure_id": "E1",
        "response_id": "R1",
        "exposure_level": "PLANT",
        "site_id": "",
        "plant_species": "Protea_x",
        "mammal_species": "",
        "recorded_without_direction": "true",
        "required_action": "NO_TAXON_CHERRY_PICKING",
    }
    result = evaluate([intake], [exposure])
    assert result["taxon_exposure_requires_no_cherry_picking"] is True
    assert result["site_quarantine"] == []
    assert result["selected_response"]["response_id"] == "R1"


def test_exposure_registry_must_not_record_direction() -> None:
    intake = _intake("R1", "S1", exposed="EXPOSED")
    exposure = _site_exposure()
    exposure["recorded_without_direction"] = "false"
    with pytest.raises(ValueError, match="EXPOSURE_DIRECTION_MUST_NOT_BE_RECORDED"):
        evaluate([intake], [exposure])


def test_exposed_flag_requires_registry_row() -> None:
    with pytest.raises(ValueError, match="EXPOSED response requires exposure registry row"):
        evaluate([_intake(exposed="EXPOSED")], [])


def test_forbidden_outcome_column_is_rejected(tmp_path) -> None:
    intake_path = tmp_path / "intake.csv"
    exposure_path = tmp_path / "exposure.csv"

    row = _intake()
    fields = list(row) + ["robbery_rate"]
    with intake_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({**row, "robbery_rate": ""})

    exposure_fields = [
        "exposure_id",
        "response_id",
        "exposure_level",
        "site_id",
        "plant_species",
        "mammal_species",
        "recorded_without_direction",
        "required_action",
    ]
    with exposure_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=exposure_fields)
        writer.writeheader()

    with pytest.raises(ValueError, match="ROUTE_OUTCOME_COLUMN_FORBIDDEN"):
        run(intake_path, exposure_path)
