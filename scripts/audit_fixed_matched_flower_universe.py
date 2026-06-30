"""Audit shallow public source routes for the fixed 258-work M0 universe.

The fixed universe is downloaded from the successful PR #20 harvest artifact,
verified by SHA-256, and queried against public metadata endpoints. No article
PDF, supplement, data archive, or raw biological observation is downloaded.

Usage:
    python scripts/audit_fixed_matched_flower_universe.py artifacts/fixed_258_public_routes
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.candidate_universe_public_audit import audit_candidates, write_audit
from trait_architecture.fixed_candidate_universe import load_fixed_candidate_universe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)

    candidates, snapshot = load_fixed_candidate_universe()
    audit_rows, receipts = audit_candidates(candidates, max_workers=args.workers)
    report = write_audit(args.out_dir, audit_rows=audit_rows, receipts=receipts, snapshot=snapshot)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
