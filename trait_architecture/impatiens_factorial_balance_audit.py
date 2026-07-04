"""Audit the randomized Impatiens factorial design without exporting raw rows.

The audit separately reports observed treatment-assignment cell counts for all rows
with valid assignments and aggregate pre-treatment baseline summaries for the subset
with complete baseline values. It is a descriptive implementation check, not a
post-randomization balance significance test and not an adjustment-selection procedure.
"""

from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from collections import Counter, defaultdict
from io import BytesIO
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from trait_architecture.dryad_archive_schema import _download_archive, _version_url
from trait_architecture.impatiens_models import _number
from trait_architecture.title_validated_dryad_manifest import probe_targets, read_targets


PROCESSED_SUFFIX = "Processed_Data.csv"
TREATMENTS = ("Robbing", "Florivory", "Pollination")
BASELINES = (
    ("Early_Season_Flower_Redness", "identity"),
    ("Early_Season_Condensed_Tannins", "log1p"),
    ("Date_of_First_CH_Flower", "identity"),
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _receipt(targets: list[dict[str, str]]):
    receipts, manifest = probe_targets(targets)
    for receipt in receipts:
        if receipt.manifest_status == "manifest_recovered" and _version_url(receipt):
            return receipt, manifest
    raise RuntimeError("no title-validated Dryad archive available")


def _processed(archive: zipfile.ZipFile) -> list[dict[str, str]]:
    member = next((item for item in archive.infolist() if item.filename.endswith(PROCESSED_SUFFIX)), None)
    if member is None:
        raise RuntimeError("processed table is absent")
    text = archive.read(member).decode("utf-8-sig", errors="replace")
    return [dict(row) for row in csv.DictReader(io.StringIO(text))]


def _label(row: dict[str, str]) -> str:
    levels: list[str] = []
    for field in TREATMENTS:
        value = _text(row.get(field)).upper()
        if value not in {"Y", "N"}:
            raise ValueError(f"{field} must be Y/N")
        levels.append(f"{field}_{value}")
    return "|".join(levels)


def _baseline_value(row: dict[str, str], field: str, transform: str) -> float:
    value = _number(row.get(field), field)
    if transform == "log1p":
        if value < 0:
            raise ValueError(f"{field} must be non-negative for log1p")
        return math.log1p(value)
    return value


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "mean": None, "sd": None, "min": None, "max": None}
    return {
        "n": len(values),
        "mean": mean(values),
        "sd": stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def audit(targets_csv: str | Path, out_dir: str | Path) -> dict[str, object]:
    receipt, manifest = _receipt(read_targets(targets_csv))
    archive_url = f"{_version_url(receipt)}/download"
    archive = zipfile.ZipFile(BytesIO(_download_archive(archive_url, landing_page_url=receipt.landing_page_url)))
    rows = _processed(archive)

    assignment_counts: Counter[str] = Counter()
    baseline_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    invalid_assignment = 0
    baseline_excluded = 0
    for row in rows:
        try:
            label = _label(row)
        except (TypeError, ValueError):
            invalid_assignment += 1
            continue
        assignment_counts[label] += 1
        try:
            for field, transform in BASELINES:
                _baseline_value(row, field, transform)
            baseline_groups[label].append(row)
        except (TypeError, ValueError):
            baseline_excluded += 1

    baseline_rows = []
    for label in sorted(baseline_groups):
        row: dict[str, object] = {"treatment_cell": label, "n_baseline_complete": len(baseline_groups[label])}
        for field, transform in BASELINES:
            summary = _summary([_baseline_value(item, field, transform) for item in baseline_groups[label]])
            for key, value in summary.items():
                row[f"{field}_{transform}_{key}"] = value
        baseline_rows.append(row)

    assignment_rows = [
        {"treatment_cell": label, "n_assignment_valid": count}
        for label, count in sorted(assignment_counts.items())
    ]
    assignment_cell_counts = [int(row["n_assignment_valid"]) for row in assignment_rows]
    baseline_cell_counts = [int(row["n_baseline_complete"]) for row in baseline_rows]
    report = {
        "study_id": receipt.study_id,
        "study_doi": receipt.study_doi,
        "dataset_doi": receipt.dataset_doi,
        "archive_url": archive_url,
        "manifest": manifest,
        "design_contract": "Descriptive audit of observed 2x2x2 assignment cells and pre-treatment covariates. It does not run balance hypothesis tests or select covariates.",
        "processed_rows": len(rows),
        "valid_assignment_rows": sum(assignment_cell_counts),
        "rows_with_invalid_assignment": invalid_assignment,
        "observed_assignment_cell_count": len(assignment_rows),
        "minimum_assignment_cell_n": min(assignment_cell_counts) if assignment_cell_counts else 0,
        "maximum_assignment_cell_n": max(assignment_cell_counts) if assignment_cell_counts else 0,
        "assignment_cells": assignment_rows,
        "baseline_complete_rows": sum(baseline_cell_counts),
        "rows_excluded_from_baseline_summary": baseline_excluded,
        "observed_baseline_complete_cell_count": len(baseline_rows),
        "minimum_baseline_complete_cell_n": min(baseline_cell_counts) if baseline_cell_counts else 0,
        "maximum_baseline_complete_cell_n": max(baseline_cell_counts) if baseline_cell_counts else 0,
        "baseline_complete_cells": baseline_rows,
    }
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "impatiens_factorial_balance_audit.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "processed_rows": len(rows),
        "valid_assignment_rows": sum(assignment_cell_counts),
        "baseline_complete_rows": sum(baseline_cell_counts),
        "observed_assignment_cells": len(assignment_rows),
        "minimum_assignment_cell_n": min(assignment_cell_counts) if assignment_cell_counts else 0,
    }
