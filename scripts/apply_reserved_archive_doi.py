"""Apply a reserved Zenodo DOI to the access-routing Letter submission state.

This is intentionally deterministic and fail-closed. It accepts only Zenodo
record DOIs, updates the fixed submission surfaces, and writes a machine-readable
reservation receipt. Re-running with the same DOI is idempotent; attempting to
replace a different reserved DOI is rejected.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = ROOT / "submission" / "access_routing_archive" / "RESERVED_DOI_RECEIPT.json"
RECEIPT_TYPE = "BITA_ACCESS_ROUTING_RESERVED_DOI_V1"
RESERVED_STATUS = "ZENODO_DOI_RESERVED_PENDING_PUBLICATION"
DOI_RE = re.compile(r"^10\.5281/zenodo\.(\d+)$", re.IGNORECASE)
SOURCE_DATASET_DOIS = frozenset(("10.5281/zenodo.8398202", "10.5281/zenodo.14185547"))

TARGETS = (
    "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
    "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
    "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md",
    "docs/PUBLICATION_STATUS.md",
    "docs/SUBMISSION_SCOPE.md",
    "submission/access_routing_archive/README.md",
    "submission/access_routing_archive/ZENODO_METADATA_TEMPLATE.md",
)


def normalize_zenodo_doi(value: str) -> str:
    text = str(value).strip()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^doi:\s*", "", text, flags=re.IGNORECASE)
    match = DOI_RE.fullmatch(text)
    if match is None:
        raise ValueError("RESERVED_DOI_MUST_BE_ZENODO_RECORD_DOI")
    doi = f"10.5281/zenodo.{match.group(1)}"
    if doi in SOURCE_DATASET_DOIS:
        raise ValueError("SOURCE_DATASET_DOI_CANNOT_BE_REUSED_AS_BITA_ARCHIVE_DOI")
    return doi


def _replace_once_or_already(text: str, old: str, new: str, *, label: str) -> str:
    if old in text:
        return text.replace(old, new)
    if new in text:
        return text
    raise ValueError(f"DOI_TARGET_NOT_FOUND:{label}")


def _set_doi_status(
    text: str, *, field: str, allowed_old: tuple[str, ...], label: str
) -> str:
    """Replace exactly one full status assignment, rejecting unrecognized drift."""
    pattern = re.compile(rf"(?m)^{re.escape(field)} = ([A-Z][A-Z0-9_]*)$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"DOI_TARGET_NOT_FOUND:{label}")
    match = matches[0]
    old_value = match.group(1)
    new_value = "RESERVED_PENDING_ZENODO_PUBLICATION"
    if old_value == new_value:
        return text
    if old_value not in allowed_old:
        raise ValueError(f"DOI_TARGET_NOT_FOUND:{label}:{old_value}")
    return (
        text[:match.start()]
        + f"{field} = {new_value}"
        + text[match.end():]
    )


def transform(path: str, text: str, doi: str) -> str:
    if path == "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md":
        return _replace_once_or_already(
            text,
            "[ACCESS-ROUTING ARCHIVE DOI]",
            doi,
            label=path,
        )

    if path == "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md":
        text = _replace_once_or_already(
            text,
            "[ACCESS-ROUTING ARCHIVE DOI]",
            doi,
            label=f"{path}:doi",
        )
        return _replace_once_or_already(
            text,
            "**ARCHIVE DOI REQUIRED BEFORE SUBMISSION.**",
            "**ZENODO RECORD MUST BE PUBLISHED AND DOI RESOLVING BEFORE SUBMISSION.**",
            label=f"{path}:gate",
        )

    if path == "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md":
        return _replace_once_or_already(
            text,
            "[ACCESS-ROUTING ARCHIVE DOI — REQUIRED BEFORE SUBMISSION]",
            doi,
            label=path,
        )

    if path == "docs/PUBLICATION_STATUS.md":
        text = _set_doi_status(
            text,
            field="ACCESS_ROUTING_ARCHIVE_DOI",
            allowed_old=(
                "RESERVE_IN_ZENODO_DRAFT_BEFORE_FINAL_PACKAGE_BUILD",
                "NOT_YET_RESERVED",
            ),
            label=f"{path}:doi_status",
        )
        marker = "ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_PENDING_ZENODO_PUBLICATION"
        exact = f"RESERVED_ARCHIVE_DOI = {doi}"
        if exact not in text:
            text = text.replace(marker, marker + "\n" + exact, 1)
        text = text.replace(
            "DATA_CODE_ARCHIVE = STAGING_READY_RESERVED_DOI_THEN_FINAL_BUILD",
            "DATA_CODE_ARCHIVE = RESERVED_DOI_FINAL_BUILD_REQUIRED",
        )
        return text

    if path == "docs/SUBMISSION_SCOPE.md":
        text = _set_doi_status(
            text,
            field="ARCHIVE_DOI",
            allowed_old=(
                "REQUIRED",
                "RESERVE_IN_ZENODO_DRAFT_BEFORE_FINAL_PACKAGE_BUILD",
            ),
            label=f"{path}:doi_status",
        )
        marker = "ARCHIVE_DOI = RESERVED_PENDING_ZENODO_PUBLICATION"
        exact = f"RESERVED_ARCHIVE_DOI = {doi}"
        if marker in text and exact not in text:
            text = text.replace(marker, marker + "\n" + exact, 1)
        text = text.replace(
            "DATA_CODE_ARCHIVE = STAGING_READY_DOI_REQUIRED",
            "DATA_CODE_ARCHIVE = RESERVED_DOI_FINAL_BUILD_REQUIRED",
        )
        return text

    if path == "submission/access_routing_archive/README.md":
        text = _replace_once_or_already(
            text,
            "ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_DOI_REQUIRED_BEFORE_FINAL_PACKAGE_BUILD",
            "ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_PENDING_ZENODO_PUBLICATION",
            label=f"{path}:status",
        )
        marker = "ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_PENDING_ZENODO_PUBLICATION"
        exact = f"RESERVED_ARCHIVE_DOI = {doi}"
        if exact not in text:
            text = text.replace(marker, marker + "\n" + exact, 1)
        return text

    if path == "submission/access_routing_archive/ZENODO_METADATA_TEMPLATE.md":
        old = "**DOI:** RESERVE IN ZENODO DRAFT BEFORE THE FINAL DOI-BEARING SUBMISSION COMMIT"
        new = f"**DOI:** {doi} — reserved in Zenodo draft; registered on publication"
        return _replace_once_or_already(text, old, new, label=path)

    raise ValueError(f"UNKNOWN_DOI_TARGET:{path}")


def _receipt(doi: str) -> dict[str, object]:
    return {
        "receipt": RECEIPT_TYPE,
        "status": RESERVED_STATUS,
        "doi": doi,
        "target_files": list(TARGETS),
        "final_archive_rule": (
            "Build the deposit ZIP from the exact DOI-bearing submission commit, "
            "upload it to the same Zenodo draft, verify SHA256, then publish."
        ),
        "automatic_submission_permitted": False,
    }


def apply_reserved_doi(root: Path, doi_value: str) -> dict[str, object]:
    """Validate every target before touching disk; roll back on write failure.

    An author-supplied DOI can be applied only to a fully consistent current
    submission checkout. No Zenodo publication or external submission occurs.
    """
    doi = normalize_zenodo_doi(doi_value)
    receipt_path = root / RECEIPT_PATH.relative_to(ROOT)

    old_receipt_bytes: bytes | None = None
    if receipt_path.is_file():
        old_receipt_bytes = receipt_path.read_bytes()
        existing = json.loads(old_receipt_bytes.decode("utf-8"))
        existing_doi = normalize_zenodo_doi(str(existing.get("doi", "")))
        if existing_doi != doi:
            raise ValueError("DIFFERENT_RESERVED_DOI_ALREADY_FROZEN")

    # Stage *all* changes in memory before the first file is mutated.
    original_bytes: dict[str, bytes] = {}
    replacements: dict[str, str] = {}
    for rel in TARGETS:
        path = root / rel
        raw = path.read_bytes()
        original_bytes[rel] = raw
        original = raw.decode("utf-8")
        updated = transform(rel, original, doi)
        if updated != original:
            replacements[rel] = updated

    receipt = _receipt(doi)
    payload = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    receipt_changed = old_receipt_bytes != payload
    changed = list(replacements)
    if receipt_changed:
        changed.append(str(RECEIPT_PATH.relative_to(ROOT)))

    # Write only after every source transformation has succeeded. Restore the
    # original files if a write or the final independent verification fails.
    try:
        for rel, updated in replacements.items():
            (root / rel).write_text(updated, encoding="utf-8")
        if receipt_changed:
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_bytes(payload)
        verify_reserved_doi(root)
    except Exception:
        for rel, original in original_bytes.items():
            path = root / rel
            if path.read_bytes() != original:
                path.write_bytes(original)
        if old_receipt_bytes is None:
            receipt_path.unlink(missing_ok=True)
        else:
            receipt_path.write_bytes(old_receipt_bytes)
        raise
    return {"doi": doi, "changed_files": changed, **receipt}


def verify_reserved_doi(root: Path) -> dict[str, object]:
    receipt_path = root / RECEIPT_PATH.relative_to(ROOT)
    if not receipt_path.is_file():
        return {
            "status": "ZENODO_DOI_NOT_RESERVED_YET",
            "receipt_present": False,
        }

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("receipt") != RECEIPT_TYPE:
        raise ValueError("WRONG_RESERVED_DOI_RECEIPT")
    if receipt.get("status") != RESERVED_STATUS:
        raise ValueError("RESERVED_DOI_RECEIPT_NOT_PENDING_PUBLICATION")
    doi = normalize_zenodo_doi(str(receipt.get("doi", "")))

    failures: list[str] = []
    for rel in TARGETS:
        text = (root / rel).read_text(encoding="utf-8")
        if doi not in text:
            failures.append(f"reserved_doi_missing:{rel}")

    placeholder_targets = (
        "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
        "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
        "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md",
    )
    for rel in placeholder_targets:
        text = (root / rel).read_text(encoding="utf-8")
        if "[ACCESS-ROUTING ARCHIVE DOI" in text:
            failures.append(f"archive_doi_placeholder_remains:{rel}")

    if failures:
        raise ValueError("RESERVED_DOI_VERIFICATION_FAILED:" + ",".join(failures))

    return {
        "status": "ZENODO_RESERVED_DOI_APPLIED",
        "receipt_present": True,
        "doi": doi,
        "failures": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    if args.check_only:
        result = verify_reserved_doi(args.root)
    else:
        if not args.doi:
            parser.error("--doi is required unless --check-only is used")
        result = apply_reserved_doi(args.root, args.doi)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
