"""Direction-blind title/abstract screen for the frozen OpenAlex frame.

This stage may exclude only records whose available title+abstract contain no
nectar-robbery / bypass-route signal at all. It never codes effect direction.
Records with missing abstracts or any route signal remain pending for full-text
eligibility adjudication.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.bootstrap_direct_access_geometry_bibliographic_screen import FRAME_FIELDS

ROUTE_PATTERNS = (
    r"nectar robb",
    r"nectar theft",
    r"nectar thie",
    r"floral larcen",
    r"floral robb",
    r"illegitimate (?:visit|forag|access)",
    r"illegitimate floral",
    r"secondary robb",
    r"primary robb",
    r"bypass(?:ing|ed)? (?:the )?(?:corolla|flower|floral|legitimate)",
)
ROUTE_RE = re.compile("|".join(f"(?:{p})" for p in ROUTE_PATTERNS), re.I)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _abstract_text(index: Any) -> str:
    if not isinstance(index, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for word, locs in index.items():
        if not isinstance(locs, list):
            continue
        for loc in locs:
            if isinstance(loc, int):
                positions.append((loc, str(word)))
    positions.sort()
    return " ".join(word for _, word in positions)


def classify_title_abstract(title: str, abstract: str) -> str:
    """Return EXCLUDE_NO_ROUTE_SIGNAL or FULLTEXT_REQUIRED."""
    if not abstract.strip():
        return "FULLTEXT_REQUIRED"
    combined = f"{title} {abstract}"
    if ROUTE_RE.search(combined):
        return "FULLTEXT_REQUIRED"
    return "EXCLUDE_NO_ROUTE_SIGNAL"


def _openalex_ids(source_record_ids: str) -> list[str]:
    values = [value.strip() for value in source_record_ids.split("|") if value.strip()]
    ids = []
    for value in values:
        if value.startswith("OpenAlex:https://openalex.org/"):
            ids.append(value.removeprefix("OpenAlex:https://openalex.org/"))
        elif value.startswith("https://openalex.org/"):
            ids.append(value.removeprefix("https://openalex.org/"))
        elif value.startswith("OpenAlex:W"):
            ids.append(value.removeprefix("OpenAlex:"))
    ids = sorted(set(ids))
    if not ids:
        raise ValueError(
            "TA_SCREEN_OPENALEX_ID_NOT_FOUND:" + source_record_ids
        )
    return ids


def _get_json(url: str, attempts: int = 6) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "bita-formal-title-abstract-screen/1.0",
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


def _fetch_works_batch(
    work_ids: list[str],
    batch_size: int = 50,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    import urllib.parse

    output: dict[str, dict[str, Any]] = {}
    missing_ids: list[str] = []
    unique_ids = sorted(set(work_ids))
    for start in range(0, len(unique_ids), batch_size):
        chunk = unique_ids[start:start + batch_size]
        params = {
            "filter": "openalex_id:" + "|".join(chunk),
            "per-page": "100",
            "select": "id,title,display_name,abstract_inverted_index",
        }
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        payload = _get_json(url)
        rows = payload.get("results")
        if not isinstance(rows, list):
            raise RuntimeError("TA_SCREEN_OPENALEX_BATCH_RESULTS_MALFORMED")
        for row in rows:
            if not isinstance(row, dict):
                continue
            oid = str(row.get("id") or "").removeprefix("https://openalex.org/")
            if oid:
                output[oid] = row
        missing = sorted(set(chunk) - set(output))
        missing_ids.extend(missing)
        time.sleep(0.12)
    return output, sorted(set(missing_ids))


def run(
    frame_path: Path,
    decisions_path: Path,
    output_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    frame_fields, frame_rows = _read(frame_path)
    decision_fields, decisions = _read(decisions_path)
    if frame_fields != FRAME_FIELDS:
        raise ValueError("TA_SCREEN_FRAME_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("TA_SCREEN_DECISION_SCHEMA_MISMATCH")

    frame_by_id = {row["frame_id"].strip(): row for row in frame_rows}
    if len(frame_by_id) != len(frame_rows):
        raise ValueError("TA_SCREEN_DUPLICATE_FRAME_ID")

    excluded = 0
    fulltext_required = 0
    missing_abstract = 0

    pending_work_ids: dict[str, list[str]] = {}
    all_work_ids: list[str] = []
    for decision in decisions:
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            continue
        fid = decision["frame_id"].strip()
        frame = frame_by_id[fid]
        if frame["source_dbs"].strip() != "OpenAlex":
            raise ValueError(f"TA_SCREEN_NON_OPENALEX_PENDING_RECORD:{fid}")
        ids = _openalex_ids(frame["source_record_ids"])
        pending_work_ids[fid] = ids
        all_work_ids.extend(ids)

    work_map, provider_missing_ids = _fetch_works_batch(all_work_ids)
    provider_missing_set = set(provider_missing_ids)

    for decision in decisions:
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            continue
        fid = decision["frame_id"].strip()
        work_ids = pending_work_ids[fid]
        titles = []
        abstracts = []
        any_missing_abstract = False
        any_missing_provider_record = False
        for work_id in work_ids:
            work = work_map.get(work_id)
            if work is None:
                any_missing_provider_record = True
                titles.append(decision["title"].strip())
                abstracts.append("")
                continue
            titles.append(
                str(
                    work.get("title")
                    or work.get("display_name")
                    or decision["title"]
                ).strip()
            )
            abstract = _abstract_text(work.get("abstract_inverted_index"))
            abstracts.append(abstract)
            if not abstract:
                any_missing_abstract = True

        combined_title = " ".join(value for value in titles if value)
        combined_abstract = " ".join(value for value in abstracts if value)
        state = (
            "FULLTEXT_REQUIRED"
            if any_missing_provider_record or any_missing_abstract
            else classify_title_abstract(combined_title, combined_abstract)
        )

        if any_missing_abstract or any_missing_provider_record:
            missing_abstract += 1

        source_identifier = "|".join(
            f"OpenAlex:{work_id}" for work_id in work_ids
        )
        if state == "EXCLUDE_NO_ROUTE_SIGNAL":
            decision["decision_status"] = "INELIGIBLE_TITLE_ABSTRACT_NO_ROUTE_OUTCOME"
            decision["decision_basis"] = "DIRECTION_BLIND_TITLE_ABSTRACT_NO_ROBBERY_ROUTE_SIGNAL"
            decision["source_identifier"] = source_identifier
            decision["notes"] = (
                "All deduplicated OpenAlex source records had abstracts and the "
                "combined title+abstract text contained no direct nectar-robbery/"
                "floral-larceny/illegitimate-route signal; no effect direction inspected."
            )
            excluded += 1
        else:
            decision["notes"] = (
                "FULLTEXT_REQUIRED_AFTER_DIRECTION_BLIND_TITLE_ABSTRACT_SCREEN"
            )
            fulltext_required += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_TITLE_ABSTRACT_SCREEN_V1",
        "status": "DIRECTION_BLIND_TITLE_ABSTRACT_SCREEN_COMPLETE",
        "pending_records_fetched": len(pending_work_ids),
        "excluded_no_route_signal": excluded,
        "fulltext_required": fulltext_required,
        "missing_abstract_retained_for_fulltext": missing_abstract,
        "effect_direction_inspected": False,
        "exclusion_rule": (
            "exclude only when an available OpenAlex abstract plus title contains "
            "no frozen robbery/bypass-route signal; missing abstracts are retained"
        ),
        "provider": "OpenAlex",
        "provider_work_fetches": len(work_map),
        "unique_provider_work_ids_requested": len(set(all_work_ids)),
        "provider_work_ids_missing_at_screen_time": provider_missing_ids,
        "provider_work_ids_missing_retained_for_fulltext": len(provider_missing_ids),
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
