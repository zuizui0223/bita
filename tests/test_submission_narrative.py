from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_active_mechanism_identification_story() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "trait interaction != ecological mechanism" in text
    assert "interaction detection" in text
    assert "identified set" in text
    assert "partial identification" in text
    assert "four-way separability diagnostic" in text
    assert "56 directional route records" in text
    assert "25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "FRAGMENTED_IDENTIFICATION" in text
    assert "OLD_PACKAGE_STALE" in text
    assert "REBUILD_REQUIRED" in text


def test_readme_assigns_architecture_value_spine_to_slk() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy" in text
    assert "SLK owns" in text
    assert "Older BITA architecture derivations remain preserved" in text
    assert "not the novelty center of the active full paper" in text


def test_canonical_main_is_mechanism_identification_paper() -> None:
    text = (ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md").read_text(encoding="utf-8")
    assert text.startswith("# Trait interaction is not ecological mechanism")
    assert "Level 1 — positive interaction relief" in text
    assert "Level 2 — functional constraint release" in text
    assert "Level 3 — strict reversal" in text
    assert "I(\\delta)" in text
    assert "A\\times D\\times E_G\\times E_P" in text
    assert "fragmented identification frontier" in text.lower()
    assert "architecture quantities \\(R\\), \\(s\\), \\(K\\), and \\(\\Phi\\)" in text
    assert "not the novelty center of this paper" in text


def test_scope_preserves_active_identification_boundaries() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "BITA mechanism-identification paper" in text
    assert "Level 1" in text
    assert "Level 2" in text
    assert "Level 3" in text
    assert "I(delta)" in text
    assert "fragmented identification" in text.lower()
    assert "OLD_PACKAGE_STALE" in text
    assert "REBUILD_REQUIRED_BEFORE_SUBMISSION" in text
    assert "positive A x D interaction" in text
    assert "!= ecological mechanism" in text


def test_claim_freeze_blocks_reimporting_slk_novelty() -> None:
    text = (ROOT / "manuscript" / "CLAIM_FREEZE.md").read_text(encoding="utf-8")
    assert "Trait interaction is not ecological mechanism" in text
    assert "The active manuscript must not drift back" in text
    assert "L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy" in text
    assert "belongs to SLK" in text
    assert "residual by subtraction" in text
    assert "active BITA paper owns the general `Phi=R-K`" in text


def test_submission_checklist_resets_old_go_state() -> None:
    text = (ROOT / "submission" / "SUBMISSION_CHECKLIST.md").read_text(encoding="utf-8")
    assert "SCIENCE_THESIS = FROZEN" in text
    assert "OLD_30_PLUS_38_PACKAGE = STALE" in text
    assert "FIGURES = REBUILD_REQUIRED" in text
    assert "APPENDIX = REBUILD_REQUIRED" in text
    assert "EXTERNAL_SUBMISSION = NOT_YET_READY" in text
    assert "The current blocker is no longer author metadata alone" in text


def test_final_audit_marks_old_package_historical() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "BITA mechanism-identification paper" in text
    assert "HISTORICAL_PACKAGE_QA = PASS_FOR_OLD_SCIENCE_SOURCE" in text
    assert "ACTIVE_PACKAGE_STATUS = STALE" in text
    assert "ACTIVE_MAIN_RENDER = REBUILD_REQUIRED" in text
    assert "Reader-facing submission package: NOT YET READY" in text


def test_cover_letter_uses_new_thesis_and_does_not_claim_old_package_ready() -> None:
    text = (ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md").read_text(encoding="utf-8")
    assert "Trait interaction is not ecological mechanism" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17-system high-information audit" in text
    assert "fragmented identification" in text.lower()
    assert "no longer submission-current" in text
    assert "will be rebuilt" in text


def test_figure_plan_matches_active_main_story() -> None:
    captions = (ROOT / "manuscript" / "TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md").read_text(encoding="utf-8")
    plan = (ROOT / "manuscript" / "FIGURE_REBUILD_PLAN_MECHANISM_IDENTIFICATION_V1.md").read_text(encoding="utf-8")
    assert "A trait interaction is an outcome estimand, not a mechanism allocation" in captions
    assert "identified set of compatible ecological mechanisms" in captions
    assert "Crossed consumer intervention" in captions
    assert "fragmented identification frontier" in captions
    assert "RENDERED_FIGURES_STALE" in plan
    assert "No architecture-value quantities should appear" in plan


def test_legacy_three_world_document_is_provenance_not_active_scope() -> None:
    legacy = (ROOT / "docs" / "THREE_WORLD_PROGRAMME_V1.md").read_text(encoding="utf-8")
    active = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "Chapter 1 / SCH" in legacy
    assert "Chapter 2 / BALANCE" in legacy
    assert "Chapter 3 / BITA" in legacy
    assert "architecture-value spine" in active
    assert "owned by SLK" in active


def test_one_trait_shared_cue_lane_remains_externalized_to_sch() -> None:
    manuscript = (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").read_text(encoding="utf-8")
    limits = manuscript.split("### 6.4 Limits", 1)[1].split("## 7. Conclusions", 1)[0]
    assert "does not test" in limits
    assert "five attraction-to-pollination and eight attraction-to-antagonism clusters" in limits
    assert "constituent evidence" in limits
    assert not any((ROOT / "empirical" / "one_trait_shared_cue").glob("*"))
    assert not any((ROOT / "related_work" / "one_trait_shared_cue").glob("*"))
