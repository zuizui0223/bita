"""Build a finite, exportable bibliographic update frame for direct access geometry -> nectar robbery.

The frame is deliberately outcome-blind. It retains every bibliographic record returned
by each frozen larceny query from each enabled provider. Geometry and larceny term flags
are priority annotations only and never exclude a record.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "DIRECT_ACCESS_GEOMETRY_BIBLIO_QUERY_V1.json"
)
DEFAULT_FRAME = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_V1.csv"
)
DEFAULT_RECEIPT = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_RECEIPT_V1.json"
)

USER_AGENT = "bita-bibliographic-frame/1.0 (+https://github.com/zuizui0223/bita)"
RETRYABLE = {429, 500, 502, 503, 504}

FRAME_COLUMNS = (
    "candidate_id",
    "identity_key",
    "doi",
    "title",
    "publication_year",
    "publication_date",
    "journal",
    "authors",
    "abstract",
    "source_providers",
    "provider_ids",
    "matched_query_ids",
    "source_urls",
    "best_provider_rank",
    "larceny_text_match",
    "geometry_text_match",
    "screen_status",
    "screen_reason",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _clean_text(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _norm_doi(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text


def _norm_title(value: object) -> str:
    text = _clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _candidate_key(doi: str, title: str, year: str) -> str:
    if doi:
        return f"doi:{doi}"
    norm_title = _norm_title(title)
    if not norm_title:
        raise ValueError("BIBLIO_RECORD_MISSING_DOI_AND_TITLE")
    return f"titleyear:{norm_title}|{year or 'unknown'}"


def _candidate_id(identity_key: str) -> str:
    return "bib_" + hashlib.sha256(identity_key.encode("utf-8")).hexdigest()[:14]


def _request_json(url: str, *, attempts: int = 5, pause: float = 0.6) -> dict[str, Any]:
    last: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
            data = json.loads(payload.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("BIBLIO_PROVIDER_RESPONSE_NOT_OBJECT")
            return data
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in RETRYABLE or attempt + 1 >= attempts:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else pause * (2**attempt)
            time.sleep(min(delay, 20.0))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            if attempt + 1 >= attempts:
                raise
            time.sleep(min(pause * (2**attempt), 20.0))
    raise RuntimeError(f"BIBLIO_PROVIDER_REQUEST_FAILED:{last}")


def _crossref_year(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        block = item.get(key)
        if isinstance(block, dict):
            parts = block.get("date-parts")
            if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
                return str(parts[0][0])
    return ""


def _crossref_date(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "published", "issued"):
        block = item.get(key)
        if not isinstance(block, dict):
            continue
        parts = block.get("date-parts")
        if not (isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]):
            continue
        values = [int(x) for x in parts[0] if isinstance(x, int)]
        if not values:
            continue
        year = values[0]
        month = values[1] if len(values) > 1 else 1
        day = values[2] if len(values) > 2 else 1
        return f"{year:04d}-{month:02d}-{day:02d}"
    return ""


def parse_crossref_item(item: dict[str, Any], query_id: str, rank: int) -> dict[str, Any]:
    title_value = item.get("title")
    if isinstance(title_value, list):
        title = _clean_text(title_value[0] if title_value else "")
    else:
        title = _clean_text(title_value)

    journal_value = item.get("container-title")
    if isinstance(journal_value, list):
        journal = _clean_text(journal_value[0] if journal_value else "")
    else:
        journal = _clean_text(journal_value)

    authors: list[str] = []
    for author in item.get("author") or []:
        if not isinstance(author, dict):
            continue
        name = " ".join(
            part for part in (
                _clean_text(author.get("given")),
                _clean_text(author.get("family")),
            )
            if part
        )
        if name:
            authors.append(name)

    doi = _norm_doi(item.get("DOI"))
    year = _crossref_year(item)
    identity_key = _candidate_key(doi, title, year)

    return {
        "identity_key": identity_key,
        "doi": doi,
        "title": title,
        "publication_year": year,
        "publication_date": _crossref_date(item),
        "journal": journal,
        "authors": "; ".join(authors),
        "abstract": _clean_text(item.get("abstract")),
        "source_providers": {"crossref"},
        "provider_ids": {f"crossref:{doi or item.get('URL', '')}"},
        "matched_query_ids": {query_id},
        "source_urls": {_clean_text(item.get("URL"))} if item.get("URL") else set(),
        "best_provider_rank": rank,
    }


def _openalex_abstract(inverted: object) -> str:
    if not isinstance(inverted, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for token, raw_positions in inverted.items():
        if not isinstance(token, str) or not isinstance(raw_positions, list):
            continue
        for position in raw_positions:
            if isinstance(position, int):
                positions.append((position, token))
    positions.sort()
    return " ".join(token for _, token in positions)


def parse_openalex_item(item: dict[str, Any], query_id: str, rank: int) -> dict[str, Any]:
    title = _clean_text(item.get("title"))
    doi = _norm_doi(item.get("doi"))
    year_raw = item.get("publication_year")
    year = str(year_raw) if isinstance(year_raw, int) else ""

    journal = ""
    location = item.get("primary_location")
    if isinstance(location, dict):
        source = location.get("source")
        if isinstance(source, dict):
            journal = _clean_text(source.get("display_name"))

    authors: list[str] = []
    for authorship in item.get("authorships") or []:
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author")
        if isinstance(author, dict):
            name = _clean_text(author.get("display_name"))
            if name:
                authors.append(name)

    provider_id = _clean_text(item.get("id"))
    identity_key = _candidate_key(doi, title, year)
    urls = set()
    if provider_id:
        urls.add(provider_id)
    if doi:
        urls.add(f"https://doi.org/{doi}")

    return {
        "identity_key": identity_key,
        "doi": doi,
        "title": title,
        "publication_year": year,
        "publication_date": _clean_text(item.get("publication_date")),
        "journal": journal,
        "authors": "; ".join(authors),
        "abstract": _clean_text(_openalex_abstract(item.get("abstract_inverted_index"))),
        "source_providers": {"openalex"},
        "provider_ids": {f"openalex:{provider_id}"},
        "matched_query_ids": {query_id},
        "source_urls": urls,
        "best_provider_rank": rank,
    }


def _merge_record(existing: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    for field in ("source_providers", "provider_ids", "matched_query_ids", "source_urls"):
        existing[field] |= new[field]

    for field in ("doi", "title", "publication_year", "publication_date", "journal", "authors"):
        if not existing.get(field) and new.get(field):
            existing[field] = new[field]

    if len(new.get("abstract", "")) > len(existing.get("abstract", "")):
        existing["abstract"] = new["abstract"]
    if len(new.get("title", "")) > len(existing.get("title", "")):
        existing["title"] = new["title"]
    existing["best_provider_rank"] = min(
        int(existing.get("best_provider_rank", 10**9)),
        int(new.get("best_provider_rank", 10**9)),
    )
    return existing


def harvest_crossref(config: dict[str, Any], query: dict[str, str]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    provider = config["providers"]["crossref"]
    start = config["publication_window"]["from"]
    end = config["publication_window"]["until"]
    rows = int(provider["rows_per_page"])
    cap = int(config["max_records_per_provider_query"])
    cursor = "*"
    records: list[dict[str, Any]] = []
    reported_total: int | None = None
    page = 0

    while True:
        params = {
            provider["query_field"]: query["text"],
            "filter": f"from-pub-date:{start},until-pub-date:{end},type:{provider['work_type']}",
            "rows": str(rows),
            "cursor": cursor,
        }
        url = provider["endpoint"] + "?" + urllib.parse.urlencode(params)
        payload = _request_json(url)
        message = payload.get("message")
        if not isinstance(message, dict):
            raise ValueError("CROSSREF_MISSING_MESSAGE")
        if reported_total is None and isinstance(message.get("total-results"), int):
            reported_total = int(message["total-results"])
            if reported_total > cap:
                raise ValueError(
                    f"CROSSREF_QUERY_EXCEEDS_FROZEN_CAP:{query['query_id']}:{reported_total}>{cap}"
                )

        items = message.get("items")
        if not isinstance(items, list):
            raise ValueError("CROSSREF_ITEMS_NOT_LIST")
        if not items:
            break

        page += 1
        for offset, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                continue
            records.append(parse_crossref_item(item, query["query_id"], (page - 1) * rows + offset))
        if len(records) > cap:
            raise ValueError(f"CROSSREF_HARVEST_EXCEEDS_CAP:{query['query_id']}")

        next_cursor = message.get("next-cursor")
        if not next_cursor or len(items) < rows:
            break
        cursor = str(next_cursor)

    return records, {
        "provider": "crossref",
        "query_id": query["query_id"],
        "query_text": query["text"],
        "reported_total": reported_total,
        "retrieved_records": len(records),
        "pages": page,
    }


def harvest_openalex(config: dict[str, Any], query: dict[str, str]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    provider = config["providers"]["openalex"]
    start = config["publication_window"]["from"]
    end = config["publication_window"]["until"]
    per_page = int(provider["rows_per_page"])
    cap = int(config["max_records_per_provider_query"])
    cursor = "*"
    records: list[dict[str, Any]] = []
    reported_total: int | None = None
    page = 0

    search_text = query["text"]
    if provider.get("exact_phrase_search"):
        search_text = f'"{search_text}"'

    while True:
        params = {
            "search": search_text,
            "filter": (
                f"from_publication_date:{start},"
                f"to_publication_date:{end},"
                f"type:{provider['work_type']}"
            ),
            "per-page": str(per_page),
            "cursor": cursor,
        }
        url = provider["endpoint"] + "?" + urllib.parse.urlencode(params)
        payload = _request_json(url)
        meta = payload.get("meta")
        if not isinstance(meta, dict):
            raise ValueError("OPENALEX_MISSING_META")
        if reported_total is None and isinstance(meta.get("count"), int):
            reported_total = int(meta["count"])
            if reported_total > cap:
                raise ValueError(
                    f"OPENALEX_QUERY_EXCEEDS_FROZEN_CAP:{query['query_id']}:{reported_total}>{cap}"
                )

        results = payload.get("results")
        if not isinstance(results, list):
            raise ValueError("OPENALEX_RESULTS_NOT_LIST")
        if not results:
            break

        page += 1
        for offset, item in enumerate(results, start=1):
            if not isinstance(item, dict):
                continue
            records.append(parse_openalex_item(item, query["query_id"], (page - 1) * per_page + offset))
        if len(records) > cap:
            raise ValueError(f"OPENALEX_HARVEST_EXCEEDS_CAP:{query['query_id']}")

        next_cursor = meta.get("next_cursor")
        if not next_cursor or len(results) < per_page:
            break
        cursor = str(next_cursor)

    return records, {
        "provider": "openalex",
        "query_id": query["query_id"],
        "query_text": query["text"],
        "reported_total": reported_total,
        "retrieved_records": len(records),
        "pages": page,
    }


def _flag(text: str, terms: list[str]) -> bool:
    lowered = _clean_text(text).lower()
    return any(term.lower() in lowered for term in terms)


def build_frame(config: dict[str, Any]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    queries = config.get("queries")
    if not isinstance(queries, list) or not queries:
        raise ValueError("BIBLIO_QUERY_REGISTRY_HAS_NO_QUERIES")

    raw_records: list[dict[str, Any]] = []
    query_receipts: list[dict[str, Any]] = []

    if config["providers"]["crossref"].get("enabled"):
        for query in queries:
            records, receipt = harvest_crossref(config, query)
            raw_records.extend(records)
            query_receipts.append(receipt)

    if config["providers"]["openalex"].get("enabled"):
        for query in queries:
            records, receipt = harvest_openalex(config, query)
            raw_records.extend(records)
            query_receipts.append(receipt)

    merged: dict[str, dict[str, Any]] = {}
    for record in raw_records:
        key = record["identity_key"]
        if key in merged:
            merged[key] = _merge_record(merged[key], record)
        else:
            merged[key] = record

    larceny_terms = list(config["screening_priority_terms"]["larceny"])
    geometry_terms = list(config["screening_priority_terms"]["geometry"])

    frame: list[dict[str, str]] = []
    for key in sorted(merged):
        record = merged[key]
        text_blob = " ".join(
            [
                record.get("title", ""),
                record.get("abstract", ""),
            ]
        )
        frame.append(
            {
                "candidate_id": _candidate_id(key),
                "identity_key": key,
                "doi": record.get("doi", ""),
                "title": record.get("title", ""),
                "publication_year": record.get("publication_year", ""),
                "publication_date": record.get("publication_date", ""),
                "journal": record.get("journal", ""),
                "authors": record.get("authors", ""),
                "abstract": record.get("abstract", ""),
                "source_providers": ";".join(sorted(record["source_providers"])),
                "provider_ids": ";".join(sorted(x for x in record["provider_ids"] if x)),
                "matched_query_ids": ";".join(sorted(record["matched_query_ids"])),
                "source_urls": ";".join(sorted(x for x in record["source_urls"] if x)),
                "best_provider_rank": str(record["best_provider_rank"]),
                "larceny_text_match": "true" if _flag(text_blob, larceny_terms) else "false",
                "geometry_text_match": "true" if _flag(text_blob, geometry_terms) else "false",
                "screen_status": "UNSCREENED",
                "screen_reason": "",
            }
        )

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_RECEIPT_V1",
        "publication_window": config["publication_window"],
        "query_count": len(queries),
        "provider_query_count": len(query_receipts),
        "raw_provider_records": len(raw_records),
        "deduplicated_candidates": len(frame),
        "larceny_text_match_candidates": sum(
            row["larceny_text_match"] == "true" for row in frame
        ),
        "geometry_text_match_candidates": sum(
            row["geometry_text_match"] == "true" for row in frame
        ),
        "all_records_retained_before_screening": True,
        "formal_recurrence_result_open": False,
        "query_receipts": query_receipts,
    }
    return frame, receipt


def write_frame(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FRAME_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()

    registry_bytes = args.registry.read_bytes()
    config = json.loads(registry_bytes.decode("utf-8"))
    frame, receipt = build_frame(config)
    write_frame(args.frame, frame)

    frame_bytes = args.frame.read_bytes()
    receipt["query_registry_sha256"] = _sha256_bytes(registry_bytes)
    receipt["frame_sha256"] = _sha256_bytes(frame_bytes)
    receipt["frame_path"] = str(args.frame.relative_to(ROOT))
    receipt["query_registry_path"] = str(args.registry.relative_to(ROOT))
    receipt["retention_rule"] = config["retention_rule"]
    receipt["deduplication_rule"] = config["deduplication_rule"]
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
