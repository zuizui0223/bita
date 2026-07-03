"""Build the head-versus-tail source-coding queue from ranked Crossref memberships.

Example:
    python scripts/build_depth_saturation_audit.py \
      artifacts/broad_reality_evidence/broad_reality_evidence_rank_memberships.csv \
      artifacts/broad_reality_evidence/depth_saturation_audit \
      --per-route-stratum-group 10
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.depth_saturation_audit import write_depth_audit_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_memberships_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--head-rank-max", type=int, default=200)
    parser.add_argument("--tail-rank-min", type=int, default=1601)
    parser.add_argument("--tail-rank-max", type=int, default=2000)
    parser.add_argument("--per-route-stratum-group", type=int, default=10)
    args = parser.parse_args(argv)

    summary = write_depth_audit_outputs(
        args.rank_memberships_csv,
        args.out_dir,
        head_rank_max=args.head_rank_max,
        tail_rank_min=args.tail_rank_min,
        tail_rank_max=args.tail_rank_max,
        per_route_stratum_group=args.per_route_stratum_group,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
