"""Rank harvested OpenAlex candidates by shallow public-source availability.

Usage:
    python scripts/rank_broad_public_source_availability.py \
      artifacts/matched_flower_seed_harvest/matched_flower_seed_candidates.csv \
      artifacts/broad_public_source_availability
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.broad_source_availability import read_harvest, rank_candidates, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("harvest_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--top-n", type=int, default=40)
    args = parser.parse_args(argv)
    records = rank_candidates(read_harvest(args.harvest_csv))
    summary = write_outputs(records, args.out_dir, top_n=args.top_n)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
