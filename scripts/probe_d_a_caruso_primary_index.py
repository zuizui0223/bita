"""Probe public index routes from Caruso 2019 to primary-study metadata.

Usage:
    python scripts/probe_d_a_caruso_primary_index.py OUT_DIR \
      --mailto actions@users.noreply.github.com

The result is a URL-level access receipt only. It does not download an index,
extract primary-study records, or use Caruso selection gradients as d_A effects.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_caruso_index_probe import PublicMetadataClient, probe_caruso_index, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("--mailto", required=True)
    parser.add_argument("--min-interval-seconds", type=float, default=0.25)
    args = parser.parse_args(argv)
    client = PublicMetadataClient(mailto=args.mailto, min_interval_seconds=args.min_interval_seconds)
    report = write_outputs(
        args.out_dir,
        probe_caruso_index(
            fetch_json=client.json,
            fetch_html=client.html,
            unpaywall_email=args.mailto,
        ),
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
