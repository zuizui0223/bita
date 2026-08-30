from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "identification_design" / "DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv"
READOUT = ROOT / "docs" / "DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
PRIMARY_AUDIT = ROOT / "docs" / "BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md"
PUBLICATION_LEDGER = ROOT / "docs" / "PUBLICATION_MATERIAL_RECOVERY_LEDGER.md"
KESSLER_ACCESS = ROOT / "empirical" / "identification_design" / "KESSLER_2008_SUPPLEMENT_ACCESS_RECEIPT_V1.md"
KESSLER_BOUNDS = ROOT / "empirical" / "identification_design" / "KESSLER_2008_AGGREGATE_BOUNDS_V1.md"
KESSLER_POWER = ROOT / "empirical" / "identification_design" / "KESSLER_TYPE_REPLICATION_POWER_V1.json"
KESSLER_PLAN = ROOT / "docs" / "KESSLER_TYPE_REPLICATION_AND_AUGMENTATION_V1.md"


def _rows() -> dict[str, dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return {row["hypothesis_id"]: row for row in csv.DictReader(handle)}


def test_escape_route_ledger_is_complete_and_fail_closed() -> None:
    rows = _rows()
    assert list(rows) == [f"ER{i}" for i in range(1, 11)]
    assert all(row["positive_answer"] for row in rows.values())
    assert all(row["claim_ceiling"] for row in rows.values())
    assert all(row["next_valid_gate"] for row in rows.values())
    assert rows["ER6"]["current_status"] == "DIRECT_FACTORIAL_SIGN_POSITIVE_FORMAL_UNCERTAINTY_UNRESOLVED"
    assert rows["ER7"]["current_status"] == "NOT_ACHIEVED_ZERO_OF_SIXTEEN"
    assert rows["ER8"]["current_status"] == "NOT_ACHIEVED_ZERO_STRICT"
    assert rows["ER9"]["current_status"] == "UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE"
    assert rows["ER10"]["current_status"] == "ACHIEVED_METHOD_RESULT"
    assert "Kessler" in rows["ER6"]["current_evidence"]
    assert "154 observations per trait cell" in rows["ER6"]["next_valid_gate"]
    assert "250 per cell" in rows["ER6"]["next_valid_gate"]
    assert "source uncertainty" in rows["ER9"]["next_valid_gate"]
    assert "ESCAPE_IDENTIFIED" in rows["ER9"]["next_valid_gate"]


def test_readout_separates_escape_decision_from_mechanism_allocation() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "What the ecological evidence has positively answered" in text
    assert "proposed mechanisms exist" in text.lower()
    assert "rho_delta > iota_delta + kappa_delta" in text
    assert "Delta_AD W > 0" in text
    assert "full channel point identification is not required" in text
    assert "UNRESOLVED_CURRENT_TOTAL_EVIDENCE" in text
    assert "zero recovered cost assays does not imply zero cost" in text.lower()
    assert "Decide whether escape occurs" in text
    assert "Explain why it occurs" in text
    assert "manipulated two-trait common reproductive surface" in text
    assert "SIGN_ROBUST_FORMAL_SOURCE_UNCERTAINTY_UNRESOLVED" in text
    assert "do not describe the next empirical search as looking for the first manipulated A×D surface" in text


def test_kessler_registered_recovery_preserves_sign_uncertainty_separation() -> None:
    access = KESSLER_ACCESS.read_text(encoding="utf-8")
    bounds = KESSLER_BOUNDS.read_text(encoding="utf-8")
    assert "NOT_RECOVERED_FROM_REGISTERED_PUBLIC_ROUTES" in access
    assert "403" in access
    assert "formal interval wholly > 0" in access
    assert "min probability Δ" in bounds
    assert "+0.1710" in bounds
    assert "-0.2049" in bounds
    assert "sign" in bounds.lower() and "robust" in bounds.lower()
    assert "source/design-based interaction CI" in bounds


def test_prospective_replication_is_staged_not_naive_sixteen_cell_scaling() -> None:
    import json
    power = json.loads(KESSLER_POWER.read_text(encoding="utf-8"))
    plan = KESSLER_PLAN.read_text(encoding="utf-8")
    central = {row["scenario"]: row for row in power["key_scenarios"]}["published_central"]
    attenuated = {row["scenario"]: row for row in power["key_scenarios"]}["attenuated_delta_0_17"]
    assert central["planned_total_four_cell_80pct_design_effect_1_5"] == 616
    assert attenuated["planned_total_four_cell_80pct_design_effect_1_5"] == 1000
    assert "Stage 1 — confirm the total escape sign" in plan
    assert "Stage 2 — pilot the missing channel contrasts" in plan
    assert "16-cell number is a budget warning" in plan
    assert "not a power guarantee" in power["claim_boundary"]


def test_main_manuscript_separates_functional_escape_from_mechanism_and_cue_privacy() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "a distinct defence trait is a candidate escape route" in text
    assert "a two-trait allocation hypothesis" in text
    assert "positive functional escape" in text
    assert "interval wholly above zero" in text
    assert "does not by itself demonstrate cue privatization" in text
    assert "formal positive functional escape is therefore not yet uncertainty-identified" in text.lower()
    assert "a valid positive total interval would decide the escape sign" in text
    assert "Direct attraction-by-defence-like trait factorials are not wholly absent" in text
    assert "the complete escape inequality remains a generated test" not in text


def test_primary_audit_and_publication_ledger_preserve_directness_boundaries() -> None:
    audit = PRIMARY_AUDIT.read_text(encoding="utf-8")
    ledger = PUBLICATION_LEDGER.read_text(encoding="utf-8")
    assert "direct rho_delta:                    0 studies" in audit
    assert "full point identification:          0 studies" in audit
    assert "plausibility" in audit and "identification" in audit
    assert "six high-information systems source-checked" in ledger
    assert "Targeted audit is not prevalence" in ledger
