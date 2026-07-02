"""Build the B-flower full-text screening packet from a fixed response-meta queue.

Usage:
    python scripts/build_b_flower_mechanism_triage.py \
      artifacts/floral_trait_animal_response_meta/floral_trait_animal_response_candidate_queue.csv \
      artifacts/b_flower_mechanism_triage

This command never retrieves new records. It preserves all B->antagonist
candidates as a census and only ranks B->pollinator reading order.
"""

from __future__ import annotations

import argparse

from trait_architecture.b_flower_mechanism_triage import (
    DEFAULT_B_POLLINATOR_TOPUP,
    build_b_triage,
    read_queue,
    write_b_triage_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_queue_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--b-pollinator-topup", type=int, default=DEFAULT_B_POLLINATOR_TOPUP)
    args = parser.parse_args(argv)

    triage, batch, screening = build_b_triage(
        read_queue(args.candidate_queue_csv),
        b_pollinator_topup=args.b_pollinator_topup,
    )
    write_b_triage_packet(args.out_dir, triage, batch, screening)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
