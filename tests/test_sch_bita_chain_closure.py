from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "empirical" / "identification_design" / "SCH_BITA_CHAIN_CLOSURE_CANDIDATES_V1.csv"
HIERARCHY = ROOT / "docs" / "OUTCOME_ESCAPE_CLAIM_HIERARCHY_V1.md"
NICOTIANA = ROOT / "docs" / "NICOTIANA_SCH_BITA_CHAIN_CLOSURE_V1.md"
STAGE1_CONTRACT = ROOT / "docs" / "KESSLER_TYPE_STAGE1_DATA_CONTRACT_V1.md"


def _candidate_rows() -> list[dict[str, str]]:
    with CANDIDATES.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_candidate_ledger_has_ordered_fail_closed_priorities() -> None:
    rows = _candidate_rows()
    assert [row["priority"] for row in rows] == [str(i) for i in range(1, 7)]
    assert [row["candidate_id"] for row in rows] == [
        "NICOTIANA_PROGRAM",
        "PEDICULARIS_REX",
        "PETUNIA_PROGRAM",
        "DATURA_MANDUCA",
        "CUCURBITA_THEIS_ADLER",
        "IMPATIENS_PUBLIC_PANEL",
    ]
    assert all(row["claim_ceiling"] for row in rows)
    assert all(row["existing_data_action"] for row in rows)
    assert all(row["new_experiment_action"] for row in rows)


def test_nicotiana_is_ranked_as_program_composite_not_complete_experiment() -> None:
    row = _candidate_rows()[0]
    assert row["system"] == "Nicotiana attenuata"
    assert row["A_conflict_receiver_status"] == "DIRECT_PROGRAM_LEVEL_SAME_SYSTEM"
    assert row["common_W_conflict_status"] == "PARTIAL_NO_MATCHED_ANTAGONIST_LOSS_ON_COMMON_W"
    assert row["total_AxD_status"] == "DIRECT_POSITIVE_SIGN_SOURCE_UNCERTAINTY_UNRESOLVED"
    assert row["A0_A1_release_status"] == "NOT_IDENTIFIED_DESIGN_BASED"
    assert row["mechanism_allocation_status"] == "NOT_IDENTIFIED"
    assert row["claim_ceiling"] == "PROGRAM_COMPOSITE_NEAR_COMPLETE_NOT_DIRECT_COMPLETE_CHAIN"
    assert "without pooling" in row["existing_data_action"]
    assert "independently validated flower-specific defence" in row["new_experiment_action"]


def test_outcome_hierarchy_keeps_three_nested_claims_distinct() -> None:
    text = HIERARCHY.read_text(encoding="utf-8")
    for token in (
        "A0 = W10 - W00",
        "A1 = W11 - W01",
        "Delta_AD W = W11 - W10 - W01 + W00",
        "Level 1  positive interaction relief",
        "Level 2  constraint release",
        "Level 3  strict sign reversal",
        "strict reversal\n    => constraint release\n    => positive interaction relief",
    ):
        assert token in text
    assert "The reverse implications do not hold" in text
    assert "ESCAPE_IDENTIFIED" in text
    assert "alias for an uncertainty-identified positive total interaction only" in text
    assert "Do not use an unqualified statement" in text


def test_kessler_example_is_partially_identified_but_not_level_two() -> None:
    text = HIERARCHY.read_text(encoding="utf-8")
    for token in (
        "A0 = W10 - W00       in [-0.0299275, +0.0299275]",
        "A1 = W11 - W01       in [+0.2001327, +0.2398387]",
        "Delta_AD W            minimum +0.1710239",
        "A1 > 0 for every compatible allocation",
        "A0 spans zero",
        "A1_POSITIVE_A0_SIGN_UNRESOLVED_PARTIAL_IDENTIFICATION",
        "Level 2:                               unresolved because A0_max > 0",
        "The broadest auxiliary logit 95% interval can cross zero",
        "Systemic nicotine suppression",
    ):
        assert token in text


def test_nicotiana_plan_preserves_source_roles_and_no_pooling_boundary() -> None:
    text = NICOTIANA.read_text(encoding="utf-8")
    for doi in (
        "10.7554/eLife.07641",
        "10.1126/science.1160072",
        "10.1073/pnas.1703463114",
        "10.1111/jipb.12607",
    ):
        assert doi in text
    assert "PROGRAM_COMPOSITE_NEAR_COMPLETE" in text
    assert "DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED" in text
    assert "Results from different papers must not be algebraically combined" in text
    assert "an upstream JA perturbation cannot automatically serve as the BITA `D` manipulation" in text
    assert "Existing-data closure priority: 1" in text
    assert "Full mechanism-experiment practicality: conditional on selectivity pilot" in text


def test_nicotiana_stage_plan_closes_outcome_before_mechanism() -> None:
    text = NICOTIANA.read_text(encoding="utf-8")
    assert "Chain-closing Stage 0" in text
    assert "Chain-closing Stage 1" in text
    assert "Chain-closing Stage 2" in text
    assert "Chain-closing Stage 3" in text
    assert "same hawkmoth can contribute pollination and oviposition" in text
    assert "Do not commit immediately to a nominal 16-cell design" in text
    assert "A0 = W10 - W00" in text
    assert "A1 = W11 - W01" in text
    assert "Delta_AD W = A1 - A0" in text
    assert "A failure to reach Level 2 is not a failed experiment" in text


def test_stage1_data_contract_emits_all_three_levels() -> None:
    text = STAGE1_CONTRACT.read_text(encoding="utf-8")
    assert "Level 1 — positive interaction relief" in text
    assert "Level 2 — constraint release" in text
    assert "Level 3 — strict negative-to-positive reversal" in text
    assert "`ESCAPE_IDENTIFIED` is therefore a legacy token for Level 1 only" in text
    assert "point and 95% block-bootstrap interval for A0" in text
    assert "point and 95% block-bootstrap interval for A1" in text
    assert "point and 95% block-bootstrap interval for Delta_AD" in text
