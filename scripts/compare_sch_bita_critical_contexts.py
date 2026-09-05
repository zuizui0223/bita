"""Compare SCH and BITA zero crossings on one declared control axis.

Input CSVs must already contain commensurable signed margins with the same
fitness-scale semantics. This script intentionally refuses raw state-optimum
separation or raw R_state unless the user has precomputed a common margin.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trait_architecture.critical_context import compare_critical_contexts


REQUIRED_FIELDS = ("context_id", "context_value", "margin", "fitness_scale_id", "margin_semantics")
EXPECTED_SEMANTICS = "POSITIVE_MEANS_DIFFERENTIATED_ARCHITECTURE_FAVOURED"


def _read(path: Path) -> tuple[list[tuple[float, float]], str]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != REQUIRED_FIELDS:
            raise ValueError(f"{path}: columns must be {REQUIRED_FIELDS!r}")
        rows = list(reader)
    if len(rows) < 2:
        raise ValueError(f"{path}: at least two rows are required")
    scales = {row["fitness_scale_id"].strip() for row in rows}
    if len(scales) != 1 or "" in scales:
        raise ValueError(f"{path}: exactly one non-empty fitness_scale_id is required")
    semantics = {row["margin_semantics"].strip() for row in rows}
    if semantics != {EXPECTED_SEMANTICS}:
        raise ValueError(f"{path}: margin_semantics must be {EXPECTED_SEMANTICS!r}")
    points = [(float(row["context_value"]), float(row["margin"])) for row in rows]
    return points, next(iter(scales))


def compare_files(sch_path: Path, bita_path: Path, config: dict) -> dict:
    sch_points, sch_scale = _read(sch_path)
    bita_points, bita_scale = _read(bita_path)
    if sch_scale != bita_scale:
        raise ValueError("SCH and BITA margins must use the same fitness_scale_id")
    result = compare_critical_contexts(
        sch_points,
        bita_points,
        context_tolerance=float(config["context_tolerance"]),
        zero_tolerance=float(config.get("zero_tolerance", 1e-12)),
    )
    return {
        "analysis": "sch_bita_critical_context_comparison",
        "fitness_scale_id": sch_scale,
        "sch_critical_context": result.sch_crossing.context,
        "bita_critical_context": result.bita_crossing.context,
        "delta_context": result.delta_context,
        "absolute_delta_context": result.absolute_delta_context,
        "context_tolerance": result.tolerance,
        "classification": result.classification,
        "sch_bracket": {
            "left_context": result.sch_crossing.left_context,
            "right_context": result.sch_crossing.right_context,
            "left_margin": result.sch_crossing.left_margin,
            "right_margin": result.sch_crossing.right_margin,
            "exact_grid_hit": result.sch_crossing.exact_grid_hit,
        },
        "bita_bracket": {
            "left_context": result.bita_crossing.left_context,
            "right_context": result.bita_crossing.right_context,
            "left_margin": result.bita_crossing.left_margin,
            "right_margin": result.bita_crossing.right_margin,
            "exact_grid_hit": result.bita_crossing.exact_grid_hit,
        },
        "claim_ceiling": (
            "same-vs-parallel critical context on one declared commensurable margin axis; "
            "not historical modularization and not valid for raw noncommensurable chapter metrics"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sch_csv", type=Path)
    parser.add_argument("bita_csv", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = compare_files(args.sch_csv, args.bita_csv, config)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
