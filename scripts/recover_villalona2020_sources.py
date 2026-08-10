"""Recover primary and supplementary source files for Villalona et al. 2020.

Article DOI: 10.1007/s00442-020-04701-0

This utility attempts only source URLs already identified from the author-shared
ResearchGate record or the standard Springer media-object convention. It keeps
all successful payloads with checksums and does not perform biological coding.

Usage:
    python scripts/recover_villalona2020_sources.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DOI = "10.1007/s00442-020-04701-0"
ARTICLE_REFERER = "https://link.springer.com/article/10.1007/s00442-020-04701-0"
RESEARCHGATE_REFERER = (
    "https://www.researchgate.net/publication/342958960_The_role_of_toxic_nectar_"
    "secondary_compounds_in_driving_differential_bumble_bee_preferences_for_milkweed_flowers"
)
CANDIDATES = (
    (
        "villalona2020_author_shared.pdf",
        "https://www.researchgate.net/publication/profile/Anurag-Agrawal-7/publication/"
        "342958960_The_role_of_toxic_nectar_secondary_compounds_in_driving_differential_"
        "bumble_bee_preferences_for_milkweed_flowers/links/5f3ae7f292851cd302012d2f/"
        "The-role-of-toxic-nectar-secondary-compounds-in-driving-differential-bumble-bee-"
        "preferences-for-milkweed-flowers.pdf",
        RESEARCHGATE_REFERER,
    ),
    (
        "villalona2020_springer.pdf",
        "https://link.springer.com/content/pdf/10.1007/s00442-020-04701-0.pdf",
        ARTICLE_REFERER,
    ),
    (
        "villalona2020_esm1.pdf",
        "https://static-content.springer.com/esm/art%3A10.1007%2Fs00442-020-04701-0/"
        "MediaObjects/442_2020_4701_MOESM1_ESM.pdf",
        ARTICLE_REFERER,
    ),
    (
        "villalona2020_esm1.docx",
        "https://static-content.springer.com/esm/art%3A10.1007%2Fs00442-020-04701-0/"
        "MediaObjects/442_2020_4701_MOESM1_ESM.docx",
        ARTICLE_REFERER,
    ),
    (
        "villalona2020_esm1.xlsx",
        "https://static-content.springer.com/esm/art%3A10.1007%2Fs00442-020-04701-0/"
        "MediaObjects/442_2020_4701_MOESM1_ESM.xlsx",
        ARTICLE_REFERER,
    ),
    (
        "villalona2020_esm1.zip",
        "https://static-content.springer.com/esm/art%3A10.1007%2Fs00442-020-04701-0/"
        "MediaObjects/442_2020_4701_MOESM1_ESM.zip",
        ARTICLE_REFERER,
    ),
)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"


def _curl(url: str, referer: str) -> tuple[bytes, str]:
    command = [
        "curl", "--location", "--silent", "--show-error", "--max-time", "120",
        "--user-agent", USER_AGENT, "--referer", referer,
        "--write-out", "\nBITA_HTTP_STATUS:%{http_code}\n",
        url,
    ]
    completed = subprocess.run(command, check=True, capture_output=True)
    marker = b"\nBITA_HTTP_STATUS:"
    if marker not in completed.stdout:
        raise RuntimeError("curl output lacks status marker")
    payload, status_tail = completed.stdout.rsplit(marker, 1)
    status = status_tail.strip().decode("ascii", errors="replace")
    return payload, status


def _kind(payload: bytes) -> str:
    if payload.startswith(b"%PDF"):
        return "pdf"
    if payload.startswith(b"PK"):
        return "zip_container"
    preview = payload[:1000].lstrip().lower()
    if preview.startswith((b"<!doctype html", b"<html")):
        return "html"
    return "other"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, object]] = []
    successes = 0
    for filename, url, referer in CANDIDATES:
        try:
            payload, status = _curl(url, referer)
            payload_kind = _kind(payload)
            record = {
                "filename": filename,
                "url": url,
                "http_status": status,
                "bytes": len(payload),
                "payload_kind": payload_kind,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "preview": payload[:160].decode("utf-8", errors="replace"),
            }
            if status.startswith("2") and payload_kind in {"pdf", "zip_container"}:
                (destination / filename).write_bytes(payload)
                record["saved"] = True
                successes += 1
            else:
                record["saved"] = False
            attempts.append(record)
        except Exception as error:
            attempts.append({"filename": filename, "url": url, "status": "failed", "error": repr(error)})

    receipt = {
        "article_doi": DOI,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "successful_source_files": successes,
        "attempts": attempts,
        "interpretation_boundary": (
            "Recovered files are primary-source material only. No reported mean, model output, "
            "or supplementary table is promoted to a canonical bita effect until its assay, "
            "experimental unit, outcome lane, orientation, and dependence are audited."
        ),
    }
    (destination / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if successes == 0:
        raise RuntimeError("No Villalona 2020 source file was recovered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
