"""Bootstrap formal bibliographic screening from the frozen frame.

This runs only after the outcome-blind bibliographic frame has been frozen.
It annotates records already represented in the bounded 24-program direct corpus,
then leaves every other record pending for full-text eligibility screening.

Known-program matching:
1. DOI, when present in the direct corpus.
2. Normalized title + year aliases only for direct-corpus programs without a DOI.

No unknown record receives an effect direction in this step.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
DEFAULT_CORPUS = BASE / "DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv"
DEFAULT_ALIASES = BASE / "DIRECT_ACCESS_GEOMETRY_KNOWN_TITLE_ALIASES_V1.csv"

FRAME_FIELDS = (
    "frame_id",
    "dedupe_key",
    "doi",
    "title",
    "year",
    "authors",
    "publication",
    "source_dbs",
    "query_ids",
    "source_record_ids",
    "source_urls",
    "raw_rows_collapsed",
)
OUTPUT_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "source_dbs",
    "query_ids",
    "screen_status",
    "known_study_id",
    "known_direction",
    "eligibility_status",
    "direction",
    "screening_notes",
)

PROVIDER_EXCEPTION_FIELDS = (
    "study_id",
    "source_db",
    "provider_check",
    "provider_result_count",
    "external_verification",
    "adjudication",
    "notes",
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm_doi(value: str) -> str:
    text = (value or "").strip().casefold()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.rstrip(" .;,")


def _norm_title(value: str) -> str:
    text = (value or "").casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def bootstrap(
    frame_path: Path,
    frame_receipt_path: Path,
    *,
    corpus_path: Path = DEFAULT_CORPUS,
    alias_path: Path = DEFAULT_ALIASES,
    provider_coverage_exceptions_path: Path | None = None,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    frame = _read(frame_path)
    corpus = _read(corpus_path)
    aliases = _read(alias_path)
    receipt = json.loads(frame_receipt_path.read_text(encoding="utf-8"))

    if receipt.get("schema") != "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1":
        raise ValueError("BIB_SCREEN_WRONG_FRAME_RECEIPT_SCHEMA")
    if receipt.get("status") != "OUTCOME_BLIND_FRAME_FROZEN":
        raise ValueError("BIB_SCREEN_FRAME_NOT_FROZEN")
    if receipt.get("formal_recurrence_result_open") is not False:
        raise ValueError("BIB_SCREEN_FRAME_RECEIPT_RECURRING_RESULT_ALREADY_OPEN")

    if not frame:
        raise ValueError("BIB_SCREEN_EMPTY_FRAME")
    observed = tuple(frame[0].keys())
    if observed != FRAME_FIELDS:
        raise ValueError(
            f"BIB_SCREEN_FRAME_SCHEMA_MISMATCH:expected={FRAME_FIELDS}:observed={observed}"
        )
    if len(frame) != int(receipt.get("unique_bibliographic_records", -1)):
        raise ValueError("BIB_SCREEN_FRAME_RECEIPT_COUNT_MISMATCH")

    allowed_directions = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}
    doi_map: dict[str, dict[str, str]] = {}
    no_doi_studies: set[str] = set()
    corpus_by_id: dict[str, dict[str, str]] = {}

    for row in corpus:
        sid = row["study_id"].strip()
        if not sid:
            raise ValueError("BIB_SCREEN_CORPUS_EMPTY_STUDY_ID")
        if sid in corpus_by_id:
            raise ValueError(f"BIB_SCREEN_CORPUS_DUPLICATE_STUDY_ID:{sid}")
        corpus_by_id[sid] = row
        direction = row["direction"].strip()
        if direction not in allowed_directions:
            raise ValueError(f"BIB_SCREEN_CORPUS_INVALID_DIRECTION:{sid}:{direction}")

        doi = _norm_doi(row.get("doi", ""))
        if doi:
            if doi in doi_map:
                raise ValueError(
                    f"BIB_SCREEN_CORPUS_DUPLICATE_DOI:{doi}:"
                    f"{doi_map[doi]['study_id']}:{sid}"
                )
            doi_map[doi] = row
        else:
            no_doi_studies.add(sid)

    alias_map: dict[tuple[str, str], dict[str, str]] = {}
    alias_studies: set[str] = set()
    for row in aliases:
        sid = row["study_id"].strip()
        year = row["year"].strip()
        title = _norm_title(row["title_alias"])
        if sid not in corpus_by_id:
            raise ValueError(f"BIB_SCREEN_ALIAS_UNKNOWN_STUDY:{sid}")
        if _norm_doi(corpus_by_id[sid].get("doi", "")):
            raise ValueError(f"BIB_SCREEN_ALIAS_ONLY_ALLOWED_FOR_DOILESS:{sid}")
        if not year or not title:
            raise ValueError(f"BIB_SCREEN_ALIAS_MISSING_KEY:{sid}")
        key = (title, year)
        if key in alias_map:
            raise ValueError(f"BIB_SCREEN_DUPLICATE_TITLE_YEAR_ALIAS:{sid}")
        alias_map[key] = corpus_by_id[sid]
        alias_studies.add(sid)

    if alias_studies != no_doi_studies:
        missing = sorted(no_doi_studies - alias_studies)
        extra = sorted(alias_studies - no_doi_studies)
        raise ValueError(
            f"BIB_SCREEN_DOILESS_ALIAS_COVERAGE_MISMATCH:"
            f"missing={missing}:extra={extra}"
        )

    frame_source_dbs = sorted({row["source_dbs"].strip() for row in frame if row["source_dbs"].strip()})
    if len(frame_source_dbs) != 1:
        raise ValueError(
            "BIB_SCREEN_EXPECTED_SINGLE_SOURCE_DB:" + ",".join(frame_source_dbs)
        )
    frame_source_db = frame_source_dbs[0]

    provider_absent: set[str] = set()
    provider_exception_sha256 = None
    if provider_coverage_exceptions_path is not None:
        with provider_coverage_exceptions_path.open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            reader = csv.DictReader(handle)
            observed_exception_fields = tuple(reader.fieldnames or ())
            if observed_exception_fields != PROVIDER_EXCEPTION_FIELDS:
                raise ValueError(
                    "BIB_SCREEN_PROVIDER_EXCEPTION_SCHEMA_MISMATCH:"
                    f"expected={PROVIDER_EXCEPTION_FIELDS}:"
                    f"observed={observed_exception_fields}"
                )
            exception_rows = list(reader)

        for exception in exception_rows:
            sid = exception["study_id"].strip()
            if not sid or sid in provider_absent:
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_BAD_STUDY_ID:{sid}"
                )
            if sid not in corpus_by_id:
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_UNKNOWN_STUDY:{sid}"
                )
            if exception["source_db"].strip() != frame_source_db:
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_SOURCE_MISMATCH:{sid}:"
                    f"frame={frame_source_db}:"
                    f"exception={exception['source_db'].strip()}"
                )
            try:
                provider_result_count = int(
                    exception["provider_result_count"].strip()
                )
            except ValueError as exc:
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_BAD_RESULT_COUNT:{sid}"
                ) from exc
            if provider_result_count != 0:
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_NONZERO_RESULT:{sid}:"
                    f"{provider_result_count}"
                )
            if (
                exception["adjudication"].strip()
                != "VERIFIED_PROVIDER_ABSENCE"
            ):
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_NOT_VERIFIED:{sid}"
                )
            if not exception["provider_check"].strip():
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_MISSING_CHECK:{sid}"
                )
            if not exception["external_verification"].strip():
                raise ValueError(
                    f"BIB_SCREEN_PROVIDER_EXCEPTION_MISSING_VERIFICATION:{sid}"
                )
            provider_absent.add(sid)
        provider_exception_sha256 = _sha256(
            provider_coverage_exceptions_path
        )

    output: list[dict[str, str]] = []
    matched_studies: set[str] = set()
    pending_ids: list[str] = []

    for row in frame:
        doi = _norm_doi(row["doi"])
        match: dict[str, str] | None = None
        match_method = ""
        if doi and doi in doi_map:
            match = doi_map[doi]
            match_method = "DOI"
        else:
            key = (_norm_title(row["title"]), row["year"].strip())
            if key in alias_map:
                match = alias_map[key]
                match_method = "TITLE_YEAR_ALIAS"

        if match is None:
            pending_ids.append(row["frame_id"])
            output.append({
                "frame_id": row["frame_id"],
                "doi": doi,
                "title": row["title"],
                "year": row["year"],
                "source_dbs": row["source_dbs"],
                "query_ids": row["query_ids"],
                "screen_status": "PENDING_FULLTEXT_ELIGIBILITY",
                "known_study_id": "",
                "known_direction": "",
                "eligibility_status": "PENDING",
                "direction": "",
                "screening_notes": "",
            })
            continue

        sid = match["study_id"].strip()
        if sid in matched_studies:
            raise ValueError(f"BIB_SCREEN_KNOWN_STUDY_MATCHED_MULTIPLE_FRAME_RECORDS:{sid}")
        matched_studies.add(sid)
        direction = match["direction"].strip()
        output.append({
            "frame_id": row["frame_id"],
            "doi": doi,
            "title": row["title"],
            "year": row["year"],
            "source_dbs": row["source_dbs"],
            "query_ids": row["query_ids"],
            "screen_status": "KNOWN_DIRECT_CORPUS_MATCH",
            "known_study_id": sid,
            "known_direction": direction,
            "eligibility_status": "KNOWN_ELIGIBLE_DIRECT",
            "direction": direction,
            "screening_notes": f"matched_by={match_method}",
        })

    unmatched_known = sorted(set(corpus_by_id) - matched_studies)
    stale_provider_exceptions = sorted(provider_absent - set(unmatched_known))
    if stale_provider_exceptions:
        raise ValueError(
            "BIB_SCREEN_PROVIDER_EXCEPTION_STUDY_WAS_RECOVERED:"
            + ",".join(stale_provider_exceptions)
        )
    accounted_provider_absent = sorted(set(unmatched_known) & provider_absent)
    unresolved_known = sorted(set(unmatched_known) - provider_absent)
    if not unmatched_known:
        status = "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_COMPLETE"
    elif not unresolved_known and accounted_provider_absent:
        status = (
            "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_"
            "RECALL_ACCOUNTED_PROVIDER_ABSENCE"
        )
    else:
        status = "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_INCOMPLETE"
    screen_receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_V1",
        "status": status,
        "frame_sha256": _sha256(frame_path),
        "frame_receipt_sha256": _sha256(frame_receipt_path),
        "direct_corpus_sha256": _sha256(corpus_path),
        "title_alias_sha256": _sha256(alias_path),
        "frame_records": len(frame),
        "known_direct_corpus_programs": len(corpus_by_id),
        "known_programs_matched": len(matched_studies),
        "known_programs_unmatched": unmatched_known,
        "known_programs_provider_absent": accounted_provider_absent,
        "known_programs_unresolved": unresolved_known,
        "provider_coverage_exceptions_applied": bool(provider_absent),
        "provider_coverage_exception_sha256": provider_exception_sha256,
        "pending_fulltext_records": len(pending_ids),
        "pending_frame_ids": pending_ids,
        "unknown_record_direction_coded": False,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
    }
    return output, screen_receipt


def write(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--frame-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    parser.add_argument("--provider-coverage-exceptions", type=Path)
    args = parser.parse_args()

    rows, receipt = bootstrap(
        args.frame,
        args.frame_receipt,
        corpus_path=args.corpus,
        alias_path=args.aliases,
        provider_coverage_exceptions_path=args.provider_coverage_exceptions,
    )
    write(rows, args.output)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
