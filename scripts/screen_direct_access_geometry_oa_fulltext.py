"""Direction-blind full-text signal screen for OA PDF candidates.

PDFs are downloaded ephemerally and never committed. A record is auto-excluded only
when a PDF is successfully extracted, verified against the bibliographic title, and
contains no nectar-robbery / floral-larceny / illegitimate-route signal anywhere in
the extracted text. All ambiguous cases remain pending for source adjudication.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import tempfile
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Iterable

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

ACCESS_FIELDS = (
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

AUDIT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "pdf_attempts",
    "pdf_retrieved",
    "extraction_verified",
    "text_chars",
    "title_token_coverage",
    "route_signal",
    "access_signal",
    "quantitative_signal",
    "triage_lane",
    "source_identifier",
)

ROUTE_RE = re.compile(
    r"(?:nectar\s+rob\w*|nectar\s+thef\w*|nectar\s+thie\w*|"
    r"floral\s+larcen\w*|floral\s+rob\w*|"
    r"illegitimate\s+(?:visit\w*|forag\w*|access\w*)|"
    r"(?:primary|secondary)\s+rob\w*)",
    re.I,
)
ACCESS_RE = re.compile(
    r"(?:corolla|floral|flower)\s+(?:tube\s+)?(?:length|depth|width|size|shape|morpholog\w*)|"
    r"(?:tube|spur)\s+(?:length|depth|width)|"
    r"nectar\s+accessib\w*|trait\s+mismatch|morpholog\w*\s+(?:constraint|mismatch)|"
    r"(?:tongue|proboscis|glossa|bill)\s+length|short[-\s]?tongued|"
    r"visitor[-\s]flower\s+mismatch|access\s+(?:barrier|constraint|difficulty)|"
    r"legitimate\s+access",
    re.I,
)
QUANT_RE = re.compile(
    r"(?:\b(?:regress\w*|correlat\w*|association|associated|probability|frequency|"
    r"generalized\s+linear|glm|mixed[-\s]effect|model(?:led|ed|ing)?|"
    r"odds\s+ratio|chi[-\s]?square|anova)\b|"
    r"\bp\s*[<=>]|\br\s*2\s*=|\br\^2\b)",
    re.I,
)
STOP = {
    "with", "from", "into", "over", "under", "between", "among", "through",
    "their", "these", "those", "using", "study", "effect", "effects", "plant",
    "plants", "flower", "flowers", "floral", "nectar", "pollinator",
    "pollinators", "and", "the", "for", "that", "this",
}


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _ascii_norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = text.replace("-\n", "")
    text = re.sub(r"\s+", " ", text)
    return text


def _title_tokens(title: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", _ascii_norm(title))
    return sorted({token for token in tokens if len(token) >= 4 and token not in STOP})


def _title_coverage(title: str, text: str) -> float:
    tokens = _title_tokens(title)
    if not tokens:
        return 1.0
    haystack = _ascii_norm(text[:40000])
    return sum(token in haystack for token in tokens) / len(tokens)


def _download_pdf(url: str, output: Path, max_bytes: int = 40 * 1024 * 1024) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 bita-formal-fulltext-audit/1.0",
            "Accept": "application/pdf,text/html;q=0.3,*/*;q=0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise RuntimeError("PDF_TOO_LARGE")
    if not data.startswith(b"%PDF"):
        raise RuntimeError("NOT_A_PDF_RESPONSE")
    output.write_bytes(data)


def _extract_pdf(pdf: Path, txt: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(txt)],
        capture_output=True,
        text=True,
        timeout=90,
    )
    if proc.returncode != 0:
        raise RuntimeError("PDFTOTEXT_FAILED:" + proc.stderr[-500:])
    return txt.read_text(encoding="utf-8", errors="replace")


def _try_urls(urls: Iterable[str], title: str) -> tuple[str | None, str, int, float]:
    attempts = 0
    best_text = ""
    best_url: str | None = None
    best_cov = 0.0

    with tempfile.TemporaryDirectory(prefix="bita_ft_") as tmp:
        tmpdir = Path(tmp)
        for index, url in enumerate(urls, start=1):
            if not url.strip():
                continue
            attempts += 1
            pdf = tmpdir / f"source_{index}.pdf"
            txt = tmpdir / f"source_{index}.txt"
            try:
                _download_pdf(url.strip(), pdf)
                text = _extract_pdf(pdf, txt)
            except Exception:
                continue
            if len(text) < 1500:
                continue
            cov = _title_coverage(title, text)
            if cov > best_cov or (cov == best_cov and len(text) > len(best_text)):
                best_text = text
                best_url = url.strip()
                best_cov = cov
            if cov >= 0.45 and len(text) >= 3000:
                return best_url, best_text, attempts, best_cov
    return best_url, best_text, attempts, best_cov


def run(
    access_queue_path: Path,
    decisions_path: Path,
    output_decisions_path: Path,
    audit_path: Path,
    receipt_path: Path,
) -> dict[str, object]:
    access_fields, access_rows = _read(access_queue_path)
    decision_fields, decisions = _read(decisions_path)
    if access_fields != ACCESS_FIELDS:
        raise ValueError(
            f"OA_FT_ACCESS_SCHEMA_MISMATCH:expected={ACCESS_FIELDS}:observed={access_fields}"
        )
    if decision_fields != FIELDS:
        raise ValueError("OA_FT_DECISION_SCHEMA_MISMATCH")

    access_by_id = {row["frame_id"].strip(): row for row in access_rows}
    audit: list[dict[str, str]] = []
    counters: Counter[str] = Counter()

    for decision in decisions:
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            continue
        fid = decision["frame_id"].strip()
        access = access_by_id.get(fid)
        if access is None:
            raise ValueError(f"OA_FT_PENDING_MISSING_ACCESS_ROW:{fid}")

        if access["retrieval_priority"].strip() != "OA_PDF_AVAILABLE":
            lane = "NON_OA_RETAINED"
            counters[lane] += 1
            audit.append({
                "frame_id": fid,
                "doi": decision["doi"].strip(),
                "title": decision["title"].strip(),
                "year": decision["year"].strip(),
                "pdf_attempts": "0",
                "pdf_retrieved": "NO",
                "extraction_verified": "NO",
                "text_chars": "0",
                "title_token_coverage": "",
                "route_signal": "UNKNOWN",
                "access_signal": "UNKNOWN",
                "quantitative_signal": "UNKNOWN",
                "triage_lane": lane,
                "source_identifier": "",
            })
            continue

        urls = [u for u in access["pdf_urls"].split("|") if u.strip()]
        source_url, text, attempts, coverage = _try_urls(urls, decision["title"])
        retrieved = bool(source_url and text)
        verified = bool(retrieved and len(text) >= 3000 and coverage >= 0.45)

        if not verified:
            lane = "OA_PDF_EXTRACTION_UNVERIFIED_RETAINED"
            counters[lane] += 1
            decision["notes"] = (
                "OA_PDF_EXTRACTION_UNVERIFIED_RETAINED_FOR_MANUAL_FULLTEXT"
            )
            route = access_signal = quant_signal = "UNKNOWN"
        else:
            norm = _ascii_norm(text)
            route_bool = bool(ROUTE_RE.search(norm))
            access_bool = bool(ACCESS_RE.search(norm))
            quant_bool = bool(QUANT_RE.search(norm))
            route = "YES" if route_bool else "NO"
            access_signal = "YES" if access_bool else "NO"
            quant_signal = "YES" if quant_bool else "NO"

            if not route_bool:
                lane = "AUTO_EXCLUDED_NO_ROUTE_SIGNAL_IN_VERIFIED_FULLTEXT"
                counters[lane] += 1
                decision["decision_status"] = "INELIGIBLE_FULLTEXT_NO_ROUTE_OUTCOME_SIGNAL"
                decision["decision_basis"] = (
                    "DIRECTION_BLIND_VERIFIED_OA_FULLTEXT_NO_ROBBERY_ROUTE_SIGNAL"
                )
                decision["source_identifier"] = source_url or ""
                decision["notes"] = (
                    "Verified extracted OA full text contained no frozen robbery/"
                    "larceny/illegitimate-route signal; effect direction not inspected."
                )
            elif access_bool and quant_bool:
                lane = "HIGH_PRIORITY_DIRECT_TEST_ADJUDICATION"
                counters[lane] += 1
                decision["notes"] = (
                    "VERIFIED_OA_FULLTEXT_ROUTE_ACCESS_QUANT_SIGNALS_PRESENT;"
                    "DIRECTION_NOT_CODED"
                )
            elif access_bool:
                lane = "ACCESS_ROUTE_PRESENT_QUANT_UNRESOLVED"
                counters[lane] += 1
                decision["notes"] = (
                    "VERIFIED_OA_FULLTEXT_ROUTE_ACCESS_SIGNALS_PRESENT;"
                    "QUANTITATIVE_TEST_UNRESOLVED;DIRECTION_NOT_CODED"
                )
            else:
                lane = "ROUTE_PRESENT_ACCESS_UNRESOLVED"
                counters[lane] += 1
                decision["notes"] = (
                    "VERIFIED_OA_FULLTEXT_ROUTE_SIGNAL_PRESENT;"
                    "ACCESS_PREDICTOR_UNRESOLVED;DIRECTION_NOT_CODED"
                )

        audit.append({
            "frame_id": fid,
            "doi": decision["doi"].strip(),
            "title": decision["title"].strip(),
            "year": decision["year"].strip(),
            "pdf_attempts": str(attempts),
            "pdf_retrieved": "YES" if retrieved else "NO",
            "extraction_verified": "YES" if verified else "NO",
            "text_chars": str(len(text)),
            "title_token_coverage": f"{coverage:.4f}" if retrieved else "",
            "route_signal": route,
            "access_signal": access_signal,
            "quantitative_signal": quant_signal,
            "triage_lane": lane,
            "source_identifier": source_url or "",
        })

    output_decisions_path.parent.mkdir(parents=True, exist_ok=True)
    with output_decisions_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    with audit_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(audit)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_OA_FULLTEXT_SIGNAL_SCREEN_V1",
        "status": "DIRECTION_BLIND_OA_FULLTEXT_SIGNAL_SCREEN_COMPLETE",
        "candidate_records": len(audit),
        "triage_lane_counts": dict(sorted(counters.items())),
        "auto_excluded_verified_no_route_signal": counters[
            "AUTO_EXCLUDED_NO_ROUTE_SIGNAL_IN_VERIFIED_FULLTEXT"
        ],
        "high_priority_direct_test_adjudication": counters[
            "HIGH_PRIORITY_DIRECT_TEST_ADJUDICATION"
        ],
        "effect_direction_inspected": False,
        "pdf_bytes_persisted": False,
        "fulltext_text_persisted": False,
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
    parser.add_argument("--output-decisions", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.access_queue,
        args.decisions,
        args.output_decisions,
        args.audit,
        args.receipt,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
