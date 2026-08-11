"""Audit the public Figshare data declared by Barlow et al. (2017).

The accepted manuscript explicitly declares Figshare DOI/identifier 5165350 for
biological assay, nectar/galea alkaloid, and bumblebee-alkaloid bioassay data.
This script enumerates the public Figshare article and emits bounded file/schema
metadata only. Observation-level rows and non-header cell values are never written
to the artifact.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

FIGSHARE_API = "https://api.figshare.com/v2"
ARTICLE_ID = 5165350
SOURCE_DOI = "10.1016/j.cub.2017.07.012"
DATA_DOI = "10.6084/m9.figshare.5165350"
USER_AGENT = "bita-barlow2017-figshare-audit/1.1"
MAX_FILE_BYTES = 50 * 1024 * 1024
TEXT_SUFFIXES = {".csv", ".tsv", ".txt"}
TOKENS = (
    "bee", "bombus", "species", "alkaloid", "aconit", "dose", "ppm", "nectar", "sucrose",
    "visit", "rob", "choice", "consume", "time", "flower", "plant", "treat", "trial", "rep",
)
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _get(url: str, *, accept: str = "application/json,*/*") -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public Figshare endpoints
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_FILE_BYTES:
            raise ValueError(f"response too large: {length}")
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


def _audit_text(file: dict[str, object]) -> dict[str, object]:
    name = str(file.get("name") or "")
    url = str(file.get("download_url") or "")
    result: dict[str, object] = {
        "file_id": file.get("id"),
        "file_name": name,
        "size_bytes": file.get("size"),
        "suffix": _suffix(name),
        "download_url_present": bool(url),
    }
    if not url or _suffix(name) not in TEXT_SUFFIXES:
        return result
    raw = _get(url, accept="text/csv,text/plain,*/*")
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = "\t" if sample.count("\t") > sample.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    n_rows = sum(1 for _ in reader)
    result.update({
        "delimiter": "tab" if delimiter == "\t" else delimiter,
        "n_rows": n_rows,
        "headers": headers,
        "candidate_columns": _candidate_columns(headers),
    })
    return result


def _shared_strings(book: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    strings: list[str] = []
    for si in root.findall(f"{{{NS_MAIN}}}si"):
        strings.append("".join(node.text or "" for node in si.iter(f"{{{NS_MAIN}}}t")))
    return strings


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
    # Numeric/non-string first-row cells are not outcome values we need for schema.
    return value.text.strip()


def _sheet_targets(book: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in rels.findall(f"{{{NS_REL_PKG}}}Relationship")
    }
    output: list[tuple[str, str]] = []
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        return output
    for sheet in sheets.findall(f"{{{NS_MAIN}}}sheet"):
        rel_id = sheet.attrib.get(f"{{{NS_REL_DOC}}}id", "")
        target = rel_map.get(rel_id, "")
        if not target:
            continue
        if target.startswith("/"):
            path = target.lstrip("/")
        else:
            target = re.sub(r"^\.\./", "", target)
            path = f"xl/{target}" if not target.startswith("xl/") else target
        output.append((sheet.attrib.get("name", ""), path))
    return output


def _audit_xlsx(file: dict[str, object]) -> dict[str, object]:
    name = str(file.get("name") or "")
    url = str(file.get("download_url") or "")
    result: dict[str, object] = {
        "file_id": file.get("id"),
        "file_name": name,
        "size_bytes": file.get("size"),
        "suffix": _suffix(name),
        "download_url_present": bool(url),
    }
    if not url or _suffix(name) != ".xlsx":
        return result
    raw = _get(url, accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*")
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
    result["workbook_sheets"] = sheets
    result["schema_guardrail"] = "Only workbook sheet names, dimensions, and first-row headers were read; no non-header observation values were emitted."
    return result


def _audit_file(file: dict[str, object]) -> dict[str, object]:
    suffix = _suffix(str(file.get("name") or ""))
    if suffix == ".xlsx":
        return _audit_xlsx(file)
    return _audit_text(file)


def run(output_path: str | Path) -> dict[str, object]:
    article = _json(f"{FIGSHARE_API}/articles/{ARTICLE_ID}")
    files = article.get("files") if isinstance(article, dict) else []
    if not isinstance(files, list):
        files = []
    report = {
        "source_doi": SOURCE_DOI,
        "declared_data_doi": DATA_DOI,
        "figshare_article_id": ARTICLE_ID,
        "title": article.get("title") if isinstance(article, dict) else None,
        "doi": article.get("doi") if isinstance(article, dict) else None,
        "resource_doi": article.get("resource_doi") if isinstance(article, dict) else None,
        "resource_title": article.get("resource_title") if isinstance(article, dict) else None,
        "file_count": len(files),
        "files": [_audit_file(item) for item in files if isinstance(item, dict)],
        "guardrails": [
            "No observation-level rows or non-header cell values are written to the report.",
            "This is source/schema adjudication only; no biological coefficient is fitted here.",
            "Any later model must be predeclared from the primary article before reading outcome values for result selection.",
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
    print(json.dumps({"file_count": result["file_count"], "title": result["title"]}, indent=2))
