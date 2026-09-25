"""Apply source-adjudicated eligibility without coding effect direction.

Eligible records remain PENDING_FULLTEXT with an eligibility-frozen note until a
separate direction-coding stage. Ineligible records may close immediately because
their exclusion does not require inspecting the sign of the geometry-robbery effect.
Duplicate data records also remain pending until their biological target exists in
the final eligible-program ledger.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

ADJ_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "eligibility_state",
    "biological_program_id",
    "independence_relation",
    "decision_basis",
    "source_identifier",
    "direction_coded",
    "notes",
)

ELIGIBLE_STATES = {
    "ELIGIBLE_DIRECT_NEW",
    "ELIGIBLE_DIRECT_NETWORK_OVERLAP",
}
PENDING_DUPLICATE_STATES = {"DUPLICATE_DATA_RECORD"}


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def apply(
    decisions_path: Path,
    adjudication_paths: list[Path],
    output_path: Path,
    receipt_path: Path,
) -> dict[str, object]:
    decision_fields, decisions = _read(decisions_path)
    if decision_fields != FIELDS:
        raise ValueError("ELIG_APPLY_DECISION_SCHEMA_MISMATCH")
    by_id = {row["frame_id"].strip(): row for row in decisions}

    adjudications: dict[str, dict[str, str]] = {}
    for path in adjudication_paths:
        fields, rows = _read(path)
        if fields != ADJ_FIELDS:
            raise ValueError(
                f"ELIG_APPLY_ADJUDICATION_SCHEMA_MISMATCH:{path}"
            )
        for row in rows:
            fid = row["frame_id"].strip()
            if not fid or fid in adjudications:
                raise ValueError(f"ELIG_APPLY_DUPLICATE_ADJUDICATION:{fid}")
            adjudications[fid] = row

    applied_ineligible = 0
    frozen_eligible = 0
    pending_duplicates = 0

    for fid, adj in adjudications.items():
        decision = by_id.get(fid)
        if decision is None:
            raise ValueError(f"ELIG_APPLY_UNKNOWN_FRAME_ID:{fid}")
        if decision["doi"].strip() != adj["doi"].strip():
            raise ValueError(f"ELIG_APPLY_DOI_MISMATCH:{fid}")
        if decision["title"].strip() != adj["title"].strip():
            raise ValueError(f"ELIG_APPLY_TITLE_MISMATCH:{fid}")
        if adj["direction_coded"].strip() != "NO":
            raise ValueError(f"ELIG_APPLY_DIRECTION_MUST_BE_UNCODED:{fid}")

        state = adj["eligibility_state"].strip()
        source = adj["source_identifier"].strip()
        basis = adj["decision_basis"].strip()
        program = adj["biological_program_id"].strip()

        # Never overwrite a previously completed eligible/direct decision here.
        current = decision["decision_status"].strip()
        if current not in {"PENDING_FULLTEXT"} and not current.startswith("INELIGIBLE_"):
            raise ValueError(
                f"ELIG_APPLY_NONPENDING_DECISION:{fid}:{current}"
            )

        if state in ELIGIBLE_STATES:
            if not program or not basis or not source:
                raise ValueError(f"ELIG_APPLY_ELIGIBLE_MISSING_PROVENANCE:{fid}")
            decision["notes"] = (
                f"ELIGIBILITY_FROZEN_DIRECTION_UNCODED;"
                f"state={state};program={program};"
                f"independence={adj['independence_relation'].strip()};"
                f"basis={basis};source={source}"
            )
            frozen_eligible += 1
        elif state in PENDING_DUPLICATE_STATES:
            if not program or not basis or not source:
                raise ValueError(f"ELIG_APPLY_DUPLICATE_MISSING_PROVENANCE:{fid}")
            decision["notes"] = (
                f"DUPLICATE_IDENTITY_FROZEN_DIRECTION_UNCODED;"
                f"target_program={program};basis={basis};source={source}"
            )
            pending_duplicates += 1
        elif state.startswith("INELIGIBLE_"):
            if not basis or not source:
                raise ValueError(f"ELIG_APPLY_INELIGIBLE_MISSING_PROVENANCE:{fid}")
            decision["decision_status"] = state
            decision["biological_program_id"] = ""
            decision["direction"] = ""
            decision["duplicate_of_program_id"] = ""
            decision["decision_basis"] = basis
            decision["source_identifier"] = source
            decision["notes"] = adj["notes"].strip()
            applied_ineligible += 1
        else:
            raise ValueError(f"ELIG_APPLY_UNKNOWN_STATE:{fid}:{state}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_SOURCE_ELIGIBILITY_APPLY_V1",
        "status": "SOURCE_ELIGIBILITY_APPLIED_DIRECTION_UNCODED",
        "adjudication_records": len(adjudications),
        "ineligible_closed": applied_ineligible,
        "eligible_frozen_direction_uncoded": frozen_eligible,
        "duplicate_identity_frozen_direction_uncoded": pending_duplicates,
        "effect_direction_coded": False,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument(
        "--adjudication",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = apply(
        args.decisions,
        args.adjudication,
        args.output,
        args.receipt,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
