"""Audit the randomized Impatiens factorial design without exporting raw rows.

The audit reports treatment-cell counts and aggregate pre-treatment baseline
summaries for first-flower date, flower redness, and log1p floral tannins. It is a
descriptive implementation check, not a post-randomization balance significance test
and not an adjustment-selection procedure.
"""

from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from collections import defaultdict
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

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    excluded = 0
    for row in rows:
        try:
            label = _label(row)
            for field, transform in BASELINES:
                _baseline_value(row, field, transform)
            groups[label].append(row)
        except (TypeError, ValueError):
            excluded += 1

    cell_rows = []
    for label in sorted(groups):
        row: dict[str, object] = {"treatment_cell": label, "n": len(groups[label])}
        for field, transform in BASELINES:
            summary = _summary([_baseline_value(item, field, transform) for item in groups[label]])
            for key, value in summary.items():
                row[f"{field}_{transform}_{key}"] = value
        cell_rows.append(row)

    cell_counts = [int(row["n"]) for row in cell_rows]
    report = {
        "study_id": receipt.study_id,
        "study_doi": receipt.study_doi,
        "dataset_doi": receipt.dataset_doi,
        "archive_url": archive_url,
        "manifest": manifest,
        "design_contract": "Descriptive audit of observed 2x2x2 assignment cells and pre-treatment covariates. It does not run balance hypothesis tests or select covariates.",
        "processed_rows": len(rows),
        "rows_with_complete_treatments_and_baselines": sum(cell_counts),
        "rows_excluded_from_baseline_audit": excluded,
        "observed_factorial_cell_count": len(cell_rows),
        "minimum_cell_n": min(cell_counts) if cell_counts else 0,
        "maximum_cell_n": max(cell_counts) if cell_counts else 0,
        "cells": cell_rows,
    }
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "impatiens_factorial_balance_audit.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "processed_rows": len(rows),
        "complete_baseline_rows": sum(cell_counts),
        "observed_factorial_cells": len(cell_rows),
        "minimum_cell_n": min(cell_counts) if cell_counts else 0,
    }
