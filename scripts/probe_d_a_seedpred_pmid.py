"""Resolve and screen the registered seed-predation d_A candidate.

Usage:
    python scripts/probe_d_a_seedpred_pmid.py SCOUTING_CSV OUT_DIR

The output stores only public identifiers and XML section/table locators. It never
writes article prose, an effect estimate, or an eligibility decision.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_seedpred_pmid_probe import probe_scouting_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scouting_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = probe_scouting_file(args.scouting_csv, args.out_dir)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
