"""Audit article-declared EDMOND data for Kessler et al. (2019).

EDMOND is a Dataverse deployment. The article declares persistent DOI
10.17617/3.24. This script retrieves dataset metadata through the public Dataverse
API and inspects bounded public tabular files in memory. It writes only file/schema
summaries, never observation rows.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = "https://edmond.mpg.de"
PERSISTENT_ID = "doi:10.17617/3.24"
SOURCE_DOI = "10.1111/1365-2435.13332"
USER_AGENT = "bita-kessler2019-edmond-audit/1.0"
MAX_FILE_BYTES = 50 * 1024 * 1024
TABULAR_SUFFIXES = {".csv", ".tsv", ".txt"}
TOKENS = (
    "year", "genotype", "chal", "ev", "plant", "flower", "damage", "beetle", "diabrotica",
    "infest", "choice", "feeding", "time", "ba", "benzyl", "eag", "dose", "concentration",
)


def _get(url: str, *, accept: str = "application/json,*/*") -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public repository/API endpoints
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_FILE_BYTES:
            raise ValueError(f"response too large for bounded audit: {length}")
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("response exceeded configured byte limit")
    return data


def _json(url: str):
    return json.loads(_get(url).decode("utf-8"))


def _suffix(name: str) -> str:
    return Path(name).suffix.lower()


def _dataset() -> dict:
    encoded = quote(PERSISTENT_ID, safe="")
    url = f"{BASE}/api/datasets/:persistentId/?persistentId={encoded}"
    payload = _json(url)
    if payload.get("status") != "OK" or not isinstance(payload.get("data"), dict):
        raise RuntimeError(f"EDMOND dataset API failed: {payload.get('status')}")
    return payload["data"]


def _files(dataset: dict) -> list[dict]:
    version = dataset.get("latestVersion")
    if not isinstance(version, dict):
        raise RuntimeError("EDMOND dataset has no latestVersion object")
    files = version.get("files")
    if not isinstance(files, list):
        raise RuntimeError("EDMOND latestVersion has no files list")
    return [item for item in files if isinstance(item, dict)]


def _file_record(item: dict) -> dict[str, object]:
    data_file = item.get("dataFile") if isinstance(item.get("dataFile"), dict) else {}
    file_id = data_file.get("id")
    name = str(data_file.get("filename") or "")
    content_type = str(data_file.get("contentType") or "")
    result: dict[str, object] = {
        "file_id": file_id,
        "file_name": name,
        "content_type": content_type,
        "size_bytes": data_file.get("filesize"),
        "restricted": bool(data_file.get("restricted", False)),
        "description": item.get("description"),
        "categories": item.get("categories") if isinstance(item.get("categories"), list) else [],
        "suffix": _suffix(name),
    }
    if not isinstance(file_id, int) or result["restricted"] or _suffix(name) not in TABULAR_SUFFIXES:
        return result
    raw = _get(f"{BASE}/api/access/datafile/{file_id}", accept="text/csv,text/plain,*/*")
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = "\t" if sample.count("\t") > sample.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    n_rows = 0
    distinct = {h: set() for h in headers if any(token in h.lower() for token in TOKENS)}
    numeric = {h: {"n": 0, "min": None, "max": None} for h in headers}
    nonempty = {h: 0 for h in headers}
    for row in reader:
        n_rows += 1
        for h in headers:
            value = str(row.get(h, "") or "").strip()
            if not value:
                continue
            nonempty[h] += 1
            if h in distinct and len(distinct[h]) < 50:
                distinct[h].add(value)
            try:
                x = float(value)
            except ValueError:
                continue
            state = numeric[h]
            state["n"] += 1
            state["min"] = x if state["min"] is None else min(state["min"], x)
            state["max"] = x if state["max"] is None else max(state["max"], x)
    result.update({
        "n_rows": n_rows,
        "delimiter": "tab" if delimiter == "\t" else delimiter,
        "headers": headers,
        "candidate_columns": [h for h in headers if any(token in h.lower() for token in TOKENS)],
        "candidate_distinct_values_capped_50": {h: sorted(values) for h, values in distinct.items()},
        "nonempty_counts": nonempty,
        "numeric_ranges": {h: value for h, value in numeric.items() if value["n"] > 0},
    })
    return result


def run(output_path: str | Path) -> dict[str, object]:
    dataset = _dataset()
    version = dataset.get("latestVersion") if isinstance(dataset.get("latestVersion"), dict) else {}
    files = _files(dataset)
    report = {
        "source_doi": SOURCE_DOI,
        "dataset_persistent_id": PERSISTENT_ID,
        "dataset_id": dataset.get("id"),
        "dataset_title": version.get("metadataBlocks", {}).get("citation", {}).get("fields", []) if isinstance(version, dict) else None,
        "version_number": f"{version.get('versionNumber')}.{version.get('versionMinorNumber')}" if isinstance(version, dict) else None,
        "file_count": len(files),
        "files": [_file_record(item) for item in files],
        "guardrails": [
            "Observation-level rows are processed in memory and never written.",
            "This audit does not fit biological models.",
            "A later effect reconstruction requires a predeclared source-aligned outcome and exact treatment/genotype sample counts.",
        ],
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
    print(json.dumps({"dataset_id": result["dataset_id"], "file_count": result["file_count"]}, indent=2))
