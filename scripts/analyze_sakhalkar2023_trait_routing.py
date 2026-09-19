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



def trait_coverage_summary(
    rows: list[dict[str, float | str | None]],
) -> dict[str, object]:
    nonmissing = {
        key: sum(row.get(key) is not None for row in rows)
        for key in PREDICTOR_BLOCKS
    }

    def complete(keys: tuple[str, ...]) -> int:
        return sum(all(row.get(key) is not None for key in keys) for row in rows)

    return {
        "cheating_species": len(rows),
        "nonmissing": nonmissing,
        "robber_source_complete": complete(("tube_length", "tube_width", "shape")),
        "thief_source_complete": complete(("tube_length", "brightness", "shape")),
        "union_complete": complete(PREDICTOR_BLOCKS),
    }

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



def _design_for_predictors(
    rows: list[dict[str, float | str | None]],
    predictors: tuple[str, ...],
) -> tuple[list[list[float]], list[float], dict[str, list[int]], list[str]]:
    complete = [
        row
        for row in rows
        if all(row.get(key) is not None for key in predictors)
    ]
    if len(complete) < 6:
        raise ValueError("too few complete species for source-defined multitrait model")

    response = _zscore(_rankdata([float(row["route_balance"]) for row in complete]))
    numeric_predictors = [
        key for key in predictors if key in {"tube_length", "tube_width", "brightness"}
    ]
    numeric = {
        key: _zscore(_rankdata([float(row[key]) for row in complete]))
        for key in numeric_predictors
    }

    shape_levels: list[str] = []
    shape_dummies: list[str] = []
    if "shape" in predictors:
        shape_levels = sorted({str(row["shape"]) for row in complete})
        reference = shape_levels[0]
        shape_dummies = [level for level in shape_levels if level != reference]

    x: list[list[float]] = []
    blocks: dict[str, list[int]] = {}
    next_col = 1
    for key in numeric_predictors:
        blocks[key] = [next_col]
        next_col += 1
    if "shape" in predictors:
        blocks["shape"] = list(range(next_col, next_col + len(shape_dummies)))

    for i, row in enumerate(complete):
        values = [1.0]
        values.extend(numeric[key][i] for key in numeric_predictors)
        if "shape" in predictors:
            values.extend(
                1.0 if str(row["shape"]) == level else 0.0
                for level in shape_dummies
            )
        x.append(values)

    return x, response, blocks, shape_levels


def _design(
    rows: list[dict[str, float | str | None]],
) -> tuple[list[list[float]], list[float], dict[str, list[int]], list[str]]:
    return _design_for_predictors(rows, PREDICTOR_BLOCKS)


def _prepare_fitter(
    x: list[list[float]],
    cols: list[int],
) -> tuple[list[list[float]], list[list[float]]]:
    selected = [[row[index] for index in cols] for row in x]
    xt = _transpose(selected)
    inverse = _invert(_matmul(xt, selected))
    coefficient_operator = _matmul(inverse, xt)
    return selected, coefficient_operator


def _fitted_r2(
    fitter: tuple[list[list[float]], list[list[float]]],
    y: list[float],
) -> float:
    selected, coefficient_operator = fitter
    beta = _matvec(coefficient_operator, y)
    fitted = _matvec(selected, beta)
    mean_y = sum(y) / len(y)
    ss_total = sum((value - mean_y) ** 2 for value in y)
    if ss_total <= 1e-15:
        return 0.0
    ss_resid = sum((obs - pred) ** 2 for obs, pred in zip(y, fitted))
    return max(0.0, min(1.0, 1.0 - ss_resid / ss_total))


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



def _fit_predictor_model(
    rows: list[dict[str, float | str | None]],
    predictors: tuple[str, ...],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    x, y, blocks, shape_levels = _design_for_predictors(rows, predictors)
    n = len(y)
    all_cols = list(range(len(x[0])))
    full_fitter = _prepare_fitter(x, all_cols)
    full_r2 = _fitted_r2(full_fitter, y)

    reduced_fitters: dict[str, tuple[list[list[float]], list[list[float]]]] = {}
    observed_delta: dict[str, float] = {}
    for block, indices in blocks.items():
        cols = [index for index in all_cols if index not in indices]
        fitter = _prepare_fitter(x, cols)
        reduced_fitters[block] = fitter
        reduced = _fitted_r2(fitter, y)
        observed_delta[block] = max(0.0, min(1.0, full_r2 - reduced))

    rng = random.Random(seed)
    full_extreme = 0
    block_extreme = {block: 0 for block in blocks}
    shuffled = list(y)

    for _ in range(permutations):
        rng.shuffle(shuffled)
        perm_full = _fitted_r2(full_fitter, shuffled)
        if perm_full >= full_r2 - 1e-12:
            full_extreme += 1
        for block, fitter in reduced_fitters.items():
            perm_reduced = _fitted_r2(fitter, shuffled)
            perm_delta = max(0.0, perm_full - perm_reduced)
            if perm_delta >= observed_delta[block] - 1e-12:
                block_extreme[block] += 1

    full_p = (full_extreme + 1) / (permutations + 1)
    block_p = {
        block: (block_extreme[block] + 1) / (permutations + 1)
        for block in blocks
    }
    qvalues = benjamini_hochberg(block_p)

    return {
        "n_species_complete": n,
        "predictor_blocks": list(predictors),
        "shape_levels": shape_levels,
        "full_model_r2": full_r2,
        "full_model_permutation_p": full_p,
        "block_tests": {
            block: {
                "delta_r2": observed_delta[block],
                "permutation_p": block_p[block],
                "bh_q": qvalues[block],
            }
            for block in blocks
        },
        "permutations": permutations,
        "seed": seed,
    }


def fit_source_defined_model(
    rows: list[dict[str, float | str | None]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    result = _fit_predictor_model(
        rows,
        PREDICTOR_BLOCKS,
        permutations=permutations,
        seed=seed,
    )
    return {
        "analysis_name": "sakhalkar_source_defined_multitrait_route_model",
        **result,
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


def fit_source_model_set(
    rows: list[dict[str, float | str | None]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    coverage = trait_coverage_summary(rows)
    model_specs = {
        "robber_source_predictors": ("tube_length", "tube_width", "shape"),
        "thief_source_predictors": ("tube_length", "brightness", "shape"),
        "union_predictors": PREDICTOR_BLOCKS,
    }
    models: dict[str, object] = {}
    for offset, (name, predictors) in enumerate(model_specs.items()):
        complete_n = sum(
            all(row.get(key) is not None for key in predictors) for row in rows
        )
        if complete_n < 6:
            models[name] = {
                "status": "INSUFFICIENT_COMPLETE_CASES",
                "n_species_complete": complete_n,
                "predictor_blocks": list(predictors),
            }
            continue
        models[name] = {
            "status": "FIT",
            **_fit_predictor_model(
                rows,
                predictors,
                permutations=permutations,
                seed=seed + offset,
            ),
        }

    return {
        "analysis_name": "sakhalkar_source_defined_trait_routing_models",
        "coverage": coverage,
        "models": models,
        "response": "rank-transformed species-level (robbing-thieving)/(robbing+thieving)",
        "predictor_provenance": {
            "robber_source_model": ["tube_length", "shape", "tube_width"],
            "thief_source_model": ["brightness", "shape", "tube_length"],
            "union": list(PREDICTOR_BLOCKS),
        },
        "claim_boundary": (
            "No imputation is used. Source-defined predictor sets are fitted only "
            "when at least six cheating species have complete data. Models may use "
            "different complete-case species subsets and therefore are not compared "
            "by raw R2 as if they shared an identical sample."
        ),
    }


def run(output_path: str | Path, *, permutations: int = 9999) -> dict[str, object]:
    workbook = _find_workbook(_download())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    rows = build_species_trait_rows(visits, traits)
    result = fit_source_model_set(rows, permutations=permutations)
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
