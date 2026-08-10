"""Recover and inventory the study-level supplement for Parachnowitsch et al. 2019.

This is a source-recovery utility, not a meta-analysis. It downloads the publicly
listed XLSX supplement for doi:10.1093/aob/mcy132, records a provenance receipt,
and exports every worksheet to CSV without interpreting or reclassifying rows.

Usage:
    python scripts/recover_parachnowitsch2019_supplement.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ARTICLE_URLS = (
    "https://academic.oup.com/aob/article/123/2/247/5055672",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC6344224/",
)
FALLBACK_XLSX = (
    "https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/aob/123/2/"
    "10.1093_aob_mcy132/1/mcy132_suppl_aob-18212-s03.xlsx"
)
USER_AGENT = "bita-source-recovery/1.0 (+https://github.com/zuizui0223/bita)"


def _request(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def _candidate_links(page_url: str, body: bytes) -> list[str]:
    text = html.unescape(body.decode("utf-8", errors="replace"))
    hrefs = re.findall(r"href=[\"']([^\"']+)[\"']", text, flags=re.IGNORECASE)
    candidates: list[str] = []
    for href in hrefs:
        absolute = urllib.parse.urljoin(page_url, href)
        lowered = absolute.lower()
        if lowered.endswith(".xlsx") or ("mcy132" in lowered and "s03" in lowered):
            candidates.append(absolute)
    # Preserve discovery order while removing duplicates.
    return list(dict.fromkeys(candidates))


def discover_xlsx() -> tuple[str, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for page_url in ARTICLE_URLS:
        try:
            body = _request(page_url)
            links = _candidate_links(page_url, body)
            attempts.append({"url": page_url, "status": "retrieved", "candidate_links": links})
            for link in links:
                try:
                    payload = _request(link)
                except Exception as error:  # pragma: no cover - network dependent
                    attempts.append({"url": link, "status": "download_failed", "error": repr(error)})
                    continue
                if payload[:2] == b"PK":
                    attempts.append({"url": link, "status": "xlsx_recovered", "bytes": len(payload)})
                    return link, attempts
                attempts.append({"url": link, "status": "not_xlsx", "bytes": len(payload)})
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append({"url": page_url, "status": "page_failed", "error": repr(error)})

    try:
        payload = _request(FALLBACK_XLSX)
        attempts.append({"url": FALLBACK_XLSX, "status": "fallback_retrieved", "bytes": len(payload)})
        if payload[:2] == b"PK":
            return FALLBACK_XLSX, attempts
    except Exception as error:  # pragma: no cover - network dependent
        attempts.append({"url": FALLBACK_XLSX, "status": "fallback_failed", "error": repr(error)})

    raise RuntimeError(json.dumps({"message": "XLSX supplement not recovered", "attempts": attempts}, indent=2))


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return cleaned or "sheet"


def _cell_value(value: object) -> object:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def export_workbook(xlsx_path: Path, output_dir: Path) -> list[dict[str, object]]:
    from openpyxl import load_workbook

    workbook = load_workbook(xlsx_path, read_only=True, data_only=False)
    inventory: list[dict[str, object]] = []
    sheet_dir = output_dir / "sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)

    for index, worksheet in enumerate(workbook.worksheets, start=1):
        csv_path = sheet_dir / f"{index:02d}_{_safe_filename(worksheet.title)}.csv"
        nonempty_rows = 0
        nonempty_cells = 0
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            for row in worksheet.iter_rows(values_only=True):
                values = [_cell_value(value) for value in row]
                writer.writerow(values)
                row_nonempty = sum(value not in ("", None) for value in values)
                if row_nonempty:
                    nonempty_rows += 1
                    nonempty_cells += row_nonempty
        inventory.append(
            {
                "sheet_index": index,
                "sheet_name": worksheet.title,
                "max_row": worksheet.max_row,
                "max_column": worksheet.max_column,
                "nonempty_rows": nonempty_rows,
                "nonempty_cells": nonempty_cells,
                "csv_path": str(csv_path.relative_to(output_dir)),
            }
        )
    return inventory


def _write_inventory(path: Path, inventory: Iterable[dict[str, object]]) -> None:
    rows = list(inventory)
    fields = (
        "sheet_index",
        "sheet_name",
        "max_row",
        "max_column",
        "nonempty_rows",
        "nonempty_cells",
        "csv_path",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source_url, attempts = discover_xlsx()
    payload = _request(source_url)
    if payload[:2] != b"PK":
        raise RuntimeError("Recovered supplement does not have XLSX/ZIP magic bytes")

    xlsx_path = output_dir / "parachnowitsch2019_supplement_s3.xlsx"
    xlsx_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    inventory = export_workbook(xlsx_path, output_dir)
    _write_inventory(output_dir / "workbook_inventory.csv", inventory)

    receipt = {
        "article_doi": "10.1093/aob/mcy132",
        "article_title": "Evolutionary ecology of nectar",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "sha256": digest,
        "bytes": len(payload),
        "sheet_count": len(inventory),
        "attempts": attempts,
        "interpretation_boundary": (
            "This recovery preserves the published workbook and worksheet rows. "
            "No row is treated as a strict B-to-pollinator effect until the focal trait role, "
            "outcome lane, effect metric, and study independence are re-audited."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
