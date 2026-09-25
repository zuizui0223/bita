"""Build a deterministic outcome-blind bibliographic update frame."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = (
    "source_db",
    "query_id",
    "record_id",
    "doi",
    "title",
    "year",
    "authors",
    "publication",
    "url",
    "search_date",
)
QUERY_IDS = tuple(f"Q{i}" for i in range(1, 9))
MIN_YEAR = 2000
MAX_YEAR = 2026


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm_doi(value: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.rstrip(" .;,") if text else ""


def _norm_title(value: str) -> str:
    text = (value or "").casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        observed = tuple(reader.fieldnames or ())
        if observed != REQUIRED_COLUMNS:
            raise ValueError(
                f"BIB_FRAME_SCHEMA_MISMATCH:{path}:"
                f"expected={REQUIRED_COLUMNS}:observed={observed}"
            )
        return list(reader)


def build(inputs: list[Path]) -> tuple[list[dict[str, str]], dict[str, object]]:
    if not inputs:
        raise ValueError("BIB_FRAME_NO_INPUTS")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    query_counts = {qid: 0 for qid in QUERY_IDS}
    input_rows = 0
    input_receipts = []

    for path in inputs:
        rows = _read(path)
        input_receipts.append({
            "path": path.name,
            "sha256": _sha256(path),
            "rows": len(rows),
        })
        for row in rows:
            input_rows += 1
            qid = row["query_id"].strip()
            if qid not in QUERY_IDS:
                raise ValueError(f"BIB_FRAME_INVALID_QUERY_ID:{qid}")
            query_counts[qid] += 1

            title = row["title"].strip()
            if not title:
                raise ValueError("BIB_FRAME_MISSING_TITLE")
            try:
                year = int(row["year"].strip())
            except ValueError as exc:
                raise ValueError(f"BIB_FRAME_INVALID_YEAR:{row['year']}") from exc
            if year < MIN_YEAR or year > MAX_YEAR:
                raise ValueError(f"BIB_FRAME_YEAR_OUT_OF_RANGE:{year}")

            doi = _norm_doi(row["doi"])
            nt = _norm_title(title)
            if not nt:
                raise ValueError("BIB_FRAME_EMPTY_NORMALIZED_TITLE")
            key = f"doi:{doi}" if doi else f"title-year:{nt}|{year}"
            copied = dict(row)
            copied["_doi"] = doi
            copied["_year"] = str(year)
            copied["_key"] = key
            grouped[key].append(copied)

    missing_queries = [qid for qid, n in query_counts.items() if n == 0]
    if missing_queries:
        raise ValueError("BIB_FRAME_MISSING_FROZEN_QUERIES:" + ",".join(missing_queries))

    frame = []
    for key in sorted(grouped):
        rows = grouped[key]
        canonical = sorted(
            rows,
            key=lambda r: (
                r["title"].casefold(),
                r["source_db"].casefold(),
                r["record_id"],
            ),
        )[0]
        frame_id = "bib_" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        frame.append({
            "frame_id": frame_id,
            "dedupe_key": key,
            "doi": canonical["_doi"],
            "title": canonical["title"].strip(),
            "year": canonical["_year"],
            "authors": canonical["authors"].strip(),
            "publication": canonical["publication"].strip(),
            "source_dbs": "|".join(sorted({r["source_db"].strip() for r in rows})),
            "query_ids": "|".join(sorted({r["query_id"].strip() for r in rows})),
            "source_record_ids": "|".join(sorted({
                f"{r['source_db'].strip()}:{r['record_id'].strip()}" for r in rows
            })),
            "source_urls": "|".join(sorted({r["url"].strip() for r in rows if r["url"].strip()})),
            "raw_rows_collapsed": str(len(rows)),
        })

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1",
        "status": "OUTCOME_BLIND_FRAME_FROZEN",
        "publication_window": {
            "from": "2000-01-01",
            "through": "2026-09-24",
        },
        "frozen_query_ids": list(QUERY_IDS),
        "query_raw_row_counts": query_counts,
        "input_rows": input_rows,
        "unique_bibliographic_records": len(frame),
        "duplicate_rows_collapsed": input_rows - len(frame),
        "inputs": input_receipts,
        "outcome_direction_coded": False,
        "biological_independence_adjudicated": False,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
    }
    return frame, receipt


def write_frame(frame: list[dict[str, str]], output: Path) -> None:
    fields = (
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
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(frame)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    frame, receipt = build(args.input)
    write_frame(frame, args.output)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
