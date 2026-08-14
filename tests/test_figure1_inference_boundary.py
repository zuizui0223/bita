from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FIGURE = ROOT / "manuscript" / "figures" / "FIGURE_1_MECHANISTIC_ARCHITECTURE.svg"


def test_figure1_exposes_orientation_and_inference_contract() -> None:
    ET.parse(FIGURE)
    text = FIGURE.read_text(encoding="utf-8")

    for token in (
        "Signed identity",
        "W_AD = M_AD − G_AD − C_AD",
        "ORIENTATION GATE",
        "M_AD ≤ 0   ·   G_AD ≤ 0   ·   C_AD ≥ 0",
        "W_AD = ρ − ι − κ",
        "complementary iff  ρ &gt; ι + κ",
        "INFERENCE BOUNDARY",
        "does not uniquely identify M_AD, G_AD, and C_AD",
        "Channel-specific measurements, interventions",
    ):
        assert token in text
