from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"


def test_known_reference_corrections_are_preserved() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    assert "*Functional Ecology* 31:65–75" in text
    assert "https://doi.org/10.1111/1365-2435.12761" in text
    assert "10.1146/annurev-ento-031616-035013" not in text
    assert "*Annual Review of Entomology* 62:117–138" not in text

    assert "10.1111/nph.12930" not in text
    assert "Floral integration, modularity, and accuracy" not in text

    for obsolete in (
        "Fenster CB, Armbruster WS",
        "Harder LD, Johnson SD",
        "Krupnick GA, Weis AE, Campbell DR",
        "McCall AC, Irwin RE",
        "Mothershead K, Marquis RJ",
        "Schiestl FP, Johnson SD",
    ):
        assert obsolete not in text


def test_core_empirical_reference_identities_remain_present() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for doi in (
        "10.1002/ecy.70036",
        "10.1093/aob/mcad064",
        "10.1002/ajb2.1182",
    ):
        assert doi in text
