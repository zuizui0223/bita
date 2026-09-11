from __future__ import annotations

from pathlib import Path

from scripts import build_bita_mechanism_candidate_sources as builder

ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"


def test_main_submission_source_is_current_mechanism_identification_paper() -> None:
    text = builder.build_main_source()
    ordered = [
        "Trait interaction is not ecological mechanism",
        "**Journal:** Ecology",
        "**Manuscript type:** Concepts & Synthesis",
        builder.TITLE_BREAK,
        "## Abstract",
        "## 1. Introduction",
        "## 2. What a trait interaction actually identifies",
        "## 3. Partial identification before full mechanism allocation",
        "## 4. A crossed intervention design for channel identification",
        "## 5. The empirical pattern",
        "## 6. Designing the next identifiable experiment",
        "## 7. Relation to SCH and SLK",
        "## 8. Discussion",
        "## 9. Claim ceiling",
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
        "identified set",
        "partial identification",
        "four-way separability",
        "56 directional route records from 25 independent biological clusters",
        "17 high-information systems",
        "fragmented identification",
    ):
        assert token.lower() in text.lower(), token
    assert "When does a trait trade-off resolve by differentiation rather than compromise?" not in text
    assert "300 nonzero-conflict evaluations" not in text


def test_main_has_five_current_mechanism_identification_figures() -> None:
    text = builder.build_main_source()
    assert len(builder.FIGURES) == 5
    for idx, name in enumerate(builder.FIGURES, 1):
        assert name in text
        assert f"**Figure {idx}." in text
    assert text.count(builder.PAGE_BREAK) == 4


def test_appendix_is_current_identification_support_not_architecture_main() -> None:
    text = builder.build_appendix_source()
    assert text.startswith("# Appendix S1 — Identification design")
    assert "Architecture-value derivations retained elsewhere" in text
    assert "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv" in text
    assert "Main Figs. 3–4" in text
    assert "earlier theorem-led manuscript" not in text


def test_open_research_package_exports_current_identification_products(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(builder, "DATA_OUT", tmp_path)
    manifest = builder.build_open_research_manifest()
    names = {p.name for p in tmp_path.iterdir()}
    assert names == {
        "high_information_identification_coverage_v2.csv",
        "impatiens_2018_identification_retrofit_v1.json",
        "pattern_expansion_readout_v1.json",
    }
    assert "17-system high-information identification frontier" in manifest
    assert "56-route / 25-cluster recurrence readout" in manifest
    assert "not prevalence estimates" in manifest


def test_cover_letter_marks_old_architecture_package_stale() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Trait interaction is not ecological mechanism" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17-system high-information audit" in text
    assert "previously generated 30-page Main / 38-page Appendix package" in text
    assert "no longer submission-current" in text
    assert "new journal-formatted package will be rebuilt" in text


def test_historical_sources_remain_preserved_but_are_not_active_builder_inputs() -> None:
    assert (ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md").exists()
    assert (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").exists()
    source = (ROOT / "scripts" / "build_bita_mechanism_candidate_sources.py").read_text(encoding="utf-8")
    assert "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md" in source
    assert "MANUSCRIPT_THEORETICAL_ECOLOGY.md" not in source
