"""Audit public article/repository routes for the fixed c_D reading queue.

The fixed c_D candidate set must not grow during source recovery. This module
applies DOI-exact Crossref/OpenAlex/repository and Unpaywall lookups to each of its
four registered studies and writes provenance-separated receipts. A public location
is an access lead only, never a numerical effect or evidence of a natural-dose
comparison.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote

from .c_d_source_resolution import read_fulltext_queue
from .public_article_source_scout import (
    ARTICLE_RECEIPT_FIELDS,
    ArticleSourceReceipt,
    audit_study_sources,
    normalise_doi,
)


UNPAYWALL_WORKS = "https://api.unpaywall.org/v2/"
SCOUT_FIELDS = (
    "queue_id", "study_id", "study_cluster_id", "taxon", "trait_class",
    "outcome_class", "design_class", "primary_reading_goal", *ARTICLE_RECEIPT_FIELDS,
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _url(value: object) -> str:
    value = _text(value)
    return value if value.startswith(("https://", "http://")) else ""


def _unpaywall_locations(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
    best = payload.get("best_oa_location")
    if isinstance(best, dict):
        yield best
    locations = payload.get("oa_locations")
    if isinstance(locations, list):
        for location in locations:
            if isinstance(location, dict):
                yield location


def unpaywall_receipts(
    doi: str,
    *,
    email: str,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> list[ArticleSourceReceipt]:
    """Return DOI-exact OA candidates advertised by Unpaywall, without fetching files."""

    doi = normalise_doi(doi)
    if not email:
        raise ValueError("Unpaywall lookup requires a contact email")
    request_url = f"{UNPAYWALL_WORKS}{quote(doi, safe='')}?email={quote(email, safe='@._+-')}"
    try:
        status, payload = fetch_json(request_url)
        if status >= 400 or not isinstance(payload, dict):
            raise RuntimeError(f"HTTP {status}")
        title = _text(payload.get("title"))
        identifier = _text(payload.get("doi")) or doi
        receipts: list[ArticleSourceReceipt] = []
        seen: set[str] = set()
        for location in _unpaywall_locations(payload):
            pdf = _url(location.get("url_for_pdf"))
            landing = _url(location.get("url"))
            candidate = pdf or landing
            if not candidate or candidate in seen:
                continue
            seen.add(candidate)
            version = _text(location.get("version"))
            host_type = _text(location.get("host_type"))
            receipts.append(ArticleSourceReceipt(
                study_doi=doi,
                provider="Unpaywall",
                source_kind="open_access_location",
                resolution_status="public_fulltext_candidate" if pdf else "public_landing_candidate",
                request_url=request_url,
                source_identifier=identifier,
                title=title,
                landing_page_url=landing,
                content_url=pdf,
                content_type="application/pdf" if pdf else "",
                license_label=_text(location.get("license")),
                relation_to_article="exact_article_doi",
                notes=(
                    "Unpaywall identifies a DOI-exact public PDF candidate. Accessibility and table contents remain untested."
                    if pdf else
                    "Unpaywall identifies a DOI-exact OA landing page but no PDF URL."
                ) + (f" host_type={host_type}; version={version}." if host_type or version else ""),
            ))
        if not receipts:
            receipts.append(ArticleSourceReceipt(
                study_doi=doi,
                provider="Unpaywall",
                source_kind="open_access_location",
                resolution_status="not_found",
                request_url=request_url,
                source_identifier=identifier,
                title=title,
                landing_page_url="",
                content_url="",
                content_type="",
                license_label="",
                relation_to_article="exact_article_doi",
                notes="No DOI-exact public full-text location was returned by Unpaywall.",
            ))
        return receipts
    except Exception as error:
        return [ArticleSourceReceipt(
            study_doi=doi,
            provider="Unpaywall",
            source_kind="open_access_location",
            resolution_status="access_failed",
            request_url=request_url,
            source_identifier="",
            title="",
            landing_page_url="",
            content_url="",
            content_type="",
            license_label="",
            relation_to_article="not_checked",
            notes=f"{type(error).__name__}: {error}",
        )]


def scout_queue(
    rows: Iterable[dict[str, str]],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
    unpaywall_email: str,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Return separate source receipts and per-study source-feasibility reports."""

    rows = list(rows)
    receipts: list[dict[str, str]] = []
    reports: list[dict[str, object]] = []
    for row in rows:
        source_receipts, report = audit_study_sources(
            study_doi=row["doi"],
            queue_id=row["queue_id"],
            study_id=row["study_id"],
            fetch_json=fetch_json,
        )
        source_receipts = [*source_receipts, *unpaywall_receipts(
            row["doi"], email=unpaywall_email, fetch_json=fetch_json,
        )]
        reports.append({
            "queue_id": row["queue_id"],
            "study_id": row["study_id"],
            "study_cluster_id": row["study_cluster_id"],
            "doi": row["doi"],
            "taxon": _text(row.get("taxon")),
            **report,
            "has_unpaywall_public_pdf_candidate": any(
                receipt.provider == "Unpaywall"
                and receipt.resolution_status == "public_fulltext_candidate"
                and bool(receipt.content_url)
                for receipt in source_receipts
            ),
        })
        for receipt in source_receipts:
            receipts.append({
                "queue_id": row["queue_id"],
                "study_id": row["study_id"],
                "study_cluster_id": row["study_cluster_id"],
                "taxon": _text(row.get("taxon")),
                "trait_class": _text(row.get("trait_class")),
                "outcome_class": _text(row.get("outcome_class")),
                "design_class": _text(row.get("design_class")),
                "primary_reading_goal": _text(row.get("primary_reading_goal")),
                **{key: _text(value) for key, value in asdict(receipt).items()},
            })
    report = {
        "queue_count": len(rows),
        "study_reports": reports,
        "studies_with_public_pdf_candidate": sum(bool(row["has_public_pdf_candidate"]) for row in reports),
        "studies_with_unpaywall_public_pdf_candidate": sum(
            bool(row["has_unpaywall_public_pdf_candidate"]) for row in reports
        ),
        "studies_with_linked_repository_manifest": sum(bool(row["has_linked_repository_manifest"]) for row in reports),
        "decision_boundary": (
            "Public article and repository routes are source-access leads only. They do not establish "
            "file identity beyond the recorded relation, article table contents, effect values, or B2 eligibility."
        ),
    }
    return receipts, report


def write_scout(out_dir: str | Path, receipts: Iterable[dict[str, str]], report: dict[str, object]) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "c_d_public_source_receipts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCOUT_FIELDS)
        writer.writeheader()
        writer.writerows(receipts)
    (destination / "c_d_public_source_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )


def scout_queue_file(
    queue_csv: str | Path,
    out_dir: str | Path,
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
    unpaywall_email: str,
) -> dict[str, object]:
    receipts, report = scout_queue(
        read_fulltext_queue(queue_csv),
        fetch_json=fetch_json,
        unpaywall_email=unpaywall_email,
    )
    write_scout(out_dir, receipts, report)
    return report
