"""Create a reproducible human-coding packet from a fixed broad abstract map.

Usage:
    python scripts/build_broad_abstract_label_audit.py \
      artifacts/broad_abstract_evidence/broad_abstract_evidence_records.csv \
      artifacts/broad_abstract_evidence/fixed_l1_abstract_packet.csv \
      artifacts/broad_abstract_label_audit

No discovery retrieval is performed. Both inputs must originate from the same
fixed broad-map artifact.
"""

from __future__ import annotations

import argparse

from trait_architecture.broad_abstract_label_audit import (
    DEFAULT_NONJOINT_TARGET,
    DEFAULT_SEED,
    build_audit_packet,
    read_rows,
    write_audit_packet,
)

RECORD_REQUIRED = {
    "candidate_id", "doi", "publication_year", "work_type", "route_families", "source_queries",
    "shallow_screen_status", "abstract_retrieval_state", "crossref_lookup_status", "crossref_abstract_available",
    "abstract_code_status", "floral_context_signal", "empirical_language_signal", "review_language_signal",
    "A_signal", "B_signal", "P_signal", "H_signal", "W_signal", "shared_cost_language_signal",
    "candidate_A_to_P", "candidate_A_to_H", "candidate_B_to_H", "candidate_B_to_P", "candidate_joint_channels",
}
PACKET_REQUIRED = {
    "candidate_id", "doi", "title", "publication_year", "work_type", "container_title", "publisher",
    "abstract_retrieval_state", "crossref_lookup_status", "crossref_abstract_available", "crossref_abstract_text",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_records_csv")
    parser.add_argument("abstract_packet_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--nonjoint-target", type=int, default=DEFAULT_NONJOINT_TARGET)
    args = parser.parse_args(argv)

    packet, coding, design = build_audit_packet(
        read_rows(args.evidence_records_csv, RECORD_REQUIRED),
        read_rows(args.abstract_packet_csv, PACKET_REQUIRED),
        seed=args.seed,
        nonjoint_target=args.nonjoint_target,
    )
    write_audit_packet(args.out_dir, packet, coding, design)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
