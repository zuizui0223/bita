"""Does male-biased floral allocation have an association beyond losing oviposition targets?

A post-open *observational* falsification/mediator-target sensitivity analysis
of SHA256-locked HUSCAP 2025 Peucedanum raw data (DOI 10.14943/hu95572).
No developmental K(u), mutant invasion or causal treatment is identified.
Only summary output is written; the source individual rows are not redistributed.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path

from scripts.audit_bita_peucedanum2025_huscap import fetch
from scripts.inspect_bita_peucedanum2025_raw import checked_csvs, number
from scripts.analyze_bita_peucedanum2025_within_context import (
    fwl, five_plot_jackknife, make_population_rows, SEED,
)


def residual_diagnostics(rows: list[dict], controls: tuple[str, ...],
                         *, permutations: int = 4999) -> dict:
    result=fwl(rows,controls=controls,permutations=permutations,seed=SEED)
    loo={}
    for plot in sorted({row["plot"] for row in rows}):
        remaining=[r for r in rows if r["plot"]!=plot]
        try:
            loo[plot]=fwl(remaining,controls=controls,permutations=99,seed=SEED)[
                "within_context_allocation_beta"]
        except ValueError:
            loo[plot]=None
    result["geographic_plot_leave_one_out"]=loo
    result["five_geographic_plot_jackknife"]=five_plot_jackknife(
        result["within_context_allocation_beta"], loo,
    )
    return result


def make_retention_rows(source: list[dict]) -> tuple[list[dict],dict]:
    """Only use compatible observed pre/post fruit counts with I>0 and F<=I.

    A final/initial ratio is not automatically seed-predation survival:
    unreported abortion and floral phenology may cause losses as well.
    """
    out=[]
    reasons=Counter()
    for r in source:
        h=number(r.get("HflowerN"))
        m=number(r.get("MflowerN"))
        height=number(r.get("Height"))
        initial=number(r.get("InitialFruitN"))
        final=number(r.get("FinalFruitN"))
        if any(v is None for v in (h,m,height,initial,final)):
            reasons["missing_required"]=reasons["missing_required"]+1
            continue
        if h<0 or m<0 or h+m<=0 or initial<0 or final<0:
            reasons["invalid_nonnegative_counts"]+=1
            continue
        if initial==0:
            reasons["zero_initial_unidentified_denominator"]+=1
            continue
        if final>initial:
            reasons["final_exceeds_initial"]+=1
            continue
        out.append({
            "group":r["Year"]+"/"+r["Plot"], "plot":r["Plot"],
            "x":m/(h+m),
            "log_total":math.log1p(m+h),
            "log_perfect":math.log1p(h),
            "height":height,
            "y":final/initial,
            "initial":initial,
            "final":final,
        })
    return out,{
        "total_rows":len(source),
        "matched_retention_rows":len(out),
        "excluded":sum(reasons.values()),
        "exclusion_reasons":dict(sorted(reasons.items())),
    }


def analyze(blob: bytes) -> dict:
    tables=checked_csvs(blob)
    population=tables["population"]
    exposure={}
    for outcome in ("ovip","predation"):
        original,miss=make_population_rows(population,outcome)
        primary=fwl(original, controls=("log_total","height"),permutations=999)
        controlled=residual_diagnostics(
            original, controls=("log_perfect","height"),
        )
        exposure[outcome]={
            "outcome":"log1p(egg_count)" if outcome=="ovip" else "observed_predation_fraction",
            "n_source_complete":len(original),
            "n_missing_or_invalid":miss,
            "original_total_display_adjusted_beta":
                primary["within_context_allocation_beta"],
            "alternative_perfect_target_adjusted":controlled,
            "interpretation_limit":(
                "Conditioning on the number of perfect flowers probes whether "
                "the negative male-fraction association is explained solely "
                "by fewer oviposition targets. Because male fraction is "
                "a deterministic function of perfect and male counts, "
                "this is a post-open conditional association, not evidence "
                "of an active deterrent property of male flowers."
            ),
        }
    valid,checks=make_retention_rows(population)
    models={}
    if len(valid)>=20:
        panels={
            "final_to_initial_fraction":valid,
            "common_initial_fruits_log": [
                {**r, "y":math.log1p(r["initial"])} for r in valid
            ],
            "common_final_fruits_log": [
                {**r, "y":math.log1p(r["final"])} for r in valid
            ],
            "matched_log_final_minus_initial": [
                {**r, "y":math.log1p(r["final"])-math.log1p(r["initial"])}
                for r in valid
            ],
        }
        for label, rows in panels.items():
            models[label]=residual_diagnostics(rows,controls=("log_total","height"))
            models[label]["outcome"]={
                "final_to_initial_fraction":"observed final fruits / initial fruits",
                "common_initial_fruits_log":"log1p(initial fruits) on exactly the retention rows",
                "common_final_fruits_log":"log1p(final fruits) on exactly the retention rows",
                "matched_log_final_minus_initial":"log1p(final fruits)-log1p(initial fruits) on identical rows",
            }[label]
        if any(model["n_individuals"]!=len(valid) for model in models.values()):
            raise AssertionError("FRUIT_COMMON_SUPPORT_MISMATCH")
    return {
        "receipt_schema":"BITA_PEUCEDANUM2025_POSTOPEN_EXPOSURE_RECOVERY_V1",
        "doi":"10.14943/hu95572",
        "data_level":"EXACT_SHA256_PUBLIC_ORIGINAL_OBSERVATIONAL_DATA",
        "target_exposure_adjusted":exposure,
        "matched_fruit_construction":checks,
        "matched_fruit_comparison":models,
        "raw_rows_redistributed":False,
        "causal_fitness_or_heritability_identified":False,
        "claim_boundary":(
            "Comparing male-fraction models with total-display versus "
            "perfect-flower exposure controls cannot identify a predator "
            "deterrent cause, since sex fraction and count components are "
            "compositionally linked. Matched fruit retention may reflect "
            "many unmeasured processes and assumes comparable collection "
            "stages. Five geographic plots offer very limited independent "
            "replication; t4 jackknife is a diagnostic, not a causal interval. "
            "Data cannot estimate BITA architecture K(u), fitness differences "
            "between ancestral and derived architectures, or evolutionary "
            "accessibility."
        ),
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,
                        default=Path("artifacts/bita_peucedanum2025_exposure_recovery_v1.json"))
    args=parser.parse_args()
    d=analyze(fetch())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(d,sort_keys=True))


if __name__=="__main__":
    main()
