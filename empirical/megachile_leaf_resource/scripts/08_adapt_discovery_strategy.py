#!/usr/bin/env python3
"""Evaluate a reviewed discovery batch and emit the next test decision.

This script does not treat web-search hit counts as evidence. It consumes a
reviewed candidate table and decides whether to finish the batch, expand the
current strategy, refine inside the source, or pivot to the next source class.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from trait_architecture.discovery_adaptation import decide_next_strategy, round_from_records  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Reviewed candidate CSV")
    parser.add_argument("--strategy-id", required=True)
    parser.add_argument("--output", type=Path, required=True, help="JSON decision report")
    parser.add_argument("--min-batch-size", type=int, default=20)
    parser.add_argument("--min-action-yield", type=float, default=0.05)
    parser.add_argument("--min-trait-yield", type=float, default=0.02)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    round_ = round_from_records(args.strategy_id, records)
    decision = decide_next_strategy(
        round_,
        min_batch_size=args.min_batch_size,
        min_action_yield=args.min_action_yield,
        min_trait_yield=args.min_trait_yield,
    )
    report = {
        "strategy_id": round_.strategy_id,
        "candidates_checked": round_.candidates_checked,
        "direct_actions": round_.direct_actions,
        "plant_named_any_rank": round_.plant_named_any_rank,
        "trait_ready_records": round_.trait_ready_records,
        "action_yield": round_.action_yield,
        "plant_yield": round_.plant_yield,
        "trait_yield": round_.trait_yield,
        "decision": decision.status,
        "next_strategy_id": decision.next_strategy_id,
        "rationale": decision.rationale,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
