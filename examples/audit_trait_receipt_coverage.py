"""Audit functional-trait coverage for a requested network plant set.

Usage:
    python examples/audit_trait_receipt_coverage.py \
      try_wol_pollination_species_request.csv \
      empirical/functional_traits/trait_role_evidence.csv \
      trait_receipt_normalised.csv
"""

from __future__ import annotations

import json
import sys

from trait_architecture.trait_coverage_audit import (
    audit_trait_coverage_files,
    trait_coverage_report_to_dict,
)


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: python examples/audit_trait_receipt_coverage.py "
            "plant_manifest.csv trait_role_evidence.csv trait_receipt.csv"
        )
    report = audit_trait_coverage_files(*sys.argv[1:])
    print(json.dumps(trait_coverage_report_to_dict(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
