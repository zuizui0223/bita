import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
SUPP = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
CAP = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def test_main_has_identification_ladder_without_reinstating_theorem_headline() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "### 2.2 From non-identification to an identified set" in text
    assert r"\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\}" in text
    assert "from non-identification, through partial identification, to point identification" in text
    assert "### 3.6 Partial identification before point identification" in text
    assert r"\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W" in text
    assert "even though \\(\\rho_\\Delta\\) and \\(\\iota_\\Delta\\) can remain individually unidentified" in text
    assert "Theorem 1" not in text
    assert "77.2%" not in text


def test_historical_one_sided_result_is_recovered_with_kappa_only_restriction() -> None:
    text = MAN.read_text(encoding="utf-8")
    block = text.split("### 3.6 Partial identification before point identification", 1)[1].split(
        "## 4. From mechanism to pattern", 1
    )[0]
    assert r"\kappa_\Delta\ge0" in block
    assert r"\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W" in block
    assert "sharp partial-identification bound under an explicit restriction" in block
    assert r"\rho_\Delta\ge0" not in block
    assert r"\iota_\Delta\ge0" not in block


def test_coverage_is_a_design_fragmentation_frontier_not_only_zero_of_sixteen() -> None:
    text = MAN.read_text(encoding="utf-8")
    block = text.split("### 4.2 Identification-coverage audit", 1)[1].split(
        "### 4.3 A trait-factorial anchor", 1
    )[0]
    assert "more informative than a binary 0-of-16 result" in block
    assert "complementary faces of an identification frontier" in block
    assert "design fragmentation" in block
    assert "smallest additional intervention or measurement" in block


def test_active_abstract_preserves_identified_set_and_nested_outcome_claims() -> None:
    man = MAN.read_text(encoding="utf-8")
    abstract = _abstract(man)
    assert "defines an identified set" in abstract
    assert len(_words(abstract)) >= 150
    for token in ("Level 1", "Level 2", "Level 3", "A_0", "A_1"):
        assert token in abstract
    portal = PORTAL.read_text(encoding="utf-8")
    assert "- Target journal: **Ecology**" in portal


def test_supplement_contains_exact_projection_algebra() -> None:
    text = SUPP.read_text(encoding="utf-8")
    assert "### S1.1 Identified-set algebra and projection bounds" in text
    assert r"\rho-\iota=\delta+\kappa" in text
    assert r"\rho-\iota\in[\delta+k_L,\;\delta+k_U]" in text
    assert "structural, assumption-indexed identified sets" in text
    assert "sampling uncertainty" in text


def test_figure_and_cover_letter_use_partial_identification_without_inventing_values() -> None:
    captions = CAP.read_text(encoding="utf-8")
    assert "defines an identified set rather than a unique mechanism" in captions
    assert "fragmented identification frontier" in captions
    cover = COVER.read_text(encoding="utf-8")
    assert "A measured total interaction defines a set of compatible channel allocations" in cover
    assert "partial-identification bound rather than a standalone theorem" in cover
    main = MAN.read_text(encoding="utf-8")
    for forbidden in ("rho_delta = 0.", "iota_delta = 0.", "kappa_delta = 0."):
        assert forbidden not in main


def test_conclusion_closes_outcome_partial_point_sequence() -> None:
    text = MAN.read_text(encoding="utf-8")
    block = text.split("## 7. Conclusions", 1)[1].split("## Open Research statement", 1)[0]
    assert "A total interaction defines an identified set" in block
    assert "fragmentation of the information needed to allocate a joint interaction" in block
    assert "interaction relief" in block
    assert "partial identification" in block
    assert "mechanism identification" in block
