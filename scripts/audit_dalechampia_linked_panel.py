"""Audit the public secondary *Dalechampia* Dryad panel without retaining rows.

Usage:
    python scripts/audit_dalechampia_linked_panel.py \
      10.1111/j.1600-0706.2013.20780.x \
      10.5061/dryad.0k6djh9xx \
      artifacts/dalechampia_linked_panel
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.dalechampia_linked_panel import audit_package, write_audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article_doi")
    parser.add_argument("dataset_doi")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    schemas, report = audit_package(article_doi=args.article_doi, dataset_doi=args.dataset_doi)
    write_audit(args.out_dir, schemas, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
