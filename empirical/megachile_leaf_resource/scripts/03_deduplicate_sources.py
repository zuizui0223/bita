#!/usr/bin/env python3
"""Deduplicate candidate source metadata while preserving an audit trail."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from trait_architecture.host_evidence import deduplicate_metadata  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()

    rows = read_rows(args.input)
    kept, discarded = deduplicate_metadata(rows)
    fields = sorted({key for row in kept for key in row})
    write_rows(args.output, kept, fields)
    write_rows(args.audit_output, discarded, ["discarded_provider", "discarded_provider_record_id", "kept_source_id", "dedupe_fingerprint", "reason"])
    print(f"kept {len(kept)} of {len(rows)} rows; wrote {len(discarded)} duplicate audit rows")


if __name__ == "__main__":
    main()
