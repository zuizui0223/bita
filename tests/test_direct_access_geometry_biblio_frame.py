from __future__ import annotations

from scripts import build_direct_access_geometry_biblio_frame as mod


def _record(
    *,
    key: str,
    doi: str,
    title: str,
    provider: str,
    query_id: str,
    rank: int,
    abstract: str = "",
):
    return {
        "identity_key": key,
        "doi": doi,
        "title": title,
        "publication_year": "2020",
        "publication_date": "2020-01-01",
        "journal": "Example Journal",
        "authors": "A Author",
        "abstract": abstract,
        "source_providers": {provider},
        "provider_ids": {f"{provider}:id"},
        "matched_query_ids": {query_id},
        "source_urls": {f"https://example.org/{provider}"},
        "best_provider_rank": rank,
    }


def _config():
    return {
        "publication_window": {"from": "2000-01-01", "until": "2026-09-24"},
        "providers": {
            "crossref": {"enabled": True},
            "openalex": {"enabled": True},
        },
        "queries": [{"query_id": "Q01", "text": "nectar robbing", "query_role": "CORE_LARCENY"}],
        "screening_priority_terms": {
            "larceny": ["nectar rob"],
            "geometry": ["corolla", "tongue length"],
        },
        "retention_rule": "retain all",
        "deduplication_rule": ["doi", "title+year"],
    }


def test_openalex_abstract_reconstruction_is_position_ordered() -> None:
    inverted = {
        "robbing": [2],
        "Nectar": [0],
        "geometry": [3],
        "links": [1],
    }
    assert mod._openalex_abstract(inverted) == "Nectar links robbing geometry"


def test_crossref_parser_normalizes_doi_and_title() -> None:
    item = {
        "DOI": "https://doi.org/10.1000/ABC",
        "title": ["<i>Nectar</i> robbing and corolla length"],
        "container-title": ["Journal"],
        "published": {"date-parts": [[2020, 4, 3]]},
        "author": [{"given": "A", "family": "Author"}],
        "URL": "https://doi.org/10.1000/ABC",
    }
    parsed = mod.parse_crossref_item(item, "Q01", 1)
    assert parsed["doi"] == "10.1000/abc"
    assert parsed["title"] == "Nectar robbing and corolla length"
    assert parsed["publication_year"] == "2020"
    assert parsed["publication_date"] == "2020-04-03"


def test_build_frame_deduplicates_providers_without_filtering_non_geometry_records(
    monkeypatch,
) -> None:
    shared_key = "doi:10.1000/shared"
    crossref_records = [
        _record(
            key=shared_key,
            doi="10.1000/shared",
            title="Nectar robbing in a flower",
            provider="crossref",
            query_id="Q01",
            rank=3,
        ),
        _record(
            key="doi:10.1000/no-geometry",
            doi="10.1000/no-geometry",
            title="Nectar robbing across sites",
            provider="crossref",
            query_id="Q01",
            rank=4,
        ),
        _record(
            key="doi:10.1000/no-larceny",
            doi="10.1000/no-larceny",
            title="Nectar chemistry across habitats",
            provider="crossref",
            query_id="Q01",
            rank=5,
        ),
    ]
    openalex_records = [
        _record(
            key=shared_key,
            doi="10.1000/shared",
            title="Nectar robbing in a flower",
            provider="openalex",
            query_id="Q01",
            rank=1,
            abstract="Corolla geometry predicts nectar robbing.",
        )
    ]

    monkeypatch.setattr(
        mod,
        "harvest_crossref",
        lambda config, query: (
            crossref_records,
            {
                "provider": "crossref",
                "query_id": "Q01",
                "retrieved_records": 3,
            },
        ),
    )
    monkeypatch.setattr(
        mod,
        "harvest_openalex",
        lambda config, query: (
            openalex_records,
            {
                "provider": "openalex",
                "query_id": "Q01",
                "retrieved_records": 1,
            },
        ),
    )

    frame, receipt = mod.build_frame(_config())

    assert len(frame) == 2
    shared = next(row for row in frame if row["doi"] == "10.1000/shared")
    no_geometry = next(row for row in frame if row["doi"] == "10.1000/no-geometry")

    assert shared["source_providers"] == "crossref;openalex"
    assert shared["best_provider_rank"] == "1"
    assert shared["geometry_text_match"] == "true"
    assert shared["screen_status"] == "UNSCREENED"

    # Geometry priority cannot remove larceny records.
    assert no_geometry["geometry_text_match"] == "false"
    assert no_geometry["screen_status"] == "UNSCREENED"
    assert not any(row["doi"] == "10.1000/no-larceny" for row in frame)

    assert receipt["raw_provider_records"] == 4
    assert receipt["deduplicated_provider_candidates_before_text_gate"] == 3
    assert receipt["excluded_no_retention_match"] == 1
    assert receipt["deduplicated_candidates"] == 2
    assert receipt["larceny_text_match_candidates"] == 2
    assert receipt["sentinel_query_match_candidates"] == 0
    assert receipt["retention_gate_is_direction_blind"] is True
    assert receipt["sentinel_calibration_uses_effect_direction"] is False
    assert receipt["all_records_retained_before_screening"] is False
    assert receipt["formal_recurrence_result_open"] is False


def test_candidate_id_is_stable() -> None:
    assert mod._candidate_id("doi:10.1000/x") == mod._candidate_id("doi:10.1000/x")
    assert mod._candidate_id("doi:10.1000/x") != mod._candidate_id("doi:10.1000/y")


def test_provider_id_fallback_preserves_unidentified_openalex_record() -> None:
    item = {
        "id": "https://openalex.org/W123",
        "doi": None,
        "title": None,
        "publication_year": 2020,
        "publication_date": "2020-01-01",
        "authorships": [],
        "primary_location": None,
        "abstract_inverted_index": None,
    }
    parsed = mod.parse_openalex_item(item, "Q01", 1)
    assert parsed["identity_key"] == "provider:openalex:https://openalex.org/W123"
    assert parsed["provider_ids"] == {"openalex:https://openalex.org/W123"}


def test_sentinel_query_retains_record_without_larceny_text(monkeypatch) -> None:
    config = _config()
    config["providers"]["openalex"]["enabled"] = False
    config["queries"] = [
        {
            "query_id": "S01",
            "text": "sunbird pollination long billed",
            "query_role": "SENTINEL_CALIBRATION",
        }
    ]
    record = _record(
        key="doi:10.1000/sentinel",
        doi="10.1000/sentinel",
        title="Hyper-specialization for long-billed bird pollination",
        provider="crossref",
        query_id="S01",
        rank=1,
    )
    monkeypatch.setattr(
        mod,
        "harvest_crossref",
        lambda config, query: (
            [record],
            {
                "provider": "crossref",
                "query_id": "S01",
                "retrieved_records": 1,
            },
        ),
    )

    frame, receipt = mod.build_frame(config)
    assert len(frame) == 1
    assert frame[0]["larceny_text_match"] == "false"
    assert frame[0]["sentinel_query_match"] == "true"
    assert receipt["sentinel_query_match_candidates"] == 1
    assert receipt["excluded_no_retention_match"] == 0
