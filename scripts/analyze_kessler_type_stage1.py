"""Analyze a prospective Kessler-type Stage-1 2x2 reproductive experiment.

The registered Stage-1 target is the additive probability-scale interaction

    Delta_AD = p11 - p10 - p01 + p00

on one predeclared binary reproductive endpoint. The input contract preserves
plant identity, matched replicate blocks, retention/exclusions, assignment
mode, and the organ scope of the D intervention.

The first-pass uncertainty analysis resamples complete matched blocks. It does
not pretend individual flowers are exchangeable. The resulting 95% interval is
passed directly to ``classify_escape_criterion``. Mechanism allocation is not
attempted here.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import random
import sys

try:
    from trait_architecture.partial_identification import Interval, classify_escape_criterion
except ModuleNotFoundError:  # direct script execution from repository root
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from trait_architecture.partial_identification import Interval, classify_escape_criterion


REQUIRED_FIELDS = (
    "observation_id",
    "block_id",
    "plant_id",
    "flower_id",
    "A",
    "D",
    "retained",
    "outcome_binary",
    "outcome_id",
    "d_intervention_scope",
    "assignment_mode",
    "exclusion_reason",
)
ALLOWED_SCOPE = {
    "FLOWER_RESTRICTED_VALIDATED",
    "SYSTEMIC_SOURCE_FAITHFUL",
    "UNVERIFIED",
}
ALLOWED_ASSIGNMENT = {
    "RANDOMIZED_INTERVENTION",
    "SOURCE_FAITHFUL_GENOTYPE",
    "OTHER_PREDECLARED",
}
CELL_ORDER = ((1, 1), (1, 0), (0, 1), (0, 0))
CELL_NAME = {(1, 1): "p11", (1, 0): "p10", (0, 1): "p01", (0, 0): "p00"}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("input CSV contains no observations")
    return rows


def _parse_bit(value: str, name: str) -> int:
    if value not in {"0", "1"}:
        raise ValueError(f"{name} must be 0 or 1")
    return int(value)


def _validate_rows(rows: list[dict[str, str]], *, min_blocks: int) -> dict[str, object]:
    ids = [row["observation_id"] for row in rows]
    if any(not value for value in ids):
        raise ValueError("observation_id cannot be blank")
    if len(set(ids)) != len(ids):
        raise ValueError("observation_id must be unique")

    for field in (
        "block_id",
        "plant_id",
        "flower_id",
        "A",
        "D",
        "retained",
        "outcome_id",
        "d_intervention_scope",
        "assignment_mode",
    ):
        if any(not row[field] for row in rows):
            raise ValueError(f"{field} cannot be blank")

    outcome_ids = {row["outcome_id"] for row in rows}
    scopes = {row["d_intervention_scope"] for row in rows}
    assignments = {row["assignment_mode"] for row in rows}
    if len(outcome_ids) != 1:
        raise ValueError("one Stage-1 package must contain exactly one primary outcome_id")
    if len(scopes) != 1 or next(iter(scopes)) not in ALLOWED_SCOPE:
        raise ValueError("d_intervention_scope must be one consistent registered value")
    if len(assignments) != 1 or next(iter(assignments)) not in ALLOWED_ASSIGNMENT:
        raise ValueError("assignment_mode must be one consistent registered value")

    plant_cell: dict[str, tuple[int, int]] = {}
    for row in rows:
        a = _parse_bit(row["A"], "A")
        d = _parse_bit(row["D"], "D")
        retained = _parse_bit(row["retained"], "retained")
        cell = (a, d)
        prior = plant_cell.setdefault(row["plant_id"], cell)
        if prior != cell:
            raise ValueError(f"plant_id {row['plant_id']} changes A/D coordinate")
        if retained:
            _parse_bit(row["outcome_binary"], "outcome_binary for retained rows")
            if row["exclusion_reason"]:
                raise ValueError("retained rows must not have exclusion_reason")
        else:
            if not row["exclusion_reason"]:
                raise ValueError("excluded rows require exclusion_reason")
            if row["outcome_binary"] not in {"", "0", "1"}:
                raise ValueError("excluded outcome_binary must be blank, 0 or 1")

    retained_rows = [row for row in rows if row["retained"] == "1"]
    if not retained_rows:
        raise ValueError("no retained observations")

    blocks = sorted({row["block_id"] for row in retained_rows})
    if len(blocks) < min_blocks:
        raise ValueError(f"need at least {min_blocks} complete retained blocks; got {len(blocks)}")
    for block in blocks:
        cells = {
            (int(row["A"]), int(row["D"]))
            for row in retained_rows
            if row["block_id"] == block
        }
        if cells != set(CELL_ORDER):
            raise ValueError(f"block {block} is incomplete after retention: {sorted(cells)}")

    return {
        "outcome_id": next(iter(outcome_ids)),
        "d_intervention_scope": next(iter(scopes)),
        "assignment_mode": next(iter(assignments)),
        "block_count": len(blocks),
        "plant_count": len(plant_cell),
    }


def _cell_probabilities(rows: list[dict[str, str]]) -> dict[tuple[int, int], float]:
    result: dict[tuple[int, int], float] = {}
    for cell in CELL_ORDER:
        values = [
            int(row["outcome_binary"])
            for row in rows
            if row["retained"] == "1" and (int(row["A"]), int(row["D"])) == cell
        ]
        if not values:
            raise ValueError(f"cell {cell} has no retained outcomes")
        result[cell] = sum(values) / len(values)
    return result


def _delta(probabilities: dict[tuple[int, int], float]) -> float:
    return (
        probabilities[(1, 1)]
        - probabilities[(1, 0)]
        - probabilities[(0, 1)]
        + probabilities[(0, 0)]
    )


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot take quantile of empty values")
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def _block_bootstrap_delta_interval(
    rows: list[dict[str, str]],
    *,
    confidence: float,
    iterations: int,
    seed: int,
) -> Interval:
    retained = [row for row in rows if row["retained"] == "1"]
    by_block: dict[str, list[dict[str, str]]] = {}
    for row in retained:
        by_block.setdefault(row["block_id"], []).append(row)
    block_ids = sorted(by_block)
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(iterations):
        sampled = [rng.choice(block_ids) for _ in block_ids]
        resampled = [row for block in sampled for row in by_block[block]]
        draws.append(_delta(_cell_probabilities(resampled)))
    alpha = 1.0 - confidence
    return Interval(_quantile(draws, alpha / 2.0), _quantile(draws, 1.0 - alpha / 2.0))


def _cell_receipts(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    receipts: dict[str, dict[str, object]] = {}
    for cell in CELL_ORDER:
        introduced = [row for row in rows if (int(row["A"]), int(row["D"])) == cell]
        retained = [row for row in introduced if row["retained"] == "1"]
        successes = sum(int(row["outcome_binary"]) for row in retained)
        plants = {row["plant_id"] for row in introduced}
        receipts[CELL_NAME[cell]] = {
            "A": cell[0],
            "D": cell[1],
            "introduced": len(introduced),
            "retained": len(retained),
            "retention_fraction": len(retained) / len(introduced),
            "successes": successes,
            "probability": successes / len(retained),
            "plant_count": len(plants),
        }
    return receipts


def analyze_stage1(
    rows: list[dict[str, str]],
    *,
    iterations: int = 10000,
    seed: int = 20260829,
    min_blocks: int = 4,
) -> dict[str, object]:
    if iterations < 1000:
        raise ValueError("bootstrap iterations must be at least 1000")
    if min_blocks < 2:
        raise ValueError("min_blocks must be at least 2")
    identity = _validate_rows(rows, min_blocks=min_blocks)
    retained = [row for row in rows if row["retained"] == "1"]
    probabilities = _cell_probabilities(retained)
    point = _delta(probabilities)
    interval = _block_bootstrap_delta_interval(
        rows,
        confidence=0.95,
        iterations=iterations,
        seed=seed,
    )
    decision = classify_escape_criterion(interval)

    scope = str(identity["d_intervention_scope"])
    if scope == "FLOWER_RESTRICTED_VALIDATED":
        scope_ceiling = "D intervention is validated as flower-restricted for the declared experiment."
    elif scope == "SYSTEMIC_SOURCE_FAITHFUL":
        scope_ceiling = "The total sign is interpretable for the source-faithful systemic D intervention, not as a flower-exclusive defence effect."
    else:
        scope_ceiling = "D intervention scope is unverified; do not promote the result to a flower-specific defence claim."

    return {
        "analysis_id": "kessler_type_stage1_trial_analysis_v1",
        **identity,
        "primary_estimand": "additive_probability_scale_Delta_AD",
        "delta_ad_point": point,
        "delta_ad_95pct_block_bootstrap": {"low": interval.low, "high": interval.high},
        "escape_status": decision,
        "interval_method": "percentile_bootstrap_of_complete_matched_blocks",
        "bootstrap_iterations": iterations,
        "bootstrap_seed": seed,
        "cells": _cell_receipts(rows),
        "excluded_observations": sum(row["retained"] == "0" for row in rows),
        "scope_claim_ceiling": scope_ceiling,
        "claim_boundary": (
            "Stage 1 decides only the total A x D sign on the declared binary reproductive outcome. "
            "The block bootstrap is a prespecified first-pass design-based uncertainty lane and does not allocate rho_delta, iota_delta or kappa_delta. "
            "A future hierarchical/randomization analysis may supersede the bootstrap if it preserves the same estimand and registered decision rule."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260829)
    parser.add_argument("--min-blocks", type=int, default=4)
    args = parser.parse_args(argv)

    result = analyze_stage1(
        _read_rows(args.input_csv),
        iterations=args.iterations,
        seed=args.seed,
        min_blocks=args.min_blocks,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result["escape_status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
