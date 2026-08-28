from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
SUPP = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
CAP = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
FIG4 = ROOT / "manuscript" / "identification_figures" / "FIGURE_4_IDENTIFICATION_DESIGN.svg"
BRIDGE = ROOT / "docs" / "MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md"


def test_main_restores_bounded_mechanism_to_pattern_bridge() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "## 4. From mechanism to pattern: recurrence before identification" in text
    assert "### 4.1 Constituent ecological channels recur across systems" in text
    for token in (
        "56 directional route records from 25 independent biological study clusters",
        "attraction → pollination in 5 clusters",
        "attraction → antagonism in 8",
        "defence → antagonism in 18",
        "defence → pollination in 10",
        "Fourteen clusters contain more than one route",
        "17 show context- or state-dependent switching",
    ):
        assert token in text
    assert "marginal route recurrence does not estimate" in text
    assert "Mechanism → Pattern bridge is therefore two-stage" in text


def test_abstract_keeps_recurrence_without_claiming_identification() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0]
    assert "56 route records from 25 independent biological clusters" in abstract
    assert "this establishes recurrence, not channel identification" in abstract
    assert "no study combines the trait factorial" in abstract


def test_supplement_keeps_source_detail_and_inference_boundary() -> None:
    text = SUPP.read_text(encoding="utf-8")
    assert "## S5. Constituent mechanism recurrence supporting the Main Pattern layer" in text
    for token in ("`A→pollination` occurs in 5", "`A→antagonism` in 8", "`D→antagonism` in 18", "`D→pollination` in 10"):
        assert token in text
    for estimand in ("`rho_delta`", "`iota_delta`", "`Delta_AD W`", "`kappa_delta`"):
        assert estimand in text


def test_figure4_visually_connects_recurrence_to_identification_gap() -> None:
    caption = CAP.read_text(encoding="utf-8")
    svg = FIG4.read_text(encoding="utf-8")
    assert "Constituent ecological channels recur, but mechanism allocation remains unidentified" in caption
    assert "Constituent channels recur, but mechanism allocation remains unidentified" in svg
    assert "Mechanism Pattern: 56 routes / 25 clusters" in svg
    assert "A→P 5" in svg and "A→G 8" in svg and "D→G 18" in svg and "D→P 10" in svg
    assert "recurrence ≠ channel identification" in svg


def test_bridge_document_preserves_two_layer_inference() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    assert (
        "Mechanism\n"
        "→ constituent ecological recurrence\n"
        "→ total-interaction identified set\n"
        "→ fragmented identification frontier\n"
        "→ assumption-indexed partial identification\n"
        "→ selective mechanism-allocation experiment"
    ) in text
    assert "Recurrence may establish that the framework's biological ingredients are not peculiar to one system" in text
    assert "It may not validate the algebra" in text
