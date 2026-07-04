"""Audit factorial treatment cells and pre-treatment baseline summaries.

Usage:
    python scripts/audit_impatiens_factorial_balance.py TARGETS_CSV OUT_DIR

Outputs contain aggregate treatment-cell counts and baseline summaries only.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.impatiens_factorial_balance_audit import audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(audit(args.targets_csv, args.out_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
