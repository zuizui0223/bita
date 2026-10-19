"""Source-only HUSCAP 2025 Peucedanum ZIP inspection; no source data redistribution.

This DOI was explicitly cited as the DATA archive in Kudo & Shibata (2025),
Journal of Ecology DOI 10.1111/1365-2745.70130.
Do NOT substitute 2022 Dryad 10.5061/dryad.w3r2280v5 as its raw data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

DOI = "10.14943/hu95572"
PAGE = "https://eprints.lib.hokudai.ac.jp/repo/huscap/all/95572/"
ARCHIVE = PAGE + "Kudo%24Shibata_JEcol_Data.zip"
MAX_DOWNLOAD = 60 * 1024 * 1024
MAX_UNCOMPRESSED_TOTAL = 250 * 1024 * 1024
MAX_ENTRY = 80 * 1024 * 1024
RESULT_SCHEMA = "BITA_2025_HUSCAP_SOURCE_SCHEMA_PROBE_V1"


def _plain_header(data: bytes, max_rows=5) -> dict:
    """Read bounded CSV / TSV line structure, not a statistical data analysis."""
    text = data[:32768].decode("utf-8-sig", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return {"first_rows": [], "columns": 0}
    delim = "\t" if "\t" in lines[0] else ","
    rows = list(csv.reader(lines[:max_rows], delimiter=delim))
    return {
        "columns": len(rows[0]) if rows else 0,
        "first_rows": [[v[:60] for v in row[:30]] for row in rows],
        "separator": "tab" if delim == "\t" else "comma",
    }


def inspect_zip(blob: bytes) -> dict:
    """Reject HTML, malformed/oversize archives and unsafe paths before inspection."""
    if len(blob) > MAX_DOWNLOAD or not blob.startswith(b"PK"):
        raise ValueError("SOURCE_NOT_ZIP_OR_TOO_LARGE")
    output = []
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        files = [z for z in zf.infolist() if not z.is_dir()]
        if not files:
            raise ValueError("EMPTY_PRIMARY_ARCHIVE")
        if sum(z.file_size for z in files) > MAX_UNCOMPRESSED_TOTAL:
            raise ValueError("UNCOMPRESSED_ARCHIVE_TOO_LARGE")
        if len(files) > 1000:
            raise ValueError("TOO_MANY_FILES")
        for z in files:
            path = PurePosixPath(z.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in z.filename
                    or z.file_size > MAX_ENTRY):
                raise ValueError("UNSAFE_OR_OVERSIZED_ENTRY")
            name = z.filename
            lower = name.lower()
            entry = {
                "name": name, "size": z.file_size,
                "kind": "other",
            }
            if lower.endswith((".csv", ".tsv", ".txt")) and z.file_size <= 10*1024*1024:
                entry["kind"] = "tabular_text_candidate"
                with zf.open(z) as stream:
                    entry["preview"] = _plain_header(stream.read(32768))
            elif lower.endswith((".xlsx", ".xls", ".xlsm")):
                entry["kind"] = "spreadsheet_candidate_schema_not_inspected"
            elif lower.endswith(".r") or lower.endswith(".rmd"):
                entry["kind"] = "analysis_code"
            elif lower.endswith((".rdata", ".rds")):
                entry["kind"] = "serialized_R_object_no_untrusted_execution"
            output.append(entry)
    return {
        "zip_sha256": hashlib.sha256(blob).hexdigest(),
        "zip_bytes": len(blob),
        "entries": output,
        "entries_n": len(output),
        "supported_readable_tables": sum(e["kind"] == "tabular_text_candidate" for e in output),
    }


def fetch() -> bytes:
    req = urllib.request.Request(ARCHIVE, headers={
        "User-Agent": "Mozilla/5.0 (compatible; open-research-source-audit/1.0)",
        "Accept": "application/zip, application/octet-stream, */*",
    })
    with urllib.request.urlopen(req, timeout=35) as response:
        data = response.read(MAX_DOWNLOAD+1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("SOURCE_TOO_LARGE")
    return data


def audit(fetcher=fetch) -> dict:
    report = {
        "receipt_schema": RESULT_SCHEMA,
        "source_paper": "Kudo & Shibata (2025), Journal of Ecology, DOI 10.1111/1365-2745.70130",
        "doi": DOI, "source_archive_url": ARCHIVE,
        "data_level": "SOURCE_AVAILABILITY_AND_SCHEMA_ONLY",
        "raw_data_redistributed": False, "statistical_result_computed": False,
        "status": "SOURCE_NOT_VERIFIED",
    }
    try:
        analysis = inspect_zip(fetcher())
        report.update(analysis)
        report["status"] = "SOURCE_ZIP_VERIFIED_SCHEMA_LISTED"
        report["note"] = "SHA256 recorded from current source, not matched to earlier frozen archive; no biological fit yet."
    except (OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as exc:
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)[:180]
        report["note"] = "No invented data; require verified bytes before statistical reanalysis."
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("artifacts/bita_peucedanum2025_huscap_probe.json"))
    opts = ap.parse_args()
    receipt = audit()
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
