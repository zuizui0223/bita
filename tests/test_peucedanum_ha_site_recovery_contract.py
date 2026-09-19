from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BITA_PEUCEDANUM_HA_SITE_RECOVERY_INQUIRY_V1.md"
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_HA_SITE_RECOVERY_TEMPLATE_V1.json"


def test_site_recovery_template_does_not_pretend_exact_ha_is_known() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "BITA_PEUCEDANUM_HA_SITE_RECOVERY_V1"
    assert payload["ha_exact_latitude"] == "REQUIRED_BEFORE_USE"
    assert payload["ha_exact_longitude"] == "REQUIRED_BEFORE_USE"
    assert payload["national_park_zone_if_known"] == "REQUIRED_BEFORE_USE"
    assert payload["permission_to_reuse_exact_site_for_new_project"] == "REQUIRED_BEFORE_USE"


def test_inquiry_packet_keeps_historical_and_current_authorization_separate() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "historical authorization information is a routing clue only" in text
    assert "current project permission must still be obtained separately" in text
    assert "Peucedanum multivittatum" in text
    assert "RO-KAMIKAWA@env.go.jp" in text
    assert "RO-HIGASHIKAWA@env.go.jp" in text
    assert "RO-KAMISHIHORO@env.go.jp" in text


def test_sensitive_coordinates_can_remain_out_of_public_repository() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Exact sensitive coordinates should not be committed to a public repository" in text
    assert "restricted_location_reference = private record ID" in text
    assert "move to HL" in text
