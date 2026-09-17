from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_SUFFIX = "." + "md"
MANUSCRIPT = ROOT / "manuscript" / f"MANUSCRIPT_TRAIT_DIFFERENTIATION_V1{DOC_SUFFIX}"
RECEIPT = ROOT / "empirical" / "identification_design" / f"KESSLER_2008_MECHANISM_BOUND_HANDOFF_V1{DOC_SUFFIX}"


def test_active_manuscript_carries_conditional_kessler_mechanism_bound_without_overpromotion() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "KESSLER_CONDITIONAL_BIOTIC_BALANCE_LOWER_BOUND = +0.1710239" in receipt
    assert r"\rho_\Delta-\iota_\Delta\ge0.171" in manuscript
    assert "conditional partial-identification bound" in manuscript
    assert "not a measured channel effect" in manuscript
    assert "Level-2" in manuscript and "Level-3" in manuscript
