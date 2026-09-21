from __future__ import annotations

import csv

import pytest

from scripts.evaluate_third_network_collaboration_response import evaluate_rows, run


def _row(**updates: str) -> dict[str, str]:
    row = {
        "response_id": "R1",
        "source_contact": "collaborator",
        "response_date": "2026-09-21",
        "candidate_site_id": "S1",
        "candidate_region": "Cape",
        "plant_species": "Protea_a",
        "mammal_species": "Mammal_a",
        "flowering_window": "winter",
        "camera_feasible": "YES",
        "plant_depth_feasible": "YES",
        "mammal_morph_source_available": "YES",
        "land_permit_path_known": "YES",
        "ethics_path_known": "YES",
        "collaboration_interest": "YES",
        "outcome_exposure_status": "CLEAN",
        "exposure_scope_id": "",
        "notes_route_blind": "route-blind logistics only",
    }
    row.update(updates)
    return row


def test_clean_response_yields_route_blind_candidate_pool() -> None:
    result = evaluate_rows([_row()])
    assert result["status"] == "ROUTE_BLIND_COLLABORATION_POOL_AVAILABLE"
    assert result["candidate_sites_clean"] == ["S1"]
    assert result["route_blind_logistically_ready_sites"] == ["S1"]
    assert result["quarantine"]["system_exposed"] is False


def test_site_exposure_permanently_removes_site_from_clean_pool() -> None:
    result = evaluate_rows(
        [
            _row(response_id="R1"),
            _row(
                response_id="R2",
                candidate_site_id="S2",
                outcome_exposure_status="SITE_EXPOSED",
                exposure_scope_id="S2",
            ),
        ]
    )
    assert "S2" not in result["candidate_sites_clean"]
    assert result["quarantine"]["exposed_sites"] == ["S2"]


def test_plant_and_mammal_exposure_remove_entities() -> None:
    result = evaluate_rows(
        [
            _row(
                response_id="R1",
                plant_species="Protea_x",
                outcome_exposure_status="PLANT_EXPOSED",
                exposure_scope_id="Protea_x",
            ),
            _row(
                response_id="R2",
                mammal_species="Mammal_x",
                outcome_exposure_status="MAMMAL_EXPOSED",
                exposure_scope_id="Mammal_x",
            ),
        ]
    )
    assert "Protea_x" not in result["candidate_plants_clean"]
    assert "Mammal_x" not in result["candidate_mammals_clean"]


def test_system_exposure_blocks_current_confirmatory_lane() -> None:
    result = evaluate_rows(
        [_row(outcome_exposure_status="SYSTEM_EXPOSED")]
    )
    assert result["status"] == "SYSTEM_OUTCOME_EXPOSED_CONFIRMATORY_LANE_BLOCKED"
    assert result["candidate_sites_clean"] == []


def test_entity_exposure_requires_scope_identifier() -> None:
    with pytest.raises(ValueError, match="requires exposure_scope_id"):
        evaluate_rows([_row(outcome_exposure_status="SITE_EXPOSED")])


def test_non_schema_outcome_column_is_rejected(tmp_path) -> None:
    path = tmp_path / "response.csv"
    row = _row()
    fields = list(row) + ["robbery_rate"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({**row, "robbery_rate": ""})
    with pytest.raises(ValueError, match="non-schema columns"):
        run(path)
