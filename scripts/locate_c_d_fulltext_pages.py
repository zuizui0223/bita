"""Locate likely dose/outcome/table pages in public PDFs for the fixed c_D queue.

Usage:
    python scripts/locate_c_d_fulltext_pages.py \
      artifacts/c_d_source_receipts/c_d_fulltext_source_receipts.csv \
      artifacts/c_d_source_receipts/c_d_fulltext_page_locators.csv

The script writes page locators only. It does not retain PDFs/text or extract an
effect; visual source verification remains required before numerical extraction.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.c_d_fulltext_locator import locate_receipts, read_receipts, write_locators


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args(argv)

    rows = locate_receipts(read_receipts(args.receipt_csv))
    report = write_locators(args.out_csv, rows)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
