"""Safely ingest one ZIP containing the complete Q1-Q8 bibliographic export packet."""
from __future__ import annotations

import argparse
import json
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from scripts.prepare_direct_access_geometry_bibliographic_frame import prepare

ALLOWED_QUERY_SUFFIXES = {".csv", ".tsv", ".txt", ".json"}
COUNT_NAME = "QUERY_COUNTS.csv"
MAX_FILES = 9
MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_TOTAL_BYTES = 200 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200.0


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def _validate_member(info: zipfile.ZipInfo) -> None:
    name = info.filename
    posix = PurePosixPath(name)

    if info.is_dir():
        raise ValueError(f"BIB_ZIP_DIRECTORIES_NOT_ALLOWED:{name}")
    if posix.is_absolute() or ".." in posix.parts:
        raise ValueError(f"BIB_ZIP_UNSAFE_PATH:{name}")
    if len(posix.parts) != 1:
        raise ValueError(f"BIB_ZIP_NESTED_PATH_NOT_ALLOWED:{name}")
    if _is_symlink(info):
        raise ValueError(f"BIB_ZIP_SYMLINK_NOT_ALLOWED:{name}")
    if info.file_size < 0 or info.file_size > MAX_FILE_BYTES:
        raise ValueError(f"BIB_ZIP_FILE_TOO_LARGE:{name}:{info.file_size}")
    if info.compress_size == 0:
        ratio = float("inf") if info.file_size else 1.0
    else:
        ratio = info.file_size / info.compress_size
    if ratio > MAX_COMPRESSION_RATIO:
        raise ValueError(f"BIB_ZIP_COMPRESSION_RATIO_TOO_HIGH:{name}:{ratio:.1f}")


def _expected_names(names: list[str]) -> None:
    if len(names) != MAX_FILES:
        raise ValueError(f"BIB_ZIP_EXPECTED_9_FILES:{len(names)}")
    if len(set(names)) != len(names):
        raise ValueError("BIB_ZIP_DUPLICATE_FILENAMES")
    if COUNT_NAME not in names:
        raise ValueError(f"BIB_ZIP_MISSING_COUNT_MANIFEST:{COUNT_NAME}")

    query_files = [name for name in names if name != COUNT_NAME]
    observed = {}
    for name in query_files:
        path = Path(name)
        qid = path.stem.upper()
        if qid not in {f"Q{i}" for i in range(1, 9)}:
            raise ValueError(f"BIB_ZIP_INVALID_QUERY_FILENAME:{name}")
        if path.suffix.lower() not in ALLOWED_QUERY_SUFFIXES:
            raise ValueError(f"BIB_ZIP_UNSUPPORTED_QUERY_FORMAT:{name}")
        if qid in observed:
            raise ValueError(f"BIB_ZIP_MULTIPLE_QUERY_FILES:{qid}")
        observed[qid] = name

    missing = [f"Q{i}" for i in range(1, 9) if f"Q{i}" not in observed]
    if missing:
        raise ValueError("BIB_ZIP_MISSING_QUERY_FILES:" + ",".join(missing))


def ingest(
    archive: Path,
    output_dir: Path,
    *,
    search_date: str,
    source_db: str | None = None,
) -> dict[str, object]:
    if not archive.is_file():
        raise ValueError(f"BIB_ZIP_NOT_FOUND:{archive}")
    if not zipfile.is_zipfile(archive):
        raise ValueError("BIB_ZIP_INVALID_ARCHIVE")

    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        if len(infos) > MAX_FILES:
            raise ValueError(f"BIB_ZIP_TOO_MANY_FILES:{len(infos)}")
        total = 0
        for info in infos:
            _validate_member(info)
            total += info.file_size
            if total > MAX_TOTAL_BYTES:
                raise ValueError(f"BIB_ZIP_TOTAL_TOO_LARGE:{total}")
        names = [info.filename for info in infos]
        _expected_names(names)

        with tempfile.TemporaryDirectory(prefix="bita_bib_zip_") as tmp:
            extracted = Path(tmp)
            for info in infos:
                target = extracted / info.filename
                with zf.open(info, "r") as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst, length=1 << 20)

            result = prepare(
                extracted,
                output_dir,
                search_date=search_date,
                count_manifest=extracted / COUNT_NAME,
                source_db=source_db,
            )

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_ZIP_INTAKE_V1",
        "status": "Q1_Q8_ZIP_INGESTED_OUTCOME_BLIND",
        "archive_name": archive.name,
        "archive_bytes": archive.stat().st_size,
        "uncompressed_bytes": total,
        "archive_files": sorted(names),
        "source_db": result["source_db"],
        "search_date": search_date,
        "all_query_export_counts_verified": result["all_query_export_counts_verified"],
        "input_rows": result["input_rows"],
        "unique_bibliographic_records": result["unique_bibliographic_records"],
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_ZIP_INTAKE_RECEIPT_V1.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", dest="archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--search-date", required=True)
    parser.add_argument("--source-db")
    args = parser.parse_args()
    print(json.dumps(
        ingest(
            args.archive,
            args.output_dir,
            search_date=args.search_date,
            source_db=args.source_db,
        ),
        indent=2,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
