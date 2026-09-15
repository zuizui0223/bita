from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / ".github" / "workflows" / "build-bita-mechanism-review-package.yml"
LEGACY = ROOT / ".github" / "workflows" / "build-identification-candidate-package.yml"
AUDIT = ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md"
CHECKLIST = ROOT / "submission" / "SUBMISSION_CHECKLIST.md"


def test_active_review_package_is_pull_request_gated_and_submission_facing() -> None:
    text = ACTIVE.read_text(encoding="utf-8")

    assert text.startswith("name: Build BITA mechanism review package\n")
    assert "  pull_request:\n" in text
    assert "name: bita-mechanism-identification-review-package" in text
    assert 'if [ "$MAIN_PAGES" -gt 30 ]; then' in text
    assert "package_role=active_reader_facing" in text
    assert "active_submission=true" in text
    assert "legacy_candidate=false" in text
    assert "old_identification_candidate=legacy_provenance_only" in text


def test_old_identification_candidate_is_explicitly_legacy() -> None:
    text = LEGACY.read_text(encoding="utf-8")

    assert text.startswith("name: LEGACY - build identification candidate package\n")
    assert "name: legacy-identification-candidate-package" in text
    assert "package_role=provenance_regression_only" in text
    assert "legacy_candidate=true" in text
    assert "active_submission=false" in text
    assert "name: identification-candidate-package\n" not in text


def test_submission_docs_name_the_active_package_as_source_of_truth() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")

    for text in (audit, checklist):
        assert "bita-mechanism-identification-review-package" in text
        assert "PACKAGE_QA_RECEIPT.txt" in text
        assert "legacy-identification-candidate-package" in text
