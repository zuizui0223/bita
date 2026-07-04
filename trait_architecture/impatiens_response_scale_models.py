"""Fit predeclared response-scale models for the *Impatiens capensis* panel.

Raw Dryad observations are downloaded and used only in memory. Outputs contain
aggregate diagnostics and coefficients. The module separates three response units:
individual-plant pollinator rate, individual-flower natural florivory fraction, and
individual-CH-fruit seed count. Trait coefficients remain observational; clustered
sandwich inference handles repeated flowers/fruits within plant.
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
from statistics import mean, stdev
from typing import Any

from trait_architecture.dryad_archive_schema import _download_archive, _version_url
from trait_architecture.impatiens_models import MISSING, _number, yn
from trait_architecture.quasi_glm import fit_quasi_glm
from trait_architecture.title_validated_dryad_manifest import probe_targets, read_targets


TABLE_SUFFIXES = {
    "Processed_Data.csv": "Processed_Data.csv",
    "Raw_Florivory_Data.csv": "Raw_Florivory_Data.csv",
    "Raw_Seed_Data.csv": "Raw_Seed_Data.csv",
}


def _text(value: object) -> str:
    return str(value or "").strip()


def _is_missing(value: object) -> bool:
    return _text(value).lower() in MISSING


def _load_csv(archive: zipfile.ZipFile, suffix: str) -> list[dict[str, str]]:
    member = next((item for item in archive.infolist() if item.filename.endswith(suffix)), None)
    if member is None:
        raise ValueError(f"archive does not contain {suffix}")
    text = archive.read(member).decode("utf-8-sig", errors="replace")
    return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(io.StringIO(text))]


def _receipt(targets: list[dict[str, str]]):
    receipts, manifest = probe_targets(targets)
    for receipt in receipts:
        if receipt.manifest_status == "manifest_recovered" and _version_url(receipt):
            return receipt, manifest
    raise RuntimeError("no title-validated Dryad archive available")


def _zscore(values: list[float]) -> list[float]:
    if len(values) < 2:
        raise ValueError("standardization requires at least two rows")
    location, spread = mean(values), stdev(values)
    if spread <= 0:
        raise ValueError("standardization requires non-constant values")
    return [(value - location) / spread for value in values]


def _traits(processed: dict[str, str], config: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    modules = config["trait_predictors"]
    a = _number(processed.get(modules["A_flower"]["field"]), modules["A_flower"]["field"])
    tannin = _number(processed.get(modules["D_candidate"]["field"]), modules["D_candidate"]["field"])
    if tannin < 0:
        raise ValueError("condensed tannins must be non-negative for log1p transform")
    b = math.log1p(tannin)
    phenology = _number(processed.get(modules["phenology"]["field"]), modules["phenology"]["field"])
    return (
        a,
        b,
        yn(processed.get("Robbing"), "Robbing"),
        yn(processed.get("Florivory"), "Florivory"),
        yn(processed.get("Pollination"), "Pollination"),
        phenology,
    )


def _standardized_design(records: list[dict[str, Any]], *, interaction: bool) -> tuple[list[list[float]], list[str]]:
    a_values = _zscore([float(row["A"]) for row in records])
    b_values = _zscore([float(row["B"]) for row in records])
    phenology_values = _zscore([float(row["Phenology"]) for row in records])
    terms = ["Intercept", "A_z", "D_z"]
    if interaction:
        terms.append("A_z:D_z")
    terms += ["Robbing_Y", "Florivory_Y", "Pollination_Y", "Phenology_z"]
    design: list[list[float]] = []
    for index, row in enumerate(records):
        values = [1.0, a_values[index], b_values[index]]
        if interaction:
            values.append(a_values[index] * b_values[index])
        values += [
            float(row["Robbing_Y"]),
            float(row["Florivory_Y"]),
            float(row["Pollination_Y"]),
            phenology_values[index],
        ]
        design.append(values)
    return design, terms


def _processed_by_plot(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        plot = _text(row.get("Plot_Number"))
        if not plot:
            continue
        if plot in indexed:
            raise ValueError(f"Processed_Data.csv has duplicate Plot_Number {plot}")
        indexed[plot] = row
    return indexed


def _processed_rate_records(rows: list[dict[str, str]], config: dict[str, Any], outcome_field: str) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    omitted = 0
    for row in rows:
        try:
            outcome = _number(row.get(outcome_field), outcome_field)
            if outcome < 0:
                raise ValueError("pollinator rate cannot be negative")
            a, b, robbing, florivory, pollination, phenology = _traits(row, config)
            records.append({
                "y": outcome,
                "A": a,
                "B": b,
                "Robbing_Y": robbing,
                "Florivory_Y": florivory,
                "Pollination_Y": pollination,
                "Phenology": phenology,
                "cluster": _text(row.get("Plot_Number")),
            })
        except (TypeError, ValueError):
            omitted += 1
    return records, omitted


def _raw_records(
    raw_rows: list[dict[str, str]],
    processed_by_plot: dict[str, dict[str, str]],
    config: dict[str, Any],
    model: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    omitted = 0
    filter_field = _text(model.get("filter_field"))
    filter_value = _text(model.get("filter_value"))
    for row in raw_rows:
        if filter_field and _text(row.get(filter_field)) != filter_value:
            continue
        try:
            cluster = _text(row.get("Plot"))
            processed = processed_by_plot.get(cluster)
            if processed is None:
                raise ValueError("raw Plot does not link to processed Plot_Number")
            outcome = _number(row.get(model["outcome_field"]), model["outcome_field"])
            if model.get("outcome_scale") == "percent_to_fraction":
                if not 0 <= outcome <= 100:
                    raise ValueError("florivory percentage must lie in [0,100]")
                outcome /= 100.0
            elif outcome < 0:
                raise ValueError("count response cannot be negative")
            a, b, robbing, florivory, pollination, phenology = _traits(processed, config)
            records.append({
                "y": outcome,
                "A": a,
                "B": b,
                "Robbing_Y": robbing,
                "Florivory_Y": florivory,
                "Pollination_Y": pollination,
                "Phenology": phenology,
                "cluster": cluster,
            })
        except (TypeError, ValueError):
            omitted += 1
    return records, omitted


def _serialize_model(
    model: dict[str, Any],
    records: list[dict[str, Any]],
    omitted: int,
) -> dict[str, Any]:
    design, terms = _standardized_design(records, interaction=bool(model.get("interaction")))
    response = [float(row["y"]) for row in records]
    cluster_field = model.get("cluster_field")
    clusters = [str(row["cluster"]) for row in records] if cluster_field else None
    result = fit_quasi_glm(response, design, terms, family=model["family"], clusters=clusters)
    return {
        "analysis_id": model["analysis_id"],
        "family": model["family"],
        "source_table": model["source_table"],
        "outcome_field": model["outcome_field"],
        "response_contract": model["response_contract"],
        "inference_contract": model["inference_contract"],
        "interaction": bool(model.get("interaction")),
        "n_response_records": result.n,
        "n_omitted": omitted,
        "cluster_count": result.cluster_count,
        "mean_response": result.mean_response,
        "pearson_dispersion": result.pearson_dispersion,
        "iterations": result.iterations,
        "converged": result.converged,
        "coefficients": [asdict(item) for item in result.coefficients],
    }


def run(config_json: str | Path, targets_csv: str | Path, out_dir: str | Path) -> dict[str, object]:
    config = json.loads(Path(config_json).read_text(encoding="utf-8"))
    receipt, manifest = _receipt(read_targets(targets_csv))
    archive_url = f"{_version_url(receipt)}/download"
    archive = zipfile.ZipFile(BytesIO(_download_archive(archive_url, landing_page_url=receipt.landing_page_url)))
    processed = _load_csv(archive, TABLE_SUFFIXES["Processed_Data.csv"])
    processed_by_plot = _processed_by_plot(processed)
    summaries: list[dict[str, Any]] = []
    for model in config["models"]:
        source = _text(model["source_table"])
        if source == "Processed_Data.csv":
            records, omitted = _processed_rate_records(processed, config, model["outcome_field"])
        else:
            raw_rows = _load_csv(archive, TABLE_SUFFIXES[source])
            records, omitted = _raw_records(raw_rows, processed_by_plot, config, model)
        if len(records) <= 8:
            raise RuntimeError(f"{model['analysis_id']}: too few complete records ({len(records)})")
        summaries.append(_serialize_model(model, records, omitted))
    report = {
        "study_id": config["study_id"],
        "study_doi": config["study_doi"],
        "dataset_doi": config["dataset_doi"],
        "archive_url": archive_url,
        "manifest": manifest,
        "unit_contract": config["unit_contract"],
        "model_summaries": summaries,
        "guardrails": config["guardrails"],
        "warning": "Response-scale models are predeclared observational analyses. Raw rows are used only in memory and are not written to outputs.",
    }
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "impatiens_response_scale_model_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "model_count": len(summaries),
        "model_record_counts": {summary["analysis_id"]: summary["n_response_records"] for summary in summaries},
    }
