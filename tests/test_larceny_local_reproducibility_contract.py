from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
MANIFEST = ROOT / "SUPPLEMENT_MANIFEST.md"
LOCAL_EFFECTS = ROOT / "empirical" / "broad_reality_evidence" / "larceny_gate" / "results" / "larceny_contributing_effects.csv"
MODERN = ROOT / "scripts" / "run_leal_modern_estimator_sensitivity.py"


def test_canonical_leal_inputs_are_local_not_external_only() -> None:
    assert LOCAL_EFFECTS.is_file()
    text = MODERN.read_text(encoding="utf-8")
    assert "local_path = ROOT / PINNED_PATH" in text
    assert "canonical Leal contributing effects missing" in text


def test_data_availability_and_manifest_state_local_assets_plus_provenance() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    assert "included directly in the canonical repository tree" in manuscript
    assert "included directly in the canonical repository tree" in manifest
    for text in (manuscript, manifest):
        assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
