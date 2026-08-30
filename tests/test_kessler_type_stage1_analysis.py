from __future__ import annotations

import pytest

from scripts.analyze_kessler_type_stage1 import analyze_stage1


def _rows_from_probabilities(
    probabilities: dict[tuple[int, int], float],
    *,
    blocks: int = 6,
    scope: str = "FLOWER_RESTRICTED_VALIDATED",
):
    rows = []
    observation = 0
    for block in range(blocks):
        for a, d in ((1, 1), (1, 0), (0, 1), (0, 0)):
            plant_id = f"B{block:02d}_A{a}D{d}"
            successes = int(probabilities[(a, d)] * 10)
            for flower in range(10):
                observation += 1
                rows.append(
                    {
                        "observation_id": f"O{observation:05d}",
                        "block_id": f"B{block:02d}",
                        "plant_id": plant_id,
                        "flower_id": f"{plant_id}_F{flower:02d}",
                        "A": str(a),
                        "D": str(d),
                        "retained": "1",
                        "outcome_binary": "1" if flower < successes else "0",
                        "outcome_id": "CAPSULE_SUCCESS",
                        "d_intervention_scope": scope,
                        "assignment_mode": "RANDOMIZED_INTERVENTION",
                        "exclusion_reason": "",
                    }
                )
    return rows


def _rows(*, blocks: int = 6, positive: bool = True, scope: str = "FLOWER_RESTRICTED_VALIDATED"):
    probabilities = {
        (1, 1): 0.4 if positive else 0.2,
        (1, 0): 0.1 if positive else 0.2,
        (0, 1): 0.1 if positive else 0.2,
        (0, 0): 0.1 if positive else 0.2,
    }
    return _rows_from_probabilities(probabilities, blocks=blocks, scope=scope)


def test_positive_complete_blocks_identify_relief_and_constraint_release() -> None:
    result = analyze_stage1(_rows(positive=True), iterations=1000)
    assert result["analysis_id"] == "kessler_type_stage1_trial_analysis_v2"
    assert result["delta_ad_point"] == pytest.approx(0.3)
    assert result["delta_ad_95pct_block_bootstrap"]["low"] > 0
    assert result["a0_attraction_effect_without_defence_point"] == pytest.approx(0.0)
    assert result["a0_95pct_block_bootstrap"] == {"low": 0.0, "high": 0.0}
    assert result["a1_attraction_effect_with_defence_point"] == pytest.approx(0.3)
    assert result["a1_95pct_block_bootstrap"]["low"] > 0
    assert result["escape_status"] == "ESCAPE_IDENTIFIED"
    assert "Backwards-compatible token" in result["escape_status_semantics"]
    hierarchy = result["outcome_claim_hierarchy"]
    assert hierarchy["interaction_relief_status"] == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    assert hierarchy["constraint_release_status"] == "CONSTRAINT_RELEASE_IDENTIFIED"
    # A0 is identified exactly at zero, so a strict negative-to-positive claim is refuted.
    assert hierarchy["strict_reversal_status"] == "STRICT_REVERSAL_REFUTED"
    assert result["block_count"] == 6
    assert result["cells"]["p11"]["probability"] == pytest.approx(0.4)
    assert "does not allocate rho_delta" in result["claim_boundary"]
    assert "not by itself" in result["escape_status_semantics"]


def test_zero_interaction_refutes_positive_relief_and_release() -> None:
    result = analyze_stage1(_rows(positive=False), iterations=1000)
    assert result["delta_ad_point"] == pytest.approx(0.0)
    assert result["delta_ad_95pct_block_bootstrap"] == {"low": 0.0, "high": 0.0}
    assert result["escape_status"] == "ESCAPE_REFUTED"
    hierarchy = result["outcome_claim_hierarchy"]
    assert hierarchy["interaction_relief_status"] == "POSITIVE_INTERACTION_RELIEF_REFUTED"
    assert hierarchy["constraint_release_status"] == "CONSTRAINT_RELEASE_REFUTED"
    assert hierarchy["strict_reversal_status"] == "STRICT_REVERSAL_REFUTED"


def test_positive_interaction_can_leave_attraction_negative_in_both_defence_states() -> None:
    rows = _rows_from_probabilities(
        {
            (1, 1): 0.2,
            (1, 0): 0.1,
            (0, 1): 0.4,
            (0, 0): 0.7,
        }
    )
    result = analyze_stage1(rows, iterations=1000)
    assert result["a0_attraction_effect_without_defence_point"] == pytest.approx(-0.6)
    assert result["a1_attraction_effect_with_defence_point"] == pytest.approx(-0.2)
    assert result["delta_ad_point"] == pytest.approx(0.4)
    hierarchy = result["outcome_claim_hierarchy"]
    assert hierarchy["interaction_relief_status"] == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    assert hierarchy["constraint_release_status"] == "CONSTRAINT_RELEASE_REFUTED"
    assert hierarchy["strict_reversal_status"] == "STRICT_REVERSAL_REFUTED"


def test_strict_negative_to_positive_reversal_is_separately_identified() -> None:
    rows = _rows_from_probabilities(
        {
            (1, 1): 0.6,
            (1, 0): 0.2,
            (0, 1): 0.3,
            (0, 0): 0.5,
        }
    )
    result = analyze_stage1(rows, iterations=1000)
    assert result["a0_attraction_effect_without_defence_point"] == pytest.approx(-0.3)
    assert result["a1_attraction_effect_with_defence_point"] == pytest.approx(0.3)
    assert result["delta_ad_point"] == pytest.approx(0.6)
    hierarchy = result["outcome_claim_hierarchy"]
    assert hierarchy["interaction_relief_status"] == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    assert hierarchy["constraint_release_status"] == "CONSTRAINT_RELEASE_IDENTIFIED"
    assert hierarchy["strict_reversal_status"] == "STRICT_REVERSAL_IDENTIFIED"


def test_systemic_scope_preserves_sign_but_limits_flower_specific_claim() -> None:
    result = analyze_stage1(
        _rows(positive=True, scope="SYSTEMIC_SOURCE_FAITHFUL"), iterations=1000
    )
    assert result["escape_status"] == "ESCAPE_IDENTIFIED"
    assert "systemic D intervention" in result["scope_claim_ceiling"]
    assert "not as a flower-exclusive" in result["scope_claim_ceiling"]


def test_incomplete_retained_block_fails_closed() -> None:
    rows = _rows()
    for row in rows:
        if row["block_id"] == "B00" and row["A"] == "1" and row["D"] == "1":
            row["retained"] = "0"
            row["outcome_binary"] = ""
            row["exclusion_reason"] = "PREDECLARED_LOSS"
    with pytest.raises(ValueError, match="block B00 is incomplete"):
        analyze_stage1(rows, iterations=1000)


def test_plant_coordinate_drift_fails_closed() -> None:
    rows = _rows()
    rows[1]["A"] = "0"
    with pytest.raises(ValueError, match="changes A/D coordinate"):
        analyze_stage1(rows, iterations=1000)


def test_excluded_rows_require_reason() -> None:
    rows = _rows()
    rows[0]["retained"] = "0"
    rows[0]["outcome_binary"] = ""
    with pytest.raises(ValueError, match="excluded rows require exclusion_reason"):
        analyze_stage1(rows, iterations=1000)
