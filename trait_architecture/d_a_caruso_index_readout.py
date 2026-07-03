"""Classify the Caruso primary-index route after bounded source checks.

This combines the manifest and XLSX-schema *receipts* into a final route verdict.
It distinguishes no index candidate from a public-file access block, so an HTTP 401
before workbook parsing is never misreported as absence of bibliographic columns.
It never reads any study data or adds a Part B effect.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping


DO_NOT_INFER = (
    "Route readout only. Do not infer primary-study identifiers, trait-to-antagonism routes, selection gradients, "
    "effect values, denominators, uncertainty, or B2 eligibility."
)


def _text(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def classify_index_route(
    manifest_rows: Iterable[Mapping[str, str]],
    schema_rows: Iterable[Mapping[str, str]],
) -> dict[str, object]:
    """Return one honest next action from bounded discovery receipts."""

    manifest = list(manifest_rows)
    schema = list(schema_rows)
    manifest_files = [row for row in manifest if _text(row.get("access_status")) == "file_manifest_entry"]
    exp_stud_files = [
        row for row in manifest_files
        if "exp_stud" in _text(row.get("filename")).casefold()
        or _text(row.get("primary_study_index_candidate")) == "true"
    ]
    recovered = [row for row in schema if _text(row.get("download_status")) == "schema_recovered"]
    blocked = [row for row in schema if _text(row.get("download_status")) == "download_or_parse_failed"]
    bibliographic = [
        row for row in recovered
        if _text(row.get("schema_decision")) == "bibliographic_index_columns_present_needs_identifier_extraction"
    ]

    if bibliographic:
        next_action = "extract_bibliographic_identifiers_only"
        verdict = "schema_recovered_with_bibliographic_identifier_columns"
    elif blocked:
        has_401 = any("download_http_401" in _text(row.get("schema_decision")) for row in blocked)
        next_action = (
            "retain_caruso_as_system_seed_only_public_xlsx_download_unauthorized"
            if has_401 else "retain_caruso_as_system_seed_only_public_xlsx_schema_access_blocked"
        )
        verdict = "public_xlsx_access_blocked_before_schema"
    elif exp_stud_files and recovered:
        next_action = "stop_before_row_level_extraction_no_bibliographic_identifier_columns"
        verdict = "xlsx_schema_recovered_without_bibliographic_identifier_columns"
    elif exp_stud_files:
        next_action = "retain_caruso_as_system_seed_only_schema_not_recovered"
        verdict = "candidate_xlsx_without_schema_receipt"
    else:
        next_action = "retain_caruso_as_system_seed_only_no_primary_study_index_file_candidate"
        verdict = "no_primary_study_index_file_candidate"

    return {
        "manifest_file_count": len(manifest_files),
        "experimental_study_xlsx_candidate_count": len(exp_stud_files),
        "schema_receipt_count": len(schema),
        "schema_recovered_count": len(recovered),
        "schema_access_blocked_count": len(blocked),
        "bibliographic_identifier_schema_count": len(bibliographic),
        "route_verdict": verdict,
        "next_action": next_action,
        "decision_boundary": DO_NOT_INFER,
    }


def write_readout(
    out_dir: str | Path,
    *,
    manifest_csv: str | Path,
    schema_csv: str | Path,
) -> dict[str, object]:
    report = classify_index_route(read_csv(manifest_csv), read_csv(schema_csv))
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "d_a_caruso_index_route_readout.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
