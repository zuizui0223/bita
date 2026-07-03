"""Render bounded previews for the primary eLife d_A figures.

Usage:
    python scripts/render_d_a_elife_figure_previews.py \
      artifacts/d_a_elife_assets/d_a_elife_asset_receipts.csv \
      artifacts/d_a_elife_figure_previews

The output is for internal C4 visual reading. It does not digitize data or infer an
effect.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_elife_figure_preview import read_assets, render_previews, write_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    rows = render_previews(read_assets(args.asset_csv), args.out_dir)
    report = write_manifest(args.out_dir, rows)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
