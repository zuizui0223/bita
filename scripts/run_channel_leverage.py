"""Rank the three channels' parameters by value of information.

Usage:
    python scripts/run_channel_leverage.py \
      configs/part_i_robustness_grid.json artifacts/supplement/channel_leverage [half_width]

For each parameter of the three-channel balance, the analysis asks what fraction of
the declared grid's sign classifications would be settled if that parameter were
pinned to a given relative precision. The ranking says which measurement would
change conclusions — not which is easiest to obtain, and not what any parameter is.

Evaluated across all four declared endpoint-normalized response-shape variants.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.channel_leverage import write_channel_leverage_outputs
from trait_architecture.empirical_leverage import load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_json")
    parser.add_argument("out_dir")
    parser.add_argument("ranking_half_width", nargs="?", type=float, default=0.25)
    args = parser.parse_args(argv)

    if args.ranking_half_width <= 0:
        parser.error("ranking_half_width must be positive")

    diagnostics = write_channel_leverage_outputs(
        args.out_dir,
        load_config(args.config_json),
        ranking_half_width=args.ranking_half_width,
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
