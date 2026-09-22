"""Verify a completed third-network confirmatory analysis bundle.

The verifier is read-only. It rechecks:
- receipt identity/status;
- SHA256 for every generated scientific output;
- consistency between receipt and input-freeze manifest;
- consistency of headline third-network and k=3 values;
- optional SHA256 recheck of the original frozen source inputs.

It never reruns or changes the scientific analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

RECEIPT_TYPE = "BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1"
COMPLETE_STATUS = "CONFIRMATORY_ANALYSIS_COMPLETE"
VERIFIED_STATUS = "CONFIRMATORY_BUNDLE_VERIFIED"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _same_float(a: object, b: object) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-15)


def verify(
    bundle_dir: str | Path,
    *,
    source_dir: str | Path | None = None,
) -> dict[str, object]:
    root = Path(bundle_dir)
    receipt_path = root / "confirmatory_analysis_receipt.json"
    if not receipt_path.is_file():
        raise ValueError("CONFIRMATORY_RECEIPT_MISSING")

    receipt = _load_json(receipt_path)
    failures: list[str] = []

    if receipt.get("receipt") != RECEIPT_TYPE:
        failures.append("wrong_receipt_type")
    if receipt.get("status") != COMPLETE_STATUS:
        failures.append("analysis_not_complete")

    output_hashes = receipt.get("output_sha256", {})
    if not isinstance(output_hashes, dict) or not output_hashes:
        failures.append("output_hash_receipts_missing")
        output_hashes = {}

    output_checks: dict[str, dict[str, object]] = {}
    for filename, expected in output_hashes.items():
        path = root / str(filename)
        exists = path.is_file()
        actual = _sha256(path) if exists else None
        match = exists and actual == str(expected)
        output_checks[str(filename)] = {
            "exists": exists,
            "expected_sha256": str(expected),
            "actual_sha256": actual,
            "match": match,
        }
        if not match:
            failures.append(f"output_hash_mismatch:{filename}")

    manifest_path = root / "input_freeze_manifest.json"
    third_path = root / "third_network_result.json"
    joint_path = root / "joint_access_routing_k3_result.json"

    manifest = _load_json(manifest_path) if manifest_path.is_file() else {}
    third = _load_json(third_path) if third_path.is_file() else {}
    joint = _load_json(joint_path) if joint_path.is_file() else {}

    if manifest.get("status") != "INPUTS_FROZEN_READY_FOR_JOIN":
        failures.append("input_freeze_manifest_not_ready")

    source_receipt = receipt.get("source_input_sha256")
    if source_receipt != manifest.get("files"):
        failures.append("source_input_receipt_manifest_mismatch")

    if receipt.get("input_freeze_status") != manifest.get("status"):
        failures.append("input_freeze_status_mismatch")

    manifest_rel = manifest.get("route_reliability", {})
    if not isinstance(manifest_rel, dict):
        manifest_rel = {}
    if receipt.get("route_reliability_status") != manifest_rel.get("status"):
        failures.append("route_reliability_status_mismatch")
    if not _same_float(
        receipt.get("route_reliability_kappa", float("nan")),
        manifest_rel.get("kappa_LBAN", float("nan")),
    ):
        failures.append("route_reliability_kappa_mismatch")

    receipt_third = receipt.get("third_network", {})
    if not isinstance(receipt_third, dict):
        receipt_third = {}
    third_effect = third.get("effect", {})
    if not isinstance(third_effect, dict):
        third_effect = {}
    if receipt_third.get("status") != third.get("status"):
        failures.append("third_network_status_mismatch")
    if not _same_float(
        receipt_third.get("rho_site_adjusted_rank", float("nan")),
        third_effect.get("rho_site_adjusted_rank", float("nan")),
    ):
        failures.append("third_network_rho_mismatch")
    if not _same_float(
        receipt_third.get("permutation_p_two_sided", float("nan")),
        third_effect.get("permutation_p_two_sided", float("nan")),
    ):
        failures.append("third_network_p_mismatch")

    receipt_joint = receipt.get("joint_k3", {})
    if not isinstance(receipt_joint, dict):
        receipt_joint = {}
    if int(receipt_joint.get("network_count", -1)) != int(joint.get("network_count", -2)):
        failures.append("joint_network_count_mismatch")
    if not _same_float(
        receipt_joint.get("joint_equal_network_fisher_z_rho", float("nan")),
        joint.get("joint_equal_network_fisher_z_rho", float("nan")),
    ):
        failures.append("joint_rho_mismatch")
    if not _same_float(
        receipt_joint.get("joint_permutation_p_two_sided", float("nan")),
        joint.get("joint_permutation_p_two_sided", float("nan")),
    ):
        failures.append("joint_p_mismatch")
    if receipt_joint.get("network_direction_concordance") != joint.get(
        "network_direction_concordance"
    ):
        failures.append("joint_direction_concordance_mismatch")

    existing = receipt.get("existing_network_inputs", {})
    if not isinstance(existing, dict):
        existing = {}
    for key, doi in (
        ("sakhalkar", "10.5281/zenodo.8398202"),
        ("aubert_ephi", "10.5281/zenodo.14185547"),
    ):
        entry = existing.get(key, {})
        if not isinstance(entry, dict):
            failures.append(f"existing_network_input_missing:{key}")
            continue
        digest = str(entry.get("stable_json_sha256", ""))
        if len(digest) != 64:
            failures.append(f"existing_network_digest_invalid:{key}")
        else:
            try:
                int(digest, 16)
            except ValueError:
                failures.append(f"existing_network_digest_invalid:{key}")
        if entry.get("source_doi") != doi:
            failures.append(f"existing_network_source_doi_mismatch:{key}")

    source_checks: dict[str, dict[str, object]] = {}
    source_mode = "SOURCE_INPUTS_NOT_RECHECKED"
    if source_dir is not None:
        source_mode = "SOURCE_INPUTS_RECHECKED"
        source_root = Path(source_dir)
        files = manifest.get("files", {})
        if not isinstance(files, dict):
            files = {}
            failures.append("manifest_source_files_missing")
        for key, entry in files.items():
            if not isinstance(entry, dict):
                failures.append(f"manifest_source_entry_invalid:{key}")
                continue
            filename = str(entry.get("filename", ""))
            expected = str(entry.get("sha256", ""))
            path = source_root / filename
            exists = path.is_file()
            actual = _sha256(path) if exists else None
            match = exists and actual == expected
            source_checks[str(key)] = {
                "filename": filename,
                "exists": exists,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": match,
            }
            if not match:
                failures.append(f"source_hash_mismatch:{key}")

    return {
        "receipt": "BITA_THIRD_NETWORK_CONFIRMATORY_BUNDLE_VERIFY_V1",
        "status": VERIFIED_STATUS if not failures else "CONFIRMATORY_BUNDLE_INVALID",
        "bundle_dir": str(root),
        "analysis_receipt_sha256": _sha256(receipt_path),
        "repository_commit": receipt.get("repository_commit"),
        "output_checks": output_checks,
        "source_recheck_mode": source_mode,
        "source_checks": source_checks,
        "failures": failures,
        "claim_boundary": (
            "Verification confirms bundle integrity and internal receipt consistency only. "
            "It does not change the scientific interpretation or manuscript claim ceiling."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir")
    parser.add_argument("--source-dir")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = verify(args.bundle_dir, source_dir=args.source_dir)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if result["status"] != VERIFIED_STATUS:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
