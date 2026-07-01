"""Retrieve the existing broad Crossref corpus beyond one 1,000-record page.

Usage:
    python scripts/harvest_broad_reality_evidence_paged.py \
      empirical/broad_reality_evidence/broad_evidence_query_registry.csv \
      artifacts/broad_reality_evidence \
      --rows-per-query 2000
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from trait_architecture.broad_reality_deep import harvest_crossref_paged
from trait_architecture.broad_reality_evidence import read_query_registry, summary, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query_registry")
    parser.add_argument("out_dir")
    parser.add_argument("--rows-per-query", type=int, default=2000)
    args = parser.parse_args(argv)

    queries = read_query_registry(args.query_registry)
    candidates, reports = harvest_crossref_paged(
        queries,
        rows_per_query=args.rows_per_query,
    )
    write_outputs(Path(args.out_dir), candidates, reports)
    print(json.dumps(summary(candidates, reports), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
