"""Exact 2025 HUSCAP Peucedanum source schema & aggregation diagnostic.

This is an observational source-inspection receipt ONLY, not a causal or
evolutionary specialization test. Uses source ZIP checksum and never writes
raw individual-level data to the output artifact.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from scripts.audit_bita_peucedanum2025_huscap import fetch

EXPECTED_ZIP_SHA256 = "07d9f718d58b795553d50c2cb2b33e9a7dd3df9e34b5c1757ed55d5674c777ca"
INPUTS = {
    "population": {
        "path": "All_Plots_Data.csv",
        "fields": (
            "Year", "Plot", "ID", "HflowerN", "MflowerN", "InitialFruitN",
            "Height", "OvipN", "FinalFruitN", "PredationR",
        ),
    },
    "paternity": {
        "path": "HA_Plot_Data.csv",
        "fields": (
            "ID", "HFlowerNo", "MFlowerNo", "Height", "TotalMFlowerNo",
            "TotalFlowerNo", "InitialFruitNo", "EstFinalFruitNo",
            "DamagedFruitNo", "SiredSeedNo",
        ),
    },
}
NULL = {"", "NA", "N/A", "NaN", "nan", "-", "null"}


def checked_csvs(blob: bytes) -> dict[str, list[dict]]:
    if hashlib.sha256(blob).hexdigest() != EXPECTED_ZIP_SHA256:
        raise ValueError("2025_HUSCAP_ARCHIVE_SHA256_DRIFT")
    out = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for name, spec in INPUTS.items():
            info = [x for x in z.namelist() if x == spec["path"]]
            if len(info) != 1:
                raise ValueError("MISSING_OR_DUPLICATED_PRIMARY_TABLE:" + spec["path"])
            raw = z.read(info[0])
            text = raw.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            if tuple(reader.fieldnames or ()) != spec["fields"]:
                raise ValueError("SOURCE_PRIMARY_COLUMN_DRIFT:" + name)
            rows = list(reader)
            if not rows:
                raise ValueError("EMPTY_SOURCE:" + name)
            out[name] = rows
    return out


def number(value: str) -> float | None:
    value = (value or "").strip()
    if value in NULL:
        return None
    try:
        result = float(value)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def describe(values: list[float | None]) -> dict:
    a = sorted(x for x in values if x is not None)
    if not a:
        return {"observed": 0, "missing": len(values)}
    return {
        "observed": len(a), "missing": len(values)-len(a),
        "min": a[0], "median": statistics.median(a),
        "mean": statistics.fmean(a), "max": a[-1],
    }


def group_means(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["Year"], row["Plot"])].append(row)
    out = []
    for (year, plot), rr in sorted(groups.items()):
        sex = []
        for r in rr:
            h, m = number(r["HflowerN"]), number(r["MflowerN"])
            if h is not None and m is not None and h+m > 0:
                sex.append(m/(m+h))
        out.append({
            "year": year, "plot": plot, "n_plants": len(rr),
            "n_male_fraction": len(sex),
            "male_fraction_mean": statistics.fmean(sex) if sex else None,
            "mean_oviposition": describe([number(r["OvipN"]) for r in rr])["mean"]
                if any(number(r["OvipN"]) is not None for r in rr) else None,
            "mean_predation": describe([number(r["PredationR"]) for r in rr])["mean"]
                if any(number(r["PredationR"]) is not None for r in rr) else None,
        })
    return out


def inspect(blob: bytes) -> dict:
    data = checked_csvs(blob)
    population, pat = data["population"], data["paternity"]
    numeric = {}
    for name, rows in data.items():
        numeric[name] = {}
        for field in INPUTS[name]["fields"]:
            if field in ("Year","Plot","ID"):
                continue
            numeric[name][field] = describe([number(r[field]) for r in rows])
    groups = group_means(population)
    return {
        "receipt_schema": "BITA_PEUCEDANUM2025_EXACT_RAW_TABLE_INSPECTION_V1",
        "data_level": "ORIGINAL_PUBLIC_RAW_ROWS_AGGREGATED_FOR_DIAGNOSIS",
        "doi": "10.14943/hu95572",
        "zip_sha256": EXPECTED_ZIP_SHA256,
        "raw_rows_redistributed": False,
        "statistical_hypothesis_test_run": False,
        "n_population_rows": len(population),
        "n_paternity_rows": len(pat),
        "population_year_counts": dict(sorted(Counter(x["Year"] for x in population).items())),
        "population_plot_counts": dict(sorted(Counter(x["Plot"] for x in population).items())),
        "paternity_id_unique": len({x["ID"] for x in pat}) == len(pat),
        "year_plot_aggregates": groups,
        "numeric_fields": numeric,
        "warning": (
            "PredationR is an outcome/exposure proxy potentially confounded "
            "by year, plot, phenology and host selection; not a randomized "
            "trade-off or direct empirical BITA architecture gain. Source "
            "annotations and original script require interpretation."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("artifacts/bita_peucedanum2025_raw_diagnostic.json"))
    args = ap.parse_args()
    result = inspect(fetch())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
