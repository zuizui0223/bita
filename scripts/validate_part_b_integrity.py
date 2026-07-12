"""Integrity guard for the retained verified Part B effect table.

The submission supplement no longer carries candidate-scouting or moderator-coding
queues. This guard therefore checks only the committed verified effect table:

- rows satisfy the registered effect schema;
- effects eligible for quantitative synthesis have a non-empty source basis;
- eligible effects are not sourced from candidate or unverified material;
- eligible effects include a source locator.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trait_architecture.broad_meta_analysis import read_csv_rows, validate_effect_rows

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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("effects_csv")
    args = parser.parse_args(argv)

    violations = check_verified_effects(args.effects_csv)
    if violations:
        print("Part B integrity check FAILED:")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print("Part B integrity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
