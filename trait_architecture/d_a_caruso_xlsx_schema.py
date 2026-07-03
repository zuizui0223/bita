"""Capped schema inspection for a Caruso-linked Dryad XLSX candidate.

This stage follows a verified Dryad manifest entry only when its filename suggests an
experimental-study database (`exp_stud`) or the manifest marked it as a study-index
candidate. It resolves the file's public metadata route first, then downloads the
exact XLSX file under a strict byte cap, reads workbook metadata, sheet names,
dimensions, and the first-row field names, and discards the bytes. No data rows,
effect values, selection gradients, or primary-study identifiers are written to
output.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


CARUSO_SOURCE_DOI = "10.1111/evo.13639"
DRYAD_DATASET_DOI = "10.5061/dryad.2v8c5g0"
MAX_WORKBOOK_BYTES = 1 * 1024 * 1024
USER_AGENT = "biotic-interaction-trait-architecture d-a-caruso-xlsx-schema/0.1"
BIBLIO_TERMS = ("doi", "author", "citation", "reference", "source", "paper", "year", "study")
ROUTE_TERMS = ("trait", "floral", "flower", "herbivor", "antagon", "pollinator", "damage", "oviposition", "seed")
SELECTION_TERMS = ("selection", "gradient", "beta", "coefficient", "standard error", "stderr", "se")
SCHEMA_FIELDS = (
    "source_doi", "dataset_doi", "filename", "file_url", "file_metadata_status", "resolved_file_url",
    "workbook_format", "download_status", "source_bytes", "sheet_name", "worksheet_dimension", "header_fields",
    "bibliographic_identifier_columns", "route_context_columns", "selection_metric_columns", "schema_decision", "do_not_infer",
)
DO_NOT_INFER = (
    "Workbook schema receipt only. Do not infer or retain data rows, primary-study identifiers, trait-to-antagonism "
    "routes, selection gradients, effect values, denominators, uncertainty, or B2 eligibility."
)
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"


class DownloadHTTPError(RuntimeError):
    """A bounded file fetch failed with a known public HTTP status."""

    def __init__(self, status: int):
        self.status = status
        super().__init__(f"HTTP {status}")


@dataclass(frozen=True)
class XlsxSchemaReceipt:
    source_doi: str
    dataset_doi: str
    filename: str
    file_url: str
    file_metadata_status: str
    resolved_file_url: str
    workbook_format: str
    download_status: str
    source_bytes: str
    sheet_name: str
    worksheet_dimension: str
    header_fields: str
    bibliographic_identifier_columns: str
    route_context_columns: str
    selection_metric_columns: str
    schema_decision: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _matches(fields: Iterable[str], terms: Iterable[str]) -> list[str]:
    return [field for field in fields if any(term in field.casefold() for term in terms)]


def read_manifest(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    selected: list[dict[str, str]] = []
    for row in rows:
        filename = row.get("filename", "").casefold()
        if row.get("access_status") != "file_manifest_entry" or not filename.endswith(".xlsx"):
            continue
        # The Caruso manifest calls the experimental-study database `Exp_stud`.
        if row.get("primary_study_index_candidate") == "true" or "exp_stud" in filename:
            selected.append(row)
    return selected


def _json(url: str) -> tuple[int, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=60) as response:  # nosec B310: exact public Dryad file-metadata route
            status = int(getattr(response, "status", response.getcode()))
            return status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return int(error.code), None
    except (UnicodeDecodeError, json.JSONDecodeError):
        return 0, None


def _download(url: str) -> bytes:
    # Dryad may redirect to object storage; urlopen follows standard redirects.
    request = Request(url, headers={"Accept": "*/*", "User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=90) as response:  # nosec B310: exact public Dryad route from file metadata
            payload = response.read(MAX_WORKBOOK_BYTES + 1)
    except HTTPError as error:
        raise DownloadHTTPError(int(error.code)) from error
    if len(payload) > MAX_WORKBOOK_BYTES:
        raise ValueError(f"workbook exceeds {MAX_WORKBOOK_BYTES} byte cap")
    return payload


def _resource(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _metadata_url(download_url: str) -> str:
    return download_url[:-len("/download")] if download_url.rstrip("/").endswith("/download") else download_url


def _download_link(payload: Any, *, base_url: str) -> str:
    links = _resource(payload).get("_links")
    if not isinstance(links, dict):
        return ""
    for key in ("stash:download", "download"):
        item = links.get(key)
        href = _text(item.get("href")) if isinstance(item, dict) else _text(item)
        if href:
            return urljoin(base_url, href)
    return ""


def _resolve_download_url(
    raw_url: str,
    *,
    fetch_json: Callable[[str], tuple[int, Any]] = _json,
) -> tuple[str, str]:
    """Resolve the provider's canonical download route; retain a fallback receipt."""

    metadata_url = _metadata_url(raw_url)
    try:
        status, payload = fetch_json(metadata_url)
    except Exception as error:
        return raw_url, f"metadata_request_failed:{type(error).__name__}"
    if status >= 400 or not isinstance(payload, dict):
        return raw_url, f"metadata_http_{status}_fallback"
    canonical = _download_link(payload, base_url=metadata_url)
    return (canonical, f"metadata_http_{status}_resolved") if canonical else (raw_url, f"metadata_http_{status}_no_download_link_fallback")


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.itertext()).strip() for node in root.findall(f"{NS}si")]


def _sheet_routes(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        _text(rel.get("Id")): _text(rel.get("Target"))
        for rel in rels.findall(f"{PKG_REL_NS}Relationship")
    }
    routes: list[tuple[str, str]] = []
    for sheet in workbook.findall(f".//{NS}sheet"):
        name = _text(sheet.get("name"))
        relation_id = _text(sheet.get(f"{REL_NS}id"))
        target = targets.get(relation_id, "")
        if target:
            routes.append((name, "xl/" + target.lstrip("/")))
    return routes


def _cell_text(cell: ET.Element, shared: list[str]) -> str:
    kind = _text(cell.get("t"))
    if kind == "inlineStr":
        return "".join(cell.itertext()).strip()
    value = cell.find(f"{NS}v")
    raw = _text(value.text if value is not None else "")
    if kind == "s" and raw.isdigit():
        index = int(raw)
        return shared[index] if 0 <= index < len(shared) else ""
    return raw


def _header_and_dimension(archive: zipfile.ZipFile, path: str, shared: list[str]) -> tuple[list[str], str]:
    root = ET.fromstring(archive.read(path))
    dimension = root.find(f"{NS}dimension")
    dimension_ref = _text(dimension.get("ref") if dimension is not None else "")
    first_row = root.find(f".//{NS}sheetData/{NS}row")
    if first_row is None:
        return [], dimension_ref
    fields = [_cell_text(cell, shared) for cell in first_row.findall(f"{NS}c")]
    return [field for field in fields if field][:100], dimension_ref


def _failed_receipt(filename: str, file_url: str, metadata_status: str, resolved_url: str, failure: str) -> XlsxSchemaReceipt:
    return XlsxSchemaReceipt(
        CARUSO_SOURCE_DOI, DRYAD_DATASET_DOI, filename, file_url, metadata_status, resolved_url,
        "xlsx", "download_or_parse_failed", "", "", "", "", "", "", "", f"retain_as_manifest_candidate:{failure}",
    )


def inspect_xlsx_candidate(
    row: dict[str, str],
    *,
    download: Callable[[str], bytes] = _download,
    fetch_json: Callable[[str], tuple[int, Any]] = _json,
) -> list[XlsxSchemaReceipt]:
    filename, file_url = row["filename"], row["file_url"]
    resolved_url, metadata_status = _resolve_download_url(file_url, fetch_json=fetch_json)
    try:
        payload = download(resolved_url)
        archive = zipfile.ZipFile(io.BytesIO(payload))
        shared = _shared_strings(archive)
        routes = _sheet_routes(archive)
    except DownloadHTTPError as error:
        return [_failed_receipt(filename, file_url, metadata_status, resolved_url, f"download_http_{error.status}")]
    except Exception as error:
        return [_failed_receipt(filename, file_url, metadata_status, resolved_url, type(error).__name__)]

    output: list[XlsxSchemaReceipt] = []
    for sheet_name, sheet_path in routes:
        try:
            headers, dimension = _header_and_dimension(archive, sheet_path, shared)
        except (KeyError, ET.ParseError):
            headers, dimension = [], ""
        bibliographic = _matches(headers, BIBLIO_TERMS)
        route_context = _matches(headers, ROUTE_TERMS)
        selection = _matches(headers, SELECTION_TERMS)
        decision = "bibliographic_index_columns_present_needs_identifier_extraction" if bibliographic else "no_bibliographic_identifier_columns_in_xlsx_headers"
        output.append(XlsxSchemaReceipt(
            CARUSO_SOURCE_DOI, DRYAD_DATASET_DOI, filename, file_url, metadata_status, resolved_url,
            "xlsx", "schema_recovered", str(len(payload)), sheet_name, dimension, ";".join(headers),
            ";".join(bibliographic), ";".join(route_context), ";".join(selection), decision,
        ))
    return output or [XlsxSchemaReceipt(
        CARUSO_SOURCE_DOI, DRYAD_DATASET_DOI, filename, file_url, metadata_status, resolved_url,
        "xlsx", "schema_recovered_no_sheets", str(len(payload)), "", "", "", "", "", "",
        "retain_as_manifest_candidate_no_worksheet_schema",
    )]


def inspect_manifest(
    manifest_csv: str | Path,
    *,
    download: Callable[[str], bytes] = _download,
    fetch_json: Callable[[str], tuple[int, Any]] = _json,
) -> list[XlsxSchemaReceipt]:
    return [
        receipt for row in read_manifest(manifest_csv)
        for receipt in inspect_xlsx_candidate(row, download=download, fetch_json=fetch_json)
    ]


def write_outputs(out_dir: str | Path, rows: Iterable[XlsxSchemaReceipt]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_caruso_xlsx_schema.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "xlsx_schema_sheet_count": len(rows),
        "sheets_with_bibliographic_identifier_columns": sum(row.schema_decision == "bibliographic_index_columns_present_needs_identifier_extraction" for row in rows),
        "next_action": "extract_bibliographic_identifiers_only" if any(row.schema_decision == "bibliographic_index_columns_present_needs_identifier_extraction" for row in rows) else "stop_before_row_level_extraction_no_bibliographic_identifier_columns",
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_caruso_xlsx_schema_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report
