from __future__ import annotations

import json

import pytest

from scripts.run_third_network_release_rehearsal import run


@pytest.mark.parametrize(
    ("scenario", "expected_state"),
    [
        ("positive", "THREE_NETWORK_DIRECTIONAL_CONCORDANCE"),
        ("null", "THREE_NETWORK_DIRECTIONAL_NONCONCORDANCE"),
        ("opposite", "THREE_NETWORK_DIRECTIONAL_NONCONCORDANCE"),
    ],
)
def test_release_rehearsal_runs_complete_chain(
    tmp_path,
    scenario: str,
    expected_state: str,
) -> None:
    root = tmp_path / scenario
    receipt = run(root, scenario=scenario, permutations=19)

    assert receipt["status"] == "PASS"
    assert receipt["mode"] == "DEVELOPMENT_ONLY_SYNTHETIC_RELEASE_REHEARSAL"
    assert receipt["scientific_claim_allowed"] is False
    assert receipt["automatic_manuscript_edit_permitted"] is False
    assert receipt["confirmatory_bundle_status"] == "CONFIRMATORY_ANALYSIS_COMPLETE"
    assert receipt["bundle_verification_status"] == "CONFIRMATORY_BUNDLE_VERIFIED"
    assert receipt["source_recheck_mode"] == "SOURCE_INPUTS_RECHECKED"
    assert receipt["claim_transition_state"] == expected_state
    assert receipt["third_network_must_be_retained"] is True
    assert receipt["claim_transition_automatic_edit"] is False

    assert (root / "confirmatory_bundle" / "BUNDLE_SHA256SUMS.txt").is_file()
    assert (root / "bundle_verification.json").is_file()
    assert (root / "claim_transition_plan.json").is_file()
    assert (root / "release_rehearsal_receipt.json").is_file()


def test_release_rehearsal_preserves_positive_null_opposite_directions(tmp_path) -> None:
    receipts = {
        scenario: run(tmp_path / scenario, scenario=scenario, permutations=19)
        for scenario in ("positive", "null", "opposite")
    }

    assert receipts["positive"]["third_network_rho"] > 0
    assert abs(float(receipts["null"]["third_network_rho"])) < 0.1
    assert receipts["opposite"]["third_network_rho"] < 0

    assert receipts["positive"]["joint_k3_direction_concordance"] == "3_of_3_positive"
    assert receipts["opposite"]["joint_k3_direction_concordance"] == "not_3_of_3_positive"
    assert all(
        receipt["third_network_must_be_retained"] is True
        for receipt in receipts.values()
    )


def test_release_rehearsal_rejects_nonempty_output_dir(tmp_path) -> None:
    root = tmp_path / "used"
    root.mkdir()
    (root / "stale.txt").write_text("stale", encoding="utf-8")
    with pytest.raises(ValueError, match="RELEASE_REHEARSAL_OUTPUT_DIR_NOT_EMPTY"):
        run(root, scenario="positive", permutations=9)


def test_rehearsal_plan_is_development_only_even_if_bundle_is_verified(tmp_path) -> None:
    root = tmp_path / "positive"
    receipt = run(root, scenario="positive", permutations=9)
    plan = json.loads((root / "claim_transition_plan.json").read_text(encoding="utf-8"))

    assert receipt["bundle_verification_status"] == "CONFIRMATORY_BUNDLE_VERIFIED"
    assert receipt["scientific_claim_allowed"] is False
    assert plan["automatic_manuscript_edit_permitted"] is False
    assert plan["production_required"] is False
