from __future__ import annotations

import pytest

from scripts.plan_third_network_claim_transition import (
    PREREGISTERED_COMMON_CLAIM,
    PRODUCTION_INPUT_MODE,
    plan_claim_transition,
)
from scripts.verify_third_network_confirmatory_bundle import VERIFIED_STATUS
from trait_architecture.existing_k3_inputs import (
    MATCH_STATUS as EXISTING_K3_MATCH_STATUS,
)


RETENTION = (
    "retain_confirmatory_third_network_regardless_of_positive_null_or_opposite_direction"
)


def _receipt(
    *,
    rho_t: float,
    p_t: float,
    concordance: str,
    rho_j3: float = 0.25,
    p_j3: float = 0.01,
    mode: str = PRODUCTION_INPUT_MODE,
    commit: str = "a" * 40,
) -> dict[str, object]:
    direction = "positive" if rho_t > 0 else "opposite" if rho_t < 0 else "zero"
    return {
        "receipt": "BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1",
        "status": "CONFIRMATORY_ANALYSIS_COMPLETE",
        "repository_commit": commit,
        "existing_network_input_mode": mode,
        "existing_network_canonical_status": EXISTING_K3_MATCH_STATUS,
        "third_network_retention_rule": RETENTION,
        "third_network": {
            "status": "CONFIRMATORY_GATE_PASS",
            "rho_site_adjusted_rank": rho_t,
            "permutation_p_two_sided": p_t,
            "direction": direction,
            "seed": 20260921,
        },
        "joint_k3": {
            "network_count": 3,
            "joint_equal_network_fisher_z_rho": rho_j3,
            "joint_permutation_p_two_sided": p_j3,
            "network_direction_concordance": concordance,
            "seed": 20260921,
        },
    }


def _plan(receipt: dict[str, object]) -> dict[str, object]:
    return plan_claim_transition(
        receipt,
        bundle_verification_status=VERIFIED_STATUS,
        source_recheck_mode="SOURCE_INPUTS_RECHECKED",
        production_required=True,
    )


@pytest.mark.parametrize("p_value", [0.0001, 0.49, 1.0])
def test_positive_third_network_is_retained_independent_of_p_value(p_value: float) -> None:
    plan = _plan(
        _receipt(
            rho_t=0.23,
            p_t=p_value,
            concordance="3_of_3_positive",
        )
    )
    assert plan["claim_state"] == "THREE_NETWORK_DIRECTIONAL_CONCORDANCE"
    assert plan["third_network_must_be_retained"] is True
    assert plan["third_network_p_two_sided"] == p_value
    assert plan["all_three_effects_positive"] is True
    assert plan["licensed_common_claim"] == PREREGISTERED_COMMON_CLAIM
    assert plan["automatic_manuscript_edit_permitted"] is False


@pytest.mark.parametrize("p_value", [0.0001, 0.67, 1.0])
def test_opposite_third_network_is_retained_independent_of_p_value(p_value: float) -> None:
    plan = _plan(
        _receipt(
            rho_t=-0.23,
            p_t=p_value,
            concordance="not_3_of_3_positive",
        )
    )
    assert plan["claim_state"] == "THREE_NETWORK_DIRECTIONAL_NONCONCORDANCE"
    assert plan["third_network_must_be_retained"] is True
    assert plan["third_network_p_two_sided"] == p_value
    assert plan["all_three_effects_positive"] is False
    assert "does not extend to all three networks" in plan["licensed_result_statements"][1]


def test_zero_third_network_retires_k2_ceiling_without_claiming_corroboration() -> None:
    plan = _plan(
        _receipt(
            rho_t=0.0,
            p_t=1.0,
            concordance="not_3_of_3_positive",
        )
    )
    assert plan["claim_state"] == "THREE_NETWORK_ZERO_THIRD_EFFECT"
    assert plan["existing_k2_ceiling_statement_must_be_retired"] is True
    assert plan["third_network_must_be_retained"] is True
    assert "does not add directional concordance" in plan["licensed_result_statements"][1]


def test_claim_transition_requires_verified_bundle() -> None:
    with pytest.raises(ValueError, match="CONFIRMATORY_BUNDLE_NOT_VERIFIED"):
        plan_claim_transition(
            _receipt(rho_t=0.2, p_t=0.2, concordance="3_of_3_positive"),
            bundle_verification_status="CONFIRMATORY_BUNDLE_INVALID",
            source_recheck_mode="SOURCE_INPUTS_RECHECKED",
            production_required=True,
        )


def test_claim_transition_requires_source_recheck_in_production() -> None:
    with pytest.raises(ValueError, match="SOURCE_INPUTS_MUST_BE_RECHECKED"):
        plan_claim_transition(
            _receipt(rho_t=0.2, p_t=0.2, concordance="3_of_3_positive"),
            bundle_verification_status=VERIFIED_STATUS,
            source_recheck_mode="SOURCE_INPUTS_NOT_RECHECKED",
            production_required=True,
        )


def test_claim_transition_rejects_synthetic_or_nonproduction_bundle() -> None:
    with pytest.raises(ValueError, match="NONPRODUCTION_CONFIRMATORY_BUNDLE"):
        _plan(
            _receipt(
                rho_t=0.2,
                p_t=0.2,
                concordance="3_of_3_positive",
                mode="TEST_SYNTHETIC_EXISTING_NETWORKS",
            )
        )


def test_claim_transition_requires_exact_repository_sha() -> None:
    with pytest.raises(ValueError, match="PRODUCTION_RECEIPT_REPOSITORY_COMMIT_INVALID"):
        _plan(
            _receipt(
                rho_t=0.2,
                p_t=0.2,
                concordance="3_of_3_positive",
                commit="TEST-COMMIT",
            )
        )


def test_claim_transition_requires_canonical_existing_network_lock() -> None:
    receipt = _receipt(rho_t=0.2, p_t=0.2, concordance="3_of_3_positive")
    receipt["existing_network_canonical_status"] = "CANONICAL_EXISTING_K3_INPUTS_MISMATCH"
    with pytest.raises(ValueError, match="CANONICAL_EXISTING_K3_INPUTS_NOT_VERIFIED"):
        _plan(receipt)


def test_claim_transition_requires_frozen_retention_rule() -> None:
    receipt = _receipt(rho_t=-0.2, p_t=0.9, concordance="not_3_of_3_positive")
    receipt["third_network_retention_rule"] = "replace_if_unfavorable"
    with pytest.raises(ValueError, match="THIRD_NETWORK_RETENTION_RULE"):
        _plan(receipt)


def test_claim_transition_detects_direction_concordance_inconsistency() -> None:
    with pytest.raises(ValueError, match="JOINT_DIRECTION_CONCORDANCE_INCONSISTENT"):
        _plan(
            _receipt(
                rho_t=-0.2,
                p_t=0.5,
                concordance="3_of_3_positive",
            )
        )


def test_claim_transition_preserves_k3_claim_ceiling() -> None:
    plan = _plan(
        _receipt(
            rho_t=0.2,
            p_t=0.8,
            concordance="3_of_3_positive",
        )
    )
    prohibited = " ".join(plan["prohibited_claims"]).lower()
    assert "universal causality" in prohibited
    assert "between-network heterogeneity" in prohibited
    assert "population-level mean" in prohibited
    assert len(plan["required_update_targets"]) >= 5
