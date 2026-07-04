"""Fit predeclared randomized factorial fitness-component models for *Impatiens*.

The source experiment randomised supplemental nectar robbing, florivory, and
pollination assignments. These models estimate treatment-assignment contrasts on two
reproductive components using the full 2x2x2 factorial, effect coding (N=-0.5,
Y=+0.5), and a pre-treatment phenology adjustment. They deliberately omit the
observational flower redness and floral tannin predictors so that treatment effects
are not conditioned on post hoc trait missingness or misrepresented as trait effects.

Raw Dryad observations are read only in memory. Outputs contain aggregate
coefficients and diagnostics, not individual records.
"""

from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from dataclasses import asdict
from io import BytesIO
from pathlib import Path
from typing import Any

from trait_architecture.dryad_archive_schema import _download_archive, _version_url
from trait_architecture.impatiens_models import _number, transform, zscore
from trait_architecture.standardized_ols import fit_ols_hc3
from trait_architecture.title_validated_dryad_manifest import probe_targets, read_targets


PROCESSED_SUFFIX = "Processed_Data.csv"
TREATMENTS = ("Robbing", "Florivory", "Pollination")


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


def _effect_code(value: object, field: str) -> float:
    label = _text(value).upper()
    if label == "N":
        return -0.5
    if label == "Y":
        return 0.5
    raise ValueError(f"{field} must be Y/N for effect coding")


def _phenology_field(config: dict[str, Any]) -> str:
    adjustment = config.get("phenology_adjustment")
    if not isinstance(adjustment, dict) or adjustment.get("transform") != "identity_then_zscore":
        raise ValueError("config must declare identity_then_zscore phenology adjustment")
    field = _text(adjustment.get("field"))
    if not field:
        raise ValueError("config phenology adjustment needs field")
    return field


def _prepare_records(rows: list[dict[str, str]], model: dict[str, Any], phenology_field: str) -> tuple[list[dict[str, float]], int]:
    records: list[dict[str, float]] = []
    omitted = 0
    outcome_field = _text(model.get("outcome_field"))
    transform_name = _text(model.get("outcome_transform"))
    for row in rows:
        try:
            outcome_raw = _number(row.get(outcome_field), outcome_field)
            outcome = transform(outcome_raw, "log1p_then_zscore" if transform_name == "log1p" else "identity_then_zscore")
            phenology = _number(row.get(phenology_field), phenology_field)
            treatment = {field: _effect_code(row.get(field), field) for field in TREATMENTS}
            records.append({"y": outcome, "Phenology": phenology, **treatment})
        except (TypeError, ValueError):
            omitted += 1
    return records, omitted


def _design(records: list[dict[str, float]]) -> tuple[list[float], list[list[float]], list[str]]:
    y = zscore([row["y"] for row in records])
    phenology = zscore([row["Phenology"] for row in records])
    terms = [
        "Intercept",
        "Robbing_c",
        "Florivory_c",
        "Pollination_c",
        "Robbing_c:Florivory_c",
        "Robbing_c:Pollination_c",
        "Florivory_c:Pollination_c",
        "Robbing_c:Florivory_c:Pollination_c",
        "Phenology_z",
    ]
    design: list[list[float]] = []
    for index, row in enumerate(records):
        robbing = row["Robbing"]
        florivory = row["Florivory"]
        pollination = row["Pollination"]
        design.append([
            1.0,
            robbing,
            florivory,
            pollination,
            robbing * florivory,
            robbing * pollination,
            florivory * pollination,
            robbing * florivory * pollination,
            phenology[index],
        ])
    return y, design, terms


def _summary(model: dict[str, Any], records: list[dict[str, float]], omitted: int) -> dict[str, Any]:
    y, design, terms = _design(records)
    result = fit_ols_hc3(y, design, terms)
    coefficients = [asdict(item) for item in result.coefficients]
    return {
        "analysis_id": model["analysis_id"],
        "outcome_field": model["outcome_field"],
        "outcome_transform": model["outcome_transform"],
        "outcome_definition": model["outcome_definition"],
        "interpretation": model["interpretation"],
        "treatment_coding": "effect-coded N=-0.5, Y=+0.5; full 2x2x2 factorial retained",
        "n_complete": result.n,
        "n_omitted": omitted,
        "r_squared": result.r_squared,
        "residual_df": result.residual_df,
        "coefficients": coefficients,
    }


def run(config_json: str | Path, targets_csv: str | Path, out_dir: str | Path) -> dict[str, object]:
    config = json.loads(Path(config_json).read_text(encoding="utf-8"))
    receipt, manifest = _receipt(read_targets(targets_csv))
    archive_url = f"{_version_url(receipt)}/download"
    archive = zipfile.ZipFile(BytesIO(_download_archive(archive_url, landing_page_url=receipt.landing_page_url)))
    rows = _processed(archive)
    phenology_field = _phenology_field(config)
    summaries: list[dict[str, Any]] = []
    for model in config["models"]:
        records, omitted = _prepare_records(rows, model, phenology_field)
        summaries.append(_summary(model, records, omitted))
    report = {
        "study_id": config["study_id"],
        "study_doi": config["study_doi"],
        "dataset_doi": config["dataset_doi"],
        "archive_url": archive_url,
        "manifest": manifest,
        "design": config["design"],
        "treatment_coding": config["treatment_coding"],
        "model_summaries": summaries,
        "guardrails": config["guardrails"],
        "warning": "Treatment coefficients are assignment contrasts in the randomized factorial experiment. They are not causal effects of early flower redness or floral tannins, and outcomes are reproductive components rather than total lifetime fitness.",
    }
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "impatiens_randomized_fitness_model_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "model_count": len(summaries),
        "complete_case_counts": {summary["analysis_id"]: summary["n_complete"] for summary in summaries},
    }
