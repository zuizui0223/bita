"""Normalize bibliographic database exports into the frozen Q1-Q8 raw schema.

This importer is outcome-blind. It converts provider-specific fields only; it never
filters records by relevance, effect direction, study design, species, or outcome.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Iterable

QUERY_IDS = {f"Q{i}" for i in range(1, 9)}
MIN_DATE = date(2000, 1, 1)
MAX_DATE = date(2026, 9, 24)
OUTPUT_FIELDS = (
    "source_db",
    "query_id",
    "record_id",
    "doi",
    "title",
    "year",
    "authors",
    "publication",
    "url",
    "search_date",
)

CSV_ALIASES = {
    "record_id": (
        "record_id", "EID", "eid", "UT", "UT (Unique WOS ID)",
        "Accession Number", "Accession number", "OpenAlex ID", "ID",
    ),
    "doi": ("doi", "DOI", "Doi", "DI"),
    "title": ("title", "Title", "Document Title", "Article Title", "TI"),
    "year": ("year", "Year", "Publication Year", "PY"),
    "authors": (
        "authors", "Authors", "Author(s)", "Author full names", "AU",
        "Authors with affiliations",
    ),
    "publication": (
        "publication", "Publication", "Source title", "Source Title",
        "Publication Name", "SO", "Journal", "Source",
    ),
    "url": ("url", "URL", "Url", "Link", "Document URL", "Full Text Link"),
}


def _norm_doi(value: object) -> str:
    text = str(value or "").strip()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.I)
    text = re.sub(r"^doi:\s*", "", text, flags=re.I)
    return text.rstrip(" .;,")


def _first(row: dict[str, object], aliases: Iterable[str]) -> str:
    for key in aliases:
        value = row.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def _year_from_date_parts(item: dict[str, object]) -> str:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        value = item.get(key)
        if not isinstance(value, dict):
            continue
        parts = value.get("date-parts")
        if (
            isinstance(parts, list)
            and parts
            and isinstance(parts[0], list)
            and parts[0]
        ):
            return str(parts[0][0])
    return ""


def _join_crossref_authors(item: dict[str, object]) -> str:
    authors = item.get("author")
    if not isinstance(authors, list):
        return ""
    names = []
    for author in authors:
        if not isinstance(author, dict):
            continue
        given = str(author.get("given") or "").strip()
        family = str(author.get("family") or "").strip()
        name = " ".join(part for part in (given, family) if part)
        if name:
            names.append(name)
    return "; ".join(names)


def _join_openalex_authors(item: dict[str, object]) -> str:
    authorships = item.get("authorships")
    if not isinstance(authorships, list):
        return ""
    names = []
    for authorship in authorships:
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author")
        if isinstance(author, dict):
            name = str(author.get("display_name") or "").strip()
            if name:
                names.append(name)
    return "; ".join(names)


def _crossref_rows(payload: object) -> list[dict[str, str]]:
    if isinstance(payload, dict):
        message = payload.get("message")
        if isinstance(message, dict):
            items = message.get("items")
        else:
            items = payload.get("items")
    else:
        items = payload
    if not isinstance(items, list):
        raise ValueError("BIB_EXPORT_CROSSREF_ITEMS_NOT_FOUND")

    rows = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("BIB_EXPORT_CROSSREF_ITEM_NOT_OBJECT")
        titles = item.get("title")
        title = (
            str(titles[0]).strip()
            if isinstance(titles, list) and titles
            else str(titles or "").strip()
        )
        containers = item.get("container-title")
        publication = (
            str(containers[0]).strip()
            if isinstance(containers, list) and containers
            else str(containers or "").strip()
        )
        doi = _norm_doi(item.get("DOI"))
        record_id = doi or str(item.get("URL") or "").strip()
        rows.append({
            "record_id": record_id,
            "doi": doi,
            "title": title,
            "year": _year_from_date_parts(item),
            "authors": _join_crossref_authors(item),
            "publication": publication,
            "url": str(item.get("URL") or "").strip(),
        })
    return rows


def _openalex_rows(payload: object) -> list[dict[str, str]]:
    if isinstance(payload, dict):
        items = payload.get("results")
    else:
        items = payload
    if not isinstance(items, list):
        raise ValueError("BIB_EXPORT_OPENALEX_RESULTS_NOT_FOUND")

    rows = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("BIB_EXPORT_OPENALEX_ITEM_NOT_OBJECT")
        primary = item.get("primary_location")
        publication = ""
        url = ""
        if isinstance(primary, dict):
            source = primary.get("source")
            if isinstance(source, dict):
                publication = str(source.get("display_name") or "").strip()
            url = str(primary.get("landing_page_url") or "").strip()
        if not url:
            url = str(item.get("id") or "").strip()
        rows.append({
            "record_id": str(item.get("id") or "").strip(),
            "doi": _norm_doi(item.get("doi")),
            "title": str(item.get("title") or item.get("display_name") or "").strip(),
            "year": str(item.get("publication_year") or "").strip(),
            "authors": _join_openalex_authors(item),
            "publication": publication,
            "url": url,
        })
    return rows


def _tabular_rows(path: Path, delimiter: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("BIB_EXPORT_TABULAR_HEADER_MISSING")
        rows = []
        for row in reader:
            rows.append({
                field: _first(row, aliases)
                for field, aliases in CSV_ALIASES.items()
            })
    return rows


def _generic_rows(path: Path, delimiter: str) -> list[dict[str, str]]:
    return _tabular_rows(path, delimiter)


def _detect_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and (
            isinstance(payload.get("message"), dict)
            or "items" in payload
        ):
            return "crossref_json"
        if isinstance(payload, dict) and "results" in payload:
            return "openalex_json"
        raise ValueError("BIB_EXPORT_JSON_PROVIDER_NOT_DETECTED")
    if suffix in {".tsv", ".txt"}:
        return "wos_tsv"
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            header = next(csv.reader(handle), [])
        normalized = {x.strip() for x in header}
        if {"EID", "Title"} <= normalized or "Source title" in normalized:
            return "scopus_csv"
        return "generic_csv"
    raise ValueError(f"BIB_EXPORT_FORMAT_NOT_DETECTED:{suffix}")


def _validate_source_rows(
    rows: list[dict[str, str]],
    *,
    source_db: str,
    query_id: str,
    search_date: str,
) -> list[dict[str, str]]:
    if query_id not in QUERY_IDS:
        raise ValueError(f"BIB_EXPORT_INVALID_QUERY_ID:{query_id}")
    try:
        search_day = date.fromisoformat(search_date)
    except ValueError as exc:
        raise ValueError(f"BIB_EXPORT_INVALID_SEARCH_DATE:{search_date}") from exc
    if not source_db.strip():
        raise ValueError("BIB_EXPORT_SOURCE_DB_REQUIRED")
    if not rows:
        raise ValueError("BIB_EXPORT_ZERO_ROWS_REQUIRES_AMENDMENT")

    output = []
    seen_record_ids: set[str] = set()
    for index, row in enumerate(rows, start=1):
        title = row.get("title", "").strip()
        record_id = row.get("record_id", "").strip()
        year_text = row.get("year", "").strip()

        if not title:
            raise ValueError(f"BIB_EXPORT_MISSING_TITLE:row={index}")
        if not record_id:
            raise ValueError(f"BIB_EXPORT_MISSING_RECORD_ID:row={index}")
        if record_id in seen_record_ids:
            raise ValueError(f"BIB_EXPORT_DUPLICATE_RECORD_ID_WITHIN_QUERY:{record_id}")
        seen_record_ids.add(record_id)
        try:
            year = int(year_text)
        except ValueError as exc:
            raise ValueError(f"BIB_EXPORT_INVALID_YEAR:row={index}:{year_text}") from exc
        if year < MIN_DATE.year or year > MAX_DATE.year:
            raise ValueError(f"BIB_EXPORT_YEAR_OUT_OF_WINDOW:row={index}:{year}")

        output.append({
            "source_db": source_db.strip(),
            "query_id": query_id,
            "record_id": record_id,
            "doi": _norm_doi(row.get("doi")),
            "title": title,
            "year": str(year),
            "authors": row.get("authors", "").strip(),
            "publication": row.get("publication", "").strip(),
            "url": row.get("url", "").strip(),
            "search_date": search_day.isoformat(),
        })
    return output


def normalize(
    path: Path,
    *,
    fmt: str,
    source_db: str | None,
    query_id: str,
    search_date: str,
) -> list[dict[str, str]]:
    selected = _detect_format(path) if fmt == "auto" else fmt

    if selected == "crossref_json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = _crossref_rows(payload)
        provider = source_db or "Crossref"
    elif selected == "openalex_json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = _openalex_rows(payload)
        provider = source_db or "OpenAlex"
    elif selected == "scopus_csv":
        rows = _tabular_rows(path, ",")
        provider = source_db or "Scopus"
    elif selected == "wos_tsv":
        rows = _tabular_rows(path, "\t")
        provider = source_db or "WebOfScience"
    elif selected == "generic_csv":
        rows = _generic_rows(path, ",")
        provider = source_db or "GenericBibliographicDB"
    else:
        raise ValueError(f"BIB_EXPORT_UNSUPPORTED_FORMAT:{selected}")

    return _validate_source_rows(
        rows,
        source_db=provider,
        query_id=query_id,
        search_date=search_date,
    )


def write(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--format",
        default="auto",
        choices=(
            "auto",
            "scopus_csv",
            "wos_tsv",
            "crossref_json",
            "openalex_json",
            "generic_csv",
        ),
    )
    parser.add_argument("--source-db")
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--search-date", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = normalize(
        args.input,
        fmt=args.format,
        source_db=args.source_db,
        query_id=args.query_id,
        search_date=args.search_date,
    )
    write(rows, args.output)
    print(json.dumps({
        "status": "BIB_EXPORT_NORMALIZED_OUTCOME_BLIND",
        "source_db": rows[0]["source_db"],
        "query_id": args.query_id,
        "rows": len(rows),
        "output": str(args.output),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
