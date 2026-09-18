"""Audit Aubert et al. 2026 public Dryad assets without emitting raw rows."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

DATASET_DOI = "10.5061/dryad.rn8pk0pqx"
DOWNLOAD_URL = "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.rn8pk0pqx/download"
USER_AGENT = "bita-aubert2026-dryad-audit/1.0"
MAX_BYTES = 64 * 1024 * 1024
REQUIRED = {
    "Interactions_data_Ecuador.txt",
    "Cameras_data_Ecuador.txt",
    "Plant_traits.txt",
    "script.R",
}


def _read_table(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig", errors="replace")
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = "\t"
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    rows = [dict(row) for row in reader]
    return list(reader.fieldnames or []), rows


def _basename_map(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    out: dict[str, zipfile.ZipInfo] = {}
    for item in archive.infolist():
        if item.is_dir():
            continue
        base = Path(item.filename).name
        if base in out:
            raise ValueError(f"duplicate archive basename: {base}")
        out[base] = item
    return out


def summarize_archive(data: bytes) -> dict[str, object]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = _basename_map(archive)
        missing = sorted(REQUIRED - set(members))

        report: dict[str, object] = {
            "dataset_doi": DATASET_DOI,
            "required_files_present": not missing,
            "missing_required_files": missing,
            "archive_member_count": len(members),
        }
        if missing:
            return report

        i_header, interactions = _read_table(archive.read(members["Interactions_data_Ecuador.txt"]))
        c_header, cameras = _read_table(archive.read(members["Cameras_data_Ecuador.txt"]))
        p_header, traits = _read_table(archive.read(members["Plant_traits.txt"]))
        script_text = archive.read(members["script.R"]).decode("utf-8-sig", errors="replace")

        robbing = Counter(
            str(row.get("nectar_robbing", "")).strip()
            for row in interactions
            if str(row.get("nectar_robbing", "")).strip()
        )
        sites = {
            str(row.get("site", "")).strip()
            for row in interactions
            if str(row.get("site", "")).strip()
        }

        report.update(
            {
                "interaction_rows": len(interactions),
                "camera_rows": len(cameras),
                "plant_trait_rows": len(traits),
                "interaction_columns": i_header,
                "camera_columns": c_header,
                "plant_trait_columns": p_header,
                "interaction_sites": len(sites),
                "nectar_robbing_counts": dict(sorted(robbing.items())),
                "script_present": True,
                "script_line_count": len(script_text.splitlines()),
                "guardrail": (
                    "Aggregate/schema audit only. Raw interaction, camera, plant-trait, "
                    "and script contents are not emitted."
                ),
            }
        )
        return report


def _download() -> bytes:
    request = Request(
        DOWNLOAD_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,application/octet-stream,*/*",
            "X-API-Version": "2.1.0",
        },
    )
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public Dryad DOI
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Dryad archive exceeds configured size limit")
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
                "required_files_present": result["required_files_present"],
                "interaction_rows": result.get("interaction_rows"),
                "interaction_sites": result.get("interaction_sites"),
                "nectar_robbing_counts": result.get("nectar_robbing_counts"),
            },
            indent=2,
            sort_keys=True,
        )
    )
