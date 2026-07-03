"""Bounded, non-retentive PDF page locator for the fixed c_D source queue.

This module follows c_D source receipts. It downloads only an unauthenticated PDF
response advertised by Crossref or a DOI-exact OpenAlex public-fulltext location,
keeps it in a temporary directory, and emits page *locators* (page number plus
matched extraction keywords). It never stores article text or PDFs in repository
artefacts, never extracts numerical effects, and never promotes a source into B2.
Its sole purpose is to determine whether a public source can be read efficiently
enough for a human C4 extraction.

PDF text is used only to locate candidate pages. Any later numerical extraction
must visually verify the relevant table/figure/page and meet the registered c_D
extraction gate.
"""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError
from urllib.request import Request, urlopen


MAX_PDF_BYTES = 25 * 1024 * 1024
USER_AGENT = "bita c-d-fulltext-locator/0.1"
KEYWORDS = (
    "alkaloid", "nicotine", "zygacine", "concentration", "dose", "natural",
    "nectar", "syrup", "visitation", "visit", "foraging", "feeding",
    "frequency", "duration", "time per flower", "table", "figure", "replicate",
)
LOCATOR_FIELDS = (
    "queue_id", "study_id", "study_cluster_id", "doi", "taxon", "trait_class",
    "outcome_class", "design_class", "source_url", "pdf_access_status", "http_status",
    "content_type", "pdf_bytes", "page_count", "candidate_pages", "locator_status",
    "locator_note", "do_not_infer",
)
DO_NOT_INFER = (
    "This output locates candidate PDF pages only. It does not verify table values, "
    "dose relevance, denominators, variance, experimental unit, effect size, or B2 eligibility."
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _pdf_urls(row: dict[str, str]) -> list[str]:
    urls = [url.strip() for url in _text(row.get("crossref_content_urls")).split(";") if url.strip()]
    return [url for url in urls if "/pdf/" in url.lower() or "/pdfdirect/" in url.lower() or url.lower().endswith(".pdf")]


def _fetch_pdf(url: str) -> tuple[int, str, bytes]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"})
    with urlopen(request, timeout=60) as response:  # nosec B310: URL was declared by an exact-DOI source receipt
        status = int(getattr(response, "status", response.getcode()))
        content_type = _text(response.headers.get("Content-Type")).lower()
        payload = response.read(MAX_PDF_BYTES + 1)
    if len(payload) > MAX_PDF_BYTES:
        raise ValueError(f"response exceeds {MAX_PDF_BYTES} byte cap")
    return status, content_type, payload


def _terms_on_page(text: str) -> list[str]:
    folded = text.casefold()
    found: list[str] = []
    for term in KEYWORDS:
        if term in folded:
            found.append(term)
    return found


def _candidate_pages(pdf_bytes: bytes) -> tuple[int, str]:
    """Return page count and stable candidate-page JSON without persisting article text."""

    try:
        from pypdf import PdfReader
    except ImportError as error:  # pragma: no cover - workflow installs pypdf
        raise RuntimeError("pypdf is required for PDF page location") from error

    with tempfile.NamedTemporaryFile(suffix=".pdf") as handle:
        handle.write(pdf_bytes)
        handle.flush()
        reader = PdfReader(handle.name)
        pages: list[dict[str, object]] = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            terms = _terms_on_page(text)
            if terms:
                # Keyword score prioritizes pages that contain outcome plus treatment terms.
                score = len(terms)
                pages.append({"page": index, "matched_terms": terms, "score": score})
        page_count = len(reader.pages)
    pages.sort(key=lambda row: (-int(row["score"]), int(row["page"])))
    return page_count, json.dumps(pages[:8], sort_keys=True)


def locate_receipt_row(
    row: dict[str, str],
    *,
    fetch_pdf: Callable[[str], tuple[int, str, bytes]] = _fetch_pdf,
) -> dict[str, str]:
    """Attempt only declared PDF URLs, returning the first readable candidate."""

    base = {
        "queue_id": _text(row.get("queue_id")),
        "study_id": _text(row.get("study_id")),
        "study_cluster_id": _text(row.get("study_cluster_id")),
        "doi": _text(row.get("doi")),
        "taxon": _text(row.get("taxon")),
        "trait_class": _text(row.get("trait_class")),
        "outcome_class": _text(row.get("outcome_class")),
        "design_class": _text(row.get("design_class")),
        "source_url": "",
        "pdf_access_status": "no_declared_pdf_url",
        "http_status": "",
        "content_type": "",
        "pdf_bytes": "",
        "page_count": "",
        "candidate_pages": "",
        "locator_status": "not_run",
        "locator_note": "The source receipt supplied no PDF-like URL.",
        "do_not_infer": DO_NOT_INFER,
    }
    urls = _pdf_urls(row)
    if not urls:
        return base
    failures: list[str] = []
    for url in urls:
        try:
            status, content_type, payload = fetch_pdf(url)
            if status >= 400:
                failures.append(f"HTTP {status} at {url}")
                continue
            if not payload.startswith(b"%PDF"):
                failures.append(f"non-PDF response at {url}")
                continue
            page_count, candidate_pages = _candidate_pages(payload)
            return {
                **base,
                "source_url": url,
                "pdf_access_status": "public_pdf_recovered",
                "http_status": str(status),
                "content_type": content_type,
                "pdf_bytes": str(len(payload)),
                "page_count": str(page_count),
                "candidate_pages": candidate_pages,
                "locator_status": "candidate_pages_located",
                "locator_note": "Temporary public PDF parsed only to locate likely dose/outcome/table pages; no article text retained.",
            }
        except HTTPError as error:
            failures.append(f"HTTP {error.code} at {url}")
        except Exception as error:
            failures.append(f"{type(error).__name__} at {url}: {error}")
    return {
        **base,
        "pdf_access_status": "public_pdf_not_recovered",
        "locator_status": "access_or_parse_failed",
        "locator_note": "; ".join(failures),
    }


def read_receipts(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    required = {"queue_id", "doi", "crossref_content_urls", "study_cluster_id"}
    if rows and not required.issubset(rows[0]):
        raise ValueError("c_D source receipt file lacks required fields")
    return rows


def read_public_source_receipts(path: str | Path) -> list[dict[str, str]]:
    """Read only exact-DOI public-PDF candidates from the provenance-separated scout."""

    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    required = {
        "queue_id", "study_id", "study_cluster_id", "doi", "content_url",
        "resolution_status", "relation_to_article",
    }
    if rows and not required.issubset(rows[0]):
        raise ValueError("c_D public-source receipt file lacks required fields")
    candidates: list[dict[str, str]] = []
    for row in rows:
        if row["resolution_status"] != "public_fulltext_candidate":
            continue
        if row["relation_to_article"] != "exact_article_doi" or not row["content_url"]:
            continue
        candidates.append({
            "queue_id": row["queue_id"],
            "study_id": row["study_id"],
            "study_cluster_id": row["study_cluster_id"],
            "doi": row["doi"],
            "taxon": _text(row.get("taxon")),
            "trait_class": _text(row.get("trait_class")),
            "outcome_class": _text(row.get("outcome_class")),
            "design_class": _text(row.get("design_class")),
            "crossref_content_urls": row["content_url"],
        })
    return candidates


def locate_receipts(
    rows: Iterable[dict[str, str]],
    *,
    fetch_pdf: Callable[[str], tuple[int, str, bytes]] = _fetch_pdf,
) -> list[dict[str, str]]:
    return [locate_receipt_row(row, fetch_pdf=fetch_pdf) for row in rows]


def write_locators(path: str | Path, rows: Iterable[dict[str, str]]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOCATOR_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return {
        "queue_count": len(rows),
        "public_pdf_recovered": sum(row["pdf_access_status"] == "public_pdf_recovered" for row in rows),
        "candidate_pages_located": sum(row["locator_status"] == "candidate_pages_located" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
