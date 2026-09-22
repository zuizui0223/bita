"""Development-only rehearsal of the complete third-network release chain.

This runner deliberately uses synthetic fixtures and must never be cited as
biological evidence. It exercises the production bundle path end to end:

synthetic frozen inputs
-> transactional confirmatory bundle
-> read-only bundle verification with source recheck
-> retained-result claim-transition planner

The third network is retained for positive, null-like and opposite scenarios.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.plan_third_network_claim_transition import plan_claim_transition
from scripts.run_third_network_confirmatory_pipeline import run_with_network_inputs
from scripts.run_third_network_synthetic_e2e import (
    SCENARIOS,
    _synthetic_aubert,
    _synthetic_sakhalkar,
    run as run_synthetic_e2e,
)
from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS,
    verify,
)

RECEIPT = "BITA_THIRD_NETWORK_RELEASE_REHEARSAL_V1"
TEST_COMMIT = "0" * 40
TEST_INPUT_MODE = "TEST_SYNTHETIC_EXISTING_NETWORKS"


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(
    output_dir: str | Path,
    *,
    scenario: str,
    permutations: int = 49,
) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {sorted(SCENARIOS)}")
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    root = Path(output_dir)
    if root.exists() and any(root.iterdir()):
        raise ValueError("RELEASE_REHEARSAL_OUTPUT_DIR_NOT_EMPTY")
    root.mkdir(parents=True, exist_ok=True)

    fixture = root / "synthetic_fixture"
    synthetic_receipt = run_synthetic_e2e(
        fixture,
        permutations=permutations,
        scenario=scenario,
    )
    if synthetic_receipt["status"] != "PASS":
        raise RuntimeError("synthetic fixture failed before production rehearsal")

    bundle = root / "confirmatory_bundle"
    production_receipt = run_with_network_inputs(
        events_csv=fixture / "confirmatory_events.csv",
        plant_traits_csv=fixture / "plant_traits.csv",
        mammal_traits_csv=fixture / "mammal_traits.csv",
        camera_deployment_csv=fixture / "camera_deployment.csv",
        confirmatory_freeze_json=fixture / "confirmatory_freeze.json",
        field_readiness_json=fixture / "field_readiness_receipt.json",
        sakhalkar_points=_synthetic_sakhalkar(),
        aubert_rows=_synthetic_aubert(),
        output_dir=bundle,
        repository_commit=TEST_COMMIT,
        existing_network_input_mode=TEST_INPUT_MODE,
        permutations=permutations,
    )

    verification = verify(bundle, source_dir=fixture)
    if verification["status"] != VERIFIED_STATUS:
        raise RuntimeError(
            "release rehearsal bundle failed verification: "
            + ",".join(str(x) for x in verification.get("failures", []))
        )

    plan = plan_claim_transition(
        production_receipt,
        bundle_verification_status=str(verification["status"]),
        source_recheck_mode=str(verification["source_recheck_mode"]),
        production_required=False,
    )

    existing_checks = verification.get("existing_network_checks", {})
    existing_inputs_verified = (
        isinstance(existing_checks, dict)
        and set(existing_checks) == {"sakhalkar", "aubert_ephi"}
        and all(
            isinstance(entry, dict)
            and entry.get("analysis_units_match") is True
            and entry.get("stable_json_match") is True
            and entry.get("file_sha256_match") is True
            and entry.get("source_doi_match") is True
            for entry in existing_checks.values()
        )
    )
    if not existing_inputs_verified:
        raise RuntimeError("bundled existing-network inputs failed independent verification")

    receipt = {
        "receipt": RECEIPT,
        "status": "PASS",
        "mode": "DEVELOPMENT_ONLY_SYNTHETIC_RELEASE_REHEARSAL",
        "scientific_claim_allowed": False,
        "automatic_manuscript_edit_permitted": False,
        "scenario": scenario,
        "permutations": permutations,
        "synthetic_fixture_status": synthetic_receipt["status"],
        "confirmatory_bundle_status": production_receipt["status"],
        "bundle_verification_status": verification["status"],
        "source_recheck_mode": verification["source_recheck_mode"],
        "existing_network_inputs_verified": existing_inputs_verified,
        "third_network_rho": production_receipt["third_network"][
            "rho_site_adjusted_rank"
        ],
        "third_network_direction": production_receipt["third_network"]["direction"],
        "third_network_p_two_sided": production_receipt["third_network"][
            "permutation_p_two_sided"
        ],
        "joint_k3_rho": production_receipt["joint_k3"][
            "joint_equal_network_fisher_z_rho"
        ],
        "joint_k3_direction_concordance": production_receipt["joint_k3"][
            "network_direction_concordance"
        ],
        "claim_transition_state": plan["claim_state"],
        "claim_transition_action": plan["manuscript_action"],
        "third_network_must_be_retained": plan["third_network_must_be_retained"],
        "claim_transition_automatic_edit": plan[
            "automatic_manuscript_edit_permitted"
        ],
        "bundle_repository_commit": production_receipt["repository_commit"],
        "bundle_existing_network_input_mode": production_receipt[
            "existing_network_input_mode"
        ],
        "claim_boundary": (
            "This is a development-only synthetic rehearsal of the release chain. "
            "It cannot support a biological claim, cannot modify the manuscript, "
            "and cannot substitute for a real production bundle."
        ),
    }
    _write_json(root / "release_rehearsal_receipt.json", receipt)
    _write_json(root / "bundle_verification.json", verification)
    _write_json(root / "claim_transition_plan.json", plan)
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), required=True)
    parser.add_argument("--permutations", type=int, default=49)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output_dir,
                scenario=args.scenario,
                permutations=args.permutations,
            ),
            indent=2,
            sort_keys=True,
        )
    )
