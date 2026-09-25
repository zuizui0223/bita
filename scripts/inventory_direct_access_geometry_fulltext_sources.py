"""Inventory full-text access for direction-blind formal-frame candidates."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.bootstrap_direct_access_geometry_bibliographic_screen import FRAME_FIELDS


OUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "query_ids",
    "openalex_ids",
    "openalex_types",
    "abstract_available",
    "oa_status",
    "oa_pdf_urls",
    "landing_page_urls",
    "access_state",
)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _openalex_ids(source_record_ids: str) -> list[str]:
    values = [v.strip() for v in source_record_ids.split("|") if v.strip()]
    ids: list[str] = []
    for value in values:
        if value.startswith("OpenAlex:https://openalex.org/"):
            ids.append(value.removeprefix("OpenAlex:https://openalex.org/"))
        elif value.startswith("https://openalex.org/"):
            ids.append(value.removeprefix("https://openalex.org/"))
        elif value.startswith("OpenAlex:W"):
            ids.append(value.removeprefix("OpenAlex:"))
    ids = sorted(set(ids))
    if not ids:
        raise ValueError("FT_INVENTORY_NO_OPENALEX_ID:" + source_record_ids)
    return ids


def _get_json(url: str, attempts: int = 6) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "bita-formal-fulltext-inventory/1.0",
            "Accept": "application/json",
        },
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in {429, 500, 502, 503, 504}:
                raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
        time.sleep(min(30, 2**attempt))
    assert last is not None
    raise last


def _fetch_batch(work_ids: list[str], batch_size: int = 50) -> tuple[dict[str, dict[str, Any]], list[str]]:
    output: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    unique = sorted(set(work_ids))
    select = ",".join(
        (
            "id",
            "doi",
            "title",
            "display_name",
            "publication_year",
            "type",
            "abstract_inverted_index",
            "open_access",
            "best_oa_location",
            "primary_location",
            "locations",
        )
    )
    for start in range(0, len(unique), batch_size):
        chunk = unique[start:start + batch_size]
        params = {
            "filter": "openalex_id:" + "|".join(chunk),
            "per-page": "100",
            "select": select,
        }
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        payload = _get_json(url)
        rows = payload.get("results")
        if not isinstance(rows, list):
            raise RuntimeError("FT_INVENTORY_OPENALEX_RESULTS_MALFORMED")
        seen_chunk: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            oid = str(row.get("id") or "").removeprefix("https://openalex.org/")
            if oid:
                output[oid] = row
                seen_chunk.add(oid)
        missing.extend(sorted(set(chunk) - seen_chunk))
        time.sleep(0.12)
    return output, sorted(set(missing))


def _location_urls(work: dict[str, Any]) -> tuple[list[str], list[str]]:
    pdfs: set[str] = set()
    landings: set[str] = set()

    candidates: list[Any] = [
        work.get("best_oa_location"),
        work.get("primary_location"),
    ]
    locations = work.get("locations")
    if isinstance(locations, list):
        candidates.extend(locations)

    for location in candidates:
        if not isinstance(location, dict):
            continue
        pdf = str(location.get("pdf_url") or "").strip()
        landing = str(location.get("landing_page_url") or "").strip()
        if pdf:
            pdfs.add(pdf)
        if landing:
            landings.add(landing)
    return sorted(pdfs), sorted(landings)


def run(frame_path: Path, decisions_path: Path, output_path: Path, receipt_path: Path) -> dict[str, Any]:
    frame_fields, frame_rows = _read(frame_path)
    decision_fields, decision_rows = _read(decisions_path)
    if frame_fields != FRAME_FIELDS:
        raise ValueError("FT_INVENTORY_FRAME_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("FT_INVENTORY_DECISION_SCHEMA_MISMATCH")

    frame_by_id = {row["frame_id"].strip(): row for row in frame_rows}
    pending = [
        row for row in decision_rows
        if row["decision_status"].strip() == "PENDING_FULLTEXT"
    ]

    ids_by_frame: dict[str, list[str]] = {}
    all_ids: list[str] = []
    for decision in pending:
        fid = decision["frame_id"].strip()
        frame = frame_by_id[fid]
        ids = _openalex_ids(frame["source_record_ids"])
        ids_by_frame[fid] = ids
        all_ids.extend(ids)

    work_map, missing_ids = _fetch_batch(all_ids)
    missing_set = set(missing_ids)

    rows: list[dict[str, str]] = []
    counts = {
        "OA_PDF_AVAILABLE": 0,
        "LANDING_PAGE_ONLY": 0,
        "NO_PROVIDER_LOCATION": 0,
        "PROVIDER_RECORD_MISSING": 0,
    }
    abstract_available_count = 0

    for decision in pending:
        fid = decision["frame_id"].strip()
        work_ids = ids_by_frame[fid]
        works = [work_map[oid] for oid in work_ids if oid in work_map]
        missing_here = [oid for oid in work_ids if oid in missing_set]

        types = sorted({
            str(work.get("type") or "").strip()
            for work in works
            if str(work.get("type") or "").strip()
        })
        oa_statuses = sorted({
            str((work.get("open_access") or {}).get("oa_status") or "").strip()
            for work in works
            if isinstance(work.get("open_access"), dict)
            and str((work.get("open_access") or {}).get("oa_status") or "").strip()
        })

        pdfs: set[str] = set()
        landings: set[str] = set()
        abstract_available = False
        for work in works:
            p, l = _location_urls(work)
            pdfs.update(p)
            landings.update(l)
            if isinstance(work.get("abstract_inverted_index"), dict) and work["abstract_inverted_index"]:
                abstract_available = True

        if abstract_available:
            abstract_available_count += 1

        if missing_here:
            access_state = "PROVIDER_RECORD_MISSING"
        elif pdfs:
            access_state = "OA_PDF_AVAILABLE"
        elif landings:
            access_state = "LANDING_PAGE_ONLY"
        else:
            access_state = "NO_PROVIDER_LOCATION"
        counts[access_state] += 1

        rows.append({
            "frame_id": fid,
            "doi": decision["doi"].strip(),
            "title": decision["title"].strip(),
            "year": decision["year"].strip(),
            "query_ids": decision["query_ids"].strip(),
            "openalex_ids": "|".join(work_ids),
            "openalex_types": "|".join(types),
            "abstract_available": "YES" if abstract_available else "NO",
            "oa_status": "|".join(oa_statuses),
            "oa_pdf_urls": "|".join(sorted(pdfs)),
            "landing_page_urls": "|".join(sorted(landings)),
            "access_state": access_state,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FULLTEXT_SOURCE_INVENTORY_V1",
        "status": "FULLTEXT_SOURCE_ACCESS_INVENTORIED",
        "candidate_records": len(pending),
        "access_state_counts": counts,
        "abstract_available_records": abstract_available_count,
        "provider_work_ids_requested": len(set(all_ids)),
        "provider_work_ids_missing": missing_ids,
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
