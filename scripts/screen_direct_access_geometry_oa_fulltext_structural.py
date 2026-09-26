"""Direction-blind structural full-text screen for OA PDF candidates.

This screen never codes the sign of a geometry-robbery association. It may only
exclude an OA-PDF candidate when text extraction is sufficient and the full text
lacks either (a) any direct robbery/bypass-route signal or (b) any access-geometry
predictor signal. Retrieval/extraction failures remain pending.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

ACCESS_FIELDS = (
    "frame_id","doi","title","year","query_ids","openalex_ids","oa_statuses",
    "pdf_urls","landing_urls","frame_source_urls","retrieval_priority","notes",
)

ROUTE_PATTERNS = (
    r"nectar robb",
    r"nectar theft",
    r"nectar thie",
    r"floral larcen",
    r"floral robb",
    r"illegitimate (?:visit|forag|access)",
    r"secondary robb",
    r"primary robb",
    r"robbed flower",
    r"robbery frequenc",
    r"robbery rate",
    r"robbery probabil",
    r"holes? per corolla",
    r"nectar holes?",
)
GEOMETRY_PATTERNS = (
    r"corolla length",
    r"corolla tube",
    r"tube length",
    r"tube depth",
    r"flower length",
    r"floral length",
    r"flower size",
    r"flower width",
    r"floral morpholog",
    r"nectar accessib",
    r"trait mismatch",
    r"morphological (?:constraint|mismatch)",
    r"tongue length",
    r"proboscis length",
    r"glossa length",
    r"bill length",
    r"beak length",
    r"short-tongued",
    r"long-tubed",
    r"long corolla",
    r"short corolla",
    r"spur length",
    r"aperture",
)
ROUTE_RE = re.compile("|".join(f"(?:{p})" for p in ROUTE_PATTERNS), re.I)
GEOMETRY_RE = re.compile("|".join(f"(?:{p})" for p in GEOMETRY_PATTERNS), re.I)

MIN_EXTRACTED_CHARS = 2500
MAX_PDF_BYTES = 50 * 1024 * 1024


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def classify_fulltext(text: str) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    if len(compact) < MIN_EXTRACTED_CHARS:
        return "RETAIN_EXTRACTION_INSUFFICIENT"
    if not ROUTE_RE.search(compact):
        return "EXCLUDE_NO_ROUTE_SIGNAL"
    if not GEOMETRY_RE.search(compact):
        return "EXCLUDE_NO_GEOMETRY_SIGNAL"
    return "RETAIN_STRUCTURAL_SIGNALS_PRESENT"


def _download_pdf(url: str, attempts: int = 4) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "bita-formal-fulltext-screen/1.0",
            "Accept": "application/pdf,*/*;q=0.8",
        },
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                length = resp.headers.get("Content-Length")
                if length and int(length) > MAX_PDF_BYTES:
                    raise ValueError("PDF_TOO_LARGE")
                data = resp.read(MAX_PDF_BYTES + 1)
                if len(data) > MAX_PDF_BYTES:
                    raise ValueError("PDF_TOO_LARGE")
                if not data.startswith(b"%PDF"):
                    raise ValueError("NOT_PDF_RESPONSE")
                return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
            last = exc
            time.sleep(min(8, 2 ** attempt))
    assert last is not None
    raise last


def _extract_text(data: bytes) -> str:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(io.BytesIO(data), strict=False)
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    return "\n".join(parts)


def _screen_one(row: dict[str, str]) -> dict[str, Any]:
    urls = [u.strip() for u in row["pdf_urls"].split("|") if u.strip()]
    errors: list[str] = []
    for url in urls:
        try:
            data = _download_pdf(url)
            text = _extract_text(data)
            state = classify_fulltext(text)
            return {
                "frame_id": row["frame_id"],
                "state": state,
                "used_url": url,
                "extracted_chars": len(re.sub(r"\s+", " ", text).strip()),
                "route_signal": bool(ROUTE_RE.search(text)),
                "geometry_signal": bool(GEOMETRY_RE.search(text)),
                "errors": errors,
            }
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    return {
        "frame_id": row["frame_id"],
        "state": "RETAIN_RETRIEVAL_FAILED",
        "used_url": "",
        "extracted_chars": 0,
        "route_signal": False,
        "geometry_signal": False,
        "errors": errors,
    }


def run(
    decisions_path: Path,
    access_queue_path: Path,
    output_path: Path,
    receipt_path: Path,
    audit_path: Path,
    *,
    max_workers: int = 6,
) -> dict[str, Any]:
    decision_fields, decisions = _read(decisions_path)
    access_fields, access_rows = _read(access_queue_path)
    if decision_fields != FIELDS:
        raise ValueError("FT_STRUCT_DECISION_SCHEMA_MISMATCH")
    if access_fields != ACCESS_FIELDS:
        raise ValueError(
            f"FT_STRUCT_ACCESS_SCHEMA_MISMATCH:expected={ACCESS_FIELDS}:observed={access_fields}"
        )

    access_by_id = {row["frame_id"].strip(): row for row in access_rows}
    targets = [
        row for row in access_rows
        if row["retrieval_priority"].strip() == "OA_PDF_AVAILABLE"
    ]

    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {pool.submit(_screen_one, row): row["frame_id"] for row in targets}
        for future in as_completed(future_map):
            result = future.result()
            results[result["frame_id"]] = result

    state_counts: dict[str, int] = {}
    for result in results.values():
        state = result["state"]
        state_counts[state] = state_counts.get(state, 0) + 1

    for decision in decisions:
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            continue
        fid = decision["frame_id"].strip()
        access = access_by_id.get(fid)
        if not access or access["retrieval_priority"].strip() != "OA_PDF_AVAILABLE":
            continue
        result = results[fid]
        state = result["state"]

        if state == "EXCLUDE_NO_ROUTE_SIGNAL":
            decision["decision_status"] = "INELIGIBLE_FULLTEXT_NO_ROUTE_OUTCOME"
            decision["decision_basis"] = "DIRECTION_BLIND_FULLTEXT_NO_ROBBERY_ROUTE_SIGNAL"
            decision["source_identifier"] = result["used_url"]
            decision["notes"] = "OA PDF text extracted; no frozen robbery/bypass-route signal; effect direction not inspected."
        elif state == "EXCLUDE_NO_GEOMETRY_SIGNAL":
            decision["decision_status"] = "INELIGIBLE_FULLTEXT_NO_ACCESS_GEOMETRY_PREDICTOR"
            decision["decision_basis"] = "DIRECTION_BLIND_FULLTEXT_NO_ACCESS_GEOMETRY_SIGNAL"
            decision["source_identifier"] = result["used_url"]
            decision["notes"] = "OA PDF text extracted; robbery-route signal present but no frozen access-geometry predictor signal; effect direction not inspected."
        else:
            decision["notes"] = (
                "FULLTEXT_STRUCTURAL_SCREEN_RETAINED:"
                + state
                + ";DIRECTION_NOT_INSPECTED"
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    audit_fields = (
        "frame_id","state","used_url","extracted_chars",
        "route_signal","geometry_signal","error_count",
    )
    with audit_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit_fields)
        writer.writeheader()
        for fid in sorted(results):
            r = results[fid]
            writer.writerow({
                "frame_id": fid,
                "state": r["state"],
                "used_url": r["used_url"],
                "extracted_chars": r["extracted_chars"],
                "route_signal": "YES" if r["route_signal"] else "NO",
                "geometry_signal": "YES" if r["geometry_signal"] else "NO",
                "error_count": len(r["errors"]),
            })

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_OA_FULLTEXT_STRUCTURAL_SCREEN_V1",
        "status": "DIRECTION_BLIND_OA_FULLTEXT_STRUCTURAL_SCREEN_COMPLETE",
        "oa_pdf_candidates": len(targets),
        "state_counts": dict(sorted(state_counts.items())),
        "effect_direction_inspected": False,
        "minimum_extracted_characters_for_exclusion": MIN_EXTRACTED_CHARS,
        "retrieval_or_extraction_failures_retained": state_counts.get("RETAIN_RETRIEVAL_FAILED", 0)
            + state_counts.get("RETAIN_EXTRACTION_INSUFFICIENT", 0),
        "remaining_pending_records": sum(
            row["decision_status"].strip() == "PENDING_FULLTEXT"
            for row in decisions
        ),
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--access-queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--max-workers", type=int, default=6)
    args = parser.parse_args()
    result = run(
        args.decisions,
        args.access_queue,
        args.output,
        args.receipt,
        args.audit,
        max_workers=args.max_workers,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
