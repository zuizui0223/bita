"""Generate the formal finite-frame direct-geometry recurrence summary.

The summary is descriptive at the independent biological-program level. It does
not calculate a p-value or pooled effect and does not alter the primary k=2
network statistic.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.validate_direct_access_geometry_fulltext_decisions import validate as validate_fulltext
from scripts.validate_leal2025_direct_geometry_screen import validate as validate_historical

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
DEFAULT_HISTORICAL_SCREEN = BASE / "LEAL2025_DIRECT_GEOMETRY_SCREEN_V1.csv"
DEFAULT_CROSSWALK = BASE / "DIRECT_ACCESS_GEOMETRY_LEAL2025_CROSSWALK_V1.csv"

DIRECTIONS = ("POSITIVE", "NULL", "OPPOSITE", "MIXED")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(
    screen_path: Path,
    decisions_path: Path,
    bootstrap_receipt_path: Path,
    *,
    historical_screen_path: Path = DEFAULT_HISTORICAL_SCREEN,
    crosswalk_path: Path = DEFAULT_CROSSWALK,
) -> dict[str, object]:
    bootstrap = json.loads(bootstrap_receipt_path.read_text(encoding="utf-8"))
    if (
        bootstrap.get("schema")
        != "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_V1"
    ):
        raise ValueError("FORMAL_SUMMARY_WRONG_BOOTSTRAP_RECEIPT_SCHEMA")
    allowed_bootstrap_statuses = {
        "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_COMPLETE",
        "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_ACCOUNTED_PROVIDER_ABSENCE",
    }
    if bootstrap.get("status") not in allowed_bootstrap_statuses:
        raise ValueError("FORMAL_SUMMARY_KNOWN_CORPUS_RECALL_INCOMPLETE")
    known_count = int(bootstrap.get("known_direct_corpus_programs", -1))
    matched_count = int(bootstrap.get("known_programs_matched", -1))
    unmatched = list(bootstrap.get("known_programs_unmatched") or [])
    provider_absent = list(
        bootstrap.get("known_programs_provider_absent") or []
    )
    unresolved = list(
        bootstrap.get("known_programs_unresolved") or []
    )
    if (
        known_count != 24
        or matched_count + len(provider_absent) != 24
        or unresolved != []
        or sorted(unmatched) != sorted(provider_absent)
    ):
        raise ValueError(
            "FORMAL_SUMMARY_EXPECTED_ACCOUNTED_24_PROGRAM_RECALL:"
            f"known={known_count}:matched={matched_count}:"
            f"provider_absent={provider_absent}:unresolved={unresolved}:"
            f"unmatched={unmatched}"
        )
    if bootstrap.get("unknown_record_direction_coded") is not False:
        raise ValueError("FORMAL_SUMMARY_BOOTSTRAP_DIRECTION_LEAK")
    if bootstrap.get("formal_recurrence_result_open") is not False:
        raise ValueError("FORMAL_SUMMARY_BOOTSTRAP_ALREADY_OPEN")

    historical = validate_historical(historical_screen_path)
    if historical["eligible_direct_geometry_test"] != 4:
        raise ValueError("FORMAL_SUMMARY_HISTORICAL_ELIGIBLE_SET_NOT_FOUR")
    if historical["eligible_directions"] != {
        "POSITIVE": 2,
        "NULL": 1,
        "OPPOSITE": 0,
        "MIXED": 1,
    }:
        raise ValueError("FORMAL_SUMMARY_HISTORICAL_DIRECTION_SET_CHANGED")

    fulltext = validate_fulltext(
        screen_path,
        decisions_path,
        require_complete=True,
    )
    if not fulltext["fulltext_screen_complete"]:
        raise ValueError("FORMAL_SUMMARY_FULLTEXT_NOT_COMPLETE")
    if fulltext["pending_records"] != 0:
        raise ValueError("FORMAL_SUMMARY_PENDING_RECORDS_REMAIN")
    if not fulltext["biological_program_ids_unique"]:
        raise ValueError("FORMAL_SUMMARY_PROGRAM_IDS_NOT_UNIQUE")

    decisions = _read_csv(decisions_path)
    source_dbs = sorted({
        row["source_dbs"].strip()
        for row in decisions
        if row["source_dbs"].strip()
    })
    if len(source_dbs) != 1:
        raise ValueError(
            "FORMAL_SUMMARY_EXPECTED_SINGLE_SOURCE_DB:" + ",".join(source_dbs)
        )

    eligible_rows = [
        row for row in decisions
        if row["decision_status"].strip() == "ELIGIBLE_DIRECT"
    ]
    eligible_ids = {row["biological_program_id"].strip() for row in eligible_rows}
    if "" in eligible_ids:
        raise ValueError("FORMAL_SUMMARY_EMPTY_ELIGIBLE_PROGRAM_ID")

    preexisting_rows = [
        row for row in eligible_rows
        if row["decision_basis"].strip().startswith("PREEXISTING_")
    ]
    if len(preexisting_rows) != matched_count:
        raise ValueError(
            "FORMAL_SUMMARY_PREEXISTING_RECOVERY_COUNT_MISMATCH:"
            f"expected={matched_count}:observed={len(preexisting_rows)}"
        )
    recovered_preexisting_ids = {
        row["biological_program_id"].strip() for row in preexisting_rows
    }
    leaked_provider_absent = sorted(
        set(provider_absent) & recovered_preexisting_ids
    )
    if leaked_provider_absent:
        raise ValueError(
            "FORMAL_SUMMARY_PROVIDER_ABSENT_PROGRAM_ENTERED_DENOMINATOR:"
            + ",".join(leaked_provider_absent)
        )

    crosswalk = _read_csv(crosswalk_path)
    historical_direct_ids = {
        row["direct_study_id"].strip()
        for row in crosswalk
        if row["leal2025_frame_status"].strip() == "IN_FRAME"
    }
    if len(historical_direct_ids) != 4:
        raise ValueError(
            f"FORMAL_SUMMARY_EXPECTED_4_HISTORICAL_CROSSWALK:{len(historical_direct_ids)}"
        )
    missing_historical = sorted(historical_direct_ids - eligible_ids)
    if missing_historical:
        raise ValueError(
            "FORMAL_SUMMARY_HISTORICAL_PROGRAM_NOT_IN_ELIGIBLE_FRAME:"
            + ",".join(missing_historical)
        )

    direction_counts = Counter(row["direction"].strip() for row in eligible_rows)
    observed_keys = set(direction_counts)
    if observed_keys - set(DIRECTIONS):
        raise ValueError(
            "FORMAL_SUMMARY_INVALID_DIRECTIONS:"
            + ",".join(sorted(observed_keys - set(DIRECTIONS)))
        )

    new_rows = [
        row for row in eligible_rows
        if not row["decision_basis"].strip().startswith("PREEXISTING_")
    ]
    new_directions = Counter(row["direction"].strip() for row in new_rows)

    result = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1",
        "status": "FORMAL_FINITE_FRAME_DIRECTION_SUMMARY_OPEN",
        "frame_records": fulltext["frame_records"],
        "source_db": source_dbs[0],
        "eligible_direct_programs": len(eligible_rows),
        "direction_counts": {
            key: direction_counts.get(key, 0) for key in DIRECTIONS
        },
        "preexisting_direct_programs_recovered": len(preexisting_rows),
        "preexisting_provider_absent_programs": len(provider_absent),
        "preexisting_provider_absent_program_ids": sorted(provider_absent),
        "known_corpus_programs_accounted": matched_count + len(provider_absent),
        "new_eligible_programs_from_formal_frame": len(new_rows),
        "new_eligible_direction_counts": {
            key: new_directions.get(key, 0) for key in DIRECTIONS
        },
        "duplicate_bibliographic_records": fulltext["duplicate_records"],
        "ineligible_bibliographic_records": fulltext["ineligible_records"],
        "historical_direct_eligible_programs": 4,
        "historical_direct_directions": historical["eligible_directions"],
        "historical_anchor_double_counted": False,
        "formal_recurrence_descriptive_summary_open": True,
        "formal_direction_p_value_computed": False,
        "pooled_effect_computed": False,
        "natural_prevalence_estimated": False,
        "primary_standardized_network_k": 2,
        "claim": (
            "Within the frozen Q1-Q8 bibliographic frame, "
            f"{len(eligible_rows)} independent study programs directly tested the "
            "access-geometry to nectar-robbery relation; directions were "
            f"{direction_counts.get('POSITIVE', 0)} positive, "
            f"{direction_counts.get('NULL', 0)} null, "
            f"{direction_counts.get('OPPOSITE', 0)} opposite and "
            f"{direction_counts.get('MIXED', 0)} mixed. "
            "This is a finite-frame evidence distribution, not natural prevalence "
            "and not an additional network-level replication count. "
            f"{len(provider_absent)} pre-existing direct program(s) independently "
            "verified as absent from the selected bibliographic provider are reported "
            "outside the formal denominator."
        ),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--bootstrap-receipt", type=Path, required=True)
    parser.add_argument("--historical-screen", type=Path, default=DEFAULT_HISTORICAL_SCREEN)
    parser.add_argument("--crosswalk", type=Path, default=DEFAULT_CROSSWALK)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = summarize(
        args.screen,
        args.decisions,
        args.bootstrap_receipt,
        historical_screen_path=args.historical_screen,
        crosswalk_path=args.crosswalk,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
