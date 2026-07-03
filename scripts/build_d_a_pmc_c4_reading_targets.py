"""Build C4 reading targets for viable PMC d_A candidates.

Usage:
    python scripts/build_d_a_pmc_c4_reading_targets.py \
      artifacts/d_a_pmc_fulltext_screen/d_a_pmc_fulltext_screen.csv \
      artifacts/d_a_pmc_c4_reading_targets

Outputs only source locators and blank C4 work instructions. It does not extract
an effect or decide Part B inclusion.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_pmc_reading_targets import build_targets, read_screen, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screen_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = write_outputs(args.out_dir, build_targets(read_screen(args.screen_csv)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
