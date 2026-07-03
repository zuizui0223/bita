"""Screen registered PMC d_A leads for source-level direct-route feasibility.

Usage:
    python scripts/screen_d_a_pmc_fulltext.py \
      empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv \
      artifacts/d_a_pmc_fulltext_screen

Outputs only term-family and section/table locators. It does not retain full text,
extract effects, or infer a direct d_A relationship.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_pmc_screen import read_candidates, screen_candidates, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = write_outputs(args.out_dir, screen_candidates(read_candidates(args.candidate_csv)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
