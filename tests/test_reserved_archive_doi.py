from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.apply_reserved_archive_doi import (
    RECEIPT_TYPE,
    RESERVED_STATUS,
    TARGETS,
    apply_reserved_doi,
    normalize_zenodo_doi,
    verify_reserved_doi,
)


def _fixture(root: Path) -> None:
    payloads = {
        "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md":
            "archived at **[ACCESS-ROUTING ARCHIVE DOI]**\n",
        "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md":
            "archived at **[ACCESS-ROUTING ARCHIVE DOI]**. "
            "**ARCHIVE DOI REQUIRED BEFORE SUBMISSION.**\n",
        "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md":
            "archived at **[ACCESS-ROUTING ARCHIVE DOI — REQUIRED BEFORE SUBMISSION]**\n",
        "docs/PUBLICATION_STATUS.md":
            "ACCESS_ROUTING_ARCHIVE_DOI = RESERVE_IN_ZENODO_DRAFT_BEFORE_FINAL_PACKAGE_BUILD\n"
            "DATA_CODE_ARCHIVE = STAGING_READY_RESERVED_DOI_THEN_FINAL_BUILD\n",
        "docs/SUBMISSION_SCOPE.md":
            "ARCHIVE_DOI = REQUIRED\n"
            "DATA_CODE_ARCHIVE = STAGING_READY_DOI_REQUIRED\n",
        "submission/access_routing_archive/README.md":
            "ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_DOI_REQUIRED_BEFORE_FINAL_PACKAGE_BUILD\n",
        "submission/access_routing_archive/ZENODO_METADATA_TEMPLATE.md":
            "**DOI:** RESERVE IN ZENODO DRAFT BEFORE THE FINAL DOI-BEARING SUBMISSION COMMIT\n",
    }
    assert set(payloads) == set(TARGETS)
    for rel, text in payloads.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "value",
    [
        "10.5281/zenodo.12345678",
        "doi:10.5281/zenodo.12345678",
        "https://doi.org/10.5281/zenodo.12345678",
        "https://dx.doi.org/10.5281/zenodo.12345678",
    ],
)
def test_normalize_reserved_zenodo_doi(value: str) -> None:
    assert normalize_zenodo_doi(value) == "10.5281/zenodo.12345678"


@pytest.mark.parametrize(
    "value",
    [
        "",
        "10.1000/example",
        "10.5281/zenodo.not-a-number",
        "https://zenodo.org/records/123",
    ],
)
def test_reject_non_zenodo_record_doi(value: str) -> None:
    with pytest.raises(ValueError, match="RESERVED_DOI_MUST_BE_ZENODO_RECORD_DOI"):
        normalize_zenodo_doi(value)


def test_apply_reserved_doi_updates_all_submission_surfaces(tmp_path: Path) -> None:
    _fixture(tmp_path)
    doi = "10.5281/zenodo.12345678"

    result = apply_reserved_doi(tmp_path, doi)
    assert result["status"] == RESERVED_STATUS
    assert result["doi"] == doi

    receipt = json.loads(
        (tmp_path / "submission/access_routing_archive/RESERVED_DOI_RECEIPT.json")
        .read_text(encoding="utf-8")
    )
    assert receipt["receipt"] == RECEIPT_TYPE
    assert receipt["status"] == RESERVED_STATUS
    assert receipt["doi"] == doi
    assert receipt["automatic_submission_permitted"] is False

    for rel in TARGETS:
        text = (tmp_path / rel).read_text(encoding="utf-8")
        assert doi in text

    for rel in (
        "manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md",
        "submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md",
        "submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md",
    ):
        assert "[ACCESS-ROUTING ARCHIVE DOI" not in (
            tmp_path / rel
        ).read_text(encoding="utf-8")

    verified = verify_reserved_doi(tmp_path)
    assert verified["status"] == "ZENODO_RESERVED_DOI_APPLIED"
    assert verified["failures"] == []


def test_apply_is_idempotent_for_same_reserved_doi(tmp_path: Path) -> None:
    _fixture(tmp_path)
    doi = "10.5281/zenodo.12345678"
    apply_reserved_doi(tmp_path, doi)
    second = apply_reserved_doi(tmp_path, doi)
    assert second["changed_files"] == []


def test_refuses_switching_to_a_different_reserved_doi(tmp_path: Path) -> None:
    _fixture(tmp_path)
    apply_reserved_doi(tmp_path, "10.5281/zenodo.12345678")
    with pytest.raises(ValueError, match="DIFFERENT_RESERVED_DOI_ALREADY_FROZEN"):
        apply_reserved_doi(tmp_path, "10.5281/zenodo.99999999")


def test_check_only_state_before_reservation_is_explicit(tmp_path: Path) -> None:
    _fixture(tmp_path)
    result = verify_reserved_doi(tmp_path)
    assert result == {
        "status": "ZENODO_DOI_NOT_RESERVED_YET",
        "receipt_present": False,
    }
