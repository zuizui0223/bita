"""Audit the public EPHI Zenodo mirror used to reconstruct Aubert et al. 2026.

Aggregate/schema output only. Raw rows are never emitted.
"""

from __future__ import annotations

import csv
import io
import json
import urllib.request
from urllib.parse import quote
from collections import Counter
from pathlib import Path

BASE = "https://zenodo.org/records/14185547/files"
FILES = {
    "interactions": "Interactions_data_Ecuador.txt",
    "cameras": "Cameras_data_Ecuador.txt",
    "plants": "Plant_traits.txt",
    "birds": "Hummingbird_traits.txt",
}
METADATA_FILES = {
    "metadata_interactions": "Metadata EPHI interactions.csv",
    "metadata_plants": "Metadata EPHI plant traits.csv",
    "metadata_birds": "Metadata EPHI hummingbird traits.csv",
}
USER_AGENT = "bita-aubert-zenodo-mirror-audit/1.0"


def _download(name: str) -> bytes:
    url = f"{BASE}/{quote(name)}?download=1"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as response:  # nosec B310 fixed public Zenodo URL
        return response.read()


def _read(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
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


def summarize_tables(tables: dict[str, tuple[list[str], list[dict[str, str]]]]) -> dict[str, object]:
    out: dict[str, object] = {
        "source": "EPHI Zenodo 10.5281/zenodo.14185547",
        "tables": {},
        "guardrail": "Aggregate/schema audit only; no raw rows are emitted.",
    }
    for key, (header, rows) in tables.items():
        entry: dict[str, object] = {"rows": len(rows), "columns": header}
        if key == "interactions":
            entry["sites"] = sorted({
                str(row.get("site", "")).strip()
                for row in rows
                if str(row.get("site", "")).strip()
            })
            entry["site_count"] = len(entry["sites"])
            rob_field = "nectar_robbing" if "nectar_robbing" in header else "piercing"
            fam_field = "bird_family" if "bird_family" in header else "hummingbird_family"
            entry["robbing_field"] = rob_field
            entry["nectar_robbing_counts"] = dict(sorted(Counter(
                str(row.get(rob_field, "")).strip()
                for row in rows
                if str(row.get(rob_field, "")).strip()
            ).items()))
            entry["bird_family_field"] = fam_field
            entry["bird_family_counts"] = dict(sorted(Counter(
                str(row.get(fam_field, "")).strip()
                for row in rows
                if str(row.get(fam_field, "")).strip()
            ).items()))
        out["tables"][key] = entry
    return out


def _metadata_matches(data: bytes, terms: tuple[str, ...]) -> list[str]:
    text = data.decode("utf-8-sig", errors="replace")
    matches = []
    for line in text.splitlines():
        low = line.lower()
        if any(term.lower() in low for term in terms):
            matches.append(line.strip())
    return matches


def run(output: str | Path) -> dict[str, object]:
    tables = {}
    for key, name in FILES.items():
        tables[key] = _read(_download(name))
    result = summarize_tables(tables)
    result["metadata_matches"] = {}
    terms = ("piercing", "culmen_length", "bill_length", "Tubelength")
    for key, name in METADATA_FILES.items():
        result["metadata_matches"][key] = _metadata_matches(_download(name), terms)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
