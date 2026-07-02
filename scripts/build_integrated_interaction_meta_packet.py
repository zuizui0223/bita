"""Build the unified A/B x pollinator/antagonist effect-ledger packet.

Usage:
    python scripts/build_integrated_interaction_meta_packet.py \
      artifacts/floral_trait_animal_response_meta/floral_trait_animal_response_candidate_queue.csv \
      artifacts/integrated_interaction_meta

Optionally pass a previously populated integrated effect ledger to re-run its
metric harmonization and balance dashboard after full-text extraction:

    --effect-ledger-csv extracted_effect_ledger.csv

The command does not run discovery searches. It carries every candidate route
from the fixed corpus into one master ledger and makes metric/outcome/design
variation explicit for a later hierarchical model.
"""

from __future__ import annotations

import argparse

from trait_architecture.integrated_interaction_meta import (
    CANDIDATE_QUEUE_REQUIRED,
    EFFECT_LEDGER_FIELDS,
    build_candidate_ledger,
    make_effect_ledger,
    read_rows,
    write_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_queue_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--effect-ledger-csv", default=None)
    args = parser.parse_args(argv)

    candidate_ledger = build_candidate_ledger(
        read_rows(args.candidate_queue_csv, CANDIDATE_QUEUE_REQUIRED)
    )
    effect_ledger = (
        read_rows(args.effect_ledger_csv, EFFECT_LEDGER_FIELDS)
        if args.effect_ledger_csv
        else make_effect_ledger(candidate_ledger)
    )
    write_packet(args.out_dir, candidate_ledger, effect_ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
