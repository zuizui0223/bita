"""Build the aggregate Impatiens empirical channel-ledger SVG.

Usage:
    python scripts/build_impatiens_channel_ledger_svg.py RESPONSE_REPORT FACTORIAL_REPORT OUTPUT_SVG
"""

from __future__ import annotations

import argparse

from trait_architecture.impatiens_channel_ledger_svg import build_svg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response_report")
    parser.add_argument("factorial_report")
    parser.add_argument("output_svg")
    args = parser.parse_args(argv)
    build_svg(args.response_report, args.factorial_report, args.output_svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
