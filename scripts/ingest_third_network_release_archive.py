"""Safely ingest a third-network confirmatory release ZIP.

Sequence:
1. verify adjacent ZIP SHA256 receipt;
2. inspect ZIP paths, duplicate members, fixed metadata and internal
   FILE_SHA256SUMS before writing any archive member;
3. extract only verified regular files into a private staging directory;
4. run the full release-package verifier against staging + original ZIP;
5. atomically publish the extracted directory only after all checks pass.

No scientific replay is performed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

from scripts.verify_third_network_release_package import (
    FIXED_ZIP_MODE,
    FIXED_ZIP_TIME,
    HEX64,
    VERIFIED_STATUS,
    _safe_rel,
    verify_release_package,
)

INGEST_RECEIPT = "BITA_THIRD_NETWORK_RELEASE_ARCHIVE_INGEST_V1"
INGEST_READY = "RELEASE_ARCHIVE_INGESTED_VERIFIED"
INGEST_INVALID = "RELEASE_ARCHIVE_INGEST_INVALID"
CHECKSUM_NAME = "FILE_SHA256SUMS.txt"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_checksum_text(text: str, failures: list[str]) -> dict[str, str]:
    expected: dict[str, str] = {}
    for raw in text.splitlines():
        if not raw.strip():
            continue
        parts = raw.split("  ", 1)
        if len(parts) != 2:
            failures.append("archive_checksum_manifest_malformed")
            continue
        digest = parts[0].strip().lower()
        rel = parts[1].strip().replace("\\", "/")
        if (
            HEX64.fullmatch(digest) is None
            or not _safe_rel(rel)
            or rel == CHECKSUM_NAME
            or rel in expected
        ):
            failures.append("archive_checksum_manifest_malformed")
            continue
        expected[rel] = digest
    return expected


def inspect_archive_shell(
    zip_path: str | Path,
    sha256_receipt_path: str | Path,
) -> dict[str, object]:
    archive_path = Path(zip_path)
    sha_path = Path(sha256_receipt_path)
    failures: list[str] = []

    if not archive_path.is_file():
        failures.append("release_zip_missing")
    if not sha_path.is_file():
        failures.append("release_zip_sha256_receipt_missing")
    if failures:
        return {
            "receipt": INGEST_RECEIPT,
            "status": INGEST_INVALID,
            "failures": failures,
        }

    zip_sha = _sha256(archive_path)
    lines = [line for line in sha_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    receipt_match = False
    expected_zip_sha: str | None = None
    if len(lines) != 1:
        failures.append("release_zip_sha256_receipt_malformed")
    else:
        parts = lines[0].split("  ", 1)
        if len(parts) == 2:
            expected_zip_sha = parts[0].strip().lower()
            expected_name = parts[1].strip()
            receipt_match = (
                HEX64.fullmatch(expected_zip_sha) is not None
                and expected_name == archive_path.name
                and expected_zip_sha == zip_sha
            )
        if not receipt_match:
            failures.append("release_zip_sha256_receipt_mismatch")

    member_checks: dict[str, dict[str, object]] = {}
    internal_checksums: dict[str, str] = {}
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            if archive.comment != b"":
                failures.append("release_zip_archive_comment_forbidden")

            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                failures.append("release_zip_duplicate_member")
            if any(not _safe_rel(name) for name in names):
                failures.append("release_zip_unsafe_member")

            info_by_name = {info.filename: info for info in infos}
            checksum_info = info_by_name.get(CHECKSUM_NAME)
            if checksum_info is None:
                failures.append("archive_checksum_manifest_missing")
            else:
                try:
                    checksum_text = archive.read(checksum_info).decode("utf-8")
                except (UnicodeDecodeError, RuntimeError, KeyError):
                    failures.append("archive_checksum_manifest_unreadable")
                    checksum_text = ""
                internal_checksums = _parse_checksum_text(checksum_text, failures)

            expected_members = set(internal_checksums) | {CHECKSUM_NAME}
            if set(names) != expected_members:
                failures.append("archive_internal_inventory_mismatch")

            for info in infos:
                name = info.filename
                safe = _safe_rel(name)
                unix_mode = (info.external_attr >> 16) & 0xFFFF
                regular_file = stat.S_IFMT(unix_mode) == stat.S_IFREG
                metadata_match = (
                    safe
                    and info.create_system == 3
                    and unix_mode == FIXED_ZIP_MODE
                    and regular_file
                    and info.compress_type == zipfile.ZIP_STORED
                    and info.date_time == FIXED_ZIP_TIME
                    and (info.flag_bits & 0x1) == 0
                    and info.extra == b""
                    and info.comment == b""
                    and not info.is_dir()
                )

                try:
                    payload = archive.read(info) if safe else b""
                    readable = safe
                except (RuntimeError, KeyError, zipfile.BadZipFile):
                    payload = b""
                    readable = False

                expected_sha = internal_checksums.get(name)
                actual_sha = _sha256_bytes(payload) if readable else None
                checksum_match = (
                    name == CHECKSUM_NAME
                    or (
                        expected_sha is not None
                        and actual_sha is not None
                        and expected_sha == actual_sha
                    )
                )
                member_checks[name] = {
                    "safe_path": safe,
                    "metadata_match": metadata_match,
                    "expected_sha256": expected_sha,
                    "actual_sha256": actual_sha,
                    "checksum_match": checksum_match,
                }
                if not metadata_match:
                    failures.append(f"release_zip_member_metadata_mismatch:{name}")
                if not checksum_match:
                    failures.append(f"archive_internal_checksum_mismatch:{name}")

    except (OSError, zipfile.BadZipFile, RuntimeError, KeyError) as exc:
        failures.append(f"release_zip_unreadable:{type(exc).__name__}")

    return {
        "receipt": INGEST_RECEIPT,
        "status": INGEST_READY if not failures else INGEST_INVALID,
        "failures": sorted(set(failures)),
        "zip_path": str(archive_path),
        "sha256_receipt_path": str(sha_path),
        "actual_zip_sha256": zip_sha,
        "expected_zip_sha256": expected_zip_sha,
        "sha256_receipt_match": receipt_match,
        "internal_checksum_entries": len(internal_checksums),
        "member_checks": member_checks,
        "claim_boundary": (
            "This pre-extraction gate verifies archive transport and internal file integrity only. "
            "It does not establish the scientific result or permit manuscript claim changes."
        ),
    }


def ingest_release_archive(
    zip_path: str | Path,
    sha256_receipt_path: str | Path,
    output_dir: str | Path,
) -> dict[str, object]:
    archive_path = Path(zip_path)
    sha_path = Path(sha256_receipt_path)
    output = Path(output_dir)

    if output.exists():
        raise ValueError(f"OUTPUT_ALREADY_EXISTS: {output}")

    shell = inspect_archive_shell(archive_path, sha_path)
    if shell["status"] != INGEST_READY:
        raise ValueError(
            "ARCHIVE_SHELL_INVALID: " + ",".join(str(x) for x in shell["failures"])
        )

    staging = output.with_name(output.name + ".staging")
    if staging.exists():
        raise ValueError(f"STALE_STAGING_EXISTS: {staging}")

    try:
        staging.mkdir(parents=True, exist_ok=False)
        with zipfile.ZipFile(archive_path, "r") as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                rel = info.filename
                if not _safe_rel(rel):
                    raise ValueError(f"UNSAFE_MEMBER_AFTER_SHELL_VERIFY: {rel}")
                destination = staging.joinpath(*rel.split("/"))
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    raise ValueError(f"DUPLICATE_EXTRACTION_TARGET: {rel}")
                destination.write_bytes(archive.read(info))
                destination.chmod(0o644)

        full = verify_release_package(
            staging,
            zip_path=archive_path,
            sha256_receipt_path=sha_path,
            require_archive=True,
        )
        if full["status"] != VERIFIED_STATUS:
            raise ValueError(
                "EXTRACTED_RELEASE_INVALID: "
                + ",".join(str(x) for x in full.get("failures", []))
            )

        staging.replace(output)
        return {
            "receipt": INGEST_RECEIPT,
            "status": INGEST_READY,
            "output_dir": str(output),
            "zip_sha256": shell["actual_zip_sha256"],
            "pre_extraction_shell_status": shell["status"],
            "full_release_verification_status": full["status"],
            "scientific_claim_allowed_by_ingest_alone": False,
            "claim_boundary": (
                "The archive was verified before extraction and the extracted release passed "
                "the full read-only package verifier. Scientific replay and claim transition remain separate."
            ),
        }
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if output.exists():
            shutil.rmtree(output)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_zip")
    parser.add_argument("sha256_receipt")
    parser.add_argument("output_dir")
    parser.add_argument("--receipt")
    args = parser.parse_args()

    result = ingest_release_archive(
        args.release_zip,
        args.sha256_receipt,
        args.output_dir,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        path = Path(args.receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
