"""Locate candidate evidence pages in DOI-exact OpenAlex public-PDF candidates.

Usage:
    python scripts/locate_c_d_public_source_pages.py \
      artifacts/c_d_public_sources/c_d_public_source_receipts.csv \
      artifacts/c_d_public_sources/c_d_public_source_page_locators.csv

The source scout must have already confirmed an exact DOI relation. This script
still rechecks unauthenticated PDF access and writes locators only.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.c_d_fulltext_locator import (
    locate_receipts,
    read_public_source_receipts,
    write_locators,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_source_receipts_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args(argv)
    rows = locate_receipts(read_public_source_receipts(args.public_source_receipts_csv))
    report = write_locators(args.out_csv, rows)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
