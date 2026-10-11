from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZENODO = ROOT / "submission/access_routing_archive/ZENODO_METADATA_TEMPLATE.md"
CHECKLIST = ROOT / "submission/access_routing_archive/DEPOSIT_CHECKLIST_V1.md"
STATUS = ROOT / "docs/PUBLICATION_STATUS.md"


def test_zenodo_description_uses_supported_route_rate_interpretation():
    description = ZENODO.read_text(encoding="utf-8")
    assert "descriptive ratio of their separately fitted rate ratios is 5.311" in description
    assert "different positive-margin opportunity supports" in description
    assert "not a common-risk-set substitution effect" in description
    assert "individual birds were not tracked" in description
    assert "robbery is retained relative to legitimate feeding by a factor" not in description


def test_release_checklist_does_not_promote_observational_ratio_to_substitution():
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "descriptive ratio of separately fitted robbery/legitimate RRs 5.311" in checklist
    assert "not a common-risk-set substitution factor" in checklist
    assert "upload to the reserved Zenodo draft" in checklist.lower()
    assert "publish and verify" in checklist.lower()


def test_publication_status_retains_external_gates_and_species_level_claim():
    status = STATUS.read_text(encoding="utf-8")
    assert "not proof that" in status
    assert "a causal buffering or individual tactic-switching mechanism has" in status
    assert "different positive-margin support sets" in status
    assert "ACCESS_ROUTING_ARCHIVE_DOI = NOT_YET_RESERVED" in status
    assert "ZENODO_ACCESS_TOKEN_GITHUB_SECRET = MISSING_CONFIRMED" in status
    assert "EXTERNAL_SUBMISSION = BLOCKED" in status
