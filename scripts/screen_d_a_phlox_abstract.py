"""Screen the fixed Phlox candidate for a direct display-to-florivory route.

Usage:
    python scripts/screen_d_a_phlox_abstract.py SCOUTING_CSV OUT_DIR

The output records abstract-structure signals only. It never extracts an effect
estimate or modifies the Part B effect table.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_phlox_abstract_screen import screen_scouting_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scouting_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(screen_scouting_file(args.scouting_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
