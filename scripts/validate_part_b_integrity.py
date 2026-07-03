"""Integrity guard for the Part B data files (honesty-contract enforcement).

Checks that the verified/candidate/queue boundary is not crossed:

1. verified effect table   - passes validate_effect_rows; no eligible effect is
                             sourced from a candidate/unverified basis; each has a
                             source_locator.
2. candidate scouting table - carries no effect_value/standard_error columns (a
                             candidate is a lead, never an effect) and every row is
                             flagged unverified.
3. moderator coding queue  - passes validate_effect_rows; every row with a blank
                             moderator_level is explicitly marked
                             needs_moderator_level_coding (honest missingness).

Exit code is non-zero if any check fails, so CI blocks a leak of an unverified
lead into the verified effect base. Designed to be importable and testable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trait_architecture.broad_meta_analysis import read_csv_rows, validate_effect_rows

ALLOWED_CANDIDATE_STATUSES = frozenset({"candidate_unverified", "seed_synthesis_unverified"})
FORBIDDEN_EFFECT_SOURCE_TOKENS = ("candidate", "unverified")


def check_verified_effects(path: str | Path) -> list[str]:
    violations: list[str] = []
    rows = read_csv_rows(path)
    try:
        validate_effect_rows(rows)
    except ValueError as error:
        violations.append(f"{path}: effect rows fail validation: {error}")
        return violations
    for row in rows:
        if (row.get("analysis_status") or "").strip() != "eligible_for_quantitative_synthesis":
            continue
        effect_id = (row.get("effect_id") or "").strip()
        basis = (row.get("source_basis") or "").strip().lower()
        if not basis:
            violations.append(f"{path}: eligible effect {effect_id} has no source_basis")
        if any(token in basis for token in FORBIDDEN_EFFECT_SOURCE_TOKENS):
            violations.append(
                f"{path}: eligible effect {effect_id} is sourced from an unverified/candidate basis"
            )
        if not (row.get("source_locator") or "").strip():
            violations.append(f"{path}: eligible effect {effect_id} has no source_locator")
    return violations


def check_candidates(path: str | Path) -> list[str]:
    violations: list[str] = []
    rows = read_csv_rows(path)
    if not rows:
        return violations
    columns = set(rows[0].keys())
    for banned in ("effect_value", "standard_error"):
        if banned in columns:
            violations.append(f"{path}: candidate table must not carry an '{banned}' column")
    for row in rows:
        status = (row.get("verification_status") or "").strip()
        if status not in ALLOWED_CANDIDATE_STATUSES:
            candidate_id = (row.get("candidate_id") or "").strip()
            violations.append(
                f"{path}: candidate {candidate_id} has verification_status '{status}' "
                f"(must be one of {sorted(ALLOWED_CANDIDATE_STATUSES)})"
            )
    return violations


def check_coding_queue(path: str | Path) -> list[str]:
    violations: list[str] = []
    rows = read_csv_rows(path)
    try:
        validate_effect_rows(rows)
    except ValueError as error:
        violations.append(f"{path}: queue rows fail validation: {error}")
        return violations
    for row in rows:
        if (row.get("moderator_level") or "").strip():
            continue
        status = (row.get("coding_status") or "").strip()
        if status != "needs_moderator_level_coding":
            effect_id = (row.get("effect_id") or "").strip()
            violations.append(
                f"{path}: queue row {effect_id} has a blank moderator_level but "
                f"coding_status is '{status}' (expected needs_moderator_level_coding)"
            )
    return violations


def check_part_b_integrity(effects_path: str | Path, candidates_path: str | Path, queue_path: str | Path) -> list[str]:
    violations: list[str] = []
    violations += check_verified_effects(effects_path)
    violations += check_candidates(candidates_path)
    violations += check_coding_queue(queue_path)
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("effects_csv")
    parser.add_argument("candidates_csv")
    parser.add_argument("queue_csv")
    args = parser.parse_args(argv)

    violations = check_part_b_integrity(args.effects_csv, args.candidates_csv, args.queue_csv)
    if violations:
        print("Part B integrity check FAILED:")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print("Part B integrity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
