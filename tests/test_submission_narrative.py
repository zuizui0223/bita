from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_has_one_primary_claim_and_preliminary_context() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "one primary theory claim" in text
    assert "preliminary mechanism context" in text
    assert "two linked but unequal claims" not in text
    assert "second independent submission claim" in text


def test_manifest_does_not_promote_literature_to_claim_two() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "## Primary claim:" in text
    assert "## Preliminary literature context:" in text
    assert "## Claim 2:" not in text


def test_scope_keeps_assurance_auxiliary() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "**Auxiliary moderator:**" in text
    assert "reproductive assurance `R`" in text
    assert "background moderator" in text
    assert "not a third focal trait" in text


def test_final_audit_records_assurance_decision() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "16 of 1,296" in text
    assert "three-trait theory" in text
    assert "preliminary context only" in text
