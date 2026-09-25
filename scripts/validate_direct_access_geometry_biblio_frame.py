"""Validate the frozen bibliographic frame against known direct-study coverage."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
DEFAULT_FRAME = BASE / "DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_V1.csv"
DEFAULT_RECEIPT = BASE / "DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_RECEIPT_V1.json"
DEFAULT_DIRECT = BASE / "DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _norm_doi(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(
    frame_path: Path = DEFAULT_FRAME,
    receipt_path: Path = DEFAULT_RECEIPT,
    direct_path: Path = DEFAULT_DIRECT,
    *,
    require_known_coverage: bool = True,
) -> dict[str, object]:
    frame = _read(frame_path)
    direct = _read(direct_path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    if not frame:
        raise ValueError("BIBLIO_FRAME_EMPTY")
    if receipt.get("frame_sha256") != _sha256(frame_path):
        raise ValueError("BIBLIO_FRAME_SHA256_MISMATCH")
    if receipt.get("deduplicated_candidates") != len(frame):
        raise ValueError("BIBLIO_FRAME_COUNT_RECEIPT_MISMATCH")
    if any(row.get("screen_status") != "UNSCREENED" for row in frame):
        raise ValueError("BIBLIO_FRAME_PREMATURE_SCREENING")
    if any(
        row.get("larceny_text_match") != "true"
        and row.get("sentinel_query_match") != "true"
        for row in frame
    ):
        raise ValueError("BIBLIO_FRAME_CONTAINS_UNJUSTIFIED_NONLARCENY_ROW")

    frame_dois = {_norm_doi(row.get("doi", "")) for row in frame if _norm_doi(row.get("doi", ""))}
    known = [
        (row["study_id"], _norm_doi(row.get("doi", "")), row["direction"])
        for row in direct
        if _norm_doi(row.get("doi", ""))
    ]
    missing = [
        {"study_id": study_id, "doi": doi, "direction": direction}
        for study_id, doi, direction in known
        if doi not in frame_dois
    ]
    direction_totals: dict[str, int] = {}
    direction_missing: dict[str, int] = {}
    for _, _, direction in known:
        direction_totals[direction] = direction_totals.get(direction, 0) + 1
    for row in missing:
        direction = str(row["direction"])
        direction_missing[direction] = direction_missing.get(direction, 0) + 1

    result = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_VALIDATION_V1",
        "frame_candidates": len(frame),
        "known_direct_programs": len(direct),
        "known_direct_programs_with_doi": len(known),
        "known_doi_covered": len(known) - len(missing),
        "known_doi_missing": len(missing),
        "missing_known_programs": missing,
        "known_direction_totals": dict(sorted(direction_totals.items())),
        "missing_by_direction": dict(sorted(direction_missing.items())),
        "formal_recurrence_result_open": False,
    }
    if require_known_coverage and missing:
        detail = ",".join(f"{row['study_id']}:{row['doi']}" for row in missing)
        raise ValueError("BIBLIO_FRAME_MISSES_KNOWN_DIRECT_PROGRAMS:" + detail)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--direct", type=Path, default=DEFAULT_DIRECT)
    parser.add_argument("--allow-missing-known", action="store_true")
    args = parser.parse_args()
    result = validate(
        args.frame,
        args.receipt,
        args.direct,
        require_known_coverage=not args.allow_missing_known,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
