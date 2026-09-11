from scripts import build_bita_mechanism_candidate_sources as candidate


def test_active_main_is_mechanism_identification_not_architecture_paper() -> None:
    text = candidate.build_main_source()
    assert "Trait interaction is not ecological mechanism" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "When does a trait trade-off resolve by differentiation rather than compromise?" not in text
    assert "300 nonzero-conflict evaluations" not in text
    assert "Delta_arch = sL_S* - K" not in text


def test_main_uses_new_five_figure_sequence() -> None:
    text = candidate.build_main_source()
    for name in candidate.FIGURES:
        assert f"mechanism_identification_figures/{name}" in text
    assert text.count("[[ECOLOGY_PAGE_BREAK]]") == 4
    assert "Figure 1. A trait interaction is an outcome estimand, not a mechanism allocation." in text
    assert "Figure 5. The BITA promotion ladder and its boundary with SCH and SLK." in text


def test_main_has_real_focused_references_not_placeholder() -> None:
    text = candidate.build_main_source()
    assert "Catford JA" in text
    assert "Kessler D, Gase K, Baldwin IT (2008)" in text
    assert "Egan PA" in text
    assert "Use `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`" not in text


def test_appendix_is_identification_focused() -> None:
    text = candidate.build_appendix_source()
    assert "Appendix S1 — Identification design" in text
    assert "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv" in text
    assert "Architecture-value derivations retained elsewhere" in text


def test_open_research_manifest_uses_active_identification_products(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(candidate, "DATA_OUT", tmp_path)
    text = candidate.build_open_research_manifest()
    assert "17-system high-information identification frontier" in text
    assert "56-route / 25-cluster recurrence readout" in text
    assert (tmp_path / "high_information_identification_coverage_v2.csv").exists()
    assert (tmp_path / "impatiens_2018_identification_retrofit_v1.json").exists()
    assert (tmp_path / "pattern_expansion_readout_v1.json").exists()
