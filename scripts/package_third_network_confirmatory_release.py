"""Build a deterministic archival package for a completed third-network analysis.

Production is the default. Development/synthetic bundles are accepted only when
explicitly requested with --development-only.

The resulting directory and ZIP contain:
- the complete verified confirmatory bundle;
- the exact six frozen third-network source inputs;
- the retained-result claim-transition plan;
- frozen protocol documents;
- the minimal code needed for offline scientific replay;
- complete per-file SHA256 receipts.

The ZIP uses sorted paths, fixed member metadata and ZIP_STORED members so
identical frozen inputs and repository code produce identical ZIP bytes without
depending on zlib compression behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.plan_third_network_claim_transition import (
    PRODUCTION_INPUT_MODE,
    plan_claim_transition,
)
from scripts.run_third_network_confirmatory_pipeline import (
    _current_checkout_commit,
)
from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS,
    verify,
)

RECEIPT = "BITA_THIRD_NETWORK_CONFIRMATORY_RELEASE_PACKAGE_V1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_SOURCE_KEYS = {
    "events",
    "plant_traits",
    "mammal_traits",
    "camera_deployment",
    "confirmatory_freeze",
    "field_readiness",
}
CODE_MANIFEST = (
    "empirical/floral_defence_selectivity/"
    "THIRD_NETWORK_RELEASE_CODE_MANIFEST_V1.txt"
)
PROTOCOL_FILES = (
    "empirical/floral_defence_selectivity/THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_PROSPECTIVE_MAMMAL_DESIGN_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_ROUTE_CODING_MANUAL_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_PILOT_SPLIT_CONTRACT_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_SEED_RECEIPT_V1.json",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_CONFIRMATORY_ANALYSIS_RUNNER_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_CLAIM_TRANSITION_GATE_V1.md",
    "empirical/floral_defence_selectivity/THIRD_NETWORK_RELEASE_REHEARSAL_V1.md",
    CODE_MANIFEST,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _safe_relative_file(value: str, *, label: str) -> Path:
    text = str(value).strip().replace("\\", "/")
    path = Path(text)
    if (
        not text
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or path.name in {"", ".", ".."}
    ):
        raise ValueError(f"UNSAFE_{label.upper()}_PATH: {value!r}")
    return path


def _prepare_output(
    output_dir: str | Path,
) -> tuple[Path, Path, Path, Path, Path, Path]:
    final = Path(output_dir)
    final.parent.mkdir(parents=True, exist_ok=True)
    staging = final.with_name(final.name + ".inprogress")
    zip_path = (
        final.with_suffix(final.suffix + ".zip")
        if final.suffix
        else Path(str(final) + ".zip")
    )
    sha_path = Path(str(zip_path) + ".sha256")
    zip_tmp = Path(str(zip_path) + ".inprogress")
    sha_tmp = Path(str(sha_path) + ".inprogress")

    for candidate, label in (
        (final, "RELEASE_OUTPUT"),
        (staging, "RELEASE_STAGING"),
        (zip_path, "RELEASE_ZIP"),
        (sha_path, "RELEASE_ZIP_SHA"),
        (zip_tmp, "RELEASE_ZIP_STAGING"),
        (sha_tmp, "RELEASE_ZIP_SHA_STAGING"),
    ):
        if candidate.exists():
            if candidate == final and candidate.is_dir() and not any(candidate.iterdir()):
                candidate.rmdir()
            else:
                raise ValueError(f"{label}_EXISTS: {candidate}")

    staging.mkdir(parents=False, exist_ok=False)
    return final, staging, zip_path, zip_tmp, sha_path, sha_tmp


def _remove_if_exists(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _publish_release_transaction(
    *,
    staging: Path,
    final: Path,
    zip_tmp: Path,
    zip_path: Path,
    sha_tmp: Path,
    sha_path: Path,
) -> None:
    """Publish the three release products as one rollback-safe transaction.

    Filesystems do not provide an atomic multi-path rename. We therefore stage
    every product first, publish only after all bytes are complete, and roll back
    every already-published path if any later rename fails. Because _prepare_output
    refuses pre-existing targets, rollback cannot delete a prior valid release.
    """

    try:
        staging.replace(final)
        zip_tmp.replace(zip_path)
        sha_tmp.replace(sha_path)
    except Exception:
        # Remove both unpublished staging paths and any products that were
        # already promoted before the injected/real failure occurred.
        for candidate in (
            sha_tmp,
            zip_tmp,
            sha_path,
            zip_path,
            final,
            staging,
        ):
            _remove_if_exists(candidate)
        raise


def _copy_file(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise ValueError(f"REQUIRED_RELEASE_FILE_MISSING: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _copy_bundle(bundle_dir: Path, destination: Path) -> None:
    if not bundle_dir.is_dir():
        raise ValueError("CONFIRMATORY_BUNDLE_DIR_MISSING")
    shutil.copytree(bundle_dir, destination)


def _copy_frozen_inputs(
    *,
    bundle_dir: Path,
    source_dir: Path,
    destination: Path,
) -> dict[str, dict[str, object]]:
    manifest_path = bundle_dir / "input_freeze_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", {})
    if not isinstance(files, dict) or set(files) != EXPECTED_SOURCE_KEYS:
        raise ValueError("INPUT_FREEZE_SOURCE_FILE_SET_MISMATCH")

    seen_filenames: set[str] = set()
    copied: dict[str, dict[str, object]] = {}
    for key in sorted(EXPECTED_SOURCE_KEYS):
        entry = files.get(key, {})
        if not isinstance(entry, dict):
            raise ValueError(f"INPUT_FREEZE_SOURCE_ENTRY_INVALID:{key}")
        filename_path = _safe_relative_file(
            str(entry.get("filename", "")),
            label="frozen_input",
        )
        if len(filename_path.parts) != 1:
            raise ValueError(f"FROZEN_INPUT_FILENAME_MUST_BE_BASENAME:{key}")
        filename = filename_path.name
        if filename in seen_filenames:
            raise ValueError(f"DUPLICATE_FROZEN_INPUT_FILENAME:{filename}")
        seen_filenames.add(filename)

        expected = str(entry.get("sha256", "")).strip().lower()
        source = source_dir / filename
        if not source.is_file():
            raise ValueError(f"FROZEN_SOURCE_FILE_MISSING:{key}")
        actual = _sha256(source)
        if actual != expected:
            raise ValueError(f"FROZEN_SOURCE_HASH_MISMATCH:{key}")

        target = destination / filename
        _copy_file(source, target)
        copied[key] = {
            "filename": filename,
            "sha256": actual,
        }
    return copied


def _copy_code(repo_root: Path, destination: Path) -> dict[str, str]:
    manifest_path = repo_root / CODE_MANIFEST
    if not manifest_path.is_file():
        raise ValueError("THIRD_NETWORK_RELEASE_CODE_MANIFEST_MISSING")

    entries = [
        line.strip()
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not entries or len(entries) != len(set(entries)):
        raise ValueError("THIRD_NETWORK_RELEASE_CODE_MANIFEST_INVALID")

    copied: dict[str, str] = {}
    for raw in entries:
        rel = _safe_relative_file(raw, label="code_manifest")
        source = repo_root / rel
        target = destination / rel
        _copy_file(source, target)
        copied[rel.as_posix()] = _sha256(target)
    return copied


def _copy_protocol(repo_root: Path, destination: Path) -> dict[str, str]:
    copied: dict[str, str] = {}
    for raw in PROTOCOL_FILES:
        rel = _safe_relative_file(raw, label="protocol")
        source = repo_root / rel
        target = destination / rel.name
        if target.name in copied:
            raise ValueError(f"DUPLICATE_PROTOCOL_BASENAME:{target.name}")
        _copy_file(source, target)
        copied[target.name] = _sha256(target)
    return copied


def _readme(*, development_only: bool) -> str:
    mode = "DEVELOPMENT_ONLY_SYNTHETIC" if development_only else "PRODUCTION_CONFIRMATORY"
    return f"""# BITA third-network confirmatory release package

Package mode: **{mode}**

This archive is self-contained for replay of the frozen third-network and equal-network k=3 scientific outputs.

## Contents

- `confirmatory_bundle/` — verified analysis outputs, exact Sakhalkar/Aubert k=3 inputs, and bundle receipts.
- `frozen_inputs/` — exact six third-network source inputs referenced by the input-freeze manifest.
- `claim_transition_plan.json` — retained-result reporting plan.
- `protocol/` — preregistration, route coding, seeds, runner and claim boundaries.
- `code/` — minimal replay code frozen by the release code manifest.
- `release_manifest.json` — package provenance.
- `FILE_SHA256SUMS.txt` — SHA256 for every other package file.

## Offline replay

From the extracted archive root:

~~~bash
PYTHONPATH=code python code/scripts/reproduce_third_network_confirmatory_release.py . \
  --output reproduction.json
~~~

A valid replay exits successfully with:

~~~text
REPRODUCTION_MATCH
~~~

No public-data download is required because the exact Sakhalkar and Aubert/EPHI analysis rows entering k=3 are included in the confirmatory bundle.

## Claim boundary

This package preserves the analysis and reporting contract. It does not itself edit the manuscript or broaden the frozen k=3 claim ceiling.
"""


def _write_checksums(root: Path) -> Path:
    checksum = root / "FILE_SHA256SUMS.txt"
    lines: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        if not path.is_file() or path == checksum:
            continue
        rel = path.relative_to(root).as_posix()
        lines.append(f"{_sha256(path)}  {rel}")
    checksum.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum


def _deterministic_zip(root: Path, output_zip: Path) -> None:
    """Write a byte-stable ZIP without compression-library dependence."""
    fixed_time = (1980, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(
        output_zip,
        "w",
        compression=zipfile.ZIP_STORED,
    ) as archive:
        for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(rel, date_time=fixed_time)
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_STORED)


def package_release(
    *,
    bundle_dir: str | Path,
    source_dir: str | Path,
    output_dir: str | Path,
    development_only: bool = False,
    repo_root: str | Path | None = None,
) -> dict[str, object]:
    bundle = Path(bundle_dir)
    source = Path(source_dir)
    repo = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[1]

    verification = verify(bundle, source_dir=source)
    if verification["status"] != VERIFIED_STATUS:
        raise ValueError(
            "CONFIRMATORY_BUNDLE_NOT_VERIFIED: "
            + ",".join(str(x) for x in verification.get("failures", []))
        )

    receipt_path = bundle / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict):
        raise ValueError("CONFIRMATORY_RECEIPT_INVALID")

    mode = str(receipt.get("existing_network_input_mode", "")).strip()
    repository_commit = str(receipt.get("repository_commit", "")).strip().lower()

    if not development_only:
        if mode != PRODUCTION_INPUT_MODE:
            raise ValueError("NONPRODUCTION_CONFIRMATORY_BUNDLE")
        if not HEX40.fullmatch(repository_commit):
            raise ValueError("PRODUCTION_RECEIPT_REPOSITORY_COMMIT_INVALID")
        current = _current_checkout_commit()
        if current is None:
            raise ValueError("PRODUCTION_CHECKOUT_COMMIT_UNRESOLVED")
        if current != repository_commit:
            raise ValueError(
                f"PRODUCTION_RELEASE_COMMIT_MISMATCH: receipt={repository_commit} current={current}"
            )

    claim_plan = plan_claim_transition(
        receipt,
        bundle_verification_status=str(verification["status"]),
        source_recheck_mode=str(verification["source_recheck_mode"]),
        production_required=not development_only,
    )

    final, staging, zip_path, zip_tmp, sha_path, sha_tmp = _prepare_output(output_dir)

    try:
        _copy_bundle(bundle, staging / "confirmatory_bundle")
        frozen_inputs = _copy_frozen_inputs(
            bundle_dir=bundle,
            source_dir=source,
            destination=staging / "frozen_inputs",
        )
        code_hashes = _copy_code(repo, staging / "code")
        protocol_hashes = _copy_protocol(repo, staging / "protocol")

        _write_json(staging / "claim_transition_plan.json", claim_plan)
        (staging / "README.md").write_text(
            _readme(development_only=development_only),
            encoding="utf-8",
        )

        existing_checks = verification.get("existing_network_checks", {})
        existing_verified = (
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
        if not existing_verified:
            raise ValueError("EXISTING_NETWORK_INPUTS_NOT_VERIFIED")

        release_manifest = {
            "receipt": RECEIPT,
            "status": "RELEASE_PACKAGE_READY",
            "mode": (
                "DEVELOPMENT_ONLY_SYNTHETIC"
                if development_only
                else "PRODUCTION_CONFIRMATORY"
            ),
            "scientific_claim_allowed_by_archive_alone": False,
            "claim_transition_plan_ready": True,
            "automatic_manuscript_edit_permitted": False,
            "repository_commit": repository_commit,
            "existing_network_input_mode": mode,
            "network_count": 3,
            "archive_zip_method": "ZIP_STORED",
            "archive_member_order": "LEXICOGRAPHIC_RELATIVE_PATH",
            "archive_member_timestamp": "1980-01-01T00:00:00",
            "archive_byte_determinism_contract": (
                "Identical package files produce identical ZIP bytes without zlib compression."
            ),
            "third_network_direction": claim_plan["third_network_direction"],
            "claim_state": claim_plan["claim_state"],
            "third_network_must_be_retained": claim_plan[
                "third_network_must_be_retained"
            ],
            "bundle_verification_status": verification["status"],
            "source_recheck_mode": verification["source_recheck_mode"],
            "analysis_receipt_sha256": verification[
                "analysis_receipt_sha256"
            ],
            "bundle_checksum_manifest_sha256": verification[
                "bundle_checksum_manifest_sha256"
            ],
            "existing_network_inputs_verified": existing_verified,
            "frozen_inputs": frozen_inputs,
            "code_files": code_hashes,
            "protocol_files": protocol_hashes,
            "claim_boundary": (
                "Archive readiness preserves a verified retained third-network result "
                "and its frozen reporting ceiling. It does not perform manuscript edits."
            ),
        }
        _write_json(staging / "release_manifest.json", release_manifest)
        checksum = _write_checksums(staging)

        _deterministic_zip(staging, zip_tmp)
        zip_sha = _sha256(zip_tmp)
        sha_tmp.write_text(
            f"{zip_sha}  {zip_path.name}\n",
            encoding="utf-8",
        )

        _publish_release_transaction(
            staging=staging,
            final=final,
            zip_tmp=zip_tmp,
            zip_path=zip_path,
            sha_tmp=sha_tmp,
            sha_path=sha_path,
        )

        return {
            **release_manifest,
            "release_dir": str(final),
            "zip_path": str(zip_path),
            "zip_sha256": zip_sha,
            "zip_sha256_receipt": str(sha_path),
            "file_checksum_manifest_sha256": _sha256(
                final / checksum.name
            ),
        }

    except Exception:
        # This cleanup is idempotent with _publish_release_transaction and also
        # covers failures that occur before publication begins.
        for candidate in (
            sha_tmp,
            zip_tmp,
            sha_path,
            zip_path,
            final,
            staging,
        ):
            _remove_if_exists(candidate)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--development-only", action="store_true")
    args = parser.parse_args()

    result = package_release(
        bundle_dir=args.bundle_dir,
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        development_only=args.development_only,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
