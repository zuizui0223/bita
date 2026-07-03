"""Probe public source routes for the registered scent/reward d_A eLife lead.

Usage:
    python scripts/probe_d_a_elife_source.py \
      empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv \
      artifacts/d_a_elife_source_probe

This writes only URL reachability and content-type receipts. It does not read the
article, extract an effect, or assess direct-route eligibility.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_elife_probe import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--mailto", default=None)
    args = parser.parse_args(argv)
    report = run(args.candidate_csv, args.out_dir, mailto=args.mailto)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
