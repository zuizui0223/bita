"""Audit the public Figshare collection linked by Theis & Adler (2012).

The publisher declares collection DOI 10.6084/m9.figshare.c.3304428. This script
uses only the public Figshare v2 API, enumerates collection articles/files, and
recovers bounded schemas from tabular files. Observation-level rows are never
written to repository or Actions artifacts.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen

API = "https://api.figshare.com/v2"
COLLECTION_ID = 3304428
COLLECTION_DOI = "10.6084/m9.figshare.c.3304428"
ARTICLE_DOI = "10.1890/11-0825.1"
USER_AGENT = "bita-theis2012-figshare-audit/1.0"
MAX_FILE_BYTES = 40 * 1024 * 1024
TABULAR = {".csv", ".tsv", ".txt"}
KEY_TOKENS = ("plant", "plot", "block", "treat", "fragrance", "scent", "beetle", "poll", "seed", "fruit", "flower")


def _get(url: str, *, accept: str = "application/json,*/*") -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public Figshare API/file URLs
        size = response.headers.get("Content-Length")
        if size and int(size) > MAX_FILE_BYTES:
            raise ValueError(f"response too large for bounded audit: {size}")
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("response exceeded configured byte limit")
    return data


def _json(url: str):
    return json.loads(_get(url).decode("utf-8"))


def _suffix(name: str) -> str:
    return Path(name).suffix.lower()


def _audit_text_file(file: dict[str, object]) -> dict[str, object]:
    name = str(file.get("name") or "")
    url = str(file.get("download_url") or "")
    result: dict[str, object] = {
        "file_id": file.get("id"),
        "file_name": name,
        "size_bytes": file.get("size"),
        "download_url_present": bool(url),
        "suffix": _suffix(name),
    }
    if not url or _suffix(name) not in TABULAR:
        return result
    raw = _get(url, accept="text/csv,text/plain,*/*")
    text = raw.decode("utf-8-sig", errors="replace")
    first = text.splitlines()[:1]
    if not first:
        result["schema_status"] = "empty_file"
        return result
    delimiter = "\t" if _suffix(name) == ".tsv" or first[0].count("\t") > first[0].count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    result["schema_status"] = "header_recovered"
    result["delimiter"] = "tab" if delimiter == "\t" else "comma"
    result["headers"] = headers
    result["candidate_columns"] = [h for h in headers if any(t in h.lower() for t in KEY_TOKENS)]
    n_rows = 0
    nonempty = {h: 0 for h in headers}
    numeric = {h: {"n": 0, "min": None, "max": None} for h in headers}
    for row in reader:
        n_rows += 1
        for h in headers:
            value = str(row.get(h, "") or "").strip()
            if not value:
                continue
            nonempty[h] += 1
            try:
                x = float(value)
            except ValueError:
                continue
            state = numeric[h]
            state["n"] += 1
            state["min"] = x if state["min"] is None else min(state["min"], x)
            state["max"] = x if state["max"] is None else max(state["max"], x)
    result["n_rows"] = n_rows
    result["nonempty_counts"] = nonempty
    result["numeric_ranges"] = {h: v for h, v in numeric.items() if v["n"] > 0}
    return result


def run(output_path: str | Path) -> dict[str, object]:
    collection = _json(f"{API}/collections/{COLLECTION_ID}")
    articles = _json(f"{API}/collections/{COLLECTION_ID}/articles?page_size=100")
    article_reports = []
    for light in articles:
        article_id = light.get("id")
        detail = _json(f"{API}/articles/{article_id}")
        files = detail.get("files") if isinstance(detail, dict) else []
        file_reports = [_audit_text_file(f) for f in files] if isinstance(files, list) else []
        article_reports.append({
            "id": article_id,
            "title": detail.get("title") if isinstance(detail, dict) else light.get("title"),
            "doi": detail.get("doi") if isinstance(detail, dict) else None,
            "url_public_api": detail.get("url_public_api") if isinstance(detail, dict) else None,
            "file_count": len(files) if isinstance(files, list) else 0,
            "files": file_reports,
        })
    report = {
        "source_article_doi": ARTICLE_DOI,
        "collection_id": COLLECTION_ID,
        "collection_doi": COLLECTION_DOI,
        "collection_title": collection.get("title") if isinstance(collection, dict) else None,
        "resource_doi": collection.get("resource_doi") if isinstance(collection, dict) else None,
        "resource_title": collection.get("resource_title") if isinstance(collection, dict) else None,
        "article_count": len(article_reports),
        "articles": article_reports,
        "guardrail": "Public Figshare source audit only. Raw observations are processed in memory and never emitted; no effect is registered until design, denominator/unit, and uncertainty are source-verified.",
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
    print(json.dumps({"article_count": result["article_count"]}, indent=2))
