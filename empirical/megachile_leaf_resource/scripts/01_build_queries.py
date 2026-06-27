#!/usr/bin/env python3
"""Build reproducible bilingual search queries for reviewed Megachile evidence.

Example:
python empirical/megachile_leaf_resource/scripts/01_build_queries.py \
  --species empirical/megachile_leaf_resource/data_raw/megachile_species.csv \
  --output empirical/megachile_leaf_resource/data_raw/search_queries.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from trait_architecture.host_evidence import build_query_rows  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("query_id", "bee_name_accepted", "language", "query_family", "query_string", "purpose")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--species", type=Path, required=True, help="CSV with bee_name_accepted and optional bee_name_japanese")
    parser.add_argument("--output", type=Path, required=True, help="Destination search_queries.csv")
    args = parser.parse_args()

    rows = read_rows(args.species)
    if not rows:
        raise SystemExit("species table is empty; populate a curated checklist before building queries")
    queries = build_query_rows(rows)
    write_rows(args.output, queries)
    print(f"wrote {len(queries)} queries for {len(rows)} bee taxa to {args.output}")


if __name__ == "__main__":
    main()
