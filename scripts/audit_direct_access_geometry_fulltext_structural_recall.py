"""Recall audit for the direction-blind OA fulltext structural screen.

Known direct-corpus programs are calibration positives for eligibility structure,
not for effect direction. This audit asks whether the frozen route/access regexes
recover both required structural signals in adequately extracted OA full texts.
"""
from __future__ import annotations

import argparse
import csv
import json
import urllib.parse
from collections import Counter
from pathlib import Path

from scripts.bootstrap_direct_access_geometry_bibliographic_screen import FRAME_FIELDS, OUTPUT_FIELDS as SCREEN_FIELDS
from scripts.inventory_direct_access_geometry_fulltext_access import _fetch_works, _location_urls
from scripts.screen_direct_access_geometry_oa_fulltext_structure import (
    ACCESS_RE,
    MIN_EXTRACTED_CHARS,
    _download_pdf,
    _extract_text,
)
from scripts.screen_direct_access_geometry_openalex_title_abstract import ROUTE_RE, _openalex_ids

AUDIT_FIELDS = (
    "frame_id",
    "known_study_id",
    "title",
    "oa_pdf_available",
    "pdf_retrieved",
    "extracted_chars",
    "route_signal_present",
    "access_geometry_signal_present",
    "audit_state",
)


def _read(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def run(frame_path: Path, screen_path: Path, output_path: Path, receipt_path: Path):
    frame_fields, frame = _read(frame_path)
    screen_fields, screen = _read(screen_path)
    if frame_fields != FRAME_FIELDS:
        raise ValueError("FT_RECALL_FRAME_SCHEMA_MISMATCH")
    if screen_fields != SCREEN_FIELDS:
        raise ValueError("FT_RECALL_SCREEN_SCHEMA_MISMATCH")

    frame_by_id = {row["frame_id"].strip(): row for row in frame}
    known = [
        row for row in screen
        if row["screen_status"].strip() == "KNOWN_DIRECT_CORPUS_MATCH"
    ]

    ids_by_fid = {}
    all_ids = []
    for row in known:
        fid = row["frame_id"].strip()
        ids = _openalex_ids(frame_by_id[fid]["source_record_ids"])
        ids_by_fid[fid] = ids
        all_ids.extend(ids)

    works = _fetch_works(all_ids)
    rows = []
    counts = Counter()
    adequately_extracted = 0
    structural_failures = []

    for row in known:
        fid = row["frame_id"].strip()
        pdfs = set()
        for oid in ids_by_fid[fid]:
            wpdfs, _ = _location_urls(works[oid])
            pdfs |= wpdfs

        if not pdfs:
            state = "NO_OA_PDF_NOT_TESTABLE"
            counts[state] += 1
            rows.append({
                "frame_id": fid,
                "known_study_id": row["known_study_id"],
                "title": row["title"],
                "oa_pdf_available": "false",
                "pdf_retrieved": "false",
                "extracted_chars": "0",
                "route_signal_present": "",
                "access_geometry_signal_present": "",
                "audit_state": state,
            })
            continue

        pdf, _, retrieval = _download_pdf(sorted(pdfs))
        if pdf is None:
            state = "OA_PDF_RETRIEVAL_FAILED_NOT_TESTABLE"
            counts[state] += 1
            rows.append({
                "frame_id": fid,
                "known_study_id": row["known_study_id"],
                "title": row["title"],
                "oa_pdf_available": "true",
                "pdf_retrieved": "false",
                "extracted_chars": "0",
                "route_signal_present": "",
                "access_geometry_signal_present": "",
                "audit_state": state,
            })
            continue

        text, extraction = _extract_text(pdf)
        chars = len(text.strip())
        if extraction != "TEXT_EXTRACTED" or chars < MIN_EXTRACTED_CHARS:
            state = "TEXT_INADEQUATE_NOT_TESTABLE"
            counts[state] += 1
            rows.append({
                "frame_id": fid,
                "known_study_id": row["known_study_id"],
                "title": row["title"],
                "oa_pdf_available": "true",
                "pdf_retrieved": "true",
                "extracted_chars": str(chars),
                "route_signal_present": "",
                "access_geometry_signal_present": "",
                "audit_state": state,
            })
            continue

        adequately_extracted += 1
        route = bool(ROUTE_RE.search(text))
        access = bool(ACCESS_RE.search(text))
        if route and access:
            state = "STRUCTURE_RECALLED"
        else:
            state = "STRUCTURE_RECALL_FAILURE"
            structural_failures.append({
                "study_id": row["known_study_id"],
                "route": route,
                "access": access,
            })
        counts[state] += 1
        rows.append({
            "frame_id": fid,
            "known_study_id": row["known_study_id"],
            "title": row["title"],
            "oa_pdf_available": "true",
            "pdf_retrieved": "true",
            "extracted_chars": str(chars),
            "route_signal_present": str(route).lower(),
            "access_geometry_signal_present": str(access).lower(),
            "audit_state": state,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FULLTEXT_STRUCTURAL_RECALL_AUDIT_V1",
        "status": (
            "PASS_KNOWN_STRUCTURAL_RECALL"
            if not structural_failures
            else "FAIL_KNOWN_STRUCTURAL_RECALL"
        ),
        "known_programs_in_provider_frame": len(known),
        "adequately_extracted_known_fulltexts": adequately_extracted,
        "structural_recall_failures": structural_failures,
        "state_counts": dict(sorted(counts.items())),
        "effect_direction_used_for_screening": False,
    }
    receipt_path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--frame", type=Path, required=True)
    p.add_argument("--screen", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    a=p.parse_args()
    r=run(a.frame,a.screen,a.output,a.receipt)
    print(json.dumps(r, indent=2, sort_keys=True))
    if r["status"] != "PASS_KNOWN_STRUCTURAL_RECALL":
        return 2
    return 0


if __name__=="__main__":
    raise SystemExit(main())
