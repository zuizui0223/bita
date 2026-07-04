"""Build a bounded Part A theory-to-empirics bridge for the Impatiens core.

Usage:
    python scripts/build_impatiens_theory_bridge.py RESPONSE_REPORT FACTORIAL_REPORT OUTPUT_MD
"""

from __future__ import annotations

import argparse

from trait_architecture.impatiens_theory_bridge import build_bridge


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response_report")
    parser.add_argument("factorial_report")
    parser.add_argument("output_md")
    args = parser.parse_args(argv)
    build_bridge(args.response_report, args.factorial_report, args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
