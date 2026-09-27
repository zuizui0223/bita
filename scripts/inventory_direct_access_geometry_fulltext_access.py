"""Inventory full-text access routes for pending formal-frame candidates.

The inventory is direction-blind. It reads only bibliographic/provider access
metadata and does not inspect effect estimates or geometry-robbery direction.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.bootstrap_direct_access_geometry_bibliographic_screen import FRAME_FIELDS
from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.screen_direct_access_geometry_openalex_title_abstract import _openalex_ids

OUTPUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "query_ids",
    "openalex_ids",
    "oa_statuses",
    "pdf_urls",
    "landing_urls",
    "frame_source_urls",
    "retrieval_priority",
    "notes",
)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _get_json(url: str, attempts: int = 6) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "bita-formal-fulltext-access-inventory/1.0",
            "Accept": "application/json",
        },
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504}:
                raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
        time.sleep(min(30, 2 ** attempt))
    assert last_error is not None
    raise last_error


def _fetch_works(
    work_ids: list[str],
    batch_size: int = 50,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    output: dict[str, dict[str, Any]] = {}
    missing_ids: list[str] = []
    ids = sorted(set(work_ids))
    for start in range(0, len(ids), batch_size):
        chunk = ids[start:start + batch_size]
        params = {
            "filter": "openalex_id:" + "|".join(chunk),
            "per-page": "100",
            "select": (
                "id,doi,title,open_access,best_oa_location,"
                "primary_location,locations"
            ),
        }
        payload = _get_json(
            "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        )
        results = payload.get("results")
        if not isinstance(results, list):
            raise RuntimeError("FT_ACCESS_OPENALEX_RESULTS_MALFORMED")
        for row in results:
            if not isinstance(row, dict):
                continue
            oid = str(row.get("id") or "").removeprefix("https://openalex.org/")
            if oid:
                output[oid] = row
        missing = sorted(set(chunk) - set(output))
        missing_ids.extend(missing)
        time.sleep(0.12)
    return output, sorted(set(missing_ids))


def _location_urls(work: dict[str, Any]) -> tuple[set[str], set[str]]:
    pdfs: set[str] = set()
    landings: set[str] = set()

    candidates = []
    for key in ("best_oa_location", "primary_location"):
        value = work.get(key)
        if isinstance(value, dict):
            candidates.append(value)
    locations = work.get("locations")
    if isinstance(locations, list):
        candidates.extend(x for x in locations if isinstance(x, dict))

    for loc in candidates:
        pdf = str(loc.get("pdf_url") or "").strip()
        landing = str(loc.get("landing_page_url") or "").strip()
        if pdf:
            pdfs.add(pdf)
        if landing:
            landings.add(landing)
    return pdfs, landings


def run(
    frame_path: Path,
    decisions_path: Path,
    output_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    frame_fields, frame_rows = _read(frame_path)
    decision_fields, decisions = _read(decisions_path)
    if frame_fields != FRAME_FIELDS:
        raise ValueError("FT_ACCESS_FRAME_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("FT_ACCESS_DECISION_SCHEMA_MISMATCH")

    frame_by_id = {row["frame_id"].strip(): row for row in frame_rows}
    pending = [
        row for row in decisions
        if row["decision_status"].strip() == "PENDING_FULLTEXT"
    ]

    pending_ids: dict[str, list[str]] = {}
    all_ids: list[str] = []
    for row in pending:
        fid = row["frame_id"].strip()
        frame = frame_by_id[fid]
        if frame["source_dbs"].strip() != "OpenAlex":
            raise ValueError(f"FT_ACCESS_NON_OPENALEX_PENDING:{fid}")
        ids = _openalex_ids(frame["source_record_ids"])
        pending_ids[fid] = ids
        all_ids.extend(ids)

    work_map, missing_provider_ids = _fetch_works(all_ids)
    missing_provider_set = set(missing_provider_ids)
    output: list[dict[str, str]] = []
    priorities: Counter[str] = Counter()
    oa_status_counter: Counter[str] = Counter()

    for decision in pending:
        fid = decision["frame_id"].strip()
        frame = frame_by_id[fid]
        pdfs: set[str] = set()
        landings: set[str] = set()
        oa_statuses: set[str] = set()

        missing_here = [
            oid for oid in pending_ids[fid] if oid in missing_provider_set
        ]
        for oid in pending_ids[fid]:
            work = work_map.get(oid)
            if work is None:
                continue
            work_pdfs, work_landings = _location_urls(work)
            pdfs |= work_pdfs
            landings |= work_landings
            oa = work.get("open_access")
            if isinstance(oa, dict):
                status = str(oa.get("oa_status") or "").strip()
                if status:
                    oa_statuses.add(status)

        if missing_here:
            priority = "PROVIDER_RECORD_MISSING"
        elif pdfs:
            priority = "OA_PDF_AVAILABLE"
        elif landings:
            priority = "LANDING_OR_DOI_ONLY"
        elif decision["doi"].strip() or frame["source_urls"].strip():
            priority = "DOI_OR_FRAME_URL_ONLY"
        else:
            priority = "NO_PROVIDER_ACCESS_URL"

        priorities[priority] += 1
        for status in oa_statuses or {"unknown"}:
            oa_status_counter[status] += 1

        output.append(
            {
                "frame_id": fid,
                "doi": decision["doi"].strip(),
                "title": decision["title"].strip(),
                "year": decision["year"].strip(),
                "query_ids": decision["query_ids"].strip(),
                "openalex_ids": "|".join(pending_ids[fid]),
                "oa_statuses": "|".join(sorted(oa_statuses)),
                "pdf_urls": "|".join(sorted(pdfs)),
                "landing_urls": "|".join(sorted(landings)),
                "frame_source_urls": frame["source_urls"].strip(),
                "retrieval_priority": priority,
                "notes": "DIRECTION_NOT_INSPECTED",
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FULLTEXT_ACCESS_INVENTORY_V1",
        "status": "FULLTEXT_ACCESS_INVENTORY_COMPLETE",
        "pending_fulltext_candidates": len(pending),
        "unique_openalex_work_ids_requested": len(set(all_ids)),
        "unique_openalex_work_ids_retrieved": len(work_map),
        "provider_work_ids_missing": missing_provider_ids,
        "retrieval_priority_counts": dict(sorted(priorities.items())),
        "oa_status_record_counts": dict(sorted(oa_status_counter.items())),
        "effect_direction_inspected": False,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.frame, args.decisions, args.output, args.receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
