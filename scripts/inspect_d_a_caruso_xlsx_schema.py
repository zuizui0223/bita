"""Inspect the Caruso-linked Dryad XLSX schema without retaining study data.

Usage:
    python scripts/inspect_d_a_caruso_xlsx_schema.py MANIFEST_CSV OUT_DIR

Only exact XLSX manifest entries whose names suggest experimental-study data are
read. The output contains sheet names, dimensions, and first-row field names only.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_caruso_xlsx_schema import inspect_manifest, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    print(json.dumps(write_outputs(args.out_dir, inspect_manifest(args.manifest_csv)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
