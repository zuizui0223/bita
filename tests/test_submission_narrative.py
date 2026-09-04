from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_balance_differentiation_and_preserved_identification_story() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "SCH / Chapter 1 — BALANCE" in text
    assert "BITA / Chapter 2 — DIFFERENTIATION" in text
    assert "Delta_arch = s * L_S* - K" in text
    assert "300 / 300" in text
    assert "60 / 60" in text
    assert "Delta_AD W = W11 - W10 - W01 + W00" in text
    assert "56 route records" in text
    assert "25 independent biological clusters" in text
    assert "17 systems" in text
    assert "fragmented identification" in text.lower()
    assert "route recurrence" in text
    assert "!= prevalence" in text
    assert "29 Main pages + 12 Appendix pages" in text
    assert "not yet declared submission-ready" in text


def test_one_trait_shared_cue_lane_is_externalized_to_sch() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    manuscript = (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").read_text(encoding="utf-8")
    limits = manuscript.split("### 6.4 Limits", 1)[1].split("## 7. Conclusions", 1)[0]
    assert "SCH / Chapter 1" in readme
    assert "does not test" in limits
    assert "five attraction-to-pollination and eight attraction-to-antagonism clusters" in limits
    assert "constituent evidence" in limits
    assert not any((ROOT / "empirical" / "one_trait_shared_cue").glob("*"))
    assert not any((ROOT / "related_work" / "one_trait_shared_cue").glob("*"))


def test_manifest_pins_identification_core_and_bounded_pattern_provenance() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "# Supplement manifest — canonical partial-identification paper" in text
    assert "## 2. Scientific core" in text
    assert "selective crossed interventions" in text
    assert "four-way separability test" in text
    assert "independent joint-channel assay" in text
    assert "## 3. Mechanism → Pattern / identification frontier" in text
    assert "56 route records" in text
    assert "These counts establish recurrence only." in text
    assert "## 4. Existing-data anchors" in text
    assert "Kessler 2008: trait-factorial anchor" in text
    assert "Egan 2021: complementary consumer-factorial anchor" in text
    assert "Impatiens capensis" in text
    assert "No screened system closes all allocation dimensions and no independent joint-cost assay is present." in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "Main Document: 29 pages" in text


def test_live_submission_docs_do_not_pin_superseded_theorem_story() -> None:
    live_docs = (
        ROOT / "README.md",
        ROOT / "SUPPLEMENT_MANIFEST.md",
        ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md",
        ROOT / "docs" / "SUBMISSION_SCOPE.md",
        ROOT / "submission" / "SUBMISSION_CHECKLIST.md",
        ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md",
        ROOT / "submission" / "MANUSCRIPT_AUDIT_V2.md",
        ROOT / "submission" / "ECOLOGY_UPLOAD_PACKAGE_PLAN.md",
        ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md",
    )
    stale_tokens = (
        "When are floral attraction and defence complementary? A one-sided mechanistic bound",
        "paperized around the one-sided selectivity bound",
        "one-sided mechanistic theorem plus",
        "Main Document: 27 pages",
        "Main 27 pages",
        "27 Main Document pages",
    )
    for path in live_docs:
        text = path.read_text(encoding="utf-8")
        for token in stale_tokens:
            assert token not in text, f"{path.name}: stale live-state token {token!r}"


def test_scope_preserves_identification_boundaries() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "Pattern layer 1" in text
    assert "Pattern layer 2" in text
    assert "source-adjudicated route ledger is **not itself a grand meta-analysis**" in text
    assert "marginal route recurrence" in text
    assert "!= total A×D interaction" in text
    assert "U_delta` is not kappa" in text
    assert "29 Main pages + 12 Appendix pages" in text


def test_chapter2_scope_explicitly_delays_canonical_repointing() -> None:
    text = (ROOT / "docs" / "CHAPTER2_SUBMISSION_SCOPE_V1.md").read_text(encoding="utf-8")
    lower = text.lower()
    assert "does not replace `docs/SUBMISSION_SCOPE.md`" in text
    assert "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md" in text
    assert "MANUSCRIPT_IDENTIFICATION_DESIGN.md" in text
    assert "K < s L_S*" in text
    assert "300/300" in text
    assert "17-system fragmented identification frontier" in text
    assert "promotion" in lower and "canonical" in lower
    assert "passes" in lower or "pass" in lower


def test_final_audit_records_preserved_identification_package_boundary() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "identification framework" in text
    assert "56 route records" in text
    assert "25 independent biological clusters" in text
    assert "independent joint-cost assay:       0" in text
    assert "full rho/iota/kappa identification: 0" in text
    assert "Main Document: 29 pages" in text
    assert "full-page visual QA — PASS" in text
    assert "The constituent channels recur, but their joint allocation remains unidentified." in text
