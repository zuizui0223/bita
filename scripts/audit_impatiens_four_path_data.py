"""Audit the title-validated Impatiens Dryad archive for empirical model design.

The audit records only aggregate counts, missingness, variable ranges, discrete-scale
checks, treatment-level counts, and overlap cardinalities. It never exports
individual observations. It is a gate before effect estimation: field presence does
not establish trait function, temporal precedence, denominator adequacy, or a causal
path.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import zipfile
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any

from trait_architecture.dryad_archive_schema import _download_archive, _version_url
from trait_architecture.title_validated_dryad_manifest import probe_targets, read_targets


PROCESSED_FIELDS = (
    "Plot_Number",
    "Robbing",
    "Florivory",
    "Pollination",
    "Early_Season_Flower_Redness",
    "Early_Season_Condensed_Tannins",
    "Pollinators_Per_Hour",
    "Average_Percent_Florivory",
    "Average_CH_Fruits_Per_Day",
    "Average_Seeds_Per_CH_Fruit",
)
RAW_TABLE_SUFFIXES = {
    "visitors": "Raw_Floral_Visitors_Data.csv",
    "florivory": "Raw_Florivory_Data.csv",
    "flower_size": "Raw_Flower_Size_Data.csv",
    "tannin": "Raw_Condensed_Tannin_Data.csv",
    "seed": "Raw_Seed_Data.csv",
}
MISSING = {"", "na", "nan", "n/a", "null", "none"}


def _text(value: object) -> str:
    return str(value or "").strip()


def _missing(value: object) -> bool:
    return _text(value).lower() in MISSING


def _load_csv(archive: zipfile.ZipFile, suffix: str) -> list[dict[str, str]]:
    member = next((item for item in archive.infolist() if item.filename.endswith(suffix)), None)
    if member is None:
        raise ValueError(f"archive does not contain {suffix}")
    text = archive.read(member).decode("utf-8-sig", errors="replace")
    return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(io.StringIO(text))]


def _numeric_summary(rows: list[dict[str, str]], field: str) -> dict[str, object]:
    values: list[float] = []
    missing = 0
    non_numeric = 0
    for row in rows:
        value = row.get(field, "")
        if _missing(value):
            missing += 1
            continue
        try:
            number = float(value)
        except ValueError:
            non_numeric += 1
            continue
        if math.isfinite(number):
            values.append(number)
        else:
            non_numeric += 1
    integer_values = sum(abs(value - round(value)) <= 1e-9 for value in values)
    return {
        "non_missing_numeric": len(values),
        "missing": missing,
        "non_numeric_or_nonfinite": non_numeric,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "zero_count": sum(value == 0 for value in values),
        "positive_count": sum(value > 0 for value in values),
        "integer_valued_count": integer_values,
        "all_numeric_values_integer": bool(values) and integer_values == len(values),
    }


def _levels(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row.get(field, "") for row in rows if not _missing(row.get(field, ""))).items()))


def _plots(rows: list[dict[str, str]], field: str) -> set[str]:
    return {_text(row.get(field)) for row in rows if not _missing(row.get(field))}


def _archive_receipt(targets: list[dict[str, str]]):
    receipts, manifest_report = probe_targets(targets)
    for receipt in receipts:
        if receipt.manifest_status == "manifest_recovered" and _version_url(receipt):
            return receipt, manifest_report
    raise RuntimeError("no title-validated Dryad version archive was recovered")


def audit(targets_csv: str, out_dir: str) -> dict[str, Any]:
    targets = read_targets(targets_csv)
    receipt, manifest_report = _archive_receipt(targets)
    archive_url = f"{_version_url(receipt)}/download"
    archive_bytes = _download_archive(archive_url, landing_page_url=receipt.landing_page_url)
    archive = zipfile.ZipFile(BytesIO(archive_bytes))

    processed = _load_csv(archive, "Processed_Data.csv")
    visitors = _load_csv(archive, RAW_TABLE_SUFFIXES["visitors"])
    florivory = _load_csv(archive, RAW_TABLE_SUFFIXES["florivory"])
    raw_tables = {name: _load_csv(archive, suffix) for name, suffix in RAW_TABLE_SUFFIXES.items()}

    processed_plots = _plots(processed, "Plot_Number")
    complete_primary = sum(
        all(not _missing(row.get(field)) for field in PROCESSED_FIELDS)
        for row in processed
    )
    report: dict[str, Any] = {
        "study_id": receipt.study_id,
        "study_doi": receipt.study_doi,
        "dataset_doi": receipt.dataset_doi,
        "archive_url": archive_url,
        "manifest": manifest_report,
        "processed_table": {
            "row_count": len(processed),
            "unique_plant_ids": len(processed_plots),
            "all_primary_fields_complete_row_count": complete_primary,
            "treatment_levels": {field: _levels(processed, field) for field in ("Robbing", "Florivory", "Pollination")},
            "numeric_field_audit": {
                field: _numeric_summary(processed, field)
                for field in PROCESSED_FIELDS
                if field not in {"Plot_Number", "Robbing", "Florivory", "Pollination"}
            },
        },
        "raw_table_structure": {},
        "response_scale_notes": {
            "pollinator_rate": "Pollinators_Per_Hour is already a 60-minute-standardized rate; individual visitor Seconds must not be treated as a survey-effort offset without a documented observation-window definition.",
            "florivory_proportion": "Per_Florivory is percent tissue missing on an individual flower. Tot_Flwrs is the number of open CH flowers during a survey and is not a damaged-tissue trial denominator.",
            "seed_count": "Num_Seeds is a fruit-level count candidate. Fruit_type and repeated Plot rows must be screened before a clustered fruit-level model is specified.",
        },
        "warning": "This is a data-availability and response-scale audit. It does not decide trait function or causal status and does not fit an effect model.",
    }
    for name, rows in raw_tables.items():
        raw_plots = _plots(rows, "Plot")
        entry: dict[str, Any] = {
            "row_count": len(rows),
            "unique_plot_ids": len(raw_plots),
            "overlap_with_processed_plot_ids": len(processed_plots.intersection(raw_plots)),
            "columns": list(rows[0]) if rows else [],
        }
        if name == "visitors":
            entry["behavior_levels"] = _levels(rows, "Behavior")
            entry["seconds"] = _numeric_summary(rows, "Seconds")
            entry["visitor_number"] = _numeric_summary(rows, "Visitor_Num")
            entry["open_flower_count"] = _numeric_summary(rows, "Num_Flowers")
            entry["survey_date_levels"] = _levels(rows, "Date")
        if name == "florivory":
            entry["per_florivory"] = _numeric_summary(rows, "Per_Florivory")
            entry["total_open_ch_flowers"] = _numeric_summary(rows, "Tot_Flwrs")
            entry["survey_date_levels"] = _levels(rows, "Date")
        if name == "seed":
            entry["fruit_type_levels"] = _levels(rows, "Fruit_type")
            entry["num_seeds"] = _numeric_summary(rows, "Num_Seeds")
            entry["collection_date_levels"] = _levels(rows, "Date_coll")
        report["raw_table_structure"][name] = entry

    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "impatiens_four_path_preanalysis_audit.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return {
        "processed_rows": len(processed),
        "processed_unique_plants": len(processed_plots),
        "complete_primary_rows": complete_primary,
        "visitor_rows": len(visitors),
        "florivory_rows": len(florivory),
        "seed_rows": len(raw_tables["seed"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(audit(args.targets_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
