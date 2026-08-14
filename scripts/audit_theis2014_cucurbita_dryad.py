"""Audit the public Dryad package for Theis et al. (2014) without retaining raw rows.

Dryad file-level download links can reject automated requests even when the public
version archive is available. This script therefore uses the API only to identify
the dataset/version and manifest, then downloads the version ZIP in memory. It
emits schema/linkage diagnostics for a fixed set of source tables and writes no
observation-level data.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

DRYAD = "https://datadryad.org"
DATASET_DOI = "10.5061/dryad.1h189"
LANDING_PAGE = f"https://doi.org/{DATASET_DOI}"
USER_AGENT = "bita-theis2014-dryad-audit/1.2"
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
TARGET_FILES = {
    "Volatiles ngflowerh.csv",
    "Nectar and Flower Size.csv",
    "Pollinator Observation.csv",
    "Herbivory 2005.csv",
    "Herbivory 2006.csv",
}
KEY_TOKENS = ("species", "variety", "tax", "code", "plant", "plot", "year", "date", "sex", "flower")


def _get(url: str, *, accept: str = "application/json,*/*", referer: str = "") -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if referer:
        headers["Referer"] = referer
    req = Request(url, headers=headers)
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public repository endpoints
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_ARCHIVE_BYTES:
            raise ValueError(f"response exceeds configured byte limit: {length}")
        content = response.read(MAX_ARCHIVE_BYTES + 1)
    if len(content) > MAX_ARCHIVE_BYTES:
        raise ValueError("response exceeded configured byte limit")
    return content


def _json(url: str):
    return json.loads(_get(url).decode("utf-8"))


def _absolute(value: object) -> str:
    text = str(value or "").strip()
    return urljoin(DRYAD, text) if text else ""


def _link(payload: dict, relation: str) -> str:
    links = payload.get("_links") or payload.get("links") or {}
    value = links.get(relation, "") if isinstance(links, dict) else ""
    if isinstance(value, dict):
        value = value.get("href", "")
    return _absolute(value)


def _manifest_and_version() -> tuple[set[str], str]:
    encoded = quote(f"doi:{DATASET_DOI}", safe="")
    dataset_url = f"{DRYAD}/api/v2/datasets/{encoded}"
    dataset = _json(dataset_url)
    version_url = _link(dataset, "stash:version")
    if not version_url:
        raise RuntimeError("Dryad dataset has no stash:version link")
    version = _json(version_url)
    files_url = _link(version, "stash:files") or _link(dataset, "stash:files")
    if not files_url:
        raise RuntimeError("Dryad dataset/version has no stash:files link")

    found: set[str] = set()
    visited: set[str] = set()
    while files_url and files_url not in visited:
        visited.add(files_url)
        payload = _json(files_url)
        embedded = payload.get("_embedded") if isinstance(payload, dict) else None
        items = []
        if isinstance(embedded, dict):
            for value in embedded.values():
                if isinstance(value, list):
                    items.extend(item for item in value if isinstance(item, dict))
        for item in items:
            name = str(item.get("path") or item.get("filename") or item.get("name") or "").strip()
            if name:
                found.add(name)
        files_url = _link(payload, "next")
    return found, version_url


def _archive(version_url: str) -> zipfile.ZipFile:
    archive_url = f"{version_url}/download"
    content = _get(
        archive_url,
        accept="application/zip,application/octet-stream,*/*",
        referer=LANDING_PAGE,
    )
    return zipfile.ZipFile(io.BytesIO(content))


def _member_map(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    result: dict[str, zipfile.ZipInfo] = {}
    for member in archive.infolist():
        if member.is_dir():
            continue
        basename = member.filename.rsplit("/", 1)[-1]
        result.setdefault(basename, member)
    return result


def _audit_csv(name: str, archive: zipfile.ZipFile, member: zipfile.ZipInfo) -> dict[str, object]:
    text = archive.read(member).decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    headers = list(reader.fieldnames or [])
    n_rows = 0
    distinct: dict[str, set[str]] = {
        h: set() for h in headers if any(token in h.lower() for token in KEY_TOKENS)
    }
    nonempty = {h: 0 for h in headers}
    numeric = {h: {"n": 0, "min": None, "max": None} for h in headers}
    for row in reader:
        n_rows += 1
        for h in headers:
            value = str(row.get(h, "") or "").strip()
            if value:
                nonempty[h] += 1
                if h in distinct and len(distinct[h]) < 30:
                    distinct[h].add(value)
                try:
                    x = float(value)
                except ValueError:
                    continue
                state = numeric[h]
                state["n"] += 1
                state["min"] = x if state["min"] is None else min(state["min"], x)
                state["max"] = x if state["max"] is None else max(state["max"], x)
    numeric_summary = {h: v for h, v in numeric.items() if v["n"] > 0}
    return {
        "file": name,
        "archive_member": member.filename,
        "n_rows": n_rows,
        "headers": headers,
        "nonempty_counts": nonempty,
        "candidate_key_distinct_values_capped_30": {h: sorted(v) for h, v in distinct.items()},
        "numeric_column_ranges": numeric_summary,
    }


def run(output_path: str | Path) -> dict[str, object]:
    manifest, version_url = _manifest_and_version()
    manifest_basenames = {name.rsplit("/", 1)[-1] for name in manifest}
    missing_manifest = sorted(TARGET_FILES.difference(manifest_basenames))
    if missing_manifest:
        raise RuntimeError(f"declared Dryad files missing from manifest: {missing_manifest}")
    archive = _archive(version_url)
    members = _member_map(archive)
    archive_member_names = sorted(m.filename for m in archive.infolist() if not m.is_dir())
    missing_archive = sorted(TARGET_FILES.difference(members))
    if missing_archive:
        raise RuntimeError(f"declared Dryad files missing from version archive: {missing_archive}")
    report = {
        "study_doi": "10.3732/ajb.1400171",
        "dataset_doi": DATASET_DOI,
        "dryad_version_url": version_url,
        "archive_url": f"{version_url}/download",
        "target_files": sorted(TARGET_FILES),
        "manifest_file_count": len(manifest),
        "manifest_file_names": sorted(manifest),
        "archive_member_count": len(archive_member_names),
        "archive_member_names": archive_member_names,
        "audits": [_audit_csv(name, archive, members[name]) for name in sorted(TARGET_FILES)],
        "guardrail": "Schema/linkage audit only; public version archive read in memory, no observation rows retained, and no effect estimated.",
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
    print(json.dumps({
        "manifest_file_count": result["manifest_file_count"],
        "archive_member_count": result["archive_member_count"],
        "audited": len(result["audits"]),
    }, indent=2))
