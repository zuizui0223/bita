from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

from scripts.audit_letter_release_gate import audit_package

SOURCE_SHA = "a" * 40
DOI = "10.5281/zenodo.12345678"


def _archive(root: Path, *, reserved: bool = False, corrupt: bool = False, source: str = SOURCE_SHA) -> Path:
    values = {
        "data_archive/archive_manifest.json": json.dumps({
            "archive_schema": "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V5",
            "analysis_tables": {
                "aubert_ephi_pair_site_analysis.csv": 2265,
                "aubert_ephi_participation_opportunities.csv": 19909,
                "sakhalkar_species_analysis.csv": 57,
            },
        }).encode(),
        "data_archive/REPOSITORY_COMMIT.txt": (source + "\n").encode(),
        "data_archive/data.csv": b"header\n1\n",
    }
    if reserved:
        values["data_archive/RESERVED_DOI_RECEIPT.json"] = json.dumps({
            "receipt": "BITA_ACCESS_ROUTING_RESERVED_DOI_V1",
            "status": "ZENODO_DOI_RESERVED_PENDING_PUBLICATION",
            "doi": DOI,
        }).encode()
    checks = "".join(
        f"{hashlib.sha256(value).hexdigest()}  ./{path.removeprefix('data_archive/')}\n"
        for path, value in sorted(values.items())
    )
    values["data_archive/FILE_SHA256SUMS.txt"] = checks.encode()
    if corrupt:
        values["data_archive/data.csv"] = b"header\n2\n"
    inner_buffer = io.BytesIO()
    with zipfile.ZipFile(inner_buffer, "w") as z:
        for p, value in values.items():
            z.writestr(p, value)
    inner = inner_buffer.getvalue()
    out = root / "staging.zip"
    markdown = (f"Data archive {DOI}" if reserved else "[ACCESS-ROUTING ARCHIVE DOI]").encode()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("access-routing-letter-data-code-v1.zip", inner)
        z.writestr("access-routing-letter-data-code-v1.sha256", hashlib.sha256(inner).hexdigest() + "  access-routing-letter-data-code-v1.zip\n")
        for filename in (
            "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
            "ECOLOGY_LETTERS_LETTER_COVER_V0.md",
            "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
        ):
            z.writestr(filename, markdown)
    return out


def _author_metadata(root: Path, *, approved: bool = False) -> Path:
    data = {
        "authors": ["Author One"] if approved else [],
        "affiliations": {"Author One": "Institute"} if approved else {},
        "correspondence": {
            "postal_address": "address" if approved else None,
            "telephone": "phone" if approved else None,
            "email": "email" if approved else None,
        },
        "authorship_statement": "contributions" if approved else None,
        "funding_statement": "none declared" if approved else None,
        "acknowledgments": "none" if approved else None,
        "conflict_of_interest_statement": "none" if approved else None,
        "ai_assisted_workflow_disclosure": "reviewed" if approved else None,
        "author_relative_novelty_statement": "novelty described" if approved else None,
        "archive_license": "CC-BY-4.0" if approved else None,
        "all_authors_approved_submitted_version": approved,
        "not_under_consideration_elsewhere": approved,
    }
    path = root / "authors.json"
    path.write_text(json.dumps(data))
    return path


def test_valid_staging_package_is_still_blocked_without_doi_and_authors(tmp_path):
    receipt = audit_package(_archive(tmp_path), _author_metadata(tmp_path), expected_head_sha=SOURCE_SHA)
    assert receipt["integrity"]["all_checksums_match"]
    assert receipt["provenance"]["source_commit_matches_head"] is True
    assert receipt["stage"] == "INTEGRITY_VERIFIED_BUT_RELEASE_BLOCKED"
    assert {"DOI_NOT_RESERVED", "AUTHOR_METADATA_INCOMPLETE", "DOI_PUBLICATION_NOT_VERIFIED"} <= set(receipt["blockers"])
    assert not receipt["submission_ready"]


def test_inner_checksum_mismatch_fails_closed(tmp_path):
    receipt = audit_package(_archive(tmp_path, corrupt=True), _author_metadata(tmp_path), expected_head_sha=SOURCE_SHA)
    assert "INNER_ARCHIVE_CHECKSUM_MISMATCH" in receipt["blockers"]
    assert receipt["stage"] == "INTEGRITY_FAILED"


def test_pull_request_virtual_merge_not_exact_reviewed_head(tmp_path):
    receipt = audit_package(_archive(tmp_path, source="b"*40), _author_metadata(tmp_path), expected_head_sha=SOURCE_SHA)
    assert receipt["integrity"]["all_checksums_match"]
    assert receipt["provenance"]["source_commit_matches_head"] is False
    assert "SOURCE_COMMIT_NOT_REVIEWED_HEAD" in receipt["blockers"]


def test_even_reserved_doi_and_author_record_require_external_publication(tmp_path):
    receipt = audit_package(_archive(tmp_path, reserved=True), _author_metadata(tmp_path, approved=True), expected_head_sha=SOURCE_SHA)
    assert receipt["integrity"]["all_checksums_match"]
    assert receipt["doi"]["reserved_in_package"]
    assert receipt["author_metadata"]["complete"]
    assert "DOI_NOT_RESERVED" not in receipt["blockers"]
    assert "AUTHOR_METADATA_INCOMPLETE" not in receipt["blockers"]
    assert "DOI_PUBLICATION_NOT_VERIFIED" in receipt["blockers"]
    assert not receipt["submission_ready"]
