from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.reserve_access_routing_zenodo_doi import build_draft_receipt, extract_reserved_doi


def _sample() -> dict[str, object]:
    return {
        "id": 12345678,
        "metadata": {
            "prereserve_doi": {
                "doi": "10.5281/zenodo.12345678",
                "recid": 12345678,
            }
        },
        "links": {
            "html": "https://zenodo.org/deposit/12345678",
            "self": "https://zenodo.org/api/deposit/depositions/12345678",
        },
        "submitted": False,
    }


def test_extract_reserved_doi_from_empty_deposition_response() -> None:
    assert extract_reserved_doi(_sample()) == "10.5281/zenodo.12345678"


def test_extract_reserved_doi_rejects_wrong_prefix() -> None:
    payload = _sample()
    payload["metadata"]["prereserve_doi"]["doi"] = "10.5072/zenodo.12345678"
    with pytest.raises(RuntimeError, match="ZENODO_RESERVED_DOI_INVALID"):
        extract_reserved_doi(payload)


def test_draft_receipt_proves_no_publish_action() -> None:
    receipt = build_draft_receipt(_sample(), "10.5281/zenodo.12345678")
    assert receipt["deposition_id"] == 12345678
    assert receipt["reserved_doi"] == "10.5281/zenodo.12345678"
    assert receipt["submitted"] is False
    assert receipt["publication_performed"] is False
    assert receipt["status"] == "ZENODO_DRAFT_CREATED_DOI_RESERVED_NOT_PUBLISHED"
