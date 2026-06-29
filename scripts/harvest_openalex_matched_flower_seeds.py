"""Harvest bibliographic M0 candidates for the matched floral-regime protocol.

This script is intentionally a *seed generator*. OpenAlex metadata can identify
papers worth reading, but it cannot establish whether floral traits, pollination,
and floral antagonism were measured in a matched biological context. Every
harvested work must therefore enter the study-card registry as M0 and be checked
against full text, supplements, and linked data before any M1/M2/D1 assignment.

Usage:
    python scripts/harvest_openalex_matched_flower_seeds.py \
      empirical/matched_flower_regime/literature_seed_queries.csv \
      artifacts/matched_flower_seeds

No third-party Python dependency is required.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
USER_AGENT = "biotic-interaction-trait-architecture matched-flower seed harvest/0.1"

REQUIRED_QUERY_COLUMNS = {
    "query_id",
    "seed_route",
    "query_text",
    "target_signal",
    "screen_priority",
    "notes",
}

ATTRACTION_TERMS = (
    "floral scent",
    "floral fragrance",
    "floral volatile",
    "floral trait",
    "flower trait",
    "flower size",
    "floral display",
    "flower display",
    "nectar reward",
    "nectar volume",
    "corolla",
    "floral colour",
    "floral color",
    "flower colour",
    "flower color",
)
BARRIER_TERMS = (
    "floral defence",
    "floral defense",
    "flower defence",
    "flower defense",
    "floral chemistry",
    "flower chemistry",
    "floral volatile",
    "floral trichome",
    "flower trichome",
    "flower toughness",
    "corolla toughness",
)
POLLINATION_TERMS = (
    "pollination",
    "pollinator",
    "pollinator visitation",
    "floral visitation",
    "pollen transfer",
    "pollen deposition",
    "pollination success",
)
ANTAGONIST_TERMS = (
    "florivory",
    "floral herbivory",
    "flower herbivory",
    "flower damage",
    "floral damage",
    "floral antagonist",
    "seed predation",
    "pre-dispersal seed predation",
    "nectar robbery",
    "nectar robber",
    "pollen theft",
    "pollen thief",
)
RECOVERABILITY_TERMS = (
    "supplementary",
    "supplement",
    "dataset",
    "data repository",
    "dryad",
    "zenodo",
    "figshare",
    "individual plant",
    "plant-level",
    "plant level",
)

CSV_FIELDNAMES = [
    "candidate_id",
    "seed_routes",
    "seed_query_ids",
    "title",
    "authors",
    "publication_year",
    "publication_date",
    "work_type",
    "doi",
    "landing_page_url",
    "open_access_url",
    "is_open_access",
    "cited_by_count",
    "metadata_match_score",
    "metadata_attraction_signal",
    "metadata_barrier_signal",
    "metadata_pollination_signal",
    "metadata_antagonist_signal",
    "metadata_recoverability_signal",
    "abstract_available",
    "abstract_text",
    "candidate_status",
    "metadata_warning",
]


@dataclass
class Candidate:
    candidate_id: str
    seed_routes: set[str] = field(default_factory=set)
    seed_query_ids: set[str] = field(default_factory=set)
    title: str = ""
    authors: str = ""
    publication_year: str = ""
    publication_date: str = ""
    work_type: str = ""
    doi: str = ""
    landing_page_url: str = ""
    open_access_url: str = ""
    is_open_access: bool = False
    cited_by_count: int = 0
    metadata_match_score: int = 0
    metadata_attraction_signal: bool = False
    metadata_barrier_signal: bool = False
    metadata_pollination_signal: bool = False
    metadata_antagonist_signal: bool = False
    metadata_recoverability_signal: bool = False
    abstract_available: bool = False
    abstract_text: str = ""
    candidate_status: str = "M0_candidate_needs_full_text"
    metadata_warning: str = (
        "Metadata is a seed only; do not infer matched traits, denominators, site-time alignment, or evidence level without full text."
    )

    def to_row(self) -> dict[str, object]:
        payload = asdict(self)
        payload["seed_routes"] = ";".join(sorted(self.seed_routes))
        payload["seed_query_ids"] = ";".join(sorted(self.seed_query_ids))
        return {fieldname: payload[fieldname] for fieldname in CSV_FIELDNAMES}


def _text(value: object) -> str:
    return str(value or "").strip()


def _lower_text(*values: object) -> str:
    return " ".join(_text(value) for value in values).lower()


def _has_term(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def reconstruct_abstract(inverted_index: object) -> str:
    """Reconstruct OpenAlex's inverted abstract index deterministically."""

    if not isinstance(inverted_index, dict):
        return ""
    positioned: list[tuple[int, str]] = []
    for token, positions in inverted_index.items():
        if not isinstance(token, str) or not isinstance(positions, list):
            continue
        for position in positions:
            if isinstance(position, int) and position >= 0:
                positioned.append((position, token))
    return " ".join(token for _, token in sorted(positioned))


def _authors(work: dict[str, Any]) -> str:
    names: list[str] = []
    for authorship in work.get("authorships", []) or []:
        author = authorship.get("author") if isinstance(authorship, dict) else None
        name = author.get("display_name") if isinstance(author, dict) else None
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
        if len(names) >= 5:
            break
    return "; ".join(names)


def _location_urls(work: dict[str, Any]) -> tuple[str, str]:
    primary = work.get("primary_location")
    best_oa = work.get("best_oa_location")
    primary_landing = ""
    oa_url = ""
    if isinstance(primary, dict):
        primary_landing = _text(primary.get("landing_page_url") or primary.get("pdf_url"))
    if isinstance(best_oa, dict):
        oa_url = _text(best_oa.get("pdf_url") or best_oa.get("landing_page_url"))
    return primary_landing, oa_url


def candidate_from_work(work: dict[str, Any], query_id: str, seed_route: str) -> Candidate:
    openalex_id = _text(work.get("id"))
    candidate_id = f"openalex:{openalex_id.rsplit('/', 1)[-1]}" if openalex_id else "openalex:missing-id"
    title = _text(work.get("display_name") or work.get("title"))
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    search_text = _lower_text(title, abstract)
    attraction = _has_term(search_text, ATTRACTION_TERMS)
    barrier = _has_term(search_text, BARRIER_TERMS)
    pollination = _has_term(search_text, POLLINATION_TERMS)
    antagonist = _has_term(search_text, ANTAGONIST_TERMS)
    recoverability = _has_term(search_text, RECOVERABILITY_TERMS)
    score = sum((attraction, barrier, pollination, antagonist, recoverability))
    landing_page_url, open_access_url = _location_urls(work)
    open_access = work.get("open_access")
    is_open_access = bool(open_access.get("is_oa")) if isinstance(open_access, dict) else False

    return Candidate(
        candidate_id=candidate_id,
        seed_routes={seed_route},
        seed_query_ids={query_id},
        title=title,
        authors=_authors(work),
        publication_year=_text(work.get("publication_year")),
        publication_date=_text(work.get("publication_date")),
        work_type=_text(work.get("type")),
        doi=_text(work.get("doi")),
        landing_page_url=landing_page_url,
        open_access_url=open_access_url,
        is_open_access=is_open_access,
        cited_by_count=int(work.get("cited_by_count") or 0),
        metadata_match_score=score,
        metadata_attraction_signal=attraction,
        metadata_barrier_signal=barrier,
        metadata_pollination_signal=pollination,
        metadata_antagonist_signal=antagonist,
        metadata_recoverability_signal=recoverability,
        abstract_available=bool(abstract),
        abstract_text=abstract,
    )


def merge_candidate(existing: Candidate, new: Candidate) -> Candidate:
    existing.seed_routes.update(new.seed_routes)
    existing.seed_query_ids.update(new.seed_query_ids)
    existing.metadata_match_score = max(existing.metadata_match_score, new.metadata_match_score)
    existing.metadata_attraction_signal = existing.metadata_attraction_signal or new.metadata_attraction_signal
    existing.metadata_barrier_signal = existing.metadata_barrier_signal or new.metadata_barrier_signal
    existing.metadata_pollination_signal = existing.metadata_pollination_signal or new.metadata_pollination_signal
    existing.metadata_antagonist_signal = existing.metadata_antagonist_signal or new.metadata_antagonist_signal
    existing.metadata_recoverability_signal = existing.metadata_recoverability_signal or new.metadata_recoverability_signal
    return existing


def _request_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    request = Request(
        f"{url}?{urlencode(params)}",
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public metadata endpoint
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("OpenAlex response is not a JSON object")
    return payload


def read_query_registry(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError("seed-query registry is empty")
    missing = sorted(REQUIRED_QUERY_COLUMNS.difference(rows[0]))
    if missing:
        raise ValueError(f"seed-query registry missing columns: {', '.join(missing)}")
    valid_rows: list[dict[str, str]] = []
    for row in rows:
        if not _text(row.get("query_id")) or not _text(row.get("seed_route")) or not _text(row.get("query_text")):
            raise ValueError("each seed query needs query_id, seed_route, and query_text")
        valid_rows.append({key: _text(value) for key, value in row.items()})
    return valid_rows


def harvest(
    queries: list[dict[str, str]],
    results_per_query: int,
    mailto: str | None = None,
) -> tuple[list[Candidate], list[dict[str, object]]]:
    candidates: dict[str, Candidate] = {}
    query_reports: list[dict[str, object]] = []
    for query in queries:
        parameters = {
            "search": query["query_text"],
            "per-page": str(results_per_query),
            "select": ",".join(
                (
                    "id",
                    "display_name",
                    "publication_year",
                    "publication_date",
                    "type",
                    "doi",
                    "authorships",
                    "cited_by_count",
                    "open_access",
                    "primary_location",
                    "best_oa_location",
                    "abstract_inverted_index",
                )
            ),
        }
        if mailto:
            parameters["mailto"] = mailto
        try:
            response = _request_json(OPENALEX_WORKS_URL, parameters)
            works = response.get("results")
            if not isinstance(works, list):
                raise ValueError("OpenAlex response lacks a results list")
            harvested = 0
            for work in works:
                if not isinstance(work, dict):
                    continue
                candidate = candidate_from_work(work, query["query_id"], query["seed_route"])
                if candidate.candidate_id == "openalex:missing-id":
                    continue
                harvested += 1
                if candidate.candidate_id in candidates:
                    merge_candidate(candidates[candidate.candidate_id], candidate)
                else:
                    candidates[candidate.candidate_id] = candidate
            query_reports.append(
                {
                    "query_id": query["query_id"],
                    "seed_route": query["seed_route"],
                    "status": "success",
                    "works_returned": len(works),
                    "usable_candidates": harvested,
                }
            )
        except Exception as error:
            query_reports.append(
                {
                    "query_id": query["query_id"],
                    "seed_route": query["seed_route"],
                    "status": "query_failed",
                    "message": str(error),
                }
            )
    return list(candidates.values()), query_reports


def rank_key(candidate: Candidate) -> tuple[int, int, int, str]:
    # Citation count is deliberately not used: popularity is not evidence of a
    # matched panel. Open access and metadata signals simply make full-text
    # screening more efficient.
    return (
        -candidate.metadata_match_score,
        -int(candidate.is_open_access),
        -int(candidate.abstract_available),
        candidate.title.lower(),
    )


def shortlist_by_route(candidates: Iterable[Candidate], n_per_route: int) -> list[Candidate]:
    by_route: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        for route in candidate.seed_routes:
            by_route[route].append(candidate)

    selected: dict[str, Candidate] = {}
    for route, route_candidates in by_route.items():
        for candidate in sorted(route_candidates, key=rank_key)[:n_per_route]:
            selected[candidate.candidate_id] = candidate
    return sorted(selected.values(), key=rank_key)


def write_csv(path: Path, candidates: Iterable[Candidate]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(candidate.to_row())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query_registry", help="CSV created in literature_seed_queries.csv format")
    parser.add_argument("out_dir", help="directory for CSV and JSON outputs")
    parser.add_argument("--results-per-query", type=int, default=50)
    parser.add_argument("--shortlist-per-route", type=int, default=15)
    parser.add_argument("--mailto", default="")
    args = parser.parse_args(argv)

    if args.results_per_query < 1 or args.results_per_query > 200:
        raise SystemExit("--results-per-query must be between 1 and 200")
    if args.shortlist_per_route < 1:
        raise SystemExit("--shortlist-per-route must be positive")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    queries = read_query_registry(args.query_registry)
    candidates, query_reports = harvest(queries, args.results_per_query, args.mailto or None)
    all_candidates = sorted(candidates, key=rank_key)
    shortlist = shortlist_by_route(all_candidates, args.shortlist_per_route)

    write_csv(out_dir / "openalex_matched_flower_all_candidates.csv", all_candidates)
    write_csv(out_dir / "openalex_matched_flower_shortlist.csv", shortlist)
    report = {
        "source": "OpenAlex Works API",
        "purpose": "M0 bibliographic seed generation only; full-text screening required before evidence classification",
        "query_registry": str(args.query_registry),
        "results_per_query": args.results_per_query,
        "shortlist_per_route": args.shortlist_per_route,
        "query_reports": query_reports,
        "unique_candidates": len(all_candidates),
        "shortlisted_unique_candidates": len(shortlist),
        "status": "success" if any(item.get("status") == "success" for item in query_reports) else "no_successful_queries",
    }
    (out_dir / "openalex_matched_flower_harvest_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
