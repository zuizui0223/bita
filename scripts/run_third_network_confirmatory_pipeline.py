"""Run the frozen prospective third-network confirmatory analysis end to end.

Production sequence:
1. validate and freeze confirmatory inputs;
2. build checksum-verified mammal x plant x site units;
3. compute the frozen third-network r_T;
4. recompute the equal-network k=3 statistic with the two existing public networks;
5. write an immutable-style confirmatory analysis receipt.

The runner never selects or replaces the third network based on effect direction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import (
    build_public_inputs,
    combine_rhos_equal_network,
)
from scripts.analyze_joint_access_routing_k3 import (
    SEED as K3_SEED,
    summarize_joint_k3,
)
from scripts.analyze_third_access_routing_network import (
    SEED as THIRD_SEED,
    load_analysis_units,
    summarize_third_network,
)
from scripts.build_third_access_routing_units import run as build_units
from scripts.freeze_third_network_confirmatory_inputs import (
    freeze_inputs,
    write_manifest,
)

RECEIPT = "BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1"
COMPLETE_STATUS = "CONFIRMATORY_ANALYSIS_COMPLETE"
ROOT = Path(__file__).resolve().parents[1]
CANONICAL_K2_PATH = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "joint_access_routing.json"
)


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _prepare_output_dir(path: str | Path) -> Path:
    root = Path(path)
    if root.exists() and any(root.iterdir()):
        raise ValueError("CONFIRMATORY_OUTPUT_DIR_NOT_EMPTY")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _direction(value: float) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "opposite"
    return "zero"


def _validate_canonical_k2_anchor(
    *,
    canonical: dict[str, object],
    canonical_id: str,
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
    joint_k3_result: dict[str, object],
) -> dict[str, object]:
    if not str(canonical_id).strip():
        raise ValueError("canonical_k2_receipt_id is required")
    if canonical.get("network_count") != 2:
        raise ValueError("CANONICAL_K2_RECEIPT_NETWORK_COUNT_INVALID")

    effects = canonical.get("network_effects")
    if not isinstance(effects, dict):
        raise ValueError("CANONICAL_K2_RECEIPT_EFFECTS_MISSING")
    s_expected = effects.get("sakhalkar")
    a_expected = effects.get("aubert_ephi")
    if not isinstance(s_expected, dict) or not isinstance(a_expected, dict):
        raise ValueError("CANONICAL_K2_RECEIPT_NETWORKS_MISSING")

    network_effects = joint_k3_result.get("network_effects")
    if not isinstance(network_effects, dict):
        raise ValueError("K3_NETWORK_EFFECTS_MISSING")
    s_actual = float(network_effects["sakhalkar_insects"])
    a_actual = float(network_effects["aubert_ephi_birds"])

    checks = {
        "sakhalkar_n_units": len(sakhalkar_points) == int(s_expected["n_units"]),
        "aubert_n_units": len(aubert_rows) == int(a_expected["n_units"]),
        "sakhalkar_rho": math.isclose(
            s_actual,
            float(s_expected["rho"]),
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "aubert_rho": math.isclose(
            a_actual,
            float(a_expected["rho"]),
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
    }

    actual_k2 = combine_rhos_equal_network([s_actual, a_actual])
    checks["joint_k2_rho"] = math.isclose(
        actual_k2,
        float(canonical["joint_equal_network_fisher_z_rho"]),
        rel_tol=0.0,
        abs_tol=1e-15,
    )

    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise ValueError("CANONICAL_K2_ANCHOR_MISMATCH: " + ",".join(failed))

    return {
        "status": "CANONICAL_K2_ANCHOR_MATCH",
        "canonical_receipt_id": str(canonical_id).strip(),
        "checks": checks,
        "sakhalkar": {
            "n_units": len(sakhalkar_points),
            "rho": s_actual,
        },
        "aubert_ephi": {
            "n_units": len(aubert_rows),
            "rho": a_actual,
        },
        "joint_equal_network_fisher_z_rho": actual_k2,
    }


def run_with_network_inputs(
    *,
    events_csv: str | Path,
    plant_traits_csv: str | Path,
    mammal_traits_csv: str | Path,
    camera_deployment_csv: str | Path,
    confirmatory_freeze_json: str | Path,
    field_readiness_json: str | Path,
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
    output_dir: str | Path,
    repository_commit: str,
    existing_network_input_mode: str,
    canonical_k2_receipt: dict[str, object],
    canonical_k2_receipt_id: str,
    permutations: int = 9999,
    third_seed: int = THIRD_SEED,
    k3_seed: int = K3_SEED,
) -> dict[str, object]:
    if not str(repository_commit).strip():
        raise ValueError("repository_commit is required")
    if not str(existing_network_input_mode).strip():
        raise ValueError("existing_network_input_mode is required")
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    root = _prepare_output_dir(output_dir)
    manifest_json = root / "input_freeze_manifest.json"
    units_csv = root / "analysis_units.csv"
    build_audit_json = root / "unit_build_audit.json"
    third_json = root / "third_network_result.json"
    joint_json = root / "joint_access_routing_k3_result.json"
    receipt_json = root / "confirmatory_analysis_receipt.json"

    manifest = freeze_inputs(
        events_csv=events_csv,
        plant_traits_csv=plant_traits_csv,
        mammal_traits_csv=mammal_traits_csv,
        camera_deployment_csv=camera_deployment_csv,
        confirmatory_freeze_json=confirmatory_freeze_json,
        field_readiness_json=field_readiness_json,
    )
    write_manifest(manifest_json, manifest)

    build_audit = build_units(
        events_csv,
        plant_traits_csv,
        mammal_traits_csv,
        manifest_json,
        units_csv,
        build_audit_json,
    )

    third_rows = load_analysis_units(units_csv)
    third_result = summarize_third_network(
        third_rows,
        permutations=permutations,
        seed=third_seed,
    )
    _write_json(third_json, third_result)

    joint_result = summarize_joint_k3(
        sakhalkar_points,
        aubert_rows,
        third_rows,
        permutations=permutations,
        seed=k3_seed,
    )
    canonical_k2_anchor = _validate_canonical_k2_anchor(
        canonical=canonical_k2_receipt,
        canonical_id=canonical_k2_receipt_id,
        sakhalkar_points=sakhalkar_points,
        aubert_rows=aubert_rows,
        joint_k3_result=joint_result,
    )
    _write_json(joint_json, joint_result)

    third_rho = float(third_result["effect"]["rho_site_adjusted_rank"])
    receipt = {
        "receipt": RECEIPT,
        "status": COMPLETE_STATUS,
        "repository_commit": str(repository_commit).strip(),
        "existing_network_input_mode": str(existing_network_input_mode).strip(),
        "canonical_k2_anchor": canonical_k2_anchor,
        "third_network_retention_rule": (
            "retain_confirmatory_third_network_regardless_of_positive_null_or_opposite_direction"
        ),
        "input_freeze_status": manifest["status"],
        "route_reliability_status": manifest["route_reliability"]["status"],
        "route_reliability_kappa": manifest["route_reliability"]["kappa_LBAN"],
        "analysis_units": build_audit["analysis_units"],
        "third_network": {
            "status": third_result["status"],
            "rho_site_adjusted_rank": third_rho,
            "permutation_p_two_sided": third_result["effect"][
                "permutation_p_two_sided"
            ],
            "direction": _direction(third_rho),
            "seed": third_seed,
        },
        "joint_k3": {
            "network_count": joint_result["network_count"],
            "joint_equal_network_fisher_z_rho": joint_result[
                "joint_equal_network_fisher_z_rho"
            ],
            "joint_permutation_p_two_sided": joint_result[
                "joint_permutation_p_two_sided"
            ],
            "network_direction_concordance": joint_result[
                "network_direction_concordance"
            ],
            "seed": k3_seed,
        },
        "output_sha256": {
            "input_freeze_manifest.json": _sha256(manifest_json),
            "analysis_units.csv": _sha256(units_csv),
            "unit_build_audit.json": _sha256(build_audit_json),
            "third_network_result.json": _sha256(third_json),
            "joint_access_routing_k3_result.json": _sha256(joint_json),
        },
        "source_input_sha256": manifest["files"],
        "claim_boundary": (
            "This receipt records the frozen confirmatory analysis exactly as run. "
            "It does not automatically edit the manuscript, assert universal causality, "
            "estimate between-network heterogeneity, or permit replacement of an "
            "unfavorable third-network result."
        ),
    }
    _write_json(receipt_json, receipt)
    return receipt


def run(
    *,
    events_csv: str | Path,
    plant_traits_csv: str | Path,
    mammal_traits_csv: str | Path,
    camera_deployment_csv: str | Path,
    confirmatory_freeze_json: str | Path,
    field_readiness_json: str | Path,
    output_dir: str | Path,
    repository_commit: str,
    permutations: int = 9999,
) -> dict[str, object]:
    sakhalkar_points, aubert_rows = build_public_inputs()
    canonical_k2_receipt = json.loads(CANONICAL_K2_PATH.read_text(encoding="utf-8"))
    canonical_k2_receipt_id = "sha256:" + _sha256(CANONICAL_K2_PATH)
    return run_with_network_inputs(
        events_csv=events_csv,
        plant_traits_csv=plant_traits_csv,
        mammal_traits_csv=mammal_traits_csv,
        camera_deployment_csv=camera_deployment_csv,
        confirmatory_freeze_json=confirmatory_freeze_json,
        field_readiness_json=field_readiness_json,
        sakhalkar_points=sakhalkar_points,
        aubert_rows=aubert_rows,
        output_dir=output_dir,
        repository_commit=repository_commit,
        existing_network_input_mode="PUBLIC_EXISTING_NETWORKS",
        canonical_k2_receipt=canonical_k2_receipt,
        canonical_k2_receipt_id=canonical_k2_receipt_id,
        permutations=permutations,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv")
    parser.add_argument("plant_traits_csv")
    parser.add_argument("mammal_traits_csv")
    parser.add_argument("camera_deployment_csv")
    parser.add_argument("confirmatory_freeze_json")
    parser.add_argument("field_readiness_json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repository-commit", required=True)
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()

    print(
        json.dumps(
            run(
                events_csv=args.events_csv,
                plant_traits_csv=args.plant_traits_csv,
                mammal_traits_csv=args.mammal_traits_csv,
                camera_deployment_csv=args.camera_deployment_csv,
                confirmatory_freeze_json=args.confirmatory_freeze_json,
                field_readiness_json=args.field_readiness_json,
                output_dir=args.output_dir,
                repository_commit=args.repository_commit,
                permutations=args.permutations,
            ),
            indent=2,
            sort_keys=True,
        )
    )
