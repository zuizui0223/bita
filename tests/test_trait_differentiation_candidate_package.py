from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_trait_differentiation_candidate_package_sources as candidate  # noqa: E402


def test_main_candidate_uses_integrated_chapter2_source() -> None:
    text = candidate.build_main_source()
    assert text.startswith("# When does a trait trade-off resolve by differentiation rather than compromise?")
    assert "Working integrated Chapter 2 draft" not in text
    assert "**Journal:** Ecology" in text
    assert "**Manuscript type:** Concepts & Synthesis" in text
    assert "\\Delta_{arch}=sL_S^*-K" in text
    assert "decoupling fraction" in text
    assert "300 nonzero-conflict evaluations" in text
    assert "cichlid" in text.lower()
    assert "Dalechampia" in text
    assert "56 route records from 25 independent biological study clusters" in text
    assert "## References added for the Chapter 2 reframe" not in text


def test_main_candidate_separates_structural_propositions_from_quadratic_corollary() -> None:
    text = candidate.build_main_source()
    general = text.split("### 2.1 General architecture propositions", 1)[1].split(
        "### 2.2 Shared-axis architecture", 1
    )[0]
    quadratic = text.split("### 2.2 Shared-axis architecture", 1)[1].split(
        "## 3. Robustness beyond quadratic response shapes", 1
    )[0]
    for token in (
        "nested-architecture weak dominance",
        "R(\\lambda)\\ge0",
        "residual-coupling monotonicity",
        "does not require quadratic, convex or smooth loss functions",
    ):
        assert token in general, token
    assert "R=sL_S^*" not in general
    assert "\\boxed{R=sL_S^*.}" in quadratic
    assert "\\boxed{\\Delta_{arch}=W_D^*-W_S^*=sL_S^*-K.}" in quadratic


def test_ecology_abstract_and_keywords_fit_current_submission_contract() -> None:
    text = candidate.build_main_source()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    words = re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", abstract, flags=re.UNICODE)
    assert 250 <= len(words) <= 330, len(words)
    assert "cannot be lower than the best shared compromise" in abstract
    assert "stronger coupling cannot increase" in abstract
    keywords = text.split("**Keywords:**", 1)[1].split("\n", 1)[0]
    assert len([term for term in keywords.split(";") if term.strip()]) >= 5


def test_main_candidate_has_lean_integrated_reference_spine() -> None:
    text = candidate.build_main_source()
    expected = (
        "Armbruster WS, Lee J, Baldwin BG (2009)",
        "Burress ED, Martinez CM, Wainwright PC (2020)",
        "Conith AJ, Albertson RC (2021)",
        "Guillaume F, Otto SP (2012)",
        "Rüffler C, Hermisson J, Wagner GP (2012)",
        "Sack L, Buckley TN (2020)",
        "Egan PA, Muola A, Parachnowitsch AL, Stenberg JA (2021)",
        "Kessler D, Gase K, Baldwin IT (2008)",
        "Soper Gorden NL, Adler LS (2018)",
    )
    for token in expected:
        assert token in text, token
    assert len(candidate.MAIN_REFERENCE_PREFIXES) == 9
    for unused_main in (
        "McCall AC, Irwin RE (2006)",
        "Lucas-Barbosa D (2016)",
        "Theis N, Adler LS (2012)",
    ):
        assert unused_main not in candidate._reference_text(), unused_main


def test_main_candidate_embeds_exactly_five_chapter2_figures() -> None:
    text = candidate.build_main_source()
    assert text.count("**Figure ") == 5
    for idx, filename in enumerate(candidate.FIGURES, 1):
        assert f"**Figure {idx}." in text
        assert f"manuscript/trait_differentiation_figures/{filename}" in text
        assert (candidate.FIGDIR / filename).exists()


def test_candidate_appendix_keeps_new_theory_and_old_identification_provenance() -> None:
    text = candidate.build_appendix_source()
    for token in (
        "# Appendix S1 — Trait differentiation and mechanism identification",
        "## S1. Shared-versus-differentiated architecture derivation",
        "Proposition 1 — a nested differentiated architecture weakly dominates before fixed cost",
        "Proposition 2 — stronger non-negative residual coupling cannot increase recoverable loss",
        "## S2. Nonquadratic robustness design and readout",
        "## S3. Cross-system architecture-state anchors",
        "## S4. Retained floral mechanism-identification supplement",
        "2,592 declared sensitivity evaluations",
        "continuous-limit implementation check",
        "response-shape sensitivity maps for the floral worked case",
    ):
        assert token in text, token
    assert "\n# Supplementary material — identification-design manuscript" not in text
    assert "## Supplementary material — identification-design manuscript" in text


def test_open_research_candidate_sources_exist_and_use_current_coverage() -> None:
    for path in (
        candidate.ROBUSTNESS_JSON,
        candidate.HIGH_INFO_COVERAGE,
        candidate.IMPATIENS_RETROFIT,
    ):
        assert path.exists(), path
    assert candidate.HIGH_INFO_COVERAGE.name == "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv"
