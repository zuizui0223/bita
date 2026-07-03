"""Resolve d_A candidate leads to reproducible Crossref access receipts (C3).

Usage:
    python scripts/resolve_d_a_candidate_sources.py \
      empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv \
      artifacts/d_a_source_receipts

Records access and relation metadata only; it never reads article text or
estimates an effect. A resolved open-access link is a route, not evidence.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_source_resolver import (
    CrossrefFetcher,
    read_candidates,
    resolve_candidates,
    summarise,
    write_receipts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--mailto", default=None, help="Contact email for the Crossref polite pool")
    args = parser.parse_args(argv)

    fetcher = CrossrefFetcher(mailto=args.mailto)
    receipts = resolve_candidates(read_candidates(args.candidates_csv), fetch_json=fetcher.json)
    summary = summarise(receipts)
    write_receipts(args.out_dir, receipts, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
