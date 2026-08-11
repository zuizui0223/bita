"""Audit article-declared EDMOND data for Kessler et al. (2019).

EDMOND is a Dataverse deployment. The article declares persistent DOI
10.17617/3.24. This script retrieves dataset metadata through the public Dataverse
API and inspects bounded public tabular files in memory. It writes file/schema
summaries only; observation-level rows and non-header Excel values are never emitted.
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
USER_AGENT = "bita-kessler2019-edmond-audit/1.1"
MAX_FILE_BYTES = 50 * 1024 * 1024
TABULAR_SUFFIXES = {".csv", ".tsv", ".txt"}
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


def _audit_xlsx(file_id: int) -> list[dict[str, object]]:
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
        sheets.append({
            "sheet_name": sheet_name,
            "dimension": dimension_ref,
            "headers": headers,
            "candidate_columns": _candidate_columns(headers),
        })
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
        result["workbook_sheets"] = _audit_xlsx(file_id)
        result["schema_guardrail"] = "Only sheet names, dimensions, and first-row headers were read; no non-header Excel values were emitted."
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
            "Observation-level rows and non-header Excel values are never written.",
            "This audit does not fit biological models.",
            "A later effect reconstruction requires a predeclared source-aligned outcome and exact treatment/genotype sample counts.",
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
