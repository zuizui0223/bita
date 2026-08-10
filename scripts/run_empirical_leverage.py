"""Report which sign classifications a given precision on ``c_D`` would settle.

Usage:
    python scripts/run_empirical_leverage.py \
      configs/part_i_robustness_grid.json 0.45 0.25 artifacts/supplement/leverage

Arguments are the declared grid config, the centre of a candidate ``c_D`` interval,
its half-width, and an output directory.

The centre is a *declared scaffold value*, not an estimate. The repository's
implemented corollary carries ``defence_pollinator_cost = 0.45`` as an
interpretable default, and that is what the committed run uses. When the
constituent-pathway meta-analysis produces a pooled log response ratio, convert it
with ``cost_from_log_response_ratio`` and re-run with the real interval.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.empirical_leverage import load_config, write_leverage_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_json")
    parser.add_argument("interval_centre", type=float)
    parser.add_argument("interval_half_width", type=float)
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    if args.interval_half_width < 0:
        parser.error("interval_half_width must be non-negative")

    diagnostics = write_leverage_outputs(
        args.out_dir,
        load_config(args.config_json),
        max(0.0, args.interval_centre - args.interval_half_width),
        args.interval_centre + args.interval_half_width,
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
