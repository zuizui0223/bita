"""Normalize Q1-Q8 exports from one bibliographic source and freeze the frame."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.build_direct_access_geometry_bibliographic_frame import (
    build,
    write_frame,
)
from scripts.normalize_direct_access_geometry_bibliographic_export import (
    normalize,
    write,
)

QUERY_IDS = tuple(f"Q{i}" for i in range(1, 9))
SUPPORTED_SUFFIXES = {".csv", ".tsv", ".txt", ".json"}
COUNT_FIELDS = ("query_id", "source_db", "reported_total_rows", "search_date")


def _read_count_manifest(path: Path) -> dict[str, dict[str, str]]:
    import csv

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        observed = tuple(reader.fieldnames or ())
        if observed != COUNT_FIELDS:
            raise ValueError(
                f"BIB_INTAKE_COUNT_MANIFEST_SCHEMA_MISMATCH:"
                f"expected={COUNT_FIELDS}:observed={observed}"
            )
        rows = list(reader)

    if len(rows) != 8:
        raise ValueError(f"BIB_INTAKE_COUNT_MANIFEST_EXPECTED_8_ROWS:{len(rows)}")
    mapped: dict[str, dict[str, str]] = {}
    for row in rows:
        qid = row["query_id"].strip()
        if qid not in QUERY_IDS:
            raise ValueError(f"BIB_INTAKE_COUNT_MANIFEST_INVALID_QUERY:{qid}")
        if qid in mapped:
            raise ValueError(f"BIB_INTAKE_COUNT_MANIFEST_DUPLICATE_QUERY:{qid}")
        try:
            total = int(row["reported_total_rows"].strip())
        except ValueError as exc:
            raise ValueError(
                f"BIB_INTAKE_COUNT_MANIFEST_INVALID_TOTAL:{qid}:"
                f"{row['reported_total_rows']}"
            ) from exc
        if total <= 0:
            raise ValueError(f"BIB_INTAKE_COUNT_MANIFEST_NONPOSITIVE_TOTAL:{qid}:{total}")
        mapped[qid] = {
            "query_id": qid,
            "source_db": row["source_db"].strip(),
            "reported_total_rows": str(total),
            "search_date": row["search_date"].strip(),
        }
    missing = [qid for qid in QUERY_IDS if qid not in mapped]
    if missing:
        raise ValueError("BIB_INTAKE_COUNT_MANIFEST_MISSING_QUERY:" + ",".join(missing))
    return mapped


def _find_query_file(input_dir: Path, query_id: str) -> Path:
    matches = sorted(
        path for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_SUFFIXES
        and path.stem.upper() == query_id
    )
    if not matches:
        raise ValueError(f"BIB_INTAKE_MISSING_QUERY_FILE:{query_id}")
    if len(matches) > 1:
        raise ValueError(
            f"BIB_INTAKE_MULTIPLE_QUERY_FILES:{query_id}:"
            + ",".join(path.name for path in matches)
        )
    return matches[0]


def prepare(
    input_dir: Path,
    output_dir: Path,
    *,
    search_date: str,
    count_manifest: Path,
    source_db: str | None = None,
) -> dict[str, object]:
    if not input_dir.is_dir():
        raise ValueError(f"BIB_INTAKE_INPUT_DIR_NOT_FOUND:{input_dir}")

    counts = _read_count_manifest(count_manifest)
    normalized_dir = output_dir / "normalized_raw"
    normalized_paths: list[Path] = []
    source_dbs: set[str] = set()
    per_query: dict[str, dict[str, object]] = {}

    for query_id in QUERY_IDS:
        source_path = _find_query_file(input_dir, query_id)
        rows = normalize(
            source_path,
            fmt="auto",
            source_db=source_db,
            query_id=query_id,
            search_date=search_date,
        )
        providers = {row["source_db"] for row in rows}
        if len(providers) != 1:
            raise ValueError(f"BIB_INTAKE_MULTIPLE_PROVIDERS_WITHIN_QUERY:{query_id}")
        provider = next(iter(providers))
        source_dbs.add(provider)

        expected = counts[query_id]
        if expected["source_db"] != provider:
            raise ValueError(
                f"BIB_INTAKE_COUNT_SOURCE_MISMATCH:{query_id}:"
                f"manifest={expected['source_db']}:export={provider}"
            )
        if expected["search_date"] != search_date:
            raise ValueError(
                f"BIB_INTAKE_COUNT_SEARCH_DATE_MISMATCH:{query_id}:"
                f"manifest={expected['search_date']}:requested={search_date}"
            )
        expected_rows = int(expected["reported_total_rows"])
        if expected_rows != len(rows):
            raise ValueError(
                f"BIB_INTAKE_INCOMPLETE_EXPORT:{query_id}:"
                f"reported={expected_rows}:rows={len(rows)}"
            )

        out_path = normalized_dir / f"{query_id}.csv"
        write(rows, out_path)
        normalized_paths.append(out_path)
        per_query[query_id] = {
            "source_file": source_path.name,
            "normalized_file": str(out_path.relative_to(output_dir)),
            "rows": len(rows),
            "source_db": provider,
        }

    if len(source_dbs) != 1:
        raise ValueError(
            "BIB_INTAKE_MIXED_SOURCE_DATABASES:" + ",".join(sorted(source_dbs))
        )

    frame, receipt = build(normalized_paths)
    frame_path = output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv"
    receipt_path = output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_RECEIPT_V1.json"
    write_frame(frame, frame_path)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    intake = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_INTAKE_V1",
        "status": "OUTCOME_BLIND_Q1_Q8_FRAME_PREPARED",
        "source_db": next(iter(source_dbs)),
        "search_date": search_date,
        "queries": per_query,
        "count_manifest": count_manifest.name,
        "all_query_export_counts_verified": True,
        "input_rows": receipt["input_rows"],
        "unique_bibliographic_records": receipt["unique_bibliographic_records"],
        "duplicate_rows_collapsed": receipt["duplicate_rows_collapsed"],
        "frame_file": frame_path.name,
        "frame_receipt_file": receipt_path.name,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
    }
    (output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_INTAKE_RECEIPT_V1.json").write_text(
        json.dumps(intake, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return intake


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--search-date", required=True)
    parser.add_argument("--count-manifest", type=Path, required=True)
    parser.add_argument("--source-db")
    args = parser.parse_args()

    result = prepare(
        args.input_dir,
        args.output_dir,
        search_date=args.search_date,
        count_manifest=args.count_manifest,
        source_db=args.source_db,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
