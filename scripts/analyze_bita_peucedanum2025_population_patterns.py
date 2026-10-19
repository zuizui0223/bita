"""Real 2025 Peucedanum observational tests from exact HUSCAP data.

Core question: is allocation to specialized male flowers correlated with
antagonist exposure across real field populations and years? These are
POST-OPEN, descriptive and noncausal evidence; not an evolutionary transition
or direct test of BITA's K(u), s, heritability, or architecture fitness gap.

The script downloads the DOI-matched original archive, verifies an exact
SHA-256, computes plant-level and spatial summaries, and NEVER publishes raw
rows or IDs.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from scripts.audit_bita_peucedanum2025_huscap import fetch
from scripts.inspect_bita_peucedanum2025_raw import checked_csvs, group_means, number

DOI = "10.14943/hu95572"
SEED = 20261019
NULL = None


def average_ranks(values: list[float]) -> list[float]:
    """Midranks for ties, deterministic and dependency-free."""
    n = len(values)
    pairs = sorted((value, i) for i, value in enumerate(values))
    result = [0.0]*n
    start = 0
    while start < n:
        end = start + 1
        while end < n and pairs[end][0] == pairs[start][0]:
            end += 1
        midrank = ((start+1)+end)/2
        for _, idx in pairs[start:end]:
            result[idx] = midrank
        start = end
    return result


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 3:
        return None
    xm = statistics.fmean(x)
    ym = statistics.fmean(y)
    sx = sum((v-xm)**2 for v in x)
    sy = sum((v-ym)**2 for v in y)
    if sx <= 0 or sy <= 0:
        return None
    return sum((a-xm)*(b-ym) for a, b in zip(x, y))/math.sqrt(sx*sy)


def spearman(x: list[float], y: list[float]) -> float | None:
    return pearson(average_ranks(x), average_ranks(y))


def rho(rows: list[dict], x: str, y: str) -> float | None:
    valid = [r for r in rows if r.get(x) is not None and r.get(y) is not None]
    return spearman([r[x] for r in valid],[r[y] for r in valid])


def exact_plot_permutation(rows: list[dict], x: str, y: str) -> dict:
    """Exact two-sided permutation of FIVE plot-level means, 5!=120.

    This is an association test on 5 plot units, not on 18 plot×year units.
    """
    a = [r[x] for r in rows]
    b = [r[y] for r in rows]
    if len(rows) != 5 or any(v is None for v in a+b):
        raise ValueError("EXACT_PLOT_TEST_EXPECTS_FIVE_COMPLETE_PLOTS")
    observed = spearman(a,b)
    if observed is None:
        raise ValueError("CONSTANT_OR_NONFINITE_PLOT_MEANS")
    extreme = 0
    for perm in itertools.permutations(b):
        s = spearman(a,list(perm))
        extreme += abs(s) >= abs(observed)-1e-12
    return {
        "n_independent_geographic_plot_units": 5,
        "rho": observed,
        "p_exact_two_sided": extreme / math.factorial(5),
        "n_exact_permutations": math.factorial(5),
        "n_permutations_at_least_as_extreme": extreme,
    }


def group_average(rows: list[dict], y: str, years: set[str] | None = None) -> list[dict]:
    selected = [
        r for r in rows if r[y] is not None and
        (years is None or r["year"] in years)
    ]
    plots = sorted({r["plot"] for r in selected})
    out = []
    for plot in plots:
        rr = [r for r in selected if r["plot"] == plot]
        out.append({
            "plot": plot, "n_years_with_both": len(rr),
            "male_fraction": statistics.fmean(r["male_fraction_mean"] for r in rr),
            y: statistics.fmean(r[y] for r in rr),
        })
    return out


def permuted_spearman(x: list[float], y: list[float],
                      repetitions: int = 9999, seed: int = SEED) -> dict:
    if len(x) != len(y) or len(x) < 5:
        raise ValueError("NEED_AT_LEAST_FIVE_INDEPENDENT_PLANTS")
    observed = spearman(x,y)
    if observed is None:
        raise ValueError("CONSTANT_OR_NONFINITE_RANKS")
    target = average_ranks(x)
    rr = average_ranks(y)
    rng = random.Random(seed)
    exceed = 0
    for _ in range(repetitions):
        shuffled = rr.copy()
        rng.shuffle(shuffled)
        z = pearson(target, shuffled)
        exceed += abs(z) >= abs(observed)-1e-12
    return {
        "n_individuals": len(x),
        "spearman_rho": observed,
        "p_perm_two_sided": (exceed+1)/(repetitions+1),
        "permutations": repetitions,
    }


def analyze_data(raw: bytes) -> dict:
    tables = checked_csvs(raw)
    rows = group_means(tables["population"])
    all_pred = [r for r in rows if r["mean_predation"] is not None]
    all_years = sorted({r["year"] for r in rows})
    within_year = []
    for year in all_years:
        sub = [r for r in all_pred if r["year"] == year]
        within_year.append({
            "year": year, "n_plot_years_with_predation": len(sub),
            "rho_male_fraction_vs_predation": rho(
                sub, "male_fraction_mean", "mean_predation"
            ),
        })
    complete_all = group_average(rows,"mean_predation")
    complete_balanced = group_average(rows,"mean_predation",{"Y2022","Y2023"})
    if len(complete_all)!=5 or len(complete_balanced)!=5:
        raise ValueError("PLOT_GRAIN_CHANGED")
    summary = {
        "receipt_schema": "BITA_PEUCEDANUM2025_ORIGINAL_DATA_OBSERVATIONAL_V1",
        "data_level": "REANALYSIS_OF_SHA256_VERIFIED_PRIMARY_PUBLIC_RAW_DATA",
        "doi": DOI,
        "n_plants_total": len(tables["population"]),
        "n_paternity_plants": len(tables["paternity"]),
        "n_distinct_plots": len({r["plot"] for r in rows}),
        "n_plot_years": len(rows),
        "n_plot_years_with_predation": len(all_pred),
        "individual_predation_missing": sum(
            number(r["PredationR"]) is None for r in tables["population"]
        ),
        "n_oviposition_observed": sum(
            number(r["OvipN"]) is not None for r in tables["population"]
        ),
        "plot_year_descriptive_spearman": {
            "male_fraction_vs_predation": rho(
                all_pred, "male_fraction_mean", "mean_predation"
            ),
            "male_fraction_vs_oviposition": rho(
                rows, "male_fraction_mean", "mean_oviposition"
            ),
            "n_predation_complete": len(all_pred),
            "n_oviposition_complete": sum(
                r["mean_oviposition"] is not None for r in rows
            ),
            "note": "Plot-year units are REPEATED within five geographic plots: no unclustered p-value.",
        },
        "five_plot_exact": exact_plot_permutation(
            complete_all, "male_fraction","mean_predation"
        ),
        "balanced_2022_2023_five_plot_exact_post_open": exact_plot_permutation(
            complete_balanced,"male_fraction","mean_predation"
        ),
        "by_year_descriptive": within_year,
        "leave_one_plot_out_plot_year_rhos": {
            plot: rho(
                [r for r in all_pred if r["plot"] != plot],
                "male_fraction_mean","mean_predation",
            )
            for plot in sorted({r["plot"] for r in rows})
        },
    }
    # Cross-function check: same 106 individual plants with nuclear-marker
    # paternal success. This test is exploratory; no non-significance may be
    # re-labelled "equivalent / preserved male fitness".
    pairs = []
    for r in tables["paternity"]:
        h, m = number(r["HFlowerNo"]), number(r["MFlowerNo"])
        total, sired = number(r["TotalFlowerNo"]), number(r["SiredSeedNo"])
        female = number(r["EstFinalFruitNo"])
        if (h is None or m is None or h+m<=0 or total is None
                or sired is None):
            continue
        pairs.append({
            "male_fraction": m/(h+m),
            "total_display": total,
            "sired_seeds": sired,
            "female_final": female,
        })
    if len(pairs) < 30:
        raise ValueError("PATERNITY_SAMPLE_NO_LONGER_SUFFICIENT")
    summary["ha_paternity_exploratory_spearman"] = {
        "male_allocation_vs_siring": permuted_spearman(
            [r["male_fraction"] for r in pairs],
            [r["sired_seeds"] for r in pairs],
        ),
        "total_display_vs_siring": permuted_spearman(
            [r["total_display"] for r in pairs],
            [r["sired_seeds"] for r in pairs],
        ),
        "male_allocation_vs_estimated_female_final": permuted_spearman(
            [r["male_fraction"] for r in pairs if r["female_final"] is not None],
            [r["female_final"] for r in pairs if r["female_final"] is not None],
        ),
        "note": (
            "Observational correlations only, all on one HA-plot dataset. "
            "Other floral traits and size can confound associations. "
            "No null equivalence or causal male-function preservation claimed."
        ),
    }
    summary["preinterpretive_warning"] = (
        "The five plots are not five independent evolutionary transitions. "
        "Male-flower fraction is present-day allocation, not an observed "
        "ancestral shared-to-differentiated origin. PredationR has missingness "
        "and is an outcome/exposure proxy, not randomized selection strength. "
        "No K(u), genotype-accessibility, phylogenetic origin, or paired "
        "architecture fitness difference is measured. All tests post-open "
        "exploratory; the 2022–2023 subset is a sensitivity, not confirmatory."
    )
    summary["raw_rows_redistributed"] = False
    return summary


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,
                    default=Path("artifacts/bita_peucedanum2025_observational_v1.json"))
    args=ap.parse_args()
    result=analyze_data(fetch())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
