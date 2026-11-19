"""Audit the original Pineau et al. 2024 XLSX Figure 2 worksheets.

No openpyxl/pandas/Excel recalculation. Uses Python's ZIP + XML primitives
to read cached cell values from the author's Git SHA-gated original XLSX.
The workbook is never committed to BITA; only aggregate receipts are retained.

Scientific units: separately started competition time series, nested within
the single PO-4 evolved Small/Large genotype pair, NOT independent evolution
origins, and NOT independent published research programmes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import statistics
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from collections import Counter

AUTHOR_COMMIT = "071affa79f16f0a469f099058372a7488c35c0c2"
XLSX_BLOB_SHA1 = "8f7d01b388489374aba210db96495f387d4338e2"
XLSX_SHA256 = "b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f"
WORKBOOK_ORIGINAL_BYTES = 1535384
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pkg": "http://schemas.openxmlformats.org/package/2006/relationships"}
RID = "{" + NS["r"] + "}id"
F2_NAMES = ("F2A", "F2C")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def verify_author_bytes(raw: bytes) -> dict:
    sha1 = git_blob_sha1(raw)
    sha256 = hashlib.sha256(raw).hexdigest()
    if sha1 != XLSX_BLOB_SHA1 or sha256 != XLSX_SHA256 or len(raw) != WORKBOOK_ORIGINAL_BYTES:
        raise ValueError("untrusted Pineau original author XLSX bytes")
    return {"author_commit": AUTHOR_COMMIT,
            "git_blob_sha1": sha1, "sha256": sha256, "source_bytes": len(raw)}


def col_index(addr: str) -> int:
    letters = re.match(r"^([A-Z]+)([0-9]+)$", addr.upper())
    if not letters:
        raise ValueError("invalid spreadsheet A1 address")
    n = 0
    for x in letters.group(1):
        n = n * 26 + ord(x) - ord("A") + 1
    return n - 1


def get_workbook_sheets(z: zipfile.ZipFile) -> dict[str, str]:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relation = {}
    for r in rels.findall("pkg:Relationship", NS):
        target = r.get("Target")
        if target:
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            relation[r.get("Id")] = target
    sheets = {}
    for el in wb.findall("m:sheets/m:sheet", NS):
        name = el.get("name")
        path = relation.get(el.get(RID))
        if not name or not path or path not in z.namelist():
            raise ValueError("cannot resolve original Excel worksheet")
        sheets[name] = path
    if not all(k in sheets for k in F2_NAMES):
        raise ValueError("original XLSX lacks author original Figure 2 worksheets")
    return sheets


def get_shared_strings(z: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in z.namelist():
        return []
    root = ET.fromstring(z.read(path))
    return ["".join(elem.itertext()) for elem in root.findall("m:si", NS)]


def read_cells(z: zipfile.ZipFile, path: str, shared: list[str]) -> list[dict]:
    tree = ET.fromstring(z.read(path))
    rows = []
    for row in tree.findall("m:sheetData/m:row", NS):
        out = {}
        formulas = 0
        for c in row.findall("m:c", NS):
            address = c.get("r")
            if address is None:
                raise ValueError("source cell missing address")
            idx = col_index(address)
            typ = c.get("t")
            v = c.find("m:v", NS)
            f = c.find("m:f", NS)
            if f is not None:
                formulas += 1
            if typ == "inlineStr":
                el = c.find("m:is", NS)
                value = "".join(el.itertext()) if el is not None else ""
            elif v is None:
                value = None
            elif typ == "s":
                value = shared[int(v.text)]
            elif typ in ("str", "e"):
                value = v.text
            elif typ == "b":
                value = bool(int(v.text))
            else:
                try:
                    value = float(v.text)
                    if not math.isfinite(value):
                        raise ValueError("non-finite source workbook number")
                except (TypeError, ValueError) as ex:
                    raise ValueError("unexpected original source numeric Excel cell") from ex
            if idx in out:
                raise ValueError("duplicate worksheet column cell")
            out[idx] = value
        if out:
            rows.append({"excel_row": int(row.get("r")), "cells": out, "formula_count": formulas})
    return rows


def numeric_matrix(rows: list[dict], sheet_name: str) -> dict:
    ncols = max((max(x["cells"]) for x in rows), default=-1) + 1
    if ncols == 0:
        raise ValueError("empty Figure 2 source worksheet")
    rawrows = [[row["cells"].get(j) for j in range(ncols)] for row in rows]
    metadata = []
    numeric = []
    for row, values in zip(rows, rawrows):
        numeric_values = [x for x in values if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if len(numeric_values) >= 2:
            numeric.append({"excel_row": row["excel_row"], "values": values})
        else:
            metadata.append({"excel_row": row["excel_row"], "cells": {
                str(i+1): str(x)[:60] for i, x in enumerate(values) if x is not None
            }})
    if len(numeric) < 4:
        raise ValueError("Figure 2 lacks enough observation timepoints")
    active = [j for j in range(ncols) if any(
        isinstance(row["values"][j], (int, float)) and not isinstance(row["values"][j], bool) for row in numeric)]
    counts = [sum(isinstance(row["values"][j], (int, float)) and not isinstance(row["values"][j], bool)
                  for row in numeric) for j in active]
    first = numeric[0]["values"]
    last = numeric[-1]["values"]
    summary = {
        "sheet": sheet_name,
        "all_nonempty_excel_rows": len(rows),
        "numeric_excel_row_numbers": [r["excel_row"] for r in numeric],
        "numeric_row_count": len(numeric),
        "active_column_count": len(active),
        "active_excel_columns_1indexed": [x+1 for x in active],
        "numeric_counts_per_active_column": counts,
        "header_or_nonnumeric_row_metadata": metadata[:4],
        "embedded_formula_cells": sum(x["formula_count"] for x in rows),
        "first_observed_values": [first[j] for j in active],
        "last_observed_values": [last[j] for j in active],
        "min_observed": min(float(v) for r in numeric for j in active
                            if isinstance((v := r["values"][j]), (int, float))),
        "max_observed": max(float(v) for r in numeric for j in active
                            if isinstance((v := r["values"][j]), (int, float))),
    }
    # Return full numeric row values only in process memory; freeze aggregates.
    return {"summary": summary, "rows": numeric, "active": active}


def fit_ols(x: list[float], y: list[float]) -> dict:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("minimum three paired competitions needed")
    xm = statistics.mean(x)
    ym = statistics.mean(y)
    ssx = sum((v-xm)**2 for v in x)
    if ssx <= 0:
        raise ValueError("no frequency starting spread")
    slope = sum((a-xm)*(b-ym) for a,b in zip(x,y)) / ssx
    intercept = ym-slope*xm
    yhat = [intercept+slope*a for a in x]
    sse = sum((v-u)**2 for v,u in zip(y,yhat))
    sst = sum((v-ym)**2 for v in y)
    r2 = 1-sse/sst if sst>0 else None
    return {"n_paired_trajectories":len(x), "slope":slope, "intercept":intercept,
            "r2":r2, "equilibrium_if_slope_nonzero":-intercept/slope if slope!=0 else None,
            "first_frequencies":x,"final_frequencies":[a+b for a,b in zip(x,y)],
            "mean_final_fraction":statistics.mean(a+b for a,b in zip(x,y))}


def f2_reanalysis(sheet: dict, expected_series: int) -> dict:
    rows = sheet["rows"]
    active = sheet["active"]
    first = rows[0]["values"]
    last = rows[-1]["values"]
    usable = [j for j in active if all(
        isinstance(row["values"][j], (int, float)) and not isinstance(row["values"][j], bool) for row in rows)]
    if len(usable) < 3:
        raise ValueError("too few fully observed competition trajectories")
    starts=[float(first[j]) for j in usable]
    ends=[float(last[j]) for j in usable]
    if any(not (0<=v<=1) for v in starts+ends):
        raise ValueError("competition proportion outside [0,1]")
    fit=fit_ols(starts,[end-start for start,end in zip(starts,ends)])
    return {"documented_author_script_series_count":expected_series,
            "original_sheet_active_series":len(active),
            "complete_trajectory_count":len(usable),
            "incomplete_active_excel_columns": [j+1 for j in active if j not in usable],
            "first_last_fit":fit}


def analyze_workbook(raw: bytes) -> dict:
    receipt = verify_author_bytes(raw)
    with zipfile.ZipFile(__import__("io").BytesIO(raw)) as z:
        sheets = get_workbook_sheets(z)
        strings = get_shared_strings(z)
        results = {key: numeric_matrix(read_cells(z,sheets[key],strings),key) for key in F2_NAMES}
        doc = {"source": receipt, "available_sheet_names":list(sheets),
               "sheet_count":len(sheets),
               "sheet_aggregate": {name:results[name]["summary"] for name in F2_NAMES},
               "standard_O2_reanalysis":f2_reanalysis(results["F2A"],8),
               "high_O2_reanalysis":f2_reanalysis(results["F2C"],7),
               "interpretation_limit": {
                   "workbook_verified_by_original_author_git_blob":True,
                   "worksheet_cells_parsed_without_modifying_workbook":True,
                   "competition_replicates_not_evolving_population_replicates":True,
                   "no_new_forward_diversification_origins_in_competition":True,
                   "published_highO2_n6_and_code_n7_are_not_silently_reconciled":True,
                   "original_raw_workbook_not_committed_to_bita":True
               }}
    return doc


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    d=analyze_workbook(a.input.read_bytes())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_PINEAU_F2_SOURCE_AUDIT:"+json.dumps(d,ensure_ascii=False,separators=(",",":")),flush=True)


if __name__=="__main__":
    main()
