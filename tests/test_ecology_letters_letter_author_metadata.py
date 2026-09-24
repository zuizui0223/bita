from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.validate_ecology_letters_letter_author_metadata import (
    SCHEMA,
    run,
    validate,
)


def test_committed_template_is_explicitly_incomplete() -> None:
    path = Path(__file__).resolve().parents[1] / "submission" / "ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json"
    result = run(path)
    assert result["status"] == "AUTHOR_METADATA_INCOMPLETE"
    assert result["ready_for_submission_metadata_application"] is False
    assert "authors" in result["missing"]
    assert "affiliations" in result["missing"]


def test_complete_author_metadata_passes() -> None:
    data = {
        "schema": SCHEMA,
        "status": "AUTHOR_CONTROLLED_COMPLETE",
        "authors": [
            {
                "name": "Example Author",
                "affiliation_ids": ["1"],
                "orcid": "0000-0002-1825-0097",
                "email": "author@example.edu",
                "corresponding": True,
            }
        ],
        "affiliations": {"1": "Example University"},
        "correspondence": {
            "postal_address": "1 Example Street, Example City",
            "telephone": "+00 000 000 000",
            "email": "author@example.edu",
        },
        "authorship_statement": "Example Author performed all listed roles.",
        "funding_statement": "No external funding.",
        "acknowledgments": "None.",
        "conflict_of_interest_statement": "The author declares no conflict of interest.",
        "ai_assisted_workflow_disclosure": "Approved disclosure.",
        "author_relative_novelty_statement": "Approved novelty statement.",
        "archive_license": "CC-BY-4.0",
        "all_authors_approved_submitted_version": True,
        "not_under_consideration_elsewhere": True,
    }
    result = validate(data)
    assert result["status"] == "AUTHOR_METADATA_COMPLETE"
    assert result["missing"] == []
    assert result["invalid"] == []


def test_require_complete_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "metadata.json"
    path.write_text(json.dumps({"schema": SCHEMA}), encoding="utf-8")
    with pytest.raises(ValueError, match="AUTHOR_METADATA_INCOMPLETE"):
        run(path, require_complete=True)


def test_unknown_affiliation_and_multiple_corresponding_authors_are_rejected() -> None:
    data = {
        "schema": SCHEMA,
        "authors": [
            {
                "name": "A",
                "affiliation_ids": ["9"],
                "email": "a@example.edu",
                "corresponding": True,
            },
            {
                "name": "B",
                "affiliation_ids": ["1"],
                "email": "b@example.edu",
                "corresponding": True,
            },
        ],
        "affiliations": {"1": "Example University"},
        "correspondence": {
            "postal_address": "x",
            "telephone": "x",
            "email": "a@example.edu",
        },
        "authorship_statement": "x",
        "funding_statement": "x",
        "acknowledgments": "x",
        "conflict_of_interest_statement": "x",
        "ai_assisted_workflow_disclosure": "x",
        "author_relative_novelty_statement": "x",
        "archive_license": "x",
        "all_authors_approved_submitted_version": True,
        "not_under_consideration_elsewhere": True,
    }
    result = validate(data)
    assert "exactly_one_corresponding_author" in result["invalid"]
    assert "authors[1].unknown_affiliation:9" in result["invalid"]
