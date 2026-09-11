"""Regression guards for historical and active paper-level scientific claims."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
CLAIM_FREEZE = ROOT / "manuscript" / "CLAIM_FREEZE.md"
STORY_BOUNDARY = ROOT / "docs" / "MECHANISM_PATTERN_STORY_BOUNDARY.md"
ROBUSTNESS_READOUT = ROOT / "docs" / "TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0]


def test_claim_freeze_assets_exist() -> None:
    assert CLAIM_FREEZE.exists()
    assert STORY_BOUNDARY.exists()
    assert ROBUSTNESS_READOUT.exists()


def test_legacy_manuscript_keeps_the_one_sided_theorem_visible() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    assert "one-sided" in text
    assert "W_{AD}>0" in text or "W_{AD} > 0" in text
    assert "selectivity window" in text
    assert "necessary" in text
    assert "not sufficient" in text or "converse is not" in text


def test_legacy_theorem_uses_only_nonnegative_joint_cost_as_sign_premise() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    theorem = text.split("**Theorem 1 (one-sided selectivity bound).**", 1)[1].split("## 3.", 1)[0]
    assert "joint-cost curvature is non-negative" in theorem
    assert "signs of \\(\\rho\\) and \\(\\iota\\) are not used" in theorem
    assert "If the three deployed terms are non-negative" not in theorem


def test_legacy_abstract_separates_algebraic_proof_from_grid_implementation_check() -> None:
    abstract = _abstract(_text(LEGACY_MANUSCRIPT))
    assert "prove this algebraically" in abstract
    assert "verify implementation" in abstract
    assert "we find no counterexample" not in abstract.lower()


def test_legacy_manuscript_keeps_the_verified_looseness_and_h_gate() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    for token in ("2,592", "77.2%", "35 of 48", "-1.13,+0.71", "0-8%"):
        assert token in text, token


def test_legacy_manuscript_does_not_turn_constituent_paths_into_total_calibration() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    assert "does not calibrate \\(W_{AD}\\)" in text or "does not estimate \\(W_{AD}\\)" in text
    assert "constituent-path evidence" in text
    assert (
        "unidentified, not zero" in text
        or "unidentified rather than zero" in text
        or "uncertainty, not zero" in text
    )


def test_legacy_empirical_category_counts_are_explicitly_nonadditive() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    assert "These annotations are not additive counts" in text
    assert "can overlap within the 25-cluster route universe" in text
    assert "seven context-only programs are explicitly outside route-ledger N" in text


def test_legacy_sasidharan_robustness_is_not_promoted_to_within_study_effect() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    assert "robustness of the assembled cross-study composition rather than a within-study consumer-role effect" in text
    assert "only three study components contain both physiological roles and all three paired differences are zero" in text


def test_legacy_ai_disclosure_names_both_providers_used_in_repository_history() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    disclosure = text.split("### 4.3 Computational and AI-assisted workflow transparency", 1)[1].split("## 5.", 1)[0]
    assert "OpenAI" in disclosure
    assert "Anthropic" in disclosure
    assert "AI-generated output was not treated as empirical evidence" in disclosure


def test_legacy_prohibited_overclaim_phrases_stay_absent() -> None:
    text = _text(LEGACY_MANUSCRIPT).lower()
    prohibited = (
        "we provide the first general theory",
        "we derive a novel universal criterion",
        "the selectivity window is sufficient for complementarity",
        "we empirically validate w_ad",
        "kappa is zero because",
    )
    for phrase in prohibited:
        assert phrase not in text, phrase


def test_legacy_next_experiment_remains_a_falsification_gate_not_a_missing_result() -> None:
    text = _text(LEGACY_MANUSCRIPT)
    assert "2 × 2 allocation" in text or "2 \\times 2 allocation" in text
    assert "full attraction \\times defence factorial" in text or "attraction × defence factorial" in text
    assert "sufficiently negative" in text


def test_active_claim_freeze_uses_mechanism_identification_programme() -> None:
    text = _text(CLAIM_FREEZE)
    assert "Trait interaction is not ecological mechanism" in text
    assert "Delta_AD W = rho_delta - iota_delta - kappa_delta" in text
    assert "interaction detection" in text
    assert "identified set" in text
    assert "four-way separability diagnostic" in text
    assert "independent remaining-channel assay" in text
    assert "L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy" in text
    assert "belongs to SLK" in text


def test_active_claim_freeze_preserves_outcome_hierarchy_and_historical_ceiling() -> None:
    text = _text(CLAIM_FREEZE)
    for phrase in (
        "Level 1  Delta_AD W > 0",
        "Level 2  A0 <= 0 < A1",
        "Level 3  A0 < 0 < A1",
        "positive trait interaction proves trait differentiation",
        "positive interaction proves historical splitting",
        "structural separation implies functional, developmental, or genetic independence",
    ):
        assert phrase in text, phrase
    assert "historical origin of differentiated traits has been reconstructed" in text


def test_active_claim_freeze_freezes_empirical_identification_frontier() -> None:
    text = _text(CLAIM_FREEZE)
    for token in (
        "56 directional route records",
        "25 independent biological clusters",
        "17 systems",
        "RECURRENT_CONSTITUENT_BIOLOGY",
        "FRAGMENTED_IDENTIFICATION",
    ):
        assert token in text, token
    assert "No screened system closes the full allocation design plus an independent remaining-channel assay" in text
    assert "not prevalence estimates" in text


def test_active_claim_freeze_keeps_slk_and_bita_ownership_separate() -> None:
    text = _text(CLAIM_FREEZE)
    assert "### SLK owns" in text
    assert "### BITA owns" in text
    assert "trait interaction != ecological mechanism" in text
    assert "Older BITA architecture derivations remain versioned technical provenance" in text
    assert "must not be presented as the active paper's central novelty" in text
