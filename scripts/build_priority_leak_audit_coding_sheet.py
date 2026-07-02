"""Create the blank coding ledger for the frozen priority-leak audit packet.

Usage:
  python scripts/build_priority_leak_audit_coding_sheet.py INPUT_PACKET.csv OUTPUT_SHEET.csv
"""

from __future__ import annotations

import argparse

from trait_architecture.priority_leak_audit_adjudication import (
    make_sheet,
    read,
    write_sheet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_packet_csv")
    parser.add_argument("output_sheet_csv")
    args = parser.parse_args(argv)
    sheet = make_sheet(read(args.audit_packet_csv))
    write_sheet(args.output_sheet_csv, sheet)
    abstract_rows = sum(row["source_access_status"] == "abstract_only" for row in sheet)
    print(f"audit_coding_rows={len(sheet)} abstract_only_rows={abstract_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
