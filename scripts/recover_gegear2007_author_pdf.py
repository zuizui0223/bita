"""Recover the author-hosted Gegear, Manson & Thomson (2007) PDF.

This utility downloads one already-identified primary source. It does not search
for studies, extract an effect, or alter any inclusion rule. The output is a PDF
plus a provenance receipt for source-level audit.

Usage:
    python scripts/recover_gegear2007_author_pdf.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DOI = "10.1111/j.1461-0248.2007.01027.x"
AUTHOR_PAGE = "https://thomson.eeb.utoronto.ca/publications/"
PDF_URL = (
    "https://thomson.eeb.utoronto.ca/wp-content/blogs.dir/73/files/sites/16/2024/04/"
    "Gegear-Manson-Thomson-2007-Ecological-context-influences-pollinator-deterrence-"
    "by-alkaloids-in-floral-nectar-Ecology-Letters.pdf"
)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"


def urllib_download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,*/*",
            "Referer": AUTHOR_PAGE,
        },
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def curl_download(url: str) -> bytes:
    result = subprocess.run(
        [
            "curl", "--fail", "--location", "--silent", "--show-error",
            "--max-time", "120", "--user-agent", USER_AGENT,
            "--header", "Accept: application/pdf,*/*",
            "--referer", AUTHOR_PAGE,
            url,
        ],
        check=True,
        capture_output=True,
    )
    return result.stdout


def recover() -> tuple[bytes, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for method, function in (("urllib", urllib_download), ("curl", curl_download)):
        try:
            payload = function(PDF_URL)
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append({"method": method, "status": "failed", "error": repr(error)})
            continue
        attempts.append({"method": method, "status": "retrieved", "bytes": len(payload)})
        if payload.startswith(b"%PDF"):
            return payload, attempts
        attempts[-1]["status"] = "not_pdf"
        attempts[-1]["preview"] = payload[:200].decode("utf-8", errors="replace")
    raise RuntimeError(json.dumps({"message": "author PDF not recovered", "attempts": attempts}, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload, attempts = recover()
    pdf_path = output_dir / "gegear_manson_thomson_2007.pdf"
    pdf_path.write_bytes(payload)
    receipt = {
        "article_doi": DOI,
        "article_title": "Ecological context influences pollinator deterrence by alkaloids in floral nectar",
        "author_publication_page": AUTHOR_PAGE,
        "source_url": PDF_URL,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "attempts": attempts,
        "interpretation_boundary": (
            "Primary source recovery only. Numerical effects require separate source-level "
            "identification of experiment, treatment, comparator, experimental unit, outcome, "
            "and uncertainty."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
