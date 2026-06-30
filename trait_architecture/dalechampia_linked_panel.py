"""Audit a secondary public Dryad package for the *Dalechampia* linked panel.

The package DOI belongs to a later data release, not automatically to the focal
2013 Oikos paper.  This module therefore separates:

* identity of the public data package;
* explicit metadata relation to the focal article;
* recoverable file/header structure; and
* candidate biological linkage fields.

It does not assign a trait to ``B_flower`` or estimate an effect.  No raw rows
are written to repository outputs.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from collections import Counter
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


DRYAD_BASE_URL = "https://datadryad.org"
DATACITE_BASE_URL = "https://api.datacite.org"
USER_AGENT = "biotic-interaction-trait-architecture dalechampia-linked-panel/0.1"
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
MAX_HEADER_BYTES = 131_072
MAX_FILE_PAGES = 50
NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RELATION_TYPES = frozenset({"issupplementto", "isderivedfrom", "ispartof"})


@dataclass(frozen=True)
class TableSchema:
    file_name: str
    table_format: str
    schema_status: str
    column_names: str
    candidate_linkage_fields: str
    notes: str


SCHEMA_FIELDS = tuple(TableSchema.__dataclass_fields__)


def _text(value: object) -> str:
    return str(value or "").strip()


def _normalise_doi(value: object) -> str:
    doi = _text(value).lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
            break
    return doi.strip()


def _fetch_json(url: str, *, timeout: int = 20) -> tuple[int, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # nosec B310: fixed public metadata endpoints
        return int(getattr(response, "status", response.getcode())), json.loads(response.read().decode("utf-8"))


def _fetch_bytes(url: str, *, timeout: int = 45) -> bytes:
    request = Request(url, headers={"Accept": "application/zip,application/octet-stream,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # nosec B310: fixed public version archive route
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_ARCHIVE_BYTES:
            raise ValueError(f"archive exceeds configured size: {content_length}")
        content = response.read(MAX_ARCHIVE_BYTES + 1)
    if len(content) > MAX_ARCHIVE_BYTES:
        raise ValueError("archive exceeded configured byte limit")
    return content


def _href(payload: Any, relation: str) -> str:
    if not isinstance(payload, dict):
        return ""
    links = payload.get("_links") or payload.get("links")
    if not isinstance(links, dict):
        return ""
    value = links.get(relation)
    if isinstance(value, dict):
        value = value.get("href")
    return urljoin(DRYAD_BASE_URL, _text(value)) if _text(value) else ""


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _files(payload: Any) -> list[str]:
    names: set[str] = set()
    for node in _walk(payload):
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else node
        if not isinstance(attrs, dict):
            continue
        name = _text(attrs.get("path") or attrs.get("filename") or attrs.get("file_name") or attrs.get("name"))
        if name:
            names.add(name)
    return sorted(names)


def _related_article_status(metadata: Any, article_doi: str) -> tuple[str, str]:
    if not isinstance(metadata, dict):
        return "datacite_payload_invalid", ""
    data = metadata.get("data")
    attrs = data.get("attributes") if isinstance(data, dict) and isinstance(data.get("attributes"), dict) else {}
    related = attrs.get("relatedIdentifiers") or attrs.get("related_identifiers")
    if not isinstance(related, list):
        return "no_declared_article_relation", ""
    target = _normalise_doi(article_doi)
    for item in related:
        if not isinstance(item, dict):
            continue
        related_doi = _normalise_doi(item.get("relatedIdentifier") or item.get("identifier"))
        relation = _text(item.get("relationType") or item.get("relation_type"))
        if related_doi == target:
            if relation.lower() in RELATION_TYPES:
                return "declared_related_article", relation
            return "article_mentioned_with_nonqualifying_relation", relation
    return "no_declared_article_relation", ""


def _dataset_title(metadata: Any) -> str:
    if not isinstance(metadata, dict):
        return ""
    data = metadata.get("data")
    attrs = data.get("attributes") if isinstance(data, dict) and isinstance(data.get("attributes"), dict) else {}
    titles = attrs.get("titles")
    if isinstance(titles, list):
        for item in titles:
            if isinstance(item, dict) and _text(item.get("title")):
                return _text(item["title"])
    return _text(attrs.get("title"))


def _dataset_chain(dataset_doi: str, fetch_json: Callable[[str], tuple[int, Any]]) -> tuple[list[str], str, str]:
    dataset_url = f"{DRYAD_BASE_URL}/api/v2/datasets/{quote(f'doi:{dataset_doi}', safe='')}"
    status, dataset = fetch_json(dataset_url)
    if status >= 400:
        raise RuntimeError(f"Dryad dataset endpoint HTTP {status}")
    version_url = _href(dataset, "stash:version")
    if not version_url:
        raise RuntimeError("Dryad dataset has no stash:version link")
    status, version = fetch_json(version_url)
    if status >= 400:
        raise RuntimeError(f"Dryad version endpoint HTTP {status}")
    files_url = _href(version, "stash:files")
    if not files_url:
        raise RuntimeError("Dryad version has no stash:files link")
    names: set[str] = set()
    page_url = files_url
    pages = 0
    while page_url and pages < MAX_FILE_PAGES:
        status, payload = fetch_json(page_url)
        if status >= 400:
            raise RuntimeError(f"Dryad files endpoint HTTP {status}")
        names.update(_files(payload))
        page_url = _href(payload, "next")
        pages += 1
    if page_url:
        raise RuntimeError("Dryad file pagination exceeded configured limit")
    return sorted(names), version_url, f"{version_url}/download"


def _delimiter_header(prefix: bytes) -> list[str]:
    text = prefix.decode("utf-8-sig", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("no non-empty header line")
    sample = "\n".join(lines[:5])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t; ")
    except csv.Error:
        dialect = csv.excel_tab if "\t" in lines[0] else csv.excel
    return [_text(value) for value in next(csv.reader(io.StringIO(lines[0]), dialect=dialect))]


def _xlsx_header(content: bytes) -> list[str]:
    workbook = zipfile.ZipFile(BytesIO(content))
    shared: list[str] = []
    if "xl/sharedStrings.xml" in workbook.namelist():
        root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
        shared = ["".join(node.itertext()) for node in root.findall("x:si", NS)]
    sheets = sorted(name for name in workbook.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name))
    if not sheets:
        raise ValueError("xlsx has no worksheet")
    root = ET.fromstring(workbook.read(sheets[0]))
    first_row = root.find(".//x:sheetData/x:row", NS)
    if first_row is None:
        raise ValueError("xlsx has no header row")
    values: list[str] = []
    for cell in first_row.findall("x:c", NS):
        raw = cell.findtext("x:v", default="", namespaces=NS)
        if cell.get("t") == "s" and raw.isdigit() and int(raw) < len(shared):
            values.append(_text(shared[int(raw)]))
        else:
            values.append(_text(raw))
    if not any(values):
        raise ValueError("xlsx header has no values")
    return values


def _candidate_linkage_fields(columns: Iterable[str]) -> list[str]:
    targets = ("population", "year", "date", "patch", "blossom", "flower", "id")
    return [column for column in columns if any(token in column.lower() for token in targets)]


def _archive_schemas(archive: zipfile.ZipFile) -> list[TableSchema]:
    rows: list[TableSchema] = []
    for member in sorted(archive.infolist(), key=lambda item: item.filename):
        if member.is_dir():
            continue
        lower = member.filename.lower()
        if not lower.endswith((".txt", ".csv", ".tsv", ".xlsx")):
            continue
        try:
            content = archive.read(member)
            if lower.endswith(".xlsx"):
                columns = _xlsx_header(content)
                table_format = "xlsx"
            else:
                columns = _delimiter_header(content[:MAX_HEADER_BYTES])
                table_format = "delimited_text"
            rows.append(TableSchema(
                file_name=member.filename,
                table_format=table_format,
                schema_status="header_recovered",
                column_names=";".join(columns),
                candidate_linkage_fields=";".join(_candidate_linkage_fields(columns)),
                notes="Header only; no observations retained. Semantic identity of keys still requires documentation review.",
            ))
        except Exception as error:
            rows.append(TableSchema(
                file_name=member.filename,
                table_format="xlsx" if lower.endswith(".xlsx") else "delimited_text",
                schema_status="header_parse_failed",
                column_names="",
                candidate_linkage_fields="",
                notes=f"{type(error).__name__}: {error}",
            ))
    return rows


def _linkage_overlap(schemas: Iterable[TableSchema]) -> dict[str, object]:
    parsed = [row for row in schemas if row.schema_status == "header_recovered"]
    counts: Counter[str] = Counter()
    for row in parsed:
        for field in set(token for token in row.candidate_linkage_fields.split(";") if token):
            counts[field.lower()] += 1
    repeated = sorted(field for field, count in counts.items() if count >= 3)
    return {
        "parsed_table_count": len(parsed),
        "repeated_candidate_linkage_fields_in_at_least_three_tables": repeated,
        "status": "candidate_only" if repeated else "not_demonstrated_from_headers",
    }


def audit_package(
    *,
    article_doi: str,
    dataset_doi: str,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_bytes: Callable[[str], bytes] = _fetch_bytes,
) -> tuple[list[TableSchema], dict[str, object]]:
    article_doi = _normalise_doi(article_doi)
    dataset_doi = _normalise_doi(dataset_doi)
    metadata_url = f"{DATACITE_BASE_URL}/dois/{quote(dataset_doi, safe='')}"
    status, metadata = fetch_json(metadata_url)
    if status >= 400:
        raise RuntimeError(f"DataCite endpoint HTTP {status}")
    relation_status, relation_type = _related_article_status(metadata, article_doi)
    file_names, version_url, archive_url = _dataset_chain(dataset_doi, fetch_json)
    archive = zipfile.ZipFile(BytesIO(fetch_bytes(archive_url)))
    schemas = _archive_schemas(archive)
    report = {
        "article_doi": article_doi,
        "dataset_doi": dataset_doi,
        "dataset_title": _dataset_title(metadata),
        "article_relation_status": relation_status,
        "article_relation_type": relation_type,
        "version_url": version_url,
        "archive_url": archive_url,
        "manifest_file_count": len(file_names),
        "manifest_file_names": file_names,
        "schema": {
            "header_recovered": sum(row.schema_status == "header_recovered" for row in schemas),
            "header_parse_failed": sum(row.schema_status == "header_parse_failed" for row in schemas),
            "linkage": _linkage_overlap(schemas),
        },
        "decision_boundary": "This is a secondary linked-data structural audit. It cannot establish a direct four-path study card or extract effects until source relation and independent trait functions are reviewed.",
    }
    return schemas, report


def write_audit(out_dir: str | Path, schemas: Iterable[TableSchema], report: dict[str, object]) -> None:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "dalechampia_linked_panel_header_schemas.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        for row in schemas:
            writer.writerow(asdict(row))
    (output / "dalechampia_linked_panel_audit.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
