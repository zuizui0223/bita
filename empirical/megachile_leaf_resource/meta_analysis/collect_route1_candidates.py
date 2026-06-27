"""Collect metadata candidates for Route 1: published leaf-material-use studies.

This script queries Crossref only. It deliberately does not decide whether a
paper is eligible; human screening must verify raw plant-level tables,
leaf-cut identification, and background availability.

Usage:
    python collect_route1_candidates.py route1_queries.csv route1_candidates.csv

No third-party packages are required.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CROSSREF = "https://api.crossref.org/works"
FIELDS = [
    "query_id", "query", "source", "title", "authors", "year", "doi",
    "url", "container_title", "abstract", "candidate_rank", "screen_status",
    "screen_reason", "notes",
]


def text(value: object) -> str:
    if isinstance(value, list):
        return "; ".join(str(x) for x in value)
    return str(value or "")


def fetch_crossref(query: str, rows: int) -> list[dict[str, str]]:
    params = urlencode({"query.bibliographic": query, "rows": rows, "select": "title,author,published,DOI,URL,container-title,abstract"})
    request = Request(f"{CROSSREF}?{params}", headers={"User-Agent": "biotic-interaction-trait-architecture/0.1 (research metadata screening)"})
    with urlopen(request, timeout=30) as response:  # nosec B310: fixed public API
        payload = json.load(response)
    results: list[dict[str, str]] = []
    for item in payload.get("message", {}).get("items", []):
        authors = []
        for author in item.get("author", []):
            family = author.get("family", "").strip()
            given = author.get("given", "").strip()
            authors.append(", ".join(part for part in (family, given) if part))
        dates = item.get("published", {}).get("date-parts", [[]])
        year = str(dates[0][0]) if dates and dates[0] else ""
        results.append({
            "title": text(item.get("title", [""])[0] if item.get("title") else ""),
            "authors": "; ".join(authors),
            "year": year,
            "doi": text(item.get("DOI")),
            "url": text(item.get("URL")),
            "container_title": text(item.get("container-title", [""])[0] if item.get("container-title") else ""),
            "abstract": text(item.get("abstract")),
        })
    return results


def main(query_path: str, output_path: str) -> int:
    queries = list(csv.DictReader(Path(query_path).open(encoding="utf-8")))
    seen: set[str] = set()
    output: list[dict[str, str]] = []
    for query_row in queries:
        query = query_row["query"].strip()
        if not query:
            continue
        for rank, item in enumerate(fetch_crossref(query, int(query_row.get("rows", "25") or 25)), start=1):
            key = item["doi"].lower() or item["title"].lower()
            if not key or key in seen:
                continue
            seen.add(key)
            output.append({
                "query_id": query_row.get("query_id", ""),
                "query": query,
                "source": "Crossref",
                **item,
                "candidate_rank": str(rank),
                "screen_status": "unscreened",
                "screen_reason": "",
                "notes": "",
            })
        time.sleep(1.0)
    with Path(output_path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    print(f"wrote {len(output)} unique metadata candidates to {output_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python collect_route1_candidates.py route1_queries.csv route1_candidates.csv")
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
