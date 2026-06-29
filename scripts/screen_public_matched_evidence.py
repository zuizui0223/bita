"""Discover public evidence leads across the complete matched-flower candidate universe.

This script is a discovery screen, not an evidence classifier. Every harvested
candidate remains in the output and stays M0 until its full text and public
tables are inspected under ``MATCHED_STUDY_PROTOCOL.md``.

A negative result means only ``not_discovered``. It never proves that a study has
no supplement, repository, or usable data.

Usage:
    python scripts/screen_public_matched_evidence.py \
      openalex_matched_flower_all_candidates.csv \
      artifacts/public_evidence_screen
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse, unquote
from urllib.request import Request, urlopen

DATACITE_DOIS_URL = "https://api.datacite.org/dois"
USER_AGENT = "biotic-interaction-trait-architecture public-evidence screen/0.2 (+https://github.com/zuizui0223/biotic-interaction-trait-architecture)"

# GitHub is deliberately absent: generic site-level GitHub links are not evidence
# that a candidate's data are deposited there.
REPOSITORY_HOST_FRAGMENTS = (
    "datadryad.org", "dryad.org", "zenodo.org", "figshare.com", "osf.io",
    "dataverse", "data.mendeley.com", "giga-db.org", "pangaea.de",
    "edmond.mpdl.mpg.de", "b2share",
)
DATASET_RESOURCE_TYPES = frozenset({"dataset", "collection", "software"})
ARTICLE_TO_DATA_RELATIONS = frozenset({"issupplementedby", "haspart"})
DIRECT_SUPPLEMENT_TOKENS = (
    "type=supplementary", "type=supplement", "supplementary-file",
    "supplementary_file", "supporting_information", "supporting-information",
    "additional_file", "additional-file",
)
DATA_STATEMENT_TOKENS = (
    "data-availability", "data availability", "supplementary-material",
    "supporting information", "supplementary information",
)
MACHINE_READABLE_SUFFIXES = (
    ".csv", ".tsv", ".tab", ".xlsx", ".xls", ".zip", ".rds", ".rdata", ".json",
)
INPUT_REQUIRED_COLUMNS = {
    "candidate_id", "seed_routes", "seed_query_ids", "title", "doi",
    "landing_page_url", "open_access_url", "is_open_access",
    "metadata_match_score", "metadata_attraction_signal",
    "metadata_barrier_signal", "metadata_pollination_signal",
    "metadata_antagonist_signal", "metadata_recoverability_signal",
}
OUTPUT_FIELDS = [
    "candidate_id", "seed_routes", "seed_query_ids", "title", "doi",
    "publication_year", "authors", "is_open_access", "open_access_url",
    "landing_page_url", "metadata_match_score", "metadata_attraction_signal",
    "metadata_barrier_signal", "metadata_pollination_signal",
    "metadata_antagonist_signal", "metadata_recoverability_signal",
    "openalex_public_full_text_status", "landing_page_discovery_status",
    "public_data_statement_count", "public_data_statement_urls",
    "direct_supplement_asset_count", "direct_supplement_asset_urls",
    "machine_readable_asset_count", "machine_readable_asset_urls",
    "repository_record_count", "repository_record_urls",
    "datacite_article_query_status", "datacite_related_dataset_count",
    "datacite_related_dataset_dois", "datacite_related_dataset_urls",
    "public_evidence_priority_score", "public_evidence_action",
    "automatic_evidence_level", "automatic_screen_warning",
]


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self._href, self._text = href, []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href, self._text = None, []


def text(value: object) -> str:
    return str(value or "").strip()


def truthy(value: object) -> bool:
    return text(value).lower() in {"1", "true", "yes", "y"}


def normalise_doi(value: object) -> str:
    value = unquote(text(value)).lower()
    if "doi.org/" in value:
        value = value.split("doi.org/", 1)[1]
    return value.removeprefix("doi:").split("?", 1)[0].split("#", 1)[0].strip().strip(".,; ")


def host_of(url: object) -> str:
    return (urlparse(text(url)).hostname or "").lower()


def is_repository_record(url: object) -> bool:
    host = host_of(url)
    return bool(host) and any(fragment in host for fragment in REPOSITORY_HOST_FRAGMENTS)


def _link_signal(url: object, label: object) -> str:
    return f"{text(url)} {text(label)}".lower()


def is_direct_supplement_asset(url: object, label: object) -> bool:
    signal = _link_signal(url, label)
    # A publisher's generic supporting-information or data-availability landing
    # page is a useful statement, but not an asset to retrieve as study data.
    if "/s/supporting-information" in signal or "#supplementary-material" in signal:
        return False
    return any(token in signal for token in DIRECT_SUPPLEMENT_TOKENS)


def is_public_data_statement(url: object, label: object) -> bool:
    return any(token in _link_signal(url, label) for token in DATA_STATEMENT_TOKENS)


def is_machine_readable_asset(url: object, label: object) -> bool:
    parsed = urlparse(text(url))
    if not parsed.path.lower().endswith(MACHINE_READABLE_SUFFIXES):
        return False
    # RSS/XML and generic feeds are intentionally excluded; a raw table must at
    # least be hosted on a data repository or be labelled as a file/data asset.
    return is_repository_record(url) or any(token in _link_signal(url, label) for token in ("data", "dataset", "download", "supplement", "table"))


def unique(values: Iterable[str]) -> list[str]:
    seen, result = set(), []
    for value in values:
        value = text(value)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def metadata_full_text_status(row: dict[str, str]) -> str:
    if text(row.get("open_access_url")):
        return "openalex_linked_oa_url"
    return "openalex_oa_flag_without_usable_url" if truthy(row.get("is_open_access")) else "no_openalex_oa_url"


def choose_landing_page(row: dict[str, str]) -> str:
    landing = text(row.get("landing_page_url"))
    if landing:
        return landing
    oa_url = text(row.get("open_access_url"))
    if oa_url and not urlparse(oa_url).path.lower().endswith(".pdf"):
        return oa_url
    doi = normalise_doi(row.get("doi"))
    return f"https://doi.org/{doi}" if doi else ""


def fetch_html_links(url: str, timeout_seconds: float) -> tuple[str, list[tuple[str, str]], str]:
    if not url:
        return "not_attempted_no_landing_page", [], ""
    request = Request(url, headers={"Accept": "text/html,application/xhtml+xml", "User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # nosec B310: fixed public landing pages
            final_url = response.geturl()
            if "html" not in text(response.headers.get("Content-Type")).lower():
                return "non_html_response", [], final_url
            html = response.read(1_500_000).decode("utf-8", errors="replace")
    except HTTPError as error:
        return f"http_error_{error.code}", [], ""
    except URLError as error:
        return f"url_error_{type(error.reason).__name__}", [], ""
    except TimeoutError:
        return "timeout", [], ""
    except Exception as error:
        return f"fetch_error_{type(error).__name__}", [], ""
    parser = LinkCollector()
    parser.feed(html)
    return "fetched_html", [(urljoin(final_url, href), label) for href, label in parser.links], final_url


def extract_page_resources(links: Iterable[tuple[str, str]]) -> tuple[list[str], list[str], list[str], list[str]]:
    statements, supplements, machine, repositories = [], [], [], []
    for url, label in links:
        if is_public_data_statement(url, label):
            statements.append(url)
        if is_direct_supplement_asset(url, label):
            supplements.append(url)
        if is_machine_readable_asset(url, label):
            machine.append(url)
        if is_repository_record(url):
            repositories.append(url)
    return unique(statements), unique(supplements), unique(machine), unique(repositories)


def _datacite_get(doi: str, timeout_seconds: float) -> tuple[str, dict[str, Any] | None]:
    if not doi:
        return "not_attempted_no_doi", None
    request = Request(
        f"{DATACITE_DOIS_URL}/{quote(doi, safe='')}",
        headers={"Accept": "application/vnd.api+json", "User-Agent": USER_AGENT},
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # nosec B310: fixed public DataCite API
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return f"http_error_{error.code}", None
    except URLError as error:
        return f"url_error_{type(error.reason).__name__}", None
    except TimeoutError:
        return "timeout", None
    except Exception as error:
        return f"query_error_{type(error).__name__}", None
    return ("queried", payload) if isinstance(payload, dict) else ("unexpected_payload", None)


def direct_datacite_related_datasets(article_doi: str, timeout_seconds: float) -> tuple[str, list[dict[str, str]]]:
    """Use only explicit relations declared by the article's own DataCite record.

    The prior broad text-search approach could surface unrelated DataCite records
    that happened to mention a DOI. Direct article metadata avoids treating those
    search hits as data links.
    """
    article_status, article_payload = _datacite_get(article_doi, timeout_seconds)
    if article_status != "queried" or article_payload is None:
        return article_status, []
    article_data = article_payload.get("data")
    attributes = article_data.get("attributes") if isinstance(article_data, dict) else None
    related = attributes.get("relatedIdentifiers") if isinstance(attributes, dict) else None
    if not isinstance(related, list):
        return "queried_no_explicit_related_identifiers", []

    targets: list[tuple[str, str]] = []
    for relation in related:
        if not isinstance(relation, dict):
            continue
        relation_type = text(relation.get("relationType")).lower()
        target_doi = normalise_doi(relation.get("relatedIdentifier"))
        if relation_type in ARTICLE_TO_DATA_RELATIONS and target_doi:
            targets.append((target_doi, relation_type))

    results: list[dict[str, str]] = []
    for target_doi, relation_type in targets:
        dataset_status, dataset_payload = _datacite_get(target_doi, timeout_seconds)
        if dataset_status != "queried" or dataset_payload is None:
            continue
        data = dataset_payload.get("data")
        dataset_attributes = data.get("attributes") if isinstance(data, dict) else None
        types = dataset_attributes.get("types") if isinstance(dataset_attributes, dict) else None
        resource_type = text(types.get("resourceTypeGeneral")).lower() if isinstance(types, dict) else ""
        if resource_type in DATASET_RESOURCE_TYPES:
            results.append(
                {
                    "doi": target_doi,
                    "url": text(dataset_attributes.get("url")) or f"https://doi.org/{target_doi}",
                    "relation_types": relation_type,
                }
            )
    return "queried_direct_article_relations", results


def public_evidence_action(
    oa_status: str,
    supplements: list[str],
    machine: list[str],
    repositories: list[str],
    datasets: list[dict[str, str]],
    statements: list[str],
) -> str:
    if datasets or machine:
        return "retrieve_public_table_then_full_text_screen"
    if repositories or supplements:
        return "inspect_public_repository_or_supplement_then_full_text_screen"
    if statements or oa_status.startswith("openalex_"):
        return "inspect_open_full_text_for_data_statement_or_embedded_supplement"
    return "retain_in_search_universe_check_access_manually_before_exclusion"


def priority_score(
    row: dict[str, str], datasets: list[dict[str, str]], supplements: list[str],
    machine: list[str], repositories: list[str], statements: list[str],
) -> int:
    score = int(text(row.get("metadata_match_score")) or 0) * 10
    score += 8 if truthy(row.get("is_open_access")) else 0
    score += 4 if text(row.get("open_access_url")) else 0
    score += min(3, len(statements)) * 1
    score += min(3, len(supplements)) * 6
    score += min(3, len(repositories)) * 8
    score += min(3, len(machine)) * 10
    score += min(3, len(datasets)) * 12
    return score


def read_candidates(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError("candidate CSV is empty")
    missing = sorted(INPUT_REQUIRED_COLUMNS.difference(rows[0]))
    if missing:
        raise ValueError(f"candidate CSV missing required columns: {', '.join(missing)}")
    return rows


def screen_candidates(
    candidates: Iterable[dict[str, str]], timeout_seconds: float,
    sleep_seconds: float, fetch_landing_pages: bool,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    candidates = list(candidates)
    rows: list[dict[str, str]] = []
    counts = {key: 0 for key in (
        "candidates", "openalex_linked_oa_url", "landing_page_html_fetched",
        "public_data_statement_discovered", "direct_supplement_asset_discovered",
        "machine_readable_asset_discovered", "repository_record_discovered",
        "datacite_related_dataset_discovered", "datacite_article_query_failed",
    )}
    for index, source in enumerate(candidates, start=1):
        row = {key: text(value) for key, value in source.items()}
        counts["candidates"] += 1
        doi = normalise_doi(row.get("doi"))
        oa_status = metadata_full_text_status(row)
        if oa_status == "openalex_linked_oa_url":
            counts["openalex_linked_oa_url"] += 1

        page_status, links = "not_attempted", []
        if fetch_landing_pages and truthy(row.get("is_open_access")):
            page_status, links, _ = fetch_html_links(choose_landing_page(row), timeout_seconds)
            if page_status == "fetched_html":
                counts["landing_page_html_fetched"] += 1
        statements, supplements, machine, repositories = extract_page_resources(links)
        if statements:
            counts["public_data_statement_discovered"] += 1
        if supplements:
            counts["direct_supplement_asset_discovered"] += 1
        if machine:
            counts["machine_readable_asset_discovered"] += 1
        if repositories:
            counts["repository_record_discovered"] += 1

        datacite_status, datasets = direct_datacite_related_datasets(doi, timeout_seconds)
        if datacite_status.startswith(("http_error", "url_error", "timeout", "query_error")):
            counts["datacite_article_query_failed"] += 1
        if datasets:
            counts["datacite_related_dataset_discovered"] += 1

        rows.append({
            "candidate_id": row.get("candidate_id", ""),
            "seed_routes": row.get("seed_routes", ""),
            "seed_query_ids": row.get("seed_query_ids", ""),
            "title": row.get("title", ""),
            "doi": doi,
            "publication_year": row.get("publication_year", ""),
            "authors": row.get("authors", ""),
            "is_open_access": row.get("is_open_access", ""),
            "open_access_url": row.get("open_access_url", ""),
            "landing_page_url": row.get("landing_page_url", ""),
            "metadata_match_score": row.get("metadata_match_score", ""),
            "metadata_attraction_signal": row.get("metadata_attraction_signal", ""),
            "metadata_barrier_signal": row.get("metadata_barrier_signal", ""),
            "metadata_pollination_signal": row.get("metadata_pollination_signal", ""),
            "metadata_antagonist_signal": row.get("metadata_antagonist_signal", ""),
            "metadata_recoverability_signal": row.get("metadata_recoverability_signal", ""),
            "openalex_public_full_text_status": oa_status,
            "landing_page_discovery_status": page_status,
            "public_data_statement_count": str(len(statements)),
            "public_data_statement_urls": " | ".join(statements),
            "direct_supplement_asset_count": str(len(supplements)),
            "direct_supplement_asset_urls": " | ".join(supplements),
            "machine_readable_asset_count": str(len(machine)),
            "machine_readable_asset_urls": " | ".join(machine),
            "repository_record_count": str(len(repositories)),
            "repository_record_urls": " | ".join(repositories),
            "datacite_article_query_status": datacite_status,
            "datacite_related_dataset_count": str(len(datasets)),
            "datacite_related_dataset_dois": " | ".join(item["doi"] for item in datasets),
            "datacite_related_dataset_urls": " | ".join(item["url"] for item in datasets),
            "public_evidence_priority_score": str(priority_score(row, datasets, supplements, machine, repositories, statements)),
            "public_evidence_action": public_evidence_action(oa_status, supplements, machine, repositories, datasets, statements),
            "automatic_evidence_level": "M0_candidate_needs_full_text",
            "automatic_screen_warning": "Positive link discovery is triage only. No missing link is evidence of no data, and no candidate is automatically D1/M2/M1.",
        })
        if sleep_seconds and index < len(candidates):
            time.sleep(sleep_seconds)

    report = {
        "source_universe": "all rows from the OpenAlex matched-flower harvest, not a final study set",
        "candidate_count": counts["candidates"],
        "positive_discovery_counts": counts,
        "scope": {
            "openalex": "uses harvested OA flags and linked OA URLs",
            "landing_pages": "fetches at most one public HTML page per OA candidate; does not download PDFs or data files",
            "datacite": "uses only direct article-DOI metadata and explicitly declared IsSupplementedBy/HasPart relations to Dataset/Collection/Software records",
        },
        "interpretation": [
            "A direct public resource link is a retrieval lead, not a D1 classification.",
            "A negative or failed discovery does not establish that data are unavailable.",
            "Manual full-text and table screening remains required before M1/M2/D1 assignment.",
        ],
    }
    return rows, report


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--timeout-seconds", type=float, default=12.0)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    parser.add_argument("--skip-landing-pages", action="store_true")
    args = parser.parse_args(argv)
    if args.timeout_seconds <= 0 or args.sleep_seconds < 0:
        raise SystemExit("timeout must be positive and sleep must be non-negative")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, report = screen_candidates(
        read_candidates(args.candidates_csv), args.timeout_seconds,
        args.sleep_seconds, not args.skip_landing_pages,
    )
    ranked = sorted(rows, key=lambda row: (-int(row["public_evidence_priority_score"]), row["title"].lower(), row["candidate_id"]))
    leads = [
        row for row in ranked
        if int(row["datacite_related_dataset_count"]) > 0
        or int(row["machine_readable_asset_count"]) > 0
        or int(row["repository_record_count"]) > 0
        or int(row["direct_supplement_asset_count"]) > 0
    ]
    write_csv(out_dir / "all_candidates_public_evidence_screen.csv", ranked)
    write_csv(out_dir / "public_resource_positive_leads.csv", leads)
    report["ranked_candidate_count"] = len(ranked)
    report["positive_public_resource_lead_count"] = len(leads)
    (out_dir / "public_evidence_screen_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
