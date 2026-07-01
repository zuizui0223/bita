"""Build the B/P metadata-signal priority queue for the precision expansion."""

from __future__ import annotations

import argparse

from trait_architecture.b_to_p_precision_batch import (
    select_b_to_p_precision_batch,
    write_b_to_p_precision_batch,
)
from trait_architecture.broad_source_screening import read_priority_candidates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("priority_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args(argv)

    batch = select_b_to_p_precision_batch(
        read_priority_candidates(args.priority_csv),
        limit=args.limit,
    )
    write_b_to_p_precision_batch(args.output_csv, batch)
    print(f"b_to_p_signal_queue_rows={len(batch)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
