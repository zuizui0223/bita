#!/usr/bin/env python3
"""Collect candidate source metadata from Crossref and/or OpenAlex.

The script retrieves bibliographic candidates only. It does not decide that a
paper contains a host record, download paywalled full text, or create evidence
ledger rows.

Examples:
python empirical/megachile_leaf_resource/scripts/02_collect_metadata.py \
  --queries empirical/megachile_leaf_resource/data_raw/search_queries.csv \
  --provider crossref \
  --mailto you@example.org \
  --output empirical/megachile_leaf_resource/data_raw/source_metadata_raw.csv \
  --raw-dir empirical/megachile_leaf_resource/data_raw/metadata_responses

python empirical/megachile_leaf_resource/scripts/02_collect_metadata.py \
  --queries empirical/megachile_leaf_resource/data_raw/search_queries.csv \
  --provider both \
  --openalex-api-key "$OPENALEX_API_KEY" \
  --mailto you@example.org \
  --output empirical/megachile_leaf_resource/data_raw/source_metadata_raw.csv \
  --raw-dir empirical/megachile_leaf_resource/data_raw/metadata_responses
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from trait_architecture.host_evidence import canonical_doi, stable_id  # noqa: E402

FIELDS = (
    "source_id",
    "query_id",
    "query_string",
    "provider",
    "provider_record_id",
    "title",
    "first_author",
    "publication_year",
    "doi",
    "source_url",
    "fulltext_url",
    "abstract",
    "retrieved_at_utc",
)
ERROR_FIELDS = ("query_id", "provider", "error_type", "error_message", "retrieved_at_utc")


def text(value: object | None) -> str:
    return "" if value is None else str(value).strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_queries(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"query_id", "query_string"}
    if not rows:
        raise ValueError("query file is empty")
    if not required.issubset(rows[0]):
        raise ValueError(f"query file must contain {sorted(required)}")
    return rows


def request_json(url: str, *, user_agent: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urlopen(request, timeout=45) as response:  # nosec B310: URL is built from fixed API bases
        return json.loads(response.read().decode("utf-8"))


def write_json(path: Path, payload: MappingLike) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)


# A loose alias keeps compatibility with Python 3.10 without importing typing_extensions.
MappingLike = dict[str, Any]


def first_author_from_crossref(item: MappingLike) -> str:
    authors = item.get("author") or []
    if not authors:
        return ""
    author = authors[0]
    return " ".join(part for part in (text(author.get("given")), text(author.get("family"))) if part)


def year_from_crossref(item: MappingLike) -> str:
    for key in ("published-print", "published-online", "issued", "created"):
        date_parts = (item.get(key) or {}).get("date-parts") or []
        if date_parts and date_parts[0]:
            return text(date_parts[0][0])
    return ""


def first_author_from_openalex(item: MappingLike) -> str:
    authorships = item.get("authorships") or []
    if not authorships:
        return ""
    return text((authorships[0].get("author") or {}).get("display_name"))


def abstract_from_openalex(item: MappingLike) -> str:
    inverted = item.get("abstract_inverted_index")
    if not isinstance(inverted, dict):
        return ""
    positioned: list[tuple[int, str]] = []
    for word, positions in inverted.items():
        for position in positions or []:
            if isinstance(position, int):
                positioned.append((position, str(word)))
    return " ".join(word for _, word in sorted(positioned))


def crossref_rows(query: MappingLike, *, rows: int, mailto: str) -> tuple[list[dict[str, str]], MappingLike]:
    params = {"query": query["query_string"], "rows": str(rows)}
    if mailto:
        params["mailto"] = mailto
    payload = request_json(f"https://api.crossref.org/works?{urlencode(params)}", user_agent=f"megachile-host-evidence/0.1 ({mailto or 'contact-not-supplied'})")
    output: list[dict[str, str]] = []
    for item in ((payload.get("message") or {}).get("items") or []):
        title = text((item.get("title") or [""])[0])
        doi = canonical_doi(item.get("DOI"))
        provider_record_id = doi or text(item.get("URL"))
        output.append(
            {
                "source_id": stable_id("src", "crossref", provider_record_id, title),
                "query_id": query["query_id"],
                "query_string": query["query_string"],
                "provider": "crossref",
                "provider_record_id": provider_record_id,
                "title": title,
                "first_author": first_author_from_crossref(item),
                "publication_year": year_from_crossref(item),
                "doi": doi,
                "source_url": text(item.get("URL")),
                "fulltext_url": text(((item.get("link") or [{}])[0]).get("URL")),
                "abstract": text(item.get("abstract")),
                "retrieved_at_utc": utc_now(),
            }
        )
    return output, payload


def openalex_rows(query: MappingLike, *, rows: int, api_key: str, mailto: str) -> tuple[list[dict[str, str]], MappingLike]:
    if not api_key:
        raise ValueError("OpenAlex currently requires --openalex-api-key or OPENALEX_API_KEY")
    params = {"search": query["query_string"], "per_page": str(rows), "api_key": api_key}
    if mailto:
        params["mailto"] = mailto
    payload = request_json(f"https://api.openalex.org/works?{urlencode(params)}", user_agent=f"megachile-host-evidence/0.1 ({mailto or 'contact-not-supplied'})")
    output: list[dict[str, str]] = []
    for item in payload.get("results") or []:
        doi = canonical_doi(item.get("doi"))
        primary = item.get("primary_location") or {}
        best_oa = item.get("best_oa_location") or {}
        source_url = text(primary.get("landing_page_url")) or text(best_oa.get("landing_page_url")) or text(item.get("id"))
        fulltext_url = text(best_oa.get("pdf_url"))
        provider_record_id = text(item.get("id"))
        title = text(item.get("title"))
        output.append(
            {
                "source_id": stable_id("src", "openalex", provider_record_id, title),
                "query_id": query["query_id"],
                "query_string": query["query_string"],
                "provider": "openalex",
                "provider_record_id": provider_record_id,
                "title": title,
                "first_author": first_author_from_openalex(item),
                "publication_year": text(item.get("publication_year")),
                "doi": doi,
                "source_url": source_url,
                "fulltext_url": fulltext_url,
                "abstract": abstract_from_openalex(item),
                "retrieved_at_utc": utc_now(),
            }
        )
    return output, payload


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[MappingLike]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--provider", choices=("crossref", "openalex", "both"), default="crossref")
    parser.add_argument("--rows-per-query", type=int, default=20, choices=range(1, 101))
    parser.add_argument("--delay-seconds", type=float, default=1.0)
    parser.add_argument("--mailto", default=os.environ.get("CONTACT_EMAIL", ""))
    parser.add_argument("--openalex-api-key", default=os.environ.get("OPENALEX_API_KEY", ""))
    args = parser.parse_args()

    if args.delay_seconds < 0:
        raise SystemExit("--delay-seconds must be non-negative")
    queries = read_queries(args.queries)
    providers = ("crossref", "openalex") if args.provider == "both" else (args.provider,)
    collected: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []

    for query in queries:
        for provider in providers:
            try:
                if provider == "crossref":
                    rows, raw = crossref_rows(query, rows=args.rows_per_query, mailto=args.mailto)
                else:
                    rows, raw = openalex_rows(query, rows=args.rows_per_query, api_key=args.openalex_api_key, mailto=args.mailto)
                collected.extend(rows)
                write_json(args.raw_dir / provider / f"{query['query_id']}.json", raw)
            except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                errors.append(
                    {
                        "query_id": query["query_id"],
                        "provider": provider,
                        "error_type": type(error).__name__,
                        "error_message": str(error),
                        "retrieved_at_utc": utc_now(),
                    }
                )
            time.sleep(args.delay_seconds)

    write_csv(args.output, FIELDS, collected)
    write_csv(args.output.with_name("metadata_collection_errors.csv"), ERROR_FIELDS, errors)
    print(f"wrote {len(collected)} metadata rows and {len(errors)} retrieval errors")


if __name__ == "__main__":
    main()
