from __future__ import annotations

import csv
import json

from trait_architecture.c_d_public_source_scout import scout_queue, write_scout


def _queue() -> dict[str, str]:
    return {
        "queue_id": "Q1",
        "record_id": "record",
        "study_id": "study",
        "study_cluster_id": "cluster",
        "doi": "10.1234/example",
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


def _fetch(url: str):
    if "api.crossref.org" in url:
        return 200, {"message": {"DOI": "10.1234/example", "title": ["Example"], "URL": "https://doi.org/10.1234/example"}}
    if "api.openalex.org" in url:
        return 200, {
            "id": "https://openalex.org/W1",
            "title": "Example",
            "open_access": {"is_oa": True},
            "best_oa_location": {
                "pdf_url": "https://repository.example/example.pdf",
                "landing_page_url": "https://repository.example/landing",
                "license": "cc-by",
                "source": {"display_name": "Repository"},
            },
            "locations": [],
        }
    return 404, {}


def test_scout_retains_exact_article_provenance_and_oa_candidate() -> None:
    receipts, report = scout_queue([_queue()], fetch_json=_fetch)

    assert report["queue_count"] == 1
    assert report["studies_with_public_pdf_candidate"] == 1
    assert receipts[0]["queue_id"] == "Q1"
    oa = next(row for row in receipts if row["provider"] == "OpenAlex")
    assert oa["resolution_status"] == "public_fulltext_candidate"
    assert oa["content_url"] == "https://repository.example/example.pdf"
    assert oa["relation_to_article"] == "exact_article_doi"


def test_scout_writes_receipts_and_report(tmp_path) -> None:
    receipts, report = scout_queue([_queue()], fetch_json=_fetch)
    write_scout(tmp_path, receipts, report)

    with (tmp_path / "c_d_public_source_receipts.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "c_d_public_source_report.json").read_text(encoding="utf-8"))
    assert written[0]["study_cluster_id"] == "cluster"
    assert saved["studies_with_public_pdf_candidate"] == 1
    assert "access leads only" in saved["decision_boundary"]
