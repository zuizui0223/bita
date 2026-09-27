"""Rank unresolved formal-frame candidates for direction-blind source adjudication.

This does not make eligibility or direction decisions. It prioritizes unresolved
records using only title/abstract structural signals plus prior direction-blind
full-text triage states.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.screen_direct_access_geometry_openalex_title_abstract import (
    ROUTE_RE,
    _abstract_text,
    _openalex_ids,
)
from scripts.screen_direct_access_geometry_oa_fulltext import ACCESS_RE, QUANT_RE


OUTPUT_FIELDS = (
    "priority_rank",
    "priority_score",
    "frame_id",
    "doi",
    "title",
    "year",
    "query_ids",
    "route_signal_title_abstract",
    "access_signal_title_abstract",
    "quant_signal_title_abstract",
    "explicit_secondary_title",
    "fulltext_triage_lane",
    "openalex_ids",
    "review_state",
)

SECONDARY_RE = re.compile(
    r"\b(?:systematic\s+review|meta[-\s]?analysis|review|perspective|"
    r"synthesis|overview)\b",
    re.I,
)
DIRECT_TITLE_RE = re.compile(
    r"(?:nectar\s+rob\w*|floral\s+larcen\w*).{0,80}"
    r"(?:corolla|tube|length|depth|mismatch|morpholog\w*|access|proboscis|"
    r"tongue|bill|short[-\s]?tongued)|"
    r"(?:corolla|tube|length|depth|mismatch|morpholog\w*|access|proboscis|"
    r"tongue|bill|short[-\s]?tongued).{0,80}"
    r"(?:nectar\s+rob\w*|floral\s+larcen\w*)",
    re.I,
)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _get_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "bita-formal-candidate-ranker/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _fetch_batch(ids: list[str], batch_size: int = 50) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    unique = sorted(set(ids))
    for start in range(0, len(unique), batch_size):
        chunk = unique[start:start + batch_size]
        params = {
            "filter": "openalex_id:" + "|".join(chunk),
            "per-page": "100",
            "select": "id,title,display_name,abstract_inverted_index,type",
        }
        payload = _get_json("https://api.openalex.org/works?" + urllib.parse.urlencode(params))
        rows = payload.get("results")
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                oid = str(row.get("id") or "").removeprefix("https://openalex.org/")
                if oid:
                    out[oid] = row
        time.sleep(0.12)
    return out


def run(
    decisions_path: Path,
    fulltext_audit_path: Path,
    output_path: Path,
    receipt_path: Path,
) -> dict[str, object]:
    decision_fields, decisions = _read(decisions_path)
    if decision_fields != FIELDS:
        raise ValueError("RANK_DECISION_SCHEMA_MISMATCH")

    audit_by_id: dict[str, dict[str, str]] = {}
    if fulltext_audit_path.exists():
        _, audit_rows = _read(fulltext_audit_path)
        audit_by_id = {row["frame_id"].strip(): row for row in audit_rows}

    pending = [
        row for row in decisions
        if row["decision_status"].strip() == "PENDING_FULLTEXT"
    ]
    ids_by_frame: dict[str, list[str]] = {}
    all_ids: list[str] = []
    for row in pending:
        # The source identifier can remain blank; ids are recovered from audit when available.
        audit = audit_by_id.get(row["frame_id"].strip(), {})
        ids: list[str] = []
        source = str(audit.get("source_identifier") or "")
        # source_identifier is a URL in the full-text audit, so use the access inventory is not available here.
        # Fall back to DOI-independent OpenAlex title search only when no IDs are carried by the audit.
        ids_by_frame[row["frame_id"].strip()] = ids

    # Recover OpenAlex IDs through DOI/title search only for ranking metadata.
    metadata: dict[str, dict[str, Any]] = {}
    for row in pending:
        fid = row["frame_id"].strip()
        doi = row["doi"].strip()
        if doi:
            query = urllib.parse.quote("https://doi.org/" + doi, safe="")
            try:
                work = _get_json(f"https://api.openalex.org/works/{query}")
                metadata[fid] = work
                continue
            except Exception:
                pass
        params = {
            "search": row["title"].strip(),
            "filter": f"from_publication_date:{row['year']}-01-01,to_publication_date:{row['year']}-12-31",
            "per-page": "5",
            "select": "id,title,display_name,abstract_inverted_index,type",
        }
        try:
            payload = _get_json("https://api.openalex.org/works?" + urllib.parse.urlencode(params))
            results = payload.get("results")
            if isinstance(results, list) and results:
                metadata[fid] = results[0]
        except Exception:
            pass
        time.sleep(0.05)

    rows_out: list[dict[str, str]] = []
    score_counts: dict[str, int] = {}
    for row in pending:
        fid = row["frame_id"].strip()
        work = metadata.get(fid, {})
        title = str(work.get("title") or work.get("display_name") or row["title"]).strip()
        abstract = _abstract_text(work.get("abstract_inverted_index"))
        combined = f"{title} {abstract}"

        route = bool(ROUTE_RE.search(combined))
        access = bool(ACCESS_RE.search(combined))
        quant = bool(QUANT_RE.search(combined))
        secondary = bool(SECONDARY_RE.search(title))
        direct_title = bool(DIRECT_TITLE_RE.search(title))

        audit = audit_by_id.get(fid, {})
        fulltext_lane = str(audit.get("triage_lane") or "")

        score = 0
        if direct_title:
            score += 5
        if route:
            score += 2
        if access:
            score += 2
        if quant:
            score += 1
        if route and access:
            score += 2
        if fulltext_lane == "HIGH_PRIORITY_DIRECT_TEST_ADJUDICATION":
            score += 6
        elif fulltext_lane == "ACCESS_ROUTE_PRESENT_QUANT_UNRESOLVED":
            score += 4
        elif fulltext_lane == "ROUTE_PRESENT_ACCESS_UNRESOLVED":
            score += 1
        if secondary:
            score -= 5

        score_counts[str(score)] = score_counts.get(str(score), 0) + 1
        rows_out.append({
            "priority_rank": "",
            "priority_score": str(score),
            "frame_id": fid,
            "doi": row["doi"].strip(),
            "title": row["title"].strip(),
            "year": row["year"].strip(),
            "query_ids": row["query_ids"].strip(),
            "route_signal_title_abstract": "YES" if route else "NO",
            "access_signal_title_abstract": "YES" if access else "NO",
            "quant_signal_title_abstract": "YES" if quant else "NO",
            "explicit_secondary_title": "YES" if secondary else "NO",
            "fulltext_triage_lane": fulltext_lane,
            "openalex_ids": str(work.get("id") or "").removeprefix("https://openalex.org/"),
            "review_state": "UNRESOLVED_DIRECTION_BLIND",
        })

    rows_out.sort(
        key=lambda x: (
            -int(x["priority_score"]),
            int(x["year"]) if x["year"].isdigit() else 9999,
            x["title"].casefold(),
        )
    )
    for rank, row in enumerate(rows_out, start=1):
        row["priority_rank"] = str(rank)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows_out)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_DIRECTION_BLIND_PRIORITY_QUEUE_V1",
        "status": "DIRECTION_BLIND_PRIORITY_QUEUE_COMPLETE",
        "unresolved_candidates": len(rows_out),
        "score_counts": dict(sorted(score_counts.items(), key=lambda x: int(x[0]), reverse=True)),
        "effect_direction_inspected": False,
        "eligibility_decision_made": False,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--fulltext-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.decisions, args.fulltext_audit, args.output, args.receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
