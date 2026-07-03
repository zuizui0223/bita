"""Write an honest final readout for the bounded Caruso primary-index route.

Usage:
    python scripts/read_d_a_caruso_index_route.py MANIFEST_CSV SCHEMA_CSV OUT_DIR

The result classifies only access and schema receipts; it does not extract study
identifiers or effect data.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_caruso_index_readout import write_readout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest_csv")
    parser.add_argument("schema_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = write_readout(
        args.out_dir,
        manifest_csv=args.manifest_csv,
        schema_csv=args.schema_csv,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
