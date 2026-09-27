"""Fetch the frozen Q1-Q8 direct access-geometry bibliographic frame from OpenAlex.

This is outcome-blind. It executes the exact frozen Boolean query strings against
OpenAlex works search, paginates every result through the frozen publication-date
window, and writes provider-native JSON plus the required count manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://api.openalex.org/works"
FROM_DATE = "2000-01-01"
THROUGH_DATE = "2026-09-24"
PER_PAGE = 100

QUERIES = {
    "Q1": '("nectar robbing" OR "floral larceny") AND "corolla length"',
    "Q2": '"nectar robbery" AND "corolla length"',
    "Q3": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("tube length" OR "tube depth")',
    "Q4": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("flower size" OR "flower width")',
    "Q5": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("floral morphology" OR "nectar accessibility" OR "trait mismatch")',
    "Q6": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("tongue length" OR proboscis OR glossa OR "bill length")',
    "Q7": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("morphological constraint" OR "morphological constraints" OR "short-tongued")',
    "Q8": '("nectar robbing" OR "nectar robbery" OR "floral larceny") AND ("switch to robbing" OR "switching to robbing" OR "shortened corolla")',
}

SELECT = "id,doi,title,display_name,publication_year,authorships,primary_location"


def _get_json(params: dict[str, str], *, attempts: int = 6) -> tuple[dict, str]:
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "bita-formal-bibliographic-frame/1.0",
            "Accept": "application/json",
        },
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return payload, url
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504}:
                raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
        time.sleep(min(60, 2 ** attempt))
    assert last_error is not None
    raise last_error


def fetch_query(query_id: str, query: str) -> tuple[dict, dict]:
    cursor = "*"
    results: list[dict] = []
    reported_count: int | None = None
    request_urls: list[str] = []

    while cursor:
        payload, url = _get_json({
            "search": query,
            "filter": f"from_publication_date:{FROM_DATE},to_publication_date:{THROUGH_DATE}",
            "per-page": str(PER_PAGE),
            "cursor": cursor,
            "select": SELECT,
        })
        request_urls.append(url)
        meta = payload.get("meta")
        page = payload.get("results")
        if not isinstance(meta, dict) or not isinstance(page, list):
            raise RuntimeError(f"{query_id}: malformed OpenAlex response")
        if reported_count is None:
            reported_count = int(meta["count"])
        elif int(meta["count"]) != reported_count:
            raise RuntimeError(f"{query_id}: result count changed during cursor paging")

        results.extend(page)
        next_cursor = meta.get("next_cursor")
        if not page:
            cursor = ""
        else:
            cursor = str(next_cursor or "")

    if reported_count is None:
        raise RuntimeError(f"{query_id}: no OpenAlex response")
    if reported_count <= 0:
        raise RuntimeError(f"{query_id}: zero-result query requires protocol amendment")
    if len(results) != reported_count:
        raise RuntimeError(
            f"{query_id}: incomplete export reported={reported_count} fetched={len(results)}"
        )

    ids = [str(row.get("id") or "") for row in results]
    if any(not value for value in ids):
        raise RuntimeError(f"{query_id}: OpenAlex result missing id")
    if len(ids) != len(set(ids)):
        raise RuntimeError(f"{query_id}: duplicate OpenAlex IDs within query")

    output = {
        "meta": {
            "count": reported_count,
            "source_db": "OpenAlex",
            "query_id": query_id,
            "query": query,
            "from_publication_date": FROM_DATE,
            "through_publication_date": THROUGH_DATE,
            "cursor_pages": len(request_urls),
        },
        "results": results,
    }
    receipt = {
        "query_id": query_id,
        "query": query,
        "reported_total_rows": reported_count,
        "fetched_rows": len(results),
        "pages": len(request_urls),
    }
    return output, receipt


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(output_dir: Path, search_date: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    receipts = []
    count_rows = []

    for query_id, query in QUERIES.items():
        payload, receipt = fetch_query(query_id, query)
        path = output_dir / f"{query_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
        receipt["sha256"] = _sha256(path)
        receipts.append(receipt)
        count_rows.append({
            "query_id": query_id,
            "source_db": "OpenAlex",
            "reported_total_rows": str(receipt["reported_total_rows"]),
            "search_date": search_date,
        })

    count_path = output_dir / "QUERY_COUNTS.csv"
    with count_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("query_id", "source_db", "reported_total_rows", "search_date"),
        )
        writer.writeheader()
        writer.writerows(count_rows)

    report = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_OPENALEX_FETCH_V1",
        "status": "COMPLETE_OUTCOME_BLIND_Q1_Q8_OPENALEX_EXPORT",
        "source_db": "OpenAlex",
        "search_date": search_date,
        "publication_window": [FROM_DATE, THROUGH_DATE],
        "query_contract": QUERIES,
        "queries": receipts,
        "count_manifest_sha256": _sha256(count_path),
        "outcome_direction_inspected": False,
    }
    (output_dir / "OPENALEX_FETCH_RECEIPT_V1.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--search-date", required=True)
    args = parser.parse_args()
    report = run(args.output_dir, args.search_date)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
