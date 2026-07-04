"""Run the predeclared response-scale *Impatiens capensis* model set.

Usage:
    python scripts/run_impatiens_response_scale_models.py CONFIG_JSON TARGETS_CSV OUT_DIR

Raw archive rows are used only in memory. The output is an aggregate coefficient and
diagnostic report with observational-inference boundaries.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.impatiens_response_scale_models import run


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
