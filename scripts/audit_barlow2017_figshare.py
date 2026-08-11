"""Audit the public Figshare data declared by Barlow et al. (2017).

The accepted manuscript explicitly declares Figshare DOI/identifier 5165350 for
biological assay, nectar/galea alkaloid, and bumblebee-alkaloid bioassay data.
This script enumerates the public Figshare article and emits bounded file/schema
metadata only. Observation-level rows are never written to the artifact.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen

FIGSHARE_API = "https://api.figshare.com/v2"
ARTICLE_ID = 5165350
SOURCE_DOI = "10.1016/j.cub.2017.07.012"
DATA_DOI = "10.6084/m9.figshare.5165350"
USER_AGENT = "bita-barlow2017-figshare-audit/1.0"
MAX_FILE_BYTES = 50 * 1024 * 1024
TEXT_SUFFIXES = {".csv", ".tsv", ".txt"}
TOKENS = (
    "bee", "bombus", "species", "alkaloid", "aconit", "dose", "ppm", "nectar", "sucrose",
    "visit", "rob", "choice", "consume", "time", "flower", "plant", "treat", "trial", "rep",
)


def _get(url: str, *, accept: str = "application/json,*/*") -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public Figshare endpoints
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_FILE_BYTES:
            raise ValueError(f"response too large: {length}")
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("response exceeded configured byte limit")
    return data


def _json(url: str):
    return json.loads(_get(url).decode("utf-8"))


def _suffix(name: str) -> str:
    return Path(name).suffix.lower()


def _audit_text(file: dict[str, object]) -> dict[str, object]:
    name = str(file.get("name") or "")
    url = str(file.get("download_url") or "")
    result: dict[str, object] = {
        "file_id": file.get("id"),
        "file_name": name,
        "size_bytes": file.get("size"),
        "suffix": _suffix(name),
        "download_url_present": bool(url),
    }
    if not url or _suffix(name) not in TEXT_SUFFIXES:
        return result
    raw = _get(url, accept="text/csv,text/plain,*/*")
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
    nonempty = {h: 0 for h in headers}
    distinct = {h: set() for h in headers if any(token in h.lower() for token in TOKENS)}
    numeric = {h: {"n": 0, "min": None, "max": None} for h in headers}
    for row in reader:
        n_rows += 1
        for h in headers:
            value = str(row.get(h, "") or "").strip()
            if not value:
                continue
            nonempty[h] += 1
            if h in distinct and len(distinct[h]) < 40:
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
        "delimiter": "tab" if delimiter == "\t" else delimiter,
        "n_rows": n_rows,
        "headers": headers,
        "candidate_columns": [h for h in headers if any(token in h.lower() for token in TOKENS)],
        "candidate_distinct_values_capped_40": {h: sorted(values) for h, values in distinct.items()},
        "nonempty_counts": nonempty,
        "numeric_ranges": {h: v for h, v in numeric.items() if v["n"] > 0},
    })
    return result


def run(output_path: str | Path) -> dict[str, object]:
    article = _json(f"{FIGSHARE_API}/articles/{ARTICLE_ID}")
    files = article.get("files") if isinstance(article, dict) else []
    if not isinstance(files, list):
        files = []
    report = {
        "source_doi": SOURCE_DOI,
        "declared_data_doi": DATA_DOI,
        "figshare_article_id": ARTICLE_ID,
        "title": article.get("title") if isinstance(article, dict) else None,
        "doi": article.get("doi") if isinstance(article, dict) else None,
        "resource_doi": article.get("resource_doi") if isinstance(article, dict) else None,
        "resource_title": article.get("resource_title") if isinstance(article, dict) else None,
        "file_count": len(files),
        "files": [_audit_text(item) for item in files if isinstance(item, dict)],
        "guardrails": [
            "No observation-level rows are written to the report.",
            "This is source/schema adjudication only; no biological coefficient is fitted here.",
            "Any later model must be predeclared from the primary article before reading outcome values for result selection.",
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
    print(json.dumps({"file_count": result["file_count"], "title": result["title"]}, indent=2))
