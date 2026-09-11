from pathlib import Path
import re

from scripts import build_bita_mechanism_candidate_sources as candidate


ROOT = Path(__file__).resolve().parents[1]


def test_main_candidate_uses_active_mechanism_identification_source() -> None:
    text = candidate.build_main_source()
    assert text.startswith("# Trait interaction is not ecological mechanism")
    assert "**Journal:** Ecology" in text
    assert "**Manuscript type:** Concepts & Synthesis" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "identified set" in text
    assert "four-way separability" in text
    assert "When does a trait trade-off resolve by differentiation rather than compromise?" not in text
    assert "300 nonzero-conflict evaluations" not in text


def test_main_candidate_separates_interaction_from_mechanism_allocation() -> None:
    text = candidate.build_main_source()
    assert "Delta_AD W" in text
    assert "rho_delta" in text
    assert "iota_delta" in text
    assert "kappa_delta" in text
    assert "does not identify" in text
    assert "partial identification" in text
    assert "remaining joint channel" in text


def test_ecology_abstract_and_keywords_fit_current_submission_contract() -> None:
    text = candidate.build_main_source()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    words = re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", abstract, flags=re.UNICODE)
    assert 150 <= len(words) <= 350, len(words)
    assert "interaction" in abstract.lower()
    assert "mechanism" in abstract.lower()
    assert "identified set" in abstract.lower()
    keywords = text.split("**Keywords:**", 1)[1].split("\n", 1)[0]
    assert 5 <= len([term for term in keywords.split(";") if term.strip()]) <= 12


def test_main_candidate_has_focused_identification_reference_spine() -> None:
    text = candidate.build_main_source()
    for token in (
        "Kessler D, Gase K, Baldwin IT (2008)",
        "Egan PA",
        "Catford JA",
    ):
        assert token in text, token
    assert "Use `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`" not in text


def test_main_candidate_embeds_exactly_five_current_figures() -> None:
    text = candidate.build_main_source()
    assert len(candidate.FIGURES) == 5
    assert text.count("**Figure ") == 5
    for idx, filename in enumerate(candidate.FIGURES, 1):
        assert f"**Figure {idx}." in text
        assert f"mechanism_identification_figures/{filename}" in text
        assert (candidate.FIGDIR / filename).exists()


def test_candidate_appendix_is_identification_focused() -> None:
    text = candidate.build_appendix_source()
    assert text.startswith("# Appendix S1 — Identification design")
    assert "Architecture-value derivations retained elsewhere" in text
    assert "identified" in text.lower()
    assert "Main Figs. 3–4" in text
    assert "earlier theorem-led manuscript" not in text


def test_open_research_candidate_sources_use_current_identification_coverage(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(candidate, "DATA_OUT", tmp_path)
    manifest = candidate.build_open_research_manifest()
    assert candidate.HIGH_INFO.name == "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv"
    assert candidate.IMPATIENS.name == "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json"
    assert candidate.PATTERN_READOUT.name == "PATTERN_EXPANSION_READOUT_V1.json"
    assert "17-system high-information identification frontier" in manifest
    assert "56-route / 25-cluster recurrence readout" in manifest
