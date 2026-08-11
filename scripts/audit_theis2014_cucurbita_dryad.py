"""Audit the public Dryad package for Theis et al. (2014) without retaining raw rows.

The script recovers the Dryad API manifest for DOI 10.5061/dryad.1h189, downloads
only a declared set of source tables in memory, and emits schema/linkage diagnostics.
It does not fit a biological effect model and does not write observation-level data.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

DRYAD = "https://datadryad.org"
DATASET_DOI = "10.5061/dryad.1h189"
USER_AGENT = "bita-theis2014-dryad-audit/1.0"
TARGET_FILES = {
    "Volatiles ngflowerh.csv",
    "Nectar and Flower Size.csv",
    "Pollinator Observation.csv",
    "Herbivory 2005.csv",
    "Herbivory 2006.csv",
}
KEY_TOKENS = ("species", "variety", "tax", "code", "plant", "plot", "year", "date", "sex", "flower")


def _get(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"})
    with urlopen(req, timeout=30) as response:  # nosec B310: fixed public repository endpoints
        return response.read()


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


def _manifest() -> dict[str, str]:
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

    found: dict[str, str] = {}
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
            links = item.get("_links") or item.get("links") or {}
            download = ""
            if isinstance(links, dict):
                for key in ("stash:download", "download", "content"):
                    value = links.get(key, "")
                    if isinstance(value, dict):
                        value = value.get("href", "")
                    if value:
                        download = _absolute(value)
                        break
            if name and download:
                found[name] = download
        files_url = _link(payload, "next")
    return found


def _audit_csv(name: str, url: str) -> dict[str, object]:
    text = _get(url).decode("utf-8-sig", errors="replace")
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
        "n_rows": n_rows,
        "headers": headers,
        "nonempty_counts": nonempty,
        "candidate_key_distinct_values_capped_30": {h: sorted(v) for h, v in distinct.items()},
        "numeric_column_ranges": numeric_summary,
    }


def run(output_path: str | Path) -> dict[str, object]:
    manifest = _manifest()
    missing = sorted(TARGET_FILES.difference(manifest))
    if missing:
        raise RuntimeError(f"declared Dryad files missing: {missing}")
    report = {
        "study_doi": "10.3732/ajb.1400171",
        "dataset_doi": DATASET_DOI,
        "target_files": sorted(TARGET_FILES),
        "manifest_file_count": len(manifest),
        "audits": [_audit_csv(name, manifest[name]) for name in sorted(TARGET_FILES)],
        "guardrail": "Schema/linkage audit only; no observation rows retained and no effect estimated.",
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
    print(json.dumps({"manifest_file_count": result["manifest_file_count"], "audited": len(result["audits"])}, indent=2))
