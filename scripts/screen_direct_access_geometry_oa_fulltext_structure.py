"""Direction-blind structural screen of OA full text for formal-frame candidates.

Raw PDFs and extracted full text are not persisted. Automatic exclusion is allowed
only when adequately extracted full text contains no access-geometry signal or no
robbery/bypass-route signal. Effect direction is never coded in this stage.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.inventory_direct_access_geometry_fulltext_access import OUTPUT_FIELDS as ACCESS_FIELDS
from scripts.screen_direct_access_geometry_openalex_title_abstract import ROUTE_RE

MIN_EXTRACTED_CHARS = 3000
MAX_PDF_BYTES = 30 * 1024 * 1024

ACCESS_PATTERNS = (
    r"corolla (?:tube )?(?:length|width|depth|size)",
    r"(?:floral|flower) (?:tube )?(?:length|width|depth|size)",
    r"tube (?:length|width|depth)",
    r"spur length",
    r"floral depth",
    r"nectar accessib",
    r"flower accessib",
    r"floral accessib",
    r"access constraint",
    r"morphological constraint",
    r"trait mismatch",
    r"morphological mismatch",
    r"mechanical mismatch",
    r"tongue length",
    r"proboscis length",
    r"glossa length",
    r"bill length",
    r"beak length",
    r"short[- ]tongued",
    r"long[- ]tongued",
    r"short[- ]billed",
    r"long[- ]billed",
    r"corolla opening",
    r"floral opening",
    r"aperture",
    r"legitimate access",
)
ACCESS_RE = re.compile("|".join(f"(?:{p})" for p in ACCESS_PATTERNS), re.I)

OUTPUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "retrieval_status",
    "pdf_url_used",
    "extracted_chars",
    "route_signal_present",
    "access_geometry_signal_present",
    "structural_screen_state",
    "notes",
)


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _download_pdf(urls: list[str]) -> tuple[bytes | None, str, str]:
    errors = []
    for url in urls:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "bita-formal-fulltext-screen/1.0",
                "Accept": "application/pdf,text/html;q=0.5,*/*;q=0.1",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read(MAX_PDF_BYTES + 1)
                content_type = str(response.headers.get("Content-Type") or "")
            if len(content) > MAX_PDF_BYTES:
                errors.append(f"too_large:{url}")
                continue
            if content.startswith(b"%PDF") or "application/pdf" in content_type.lower():
                return content, url, "PDF_DOWNLOADED"
            errors.append(f"not_pdf:{url}:{content_type}")
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{url}")
    return None, "", "PDF_RETRIEVAL_FAILED:" + ";".join(errors[:5])


def _extract_text(pdf: bytes) -> tuple[str, str]:
    from pypdf import PdfReader  # type: ignore

    try:
        reader = PdfReader(io.BytesIO(pdf), strict=False)
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                parts.append("")
        text = "\n".join(parts)
        return text, "TEXT_EXTRACTED"
    except Exception as exc:
        return "", f"TEXT_EXTRACTION_FAILED:{type(exc).__name__}"


def run(
    access_queue_path: Path,
    decisions_path: Path,
    output_path: Path,
    updated_decisions_path: Path,
    receipt_path: Path,
) -> dict[str, object]:
    access_fields, access_rows = _read(access_queue_path)
    decision_fields, decisions = _read(decisions_path)
    if access_fields != ACCESS_FIELDS:
        raise ValueError("FT_STRUCT_ACCESS_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("FT_STRUCT_DECISION_SCHEMA_MISMATCH")

    decisions_by_id = {row["frame_id"].strip(): row for row in decisions}
    output = []
    counts: Counter[str] = Counter()

    for access in access_rows:
        fid = access["frame_id"].strip()
        decision = decisions_by_id[fid]
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            raise ValueError(f"FT_STRUCT_EXPECTED_PENDING:{fid}")

        pdf_urls = [u for u in access["pdf_urls"].split("|") if u]
        if not pdf_urls:
            state = "NON_PDF_ACCESS_PATH_PENDING"
            counts[state] += 1
            output.append(
                {
                    "frame_id": fid,
                    "doi": access["doi"],
                    "title": access["title"],
                    "year": access["year"],
                    "retrieval_status": "NO_DIRECT_OA_PDF",
                    "pdf_url_used": "",
                    "extracted_chars": "0",
                    "route_signal_present": "",
                    "access_geometry_signal_present": "",
                    "structural_screen_state": state,
                    "notes": "Retained; landing/DOI retrieval required.",
                }
            )
            continue

        pdf, used_url, retrieval = _download_pdf(pdf_urls)
        if pdf is None:
            state = "OA_PDF_RETRIEVAL_FAILED_RETAIN"
            counts[state] += 1
            output.append(
                {
                    "frame_id": fid,
                    "doi": access["doi"],
                    "title": access["title"],
                    "year": access["year"],
                    "retrieval_status": retrieval,
                    "pdf_url_used": "",
                    "extracted_chars": "0",
                    "route_signal_present": "",
                    "access_geometry_signal_present": "",
                    "structural_screen_state": state,
                    "notes": "Retained; no automatic exclusion after retrieval failure.",
                }
            )
            continue

        text, extraction = _extract_text(pdf)
        chars = len(text.strip())
        if extraction != "TEXT_EXTRACTED" or chars < MIN_EXTRACTED_CHARS:
            state = "OA_PDF_TEXT_INADEQUATE_RETAIN"
            counts[state] += 1
            output.append(
                {
                    "frame_id": fid,
                    "doi": access["doi"],
                    "title": access["title"],
                    "year": access["year"],
                    "retrieval_status": extraction,
                    "pdf_url_used": used_url,
                    "extracted_chars": str(chars),
                    "route_signal_present": "",
                    "access_geometry_signal_present": "",
                    "structural_screen_state": state,
                    "notes": "Retained; extracted text inadequate for automatic exclusion.",
                }
            )
            continue

        route_present = bool(ROUTE_RE.search(text))
        access_present = bool(ACCESS_RE.search(text))

        if not route_present:
            state = "INELIGIBLE_FULLTEXT_NO_ROUTE_SIGNAL"
            decision["decision_status"] = state
            decision["decision_basis"] = "DIRECTION_BLIND_OA_FULLTEXT_NO_ROBBERY_ROUTE_SIGNAL"
            decision["source_identifier"] = used_url
            decision["notes"] = (
                "OA full text extracted adequately and contained no frozen direct "
                "robbery/bypass-route signal; effect direction not inspected."
            )
        elif not access_present:
            state = "INELIGIBLE_FULLTEXT_NO_ACCESS_GEOMETRY_SIGNAL"
            decision["decision_status"] = state
            decision["decision_basis"] = "DIRECTION_BLIND_OA_FULLTEXT_NO_ACCESS_GEOMETRY_SIGNAL"
            decision["source_identifier"] = used_url
            decision["notes"] = (
                "OA full text extracted adequately and contained no frozen access-"
                "geometry/mismatch signal; effect direction not inspected."
            )
        else:
            state = "FULLTEXT_MECHANISM_ADJUDICATION_REQUIRED"
            decision["notes"] = (
                "OA_FULLTEXT_HAS_ROUTE_AND_ACCESS_SIGNALS_DIRECTION_NOT_INSPECTED"
            )

        counts[state] += 1
        output.append(
            {
                "frame_id": fid,
                "doi": access["doi"],
                "title": access["title"],
                "year": access["year"],
                "retrieval_status": retrieval + "|" + extraction,
                "pdf_url_used": used_url,
                "extracted_chars": str(chars),
                "route_signal_present": str(route_present).lower(),
                "access_geometry_signal_present": str(access_present).lower(),
                "structural_screen_state": state,
                "notes": "DIRECTION_NOT_INSPECTED",
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output)

    with updated_decisions_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_OA_FULLTEXT_STRUCTURAL_SCREEN_V1",
        "status": "DIRECTION_BLIND_OA_FULLTEXT_STRUCTURAL_SCREEN_COMPLETE",
        "candidate_records": len(access_rows),
        "state_counts": dict(sorted(counts.items())),
        "minimum_extracted_chars_for_auto_exclusion": MIN_EXTRACTED_CHARS,
        "effect_direction_inspected": False,
        "raw_pdf_persisted": False,
        "extracted_fulltext_persisted": False,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--access-queue", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--updated-decisions", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.access_queue,
        args.decisions,
        args.output,
        args.updated_decisions,
        args.receipt,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
