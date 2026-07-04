"""Run randomized 2x2x2 treatment models for Impatiens fitness components.

Usage:
    python scripts/run_impatiens_randomized_fitness_models.py CONFIG_JSON TARGETS_CSV OUT_DIR

Raw archive records are used only in memory. Outputs contain aggregate factorial
coefficients and diagnostics.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.impatiens_factorial_fitness_models import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_json")
    parser.add_argument("targets_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(run(args.config_json, args.targets_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
