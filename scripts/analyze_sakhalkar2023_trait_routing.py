"""Source-defined multitrait routing model for Sakhalkar et al. 2023.

Predictors are frozen from the union of the source paper's parsimonious RDA models:
- robbers: tube_length + shape + tube_width
- thieves: brightness + shape + tube_length

The BITA response is plant-species robbing-vs-thieving balance. Numeric traits and
the response are rank transformed; shape is dummy coded. Significance uses
species-level response permutations. This is an observational routing analysis,
not a causal floral-defence experiment.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_sakhalkar2023_network import _as_float, _find_workbook, _rankdata
from scripts.audit_sakhalkar2023_zenodo import _download, read_xlsx_sheet_rows


PREDICTOR_BLOCKS = ("tube_length", "tube_width", "brightness", "shape")
SEED = 20260919


def build_species_trait_rows(
    raw_visits: list[dict[str, str]],
    traits: list[dict[str, str]],
) -> list[dict[str, float | str | None]]:
    visits = [
        row
        for row in raw_visits
        if str(row.get("behavior", "")).strip().lower() != "visiting"
    ]

    frequency: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in visits:
        spcode = str(row.get("spcode", "")).strip()
        behavior = str(row.get("behavior", "")).strip().lower()
        value = _as_float(str(row.get("freq_fm_per_species", "")).strip())
        if spcode and behavior and value is not None:
            frequency[spcode][behavior] += value

    trait_map: dict[str, dict[str, str]] = {}
    for row in traits:
        spcode = str(row.get("spcode", "")).strip()
        if spcode:
            trait_map[spcode] = row

    result: list[dict[str, float | str | None]] = []
    for spcode in sorted(set(frequency).intersection(trait_map)):
        rob = frequency[spcode].get("robbing", 0.0)
        thief = frequency[spcode].get("thieving", 0.0)
        total = rob + thief
        if total <= 0:
            continue
        trait = trait_map[spcode]
        shape = str(trait.get("shape", "")).strip()
        result.append(
            {
                "route_balance": (rob - thief) / total,
                "tube_length": _as_float(str(trait.get("tube_length", "")).strip()),
                "tube_width": _as_float(str(trait.get("tube_width", "")).strip()),
                "brightness": _as_float(str(trait.get("brightness", "")).strip()),
                "shape": shape or None,
            }
        )
    return result


def _zscore(values: list[float]) -> list[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    sd = math.sqrt(variance)
    if sd == 0:
        return [0.0 for _ in values]
    return [(value - mean) / sd for value in values]


def _transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def _matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    bt = _transpose(b)
    return [
        [sum(x * y for x, y in zip(row, col)) for col in bt]
        for row in a
    ]


def _matvec(a: list[list[float]], v: list[float]) -> list[float]:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def _invert(matrix: list[list[float]], ridge: float = 1e-9) -> list[list[float]]:
    n = len(matrix)
    work = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        work[i][i] += ridge

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(work[r][col]))
        if abs(work[pivot][col]) < 1e-12:
            raise ValueError("singular design matrix")
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]

        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]

        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            if factor == 0:
                continue
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[col])
            ]

    return [row[n:] for row in work]


def _fit_r2(x: list[list[float]], y: list[float], cols: list[int] | None = None) -> float:
    if cols is not None:
        x = [[row[index] for index in cols] for row in x]
    xt = _transpose(x)
    xtx = _matmul(xt, x)
    inv = _invert(xtx)
    xty = _matvec(xt, y)
    beta = _matvec(inv, xty)
    fitted = _matvec(x, beta)
    mean_y = sum(y) / len(y)
    ss_total = sum((value - mean_y) ** 2 for value in y)
    if ss_total <= 1e-15:
        return 0.0
    ss_resid = sum((obs - pred) ** 2 for obs, pred in zip(y, fitted))
    return max(0.0, min(1.0, 1.0 - ss_resid / ss_total))


def _design(rows: list[dict[str, float | str | None]]) -> tuple[list[list[float]], list[float], dict[str, list[int]], list[str]]:
    complete = [
        row
        for row in rows
        if all(row.get(key) is not None for key in ("tube_length", "tube_width", "brightness", "shape"))
    ]
    if len(complete) < 6:
        raise ValueError("too few complete species for source-defined multitrait model")

    response = _zscore(_rankdata([float(row["route_balance"]) for row in complete]))
    numeric = {
        key: _zscore(_rankdata([float(row[key]) for row in complete]))
        for key in ("tube_length", "tube_width", "brightness")
    }
    shape_levels = sorted({str(row["shape"]) for row in complete})
    reference = shape_levels[0]
    shape_dummies = [level for level in shape_levels if level != reference]

    x: list[list[float]] = []
    for i, row in enumerate(complete):
        values = [
            1.0,
            numeric["tube_length"][i],
            numeric["tube_width"][i],
            numeric["brightness"][i],
        ]
        values.extend(1.0 if str(row["shape"]) == level else 0.0 for level in shape_dummies)
        x.append(values)

    blocks: dict[str, list[int]] = {
        "tube_length": [1],
        "tube_width": [2],
        "brightness": [3],
        "shape": list(range(4, 4 + len(shape_dummies))),
    }
    return x, response, blocks, shape_levels


def benjamini_hochberg(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 1.0
    for rank_from_end, (name, pvalue) in enumerate(reversed(ordered), start=1):
        rank = m - rank_from_end + 1
        q = min(running, pvalue * m / rank)
        running = q
        adjusted[name] = min(1.0, q)
    return adjusted


def fit_source_defined_model(
    rows: list[dict[str, float | str | None]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    x, y, blocks, shape_levels = _design(rows)
    n = len(y)
    all_cols = list(range(len(x[0])))
    full_r2 = _fit_r2(x, y, all_cols)

    observed_delta: dict[str, float] = {}
    reduced_cols: dict[str, list[int]] = {}
    for block, indices in blocks.items():
        cols = [index for index in all_cols if index not in indices]
        reduced_cols[block] = cols
        reduced = _fit_r2(x, y, cols)
        observed_delta[block] = max(0.0, min(1.0, full_r2 - reduced))

    rng = random.Random(seed)
    full_extreme = 0
    block_extreme = {block: 0 for block in blocks}
    shuffled = list(y)

    for _ in range(permutations):
        rng.shuffle(shuffled)
        perm_full = _fit_r2(x, shuffled, all_cols)
        if perm_full >= full_r2 - 1e-12:
            full_extreme += 1
        for block, cols in reduced_cols.items():
            perm_reduced = _fit_r2(x, shuffled, cols)
            perm_delta = max(0.0, perm_full - perm_reduced)
            if perm_delta >= observed_delta[block] - 1e-12:
                block_extreme[block] += 1

    full_p = (full_extreme + 1) / (permutations + 1)
    block_p = {
        block: (block_extreme[block] + 1) / (permutations + 1)
        for block in blocks
    }
    qvalues = benjamini_hochberg(block_p)

    block_tests = {
        block: {
            "delta_r2": observed_delta[block],
            "permutation_p": block_p[block],
            "bh_q": qvalues[block],
        }
        for block in blocks
    }

    return {
        "analysis_name": "sakhalkar_source_defined_multitrait_route_model",
        "n_species_complete": n,
        "predictor_blocks": list(PREDICTOR_BLOCKS),
        "shape_levels": shape_levels,
        "full_model_r2": full_r2,
        "full_model_permutation_p": full_p,
        "block_tests": block_tests,
        "permutations": permutations,
        "seed": seed,
        "response": "rank-transformed species-level (robbing-thieving)/(robbing+thieving)",
        "predictor_provenance": {
            "robber_source_model": ["tube_length", "shape", "tube_width"],
            "thief_source_model": ["brightness", "shape", "tube_length"],
            "bita_union": list(PREDICTOR_BLOCKS),
        },
        "claim_boundary": (
            "Observational species-level rank model. Predictors were fixed from the "
            "source paper's parsimonious robber/thief RDA models. Response permutations "
            "test association, not causal floral-defence effects."
        ),
    }


def run(output_path: str | Path, *, permutations: int = 9999) -> dict[str, object]:
    workbook = _find_workbook(_download())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    rows = build_species_trait_rows(visits, traits)
    result = fit_source_defined_model(rows, permutations=permutations)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()
    result = run(args.output, permutations=args.permutations)
    print(json.dumps(result, indent=2, sort_keys=True))
