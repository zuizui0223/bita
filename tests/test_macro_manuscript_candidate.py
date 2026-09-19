from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "manuscript" / "MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md"
CLAIMS = ROOT / "manuscript" / "CLAIM_FREEZE_MACRO_V0.md"
REFS = ROOT / "manuscript" / "FLORAL_DEFENCE_SELECTIVITY_REFERENCES_V0.md"
FIGS = ROOT / "manuscript" / "FIGURE_PLAN_FLORAL_DEFENCE_SELECTIVITY_V0.md"
OLD_CANONICAL = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"


def test_candidate_macro_manuscript_contains_frozen_ecological_results() -> None:
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "17 independent systems" in text
    assert "17 unique study programs" in text
    assert "chemical       9" in text
    assert "physical       7" in text
    assert "10 of the 17 programs" in text
    assert "p=0.333" in text
    assert "p=0.143" in text
    assert "rho=0.346786" in text
    assert "full-model permutation p=0.202" in text
    assert "tube-length block p=0.211" in text
    assert "14,383" in text
    assert "57 plant species" in text
    assert "1,378 bird × plant × site units" in text
    assert "15 of 17 comparable sites" in text
    assert "site-stratified permutation \\(p=0.0001\\)" in text
    assert "interaction routing through unequal access and exposure domains" in text
    assert "Attraction signals can leak to antagonists" in text
    assert "three show shared tracking" in text



def test_candidate_route_macro_is_not_presented_as_prevalence() -> None:
    text = CANDIDATE.read_text(encoding="utf-8").lower()
    assert "these counts describe the source-adjudicated evidence base rather than natural prevalence" in text
    assert "d-role admission itself is conditioned on antagonist-reduction evidence" in text


def test_candidate_network_claim_is_association_not_unique_causality() -> None:
    text = CANDIDATE.read_text(encoding="utf-8").lower()
    assert "access geometry is associated with cheating route" in text
    assert "not that tube length alone uniquely causes the switch" in text
    assert "not an exact numerical replication of Aubert et al. (2026)" in text
    assert "observational" in text

def test_candidate_does_not_claim_domain_outperforms_modality() -> None:
    text = CANDIDATE.read_text(encoding="utf-8").lower()
    forbidden = [
        "domain separation predicts selectivity better than chemical",
        "domain relation outperforms",
        "domain is better than modality",
    ]
    assert all(phrase not in text for phrase in forbidden)
    assert "perfectly confound" in text


def test_candidate_claim_freeze_keeps_null_and_causal_boundaries() -> None:
    text = CLAIMS.read_text(encoding="utf-8")
    assert "NO_DETECTED_CHANGE must never be relabelled" in text
    assert "Do not call this a causal defence experiment" in text
    assert "DESCRIPTIVE_EXACT_ONLY" in text
    assert "strict Stage-2 increment from that targeted batch: 0" in text


def test_focused_references_cover_main_evidence_layers() -> None:
    text = REFS.read_text(encoding="utf-8")
    for doi in [
        "10.1007/BF00987883",
        "10.1093/aobpla/plv019",
        "10.1093/jpe/rtad036",
        "10.1002/ecs2.4696",
        "10.7554/eLife.07641",
        "10.1093/aob/mcq045",
        "10.1111/evo.13639",
        "10.1093/aob/mcaf258",
    ]:
        assert doi in text


def test_figure_plan_has_four_main_figures_and_frozen_statistics() -> None:
    text = FIGS.read_text(encoding="utf-8")
    for number in range(1, 5):
        assert f"## Figure {number} " in text
    assert "Fisher two-sided p = 0.333" in text
    assert "permutation p = 0.0086" in text
    assert "n = 57 species" in text


def test_old_canonical_remains_the_identification_manuscript() -> None:
    first = OLD_CANONICAL.read_text(encoding="utf-8").splitlines()[0]
    assert first == "# Trait interaction is not ecological mechanism: an identification framework for multifunctional traits"


def test_candidate_aubert_network_robustness_is_frozen() -> None:
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "1,378 bird × plant × site units" in text
    assert "15 of 17 comparable sites" in text
    assert "at least five resolved interactions" in text
    assert "702 pair-sites" in text
    assert "difference +0.264" in text
    assert "mismatch rho=0.505" in text
    assert "not an exact numerical replication of Aubert et al. (2026)" in text


def test_claim_freeze_blocks_causal_aubert_overclaim() -> None:
    text = CLAIMS.read_text(encoding="utf-8")
    assert "Aubert/EPHI access-barrier association is causal" in text
    assert "min >= 5 interactions" in text
    assert "n = 702" in text


def test_claim_freeze_effective_exposure_math_is_not_corrupted() -> None:
    text = CLAIMS.read_text(encoding="utf-8")
    assert r"x_H^*=\tau_H/q_H,\qquad x_P^*=\tau_P/q_P." in text
    assert "\tau_H" not in text
