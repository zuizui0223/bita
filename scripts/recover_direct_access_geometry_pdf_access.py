"""Recover PDF access URLs from landing pages for formal-frame candidates.

This is an access-only, direction-blind step. It never parses article prose for
eligibility or effect direction. It follows public HTTP(S) landing pages and
records verified PDF URLs when discoverable.
"""
from __future__ import annotations

import argparse
import csv
import html.parser
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ACCESS_FIELDS = (
    "frame_id","doi","title","year","query_ids","openalex_ids","oa_statuses",
    "pdf_urls","landing_urls","frame_source_urls","retrieval_priority","notes",
)

MAX_HTML_BYTES = 4 * 1024 * 1024
MAX_PDF_PROBE_BYTES = 4096
MAX_URLS_PER_RECORD = 12


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.meta_pdf: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        data = {str(k).casefold(): str(v or "") for k, v in attrs}
        if tag.casefold() == "a":
            href = data.get("href", "").strip()
            if href:
                self.links.append(href)
        elif tag.casefold() == "meta":
            name = (data.get("name") or data.get("property") or "").casefold()
            content = data.get("content", "").strip()
            if content and name in {
                "citation_pdf_url",
                "dc.identifier",
                "eprints.document_url",
            }:
                self.meta_pdf.append(content)


def _request(url: str, *, limit: int, accept: str) -> tuple[bytes, str, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("UNSUPPORTED_URL_SCHEME")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 bita-formal-pdf-access-rescue/1.0",
            "Accept": accept,
        },
    )
    with urllib.request.urlopen(req, timeout=35) as resp:
        data = resp.read(limit + 1)
        if len(data) > limit:
            raise ValueError("RESPONSE_TOO_LARGE")
        ctype = str(resp.headers.get("Content-Type") or "")
        final_url = str(resp.geturl())
    return data, ctype, final_url


def _is_pdf_url(url: str) -> bool:
    try:
        data, ctype, final_url = _request(
            url,
            limit=MAX_PDF_PROBE_BYTES,
            accept="application/pdf,*/*;q=0.5",
        )
    except Exception:
        return False
    return (
        data.startswith(b"%PDF")
        or "application/pdf" in ctype.casefold()
        or final_url.casefold().split("?")[0].endswith(".pdf")
    )


def _candidate_links(base_url: str, html: bytes) -> list[str]:
    parser = LinkParser()
    parser.feed(html.decode("utf-8", errors="replace"))
    raw = parser.meta_pdf + parser.links
    candidates: list[str] = []
    seen: set[str] = set()
    for href in raw:
        absolute = urllib.parse.urljoin(base_url, href)
        lower = absolute.casefold()
        if not (
            ".pdf" in lower
            or "/pdf" in lower
            or "download" in lower
            or "fulltext" in lower
            or "article-file" in lower
            or "viewcontent" in lower
        ):
            continue
        if absolute not in seen:
            seen.add(absolute)
            candidates.append(absolute)
    return candidates[:MAX_URLS_PER_RECORD]


def _rescue_record(row: dict[str, str]) -> tuple[list[str], int]:
    seeds: list[str] = []
    for field in ("landing_urls", "frame_source_urls"):
        seeds.extend(u.strip() for u in row[field].split("|") if u.strip())
    if row["doi"].strip():
        seeds.append("https://doi.org/" + row["doi"].strip())

    verified: list[str] = []
    pages_checked = 0
    for seed in list(dict.fromkeys(seeds))[:MAX_URLS_PER_RECORD]:
        if _is_pdf_url(seed):
            verified.append(seed)
            continue
        try:
            data, ctype, final_url = _request(
                seed,
                limit=MAX_HTML_BYTES,
                accept="text/html,application/xhtml+xml,*/*;q=0.5",
            )
        except Exception:
            continue
        pages_checked += 1
        if "html" not in ctype.casefold() and b"<html" not in data[:1000].lower():
            continue
        for candidate in _candidate_links(final_url, data):
            if _is_pdf_url(candidate):
                verified.append(candidate)
                if len(verified) >= 3:
                    return list(dict.fromkeys(verified)), pages_checked
    return list(dict.fromkeys(verified)), pages_checked


def run(input_path: Path, output_path: Path, receipt_path: Path) -> dict[str, object]:
    fields, rows = _read(input_path)
    if fields != ACCESS_FIELDS:
        raise ValueError(
            f"PDF_RESCUE_ACCESS_SCHEMA_MISMATCH:expected={ACCESS_FIELDS}:observed={fields}"
        )

    attempted = 0
    rescued = 0
    pages_checked = 0
    recovered_urls = 0

    for row in rows:
        if row["retrieval_priority"].strip() not in {
            "LANDING_OR_DOI_ONLY",
            "DOI_OR_FRAME_URL_ONLY",
        }:
            continue
        attempted += 1
        urls, checked = _rescue_record(row)
        pages_checked += checked
        if not urls:
            continue
        existing = [u for u in row["pdf_urls"].split("|") if u.strip()]
        merged = list(dict.fromkeys(existing + urls))
        row["pdf_urls"] = "|".join(merged)
        row["retrieval_priority"] = "RESCUED_PDF_AVAILABLE"
        row["notes"] = "DIRECTION_NOT_INSPECTED;PDF_URL_RECOVERED_FROM_PUBLIC_LANDING_PAGE"
        rescued += 1
        recovered_urls += len(urls)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ACCESS_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_PDF_ACCESS_RESCUE_V1",
        "status": "DIRECTION_BLIND_PDF_ACCESS_RESCUE_COMPLETE",
        "records_attempted": attempted,
        "records_rescued": rescued,
        "recovered_pdf_urls": recovered_urls,
        "landing_pages_checked": pages_checked,
        "effect_direction_inspected": False,
        "article_prose_used_for_eligibility": False,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.input, args.output, args.receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
