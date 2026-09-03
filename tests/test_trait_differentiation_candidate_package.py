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
    # Broader floral review sources remain in the reusable pool/supplement, not Main.
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
        "## S2. Nonquadratic robustness design and readout",
        "## S3. Cross-system architecture-state anchors",
        "## S4. Retained floral mechanism-identification supplement",
        "300",
        "continuous-limit implementation check",
        "response-shape sensitivity maps for the floral worked case",
    ):
        assert token in text, token
    # The retained standalone supplement must be nested, not introduce a second H1.
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
