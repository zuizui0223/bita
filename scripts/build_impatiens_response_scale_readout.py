"""Build a markdown readout for response-scale *Impatiens* models.

Usage:
    python scripts/build_impatiens_response_scale_readout.py REPORT_JSON OUTPUT_MD
"""

from __future__ import annotations

import argparse

from trait_architecture.impatiens_response_scale_readout import build_readout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_json")
    parser.add_argument("output_md")
    args = parser.parse_args(argv)
    build_readout(args.report_json, args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
