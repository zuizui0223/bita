"""Inspect the Caruso-linked Dryad file manifest without downloading file contents.

Usage:
    python scripts/probe_d_a_caruso_dryad_manifest.py OUT_DIR

This reports metadata and file names/mime types only. A filename candidate is not a
primary-study index until a later capped schema-inspection stage verifies it.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_caruso_dryad_manifest import PublicJSONClient, probe_dryad_manifest, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("--min-interval-seconds", type=float, default=0.25)
    args = parser.parse_args(argv)
    client = PublicJSONClient(min_interval_seconds=args.min_interval_seconds)
    report = write_outputs(args.out_dir, probe_dryad_manifest(fetch_json=client.json))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
