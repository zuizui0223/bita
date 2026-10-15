from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

from scripts.audit_letter_release_gate import audit_package

SOURCE_SHA = "a" * 40
DOI = "10.5281/zenodo.12345678"


def _archive(root: Path, *, reserved: bool = False, corrupt: bool = False, source: str = SOURCE_SHA, author_placeholder: bool = False) -> Path:
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
            content = markdown
            if reserved and filename == "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md":
                content += (
                    b"\n**Authors:** Example Author"
                    b"\n**Affiliations and author e-mail addresses:** Example Institute; example@example.edu"
                    b"\n**Corresponding author:** Example Author"
                    b"\n**Complete correspondence address:** postal address; telephone; example@example.edu"
                    b"\n**Statement of authorship:** contributions"
                    b"\n**Funding:** none declared"
                    b"\n**Acknowledgments:** none"
                    b"\n**Conflict of interest:** none"
                    b"\n**AI-assisted workflow disclosure:** reviewed"
                )
            if reserved and filename == "ECOLOGY_LETTERS_LETTER_COVER_V0.md":
                content += (
                    b"\n**Author-relative novelty statement:** novelty described"
                    b"\n**Conflict-of-interest statement:** none"
                    b"\nBest regards,\n\nExample Author\n"
                )
            if author_placeholder and filename == "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md":
                content += b"\n**Authors:** [FINAL AUTHOR LIST -- REQUIRED BEFORE SUBMISSION]"
            z.writestr(filename, content)
    return out


def _author_metadata(root: Path, *, approved: bool = False) -> Path:
    data = {
        "schema": "BITA_ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1",
        "status": "AUTHOR_CONTROLLED_COMPLETE" if approved else "AUTHOR_CONTROLLED_INCOMPLETE",
        "authors": [
            {
                "name": "Example Author",
                "affiliation_ids": ["1"],
                "email": "example@example.edu",
                "orcid": None,
                "corresponding": True,
            }
        ] if approved else [],
        "affiliations": {"1": "Example Institute"} if approved else {},
        "correspondence": {
            "postal_address": "postal address" if approved else None,
            "telephone": "telephone" if approved else None,
            "email": "example@example.edu" if approved else None,
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


def test_release_gate_rejects_unstructured_authors_even_with_all_declarations(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data["authors"] = ["Example Author"]  # previously accepted as nonempty list
    metadata.write_text(json.dumps(data))

    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert receipt["integrity"]["all_checksums_match"]
    assert receipt["author_metadata"]["complete"] is False
    assert "authors[1]" in receipt["author_metadata"]["invalid"]
    assert "AUTHOR_METADATA_INCOMPLETE" in receipt["blockers"]
    assert receipt["submission_ready"] is False


def test_release_gate_requires_affiliation_links_and_single_correspondent(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data["authors"][0]["affiliation_ids"] = ["nonexistent"]
    data["authors"][0]["corresponding"] = False
    metadata.write_text(json.dumps(data))

    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert "authors[1].unknown_affiliation:nonexistent" in receipt["author_metadata"]["invalid"]
    assert "exactly_one_corresponding_author" in receipt["author_metadata"]["invalid"]
    assert not receipt["author_metadata"]["complete"]
    assert "AUTHOR_METADATA_INCOMPLETE" in receipt["blockers"]


def test_release_gate_requires_author_metadata_schema(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data.pop("schema")
    metadata.write_text(json.dumps(data))
    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert "schema" in receipt["author_metadata"]["invalid"]
    assert not receipt["author_metadata"]["complete"]


def test_release_gate_rejects_non_object_metadata(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path)
    metadata.write_text('["not", "an", "author-record"]')
    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert receipt["author_metadata"]["missing"] == ["METADATA_FILE_UNREADABLE"]
    assert not receipt["author_metadata"]["complete"]
    assert "AUTHOR_METADATA_INCOMPLETE" in receipt["blockers"]



def test_release_gate_blocks_title_page_placeholder_even_with_valid_metadata(tmp_path):
    package = _archive(tmp_path, reserved=True, author_placeholder=True)
    receipt = audit_package(package, _author_metadata(tmp_path, approved=True), expected_head_sha=SOURCE_SHA)
    assert receipt["author_metadata"]["complete"]
    assert receipt["author_submission_surfaces"]["complete"] is False
    assert receipt["author_submission_surfaces"]["placeholders_remaining"] == [
        "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md"
    ]
    assert "AUTHOR_STATEMENTS_NOT_APPLIED_TO_SUBMISSION_FILES" in receipt["blockers"]
    assert receipt["integrity"]["all_checksums_match"]
    assert receipt["submission_ready"] is False


def test_release_gate_has_no_author_placeholder_blocker_for_complete_doc_and_record(tmp_path):
    receipt = audit_package(
        _archive(tmp_path, reserved=True),
        _author_metadata(tmp_path, approved=True),
        expected_head_sha=SOURCE_SHA,
    )
    assert receipt["author_metadata"]["complete"] is True
    assert receipt["author_submission_surfaces"]["complete"] is True
    assert "AUTHOR_STATEMENTS_NOT_APPLIED_TO_SUBMISSION_FILES" not in receipt["blockers"]
    assert "DOI_PUBLICATION_NOT_VERIFIED" in receipt["blockers"]


def test_release_gate_author_concordance_accepts_approved_synthetic_documents(tmp_path):
    receipt = audit_package(
        _archive(tmp_path, reserved=True),
        _author_metadata(tmp_path, approved=True),
        expected_head_sha=SOURCE_SHA,
    )
    assert receipt["author_metadata"]["complete"]
    assert receipt["author_submission_surfaces"]["complete"]
    assert receipt["author_submission_surfaces"]["metadata_mismatches"] == []
    assert "AUTHOR_METADATA_DOES_NOT_MATCH_SUBMISSION_FILES" not in receipt["blockers"]


def test_release_gate_rejects_stale_author_name_and_cover_signature(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data["authors"][0]["name"] = "Different Approved Author"
    metadata.write_text(json.dumps(data))
    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert receipt["author_metadata"]["complete"]
    assert "title.authors" in receipt["author_submission_surfaces"]["metadata_mismatches"]
    assert "cover.corresponding_author_signature" in receipt["author_submission_surfaces"]["metadata_mismatches"]
    assert "AUTHOR_METADATA_DOES_NOT_MATCH_SUBMISSION_FILES" in receipt["blockers"]
    assert "Different Approved Author" not in json.dumps(receipt)
    assert "Example Author" not in json.dumps(receipt)


def test_release_gate_rejects_mismatched_author_email_and_affiliation(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data["authors"][0]["email"] = "updated@example.edu"
    data["affiliations"]["1"] = "Different Institute"
    metadata.write_text(json.dumps(data))
    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert receipt["author_metadata"]["complete"]
    fields = receipt["author_submission_surfaces"]["metadata_mismatches"]
    assert "title.authors[1].email" in fields
    assert "title.authors[1].affiliation" in fields
    assert "AUTHOR_METADATA_DOES_NOT_MATCH_SUBMISSION_FILES" in receipt["blockers"]
    assert "updated@example.edu" not in json.dumps(receipt)


def test_release_gate_requires_approved_funding_novelty_and_signoff(tmp_path):
    package = _archive(tmp_path, reserved=True)
    metadata = _author_metadata(tmp_path, approved=True)
    data = json.loads(metadata.read_text())
    data["funding_statement"] = "Funding declaration updated"
    data["author_relative_novelty_statement"] = "Novelty statement updated"
    metadata.write_text(json.dumps(data))
    receipt = audit_package(package, metadata, expected_head_sha=SOURCE_SHA)
    assert "title.funding_statement" in receipt["author_submission_surfaces"]["metadata_mismatches"]
    assert "cover.author_relative_novelty_statement" in receipt["author_submission_surfaces"]["metadata_mismatches"]
    assert "AUTHOR_METADATA_DOES_NOT_MATCH_SUBMISSION_FILES" in receipt["blockers"]
