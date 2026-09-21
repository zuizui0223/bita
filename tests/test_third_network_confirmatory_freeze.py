from copy import deepcopy
import json
from pathlib import Path

from scripts.validate_third_network_confirmatory_freeze import validate

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "THIRD_NETWORK_CONFIRMATORY_FREEZE_RECEIPT_TEMPLATE_V1.json"
)


def _ready_receipt() -> dict[str, object]:
    receipt = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    receipt["site_selection"]["final_sites"] = ["S1", "S2"]
    receipt["site_selection"]["final_plant_species"] = ["P1", "P2", "P3", "P4", "P5"]
    receipt["site_selection"]["selection_basis"] = "pre-route ecology + permits + flowering"
    receipt["visitor_identification"]["protocol_version"] = "ID_V1"
    receipt["morphology"]["plant_protocol_version"] = "PLANT_MORPH_V1"
    receipt["morphology"]["mammal_protocol_version"] = "MAMMAL_MORPH_V1"
    receipt["camera_effort"]["rule"] = "fixed camera-hours per plant x site"
    receipt["permissions"]["land_access"] = "RESOLVED"
    receipt["permissions"]["animal_capture_or_handling"] = "RESOLVED"
    receipt["permissions"]["plant_measurement_or_collection"] = "RESOLVED"
    receipt["freeze_time_utc"] = "2026-09-21T00:00:00Z"
    receipt["frozen_by"] = "author"
    return receipt


def test_template_is_fail_closed() -> None:
    result = validate(json.loads(TEMPLATE.read_text(encoding="utf-8")))
    assert result["status"] == "BLOCKED"
    assert "final_sites_not_frozen" in result["failures"]
    assert "camera_effort_rule_not_frozen" in result["failures"]


def test_complete_route_blind_receipt_passes() -> None:
    result = validate(_ready_receipt())
    assert result["status"] == "READY_FOR_CONFIRMATORY_VIDEO_OPEN"
    assert result["failures"] == []


def test_pilot_route_presence_cannot_select_sites() -> None:
    receipt = _ready_receipt()
    receipt["site_selection"]["pilot_B_or_L_presence_used_for_selection"] = True
    result = validate(receipt)
    assert result["status"] == "BLOCKED"
    assert "pilot_route_used_for_selection" in result["failures"]


def test_camera_effort_cannot_adapt_to_route_outcome() -> None:
    receipt = _ready_receipt()
    receipt["camera_effort"]["may_extend_based_on_route_outcomes"] = True
    result = validate(receipt)
    assert result["status"] == "BLOCKED"
    assert "outcome_adaptive_camera_effort_forbidden" in result["failures"]
