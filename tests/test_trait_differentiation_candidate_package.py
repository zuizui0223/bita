from pathlib import Path
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


def test_main_candidate_has_integrated_reference_spine() -> None:
    text = candidate.build_main_source()
    for token in (
        "Rüffler C, Hermisson J, Wagner GP (2012)",
        "Guillaume F, Otto SP (2012)",
        "Burress ED, Martinez CM, Wainwright PC (2020)",
        "Kessler D, Gase K, Baldwin IT (2008)",
        "Egan PA, Muola A, Parachnowitsch AL, Stenberg JA (2021)",
    ):
        assert token in text, token


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
        "## S2. Nonquadratic robustness design and readout",
        "## S3. Cross-system architecture-state anchors",
        "## S4. Retained floral mechanism-identification supplement",
        "300",
        "continuous-limit implementation check",
        "response-shape sensitivity maps for the floral worked case",
    ):
        assert token in text, token
    assert text.count("# Supplementary material — identification-design manuscript") == 0


def test_open_research_candidate_sources_exist() -> None:
    for path in (
        candidate.ROBUSTNESS_JSON,
        ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv",
        ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json",
    ):
        assert path.exists(), path
