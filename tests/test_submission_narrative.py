from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_integrated_theory_and_empirical_synthesis() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "fixed theoretical core" in text
    assert "mechanism-pattern empirical synthesis" in text
    assert "what is recurrent, what is context dependent, and what remains unidentified" in text
    assert "prevalence in nature" in text
    assert "empirically calibrated regime map" not in text


def test_manifest_pins_both_quantitative_modules_and_boundaries() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "## 6. Quantitative synthesis module 1" in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "## 7. Quantitative synthesis module 2" in text
    assert "PASS_AS_DEPOSITED_REANALYSIS" in text
    assert "marginal routes do not estimate `W_AD`" in text
    assert "`kappa` is therefore unidentified, not estimated as zero" in text


def test_scope_keeps_assurance_auxiliary() -> None:
    text = (ROOT / "docs" / "SUBMISSION_SCOPE.md").read_text(encoding="utf-8")
    assert "**Auxiliary moderator:**" in text
    assert "reproductive assurance `R`" in text
    assert "background moderator" in text
    assert "not a third focal trait" in text


def test_final_audit_records_assurance_and_empirical_boundary() -> None:
    text = (ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md").read_text(encoding="utf-8")
    assert "16 of 1,296" in text
    assert "three-trait theory" in text
    assert "Gates A-H" in text
    assert "`kappa`" in text
    assert "unidentified" in text
    assert "mixed partial" in text
