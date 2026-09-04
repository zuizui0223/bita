from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SCRIPT = SCRIPTS / "build_ecology_review_package_sources.py"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"

spec = importlib.util.spec_from_file_location("ecology_review_builder", SCRIPT)
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_main_submission_source_is_canonical_trait_differentiation_chapter2() -> None:
    text = builder.build_main_submission_source()
    ordered = [
        "When does a trait trade-off resolve by differentiation rather than compromise?",
        "**Journal:** Ecology",
        "**Manuscript type:** Concepts & Synthesis",
        "**Open Research statement:**",
        builder.TITLE_BREAK,
        "## Abstract",
        "## 1. Introduction",
        "## 2. From shared-trait compromise to differentiated architecture",
        "### 2.1 General architecture propositions",
        "## 3. Robustness beyond quadratic response shapes",
        "## 4. Trait differentiation is often incomplete in real systems",
        "## 5. Once several trait axes exist, their fitness interaction still does not identify mechanism",
        "## 6. Discussion",
        "## 7. Conclusions",
        "## Acknowledgments",
        "## Author Contributions",
        "## Funding",
        "## Conflict of Interest Statement",
        "## References",
        builder.REF_BREAK,
        "**Figure 1.",
        "**Figure 2.",
        "**Figure 3.",
        "**Figure 4.",
        "**Figure 5.",
    ]
    positions = [text.index(token) for token in ordered]
    assert positions == sorted(positions)

    for token in (
        "nested-architecture weak dominance",
        "residual-coupling monotonicity",
        "300 nonzero-conflict evaluations",
        "Cichlid",
        "Dalechampia",
        "56 route records from 25 independent biological study clusters",
        "17-system high-information audit",
        "fragmented identification",
    ):
        assert token.lower() in text.lower(), token

    assert "Working integrated Chapter 2 draft" not in text
    assert "Theorem 1" not in text
    assert "77.2%" not in text.split("## References", 1)[0]


def test_main_has_five_trait_differentiation_figures_and_no_main_tables() -> None:
    text = builder.build_main_submission_source()
    names = (
        "FIGURE_1_BALANCE_TO_DIFFERENTIATION.svg",
        "FIGURE_2_ARCHITECTURE_BOUNDARY.svg",
        "FIGURE_3_ROBUSTNESS_AND_REALITY.svg",
        "FIGURE_4_MECHANISM_IDENTIFICATION.svg",
        "FIGURE_5_FRAGMENTED_IDENTIFICATION.svg",
    )
    for idx, name in enumerate(names, 1):
        assert name in text
        assert f"**Figure {idx}." in text
    assert "## Table 1." not in text
    # Breaks before Figures 4 and 5 are removed because those tall figures
    # naturally start new pages in the validated LibreOffice rendering.
    assert text.count(builder.PAGE_BREAK) == 2


def test_appendix_integrates_architecture_and_identification_support() -> None:
    text = builder.build_appendix_source()
    assert text.startswith("# Appendix S1 — Trait differentiation and mechanism identification")
    for token in (
        "Shared-versus-differentiated architecture derivation",
        "Nonquadratic robustness design and readout",
        "Cross-system architecture-state anchors",
        "Retained floral mechanism-identification supplement",
        "Identified-set algebra and projection bounds",
        "2,592",
        "77.2%",
    ):
        assert token in text, token


def test_open_research_package_preserves_provenance_and_adds_chapter2_outputs(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(builder, "OUT", tmp_path)
    monkeypatch.setattr(builder, "DATA_OUT", tmp_path / "open_research_data")
    manifest = builder.build_open_research_manifest()
    names = {p.name for p in (tmp_path / "open_research_data").iterdir()}
    for expected in (
        "model_parameters_and_scaling.csv",
        "finite_grid_local_cases.csv",
        "mechanism_pattern_route_ledger.csv",
        "conditionality_context_records.csv",
        "direct_identification_audits.csv",
        "pattern_expansion_screening.csv",
        "trait_differentiation_robustness_readout.json",
        "high_information_identification_coverage.csv",
        "impatiens_identification_retrofit.json",
        "question_method_explanation_matrix.csv",
        "defence_escape_route_hypothesis_recovery.csv",
    ):
        assert expected in names
    assert "Chapter 2 additions" in manifest
    assert "screened-set coverage, not literature prevalence" in manifest
    assert "historical mechanism/Pattern machine-readable products are retained" in manifest


def test_cover_letter_matches_canonical_30_page_chapter2_package() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "When does a trait trade-off resolve by differentiation rather than compromise?" in text
    assert "**30 Main Document pages**" in text
    assert "**38-page Appendix S1**" in text
    assert "within the standard 30-page Concepts & Synthesis target" in text
    assert "56 source-adjudicated route records from 25 independent biological clusters" in text
    assert "A measured total interaction defines a set of compatible channel allocations" in text
    assert "partial-identification bound rather than a standalone theorem" in text
    assert "acceptance stage" in text
    assert "Potential reviewers, if requested by the submission portal" in text
    assert "Complete the number and fields requested by ScholarOne" in text


def test_canonical_builder_preserves_historical_and_component_manuscripts() -> None:
    assert (ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md").exists()
    assert (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").exists()
    source = SCRIPT.read_text(encoding="utf-8")
    assert "build_trait_differentiation_candidate_package_sources" in source
    assert "build_ecology_submission_sources" in source
    assert "Retain historical machine-readable products" in source
