"""Plan the manuscript claim transition after a real third-network run.

This module is deliberately read-only with respect to manuscript files. It
requires an independently verified confirmatory bundle and, in production mode,
a recheck of the original frozen source inputs. It then maps the retained third
network result to the preregistered k=3 claim ceiling without selecting on sign
or p-value.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS,
    verify as verify_bundle,
)

PLAN_RECEIPT = "BITA_THIRD_NETWORK_CLAIM_TRANSITION_V1"
PRODUCTION_INPUT_MODE = "PUBLIC_EXISTING_NETWORKS_FIXED_DOI_REBUILD"
HEX40 = re.compile(r"^[0-9a-f]{40}$")

PREREGISTERED_COMMON_CLAIM = (
    "The same standardized access-routing association has now been tested in "
    "three independently sampled visitor networks spanning three major visitor faunas."
)

PROHIBITED_CLAIMS = [
    "a population-level mean across all ecological networks",
    "universal causality",
    "estimated between-network heterogeneity from k=3",
    "replacement or omission of the retained third network because its result is unfavorable",
    "raw-observation pooling across the three networks",
    "a unique causal effect of one access trait across all three faunas",
]

UPDATE_TARGETS = [
    {
        "file": "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
        "sections": [
            "title",
            "Abstract",
            "Methods",
            "Results",
            "What the joint test does—and does not—establish",
            "Conclusion",
            "Data accessibility and reproducibility",
        ],
        "reason": "replace the k=2 ceiling with the retained third-network test and k=3 result",
    },
    {
        "file": "manuscript/FIGURE_PLAN_ACCESS_ROUTING_LETTER_V0.md",
        "sections": ["network result figure", "joint-effect figure"],
        "reason": "add the third network and k=3 statistic without pooling raw observations",
    },
    {
        "file": "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md",
        "sections": ["evidence hierarchy", "claim ceiling"],
        "reason": "state the third-network result regardless of direction",
    },
    {
        "file": "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
        "sections": ["title", "manuscript counts", "data accessibility"],
        "reason": "synchronize the revised k=3 manuscript package",
    },
    {
        "file": "docs/SUBMISSION_SCOPE.md",
        "sections": ["Joint network test", "Third independent network priority", "Current state"],
        "reason": "replace REAL_JOINT_NETWORK_K=2 state only after a real verified bundle",
    },
]


def _finite(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _direction(rho: float) -> str:
    if rho > 0:
        return "positive"
    if rho < 0:
        return "opposite"
    return "zero"


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def plan_claim_transition(
    receipt: dict[str, object],
    *,
    bundle_verification_status: str,
    source_recheck_mode: str,
    production_required: bool = True,
) -> dict[str, object]:
    if bundle_verification_status != VERIFIED_STATUS:
        raise ValueError("CONFIRMATORY_BUNDLE_NOT_VERIFIED")

    if receipt.get("receipt") != "BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1":
        raise ValueError("WRONG_CONFIRMATORY_RECEIPT")
    if receipt.get("status") != "CONFIRMATORY_ANALYSIS_COMPLETE":
        raise ValueError("CONFIRMATORY_ANALYSIS_NOT_COMPLETE")

    mode = str(receipt.get("existing_network_input_mode", "")).strip()
    repository_commit = str(receipt.get("repository_commit", "")).strip().lower()

    if production_required:
        if source_recheck_mode != "SOURCE_INPUTS_RECHECKED":
            raise ValueError("SOURCE_INPUTS_MUST_BE_RECHECKED_BEFORE_CLAIM_TRANSITION")
        if mode != PRODUCTION_INPUT_MODE:
            raise ValueError("NONPRODUCTION_CONFIRMATORY_BUNDLE")
        if not HEX40.fullmatch(repository_commit):
            raise ValueError("PRODUCTION_RECEIPT_REPOSITORY_COMMIT_INVALID")

    retention_rule = str(receipt.get("third_network_retention_rule", "")).strip()
    if retention_rule != (
        "retain_confirmatory_third_network_regardless_of_positive_null_or_opposite_direction"
    ):
        raise ValueError("THIRD_NETWORK_RETENTION_RULE_MISSING_OR_CHANGED")

    third = receipt.get("third_network", {})
    joint = receipt.get("joint_k3", {})
    if not isinstance(third, dict) or not isinstance(joint, dict):
        raise ValueError("CONFIRMATORY_RECEIPT_RESULT_BLOCK_MISSING")

    if third.get("status") != "CONFIRMATORY_GATE_PASS":
        raise ValueError("THIRD_NETWORK_CONFIRMATORY_GATE_NOT_PASS")
    try:
        network_count = int(joint.get("network_count", -1))
    except (TypeError, ValueError) as exc:
        raise ValueError("JOINT_NETWORK_COUNT_NOT_THREE") from exc
    if network_count != 3:
        raise ValueError("JOINT_NETWORK_COUNT_NOT_THREE")

    rho_t = _finite(third.get("rho_site_adjusted_rank"), "third rho")
    p_t = _finite(third.get("permutation_p_two_sided"), "third p")
    rho_j3 = _finite(
        joint.get("joint_equal_network_fisher_z_rho"),
        "joint k3 rho",
    )
    p_j3 = _finite(joint.get("joint_permutation_p_two_sided"), "joint k3 p")

    if not (0.0 <= p_t <= 1.0 and 0.0 <= p_j3 <= 1.0):
        raise ValueError("permutation p-values must be in [0,1]")

    direction = _direction(rho_t)
    recorded_direction = str(third.get("direction", "")).strip()
    if recorded_direction and recorded_direction != direction:
        raise ValueError("THIRD_NETWORK_DIRECTION_RECEIPT_MISMATCH")

    concordance = str(joint.get("network_direction_concordance", "")).strip()
    all_three_positive = concordance == "3_of_3_positive"
    if direction == "positive" and not all_three_positive:
        raise ValueError("JOINT_DIRECTION_CONCORDANCE_INCONSISTENT")
    if direction != "positive" and all_three_positive:
        raise ValueError("JOINT_DIRECTION_CONCORDANCE_INCONSISTENT")

    if direction == "positive":
        claim_state = "THREE_NETWORK_DIRECTIONAL_CONCORDANCE"
        directional_statement = (
            "All three observed network effects are positive. "
            f"The retained third-network estimate is rho_T={_fmt(rho_t)} "
            f"with two-sided permutation p={_fmt(p_t)}."
        )
        manuscript_action = "REVISE_TO_K3_WITH_DIRECTIONAL_CONCORDANCE"
    elif direction == "opposite":
        claim_state = "THREE_NETWORK_DIRECTIONAL_NONCONCORDANCE"
        directional_statement = (
            "The retained third-network effect is opposite in sign to the first "
            f"two networks (rho_T={_fmt(rho_t)}, two-sided permutation "
            f"p={_fmt(p_t)}); directional concordance therefore does not extend "
            "to all three networks."
        )
        manuscript_action = "REVISE_TO_K3_WITH_DIRECTIONAL_NONCONCORDANCE"
    else:
        claim_state = "THREE_NETWORK_ZERO_THIRD_EFFECT"
        directional_statement = (
            "The retained third-network rank effect is zero "
            f"(rho_T={_fmt(rho_t)}, two-sided permutation p={_fmt(p_t)}); "
            "the third test therefore does not add directional concordance."
        )
        manuscript_action = "REVISE_TO_K3_WITH_ZERO_THIRD_EFFECT"

    licensed_result_statements = [
        PREREGISTERED_COMMON_CLAIM,
        directional_statement,
        (
            "With equal network weight and no raw-observation pooling, the "
            f"three-network Fisher-z statistic is rho_J3={_fmt(rho_j3)} with "
            f"two-sided permutation p={_fmt(p_j3)}."
        ),
        (
            "At k=3, the analysis still does not estimate between-network "
            "heterogeneity, a population-level network mean, or universal causality."
        ),
    ]

    return {
        "receipt": PLAN_RECEIPT,
        "status": "CLAIM_TRANSITION_PLAN_READY",
        "production_required": production_required,
        "existing_network_input_mode": mode,
        "repository_commit": repository_commit,
        "bundle_verification_status": bundle_verification_status,
        "source_recheck_mode": source_recheck_mode,
        "network_count": 3,
        "third_network_direction": direction,
        "third_network_rho": rho_t,
        "third_network_p_two_sided": p_t,
        "all_three_effects_positive": all_three_positive,
        "joint_k3_rho": rho_j3,
        "joint_k3_p_two_sided": p_j3,
        "joint_direction_concordance": concordance,
        "claim_state": claim_state,
        "manuscript_action": manuscript_action,
        "existing_k2_ceiling_statement_must_be_retired": True,
        "third_network_must_be_retained": True,
        "automatic_manuscript_edit_permitted": False,
        "licensed_common_claim": PREREGISTERED_COMMON_CLAIM,
        "licensed_result_statements": licensed_result_statements,
        "prohibited_claims": PROHIBITED_CLAIMS,
        "required_update_targets": UPDATE_TARGETS,
        "claim_boundary": (
            "This plan translates a retained, verified third-network result into "
            "the preregistered reporting ceiling. It cannot omit, replace or downweight "
            "the third network because of its sign or p-value, and it does not edit "
            "the manuscript automatically."
        ),
    }


def plan_from_bundle(
    bundle_dir: str | Path,
    *,
    source_dir: str | Path,
) -> dict[str, object]:
    verification = verify_bundle(bundle_dir, source_dir=source_dir)
    if verification["status"] != VERIFIED_STATUS:
        raise ValueError(
            "CONFIRMATORY_BUNDLE_NOT_VERIFIED: "
            + ",".join(str(x) for x in verification.get("failures", []))
        )

    receipt_path = Path(bundle_dir) / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    return plan_claim_transition(
        receipt,
        bundle_verification_status=str(verification["status"]),
        source_recheck_mode=str(verification["source_recheck_mode"]),
        production_required=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = plan_from_bundle(args.bundle_dir, source_dir=args.source_dir)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
