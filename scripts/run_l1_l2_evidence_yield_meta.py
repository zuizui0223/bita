"""Run fixed-corpus L1/L2 evidence-yield meta-analysis.

The audit-only core (posterior direct-route rates and the priority-vs-nonpriority
enrichment meta-analysis) reproduces from the committed audit CSV alone. The
membership projection layer additionally needs the frozen screened corpus; pass
it as the optional first argument. When it is omitted, projections are marked as
not computed instead of emitting misleading zeros.

Usage:
    # audit-only core, reproducible from the committed repository
    python scripts/run_l1_l2_evidence_yield_meta.py \
      empirical/broad_reality_evidence/priority_leak_audit/priority_leak_audit_yield_by_route_group_v1.csv \
      artifacts/l1_l2_evidence_yield_meta

    # full analysis including corpus-size projections
    python scripts/run_l1_l2_evidence_yield_meta.py \
      empirical/broad_reality_evidence/priority_leak_audit/priority_leak_audit_yield_by_route_group_v1.csv \
      artifacts/l1_l2_evidence_yield_meta \
      --screened-csv artifacts/broad_reality_evidence/broad_reality_evidence_screened.csv
"""

from __future__ import annotations

import argparse

from trait_architecture.evidence_yield_meta_analysis import AUDIT_FIELDS, SCREEN_FIELDS, read_rows
from trait_architecture.evidence_yield_meta_model import build_evidence_yield_meta, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_yield_csv")
    parser.add_argument("out_dir")
    parser.add_argument(
        "--screened-csv",
        default=None,
        help="Frozen screened corpus for the membership projection layer; omit for the audit-only core.",
    )
    args = parser.parse_args(argv)
    screened = read_rows(args.screened_csv, SCREEN_FIELDS) if args.screened_csv else []
    outputs = build_evidence_yield_meta(
        screened,
        read_rows(args.audit_yield_csv, AUDIT_FIELDS),
    )
    write_outputs(args.out_dir, *outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
