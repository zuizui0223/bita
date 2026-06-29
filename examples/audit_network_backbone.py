"""Audit a normalised interaction network bundle.

Usage:
    python examples/audit_network_backbone.py interactions.csv networks.csv traits.csv
"""

from __future__ import annotations

import json
import sys

from trait_architecture.network_audit import audit_files, report_to_dict


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit("usage: python examples/audit_network_backbone.py interactions.csv networks.csv traits.csv")
    report = audit_files(*sys.argv[1:])
    print(json.dumps(report_to_dict(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
