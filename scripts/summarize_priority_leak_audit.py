"""Validate completed audit coding and summarize direct-route yield.

Usage:
  python scripts/summarize_priority_leak_audit.py INPUT_PACKET.csv INPUT_SHEET.csv OUTPUT_DIR
"""

from __future__ import annotations

import argparse

from trait_architecture.priority_leak_audit_adjudication import (
    check_sheet,
    read,
    summarize,
    write_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_packet_csv")
    parser.add_argument("audit_coding_sheet_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    packet = read(args.audit_packet_csv)
    sheet = read(args.audit_coding_sheet_csv)
    check_sheet(sheet, packet_rows=packet)
    summary, comparisons, diagnostics = summarize(sheet)
    write_summary(args.output_dir, summary, comparisons, diagnostics)
    print(f"audit_rows={len(sheet)} route_groups={len(summary)} route_comparisons={len(comparisons)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
