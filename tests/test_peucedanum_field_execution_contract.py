from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BITA_PEUCEDANUM_FIELD_EXECUTION_AND_PERMISSION_GATE_V1.md"
ADMIN = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_FIELD_ADMIN_READINESS_TEMPLATE_V1.json"
RUNTIME = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_FIELD_RUNTIME_ELIGIBILITY_LEDGER_V1.csv"

RUNTIME_FIELDS = (
    "site_code",
    "plot_code",
    "unit_id",
    "observation_date",
    "observation_time",
    "male_phase_complete",
    "perfect_available",
    "male_available",
    "total_available",
    "common_support_eligible",
    "q_assignment_locked",
    "q_target",
    "manipulation_start_time",
    "manipulation_end_time",
    "eggs_before_manipulation",
    "mechanical_damage_count",
    "operator_id",
    "plant_authorization_id",
    "egg_authorization_id",
    "land_access_authorization_id",
    "notes",
)


def test_field_contract_keeps_biological_and_administrative_readiness_separate() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "BIOLOGICALLY_READY_FOR_TECHNICAL_PILOT" in text
    assert "ADMINISTRATIVELY_READY_FOR_FIELD_MANIPULATION" in text
    assert "HA exact park zone: NOT YET VERIFIED" in text
    assert "Peucedanum multivittatum" in text
    assert "No. 565" in text
    assert "ZONE_AND_AUTHORITY_DEPENDENT" in text
    assert "NOT_REQUIRED_CONFIRMED_BY_AUTHORITY" in text


def test_admin_template_is_fail_closed_for_every_planned_intervention() -> None:
    config = json.loads(ADMIN.read_text(encoding="utf-8"))
    assert config["exact_site_coordinates_verified"] == "REQUIRED_BEFORE_USE"
    assert config["national_park_zone"] == "REQUIRED_BEFORE_USE"
    assert config["plant_q_manipulation"]["planned"] is True
    assert config["plant_q_manipulation"]["regulatory_status"] == "REQUIRED_BEFORE_USE"
    assert config["leaf_sampling_for_genotyping"]["regulatory_status"] == "REQUIRED_BEFORE_USE"
    assert config["predator_egg_removal"]["regulatory_status"] == "REQUIRED_BEFORE_USE"
    assert config["other_required_authorizations_checked"] == "REQUIRED_BEFORE_USE"


def test_runtime_eligibility_ledger_has_exact_registered_header() -> None:
    with RUNTIME.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == RUNTIME_FIELDS
