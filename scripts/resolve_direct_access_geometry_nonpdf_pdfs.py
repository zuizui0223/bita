"""Resolve direct PDF files from landing/DOI-only formal-frame candidates.

This resolver is direction-blind. Landing HTML is used only to discover direct PDF
links; absence of a PDF never causes exclusion and HTML text is not used as evidence
for effect direction or eligibility.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from scripts.inventory_direct_access_geometry_fulltext_access import OUTPUT_FIELDS as ACCESS_FIELDS

MAX_BYTES = 30 * 1024 * 1024
USER_AGENT = "bita-formal-pdf-resolver/1.0"

OUTPUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "candidate_urls",
    "resolved_pdf_url",
    "resolution_status",
    "attempted_urls",
    "notes",
)


class _PdfLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: set[str] = set()
        self.meta_pdfs: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:
        d = {str(k).lower(): str(v or "") for k, v in attrs}
        if tag.lower() == "a":
            href = d.get("href", "").strip()
            if href and (
                ".pdf" in href.lower()
                or "download" in href.lower()
                or "bitstream" in href.lower()
            ):
                self.links.add(href)
        elif tag.lower() == "meta":
            name = d.get("name", "").lower()
            prop = d.get("property", "").lower()
            content = d.get("content", "").strip()
            if content and (
                name in {"citation_pdf_url", "eprints.document_url", "dc.identifier"}
                or prop in {"citation_pdf_url"}
            ):
                if ".pdf" in content.lower() or "bitstream" in content.lower():
                    self.meta_pdfs.add(content)
        elif tag.lower() == "link":
            href = d.get("href", "").strip()
            typ = d.get("type", "").lower()
            if href and "pdf" in typ:
                self.meta_pdfs.add(href)


def _candidate_urls(row: dict[str, str]) -> list[str]:
    values: list[str] = []
    for key in ("landing_urls", "frame_source_urls"):
        values.extend(u.strip() for u in row[key].split("|") if u.strip())
    doi = row["doi"].strip()
    if doi:
        values.append("https://doi.org/" + doi)
    return list(dict.fromkeys(values))


def _request(url: str, *, limit: int = MAX_BYTES) -> tuple[bytes, str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.2",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError("RESOLVE_RESPONSE_TOO_LARGE")
        final_url = response.geturl()
        ctype = str(response.headers.get("Content-Type") or "")
    return data, final_url, ctype


def _is_pdf(data: bytes, ctype: str, url: str) -> bool:
    return (
        data.startswith(b"%PDF")
        or "application/pdf" in ctype.lower()
        or (url.lower().split("?")[0].endswith(".pdf") and data[:4] == b"%PDF")
    )


def _discover_from_html(data: bytes, base_url: str) -> list[str]:
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        return []
    parser = _PdfLinkParser()
    try:
        parser.feed(text)
    except Exception:
        pass
    raw = list(parser.meta_pdfs) + list(parser.links)

    # Conservative fallback for embedded absolute PDF URLs.
    raw.extend(
        html.unescape(match)
        for match in re.findall(
            r'https?://[^\s"\'<>]+?(?:\.pdf|/bitstream/[^\s"\'<>]+)',
            text,
            flags=re.I,
        )
    )

    resolved = []
    for value in raw:
        url = urllib.parse.urljoin(base_url, html.unescape(value))
        if url.startswith(("http://", "https://")):
            resolved.append(url)
    return list(dict.fromkeys(resolved))[:20]


def resolve_row(row: dict[str, str]) -> dict[str, str]:
    seeds = _candidate_urls(row)
    attempted: list[str] = []
    discovered: list[str] = []
    errors: list[str] = []

    for seed in seeds:
        if seed in attempted:
            continue
        attempted.append(seed)
        try:
            data, final_url, ctype = _request(seed)
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{seed}")
            continue
        if _is_pdf(data, ctype, final_url):
            return {
                "frame_id": row["frame_id"],
                "doi": row["doi"],
                "title": row["title"],
                "year": row["year"],
                "candidate_urls": "|".join(seeds),
                "resolved_pdf_url": final_url,
                "resolution_status": "DIRECT_PDF_RESOLVED",
                "attempted_urls": "|".join(attempted),
                "notes": "DIRECTION_NOT_INSPECTED",
            }
        if "html" in ctype.lower() or data.lstrip().startswith(b"<"):
            discovered.extend(_discover_from_html(data, final_url))

    for url in list(dict.fromkeys(discovered)):
        if url in attempted:
            continue
        attempted.append(url)
        try:
            data, final_url, ctype = _request(url)
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{url}")
            continue
        if _is_pdf(data, ctype, final_url):
            return {
                "frame_id": row["frame_id"],
                "doi": row["doi"],
                "title": row["title"],
                "year": row["year"],
                "candidate_urls": "|".join(seeds),
                "resolved_pdf_url": final_url,
                "resolution_status": "DISCOVERED_PDF_RESOLVED",
                "attempted_urls": "|".join(attempted),
                "notes": "DIRECTION_NOT_INSPECTED",
            }

    return {
        "frame_id": row["frame_id"],
        "doi": row["doi"],
        "title": row["title"],
        "year": row["year"],
        "candidate_urls": "|".join(seeds),
        "resolved_pdf_url": "",
        "resolution_status": "NO_DIRECT_PDF_RESOLVED_RETAIN",
        "attempted_urls": "|".join(attempted),
        "notes": (
            "Retained for non-PDF/manual full-text route; landing HTML was not used "
            "to exclude the record. " + ";".join(errors[:3])
        ).strip(),
    }


def run(access_queue: Path, output: Path, receipt: Path) -> dict[str, object]:
    with access_queue.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        if fields != ACCESS_FIELDS:
            raise ValueError("PDF_RESOLVE_ACCESS_SCHEMA_MISMATCH")
        rows = [
            row for row in reader
            if row["retrieval_priority"].strip() == "LANDING_OR_DOI_ONLY"
        ]

    results = [resolve_row(row) for row in rows]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(results)

    counts = Counter(row["resolution_status"] for row in results)
    report = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_NONPDF_PDF_RESOLUTION_V1",
        "status": "NONPDF_CANDIDATE_PDF_RESOLUTION_COMPLETE",
        "candidate_records": len(rows),
        "resolution_counts": dict(sorted(counts.items())),
        "landing_html_used_for_exclusion": False,
        "effect_direction_inspected": False,
    }
    receipt.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--access-queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.access_queue, args.output, args.receipt)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
