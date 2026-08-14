"""Reconstruct the predeclared Barlow et al. (2017) Aconitum threshold window.

Reads the article-declared Figshare workbook in memory. Outputs aggregate field
regression diagnostics and laboratory dose-cell summaries only; raw rows are never
written to repository files or workflow artifacts.
"""

from __future__ import annotations

import io
import json
import math
import re
import statistics
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

FILE_URL = "https://ndownloader.figshare.com/files/8800921"
SOURCE_DOI = "10.1016/j.cub.2017.07.012"
DATA_DOI = "10.6084/m9.figshare.5165350"
USER_AGENT = "bita-barlow2017-threshold-window/1.0"
MAX_BYTES = 5 * 1024 * 1024
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
FIELD_SHEET = "bee visits nec alks"
DOSE_SHEET = "Figure S2"
FIELD_COLUMNS = {
    "A_lycoctonum": ("l_B.hort_nec", "l_nec_alk TOTAL"),
    "A_napellus": ("n_B.hort_nec", "n_nec_alk TOTAL"),
}
DOSE_COLUMNS = {
    "species": "species (1=Alycoctonum, 2=Anapellus)",
    "concentration": "conc (1=sucrose, 2=0.2ppm,3=2ppm, 4=20ppm, 5=200ppm, 6=2000ppm)",
    "volume": "volume (ul)",
    "duration": "durationprob (s)",
    "contacts": "numbercontacts",
    "first_bout": "firstboutdur (s)",
    "n_bouts": "no_bouts",
    "cum_bouts": "cum_bouts",
    "delta_suc": "deltasuc",
}
CONC_PPM = {1: 0.0, 2: 0.2, 3: 2.0, 4: 20.0, 5: 200.0, 6: 2000.0}
SPECIES = {1: "A_lycoctonum", 2: "A_napellus"}


def _get() -> bytes:
    req = Request(FILE_URL, headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream,*/*"})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public Figshare file route
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("source workbook exceeded bounded size")
    return data


def _shared_strings(book: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [
        "".join(node.text or "" for node in si.iter(f"{{{NS_MAIN}}}t"))
        for si in root.findall(f"{{{NS_MAIN}}}si")
    ]


def _sheet_targets(book: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in rels.findall(f"{{{NS_REL_PKG}}}Relationship")
    }
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    output: dict[str, str] = {}
    if sheets is None:
        return output
    for sheet in sheets.findall(f"{{{NS_MAIN}}}sheet"):
        target = rel_map.get(sheet.attrib.get(f"{{{NS_REL_DOC}}}id", ""), "")
        if not target:
            continue
        if target.startswith("/"):
            path = target.lstrip("/")
        else:
            target = re.sub(r"^\.\./", "", target)
            path = f"xl/{target}" if not target.startswith("xl/") else target
        output[sheet.attrib.get("name", "")] = path
    return output


def _cell_col(cell: ET.Element) -> str:
    match = re.match(r"([A-Z]+)", cell.attrib.get("r", ""))
    return match.group(1) if match else ""


def _cell_value(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{{{NS_MAIN}}}t")).strip()
    value = cell.find(f"{{{NS_MAIN}}}v")
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        try:
            return shared[int(value.text)].strip()
        except (ValueError, IndexError):
            return ""
    return value.text.strip()


def _rows(book: zipfile.ZipFile, path: str, shared: list[str]) -> list[dict[str, str]]:
    root = ET.fromstring(book.read(path))
    sheet_data = root.find(f"{{{NS_MAIN}}}sheetData")
    if sheet_data is None:
        return []
    return [
        {_cell_col(cell): _cell_value(cell, shared) for cell in row.findall(f"{{{NS_MAIN}}}c")}
        for row in sheet_data.findall(f"{{{NS_MAIN}}}row")
    ]


def _find_header(rows: list[dict[str, str]], required: set[str]) -> tuple[int, dict[str, str]]:
    for index, row in enumerate(rows[:15]):
        inverse = {value.strip(): col for col, value in row.items() if value.strip()}
        if required.issubset(inverse):
            return index, inverse
    raise ValueError(f"required header set not found: {sorted(required)}")


def _number(value: str) -> float:
    x = float(value.strip())
    if not math.isfinite(x):
        raise ValueError("non-finite numeric value")
    return x


def _simple_ols(x: list[float], y: list[float]) -> dict[str, float]:
    n = len(x)
    if n < 4 or n != len(y):
        raise ValueError("simple OLS requires paired n>=4")
    xbar, ybar = statistics.mean(x), statistics.mean(y)
    sxx = sum((v - xbar) ** 2 for v in x)
    syy = sum((v - ybar) ** 2 for v in y)
    sxy = sum((a - xbar) * (b - ybar) for a, b in zip(x, y))
    if sxx <= 0 or syy <= 0:
        raise ValueError("degenerate regression variance")
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    residuals = [b - (intercept + slope * a) for a, b in zip(x, y)]
    sse = sum(r * r for r in residuals)
    df = n - 2
    mse = sse / df
    se = math.sqrt(mse / sxx)
    r = sxy / math.sqrt(sxx * syy)
    r2 = r * r
    adj_r2 = 1 - (1 - r2) * (n - 1) / df
    f_stat = (r2 / (1 - r2)) * df if r2 < 1 else math.inf
    z = math.atanh(max(-0.999999999, min(0.999999999, r)))
    z_se = 1 / math.sqrt(n - 3)
    return {
        "n": n,
        "intercept": intercept,
        "slope": slope,
        "slope_se": se,
        "slope_ci95_lower": slope - 1.96 * se,
        "slope_ci95_upper": slope + 1.96 * se,
        "pearson_r": r,
        "r_squared": r2,
        "adjusted_r_squared": adj_r2,
        "f_statistic": f_stat,
        "fisher_z": z,
        "fisher_z_se": z_se,
        "fisher_z_ci95_lower": z - 1.96 * z_se,
        "fisher_z_ci95_upper": z + 1.96 * z_se,
    }


def _field_models(book: zipfile.ZipFile, targets: dict[str, str], shared: list[str]) -> dict[str, object]:
    rows = _rows(book, targets[FIELD_SHEET], shared)
    required = {item for pair in FIELD_COLUMNS.values() for item in pair}
    header_index, header = _find_header(rows, required)
    output: dict[str, object] = {}
    for species, (response_name, predictor_name) in FIELD_COLUMNS.items():
        response_col, predictor_col = header[response_name], header[predictor_name]
        x: list[float] = []
        y: list[float] = []
        nonpositive = 0
        for row in rows[header_index + 1 :]:
            if not row.get(response_col, "").strip() or not row.get(predictor_col, "").strip():
                continue
            response, predictor = _number(row[response_col]), _number(row[predictor_col])
            if response <= 0 or predictor <= 0:
                nonpositive += 1
                continue
            x.append(math.log(predictor))
            y.append(math.log(response))
        if nonpositive:
            raise ValueError(f"{species}: {nonpositive} complete pairs have non-positive values; source log scale cannot be reproduced without changing the preregistered transform")
        model = _simple_ols(x, y)
        model.update({
            "response": response_name,
            "predictor": predictor_name,
            "transform": "natural_log_both_variables",
            "effect_orientation": "negative = higher nectar alkaloid concentration associated with lower pollinator visitation",
        })
        output[species] = model
    lyco = output["A_lycoctonum"]
    output["source_integrity_check"] = {
        "source_n": 12,
        "source_adjusted_r_squared": 0.27,
        "source_f_statistic": 5.8,
        "reconstructed_n": lyco["n"],
        "abs_f_difference": abs(float(lyco["f_statistic"]) - 5.8),
        "abs_adjusted_r2_difference": abs(float(lyco["adjusted_r_squared"]) - 0.27),
    }
    return output


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "mean": None, "sd": None, "se": None, "median": None, "q1": None, "q3": None}
    ordered = sorted(values)
    n = len(values)
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if n > 1 else 0.0
    def quantile(p: float) -> float:
        if n == 1:
            return ordered[0]
        h = (n - 1) * p
        lo, hi = math.floor(h), math.ceil(h)
        if lo == hi:
            return ordered[lo]
        return ordered[lo] * (hi - h) + ordered[hi] * (h - lo)
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "se": sd / math.sqrt(n) if n else None,
        "median": statistics.median(ordered),
        "q1": quantile(0.25),
        "q3": quantile(0.75),
    }


def _dose_summaries(book: zipfile.ZipFile, targets: dict[str, str], shared: list[str]) -> dict[str, object]:
    rows = _rows(book, targets[DOSE_SHEET], shared)
    required = set(DOSE_COLUMNS.values())
    header_index, header = _find_header(rows, required)
    fields = {key: header[value] for key, value in DOSE_COLUMNS.items()}
    cells: dict[tuple[int, int], dict[str, list[float]]] = {}
    skipped = 0
    for row in rows[header_index + 1 :]:
        try:
            species_code = int(round(_number(row.get(fields["species"], ""))))
            conc_code = int(round(_number(row.get(fields["concentration"], ""))))
        except (ValueError, TypeError):
            if any(str(value).strip() for value in row.values()):
                skipped += 1
            continue
        if species_code not in SPECIES or conc_code not in CONC_PPM:
            raise ValueError(f"unexpected species/concentration code: {species_code}/{conc_code}")
        bucket = cells.setdefault((species_code, conc_code), {key: [] for key in ("volume", "duration", "contacts", "first_bout", "n_bouts", "cum_bouts", "delta_suc")})
        for field in bucket:
            raw = row.get(fields[field], "").strip()
            if raw:
                bucket[field].append(_number(raw))
    output: list[dict[str, object]] = []
    for species_code in sorted(SPECIES):
        for conc_code in sorted(CONC_PPM):
            bucket = cells.get((species_code, conc_code), {key: [] for key in ("volume", "duration", "contacts", "first_bout", "n_bouts", "cum_bouts", "delta_suc")})
            output.append({
                "species": SPECIES[species_code],
                "concentration_code": conc_code,
                "concentration_ppm": CONC_PPM[conc_code],
                "volume_ul": _summary(bucket["volume"]),
                "duration_proboscis_s": _summary(bucket["duration"]),
                "number_contacts": _summary(bucket["contacts"]),
                "first_bout_duration_s": _summary(bucket["first_bout"]),
                "number_bouts": _summary(bucket["n_bouts"]),
                "cumulative_bouts": _summary(bucket["cum_bouts"]),
                "delta_suc": _summary(bucket["delta_suc"]),
            })
    return {
        "dose_cells": output,
        "skipped_nondata_rows": skipped,
        "threshold_landmarks_ppm": {
            "source_first_reported_robber_deterrence": 20.0,
            "source_pollinator_decline_region_lower": 200.0,
            "source_pollinator_extrapolated_cessation": 380.0,
        },
        "effect_boundary": "Dose-cell summaries remain within one Barlow-et-al.-2017 study; field pollinator and laboratory robber endpoints are not pooled.",
    }


def run(output_path: str | Path) -> dict[str, object]:
    raw = _get()
    book = zipfile.ZipFile(io.BytesIO(raw))
    shared = _shared_strings(book)
    targets = _sheet_targets(book)
    for required in (FIELD_SHEET, DOSE_SHEET):
        if required not in targets:
            raise ValueError(f"required worksheet missing: {required}")
    report = {
        "source_doi": SOURCE_DOI,
        "data_doi": DATA_DOI,
        "field_D_to_pollination": _field_models(book, targets, shared),
        "laboratory_D_to_antagonism": _dose_summaries(book, targets, shared),
        "mechanism_pattern": "robber deterrence begins at much lower source-reported alkaloid concentration than pronounced field pollinator interference",
        "guardrail": "Only aggregate coefficients and dose-cell summaries are written; observation-level workbook rows remain in memory.",
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    report = run(args.output)
    lyco = report["field_D_to_pollination"]["A_lycoctonum"]
    print(json.dumps({
        "field_n": lyco["n"],
        "field_r": lyco["pearson_r"],
        "dose_cell_count": len(report["laboratory_D_to_antagonism"]["dose_cells"]),
    }, indent=2))
