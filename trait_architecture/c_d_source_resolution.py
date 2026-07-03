"""Access-receipt adapter for the fixed c_D full-text reading queue.

The B1 direction layer identifies a small set of chemical-barrier manipulation
studies as the current strongest support for ``c_D``. This module converts the
already-registered full-text reading queue into the repository's standard Crossref
access-receipt pattern, preserving Crossref-advertised article-content URLs for
subsequent bounded source reading. It records source reachability and linked-data
relation metadata only; it does not inspect article text, extract an effect,
classify dose, or promote any study into B2.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

from .d_a_source_resolver import (
    CROSSREF_WORKS,
    RECEIPT_FIELDS,
    SourceReceipt,
    resolve_candidates,
    summarise,
)


REQUIRED_QUEUE_FIELDS = frozenset({"queue_id", "doi", "study_id", "study_cluster_id"})
CONTENT_URL_FIELD = "crossref_content_urls"
DO_NOT_INFER = (
    "Access and relation metadata only. Do not infer treatment doses, natural-dose "
    "relevance, response units, experimental unit, effect value, or B2 eligibility."
)


def _text(value: object) -> str:
    return str(value or "").strip()


def read_fulltext_queue(path: str | Path) -> list[dict[str, str]]:
    """Read the fixed c_D queue and validate its identity fields."""

    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError("c_D full-text reading queue is empty")
    missing = REQUIRED_QUEUE_FIELDS.difference(rows[0])
    if missing:
        raise ValueError("c_D full-text reading queue missing fields: " + ", ".join(sorted(missing)))
    identifiers = [row["queue_id"] for row in rows]
    if any(not identifier for identifier in identifiers) or len(identifiers) != len(set(identifiers)):
        raise ValueError("c_D full-text reading queue requires unique non-empty queue_id values")
    return rows


def queue_to_source_candidates(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Map registered queue rows to the generic DOI source-resolver interface."""

    candidates: list[dict[str, str]] = []
    for row in rows:
        doi = _text(row.get("doi"))
        candidates.append({
            "candidate_id": _text(row.get("queue_id")),
            "source": f"doi:{doi}" if doi else "",
        })
    return candidates


def crossref_content_urls(doi: str, *, fetch_json) -> str:
    """Return unique Crossref-advertised full-text URLs, without fetching content."""

    if not doi:
        return ""
    try:
        status, payload = fetch_json(CROSSREF_WORKS + quote(doi, safe=""))
    except Exception:
        return ""
    if status >= 400 or not isinstance(payload, dict):
        return ""
    message = payload.get("message")
    if not isinstance(message, dict):
        return ""
    links = message.get("link")
    if not isinstance(links, list):
        return ""
    urls: list[str] = []
    for link in links:
        if not isinstance(link, dict):
            continue
        url = _text(link.get("URL"))
        if url and url not in urls:
            urls.append(url)
    return ";".join(urls)


def resolve_fulltext_queue(
    rows: Iterable[dict[str, str]],
    *,
    fetch_json,
) -> list[dict[str, str]]:
    """Resolve fixed c_D queue DOIs and retain queue metadata on every receipt."""

    queue_rows = list(rows)
    receipts = resolve_candidates(queue_to_source_candidates(queue_rows), fetch_json=fetch_json)
    receipt_by_queue = {receipt.candidate_id: receipt for receipt in receipts}
    output: list[dict[str, str]] = []
    for row in queue_rows:
        receipt = receipt_by_queue[row["queue_id"]]
        output.append({
            "queue_id": row["queue_id"],
            "study_id": _text(row.get("study_id")),
            "study_cluster_id": _text(row.get("study_cluster_id")),
            "taxon": _text(row.get("taxon")),
            "trait_class": _text(row.get("trait_class")),
            "outcome_class": _text(row.get("outcome_class")),
            "design_class": _text(row.get("design_class")),
            "primary_reading_goal": _text(row.get("primary_reading_goal")),
            CONTENT_URL_FIELD: crossref_content_urls(receipt.doi, fetch_json=fetch_json),
            **asdict(receipt),
            "do_not_infer": DO_NOT_INFER,
        })
    return output


def receipt_fields() -> tuple[str, ...]:
    """Return queue metadata plus the standard resolver receipt schema."""

    prefix = (
        "queue_id", "study_id", "study_cluster_id", "taxon", "trait_class",
        "outcome_class", "design_class", "primary_reading_goal", CONTENT_URL_FIELD,
    )
    return (*prefix, *RECEIPT_FIELDS)


def write_receipts(out_dir: str | Path, rows: Iterable[dict[str, str]]) -> dict[str, object]:
    """Write c_D source receipts and an access-only summary."""

    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "c_d_fulltext_source_receipts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=receipt_fields())
        writer.writeheader()
        writer.writerows(rows)
    base_receipts = [
        SourceReceipt(**{field: row[field] for field in RECEIPT_FIELDS})
        for row in rows
    ]
    report = {
        **summarise(base_receipts),
        "queue_count": len(rows),
        "rows_with_crossref_content_url": sum(bool(row[CONTENT_URL_FIELD]) for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "c_d_fulltext_source_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
