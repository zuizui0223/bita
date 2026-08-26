from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_integrated_theory_and_empirical_synthesis() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "fixed theoretical core" in text
    assert "mechanism-pattern empirical synthesis" in text
    assert "recurrent constituent mechanisms" in text
    assert "context-dependent" in text
    assert "unidentified rather than zero" in text or "unidentified, not zero" in text
    assert "route counts are not prevalence estimates" in text
    assert "finite-grid fractions are not probabilities of natural regimes" in text
    assert "does not calibrate or validate a universal total `W_AD`" in text
    assert "56 route-level records" in text
    assert "25 independent biological study clusters" in text


def test_manifest_pins_identification_core_and_bounded_pattern_provenance() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "# Supplement manifest — canonical identification-design paper" in text
    assert "## 2. Canonical scientific core" in text
    assert "crossed A × D × antagonist × pollinator interventions" in text
    assert "A×D×G×P separability diagnostic" in text
    assert "independent A×D joint-cost assay" in text
    assert "## 3. Existing-data identification stress tests" in text
    assert "Kessler et al. 2008 — trait-factorial anchor" in text
    assert "Egan et al. 2021 — consumer-factorial anchor" in text
    assert "Soper Gorden & Adler 2018 — public-data retrofit" in text
    assert "16-system high-information screened set" in text
    assert "## 6. Historical quantitative provenance retained" in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "Sasidharan et al. 2023 FVOC reconstruction" in text
    assert "## 7. Mechanism → Pattern recurrence layer retained in the Main argument" in text
    assert "56 source-adjudicated route records" in text
    assert "These overlapping counts are not added as independent-study prevalence" in text
    assert "Main-text role is limited to constituent-channel recurrence" in text


def test_live_submission_docs_do_not_pin_superseded_pr_or_branch_state() -> None:
    live_docs = (
        ROOT / "SUPPLEMENT_MANIFEST.md",
        ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md",
        ROOT / "docs" / "SUBMISSION_SCOPE.md",
        ROOT / "submission" / "SUBMISSION_CHECKLIST.md",
        ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md",
        ROOT / "submission" / "MANUSCRIPT_AUDIT_V2.md",
    )
    stale_tokens = (
        "PR #129 candidate",
        "analysis/pattern-expansion-v1",
        "inherited from PR #126",
        "agent/mechanism-pattern-universality-v1",
        "38-record / 14-independent-cluster",
        "38/14 evidence scaffold",
    )
    for path in live_docs:
        text = path.read_text(encoding="utf-8")
        for token in stale_tokens:
            assert token not in text, f"{path.name}: stale live-state token {token!r}"


def test_scope_keeps_assurance_auxiliary() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "**Auxiliary moderator:**" in text
    assert "reproductive assurance `R`" in text
    assert "background moderator" in text
    assert "not a third focal trait" in text


def test_final_audit_records_assurance_and_empirical_boundary() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "16 of 1,296" in text
    assert "three-trait theory" in text
    assert "Gates A-H" in text
    assert "`kappa`" in text
    assert "unidentified" in text
    assert "mixed partial" in text
    assert "one-sided" in text
    assert "77.2%" in text
    assert "Reader-facing repository-source QA: PASS" in text
