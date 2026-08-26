from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SUPPLEMENT_MANIFEST.md"
LOCAL_EFFECTS = ROOT / "empirical" / "broad_reality_evidence" / "larceny_gate" / "results" / "larceny_contributing_effects.csv"
MODERN = ROOT / "scripts" / "run_leal_modern_estimator_sensitivity.py"


def test_canonical_leal_inputs_are_local_not_external_only() -> None:
    assert LOCAL_EFFECTS.is_file()
    text = MODERN.read_text(encoding="utf-8")
    assert "local_path = ROOT / PINNED_PATH" in text
    assert "canonical Leal contributing effects missing" in text


def test_manifest_preserves_local_leal_assets_and_immutable_provenance() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")
    assert "## 6. Historical quantitative provenance retained" in manifest
    assert "Leal et al. 2025 floral-larceny module remains pinned to immutable provenance" in manifest
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in manifest
    assert "preregistration:    0e36eac" in manifest
    assert "first results:      965d657" in manifest
    assert "doi:10.1002/ecy.70036" in manifest
    assert "not used to validate the current identification framework" in manifest
