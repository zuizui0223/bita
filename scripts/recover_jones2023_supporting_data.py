"""Recover the published supporting CSV files for Jones et al. 2023.

Article: Plant secondary metabolite has dose-dependent effects on bumblebees
DOI: 10.1111/oik.10103

This is a source-recovery utility. It preserves the publisher files and writes
an auditable receipt; it does not decide which rows enter bita's strict-B pool.

Usage:
    python scripts/recover_jones2023_supporting_data.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DOI = "10.1111/oik.10103"
ARTICLE_URLS = (
    "https://nsojournals.onlinelibrary.wiley.com/doi/10.1111/oik.10103",
    "https://onlinelibrary.wiley.com/doi/10.1111/oik.10103",
)
FILES = (
    "oik13633-sup-0001-AppendixS1.csv",
    "oik13633-sup-0002-AppendixS2.csv",
    "oik13633-sup-0003-AppendixS3.csv",
)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"


def _looks_like_csv(payload: bytes) -> bool:
    if not payload or payload[:2] == b"PK":
        return False
    preview = payload[:1000].lstrip().lower()
    if preview.startswith((b"<!doctype html", b"<html", b"<?xml")):
        return False
    try:
        text = payload[:5000].decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return "," in text.splitlines()[0] and len(text.splitlines()) >= 2


def _request(url: str, referer: str | None = None) -> bytes:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/csv,text/plain,application/octet-stream,*/*",
    }
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def _curl(url: str, referer: str | None = None) -> bytes:
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "120", "--user-agent", USER_AGENT,
        "--header", "Accept: text/csv,text/plain,application/octet-stream,*/*",
    ]
    if referer:
        command += ["--referer", referer]
    command.append(url)
    completed = subprocess.run(command, check=True, capture_output=True)
    return completed.stdout


def candidate_urls(filename: str) -> list[tuple[str, str | None]]:
    encoded_doi = urllib.parse.quote(DOI, safe="")
    encoded_file = urllib.parse.quote(filename, safe="")
    candidates: list[tuple[str, str | None]] = []
    for article_url in ARTICLE_URLS:
        host = urllib.parse.urlsplit(article_url).netloc
        candidates.extend(
            [
                (
                    f"https://{host}/action/downloadSupplement?doi={encoded_doi}&file={encoded_file}",
                    article_url,
                ),
                (
                    f"https://{host}/action/downloadSupplement?doi={DOI}&file={filename}",
                    article_url,
                ),
            ]
        )
    candidates.extend(
        [
            (f"https://onlinelibrary.wiley.com/action/downloadSupplement?doi={encoded_doi}&file={encoded_file}", ARTICLE_URLS[1]),
            (f"https://nsojournals.onlinelibrary.wiley.com/action/downloadSupplement?doi={encoded_doi}&file={encoded_file}", ARTICLE_URLS[0]),
        ]
    )
    return list(dict.fromkeys(candidates))


def first_row(payload: bytes) -> list[str]:
    text = payload.decode("utf-8-sig", errors="replace")
    return next(csv.reader(text.splitlines()), [])


def recover_file(filename: str) -> tuple[bytes, str, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for url, referer in candidate_urls(filename):
        for method_name, method in (("urllib", _request), ("curl", _curl)):
            try:
                payload = method(url, referer)
            except Exception as error:
                attempts.append({
                    "filename": filename,
                    "url": url,
                    "method": method_name,
                    "status": "failed",
                    "error": repr(error),
                })
                continue
            valid = _looks_like_csv(payload)
            attempts.append({
                "filename": filename,
                "url": url,
                "method": method_name,
                "status": "csv_recovered" if valid else "not_csv",
                "bytes": len(payload),
                "preview": payload[:160].decode("utf-8", errors="replace"),
            })
            if valid:
                return payload, url, attempts
    raise RuntimeError(json.dumps({"message": f"could not recover {filename}", "attempts": attempts}, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    receipts: list[dict[str, object]] = []
    all_attempts: list[dict[str, object]] = []
    for filename in FILES:
        payload, source_url, attempts = recover_file(filename)
        all_attempts.extend(attempts)
        path = destination / filename
        path.write_bytes(payload)
        receipts.append({
            "filename": filename,
            "source_url": source_url,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "first_row": first_row(payload),
        })

    receipt = {
        "article_doi": DOI,
        "article_title": "Plant secondary metabolite has dose-dependent effects on bumblebees",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": receipts,
        "attempts": all_attempts,
        "interpretation_boundary": (
            "Publisher CSVs are preserved without selecting effects. Rows must still be mapped "
            "to assay, dose, experimental unit, outcome lane, B-role provenance, and study "
            "dependence before canonical use."
        ),
    }
    (destination / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
