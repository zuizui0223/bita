"""Audit Sakhalkar et al. 2023 public Zenodo archive without emitting raw rows."""

from __future__ import annotations

import io
import json
import zipfile
import posixpath
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import Request, urlopen

DATASET_DOI = "10.5281/zenodo.8398202"
DOWNLOAD_URL = (
    "https://zenodo.org/records/8398202/files/"
    "SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip?download=1"
)
USER_AGENT = "bita-sakhalkar2023-zenodo-audit/1.0"
MAX_BYTES = 8 * 1024 * 1024



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
            first_row = root.find(
                f"{{{_MAIN_NS}}}sheetData/{{{_MAIN_NS}}}row"
            )
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


def summarize_archive(data: bytes) -> dict[str, object]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        names = sorted(item.filename for item in members)
        csv_files = sorted(name for name in names if name.lower().endswith(".csv"))
        xlsx_files = sorted(\n            name for name in names\n            if name.lower().endswith(".xlsx") and not Path(name).name.startswith("~$")\n        )\n        xlsx_workbooks = {\n            name: inspect_xlsx_schema(archive.read(name)) for name in xlsx_files\n        }\n        r_files = sorted(name for name in names if name.lower().endswith(".r"))
        readme_files = sorted(
            name for name in names
            if Path(name).name.lower().startswith("readme")
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
            "guardrail": "Archive inventory only. File contents and raw rows are not emitted.",
        }


def _download() -> bytes:
    request = Request(DOWNLOAD_URL, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public Zenodo URL
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Zenodo archive exceeds configured size limit")
    return data


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
                "csv_files": result["csv_files"],
                "xlsx_files": result["xlsx_files"],
                "r_files": result["r_files"],
                "readme_files": result["readme_files"],
            },
            indent=2,
            sort_keys=True,
        )
    )
