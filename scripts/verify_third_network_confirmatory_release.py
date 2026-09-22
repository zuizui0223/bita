"""Read-only verification of a packaged third-network confirmatory release.

Verification layers:
1. exact package file inventory + FILE_SHA256SUMS;
2. release-manifest identity and claim-boundary fields;
3. frozen-input, code and protocol file hashes;
4. retained-result claim-plan consistency;
5. nested confirmatory-bundle verification with frozen-source recheck;
6. optional deterministic ZIP + external ZIP-SHA receipt verification.

No scientific analysis is rerun and no file is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS as BUNDLE_VERIFIED_STATUS,
    verify as verify_bundle,
)

RECEIPT = "BITA_THIRD_NETWORK_CONFIRMATORY_RELEASE_VERIFICATION_V1"
VERIFIED_STATUS = "CONFIRMATORY_RELEASE_VERIFIED"
INVALID_STATUS = "CONFIRMATORY_RELEASE_INVALID"
PACKAGE_RECEIPT = "BITA_THIRD_NETWORK_CONFIRMATORY_RELEASE_PACKAGE_V1"
PACKAGE_STATUS = "RELEASE_PACKAGE_READY"
CLAIM_PLAN_RECEIPT = "BITA_THIRD_NETWORK_CLAIM_TRANSITION_V1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_rel(value: str) -> bool:
    text = str(value).strip().replace("\\", "/")
    path = Path(text)
    return bool(
        text
        and not path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
        and path.name not in {"", ".", ".."}
    )


def _read_checksum_manifest(
    root: Path,
    failures: list[str],
) -> tuple[dict[str, str], dict[str, dict[str, object]]]:
    manifest_path = root / "FILE_SHA256SUMS.txt"
    expected: dict[str, str] = {}
    checks: dict[str, dict[str, object]] = {}

    if not manifest_path.is_file():
        failures.append("file_checksum_manifest_missing")
        return expected, checks

    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            failures.append("file_checksum_manifest_malformed")
            continue
        digest = parts[0].strip().lower()
        rel = parts[1].strip().replace("\\", "/")
        if not HEX64.fullmatch(digest) or not _safe_rel(rel) or rel in expected:
            failures.append("file_checksum_manifest_malformed")
            continue
        if rel == "FILE_SHA256SUMS.txt":
            failures.append("file_checksum_manifest_self_reference")
            continue
        expected[rel] = digest

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "FILE_SHA256SUMS.txt"
    }
    if set(expected) != actual:
        failures.append("release_file_inventory_mismatch")

    for rel in sorted(set(expected) | actual):
        path = root / rel
        exists = path.is_file()
        expected_hash = expected.get(rel)
        actual_hash = _sha256(path) if exists else None
        match = exists and expected_hash is not None and actual_hash == expected_hash
        checks[rel] = {
            "exists": exists,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "match": match,
        }
        if not match:
            failures.append(f"release_file_hash_mismatch:{rel}")

    return expected, checks


def _verify_manifest_file_map(
    *,
    root: Path,
    subdir: str,
    entries: object,
    failures: list[str],
    failure_prefix: str,
) -> dict[str, dict[str, object]]:
    checks: dict[str, dict[str, object]] = {}
    if not isinstance(entries, dict) or not entries:
        failures.append(f"{failure_prefix}_manifest_missing")
        return checks

    base = root / subdir
    expected_rel: set[str] = set()
    for key, value in entries.items():
        if not isinstance(value, str):
            failures.append(f"{failure_prefix}_manifest_invalid:{key}")
            continue
        rel = str(key).replace("\\", "/")
        if not _safe_rel(rel) or not HEX64.fullmatch(value.lower()):
            failures.append(f"{failure_prefix}_manifest_invalid:{key}")
            continue
        expected_rel.add(rel)

        path = base / rel
        exists = path.is_file()
        actual = _sha256(path) if exists else None
        match = exists and actual == value.lower()
        checks[rel] = {
            "exists": exists,
            "expected_sha256": value.lower(),
            "actual_sha256": actual,
            "match": match,
        }
        if not match:
            failures.append(f"{failure_prefix}_hash_mismatch:{rel}")

    actual_rel = {
        path.relative_to(base).as_posix()
        for path in base.rglob("*")
        if path.is_file()
    } if base.is_dir() else set()

    if expected_rel != actual_rel:
        failures.append(f"{failure_prefix}_inventory_mismatch")

    return checks


def _verify_frozen_inputs(
    root: Path,
    entries: object,
    failures: list[str],
) -> dict[str, dict[str, object]]:
    checks: dict[str, dict[str, object]] = {}
    if not isinstance(entries, dict) or not entries:
        failures.append("frozen_input_manifest_missing")
        return checks

    expected_files: set[str] = set()
    for key, entry in entries.items():
        if not isinstance(entry, dict):
            failures.append(f"frozen_input_manifest_invalid:{key}")
            continue
        filename = str(entry.get("filename", "")).strip()
        digest = str(entry.get("sha256", "")).strip().lower()
        if (
            not _safe_rel(filename)
            or len(Path(filename).parts) != 1
            or not HEX64.fullmatch(digest)
        ):
            failures.append(f"frozen_input_manifest_invalid:{key}")
            continue
        expected_files.add(filename)
        path = root / "frozen_inputs" / filename
        exists = path.is_file()
        actual = _sha256(path) if exists else None
        match = exists and actual == digest
        checks[str(key)] = {
            "filename": filename,
            "exists": exists,
            "expected_sha256": digest,
            "actual_sha256": actual,
            "match": match,
        }
        if not match:
            failures.append(f"frozen_input_hash_mismatch:{key}")

    actual_files = {
        path.name
        for path in (root / "frozen_inputs").iterdir()
        if path.is_file()
    } if (root / "frozen_inputs").is_dir() else set()
    if expected_files != actual_files:
        failures.append("frozen_input_inventory_mismatch")

    return checks


def _verify_claim_plan(
    root: Path,
    release_manifest: dict[str, object],
    failures: list[str],
) -> dict[str, object]:
    path = root / "claim_transition_plan.json"
    if not path.is_file():
        failures.append("claim_transition_plan_missing")
        return {}
    plan = _load_json(path)
    if not isinstance(plan, dict):
        failures.append("claim_transition_plan_invalid")
        return {}

    if plan.get("receipt") != CLAIM_PLAN_RECEIPT:
        failures.append("claim_transition_plan_wrong_receipt")
    if plan.get("status") != "CLAIM_TRANSITION_PLAN_READY":
        failures.append("claim_transition_plan_not_ready")
    if plan.get("third_network_must_be_retained") is not True:
        failures.append("claim_transition_retention_rule_missing")
    if plan.get("automatic_manuscript_edit_permitted") is not False:
        failures.append("claim_transition_autoedit_not_false")

    comparisons = {
        "repository_commit": (
            plan.get("repository_commit"),
            release_manifest.get("repository_commit"),
        ),
        "existing_network_input_mode": (
            plan.get("existing_network_input_mode"),
            release_manifest.get("existing_network_input_mode"),
        ),
        "claim_state": (
            plan.get("claim_state"),
            release_manifest.get("claim_state"),
        ),
        "third_network_direction": (
            plan.get("third_network_direction"),
            release_manifest.get("third_network_direction"),
        ),
        "network_count": (
            plan.get("network_count"),
            release_manifest.get("network_count"),
        ),
    }
    for label, (left, right) in comparisons.items():
        if left != right:
            failures.append(f"claim_release_manifest_mismatch:{label}")

    return plan


def _verify_zip(
    root: Path,
    *,
    zip_path: Path,
    zip_sha256_receipt: Path | None,
    failures: list[str],
) -> dict[str, object]:
    result: dict[str, object] = {
        "zip_path": str(zip_path),
        "exists": zip_path.is_file(),
    }
    if not zip_path.is_file():
        failures.append("release_zip_missing")
        return result

    zip_sha = _sha256(zip_path)
    result["zip_sha256"] = zip_sha

    if zip_sha256_receipt is not None:
        if not zip_sha256_receipt.is_file():
            failures.append("release_zip_sha256_receipt_missing")
        else:
            line = zip_sha256_receipt.read_text(encoding="utf-8").strip()
            parts = line.split("  ", 1)
            if (
                len(parts) != 2
                or not HEX64.fullmatch(parts[0].strip().lower())
                or parts[1].strip() != zip_path.name
            ):
                failures.append("release_zip_sha256_receipt_malformed")
            else:
                expected = parts[0].strip().lower()
                result["expected_zip_sha256"] = expected
                result["zip_sha256_match"] = expected == zip_sha
                if expected != zip_sha:
                    failures.append("release_zip_sha256_mismatch")

    expected_files = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }
    zip_checks: dict[str, dict[str, object]] = {}
    try:
        with zipfile.ZipFile(zip_path) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                failures.append("release_zip_duplicate_member")
            if set(names) != set(expected_files):
                failures.append("release_zip_inventory_mismatch")

            for info in infos:
                safe = _safe_rel(info.filename)
                fixed_time = info.date_time == FIXED_ZIP_TIME
                content = archive.read(info.filename)
                expected_path = expected_files.get(info.filename)
                expected_hash = _sha256(expected_path) if expected_path else None
                actual_hash = _bytes_sha256(content)
                content_match = expected_hash is not None and actual_hash == expected_hash
                zip_checks[info.filename] = {
                    "safe_path": safe,
                    "fixed_timestamp": fixed_time,
                    "content_sha256": actual_hash,
                    "expected_sha256": expected_hash,
                    "content_match": content_match,
                }
                if not safe:
                    failures.append(f"release_zip_unsafe_member:{info.filename}")
                if not fixed_time:
                    failures.append(f"release_zip_nondeterministic_timestamp:{info.filename}")
                if not content_match:
                    failures.append(f"release_zip_content_mismatch:{info.filename}")
    except (OSError, zipfile.BadZipFile, KeyError):
        failures.append("release_zip_invalid")

    result["member_checks"] = zip_checks
    return result


def verify(
    release_dir: str | Path,
    *,
    zip_path: str | Path | None = None,
    zip_sha256_receipt: str | Path | None = None,
) -> dict[str, object]:
    root = Path(release_dir)
    failures: list[str] = []

    if not root.is_dir():
        raise ValueError("CONFIRMATORY_RELEASE_DIR_MISSING")

    _expected_file_hashes, file_checks = _read_checksum_manifest(root, failures)

    manifest_path = root / "release_manifest.json"
    if not manifest_path.is_file():
        failures.append("release_manifest_missing")
        release_manifest: dict[str, object] = {}
    else:
        loaded = _load_json(manifest_path)
        if isinstance(loaded, dict):
            release_manifest = loaded
        else:
            release_manifest = {}
            failures.append("release_manifest_invalid")

    if release_manifest.get("receipt") != PACKAGE_RECEIPT:
        failures.append("release_manifest_wrong_receipt")
    if release_manifest.get("status") != PACKAGE_STATUS:
        failures.append("release_manifest_not_ready")
    if release_manifest.get("network_count") != 3:
        failures.append("release_manifest_network_count_not_three")
    if release_manifest.get("existing_network_inputs_verified") is not True:
        failures.append("release_manifest_existing_inputs_not_verified")
    if release_manifest.get("third_network_must_be_retained") is not True:
        failures.append("release_manifest_retention_rule_missing")
    if release_manifest.get("claim_transition_plan_ready") is not True:
        failures.append("release_manifest_claim_plan_not_ready")
    if release_manifest.get("scientific_claim_allowed_by_archive_alone") is not False:
        failures.append("release_manifest_archive_claim_flag_not_false")
    if release_manifest.get("automatic_manuscript_edit_permitted") is not False:
        failures.append("release_manifest_autoedit_not_false")

    frozen_checks = _verify_frozen_inputs(
        root,
        release_manifest.get("frozen_inputs"),
        failures,
    )
    code_checks = _verify_manifest_file_map(
        root=root,
        subdir="code",
        entries=release_manifest.get("code_files"),
        failures=failures,
        failure_prefix="code_file",
    )
    protocol_checks = _verify_manifest_file_map(
        root=root,
        subdir="protocol",
        entries=release_manifest.get("protocol_files"),
        failures=failures,
        failure_prefix="protocol_file",
    )
    claim_plan = _verify_claim_plan(root, release_manifest, failures)

    bundle_dir = root / "confirmatory_bundle"
    source_dir = root / "frozen_inputs"
    try:
        bundle_verification = verify_bundle(bundle_dir, source_dir=source_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        bundle_verification = {
            "status": "CONFIRMATORY_BUNDLE_INVALID",
            "failures": [f"verifier_exception:{type(exc).__name__}"],
        }
        failures.append("nested_confirmatory_bundle_verifier_exception")

    if bundle_verification.get("status") != BUNDLE_VERIFIED_STATUS:
        failures.append("nested_confirmatory_bundle_invalid")

    if (
        bundle_verification.get("analysis_receipt_sha256")
        != release_manifest.get("analysis_receipt_sha256")
    ):
        failures.append("release_manifest_analysis_receipt_hash_mismatch")
    if (
        bundle_verification.get("bundle_checksum_manifest_sha256")
        != release_manifest.get("bundle_checksum_manifest_sha256")
    ):
        failures.append("release_manifest_bundle_checksum_hash_mismatch")
    if bundle_verification.get("source_recheck_mode") != "SOURCE_INPUTS_RECHECKED":
        failures.append("nested_source_inputs_not_rechecked")

    zip_verification: dict[str, object] = {"mode": "ZIP_NOT_RECHECKED"}
    if zip_path is not None:
        zip_verification = _verify_zip(
            root,
            zip_path=Path(zip_path),
            zip_sha256_receipt=(
                Path(zip_sha256_receipt)
                if zip_sha256_receipt is not None
                else None
            ),
            failures=failures,
        )

    unique_failures = list(dict.fromkeys(failures))
    return {
        "receipt": RECEIPT,
        "status": VERIFIED_STATUS if not unique_failures else INVALID_STATUS,
        "failures": unique_failures,
        "release_file_checks": file_checks,
        "frozen_input_checks": frozen_checks,
        "code_file_checks": code_checks,
        "protocol_file_checks": protocol_checks,
        "claim_transition_plan": claim_plan,
        "nested_bundle_verification": bundle_verification,
        "zip_verification": zip_verification,
        "claim_boundary": (
            "Verification is read-only. A passing release verifies archive integrity "
            "and the frozen reporting contract; it does not edit or expand claims."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_dir")
    parser.add_argument("--zip")
    parser.add_argument("--zip-sha256-receipt")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = verify(
        args.release_dir,
        zip_path=args.zip,
        zip_sha256_receipt=args.zip_sha256_receipt,
    )
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
