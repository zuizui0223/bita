"""Direction-blind body-signal adjudication for high-priority OA full texts.

This stage removes reference-list noise from the previous broad full-text signal
screen. It still never codes effect direction. Auto-exclusion is allowed only when
a verified OA full text has zero robbery-route signal or zero access-geometry
signal before the References/Literature Cited section. All other records remain
pending for source-level adjudication.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.screen_direct_access_geometry_oa_fulltext import (
    ACCESS_RE,
    AUDIT_FIELDS,
    QUANT_RE,
    ROUTE_RE,
    _ascii_norm,
    _try_urls,
)

HIGH_LANE = "HIGH_PRIORITY_DIRECT_TEST_ADJUDICATION"

REF_HEADING_RE = re.compile(
    r"(?im)^[ \t]*(?:references|literature cited|bibliography|works cited)[ \t]*$"
)
METHOD_HEADING_RE = re.compile(
    r"(?im)^[ \t]*(?:materials? and methods?|methods?|methodology|"
    r"statistical analysis|data analysis)[ \t]*$"
)
RESULT_HEADING_RE = re.compile(
    r"(?im)^[ \t]*(?:results?|results and discussion|findings)[ \t]*$"
)

OUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "source_identifier",
    "text_chars",
    "body_chars",
    "reference_cut_applied",
    "route_body_count",
    "access_body_count",
    "quant_body_count",
    "route_access_quant_cooccurrence_windows",
    "methods_heading_present",
    "results_heading_present",
    "body_triage_lane",
)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def strip_reference_tail(text: str) -> tuple[str, bool]:
    """Cut a terminal references section only when the heading occurs late."""
    matches = list(REF_HEADING_RE.finditer(text))
    if not matches:
        return text, False
    threshold = max(1500, int(len(text) * 0.45))
    late = [m for m in matches if m.start() >= threshold]
    if not late:
        return text, False
    cut = late[-1].start()
    return text[:cut], True


def signal_counts(body: str, window: int = 1800) -> dict[str, int]:
    norm = _ascii_norm(body)
    route_matches = list(ROUTE_RE.finditer(norm))
    access_matches = list(ACCESS_RE.finditer(norm))
    quant_matches = list(QUANT_RE.finditer(norm))

    cooccur = 0
    for match in route_matches:
        start = max(0, match.start() - window)
        end = min(len(norm), match.end() + window)
        chunk = norm[start:end]
        if ACCESS_RE.search(chunk) and QUANT_RE.search(chunk):
            cooccur += 1

    return {
        "route": len(route_matches),
        "access": len(access_matches),
        "quant": len(quant_matches),
        "cooccur": cooccur,
    }


def triage_body(body: str) -> str:
    counts = signal_counts(body)
    if counts["route"] == 0:
        return "EXCLUDE_NO_ROUTE_SIGNAL_IN_MAIN_TEXT"
    if counts["access"] == 0:
        return "EXCLUDE_NO_ACCESS_SIGNAL_IN_MAIN_TEXT"
    if counts["cooccur"] > 0:
        return "RETAIN_LOCAL_ROUTE_ACCESS_QUANT_COOCCURRENCE"
    return "RETAIN_BODY_SIGNALS_SEPARATED"


def run(
    prior_audit_path: Path,
    decisions_path: Path,
    output_decisions_path: Path,
    output_audit_path: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    audit_fields, prior_audit = _read(prior_audit_path)
    decision_fields, decisions = _read(decisions_path)
    if audit_fields != AUDIT_FIELDS:
        raise ValueError("BODY_ADJUDICATION_PRIOR_AUDIT_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("BODY_ADJUDICATION_DECISION_SCHEMA_MISMATCH")

    high = {
        row["frame_id"].strip(): row
        for row in prior_audit
        if row["triage_lane"].strip() == HIGH_LANE
    }
    decision_by_id = {row["frame_id"].strip(): row for row in decisions}

    output: list[dict[str, str]] = []
    lanes: Counter[str] = Counter()
    failed_retrieval = 0

    for fid, prior in sorted(high.items()):
        decision = decision_by_id[fid]
        source = prior["source_identifier"].strip()
        url, text, _, coverage = _try_urls([source], decision["title"])

        if not url or not text or coverage < 0.45 or len(text) < 3000:
            lane = "RETAIN_BODY_READ_UNVERIFIED"
            lanes[lane] += 1
            failed_retrieval += 1
            decision["notes"] = (
                "HIGH_PRIORITY_BODY_ADJUDICATION_RETRIEVAL_UNVERIFIED;"
                "DIRECTION_NOT_CODED"
            )
            output.append({
                "frame_id": fid,
                "doi": decision["doi"].strip(),
                "title": decision["title"].strip(),
                "year": decision["year"].strip(),
                "source_identifier": source,
                "text_chars": str(len(text)),
                "body_chars": "0",
                "reference_cut_applied": "NO",
                "route_body_count": "",
                "access_body_count": "",
                "quant_body_count": "",
                "route_access_quant_cooccurrence_windows": "",
                "methods_heading_present": "",
                "results_heading_present": "",
                "body_triage_lane": lane,
            })
            continue

        body, cut = strip_reference_tail(text)
        counts = signal_counts(body)
        lane = triage_body(body)
        lanes[lane] += 1

        if lane == "EXCLUDE_NO_ROUTE_SIGNAL_IN_MAIN_TEXT":
            decision["decision_status"] = "INELIGIBLE_FULLTEXT_NO_ROUTE_OUTCOME_SIGNAL"
            decision["decision_basis"] = (
                "DIRECTION_BLIND_VERIFIED_FULLTEXT_ROUTE_SIGNAL_ABSENT_BEFORE_REFERENCES"
            )
            decision["source_identifier"] = url
            decision["notes"] = (
                "Verified OA full text had no robbery/larceny/illegitimate-route "
                "signal before the reference list; effect direction not inspected."
            )
        elif lane == "EXCLUDE_NO_ACCESS_SIGNAL_IN_MAIN_TEXT":
            decision["decision_status"] = (
                "INELIGIBLE_FULLTEXT_NO_ACCESS_GEOMETRY_PREDICTOR_SIGNAL"
            )
            decision["decision_basis"] = (
                "DIRECTION_BLIND_VERIFIED_FULLTEXT_ACCESS_SIGNAL_ABSENT_BEFORE_REFERENCES"
            )
            decision["source_identifier"] = url
            decision["notes"] = (
                "Verified OA full text had robbery-route language but no frozen "
                "access-geometry predictor signal before the reference list; "
                "effect direction not inspected."
            )
        else:
            decision["notes"] = lane + ";DIRECTION_NOT_CODED"

        output.append({
            "frame_id": fid,
            "doi": decision["doi"].strip(),
            "title": decision["title"].strip(),
            "year": decision["year"].strip(),
            "source_identifier": url,
            "text_chars": str(len(text)),
            "body_chars": str(len(body)),
            "reference_cut_applied": "YES" if cut else "NO",
            "route_body_count": str(counts["route"]),
            "access_body_count": str(counts["access"]),
            "quant_body_count": str(counts["quant"]),
            "route_access_quant_cooccurrence_windows": str(counts["cooccur"]),
            "methods_heading_present": "YES" if METHOD_HEADING_RE.search(body) else "NO",
            "results_heading_present": "YES" if RESULT_HEADING_RE.search(body) else "NO",
            "body_triage_lane": lane,
        })

    output_decisions_path.parent.mkdir(parents=True, exist_ok=True)
    with output_decisions_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    with output_audit_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BODY_SIGNAL_ADJUDICATION_V1",
        "status": "DIRECTION_BLIND_BODY_SIGNAL_ADJUDICATION_COMPLETE",
        "high_priority_input_records": len(high),
        "body_triage_lane_counts": dict(sorted(lanes.items())),
        "retrieval_unverified_retained": failed_retrieval,
        "effect_direction_inspected": False,
        "remaining_pending_records": sum(
            row["decision_status"].strip() == "PENDING_FULLTEXT"
            for row in decisions
        ),
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-audit", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output-decisions", type=Path, required=True)
    parser.add_argument("--output-audit", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.prior_audit,
        args.decisions,
        args.output_decisions,
        args.output_audit,
        args.receipt,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
