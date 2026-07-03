"""Locate source-data assets associated with the eLife d_A C4 figures.

Usage:
    python scripts/locate_d_a_elife_assets.py \
      artifacts/d_a_elife_xml_screen/d_a_elife_xml_screen.csv \
      artifacts/d_a_elife_assets

This only records declared asset URLs and bounded reachability receipts. It does
not read datasets or calculate an effect.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_elife_asset_locator import locate_assets, read_screen, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screen_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = write_outputs(args.out_dir, locate_assets(read_screen(args.screen_csv)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
