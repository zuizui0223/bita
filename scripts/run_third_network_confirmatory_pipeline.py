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
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.load_frozen_access_routing_archive import (
    MODE as FROZEN_EXISTING_NETWORK_MODE,
    load_frozen_existing_networks,
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
HEX40 = re.compile(r"^[0-9a-f]{40}$")
REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_K2_RESULT = (
    REPO_ROOT
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


def _write_bundle_checksums(root: Path) -> Path:
    path = root / "BUNDLE_SHA256SUMS.txt"
    lines = []
    for candidate in sorted(root.iterdir(), key=lambda item: item.name):
        if not candidate.is_file() or candidate.name == path.name:
            continue
        lines.append(f"{_sha256(candidate)}  {candidate.name}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _stable_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _prepare_output_dirs(path: str | Path) -> tuple[Path, Path]:
    final = Path(path)
    final.parent.mkdir(parents=True, exist_ok=True)

    if final.exists():
        if not final.is_dir() or any(final.iterdir()):
            raise ValueError("CONFIRMATORY_OUTPUT_DIR_NOT_EMPTY")
        final.rmdir()

    staging = final.with_name(final.name + ".inprogress")
    if staging.exists():
        raise ValueError("CONFIRMATORY_STAGING_DIR_EXISTS")

    staging.mkdir(parents=False, exist_ok=False)
    return final, staging


def _current_checkout_commit() -> str | None:
    github_sha = os.environ.get("GITHUB_SHA", "").strip().lower()
    if HEX40.fullmatch(github_sha):
        return github_sha

    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

    value = proc.stdout.strip().lower()
    return value if HEX40.fullmatch(value) else None


def _validate_production_repository_commit(value: str) -> str:
    commit = str(value).strip().lower()
    if not HEX40.fullmatch(commit):
        raise ValueError("repository_commit must be an exact 40-character git SHA")

    current = _current_checkout_commit()
    if current is not None and current != commit:
        raise ValueError(
            f"REPOSITORY_COMMIT_MISMATCH: requested={commit} current={current}"
        )
    return commit


def _direction(value: float) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "opposite"
    return "zero"


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
    existing_network_provenance: dict[str, object] | None = None,
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

    final_root, root = _prepare_output_dirs(output_dir)
    manifest_json = root / "input_freeze_manifest.json"
    units_csv = root / "analysis_units.csv"
    build_audit_json = root / "unit_build_audit.json"
    third_json = root / "third_network_result.json"
    joint_json = root / "joint_access_routing_k3_result.json"
    receipt_json = root / "confirmatory_analysis_receipt.json"

    try:
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
        _write_json(joint_json, joint_result)

        third_rho = float(third_result["effect"]["rho_site_adjusted_rank"])
        receipt = {
            "receipt": RECEIPT,
            "status": COMPLETE_STATUS,
            "repository_commit": str(repository_commit).strip(),
            "existing_network_input_mode": str(existing_network_input_mode).strip(),
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
            "existing_network_inputs": {
                "sakhalkar": {
                    "analysis_units": len(sakhalkar_points),
                    "stable_json_sha256": _stable_json_sha256(sakhalkar_points),
                    "source_doi": "10.5281/zenodo.8398202",
                },
                "aubert_ephi": {
                    "analysis_units": len(aubert_rows),
                    "stable_json_sha256": _stable_json_sha256(aubert_rows),
                    "source_doi": "10.5281/zenodo.14185547",
                },
            },
            "existing_network_archive_provenance": existing_network_provenance,
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
        _write_bundle_checksums(root)
        root.replace(final_root)
        return receipt

    except Exception:
        if root.exists():
            shutil.rmtree(root)
        raise


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
    existing_network_archive_dir: str | Path,
    permutations: int = 9999,
) -> dict[str, object]:
    commit = _validate_production_repository_commit(repository_commit)
    sakhalkar_points, aubert_rows, archive_receipt = load_frozen_existing_networks(
        existing_network_archive_dir,
        CANONICAL_K2_RESULT,
    )
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
        repository_commit=commit,
        existing_network_input_mode=FROZEN_EXISTING_NETWORK_MODE,
        existing_network_provenance=archive_receipt,
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
    parser.add_argument("--existing-network-archive-dir", required=True)
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
                existing_network_archive_dir=args.existing_network_archive_dir,
                permutations=args.permutations,
            ),
            indent=2,
            sort_keys=True,
        )
    )
