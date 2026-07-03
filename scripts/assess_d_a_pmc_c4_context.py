"""Assess viable PMC d_A C4 context without extracting an effect.

Usage:
    python scripts/assess_d_a_pmc_c4_context.py \
      artifacts/d_a_pmc_fulltext_screen/d_a_pmc_fulltext_screen.csv \
      artifacts/d_a_pmc_c4_context

The output contains structured field-presence signals and source locators only.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_pmc_c4_context import assess_screen_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pmc_screen_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(assess_screen_csv(args.pmc_screen_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
