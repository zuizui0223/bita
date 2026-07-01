"""Audit current OpenAlex depth for the historical and omitted query routes.

Usage:
    python scripts/audit_openalex_retrieval_scope.py \
      empirical/matched_flower_regime/literature_seed_queries.csv \
      artifacts/openalex_retrieval_scope
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trait_architecture.openalex_retrieval_scope_audit import run_scope_audit, write_scope_audit


def read_queries(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: str(value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError("query registry is empty")
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query_registry")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    _, candidates, report = run_scope_audit(read_queries(args.query_registry))
    write_scope_audit(args.out_dir, candidates, report)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
