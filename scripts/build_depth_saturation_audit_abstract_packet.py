"""Retrieve Crossref abstract metadata for the head-versus-tail audit queue."""

from __future__ import annotations

import argparse

from trait_architecture.depth_saturation_audit_packet import (
    build_depth_audit_abstract_packet,
    read_depth_audit_queue,
    write_depth_audit_abstract_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_queue_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args(argv)

    packet = build_depth_audit_abstract_packet(read_depth_audit_queue(args.audit_queue_csv))
    write_depth_audit_abstract_packet(args.out_csv, packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
