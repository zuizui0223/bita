from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_TITLE = (
    "Trait interaction is not ecological mechanism: "
    "an identification framework for multifunctional traits"
)
OLD_ARCH_TITLE = (
    "When does a trait trade-off resolve by differentiation rather than compromise? "
    "Linking trait architecture to mechanism identification"
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_submission_facing_documents_share_active_identity() -> None:
    supplement = _read("SUPPLEMENT_MANIFEST.md")
    portal = _read("submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md")
    strategy = _read("submission/TARGET_JOURNAL_STRATEGY.md")
    audit = _read("submission/MANUSCRIPT_AUDIT_V2.md")
    ledger = _read("docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md")

    for text in (supplement, portal, strategy, audit, ledger):
        assert ACTIVE_TITLE in text

    assert f"- Final title: **{ACTIVE_TITLE}**" in portal
    assert "The active BITA manuscript is:" in strategy
    assert "Canonical title:" in audit
    assert "17 high-information systems" in supplement
    assert "17 high-information systems" in portal
    assert "17 high-information systems" in audit
    assert "17-system high-information audit" in ledger


def test_active_package_receipt_is_the_reader_facing_source_of_truth() -> None:
    supplement = _read("SUPPLEMENT_MANIFEST.md")
    portal = _read("submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md")
    strategy = _read("submission/TARGET_JOURNAL_STRATEGY.md")
    audit = _read("submission/MANUSCRIPT_AUDIT_V2.md")
    ledger = _read("docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md")

    for text in (supplement, portal, strategy, audit, ledger):
        assert "PACKAGE_QA_RECEIPT.txt" in text

    for text in (supplement, portal, strategy, audit, ledger):
        assert "bita-mechanism-identification-review-package" in text

    assert "Main Document: 21 pages" in supplement
    assert "Appendix S1:   10 pages" in supplement
    assert "Main Document: 21 pages" in audit
    assert "Appendix S1:   10 pages" in audit
    assert "main_pages=21" in ledger
    assert "appendix_pages=10" in ledger


def test_stale_submission_states_cannot_be_promoted_back_to_current() -> None:
    supplement = _read("SUPPLEMENT_MANIFEST.md")
    portal = _read("submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md")
    strategy = _read("submission/TARGET_JOURNAL_STRATEGY.md")
    audit = _read("submission/MANUSCRIPT_AUDIT_V2.md")
    ledger = _read("docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md")

    assert f"Canonical target:\n\n> **{OLD_ARCH_TITLE}**" not in supplement
    assert f"- Final title: **{OLD_ARCH_TITLE}**" not in portal
    assert "The canonical manuscript is now the integrated SCH-sister Chapter 2" not in strategy
    assert "The 16-system audit is interpreted as" not in audit
    assert "| 16-system identification audit |" not in ledger

    assert "Main Document: 29 pages" not in audit
    assert "Appendix S1:   12 pages" not in audit
    assert "rendered at current scientific head; 30 pages" not in ledger
    assert "renders to 30 pages" not in ledger


def test_old_architecture_programme_is_only_provenance_in_submission_docs() -> None:
    supplement = _read("SUPPLEMENT_MANIFEST.md")
    portal = _read("submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md")
    strategy = _read("submission/TARGET_JOURNAL_STRATEGY.md")
    audit = _read("submission/MANUSCRIPT_AUDIT_V2.md")
    ledger = _read("docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md")

    # Historical material can remain reproducible, but every submission-facing
    # document must explicitly demote it below the active mechanism paper.
    assert "Historical/provenance" in supplement
    assert "Historical provenance" in portal
    assert "historical/provenance" in strategy
    assert "Historical/provenance" in audit
    assert "Historical/provenance" in ledger
