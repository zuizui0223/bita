"""Screen the fixed Trollius candidate for a public direct d_A route.

Usage:
    python scripts/probe_d_a_trollius_pmc.py SCOUTING_CSV OUT_DIR

Outputs accession and section/table locator receipts only. It does not read article
prose into artifacts, extract numeric effects, or update Part B.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_trollius_pmc_probe import probe_scouting_file


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
