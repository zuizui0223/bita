from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_declares_integrated_theory_and_empirical_synthesis() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "fixed theoretical core" in text
    assert "mechanism-pattern empirical synthesis" in text
    assert "recurrent constituent mechanisms" in text
    assert "context-dependent" in text
    assert "unidentified rather than zero" in text or "unidentified, not zero" in text
    assert "route counts are not prevalence estimates" in text
    assert "finite-grid fractions are not probabilities of natural regimes" in text
    assert "does not calibrate or validate a universal total `W_AD`" in text
    assert "56 route-level records" in text
    assert "25 independent biological study clusters" in text


def test_manifest_pins_reproduced_modules_secondary_context_and_boundaries() -> None:
    text = (ROOT / "SUPPLEMENT_MANIFEST.md").read_text(encoding="utf-8")
    assert "## 7. Reproduced quantitative synthesis module 1 — Leal et al. 2025 floral larceny" in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "## 8. Reproduced quantitative synthesis module 2 — Sasidharan et al. 2023 FVOCs" in text
    assert "PASS_AS_DEPOSITED_REANALYSIS" in text
    assert "## 9. Secondary contextual/cross-synthesis modules" in text
    assert "Haas-Desmarais et al. 2026" in text
    assert "Caruso et al. 2019" in text
    assert "Junker & Blüthgen 2010" in text
    assert "marginal routes do not estimate `W_AD`" in text
    assert "`kappa` is therefore unidentified, not estimated as zero" in text
    assert "secondary-synthesis counts are not added to route-ledger N" in text


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
