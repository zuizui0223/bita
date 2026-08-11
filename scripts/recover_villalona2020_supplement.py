"""Recover and inventory the Villalona et al. 2020 supplementary DOCX.

Article: The role of toxic nectar secondary compounds in driving differential
bumble bee preferences for milkweed flowers
DOI: 10.1007/s00442-020-04701-0

This utility preserves the publisher supplement, exports every DOCX table to
CSV, and writes a source receipt. It performs no biological reclassification
and does not select a canonical effect.

Usage:
    python scripts/recover_villalona2020_supplement.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

DOI = "10.1007/s00442-020-04701-0"
ARTICLE_URL = "https://link.springer.com/article/10.1007/s00442-020-04701-0"
SUPPLEMENT_URL = (
    "https://static-content.springer.com/esm/"
    "art%3A10.1007%2Fs00442-020-04701-0/MediaObjects/"
    "442_2020_4701_MOESM1_ESM.docx"
)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def _request(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document,"
                "application/octet-stream,*/*"
            ),
            "Referer": ARTICLE_URL,
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def _curl(url: str) -> bytes:
    command = [
        "curl",
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--max-time",
        "180",
        "--user-agent",
        USER_AGENT,
        "--header",
        (
            "Accept: application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document,application/octet-stream,*/*"
        ),
        "--referer",
        ARTICLE_URL,
        url,
    ]
    completed = subprocess.run(command, check=True, capture_output=True)
    return completed.stdout


def _is_docx(payload: bytes) -> bool:
    if payload[:2] != b"PK":
        return False
    try:
        from io import BytesIO

        with zipfile.ZipFile(BytesIO(payload)) as archive:
            names = set(archive.namelist())
            return "[Content_Types].xml" in names and "word/document.xml" in names
    except zipfile.BadZipFile:
        return False


def recover() -> tuple[bytes, str, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for method_name, method in (("urllib", _request), ("curl", _curl)):
        try:
            payload = method(SUPPLEMENT_URL)
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append(
                {
                    "url": SUPPLEMENT_URL,
                    "method": method_name,
                    "status": "failed",
                    "error": repr(error),
                }
            )
            continue
        valid = _is_docx(payload)
        attempts.append(
            {
                "url": SUPPLEMENT_URL,
                "method": method_name,
                "status": "docx_recovered" if valid else "not_docx",
                "bytes": len(payload),
                "preview": payload[:120].decode("utf-8", errors="replace"),
            }
        )
        if valid:
            return payload, SUPPLEMENT_URL, attempts
    raise RuntimeError(
        json.dumps(
            {"message": "Villalona 2020 supplementary DOCX not recovered", "attempts": attempts},
            indent=2,
        )
    )


def _node_text(node: ET.Element) -> str:
    parts = [text.text or "" for text in node.findall(".//w:t", NS)]
    return "".join(parts).strip()


def _table_rows(table: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.findall("./w:tr", NS):
        values = [_node_text(cell) for cell in row.findall("./w:tc", NS)]
        rows.append(values)
    return rows


def export_docx(docx_path: Path, output_dir: Path) -> tuple[list[dict[str, object]], int]:
    table_dir = output_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml")
        (output_dir / "word_document.xml").write_bytes(document_xml)

    root = ET.fromstring(document_xml)
    body = root.find(".//w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no document body")

    text_lines: list[str] = []
    inventory: list[dict[str, object]] = []
    table_index = 0
    for child in list(body):
        if child.tag == f"{{{W_NS}}}p":
            text = _node_text(child)
            if text:
                text_lines.append(text)
        elif child.tag == f"{{{W_NS}}}tbl":
            table_index += 1
            rows = _table_rows(child)
            csv_path = table_dir / f"table_{table_index:02d}.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerows(rows)
            max_columns = max((len(row) for row in rows), default=0)
            inventory.append(
                {
                    "table_index": table_index,
                    "row_count": len(rows),
                    "max_columns": max_columns,
                    "first_row": " | ".join(rows[0]) if rows else "",
                    "csv_path": str(csv_path.relative_to(output_dir)),
                }
            )
            text_lines.append(f"[TABLE {table_index}: {len(rows)} rows x {max_columns} columns]")
            for row in rows:
                text_lines.append("\t".join(row))

    (output_dir / "document_text.txt").write_text(
        "\n".join(text_lines) + "\n", encoding="utf-8"
    )
    with (output_dir / "table_inventory.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("table_index", "row_count", "max_columns", "first_row", "csv_path"),
        )
        writer.writeheader()
        writer.writerows(inventory)
    return inventory, len(text_lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload, source_url, attempts = recover()
    docx_path = output_dir / "villalona2020_supplement.docx"
    docx_path.write_bytes(payload)
    inventory, text_line_count = export_docx(docx_path, output_dir)

    receipt = {
        "article_doi": DOI,
        "article_title": (
            "The role of toxic nectar secondary compounds in driving differential "
            "bumble bee preferences for milkweed flowers"
        ),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "table_count": len(inventory),
        "document_text_line_count": text_line_count,
        "tables": inventory,
        "attempts": attempts,
        "interpretation_boundary": (
            "The DOCX and all table cells are preserved without selecting effects. "
            "Each contrast must still be mapped to trial, bee species, dose, time, "
            "experimental unit, outcome lane, B-role provenance, and dependence "
            "before canonical use."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
