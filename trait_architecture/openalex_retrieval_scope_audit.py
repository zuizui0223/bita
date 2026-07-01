"""Audit whether the fixed 258-work OpenAlex corpus was depth-limited.

The historical corpus is immutable. This module never rewrites it. Instead, it
runs a *current* scope audit that compares:

1. the six query IDs used in the historical PR #20 artifact at the original top
   50 versus the current top 100; and
2. the four D-level query IDs already in the query registry but not run for the
   historical artifact.

The output is a discovery-scope diagnostic, not an evidence classification or a
replacement candidate universe.
"""

from __future__ import annotations

import csv
import json
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from trait_architecture.fixed_candidate_universe import load_fixed_candidate_universe


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
USER_AGENT = "biotic-interaction-trait-architecture retrieval-scope-audit/0.3"
HISTORICAL_QUERY_IDS = frozenset({"A01", "A02", "B01", "B02", "C01", "C02"})
D_LEVEL_QUERY_IDS = frozenset({"D01", "D02", "D03", "D04"})
SCOPE_DEPTH = 100
REQUEST_INTERVAL_SECONDS = 1.0
RETRYABLE_HTTP_CODES = frozenset({429, 500, 502, 503, 504})
QUERY_REPORT_FIELDS = (
    "query_id",
    "seed_route",
    "target_level",
    "query_text",
    "historical_query",
    "scope_query",
    "api_meta_count",
    "returned_top_50",
    "returned_top_100",
    "new_ids_in_51_to_100",
    "api_count_exceeds_100",
)
CANDIDATE_FIELDS = (
    "candidate_id",
    "title",
    "doi",
    "publication_year",
    "work_type",
    "is_open_access",
    "open_access_url",
    "cited_by_count",
    "query_ids",
    "seed_routes",
    "retrieval_strata",
)
_last_request_at = 0.0


@dataclass(frozen=True)
class QueryScopeResult:
    query_id: str
    seed_route: str
    target_level: str
    query_text: str
    historical_query: bool
    scope_query: bool
    api_meta_count: int | None
    top_50_ids: frozenset[str]
    top_100_ids: frozenset[str]
    works_by_id: dict[str, dict[str, Any]]


def _text(value: object) -> str:
    return str(value or "").strip()


def _bool(value: object) -> str:
    return "true" if bool(value) else "false"


def _request_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    """Make one bounded OpenAlex request, with retries only when a key is supplied."""

    global _last_request_at
    api_key = _text(os.environ.get("OPENALEX_API_KEY"))
    max_retries = 3 if api_key else 0
    parameters = dict(params)
    if api_key:
        parameters["api_key"] = api_key

    for attempt in range(max_retries + 1):
        wait = REQUEST_INTERVAL_SECONDS - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
        request = Request(
            f"{url}?{urlencode(parameters)}",
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        )
        try:
            with urlopen(request, timeout=90) as response:  # nosec B310: fixed OpenAlex endpoint
                _last_request_at = time.monotonic()
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("OpenAlex response is not a JSON object")
            return payload
        except HTTPError as error:
            _last_request_at = time.monotonic()
            if error.code not in RETRYABLE_HTTP_CODES or attempt >= max_retries:
                raise
            time.sleep(max(REQUEST_INTERVAL_SECONDS, 2.0 ** attempt))
        except URLError:
            _last_request_at = time.monotonic()
            if attempt >= max_retries:
                raise
            time.sleep(max(REQUEST_INTERVAL_SECONDS, 2.0 ** attempt))
    raise RuntimeError("unreachable retry loop termination")


def _work_id(work: dict[str, Any]) -> str:
    raw = _text(work.get("id"))
    return f"openalex:{raw.rsplit('/', 1)[-1]}" if raw else ""


def _work_row(work: dict[str, Any]) -> dict[str, str]:
    best_oa = work.get("best_oa_location")
    oa_url = ""
    if isinstance(best_oa, dict):
        oa_url = _text(best_oa.get("pdf_url") or best_oa.get("landing_page_url"))
    open_access = work.get("open_access")
    is_oa = bool(open_access.get("is_oa")) if isinstance(open_access, dict) else False
    return {
        "candidate_id": _work_id(work),
        "title": _text(work.get("display_name") or work.get("title")),
        "doi": _text(work.get("doi")),
        "publication_year": _text(work.get("publication_year")),
        "work_type": _text(work.get("type")),
        "is_open_access": _bool(is_oa),
        "open_access_url": oa_url,
        "cited_by_count": _text(work.get("cited_by_count")),
    }


def _fetch_top_100(
    query: dict[str, str],
    *,
    request_json: Callable[[str, dict[str, str]], dict[str, Any]] = _request_json,
) -> tuple[int | None, dict[str, dict[str, Any]]]:
    response = request_json(
        OPENALEX_WORKS_URL,
        {
            "search": query["query_text"],
            "per-page": str(SCOPE_DEPTH),
            "select": ",".join((
                "id", "display_name", "publication_year", "type", "doi",
                "cited_by_count", "open_access", "best_oa_location",
            )),
        },
    )
    meta = response.get("meta")
    try:
        count = int(meta.get("count")) if isinstance(meta, dict) else None
    except (TypeError, ValueError):
        count = None
    works = response.get("results")
    if not isinstance(works, list):
        raise ValueError("OpenAlex response lacks results list")
    result: dict[str, dict[str, Any]] = {}
    for work in works:
        if not isinstance(work, dict):
            continue
        candidate_id = _work_id(work)
        if candidate_id:
            result[candidate_id] = work
    return count, result


def run_scope_audit(
    query_rows: Iterable[dict[str, str]],
    *,
    request_json: Callable[[str, dict[str, str]], dict[str, Any]] = _request_json,
) -> tuple[list[QueryScopeResult], list[dict[str, str]], dict[str, object]]:
    """Compare current top-100 depth and existing omitted D-level routes.

    Any failed API request stops the audit. An outage is never interpreted as a
    zero-candidate result.
    """

    selected = [
        row for row in query_rows
        if _text(row.get("query_id")) in HISTORICAL_QUERY_IDS | D_LEVEL_QUERY_IDS
    ]
    found_ids = {_text(row.get("query_id")) for row in selected}
    expected_ids = HISTORICAL_QUERY_IDS | D_LEVEL_QUERY_IDS
    missing = sorted(expected_ids.difference(found_ids))
    if missing:
        raise ValueError(f"query registry is missing scope-audit IDs: {', '.join(missing)}")

    results: list[QueryScopeResult] = []
    by_candidate: dict[str, dict[str, Any]] = {}
    candidate_queries: dict[str, set[str]] = defaultdict(set)
    candidate_routes: dict[str, set[str]] = defaultdict(set)
    candidate_strata: dict[str, set[str]] = defaultdict(set)

    for query in selected:
        query_id = _text(query["query_id"])
        historical = query_id in HISTORICAL_QUERY_IDS
        scope = query_id in D_LEVEL_QUERY_IDS
        try:
            meta_count, top_100 = _fetch_top_100(query, request_json=request_json)
        except Exception as error:
            raise RuntimeError(f"OpenAlex scope audit stopped at {query_id}: {error}") from error
        top_50 = dict(list(top_100.items())[:50])
        result = QueryScopeResult(
            query_id=query_id,
            seed_route=_text(query.get("seed_route")),
            target_level=_text(query.get("target_level")),
            query_text=_text(query.get("query_text")),
            historical_query=historical,
            scope_query=scope,
            api_meta_count=meta_count,
            top_50_ids=frozenset(top_50),
            top_100_ids=frozenset(top_100),
            works_by_id=top_100,
        )
        results.append(result)
        for candidate_id, work in result.works_by_id.items():
            by_candidate[candidate_id] = work
            candidate_queries[candidate_id].add(query_id)
            candidate_routes[candidate_id].add(result.seed_route)
            if historical and candidate_id in result.top_50_ids:
                candidate_strata[candidate_id].add("current_historical_top50")
            if historical and candidate_id in result.top_100_ids.difference(result.top_50_ids):
                candidate_strata[candidate_id].add("current_historical_rank51_100")
            if scope and candidate_id in result.top_50_ids:
                candidate_strata[candidate_id].add("current_D_route_top50")
            if scope and candidate_id in result.top_100_ids.difference(result.top_50_ids):
                candidate_strata[candidate_id].add("current_D_route_rank51_100")

    historical_rows, receipt = load_fixed_candidate_universe()
    fixed_ids = {row["candidate_id"] for row in historical_rows}
    current_historical_top50 = set().union(*(set(item.top_50_ids) for item in results if item.historical_query))
    current_historical_top100 = set().union(*(set(item.top_100_ids) for item in results if item.historical_query))
    current_d_top100 = set().union(*(set(item.top_100_ids) for item in results if item.scope_query))

    candidates: list[dict[str, str]] = []
    for candidate_id in sorted(by_candidate):
        row = _work_row(by_candidate[candidate_id])
        row["query_ids"] = ";".join(sorted(candidate_queries[candidate_id]))
        row["seed_routes"] = ";".join(sorted(candidate_routes[candidate_id]))
        row["retrieval_strata"] = ";".join(sorted(candidate_strata[candidate_id]))
        candidates.append(row)

    query_report_rows = [
        {
            "query_id": result.query_id,
            "seed_route": result.seed_route,
            "target_level": result.target_level,
            "query_text": result.query_text,
            "historical_query": _bool(result.historical_query),
            "scope_query": _bool(result.scope_query),
            "api_meta_count": "" if result.api_meta_count is None else str(result.api_meta_count),
            "returned_top_50": str(len(result.top_50_ids)),
            "returned_top_100": str(len(result.top_100_ids)),
            "new_ids_in_51_to_100": str(len(result.top_100_ids.difference(result.top_50_ids))),
            "api_count_exceeds_100": _bool(result.api_meta_count is not None and result.api_meta_count > SCOPE_DEPTH),
        }
        for result in results
    ]
    summary = {
        "purpose": (
            "Current OpenAlex discovery-scope audit only. It does not replace the fixed 258-work artifact, "
            "rank biological evidence, or infer trait measurements from retrieved metadata."
        ),
        "historical_fixed_snapshot": {
            "candidate_count": receipt.candidate_count,
            "source_pr": receipt.source_pr,
            "source_workflow_run": receipt.source_workflow_run,
            "source_artifact_id": receipt.source_artifact_id,
            "artifact_sha256": receipt.artifact_sha256,
        },
        "current_result_counts": {
            "historical_six_query_top50_unique": len(current_historical_top50),
            "historical_six_query_top100_unique": len(current_historical_top100),
            "historical_six_query_rank51_100_new_unique": len(current_historical_top100.difference(current_historical_top50)),
            "D01_to_D04_top100_unique": len(current_d_top100),
            "D01_to_D04_not_in_current_historical_top100": len(current_d_top100.difference(current_historical_top100)),
            "all_scope_candidates_unique": len(by_candidate),
        },
        "historical_snapshot_overlap": {
            "fixed_in_current_historical_top50": len(fixed_ids.intersection(current_historical_top50)),
            "fixed_not_in_current_historical_top50": len(fixed_ids.difference(current_historical_top50)),
            "current_historical_top50_not_in_fixed": len(current_historical_top50.difference(fixed_ids)),
            "fixed_in_current_historical_top100": len(fixed_ids.intersection(current_historical_top100)),
        },
        "interpretation_boundary": (
            "Differences from the historical artifact may reflect both retrieval depth and changing OpenAlex indexing/ranking. "
            "Only a separately versioned expansion corpus may be used for later full-text coding; this audit is not that corpus."
        ),
    }
    return results, candidates, {"query_report_rows": query_report_rows, "summary": summary}


def write_scope_audit(
    out_dir: str | Path,
    candidates: Iterable[dict[str, str]],
    report: dict[str, object],
) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "openalex_scope_query_report.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUERY_REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(report["query_report_rows"])
    with (destination / "openalex_scope_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_FIELDS)
        writer.writeheader()
        writer.writerows(candidates)
    (destination / "openalex_scope_summary.json").write_text(
        json.dumps(report["summary"], indent=2, sort_keys=True), encoding="utf-8"
    )
