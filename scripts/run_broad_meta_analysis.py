"""Run directional mapping and predeclared quantitative mini-meta-analyses.

Usage:
    python scripts/run_broad_meta_analysis.py \
      empirical/broad_reality_evidence/broad_route_records.csv \
      empirical/broad_reality_evidence/broad_effect_extractions.csv \
      empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
      artifacts/broad_meta_analysis
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.broad_meta_analysis import (
    read_csv_rows,
    read_strata,
    write_analysis_outputs,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route_records_csv")
    parser.add_argument("effect_extractions_csv")
    parser.add_argument("strata_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    diagnostics = write_analysis_outputs(
        args.out_dir,
        read_csv_rows(args.route_records_csv),
        read_csv_rows(args.effect_extractions_csv),
        read_strata(args.strata_csv),
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
