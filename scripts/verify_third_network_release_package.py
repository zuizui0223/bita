"""Read-only verifier for a packaged third-network confirmatory release.

This verifier checks the archival shell before any scientific replay:
- exact FILE_SHA256SUMS inventory and per-file hashes;
- release-manifest identity and retained-result guardrails;
- frozen-input/code/protocol hash maps against packaged files;
- nested confirmatory-bundle verification with frozen source recheck;
- optional adjacent deterministic ZIP and .sha256 receipt, including member
  inventory, bytes, timestamps, compression mode, and path safety.

It never mutates the release and never changes scientific claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

if __package__ in {None, ""}:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS as BUNDLE_VERIFIED_STATUS,
    verify as verify_bundle,
)
from trait_architecture.existing_k3_inputs import (
    MATCH_STATUS as EXISTING_K3_MATCH_STATUS,
    PRODUCTION_INPUT_MODE,
)

RECEIPT_TYPE = "BITA_THIRD_NETWORK_CONFIRMATORY_RELEASE_PACKAGE_V1"
VERIFIED_STATUS = "RELEASE_PACKAGE_VERIFIED"
INVALID_STATUS = "RELEASE_PACKAGE_INVALID"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
FIXED_ZIP_MODE = stat.S_IFREG | 0o644

# Transport/resource envelope for the analysis/code release. This archive never
# contains raw video, so these limits are deliberately generous relative to the
# expected CSV/JSON/code package while still bounding hostile input costs.
MAX_RELEASE_ZIP_BYTES = 1024 * 1024 * 1024
MAX_RELEASE_MEMBER_COUNT = 4096
MAX_RELEASE_MEMBER_BYTES = 256 * 1024 * 1024
MAX_RELEASE_TOTAL_UNCOMPRESSED_BYTES = 1024 * 1024 * 1024
MAX_CHECKSUM_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_SHA256_RECEIPT_BYTES = 4096
MAX_MEMBER_NAME_BYTES = 1024


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_zip_member(
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
) -> tuple[str, int]:
    digest = hashlib.sha256()
    bytes_read = 0
    with archive.open(info, "r") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            bytes_read += len(chunk)
            if bytes_read > MAX_RELEASE_MEMBER_BYTES:
                raise ValueError("release_zip_member_stream_exceeded_limit")
            digest.update(chunk)
    return digest.hexdigest(), bytes_read


def _zip_resource_report(
    infos: list[zipfile.ZipInfo],
    *,
    archive_size_bytes: int,
) -> dict[str, object]:
    failures: list[str] = []
    total_uncompressed = sum(int(info.file_size) for info in infos)
    max_member = max((int(info.file_size) for info in infos), default=0)
    max_name_bytes = max(
        (len(info.filename.encode("utf-8", errors="surrogatepass")) for info in infos),
        default=0,
    )

    if archive_size_bytes > MAX_RELEASE_ZIP_BYTES:
        failures.append("release_zip_size_limit_exceeded")
    if len(infos) > MAX_RELEASE_MEMBER_COUNT:
        failures.append("release_zip_member_count_limit_exceeded")
    if max_member > MAX_RELEASE_MEMBER_BYTES:
        failures.append("release_zip_member_size_limit_exceeded")
    if total_uncompressed > MAX_RELEASE_TOTAL_UNCOMPRESSED_BYTES:
        failures.append("release_zip_total_uncompressed_limit_exceeded")
    if max_name_bytes > MAX_MEMBER_NAME_BYTES:
        failures.append("release_zip_member_name_limit_exceeded")

    return {
        "status": "RESOURCE_LIMITS_PASS" if not failures else "RESOURCE_LIMITS_FAIL",
        "failures": failures,
        "archive_size_bytes": archive_size_bytes,
        "member_count": len(infos),
        "total_uncompressed_bytes": total_uncompressed,
        "max_member_bytes": max_member,
        "max_member_name_bytes": max_name_bytes,
        "limits": {
            "max_release_zip_bytes": MAX_RELEASE_ZIP_BYTES,
            "max_release_member_count": MAX_RELEASE_MEMBER_COUNT,
            "max_release_member_bytes": MAX_RELEASE_MEMBER_BYTES,
            "max_release_total_uncompressed_bytes": MAX_RELEASE_TOTAL_UNCOMPRESSED_BYTES,
            "max_checksum_manifest_bytes": MAX_CHECKSUM_MANIFEST_BYTES,
            "max_sha256_receipt_bytes": MAX_SHA256_RECEIPT_BYTES,
            "max_member_name_bytes": MAX_MEMBER_NAME_BYTES,
        },
    }


def _safe_rel(value: str) -> bool:
    text = str(value).strip().replace("\\", "/")
    if not text:
        return False
    path = PurePosixPath(text)
    return (
        not path.is_absolute()
        and "." not in path.parts
        and ".." not in path.parts
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_checksum_manifest(
    path: Path,
    failures: list[str],
) -> dict[str, str]:
    expected: dict[str, str] = {}
    if not path.is_file():
        failures.append("file_checksum_manifest_missing")
        return expected

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split("  ", 1)
        if len(parts) != 2:
            failures.append("file_checksum_manifest_malformed")
            continue
        digest = parts[0].strip().lower()
        rel = parts[1].strip().replace("\\", "/")
        if not HEX64.fullmatch(digest) or not _safe_rel(rel) or rel in expected:
            failures.append("file_checksum_manifest_malformed")
            continue
        expected[rel] = digest
    return expected


def _actual_inventory(root: Path, failures: list[str]) -> dict[str, Path]:
    actual: dict[str, Path] = {}
    if not root.is_dir():
        failures.append("release_directory_missing")
        return actual

    for path in root.rglob("*"):
        if path.is_symlink():
            failures.append(
                f"release_symlink_forbidden:{path.relative_to(root).as_posix()}"
            )
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "FILE_SHA256SUMS.txt":
            continue
        actual[rel] = path
    return actual


def _verify_declared_maps(
    root: Path,
    manifest: dict[str, object],
    failures: list[str],
) -> dict[str, dict[str, object]]:
    checks: dict[str, dict[str, object]] = {}

    frozen = manifest.get("frozen_inputs", {})
    if not isinstance(frozen, dict) or not frozen:
        failures.append("release_manifest_frozen_inputs_missing")
    else:
        for key, entry in frozen.items():
            if not isinstance(entry, dict):
                failures.append(f"release_manifest_frozen_input_invalid:{key}")
                continue
            filename = str(entry.get("filename", "")).strip()
            expected = str(entry.get("sha256", "")).strip().lower()
            rel = f"frozen_inputs/{filename}"
            path = root / rel
            actual = _sha256(path) if path.is_file() else None
            match = (
                _safe_rel(filename)
                and "/" not in filename
                and HEX64.fullmatch(expected) is not None
                and actual == expected
            )
            checks[f"frozen:{key}"] = {
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": match,
            }
            if not match:
                failures.append(f"release_manifest_frozen_input_mismatch:{key}")

    code = manifest.get("code_files", {})
    if not isinstance(code, dict) or not code:
        failures.append("release_manifest_code_files_missing")
    else:
        for rel_raw, expected_raw in code.items():
            rel_code = str(rel_raw).strip().replace("\\", "/")
            expected = str(expected_raw).strip().lower()
            rel = f"code/{rel_code}"
            path = root / rel
            actual = _sha256(path) if path.is_file() else None
            match = (
                _safe_rel(rel_code)
                and HEX64.fullmatch(expected) is not None
                and actual == expected
            )
            checks[f"code:{rel_code}"] = {
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": match,
            }
            if not match:
                failures.append(f"release_manifest_code_file_mismatch:{rel_code}")

    protocol = manifest.get("protocol_files", {})
    if not isinstance(protocol, dict) or not protocol:
        failures.append("release_manifest_protocol_files_missing")
    else:
        for filename_raw, expected_raw in protocol.items():
            filename = str(filename_raw).strip()
            expected = str(expected_raw).strip().lower()
            rel = f"protocol/{filename}"
            path = root / rel
            actual = _sha256(path) if path.is_file() else None
            match = (
                _safe_rel(filename)
                and "/" not in filename
                and HEX64.fullmatch(expected) is not None
                and actual == expected
            )
            checks[f"protocol:{filename}"] = {
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": match,
            }
            if not match:
                failures.append(
                    f"release_manifest_protocol_file_mismatch:{filename}"
                )

    return checks


def _verify_zip(
    root: Path,
    *,
    zip_path: Path,
    sha_path: Path,
    failures: list[str],
) -> dict[str, object]:
    result: dict[str, object] = {
        "zip_path": str(zip_path),
        "sha256_receipt_path": str(sha_path),
        "zip_exists": zip_path.is_file(),
        "sha256_receipt_exists": sha_path.is_file(),
    }
    if not zip_path.is_file():
        failures.append("release_zip_missing")
        return result
    if not sha_path.is_file():
        failures.append("release_zip_sha256_receipt_missing")
        return result

    zip_size = zip_path.stat().st_size
    result["zip_size_bytes"] = zip_size
    if zip_size > MAX_RELEASE_ZIP_BYTES:
        failures.append("release_zip_size_limit_exceeded")
        result["resource_limits"] = {
            "status": "RESOURCE_LIMITS_FAIL",
            "failures": ["release_zip_size_limit_exceeded"],
            "archive_size_bytes": zip_size,
            "limits": {
                "max_release_zip_bytes": MAX_RELEASE_ZIP_BYTES,
            },
        }
        return result

    sha_receipt_size = sha_path.stat().st_size
    result["sha256_receipt_size_bytes"] = sha_receipt_size
    if sha_receipt_size > MAX_SHA256_RECEIPT_BYTES:
        failures.append("release_zip_sha256_receipt_size_limit_exceeded")
        return result

    zip_sha = _sha256(zip_path)
    result["actual_zip_sha256"] = zip_sha

    lines = [line for line in sha_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    receipt_ok = False
    expected_zip_sha: str | None = None
    if len(lines) != 1:
        failures.append("release_zip_sha256_receipt_malformed")
    else:
        parts = lines[0].split("  ", 1)
        if len(parts) == 2:
            expected_zip_sha = parts[0].strip().lower()
            expected_name = parts[1].strip()
            receipt_ok = (
                HEX64.fullmatch(expected_zip_sha) is not None
                and expected_name == zip_path.name
                and expected_zip_sha == zip_sha
            )
        if not receipt_ok:
            failures.append("release_zip_sha256_receipt_mismatch")

    result["expected_zip_sha256"] = expected_zip_sha
    result["sha256_receipt_match"] = receipt_ok

    directory_files = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }

    try:
        with zipfile.ZipFile(zip_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            resource_limits = _zip_resource_report(
                infos,
                archive_size_bytes=zip_size,
            )
            result["resource_limits"] = resource_limits
            failures.extend(str(item) for item in resource_limits["failures"])

            archive_comment_empty = archive.comment == b""
            result["archive_comment_empty"] = archive_comment_empty
            if not archive_comment_empty:
                failures.append("release_zip_archive_comment_forbidden")
            if len(names) != len(set(names)):
                failures.append("release_zip_duplicate_member")
            if any(not _safe_rel(name) for name in names):
                failures.append("release_zip_unsafe_member")
            if set(names) != set(directory_files):
                failures.append("release_zip_inventory_mismatch")

            member_checks: dict[str, dict[str, object]] = {}
            for info in infos:
                name = info.filename
                safe = _safe_rel(name)
                directory_path = directory_files.get(name)
                member_resource_ok = (
                    safe
                    and info.file_size <= MAX_RELEASE_MEMBER_BYTES
                    and len(name.encode("utf-8", errors="surrogatepass")) <= MAX_MEMBER_NAME_BYTES
                )
                directory_sha = (
                    _sha256(directory_path)
                    if directory_path is not None
                    and directory_path.is_file()
                    and directory_path.stat().st_size <= MAX_RELEASE_MEMBER_BYTES
                    else None
                )
                if member_resource_ok:
                    try:
                        member_sha, member_bytes_read = _sha256_zip_member(archive, info)
                    except (OSError, RuntimeError, zipfile.BadZipFile, ValueError):
                        member_sha, member_bytes_read = None, None
                        failures.append(f"release_zip_member_stream_unreadable:{name}")
                else:
                    member_sha, member_bytes_read = None, None
                bytes_match = (
                    directory_sha is not None
                    and member_sha is not None
                    and directory_sha == member_sha
                )

                unix_mode = (info.external_attr >> 16) & 0xFFFF
                regular_file = stat.S_IFMT(unix_mode) == stat.S_IFREG
                permission_match = unix_mode == FIXED_ZIP_MODE
                create_system_match = info.create_system == 3
                unencrypted = (info.flag_bits & 0x1) == 0
                no_member_extra = info.extra == b""
                no_member_comment = info.comment == b""
                not_directory = not info.is_dir()

                metadata_match = (
                    info.compress_type == zipfile.ZIP_STORED
                    and info.date_time == FIXED_ZIP_TIME
                    and create_system_match
                    and regular_file
                    and permission_match
                    and unencrypted
                    and no_member_extra
                    and no_member_comment
                    and not_directory
                )
                member_checks[name] = {
                    "safe_path": safe,
                    "directory_sha256": directory_sha,
                    "zip_member_sha256": member_sha,
                    "bytes_match": bytes_match,
                    "metadata_match": metadata_match,
                    "resource_ok": member_resource_ok,
                    "declared_file_size": info.file_size,
                    "declared_compress_size": info.compress_size,
                    "streamed_bytes": member_bytes_read,
                    "create_system": info.create_system,
                    "unix_mode_octal": oct(unix_mode),
                    "regular_file": regular_file,
                    "permission_match": permission_match,
                    "unencrypted": unencrypted,
                    "no_member_extra": no_member_extra,
                    "no_member_comment": no_member_comment,
                    "not_directory": not_directory,
                }
                if not member_resource_ok:
                    failures.append(f"release_zip_member_resource_limit:{name}")
                if not bytes_match:
                    failures.append(f"release_zip_member_bytes_mismatch:{name}")
                if not metadata_match:
                    failures.append(f"release_zip_member_metadata_mismatch:{name}")
            result["member_checks"] = member_checks
    except (OSError, zipfile.BadZipFile, RuntimeError, KeyError) as exc:
        failures.append(f"release_zip_unreadable:{type(exc).__name__}")

    return result


def verify_release_package(
    release_dir: str | Path,
    *,
    zip_path: str | Path | None = None,
    sha256_receipt_path: str | Path | None = None,
    require_archive: bool = False,
) -> dict[str, object]:
    root = Path(release_dir)
    failures: list[str] = []

    checksum_path = root / "FILE_SHA256SUMS.txt"
    expected = _parse_checksum_manifest(checksum_path, failures)
    actual = _actual_inventory(root, failures)

    expected_names = set(expected)
    actual_names = set(actual)
    if expected_names != actual_names:
        failures.append("file_checksum_inventory_mismatch")

    file_checks: dict[str, dict[str, object]] = {}
    for rel in sorted(expected_names | actual_names):
        path = actual.get(rel)
        actual_sha = _sha256(path) if path is not None and path.is_file() else None
        expected_sha = expected.get(rel)
        match = (
            path is not None
            and expected_sha is not None
            and actual_sha == expected_sha
        )
        file_checks[rel] = {
            "expected_sha256": expected_sha,
            "actual_sha256": actual_sha,
            "match": match,
        }
        if not match:
            failures.append(f"file_checksum_mismatch:{rel}")

    manifest_path = root / "release_manifest.json"
    manifest = _load_json(manifest_path) if manifest_path.is_file() else {}
    if not isinstance(manifest, dict):
        manifest = {}
        failures.append("release_manifest_invalid")
    if manifest.get("receipt") != RECEIPT_TYPE:
        failures.append("release_manifest_wrong_receipt")
    if manifest.get("status") != "RELEASE_PACKAGE_READY":
        failures.append("release_manifest_not_ready")
    if manifest.get("network_count") != 3:
        failures.append("release_manifest_network_count_mismatch")
    if manifest.get("scientific_claim_allowed_by_archive_alone") is not False:
        failures.append("release_manifest_claim_guard_missing")
    if manifest.get("automatic_manuscript_edit_permitted") is not False:
        failures.append("release_manifest_auto_edit_guard_missing")
    if manifest.get("third_network_must_be_retained") is not True:
        failures.append("release_manifest_retention_guard_missing")
    if manifest.get("existing_network_inputs_verified") is not True:
        failures.append("release_manifest_existing_network_guard_missing")
    if (
        manifest.get("existing_network_input_mode") == PRODUCTION_INPUT_MODE
        and manifest.get("existing_network_canonical_status")
        != EXISTING_K3_MATCH_STATUS
    ):
        failures.append("release_manifest_canonical_existing_network_guard_missing")

    declared_checks = _verify_declared_maps(root, manifest, failures)

    plan_path = root / "claim_transition_plan.json"
    plan = _load_json(plan_path) if plan_path.is_file() else {}
    if not isinstance(plan, dict):
        plan = {}
        failures.append("claim_transition_plan_invalid")
    if plan.get("automatic_manuscript_edit_permitted") is not False:
        failures.append("claim_transition_auto_edit_guard_missing")
    if plan.get("third_network_must_be_retained") is not True:
        failures.append("claim_transition_retention_guard_missing")
    if (
        manifest.get("claim_state") is not None
        and plan.get("claim_state") != manifest.get("claim_state")
    ):
        failures.append("claim_state_manifest_plan_mismatch")

    bundle_dir = root / "confirmatory_bundle"
    source_dir = root / "frozen_inputs"
    try:
        bundle_verification = verify_bundle(bundle_dir, source_dir=source_dir)
    except Exception as exc:  # read-only verifier must report rather than mask.
        bundle_verification = {
            "status": "CONFIRMATORY_BUNDLE_INVALID",
            "failures": [f"exception:{type(exc).__name__}"],
        }
        failures.append("nested_confirmatory_bundle_verifier_exception")
    if bundle_verification.get("status") != BUNDLE_VERIFIED_STATUS:
        failures.append("nested_confirmatory_bundle_invalid")

    inferred_zip = Path(str(root) + ".zip")
    inferred_sha = Path(str(inferred_zip) + ".sha256")
    archive_requested = (
        require_archive
        or zip_path is not None
        or sha256_receipt_path is not None
        or inferred_zip.exists()
        or inferred_sha.exists()
    )
    archive_verification: dict[str, object] | None = None
    archive_mode = "ZIP_NOT_RECHECKED"
    if archive_requested:
        archive_verification = _verify_zip(
            root,
            zip_path=Path(zip_path) if zip_path is not None else inferred_zip,
            sha_path=(
                Path(sha256_receipt_path)
                if sha256_receipt_path is not None
                else inferred_sha
            ),
            failures=failures,
        )
        archive_mode = "ZIP_RECHECKED"

    status = VERIFIED_STATUS if not failures else INVALID_STATUS
    return {
        "receipt": "BITA_THIRD_NETWORK_RELEASE_PACKAGE_VERIFICATION_V1",
        "status": status,
        "failures": sorted(set(failures)),
        "archive_recheck_mode": archive_mode,
        "file_checksum_manifest_sha256": (
            _sha256(checksum_path) if checksum_path.is_file() else None
        ),
        "file_checks": file_checks,
        "declared_manifest_checks": declared_checks,
        "nested_confirmatory_bundle_status": bundle_verification.get("status"),
        "nested_confirmatory_bundle_failures": bundle_verification.get("failures", []),
        "archive_verification": archive_verification,
        "claim_boundary": (
            "This read-only gate verifies release integrity and frozen claim guards. "
            "It does not recompute the scientific estimand or alter manuscript claims."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_dir")
    parser.add_argument("--zip")
    parser.add_argument("--sha256-receipt")
    parser.add_argument("--require-archive", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = verify_release_package(
        args.release_dir,
        zip_path=args.zip,
        sha256_receipt_path=args.sha256_receipt,
        require_archive=args.require_archive,
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
