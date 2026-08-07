"""Check whether the empirical constituent-path layer is ready for pooling.

This script is intentionally a gate, not a meta-analysis. It prevents multiple
doses or outcomes from one study from being counted as independent replication
and preserves the repository's existing k>=3 exploratory / k>=5 stability rules.

Usage:
    python scripts/check_constituent_path_meta_readiness.py \
      empirical/constituent_path_meta/B_TO_P_PRELIMINARY_EXTRACTIONS_V1.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

EXPLORATORY_MIN_CLUSTERS = 3
STABILITY_MIN_CLUSTERS = 5


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def readiness(rows: list[dict[str, str]]) -> dict[str, object]:
    lanes: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        lane = row.get("outcome_lane", "")
        if not lane:
            raise ValueError("every extraction row must declare outcome_lane")
        cluster = row.get("independence_cluster", "")
        if not cluster:
            raise ValueError("every extraction row must declare independence_cluster")
        lanes[lane].append(row)

    lane_reports: dict[str, object] = {}
    for lane, lane_rows in sorted(lanes.items()):
        source_complete = [
            row for row in lane_rows
            if row.get("reconstruction_status", "").startswith("preliminary_reconstructed")
            or row.get("reconstruction_status", "") == "source_verified"
        ]
        eligible = [row for row in lane_rows if row.get("primary_pool_eligible", "") == "yes"]
        source_clusters = sorted({row["independence_cluster"] for row in source_complete})
        eligible_clusters = sorted({row["independence_cluster"] for row in eligible})
        k = len(eligible_clusters)
        if k >= STABILITY_MIN_CLUSTERS:
            status = "stability_eligible"
        elif k >= EXPLORATORY_MIN_CLUSTERS:
            status = "exploratory_pooling_eligible"
        else:
            status = "not_poolable"
        lane_reports[lane] = {
            "effect_rows": len(lane_rows),
            "source_complete_effect_rows": len(source_complete),
            "source_complete_independent_clusters": len(source_clusters),
            "pool_eligible_effect_rows": len(eligible),
            "pool_eligible_independent_clusters": k,
            "status": status,
            "source_complete_clusters": source_clusters,
            "pool_eligible_clusters": eligible_clusters,
        }

    return {
        "existing_repository_thresholds": {
            "exploratory_min_independent_clusters": EXPLORATORY_MIN_CLUSTERS,
            "stability_min_independent_clusters": STABILITY_MIN_CLUSTERS,
        },
        "lanes": lane_reports,
        "manuscript_gate": "remain_frozen_until_ANALYSIS_COMPLETION_GATE_is_satisfied",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extractions_csv")
    parser.add_argument("--json-out")
    args = parser.parse_args(argv)
    report = readiness(read_rows(args.extractions_csv))
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
