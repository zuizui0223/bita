"""Audit public article/repository routes for the fixed c_D reading queue.

The fixed c_D candidate set must not grow during source recovery. This module
applies the repository's existing DOI-exact Crossref/OpenAlex/repository scout to
each of its four registered studies and writes provenance-separated receipts. A
public location is an access lead only, never a numerical effect or evidence of a
natural-dose comparison.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Iterable

from .c_d_source_resolution import read_fulltext_queue
from .public_article_source_scout import ARTICLE_RECEIPT_FIELDS, audit_study_sources


SCOUT_FIELDS = (
    "queue_id", "study_id", "study_cluster_id", "taxon", "trait_class",
    "outcome_class", "design_class", "primary_reading_goal", *ARTICLE_RECEIPT_FIELDS,
)


def _text(value: object) -> str:
    return str(value or "").strip()


def scout_queue(
    rows: Iterable[dict[str, str]],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
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
        reports.append({
            "queue_id": row["queue_id"],
            "study_id": row["study_id"],
            "study_cluster_id": row["study_cluster_id"],
            "doi": row["doi"],
            "taxon": _text(row.get("taxon")),
            **report,
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
) -> dict[str, object]:
    receipts, report = scout_queue(read_fulltext_queue(queue_csv), fetch_json=fetch_json)
    write_scout(out_dir, receipts, report)
    return report
