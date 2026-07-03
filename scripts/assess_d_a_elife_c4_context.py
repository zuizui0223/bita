"""Assess fixed Schiestl C4 context without extracting an effect.

Usage:
    python scripts/assess_d_a_elife_c4_context.py \
      artifacts/d_a_elife_source_probe/d_a_elife_source_probe.csv \
      artifacts/d_a_elife_c4_context

The output is structured presence/absence signals and locators only. It never
stores article prose, digitizes figures, or adds an effect row.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_elife_c4_context import assess_probe_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_probe_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(assess_probe_csv(args.source_probe_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
