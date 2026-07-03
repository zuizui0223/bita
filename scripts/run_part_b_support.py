"""Run the full Part B support-route pipeline (layers B1-B4).

Usage:
    python scripts/run_part_b_support.py \
      empirical/broad_reality_evidence/broad_route_records.csv \
      empirical/broad_reality_evidence/part_b_arrow_effects.csv \
      empirical/broad_reality_evidence/part_b_arrow_strata.csv \
      configs/part_b_moderator_hypotheses.json \
      configs/part_b_break_even_scenarios.json \
      artifacts/part_b_support
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from trait_architecture.broad_meta_analysis import read_csv_rows, read_strata
from trait_architecture.part_b_pipeline import write_part_b_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route_records_csv")
    parser.add_argument("effect_extractions_csv")
    parser.add_argument("strata_csv")
    parser.add_argument("moderator_hypotheses_json")
    parser.add_argument("break_even_config_json")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    hypotheses = json.loads(Path(args.moderator_hypotheses_json).read_text(encoding="utf-8"))
    break_even_config = json.loads(Path(args.break_even_config_json).read_text(encoding="utf-8"))

    diagnostics = write_part_b_outputs(
        args.out_dir,
        route_rows=read_csv_rows(args.route_records_csv),
        effect_rows=read_csv_rows(args.effect_extractions_csv),
        strata=read_strata(args.strata_csv),
        moderator_hypotheses=hypotheses["hypotheses"],
        break_even_config=break_even_config,
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
