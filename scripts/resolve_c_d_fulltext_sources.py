"""Resolve the fixed c_D full-text reading queue to Crossref access receipts.

Usage:
    python scripts/resolve_c_d_fulltext_sources.py \
      empirical/broad_reality_evidence/precision_expansions/fulltext/B_TO_P_FULLTEXT_READING_QUEUE_v1.csv \
      artifacts/c_d_source_receipts

Records access and relation metadata only. A resolvable full-text link is a source
route, never a numerical effect or proof of B2 eligibility.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.c_d_source_resolution import (
    read_fulltext_queue,
    resolve_fulltext_queue,
    write_receipts,
)
from trait_architecture.d_a_source_resolver import CrossrefFetcher


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--mailto", default=None, help="Contact email for the Crossref polite pool")
    args = parser.parse_args(argv)

    fetcher = CrossrefFetcher(mailto=args.mailto)
    receipts = resolve_fulltext_queue(read_fulltext_queue(args.queue_csv), fetch_json=fetcher.json)
    report = write_receipts(args.out_dir, receipts)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
