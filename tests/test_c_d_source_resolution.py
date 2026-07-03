from __future__ import annotations

import csv
import json

import pytest

from trait_architecture.c_d_source_resolution import (
    queue_to_source_candidates,
    read_fulltext_queue,
    resolve_fulltext_queue,
    write_receipts,
)


def _queue(queue_id: str, doi: str = "10.1234/example") -> dict[str, str]:
    return {
        "queue_id": queue_id,
        "record_id": "record",
        "study_id": "study",
        "study_cluster_id": "cluster",
        "doi": doi,
        "taxon": "Example plant",
        "trait_class": "chemical_barrier",
        "outcome_class": "pollinator_preference_or_foraging",
        "design_class": "manipulation",
        "reported_direction_from_abstract": "negative",
        "existing_source_basis": "metadata",
        "current_public_source_state": "needs_resolution",
        "full_text_state": "not_yet_source_adjudicated",
        "natural_dose_relation": "unknown",
        "outcome_layer": "foraging_or_preference",
        "comparability_cell": "test",
        "analysis_action": "source_read_then_extract_if_possible",
        "primary_reading_goal": "recover dose and response",
        "do_not_infer": "none",
    }


def _crossref_payload() -> dict[str, object]:
    return {
        "message": {
            "type": "journal-article",
            "is-referenced-by-count": 17,
            "license": [{"URL": "https://license.example"}],
            "link": [
                {"content-type": "application/pdf", "URL": "https://publisher.example/article.pdf"},
                {"content-type": "text/html", "URL": "https://publisher.example/article.html"},
            ],
            "relation": {"is-supplemented-by": [{"id": "dataset"}]},
        }
    }


def test_queue_mapping_uses_registered_dois() -> None:
    candidates = queue_to_source_candidates([_queue("Q1"), _queue("Q2", doi="")])
    assert candidates == [
        {"candidate_id": "Q1", "source": "doi:10.1234/example"},
        {"candidate_id": "Q2", "source": ""},
    ]


def test_resolve_fulltext_queue_retains_reading_metadata_and_content_urls() -> None:
    calls: list[str] = []

    def fake_fetch(url: str):
        calls.append(url)
        return 200, _crossref_payload()

    rows = resolve_fulltext_queue([_queue("Q1")], fetch_json=fake_fetch)

    assert len(rows) == 1
    assert rows[0]["queue_id"] == "Q1"
    assert rows[0]["study_cluster_id"] == "cluster"
    assert rows[0]["access_state"] == "linked_data_relation_present"
    assert rows[0]["resolved"] == "true"
    assert rows[0]["crossref_content_urls"] == (
        "https://publisher.example/article.pdf;https://publisher.example/article.html"
    )
    assert "Access and relation metadata only" in rows[0]["do_not_infer"]
    assert len(calls) == 2


def test_write_receipts_emits_access_only_report(tmp_path) -> None:
    def fake_fetch(_url: str):
        return 200, _crossref_payload()

    rows = resolve_fulltext_queue([_queue("Q1")], fetch_json=fake_fetch)
    report = write_receipts(tmp_path, rows)

    with (tmp_path / "c_d_fulltext_source_receipts.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "c_d_fulltext_source_report.json").read_text(encoding="utf-8"))
    assert written[0]["queue_id"] == "Q1"
    assert written[0]["crossref_content_urls"].endswith("article.html")
    assert report["queue_count"] == 1
    assert report["rows_with_crossref_content_url"] == 1
    assert saved["counts_by_access_state"]["linked_data_relation_present"] == 1


def test_read_queue_requires_unique_nonempty_ids(tmp_path) -> None:
    path = tmp_path / "queue.csv"
    fields = list(_queue("Q1"))
    rows = [_queue("Q1"), _queue("Q1")]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="unique"):
        read_fulltext_queue(path)
