#!/usr/bin/env python3
"""Offline, fail-closed stage-audit for a BITA Ecology Letters submission bundle.

This never registers/resolves a DOI or approves authorship, nor submits content.
For actual journal submission, independent Zenodo/author gates remain required.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

# Keep standalone `python scripts/audit_letter_release_gate.py` and pytest
# imports on the same strict author metadata contract.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_ecology_letters_letter_author_metadata import validate as validate_author_record

INNER = "access-routing-letter-data-code-v1.zip"
DIGEST = "access-routing-letter-data-code-v1.sha256"
DOCS = (
    "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
    "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
    "ECOLOGY_LETTERS_LETTER_COVER_V0.md",
)
SOURCE_DOIS = {"10.5281/zenodo.8398202", "10.5281/zenodo.14185547"}
AUTHOR_PLACEHOLDERS = (
    "[FINAL AUTHOR LIST",
    "[AUTHOR-CONTROLLED",
    "AUTHOR-CONTROLLED BEFORE SUBMISSION",
    "[postal address; telephone;",
    "[Affiliation, postal address, telephone number",
)


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _read(zf: zipfile.ZipFile, name: str, errors: list[str]) -> bytes | None:
    try:
        return zf.read(name)
    except KeyError:
        errors.append("MISSING_REQUIRED_FILE:" + name)
        return None


def _optional(zf: zipfile.ZipFile, name: str) -> bytes | None:
    try:
        return zf.read(name)
    except KeyError:
        return None


def _inner_check(zf: zipfile.ZipFile, errors: list[str]) -> dict:
    raw = _read(zf, "data_archive/FILE_SHA256SUMS.txt", errors)
    if raw is None:
        return {"listed": 0, "files": 0, "verified": 0, "bad": ["MISSING_MANIFEST"]}
    names = {info.filename for info in zf.infolist() if not info.is_dir()}
    tracked, bad = set(), []
    lines = [line for line in raw.decode("utf-8").splitlines() if line.strip()]
    for line in lines:
        match = re.fullmatch(r"([a-f0-9]{64})  \./([\w./-]+)", line)
        if not match:
            bad.append("MALFORMED_CHECKSUM_LINE")
            continue
        digest, rel = match.groups()
        path = "data_archive/" + rel
        if ".." in rel.split("/") or path not in names or path in tracked:
            bad.append("INVALID_CHECKSUM_ENTRY:" + path)
            continue
        tracked.add(path)
        if _sha(zf.read(path)) != digest:
            bad.append("BAD_SHA256:" + path)
    for name in names - tracked - {"data_archive/FILE_SHA256SUMS.txt"}:
        bad.append("UNLISTED:" + name)
    if bad:
        errors.append("INNER_ARCHIVE_CHECKSUM_MISMATCH")
    return {"listed": len(lines), "files": len(names), "verified": len(tracked) - sum(v.startswith("BAD_SHA256:") for v in bad), "bad": sorted(bad)}


def _author_check(path: Path) -> dict:
    """Use the exact Letter author-schema validator, not a weaker proxy.

    Reporting only field-presence used to accept arbitrary nonempty author lists
    and nonempty affiliation objects, even without a corresponding author,
    affiliation links, author emails, or valid metadata schema. The downstream
    release receipt must never call those author records complete.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("AUTHOR_METADATA_ROOT_MUST_BE_OBJECT")
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        return {
            "complete": False,
            "missing": ["METADATA_FILE_UNREADABLE"],
            "invalid": [],
            "error": str(exc),
        }
    report = validate_author_record(data)
    return {
        "complete": report["ready_for_submission_metadata_application"],
        "missing": report["missing"],
        "invalid": report["invalid"],
    }


def _author_surface_mismatches(metadata_path: Path, documents: dict[str, str]) -> list[str]:
    """Compare fully approved author JSON with the actual submission surfaces.

    Author values are intentionally NOT returned in audit receipts or logs.
    This runs only after the separate schema validator reports completion.
    """
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    title = documents.get("ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md", "")
    cover = documents.get("ECOLOGY_LETTERS_LETTER_COVER_V0.md", "")
    mismatches: list[str] = []

    def field(document: str, label: str) -> str:
        found = re.search(r"(?m)^\\*\\*" + re.escape(label) + r":\\*\\*\\s*(.*)$", document)
        return found.group(1).strip() if found else ""

    authors = data["authors"]
    names = [author["name"].strip() for author in authors]
    title_names = [
        name.strip() for name in field(title, "Authors").split(";") if name.strip()
    ]
    if names != title_names:
        mismatches.append("title.authors")

    affiliation_line = field(title, "Affiliations and author e-mail addresses")
    for index, author in enumerate(authors, start=1):
        if author["email"].strip() not in affiliation_line:
            mismatches.append(f"title.authors[{index}].email")
        for affiliation_id in author["affiliation_ids"]:
            affiliation = data["affiliations"][str(affiliation_id)].strip()
            if affiliation not in affiliation_line:
                mismatches.append(f"title.authors[{index}].affiliation")

    correspondent = next(author["name"].strip() for author in authors if author["corresponding"])
    if correspondent not in field(title, "Corresponding author"):
        mismatches.append("title.corresponding_author")
    contact_line = field(title, "Complete correspondence address")
    for key in ("postal_address", "telephone", "email"):
        if data["correspondence"][key].strip() not in contact_line:
            mismatches.append(f"title.correspondence.{key}")

    fields = (
        ("authorship_statement", "Statement of authorship"),
        ("funding_statement", "Funding"),
        ("acknowledgments", "Acknowledgments"),
        ("conflict_of_interest_statement", "Conflict of interest"),
        ("ai_assisted_workflow_disclosure", "AI-assisted workflow disclosure"),
    )
    for key, label in fields:
        if data[key].strip() not in field(title, label):
            mismatches.append("title." + key)

    if data["author_relative_novelty_statement"].strip() not in cover:
        mismatches.append("cover.author_relative_novelty_statement")
    if data["conflict_of_interest_statement"].strip() not in cover:
        mismatches.append("cover.conflict_of_interest_statement")
    signoff = cover.split("Best regards,", 1)
    if len(signoff) != 2:
        mismatches.append("cover.corresponding_author_signature")
    else:
        first_line = next(
            (line.strip() for line in signoff[1].splitlines() if line.strip()), ""
        )
        if first_line != correspondent:
            mismatches.append("cover.corresponding_author_signature")
    return sorted(set(mismatches))


def audit_package(package_zip: Path, author_metadata_json: Path, *, expected_head_sha: str | None = None) -> dict:
    """Audit package contents offline; never declare DOI publication verified."""
    errors: list[str] = []
    source_commit = None
    inner_summary: dict = {}
    receipt = None
    documents = {}
    with zipfile.ZipFile(package_zip) as zf:
        data = _read(zf, INNER, errors)
        checksum = _read(zf, DIGEST, errors)
        if data is None or checksum is None or checksum.decode("utf-8").split()[0] != _sha(data):
            errors.append("OUTER_ARCHIVE_SHA256_MISMATCH")
        for doc in DOCS:
            raw = _read(zf, doc, errors)
            documents[doc] = raw.decode("utf-8") if raw is not None else ""
        if data is not None:
            with zipfile.ZipFile(io.BytesIO(data)) as inner:
                inner_summary = _inner_check(inner, errors)
                commit = _read(inner, "data_archive/REPOSITORY_COMMIT.txt", errors)
                source_commit = commit.decode("utf-8").strip() if commit else None
                manifest_raw = _read(inner, "data_archive/archive_manifest.json", errors)
                if manifest_raw is not None:
                    manifest = json.loads(manifest_raw)
                    if manifest.get("archive_schema") != "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V5" or manifest.get("analysis_tables") != {
                        "aubert_ephi_pair_site_analysis.csv": 2265,
                        "aubert_ephi_participation_opportunities.csv": 19909,
                        "sakhalkar_species_analysis.csv": 57,
                    }:
                        errors.append("ARCHIVE_SCHEMA_OR_FROZEN_ROWS_DRIFT")
                raw_receipt = _optional(inner, "data_archive/RESERVED_DOI_RECEIPT.json")
                if raw_receipt is not None:
                    receipt = json.loads(raw_receipt)

    if source_commit is None or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        errors.append("ARCHIVE_SOURCE_COMMIT_INVALID")
    if expected_head_sha is not None and not re.fullmatch(r"[0-9a-f]{40}", expected_head_sha):
        raise ValueError("expected_head_sha must be full 40-character Git commit SHA")
    matches_head = source_commit == expected_head_sha if expected_head_sha else None
    doi = (receipt or {}).get("doi")
    doi_ok = bool(
        isinstance(doi, str)
        and re.fullmatch(r"10\.5281/zenodo\.\d+", doi)
        and doi not in SOURCE_DOIS
        and receipt.get("status") == "ZENODO_DOI_RESERVED_PENDING_PUBLICATION"
        and all(doi in text and "[ACCESS-ROUTING ARCHIVE DOI" not in text for text in documents.values())
    )
    author = _author_check(author_metadata_json)
    blockers = list(dict.fromkeys(errors))
    if not doi_ok:
        blockers.append("DOI_NOT_RESERVED")
    if not author["complete"]:
        blockers.append("AUTHOR_METADATA_INCOMPLETE")
    incomplete_submission_docs = sorted(
        doc for doc, content in documents.items()
        if any(marker in content for marker in AUTHOR_PLACEHOLDERS)
    )
    if incomplete_submission_docs:
        blockers.append("AUTHOR_STATEMENTS_NOT_APPLIED_TO_SUBMISSION_FILES")
    author_surface_mismatches = (
        _author_surface_mismatches(author_metadata_json, documents)
        if author["complete"] and not incomplete_submission_docs
        else []
    )
    if author_surface_mismatches:
        blockers.append("AUTHOR_METADATA_DOES_NOT_MATCH_SUBMISSION_FILES")
    if expected_head_sha is not None and matches_head is False:
        blockers.append("SOURCE_COMMIT_NOT_REVIEWED_HEAD")
    blockers.append("DOI_PUBLICATION_NOT_VERIFIED")
    return {
        "analysis": "BITA_LETTER_OFFLINE_RELEASE_GATE_V1",
        "stage": "INTEGRITY_FAILED" if errors else "INTEGRITY_VERIFIED_BUT_RELEASE_BLOCKED",
        "integrity": {"all_checksums_match": not errors, "errors": errors, "inner": inner_summary},
        "provenance": {"source_commit": source_commit, "expected_head_sha": expected_head_sha, "source_commit_matches_head": matches_head},
        "doi": {"reserved_in_package": doi_ok, "doi": doi if doi_ok else None, "external_publication_checked": False},
        "author_metadata": author,
        "author_submission_surfaces": {
            "placeholders_remaining": incomplete_submission_docs,
            "metadata_mismatches": author_surface_mismatches,
            "complete": not incomplete_submission_docs and not author_surface_mismatches,
        },
        "blockers": blockers,
        "submission_ready": False,
        "external_gate": "The published DOI must resolve publicly and author-controlled fields require approval; offline inspection cannot verify these.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("package_zip", type=Path)
    ap.add_argument("author_metadata_json", type=Path)
    ap.add_argument("--expected-head-sha")
    ap.add_argument("--output-json", type=Path)
    args = ap.parse_args()
    receipt = audit_package(args.package_zip, args.author_metadata_json, expected_head_sha=args.expected_head_sha)
    data = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(data, encoding="utf-8")
    print(data)
    if not receipt["integrity"]["all_checksums_match"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
