from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_three_world_balance_differentiation_identification_story() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "SCH / Chapter 1 — SHARED-COORDINATE WORLD" in text
    assert "BALANCE / Chapter 2 — MIDDLE WORLD" in text
    assert "BITA / Chapter 3 — DIFFERENTIATED-COORDINATE WORLD" in text
    assert "Delta_arch = R - K" in text
    assert "R = s L_S*" in text
    assert "Delta_arch = s L_S* - K" in text
    assert "300 / 300" in text
    assert "60 / 60" in text
    assert "Delta_AD W = W11 - W10 - W01 + W00" in text
    assert "56 source-adjudicated route records / 25 independent biological clusters" in text
    assert "17-system high-information frontier" in text
    assert "fragmented identification" in text.lower()
    assert "route recurrence" in text
    assert "!= prevalence" in text
    assert "Main Document: 30 pages" in text
    assert "Appendix S1:   38 pages" in text
    assert "Science and pre-metadata package: GO" in text


def test_three_world_contract_keeps_bita_on_the_right_hand_architecture_boundary() -> None:
    text = (ROOT / "docs" / "THREE_WORLD_PROGRAMME_V1.md").read_text(encoding="utf-8")
    assert "Chapter 1 / SCH" in text
    assert "Chapter 2 / BALANCE" in text
    assert "Chapter 3 / BITA" in text
    assert "Phi = sL-K = 0" in text
    assert "Delta_W = sL-K" in text
    assert "BITA does not own the left-hand conflict boundary `L=0`" in text


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


def test_manifest_pins_chapter2_core_and_bounded_identification_provenance() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "# Supplement manifest — canonical trait-differentiation Chapter 2" in text
    assert "## 2. Scientific core" in text
    assert "Delta_arch = R - K" in text
    assert "R = s L_S*" in text
    assert "## 3. Robustness layer" in text
    assert "300 / 300" in text
    assert "## 5. Retained floral identification layer" in text
    assert "selective crossed interventions" in text
    assert "four-way separability test" in text
    assert "independent joint-channel assay" in text
    assert "56 route records" in text
    assert "These counts establish recurrence only." in text
    assert "No screened system closes all allocation dimensions and no independent joint-cost assay is present." in text
    assert "## 8. Historical quantitative provenance retained" in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "Main Document: 30 pages" in text
    assert "Appendix S1:   38 pages" in text


def test_live_submission_docs_do_not_pin_superseded_theorem_or_identification_only_story() -> None:
    live_docs = (
        ROOT / "README.md",
        ROOT / "SUPPLEMENT_MANIFEST.md",
        ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md",
        ROOT / "docs" / "SUBMISSION_SCOPE.md",
        ROOT / "submission" / "SUBMISSION_CHECKLIST.md",
        ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md",
        ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md",
    )
    stale_tokens = (
        "When are floral attraction and defence complementary? A one-sided mechanistic bound",
        "paperized around the one-sided selectivity bound",
        "one-sided mechanistic theorem plus",
        "Main Document: 27 pages",
        "Main 27 pages",
        "27 Main Document pages",
        "canonical partial-identification paper",
    )
    for path in live_docs:
        text = path.read_text(encoding="utf-8")
        for token in stale_tokens:
            assert token not in text, f"{path.name}: stale live-state token {token!r}"


def test_scope_preserves_identification_boundaries_inside_chapter2() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "Pattern layer 1" in text
    assert "Pattern layer 2" in text
    assert "source-adjudicated route ledger is **not itself a grand meta-analysis**" in text
    assert "marginal route recurrence" in text
    assert "!= total A×D interaction" in text
    assert "`U_delta` is not kappa by subtraction" in text
    assert "30 Main pages + 38 Appendix pages" in text
    assert "full page-by-page qa of all 68 pages" in text.lower()


def test_chapter2_promotion_receipt_records_closed_gates() -> None:
    text = (ROOT / "docs" / "CHAPTER2_SUBMISSION_SCOPE_V1.md").read_text(encoding="utf-8")
    assert "PROMOTION GATES CLOSED" in text
    assert "docs/SUBMISSION_SCOPE.md` is the canonical live submission scope" in text
    assert "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md" in text
    assert "MANUSCRIPT_IDENTIFICATION_DESIGN.md" in text
    assert "K < s L_S*" in text
    assert "300/300" in text
    assert "17-system fragmented identification frontier" in text
    assert "[x] post-promotion canonical package rebuild succeeds" in text
    assert "full visual QA: 68/68 pages PASS" in text


def test_final_audit_records_promoted_chapter2_and_preserved_identification_boundary() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "canonical trait-differentiation Chapter 2" in text
    assert "Delta_arch = R - K" in text
    assert "R = s L_S*" in text
    assert "56 route records" in text
    assert "25 independent biological clusters" in text
    assert "independent joint-cost assay:       0" in text
    assert "full rho/iota/kappa identification: 0" in text
    assert "Main Document: 30 pages" in text
    assert "Appendix S1:   38 pages" in text
    assert "full-page visual QA — PASS" in text
    assert "The constituent channels recur, but their joint allocation remains unidentified." in text
