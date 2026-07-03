from __future__ import annotations

import csv
import json

import pytest

import trait_architecture.c_d_fulltext_locator as locator
from trait_architecture.c_d_fulltext_locator import (
    locate_receipt_row,
    locate_receipts,
    read_receipts,
    write_locators,
)


def _receipt(urls: str = "https://publisher.example/article.pdf") -> dict[str, str]:
    return {
        "queue_id": "Q1",
        "study_id": "study",
        "study_cluster_id": "cluster",
        "doi": "10.1234/example",
        "taxon": "Example plant",
        "trait_class": "chemical_barrier",
        "outcome_class": "pollinator_preference_or_foraging",
        "design_class": "manipulation",
        "crossref_content_urls": urls,
    }


def _locator_output_row() -> dict[str, str]:
    return {
        "queue_id": "Q1",
        "study_id": "study",
        "study_cluster_id": "cluster",
        "doi": "10.1234/example",
        "taxon": "Example plant",
        "trait_class": "chemical_barrier",
        "outcome_class": "pollinator_preference_or_foraging",
        "design_class": "manipulation",
        "source_url": "https://publisher.example/article.pdf",
        "pdf_access_status": "public_pdf_recovered",
        "http_status": "200",
        "content_type": "application/pdf",
        "pdf_bytes": "1234",
        "page_count": "2",
        "candidate_pages": "[]",
        "locator_status": "candidate_pages_located",
        "locator_note": "temporary only",
        "do_not_infer": "boundary",
    }


def test_locator_uses_only_declared_pdf_url_and_emits_page_metadata(monkeypatch) -> None:
    calls: list[str] = []

    def fake_fetch(url: str):
        calls.append(url)
        return 200, "application/pdf", b"%PDF-1.7 fake"

    monkeypatch.setattr(locator, "_candidate_pages", lambda _bytes: (7, '[{"page": 3, "matched_terms": ["dose"], "score": 1}]'))
    row = locate_receipt_row(_receipt(), fetch_pdf=fake_fetch)

    assert calls == ["https://publisher.example/article.pdf"]
    assert row["pdf_access_status"] == "public_pdf_recovered"
    assert row["page_count"] == "7"
    assert json.loads(row["candidate_pages"])[0]["page"] == 3
    assert "does not verify table values" in row["do_not_infer"]


def test_locator_never_treats_non_pdf_or_missing_pdf_link_as_readable() -> None:
    row = locate_receipt_row(
        _receipt("https://publisher.example/article.html"),
        fetch_pdf=lambda _url: (_ for _ in ()).throw(AssertionError("must not fetch HTML link")),
    )
    assert row["pdf_access_status"] == "no_declared_pdf_url"

    non_pdf = locate_receipt_row(_receipt(), fetch_pdf=lambda _url: (200, "text/html", b"<html>paywall</html>"))
    assert non_pdf["pdf_access_status"] == "public_pdf_not_recovered"
    assert non_pdf["locator_status"] == "access_or_parse_failed"


def test_locator_writes_only_metadata_and_requires_receipt_columns(tmp_path) -> None:
    report = write_locators(tmp_path / "locators.csv", [_locator_output_row()])
    with (tmp_path / "locators.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    assert written[0]["queue_id"] == "Q1"
    assert report["public_pdf_recovered"] == 1
    assert report["candidate_pages_located"] == 1

    invalid = tmp_path / "invalid.csv"
    invalid.write_text("queue_id,doi\nQ1,10.1234/example\n", encoding="utf-8")
    with pytest.raises(ValueError, match="required"):
        read_receipts(invalid)


def test_locator_maps_all_receipts() -> None:
    rows = locate_receipts(
        [_receipt(""), _receipt("https://publisher.example/article.pdf")],
        fetch_pdf=lambda _url: (500, "", b""),
    )
    assert len(rows) == 2
    assert rows[0]["locator_status"] == "not_run"
    assert rows[1]["locator_status"] == "access_or_parse_failed"
