"""Run the predeclared moderator analyses for one constituent-pathway meta-analysis.

Usage:
    python scripts/run_context_dependence.py \
      empirical/broad_reality_evidence/broad_effect_extractions.csv \
      empirical/broad_reality_evidence/iota_pathway/iota_moderator_coding.csv \
      empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
      empirical/broad_reality_evidence/iota_pathway/iota_moderator_registry.csv \
      artifacts/supplement/iota_pathway

Every analysis is read from the declared registry. Strata below the declared cluster
thresholds report a withheld status instead of an estimate.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.broad_meta_analysis import read_csv_rows, read_strata
from trait_architecture.context_dependence import (
    read_moderator_coding,
    read_moderator_registry,
    write_context_outputs,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("effect_extractions_csv")
    parser.add_argument("moderator_coding_csv")
    parser.add_argument("strata_csv")
    parser.add_argument("moderator_registry_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    diagnostics = write_context_outputs(
        args.out_dir,
        read_csv_rows(args.effect_extractions_csv),
        read_moderator_coding(args.moderator_coding_csv),
        read_strata(args.strata_csv),
        read_moderator_registry(args.moderator_registry_csv),
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
