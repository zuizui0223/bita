"""Audit article-declared EDMOND data for Kessler et al. (2019).

EDMOND is a Dataverse deployment. The article declares persistent DOI
10.17617/3.24. This script retrieves dataset metadata through the public Dataverse
API and inspects bounded public tabular files in memory. It writes file/schema
summaries only; observation-level rows are never emitted. For Figure 1 only, it
also reports bounded structural profiles of unlabeled columns to resolve a source-
data counting discrepancy without exposing plant identifiers or outcome rows.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

BASE = "https://edmond.mpg.de"
PERSISTENT_ID = "doi:10.17617/3.24"
SOURCE_DOI = "10.1111/1365-2435.13332"
USER_AGENT = "bita-kessler2019-edmond-audit/1.2"
MAX_FILE_BYTES = 50 * 1024 * 1024
TABULAR_SUFFIXES = {".csv", ".tsv", ".txt"}
FIGURE1_NAME = "FIGURE 1. Diabrotica presence 2011. 2014. 2016.xlsx"
TOKENS = (
    "year", "genotype", "chal", "ev", "plant", "flower", "damage", "beetle", "diabrotica",
    "infest", "choice", "feeding", "time", "ba", "benzyl", "eag", "dose", "concentration",
)
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _get(url: str, *, accept: str = "application/json,*/*") -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public repository/API endpoints
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_FILE_BYTES:
            raise ValueError(f"response too large for bounded audit: {length}")
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("response exceeded configured byte limit")
    return data


def _json(url: str):
    return json.loads(_get(url).decode("utf-8"))


def _suffix(name: str) -> str:
    return Path(name).suffix.lower()


def _candidate_columns(headers: list[str]) -> list[str]:
    return [h for h in headers if any(token in h.lower() for token in TOKENS)]


def _dataset() -> dict:
    encoded = quote(PERSISTENT_ID, safe="")
    url = f"{BASE}/api/datasets/:persistentId/?persistentId={encoded}"
    payload = _json(url)
    if payload.get("status") != "OK" or not isinstance(payload.get("data"), dict):
        raise RuntimeError(f"EDMOND dataset API failed: {payload.get('status')}")
    return payload["data"]


def _files(dataset: dict) -> list[dict]:
    version = dataset.get("latestVersion")
    if not isinstance(version, dict):
        raise RuntimeError("EDMOND dataset has no latestVersion object")
    files = version.get("files")
    if not isinstance(files, list):
        raise RuntimeError("EDMOND latestVersion has no files list")
    return [item for item in files if isinstance(item, dict)]


def _shared_strings(book: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [
        "".join(node.text or "" for node in si.iter(f"{{{NS_MAIN}}}t"))
        for si in root.findall(f"{{{NS_MAIN}}}si")
    ]


def _cell_text(cell: ET.Element, shared: list[str]) -> str:
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


def _cell_col(cell: ET.Element) -> str:
    match = re.match(r"([A-Z]+)", cell.attrib.get("r", ""))
    return match.group(1) if match else ""


def _sheet_targets(book: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in rels.findall(f"{{{NS_REL_PKG}}}Relationship")
    }
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    output: list[tuple[str, str]] = []
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
        output.append((sheet.attrib.get("name", ""), path))
    return output


def _figure1_structural_profile(sheet_data: ET.Element | None, shared: list[str]) -> dict[str, object]:
    """Summarize column structure without emitting row-level combinations.

    Plant identifiers and numeric outcome values are deliberately excluded. String
    labels such as EV/CHAL or textual notes may be reported as bounded distinct sets.
    """
    if sheet_data is None:
        return {}
    rows = sheet_data.findall(f"{{{NS_MAIN}}}row")
    if not rows:
        return {}
    header_cells = {
        _cell_col(cell): _cell_text(cell, shared)
        for cell in rows[0].findall(f"{{{NS_MAIN}}}c")
    }
    profiles: dict[str, dict[str, object]] = {}
    for row in rows[1:]:
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            col = _cell_col(cell)
            value = _cell_text(cell, shared).strip()
            if not value:
                continue
            profile = profiles.setdefault(col, {"nonempty": 0, "numeric": 0, "distinct_text": set()})
            profile["nonempty"] = int(profile["nonempty"]) + 1
            try:
                float(value)
                profile["numeric"] = int(profile["numeric"]) + 1
            except ValueError:
                distinct = profile["distinct_text"]
                if isinstance(distinct, set) and len(distinct) < 20:
                    # Do not emit likely plant identifiers: only retain biologically/structurally named labels.
                    upper = value.upper()
                    if upper in {"EV", "CHAL"} or any(token in value.lower() for token in ("exclude", "omit", "dead", "missing", "note", "control", "treat")):
                        distinct.add(value)
    output: dict[str, object] = {}
    for col, profile in profiles.items():
        distinct = profile.pop("distinct_text")
        output[col] = {
            "header": header_cells.get(col, ""),
            "nonempty_count": profile["nonempty"],
            "numeric_count": profile["numeric"],
            "bounded_structural_text": sorted(distinct) if isinstance(distinct, set) else [],
        }
    return output


def _audit_xlsx(file_id: int, file_name: str) -> list[dict[str, object]]:
    raw = _get(
        f"{BASE}/api/access/datafile/{file_id}",
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
    )
    book = zipfile.ZipFile(io.BytesIO(raw))
    shared = _shared_strings(book)
    sheets: list[dict[str, object]] = []
    for sheet_name, path in _sheet_targets(book):
        root = ET.fromstring(book.read(path))
        dimension = root.find(f"{{{NS_MAIN}}}dimension")
        dimension_ref = dimension.attrib.get("ref", "") if dimension is not None else ""
        sheet_data = root.find(f"{{{NS_MAIN}}}sheetData")
        first_row = None if sheet_data is None else sheet_data.find(f"{{{NS_MAIN}}}row")
        headers: list[str] = []
        if first_row is not None:
            headers = [_cell_text(cell, shared) for cell in first_row.findall(f"{{{NS_MAIN}}}c")]
        record: dict[str, object] = {
            "sheet_name": sheet_name,
            "dimension": dimension_ref,
            "headers": headers,
            "candidate_columns": _candidate_columns(headers),
        }
        if file_name == FIGURE1_NAME:
            record["structural_column_profile"] = _figure1_structural_profile(sheet_data, shared)
        sheets.append(record)
    return sheets


def _audit_text(file_id: int) -> dict[str, object]:
    raw = _get(f"{BASE}/api/access/datafile/{file_id}", accept="text/csv,text/plain,*/*")
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        delimiter = "\t" if sample.count("\t") > sample.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    return {
        "n_rows": sum(1 for _ in reader),
        "delimiter": "tab" if delimiter == "\t" else delimiter,
        "headers": headers,
        "candidate_columns": _candidate_columns(headers),
    }


def _file_record(item: dict) -> dict[str, object]:
    data_file = item.get("dataFile") if isinstance(item.get("dataFile"), dict) else {}
    file_id = data_file.get("id")
    name = str(data_file.get("filename") or "")
    content_type = str(data_file.get("contentType") or "")
    suffix = _suffix(name)
    result: dict[str, object] = {
        "file_id": file_id,
        "file_name": name,
        "content_type": content_type,
        "size_bytes": data_file.get("filesize"),
        "restricted": bool(data_file.get("restricted", False)),
        "description": item.get("description"),
        "categories": item.get("categories") if isinstance(item.get("categories"), list) else [],
        "suffix": suffix,
    }
    if not isinstance(file_id, int) or result["restricted"]:
        return result
    if suffix == ".xlsx":
        result["workbook_sheets"] = _audit_xlsx(file_id, name)
        result["schema_guardrail"] = "Sheet/header structure plus bounded structural labels only; no observation rows, plant identifiers, or numeric outcome values are emitted."
    elif suffix in TABULAR_SUFFIXES:
        result.update(_audit_text(file_id))
    return result


def run(output_path: str | Path) -> dict[str, object]:
    dataset = _dataset()
    version = dataset.get("latestVersion") if isinstance(dataset.get("latestVersion"), dict) else {}
    files = _files(dataset)
    report = {
        "source_doi": SOURCE_DOI,
        "dataset_persistent_id": PERSISTENT_ID,
        "dataset_id": dataset.get("id"),
        "dataset_title": version.get("metadataBlocks", {}).get("citation", {}).get("fields", []) if isinstance(version, dict) else None,
        "version_number": f"{version.get('versionNumber')}.{version.get('versionMinorNumber')}" if isinstance(version, dict) else None,
        "file_count": len(files),
        "files": [_file_record(item) for item in files],
        "guardrails": [
            "Observation-level rows, plant identifiers, and numeric non-header Excel values are never written.",
            "Figure-1 structural labels are audited only to adjudicate source/data counting discrepancies.",
            "This audit does not fit biological models.",
        ],
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
    result = run(args.output)
    print(json.dumps({"dataset_id": result["dataset_id"], "file_count": result["file_count"]}, indent=2))
