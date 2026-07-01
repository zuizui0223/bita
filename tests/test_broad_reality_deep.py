from __future__ import annotations

from trait_architecture.broad_reality_deep import harvest_crossref_paged


def query() -> dict[str, str]:
    return {
        "query_id": "AP01",
        "route_family": "A_to_pollination",
        "query_text": "floral trait pollination",
        "primary_empirical_question": "A to P",
        "expected_contribution": "coverage",
    }


def record(index: int) -> dict[str, object]:
    return {
        "DOI": f"10.1/{index}",
        "title": [f"Flower trait {index}"],
        "issued": {"date-parts": [[2020]]},
        "type": "journal-article",
        "container-title": ["Flower Journal"],
        "abstract": "Flower trait and pollination outcome.",
    }


def test_paged_harvest_uses_offsets_and_marks_cap_when_requested_depth_is_reached() -> None:
    calls: list[dict[str, str]] = []

    def fake_request(_: str, params: dict[str, str]) -> dict[str, object]:
        calls.append(params)
        offset = int(params["offset"])
        rows = int(params["rows"])
        items = [record(index) for index in range(offset + 1, offset + rows + 1)]
        return {"message": {"items": items, "total-results": 9000}}

    candidates, reports = harvest_crossref_paged([query()], rows_per_query=2000, request_json=fake_request)

    assert len(candidates) == 2000
    assert [call["offset"] for call in calls] == ["0", "1000"]
    assert reports[0]["works_returned"] == "2000"
    assert "pages=2" in reports[0]["message"]
    assert "retrieval_cap_reached=true" in reports[0]["message"]
    assert "provider_has_more_than_requested=true" in reports[0]["message"]


def test_paged_harvest_stops_on_short_page_before_requested_depth() -> None:
    def fake_request(_: str, params: dict[str, str]) -> dict[str, object]:
        offset = int(params["offset"])
        if offset == 0:
            return {"message": {"items": [record(1), record(2)], "total-results": 2}}
        raise AssertionError("short first page should stop retrieval")

    candidates, reports = harvest_crossref_paged([query()], rows_per_query=2000, request_json=fake_request)

    assert len(candidates) == 2
    assert reports[0]["works_returned"] == "2"
    assert "retrieval_cap_reached=false" in reports[0]["message"]
