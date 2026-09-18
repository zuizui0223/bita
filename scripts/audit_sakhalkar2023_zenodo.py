"""Audit Sakhalkar et al. 2023 public Zenodo archive without emitting raw rows."""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

DATASET_DOI = "10.5281/zenodo.8398202"
DOWNLOAD_URL = (
    "https://zenodo.org/records/8398202/files/"
    "SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip?download=1"
)
USER_AGENT = "bita-sakhalkar2023-zenodo-audit/1.0"
MAX_BYTES = 8 * 1024 * 1024


def summarize_archive(data: bytes) -> dict[str, object]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        names = sorted(item.filename for item in members)
        csv_files = sorted(name for name in names if name.lower().endswith(".csv"))
        r_files = sorted(name for name in names if name.lower().endswith(".r"))
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
                "r_files": result["r_files"],
                "readme_files": result["readme_files"],
            },
            indent=2,
            sort_keys=True,
        )
    )
