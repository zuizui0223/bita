from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "empirical" / "identification_design" / "EXISTING_STUDY_IDENTIFICATION_AUDIT_V1.csv"
DESIGN = ROOT / "docs" / "IDENTIFICATION_DESIGN_V1.md"


def read_rows():
    with AUDIT.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_anchor_audit_contains_distinct_near_miss_classes() -> None:
    rows = read_rows()
    assert len(rows) == 4
    ids = {row["study_id"] for row in rows}
    assert ids == {
        "Gorden_Adler_2018_Impatiens_capensis",
        "Kessler_et_al_2015_Nicotiana",
        "Kessler_et_al_2008_Nicotiana",
        "Sun_Huang_2015_Pedicularis_rex",
    }
    roles = {row["design_role"] for row in rows}
    assert roles == {
        "TOTAL_INTERACTION_NEAR_MISS",
        "FACTORIAL_PHENOTYPE_NEAR_MISS",
        "NEAR_DIRECT_D_SCOPE_CASE",
        "SELECTIVE_SYSTEM_ANCHOR",
    }


def test_anchor_audit_does_not_claim_rho_iota_or_kappa_are_recovered() -> None:
    rows = read_rows()
    for row in rows:
        recoverable = row["recoverable_now"].lower()
        assert "rho_delta" not in recoverable
        assert "iota_delta" not in recoverable
        assert row["independent_kappa_assay"] == "no"


def test_identification_design_keeps_discrete_and_local_estimands_distinct() -> None:
    text = DESIGN.read_text(encoding="utf-8")
    assert "secant interaction across the chosen two levels" in text
    assert "It is not a local mixed partial" in text
    assert "A × D × G × P" in text
    assert "not two independent tests" in text
    assert "iota_delta = iota_increment_delta - m0_delta" in text
    assert "Do not automatically call `U_delta` kappa" in text
    assert "The 2,592-point finite grid becomes implementation/model-family sensitivity material" in text
