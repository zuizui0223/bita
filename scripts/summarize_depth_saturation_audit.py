"""Summarize completed head-versus-tail direct-route coding."""

from __future__ import annotations

import argparse

from trait_architecture.depth_saturation_audit_adjudication import (
    summarize_depth_audit,
    write_depth_audit_summary,
)
from trait_architecture.priority_leak_audit_adjudication import read


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("coding_sheet_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    summary, comparisons, diagnostics = summarize_depth_audit(read(args.coding_sheet_csv))
    write_depth_audit_summary(args.out_dir, summary, comparisons, diagnostics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
