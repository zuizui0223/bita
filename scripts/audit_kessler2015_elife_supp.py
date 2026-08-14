"""Audit public eLife supplementary assets for Kessler et al. (2015).

The focal article fully crosses floral scent production and nectar production.
This script retrieves the article's public supplementary ZIP and reports only
member names and table schemas. It does not retain or emit observation-level rows.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

ARTICLE_DOI = "10.7554/eLife.07641"
SUPP_URL = "https://cdn.elifesciences.org/articles/07641/elife-07641-supp-v1.zip"
USER_AGENT = "bita-kessler2015-supp-audit/1.0"
MAX_BYTES = 100 * 1024 * 1024


def _download() -> bytes:
    req = Request(SUPP_URL, headers={"User-Agent": USER_AGENT, "Accept": "application/zip,*/*"})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public eLife asset
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("supplementary archive exceeds configured size limit")
    return data


def _csv_header(data: bytes) -> list[str]:
    text = data.decode("utf-8-sig", errors="replace")
    return list(csv.reader(io.StringIO(text)).__next__())


def run(output_path: str | Path) -> dict[str, object]:
    archive = zipfile.ZipFile(io.BytesIO(_download()))
    members = []
    for item in sorted(archive.infolist(), key=lambda x: x.filename):
        if item.is_dir():
            continue
        suffix = Path(item.filename).suffix.lower()
        record: dict[str, object] = {
            "file_name": item.filename,
            "size_bytes": item.file_size,
            "suffix": suffix,
        }
        if suffix in {".csv", ".tsv", ".txt"} and item.file_size <= 10 * 1024 * 1024:
            prefix = archive.read(item)
            if suffix == ".csv":
                try:
                    record["header"] = _csv_header(prefix)
                except Exception as error:
                    record["header_error"] = f"{type(error).__name__}: {error}"
            else:
                first = prefix.decode("utf-8-sig", errors="replace").splitlines()[:1]
                record["first_line"] = first[0] if first else ""
        members.append(record)
    report = {
        "article_doi": ARTICLE_DOI,
        "supplement_url": SUPP_URL,
        "member_count": len(members),
        "members": members,
        "target_design": "RNAi 2x2: scent present/absent x nectar present/absent",
        "guardrail": "Asset/schema audit only. No raw rows are written and no direct A x D effect is promoted without a defensible D orientation and uncertainty-bearing contrast.",
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({"member_count": result["member_count"]}, indent=2))
