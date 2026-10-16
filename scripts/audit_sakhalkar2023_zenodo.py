"""Audit Sakhalkar et al. 2023 public Zenodo archive without emitting raw rows."""

from __future__ import annotations

import hashlib
import io
import json
import sys
from http.client import IncompleteRead
import posixpath
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DATASET_DOI = "10.5281/zenodo.8398202"
DOWNLOAD_URL = (
    "https://zenodo.org/records/8398202/files/"
    "SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip?download=1"
)
USER_AGENT = "bita-sakhalkar2023-zenodo-audit/1.0"
MAX_BYTES = 8 * 1024 * 1024

# Author-owned, tagged GitHub source for the exact Zenodo v1.0.0 release.
# Provenance was checked against the public GitHub git/ref and git/tree APIs.
# The tag resolves to the immutable commit below, and its input workbook has
# this Git blob SHA-1. We never accept an unpinned branch or a mismatched file.
UPSTREAM_COMMIT = "605d76245a8e89ec9932d0ce5368e47f1ecabd5c"
UPSTREAM_WORKBOOK_BLOB_SHA1 = "0ee25ea58c12e5641d0eda9926f8aa87bb5e35e6"
UPSTREAM_WORKBOOK_SIZE = 755_561
UPSTREAM_WORKBOOK_NAME = "cheaters_visitation_and_trait_data.xlsx"
UPSTREAM_SNAPSHOT_URL = (
    "https://codeload.github.com/"
    "SaileeSakhalkar/cheaters-among-pollinators-ecosphere/zip/"
    f"{UPSTREAM_COMMIT}"
)

_MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def _xlsx_shared_strings(book: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in book.namelist():
        return []
    root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for si in root.findall(f"{{{_MAIN_NS}}}si"):
        values.append("".join(t.text or "" for t in si.iter(f"{{{_MAIN_NS}}}t")))
    return values


def _xlsx_cell_text(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(f"{{{_MAIN_NS}}}t"))
    value = cell.find(f"{{{_MAIN_NS}}}v")
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        try:
            return shared[int(value.text)]
        except (ValueError, IndexError):
            return ""
    return value.text


def inspect_xlsx_schema(data: bytes) -> dict[str, object]:
    with zipfile.ZipFile(io.BytesIO(data)) as book:
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        rel_root = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        rels = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rel_root.findall(f"{{{_PKG_REL_NS}}}Relationship")
            if "Id" in rel.attrib and "Target" in rel.attrib
        }
        shared = _xlsx_shared_strings(book)
        sheets: list[dict[str, object]] = []
        sheets_node = workbook.find(f"{{{_MAIN_NS}}}sheets")
        if sheets_node is None:
            return {"sheets": sheets}

        for sheet in sheets_node.findall(f"{{{_MAIN_NS}}}sheet"):
            rel_id = sheet.attrib.get(f"{{{_DOC_REL_NS}}}id", "")
            target = rels.get(rel_id)
            if not target:
                continue
            sheet_path = posixpath.normpath(posixpath.join("xl", target.lstrip("/")))
            root = ET.fromstring(book.read(sheet_path))
            dimension = root.find(f"{{{_MAIN_NS}}}dimension")
            first_row = root.find(f"{{{_MAIN_NS}}}sheetData/{{{_MAIN_NS}}}row")
            headers: list[str] = []
            if first_row is not None:
                headers = [
                    _xlsx_cell_text(cell, shared)
                    for cell in first_row.findall(f"{{{_MAIN_NS}}}c")
                ]
            sheets.append(
                {
                    "name": sheet.attrib.get("name", ""),
                    "dimension": "" if dimension is None else dimension.attrib.get("ref", ""),
                    "headers": headers,
                }
            )
        return {"sheets": sheets}



def _column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha()).upper()
    value = 0
    for ch in letters:
        value = value * 26 + (ord(ch) - ord("A") + 1)
    return max(value - 1, 0)


def read_xlsx_sheet_rows(data: bytes, sheet_name: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(io.BytesIO(data)) as book:
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        rel_root = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        rels = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rel_root.findall(f"{{{_PKG_REL_NS}}}Relationship")
            if "Id" in rel.attrib and "Target" in rel.attrib
        }
        target_path: str | None = None
        sheets_node = workbook.find(f"{{{_MAIN_NS}}}sheets")
        if sheets_node is None:
            raise ValueError("workbook has no sheets")
        for sheet in sheets_node.findall(f"{{{_MAIN_NS}}}sheet"):
            if sheet.attrib.get("name") != sheet_name:
                continue
            rel_id = sheet.attrib.get(f"{{{_DOC_REL_NS}}}id", "")
            target = rels.get(rel_id)
            if target:
                target_path = posixpath.normpath(
                    posixpath.join("xl", target.lstrip("/"))
                )
            break
        if target_path is None:
            raise ValueError(f"worksheet not found: {sheet_name}")

        shared = _xlsx_shared_strings(book)
        root = ET.fromstring(book.read(target_path))
        xml_rows = root.findall(f"{{{_MAIN_NS}}}sheetData/{{{_MAIN_NS}}}row")
        if not xml_rows:
            return []

        def values(row: ET.Element) -> list[str]:
            cells = row.findall(f"{{{_MAIN_NS}}}c")
            if not cells:
                return []
            max_index = max(
                _column_index(cell.attrib.get("r", "A1")) for cell in cells
            )
            out = [""] * (max_index + 1)
            for cell in cells:
                index = _column_index(cell.attrib.get("r", "A1"))
                out[index] = _xlsx_cell_text(cell, shared)
            return out

        headers = values(xml_rows[0])
        records: list[dict[str, str]] = []
        for xml_row in xml_rows[1:]:
            row_values = values(xml_row)
            row_values.extend([""] * max(0, len(headers) - len(row_values)))
            records.append(
                {
                    header: row_values[index] if index < len(row_values) else ""
                    for index, header in enumerate(headers)
                    if header
                }
            )
        return records

def summarize_archive(data: bytes) -> dict[str, object]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        names = sorted(item.filename for item in members)
        csv_files = sorted(name for name in names if name.lower().endswith(".csv"))
        xlsx_files = sorted(
            name
            for name in names
            if name.lower().endswith(".xlsx")
            and not Path(name).name.startswith("~$")
        )
        xlsx_workbooks = {
            name: inspect_xlsx_schema(archive.read(name)) for name in xlsx_files
        }
        r_files = sorted(name for name in names if name.lower().endswith(".r"))
        readme_files = sorted(
            name for name in names if Path(name).name.lower().startswith("readme")
        )
        return {
            "dataset_doi": DATASET_DOI,
            "archive_member_count": len(members),
            "member_names": names,
            "total_uncompressed_bytes": sum(item.file_size for item in members),
            "csv_files": csv_files,
            "xlsx_files": xlsx_files,
            "xlsx_workbooks": xlsx_workbooks,
            "r_files": r_files,
            "readme_files": readme_files,
            "guardrail": (
                "Schema/inventory audit only. Raw data rows and script contents are not emitted."
            ),
        }


def _pinned_author_github_snapshot() -> bytes:
    """Use only the exact author-owned v1.0.0 commit if Zenodo transport fails.

    The ZIP container itself need not be byte-identical to Zenodo's GitHub export:
    the primary biological workbook must match its immutable git-blob identity.
    Manuscript-facing data/model outputs are still checked against frozen receipts.
    """
    request = Request(
        UPSTREAM_SNAPSHOT_URL,
        headers={"User-Agent": USER_AGENT, "Accept": "application/zip"},
    )
    with urlopen(request, timeout=60) as response:  # nosec B310: pinned author commit
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Pinned author GitHub archive exceeds configured size limit")

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = [item for item in archive.infolist() if not item.is_dir()]
            if sum(item.file_size for item in members) > 4 * MAX_BYTES:
                raise ValueError("Pinned author GitHub archive exceeds decompressed size limit")
            workbooks = [
                item for item in members
                if Path(item.filename).name == UPSTREAM_WORKBOOK_NAME
            ]
            if len(workbooks) != 1:
                raise ValueError(
                    f"Pinned author GitHub snapshot contains {len(workbooks)} "
                    "primary workbooks rather than exactly one"
                )
            if workbooks[0].file_size != UPSTREAM_WORKBOOK_SIZE:
                raise ValueError("Pinned author workbook size differs from tagged git tree")
            workbook = archive.read(workbooks[0])
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        raise ValueError("Invalid pinned author GitHub ZIP") from exc

    git_blob = hashlib.sha1(
        f"blob {len(workbook)}\0".encode("ascii") + workbook
    ).hexdigest()
    if git_blob != UPSTREAM_WORKBOOK_BLOB_SHA1:
        raise ValueError("Pinned author workbook git blob SHA-1 mismatch")
    print(
        "SOURCE_PROVENANCE: verified pinned author GitHub v1.0.0 source; "
        f"commit={UPSTREAM_COMMIT}; "
        f"workbook git blob={git_blob}; "
        "no assumption about the current Zenodo service status; "
        "frozen result checks still required.",
        file=sys.stderr,
    )
    return data


def _download() -> bytes:
    request = Request(DOWNLOAD_URL, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    attempts = 4
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310: fixed public Zenodo URL
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Zenodo archive exceeds configured size limit")
            return data
        except HTTPError as error:
            last_error = error
            if error.code < 500:
                # A changed/deleted Zenodo source is NOT a transient outage.
                raise RuntimeError(
                    f"Non-retryable Zenodo source response: HTTP {error.code}"
                ) from error
        except (URLError, ConnectionError, TimeoutError, IncompleteRead) as error:
            last_error = error
        if attempt < attempts - 1:
            time.sleep(2 ** attempt)

    # The author-maintained public GitHub tag is a separate, fixed source path,
    # NOT an unverified mirror or an excuse to emit committed summary statistics.
    try:
        print(
            "ZENODO_TRANSIENT_FAILURE: exhausted four retryable attempts; "
            "verifying pinned author-source fallback.",
            file=sys.stderr,
        )
        return _pinned_author_github_snapshot()
    except (HTTPError, URLError, ConnectionError, TimeoutError, IncompleteRead,
            ValueError, zipfile.BadZipFile, OSError) as fallback_error:
        raise RuntimeError(
            "Unable to retrieve the frozen Sakhalkar 2023 source after Zenodo "
            "retries and a pinned author-GitHub integrity check. "
            f"Dataset DOI: {DATASET_DOI}; tagged commit: {UPSTREAM_COMMIT}. "
            f"Last Zenodo error: {last_error}; "
            f"pinned author source error: {fallback_error}"
        ) from fallback_error


def run(output_path: str | Path) -> dict[str, object]:
    report = summarize_archive(_download())
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    result = run(args.output)
    print(
        json.dumps(
            {
                "archive_member_count": result["archive_member_count"],
                "xlsx_files": result["xlsx_files"],
                "r_files": result["r_files"],
                "readme_files": result["readme_files"],
            },
            indent=2,
            sort_keys=True,
        )
    )
