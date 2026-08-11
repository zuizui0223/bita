"""Reconstruct the predeclared Kessler et al. (2019) defensive-scent effect.

Reads the article-declared EDMOND Figure-1 workbook in memory and writes aggregate
2x2 tables, Fisher exact tests, log odds ratios, and within-study season summaries.
No observation-level data are retained.
"""

from __future__ import annotations

import io
import json
import math
import re
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

BASE = "https://edmond.mpg.de"
FILE_ID = 102481
SOURCE_DOI = "10.1111/1365-2435.13332"
DATASET_DOI = "10.17617/3.24"
FILE_NAME = "FIGURE 1. Diabrotica presence 2011. 2014. 2016.xlsx"
YEARS = ("2011", "2014", "2016")
USER_AGENT = "bita-kessler2019-defensive-scent-reconstruction/1.1"
MAX_FILE_BYTES = 5 * 1024 * 1024
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
SOURCE_P = {"2011": 0.035, "2014": 0.013, "2016": 0.098}
ALLOWED_LINES = {"EV", "CHAL"}


def _get(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream,*/*"})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public Dataverse file endpoint
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
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
    output: dict[str, str] = {}
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
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


def _normalise_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _row_values(row: ET.Element, shared: list[str]) -> dict[str, str]:
    return {_cell_col(cell): _cell_value(cell, shared) for cell in row.findall(f"{{{NS_MAIN}}}c")}


def _discover_unlabelled_line_col(rows: list[ET.Element], header_index: int, shared: list[str]) -> str:
    """Find an unlabeled genotype column whose non-empty values are exactly EV/CHAL.

    This is a structural fallback for the deposited 2014 sheet, whose genotype
    values occupy a column without a header. It does not inspect the outcome when
    deciding which predictor column to use.
    """
    by_column: dict[str, set[str]] = {}
    for row in rows[header_index + 1 :]:
        for col, raw in _row_values(row, shared).items():
            value = raw.strip().upper()
            if not value:
                continue
            by_column.setdefault(col, set()).add(value)
    candidates = [
        col for col, values in by_column.items()
        if values and values.issubset(ALLOWED_LINES) and values == ALLOWED_LINES
    ]
    if len(candidates) != 1:
        raise ValueError(f"unlabelled genotype column ambiguous or absent: candidates={candidates}")
    return candidates[0]


def _parse_sheet(book: zipfile.ZipFile, path: str, shared: list[str], year: str) -> list[dict[str, str]]:
    root = ET.fromstring(book.read(path))
    data = root.find(f"{{{NS_MAIN}}}sheetData")
    if data is None:
        raise ValueError(f"{year}: no sheetData")
    rows = data.findall(f"{{{NS_MAIN}}}row")
    header_map: dict[str, str] | None = None
    header_index = -1
    for index, row in enumerate(rows[:15]):
        by_col = _row_values(row, shared)
        normal = {col: _normalise_header(value) for col, value in by_col.items() if value}
        presence_cols = [col for col, value in normal.items() if value.startswith("presence")]
        # Presence is mandatory. The genotype header may legitimately be blank in 2014.
        if presence_cols:
            header_map = normal
            header_index = index
            break
    if header_map is None:
        raise ValueError(f"{year}: required presence header row not found")

    line_col = next((col for col, name in header_map.items() if name == "line"), None)
    if line_col is None:
        line_col = _discover_unlabelled_line_col(rows, header_index, shared)
    presence_col = next(col for col, name in header_map.items() if name.startswith("presence"))
    beetle_col = next((col for col, name in header_map.items() if name == "number_of_beetles"), None)
    plant_col = next((col for col, name in header_map.items() if name == "plant_number"), None)

    output: list[dict[str, str]] = []
    for row in rows[header_index + 1 :]:
        values = _row_values(row, shared)
        line = values.get(line_col, "").strip().upper()
        presence = values.get(presence_col, "").strip()
        if not line and not presence:
            continue
        output.append({
            "line": line,
            "presence": presence,
            "beetles": values.get(beetle_col, "").strip() if beetle_col else "",
            "plant": values.get(plant_col, "").strip() if plant_col else "",
        })
    return output


def _fisher_probability(a: int, row1: int, col1: int, total: int) -> float:
    return math.comb(col1, a) * math.comb(total - col1, row1 - a) / math.comb(total, row1)


def _fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    row1 = a + b
    col1 = a + c
    total = a + b + c + d
    observed = _fisher_probability(a, row1, col1, total)
    lower = max(0, row1 - (total - col1))
    upper = min(row1, col1)
    p = 0.0
    for candidate in range(lower, upper + 1):
        prob = _fisher_probability(candidate, row1, col1, total)
        if prob <= observed + 1e-12:
            p += prob
    return min(1.0, p)


def _log_or(a: int, b: int, c: int, d: int) -> tuple[float, float, str]:
    cells = [float(a), float(b), float(c), float(d)]
    correction = "none"
    if any(value == 0 for value in cells):
        cells = [value + 0.5 for value in cells]
        correction = "haldane_anscombe_0.5"
    aa, bb, cc, dd = cells
    estimate = math.log((aa * dd) / (bb * cc))
    se = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    return estimate, se, correction


def _year_summary(year: str, records: list[dict[str, str]]) -> dict[str, object]:
    counts = {"EV": {0: 0, 1: 0}, "CHAL": {0: 0, 1: 0}}
    seen_plants: dict[str, set[str]] = {"EV": set(), "CHAL": set()}
    beetle_presence_mismatch = 0
    for row in records:
        line = row["line"]
        if line not in counts:
            raise ValueError(f"{year}: unexpected line label {line!r}")
        try:
            presence_float = float(row["presence"])
        except ValueError as error:
            raise ValueError(f"{year}: invalid presence {row['presence']!r}") from error
        if presence_float not in (0.0, 1.0):
            raise ValueError(f"{year}: presence must be 0/1, got {presence_float}")
        presence = int(presence_float)
        counts[line][presence] += 1
        plant = row["plant"]
        if plant:
            if plant in seen_plants[line]:
                raise ValueError(f"{year}: duplicate plant {plant!r} in {line}")
            seen_plants[line].add(plant)
        if row["beetles"]:
            try:
                beetles = float(row["beetles"])
                if (beetles > 0) != bool(presence):
                    beetle_presence_mismatch += 1
            except ValueError:
                pass

    a, b = counts["EV"][1], counts["EV"][0]
    c, d = counts["CHAL"][1], counts["CHAL"][0]
    if min(a + b, c + d) == 0:
        raise ValueError(f"{year}: one genotype has no eligible observations")
    estimate, se, correction = _log_or(a, b, c, d)
    fisher = _fisher_two_sided(a, b, c, d)
    return {
        "year": year,
        "table": {"EV_infested": a, "EV_not_infested": b, "CHAL_infested": c, "CHAL_not_infested": d},
        "n_EV": a + b,
        "n_CHAL": c + d,
        "prop_EV": a / (a + b),
        "prop_CHAL": c / (c + d),
        "fisher_two_sided_p": fisher,
        "source_reported_fisher_p": SOURCE_P[year],
        "fisher_abs_difference_from_source": abs(fisher - SOURCE_P[year]),
        "effect_measure": "log_odds_ratio_EV_vs_CHAL_infestation",
        "log_odds_ratio": estimate,
        "standard_error": se,
        "ci95_lower": estimate - 1.96 * se,
        "ci95_upper": estimate + 1.96 * se,
        "continuity_correction": correction,
        "beetle_presence_mismatch_count": beetle_presence_mismatch,
    }


def _fixed_summary(years: list[dict[str, object]]) -> dict[str, float]:
    weights = [1.0 / float(item["standard_error"]) ** 2 for item in years]
    estimates = [float(item["log_odds_ratio"]) for item in years]
    total_weight = sum(weights)
    estimate = sum(w * e for w, e in zip(weights, estimates)) / total_weight
    se = math.sqrt(1.0 / total_weight)
    return {
        "log_odds_ratio": estimate,
        "standard_error": se,
        "ci95_lower": estimate - 1.96 * se,
        "ci95_upper": estimate + 1.96 * se,
    }


def run(output_path: str | Path) -> dict[str, object]:
    raw = _get(f"{BASE}/api/access/datafile/{FILE_ID}")
    book = zipfile.ZipFile(io.BytesIO(raw))
    shared = _shared_strings(book)
    targets = _sheet_targets(book)
    missing = [year for year in YEARS if year not in targets]
    if missing:
        raise ValueError(f"missing declared year sheets: {missing}")
    summaries = [_year_summary(year, _parse_sheet(book, targets[year], shared, year)) for year in YEARS]
    report = {
        "source_doi": SOURCE_DOI,
        "dataset_doi": DATASET_DOI,
        "file_id": FILE_ID,
        "file_name": FILE_NAME,
        "effect_orientation": "negative logOR = BA-emitting EV has lower infestation than BA-silenced CHAL",
        "year_summaries": summaries,
        "within_study_fixed_season_summary": _fixed_summary(summaries),
        "leave_2016_out_summary": _fixed_summary([item for item in summaries if item["year"] != "2016"]),
        "independence_boundary": "Three field seasons are repeated evidence within one Kessler-et-al.-2019 study cluster, not three literature studies.",
        "guardrail": "Only aggregate contingency counts and derived statistics are written; observation rows are never retained.",
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
    print(json.dumps({
        "year_count": len(report["year_summaries"]),
        "combined_log_or": report["within_study_fixed_season_summary"]["log_odds_ratio"],
    }, indent=2))
