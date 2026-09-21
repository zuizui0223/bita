from pathlib import Path

import pytest

pytestmark = pytest.mark.prose_contract

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_CAPE_COLLABORATION_ROUTE_V1.md"
EMAIL = ROOT / "submission" / "THIRD_NETWORK_CAPE_COLLABORATION_EMAIL_V1.md"
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"


def test_collaboration_route_preserves_outcome_blind_site_selection() -> None:
    text = ROUTE.read_text(encoding="utf-8")
    assert "HISTORICAL_ROUTE_OUTCOME_DISCLOSURE_BEFORE_SITE_FREEZE = NOT_REQUESTED" in text
    assert "do **not** ask collaborators" in text
    assert "unpublished B/L event counts" in text
    assert "route-blind feasibility" in text
    assert "If no collaboration can satisfy the frozen richness/schema gates, retain k=2" in text


def test_outreach_email_does_not_request_favorable_historical_outcomes() -> None:
    text = EMAIL.read_text(encoding="utf-8")
    assert "do not send automatically" in text
    assert "not** asking which species or sites have shown more destructive/bypass behavior" in text
    assert "5 mammal species, 5 plant species and 30 matched units" in text
    assert "planning target of at least 70 units" in text
    assert "If the eventual mammal result is null or opposite in sign, it remains the confirmatory third test." in text


def test_current_official_contact_shortlist_is_recorded() -> None:
    text = ROUTE.read_text(encoding="utf-8")
    for token in (
        "SteenhuisenS@ufs.ac.za",
        "jeremy.midgley@uct.ac.za",
        "c.peter@ru.ac.za",
        "JohnsonSd@ukzn.ac.za",
    ):
        assert token in text


def test_submission_scope_points_to_outcome_blind_collaboration_next_action() -> None:
    text = SCOPE.read_text(encoding="utf-8")
    assert "THIRD_NETWORK_CAPE_COLLABORATION_ROUTE_V1.md" in text
    assert "THIRD_NETWORK_CAPE_COLLABORATION_EMAIL_V1.md" in text
    assert "NEXT_EXTERNAL_ACTION = OUTCOME_BLIND_CAPE_COLLABORATION_INQUIRY" in text
    assert "COLLABORATION_EMAIL = DRAFT_AUTHOR_APPROVAL_REQUIRED" in text
    assert "\\n- `scripts/evaluate_third_network_route_blind_presurvey.py`" not in text



def test_collaboration_reply_quarantine_is_in_scope() -> None:
    scope = SCOPE.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")

    for token in (
        "THIRD_NETWORK_COLLABORATION_RESPONSE_INTAKE_SCHEMA_V1.csv",
        "THIRD_NETWORK_COLLABORATION_EXPOSURE_REGISTRY_V1.csv",
        "THIRD_NETWORK_COLLABORATION_INTAKE_PROTOCOL_V1.md",
        "evaluate_third_network_collaboration_intake.py",
        "COLLABORATION_REPLY_QUARANTINE = IMPLEMENTED",
    ):
        assert token in scope

    assert "site-specific historical route-outcome information" in route
    assert "that site is quarantined" in route
    assert "first route-blind feasible collaboration" in route
    assert "\\n- `empirical/floral_defence_selectivity/THIRD_NETWORK_COLLABORATION_EXPOSURE_REGISTRY_V1.csv`" not in scope
