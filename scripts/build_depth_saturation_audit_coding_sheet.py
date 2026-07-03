"""Create a frozen source-coding sheet for the head-versus-tail audit packet."""

from __future__ import annotations

import argparse

from trait_architecture.priority_leak_audit_adjudication import make_sheet, read, write_sheet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_packet_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args(argv)

    sheet = make_sheet(read(args.audit_packet_csv))
    write_sheet(args.out_csv, sheet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
