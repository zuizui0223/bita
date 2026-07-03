"""Paged Crossref retrieval for the existing broad evidence query registry.

This module preserves the existing query registry and candidate construction. It
only permits a requested depth above Crossref's 1,000-record page limit by
retrieving consecutive score-ranked pages and keeping an auditable per-query
receipt. Callers may observe each page before corpus-level deduplication to build
rank-binned retrieval diagnostics.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable

from .broad_reality_evidence import (
    CROSSREF_WORKS_URL,
    Candidate,
    _request_json,
    candidate_from_crossref_item,
    merge_candidate,
)

CROSSREF_PAGE_SIZE = 1000
MAX_DEEP_ROWS_PER_QUERY = 5000
PageObserver = Callable[[dict[str, str], int, list[Candidate], int], None]


def harvest_crossref_paged(
    queries: Iterable[dict[str, str]],
    *,
    rows_per_query: int,
    page_size: int = CROSSREF_PAGE_SIZE,
    page_observer: PageObserver | None = None,
    request_json: Callable[[str, dict[str, str]], dict[str, Any]] = _request_json,
) -> tuple[list[Candidate], list[dict[str, str]]]:
    """Retrieve a fixed total depth per query using Crossref score-ranked pages.

    ``rows_per_query`` means a total requested depth, not the size of a single
    Crossref response. A query stops early only when Crossref returns a short
    page. The receipt records whether the requested depth was reached; reaching
    it is a retrieval cap, not a claim that the provider has no further works.

    ``page_observer`` receives the query, zero-based page offset, title-bearing
    candidate memberships from that page, and the raw number of records returned.
    It is deliberately called before the cross-query candidate deduplication so a
    caller can diagnose yield across ranked pages within each query.
    """

    if not 1 <= rows_per_query <= MAX_DEEP_ROWS_PER_QUERY:
        raise ValueError(
            f"rows_per_query must be between 1 and {MAX_DEEP_ROWS_PER_QUERY} for paged retrieval"
        )
    if not 1 <= page_size <= CROSSREF_PAGE_SIZE:
        raise ValueError(
            f"page_size must be between 1 and {CROSSREF_PAGE_SIZE} for Crossref retrieval"
        )

    candidates: dict[str, Candidate] = {}
    reports: list[dict[str, str]] = []
    for query in queries:
        collected = 0
        pages = 0
        api_total_results = ""
        try:
            while collected < rows_per_query:
                page_rows = min(page_size, rows_per_query - collected)
                page_offset = collected
                payload = request_json(
                    CROSSREF_WORKS_URL,
                    {
                        "query.bibliographic": query["query_text"],
                        "filter": "type:journal-article",
                        "sort": "score",
                        "order": "desc",
                        "rows": str(page_rows),
                        "offset": str(page_offset),
                    },
                )
                message = payload.get("message")
                if not isinstance(message, dict):
                    raise ValueError("Crossref response lacks message object")
                items = message.get("items")
                if not isinstance(items, list):
                    raise ValueError("Crossref response lacks items list")
                if not api_total_results:
                    api_total_results = str(message.get("total-results", ""))
                pages += 1
                page_candidates: list[Candidate] = []
                for local_rank, item in enumerate(items, start=1):
                    if not isinstance(item, dict):
                        continue
                    candidate = candidate_from_crossref_item(item, query, page_offset + local_rank)
                    if not candidate.title:
                        continue
                    page_candidates.append(candidate)
                    if candidate.candidate_id in candidates:
                        merge_candidate(candidates[candidate.candidate_id], candidate)
                    else:
                        candidates[candidate.candidate_id] = candidate
                if page_observer is not None:
                    page_observer(query, page_offset, page_candidates, len(items))
                collected += len(items)
                if len(items) < page_rows:
                    break
            reports.append({
                "query_id": query["query_id"],
                "route_family": query["route_family"],
                "query_text": query["query_text"],
                "requested_rows": str(rows_per_query),
                "works_returned": str(collected),
                "api_total_results": api_total_results,
                "status": "success",
                "message": (
                    f"pages={pages}; retrieval_cap_reached={str(collected == rows_per_query).lower()}; "
                    f"provider_has_more_than_requested={str(api_total_results.isdigit() and int(api_total_results) > rows_per_query).lower()}"
                ),
            })
        except Exception as error:
            reports.append({
                "query_id": query["query_id"],
                "route_family": query["route_family"],
                "query_text": query["query_text"],
                "requested_rows": str(rows_per_query),
                "works_returned": str(collected),
                "api_total_results": api_total_results,
                "status": "query_failed",
                "message": str(error),
            })

    failed = [row["query_id"] for row in reports if row["status"] != "success"]
    if failed:
        raise RuntimeError("Crossref broad corpus retrieval incomplete: " + ", ".join(failed))
    return sorted(candidates.values(), key=lambda item: (item.title.lower(), item.doi)), reports
