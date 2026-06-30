"""Inspect a DOI-linked Dryad package using file names and table headers only."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable

from trait_architecture.dalechampia_linked_panel import (
    SCHEMA_FIELDS,
    TableSchema,
    _fetch_bytes,
    _fetch_json,
    audit_package,
)


def audit_exact_dryad_panel(
    *,
    article_doi: str,
    dataset_doi: str,
    study_label: str,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_bytes: Callable[[str], bytes] = _fetch_bytes,
) -> tuple[list[TableSchema], dict[str, object]]:
    """Recover the manifest and headers for an exact article-linked package."""

    schemas, report = audit_package(
        article_doi=article_doi,
        dataset_doi=dataset_doi,
        fetch_json=fetch_json,
        fetch_bytes=fetch_bytes,
    )
    report["study_label"] = study_label
    report["decision_boundary"] = (
        "This audit records package manifest and headers only. It does not establish "
        "trait roles, direct effects, or an empirical evidence level."
    )
    return schemas, report


def write_exact_dryad_panel_audit(
    out_dir: str | Path,
    schemas: list[TableSchema],
    report: dict[str, object],
    *,
    output_stem: str,
) -> None:
    """Write header-only outputs using a study-specific filename prefix."""

    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    with (output / f"{output_stem}_header_schemas.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        for row in schemas:
            writer.writerow(asdict(row))
    (output / f"{output_stem}_audit.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
