"""Joint cross-network test of the BITA access-routing prediction.

The two public datasets have different response constructions and inferential
units, so raw observations are never pooled. Each network contributes one
Spearman rank association on a common directional construct:

    stronger access constraint -> greater bypass / robbing propensity

The primary joint statistic is an equal-network Fisher-z mean correlation.
The null shuffles Sakhalkar outcomes across plant species and Aubert/EPHI
outcomes within site, preserving the latter dataset's site composition.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_sakhalkar2023_network import (
    _find_workbook,
    _spearman,
    species_route_points,
)
from scripts.audit_sakhalkar2023_zenodo import (
    _download as _download_sakhalkar,
    read_xlsx_sheet_rows,
)
from scripts.analyze_aubert2026_zenodo_extension import (
    FILES as AUBERT_FILES,
    _download as _download_aubert,
    _read as _read_aubert,
    build_pair_site_rows,
)

SEED = 20260920


def _clip_rho(value: float) -> float:
    return min(0.999999999999, max(-0.999999999999, value))


def combine_rhos_equal_network(rhos: list[float]) -> float:
    """Equal-network Fisher-z mean, back-transformed to correlation scale."""
    if not rhos:
        raise ValueError("at least one network correlation is required")
    if any(not math.isfinite(rho) for rho in rhos):
        raise ValueError("all network correlations must be finite")
    z_mean = sum(math.atanh(_clip_rho(rho)) for rho in rhos) / len(rhos)
    return math.tanh(z_mean)


def _permute_within_site(
    values: list[float],
    sites: list[str],
    *,
    rng: random.Random,
) -> list[float]:
    by_site: dict[str, list[int]] = defaultdict(list)
    for index, site in enumerate(sites):
        by_site[site].append(index)

    out = list(values)
    for indices in by_site.values():
        local = [values[index] for index in indices]
        rng.shuffle(local)
        for index, value in zip(indices, local):
            out[index] = value
    return out


def summarize_joint(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    if len(sakhalkar_points) < 3:
        raise ValueError("too few Sakhalkar species-level points")
    if len(aubert_rows) < 4:
        raise ValueError("too few Aubert pair-site rows")
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    sx = [float(row["tube_length"]) for row in sakhalkar_points]
    sy = [float(row["balance"]) for row in sakhalkar_points]
    ax = [float(row["mismatch_log_t_over_b"]) for row in aubert_rows]
    ay = [float(row["robbery_rate"]) for row in aubert_rows]
    sites = [str(row["site"]) for row in aubert_rows]

    s_rho = _spearman(sx, sy)
    a_rho = _spearman(ax, ay)
    if not math.isfinite(s_rho) or not math.isfinite(a_rho):
        raise ValueError("network correlations must be finite")

    joint_fisher = combine_rhos_equal_network([s_rho, a_rho])
    joint_mean = (s_rho + a_rho) / 2.0

    rng_s = random.Random(seed)
    rng_a = random.Random(seed + 1)
    shuffled_s = list(sy)

    joint_extreme = 0
    s_extreme = 0
    a_extreme = 0
    positive_both = 0

    for _ in range(permutations):
        rng_s.shuffle(shuffled_s)
        perm_a = _permute_within_site(ay, sites, rng=rng_a)

        ps = _spearman(sx, shuffled_s)
        pa = _spearman(ax, perm_a)
        if not math.isfinite(ps) or not math.isfinite(pa):
            continue

        pj = combine_rhos_equal_network([ps, pa])
        if abs(pj) >= abs(joint_fisher) - 1e-15:
            joint_extreme += 1
        if abs(ps) >= abs(s_rho) - 1e-15:
            s_extreme += 1
        if abs(pa) >= abs(a_rho) - 1e-15:
            a_extreme += 1
        if ps > 0 and pa > 0:
            positive_both += 1

    result = {
        "analysis_name": "joint_equal_network_access_routing",
        "network_count": 2,
        "network_effects": {
            "sakhalkar": {
                "n_units": len(sakhalkar_points),
                "unit": "plant_species",
                "access_constraint": "tube_length",
                "bypass_response": "robbing_minus_thieving_balance",
                "rho": s_rho,
                "permutation_p_two_sided_recomputed": (s_extreme + 1) / (permutations + 1),
            },
            "aubert_ephi": {
                "n_units": len(aubert_rows),
                "unit": "bird_x_plant_x_site",
                "access_constraint": "log_flower_tube_over_bill",
                "bypass_response": "robbery_rate",
                "rho": a_rho,
                "site_count": len(set(sites)),
                "permutation_p_two_sided_within_site": (a_extreme + 1) / (permutations + 1),
            },
        },
        "joint_equal_network_fisher_z_rho": joint_fisher,
        "joint_equal_network_mean_rho": joint_mean,
        "joint_permutation_p_two_sided": (joint_extreme + 1) / (permutations + 1),
        "null_probability_both_positive": (positive_both + 1) / (permutations + 1),
        "network_direction_concordance": "2_of_2_positive",
        "sakhalkar_permutation_scheme": "across_species",
        "aubert_permutation_scheme": "within_site",
        "permutations": permutations,
        "seed": seed,
        "claim_boundary": (
            "Networks contribute equally to the joint statistic; raw observations are not pooled. "
            "The result tests recurrence of a common rank-based access-routing direction, not a "
            "shared causal coefficient or commensurate raw effect size."
        ),
        "guardrail": "Aggregate output only; no species or site identifiers are emitted.",
    }
    return result


def build_public_inputs() -> tuple[
    list[dict[str, float | str]],
    list[dict[str, float | str | bool | int]],
]:
    sakh_workbook = _find_workbook(_download_sakhalkar())
    visits = read_xlsx_sheet_rows(sakh_workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(sakh_workbook, "plant_traits")
    sakh_points = species_route_points(visits, traits)

    tables = {
        key: _read_aubert(_download_aubert(name))
        for key, name in AUBERT_FILES.items()
    }
    aubert_rows, _audit = build_pair_site_rows(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
    )
    return sakh_points, aubert_rows


def run(
    output: str | Path,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    sakh_points, aubert_rows = build_public_inputs()
    result = summarize_joint(
        sakh_points,
        aubert_rows,
        permutations=permutations,
        seed=seed,
    )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.output, permutations=args.permutations, seed=args.seed),
            indent=2,
            sort_keys=True,
        )
    )
