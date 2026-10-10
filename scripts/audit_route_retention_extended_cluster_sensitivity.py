#!/usr/bin/env python3
"""Post-outcome robustness of extended robbery MLE to bird/site deletion.

The original 3-state Poisson formula and the minimal-face construction are
unchanged. This is an exploratory stability audit, not confirmatory evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.analyze_route_retention_extended_mle import read_records, fit_extended, joint_category_rank


def summarize(records, *, kind):
    if kind == "site":
        selector = lambda record: record[1].split("@@")[1]
    elif kind == "bird":
        selector = lambda record: record[1].split("@@")[0]
    else:
        raise ValueError(kind)

    units = sorted({selector(record) for record in records})
    fits = []
    for unit in units:
        remaining = [rec for rec in records if selector(rec) != unit]
        estimate = fit_extended(remaining)
        if estimate["status"] == "FIT":
            rank = joint_category_rank(remaining)["joint_contrast_rank"]
            if rank != 2:
                estimate["status"] = "RANK_DEFICIENT"
                estimate["joint_contrast_rank"] = rank
        fits.append({"left_out":unit, **estimate})

    valid = [item for item in fits if item["status"] == "FIT"]
    keys = ("moderate_accessible","severe_accessible","severe_moderate")
    ranges = {
        key: {
            "min":min(item["rate_ratios"][key] for item in valid),
            "max":max(item["rate_ratios"][key] for item in valid),
            "fraction_less_than_one":sum(item["rate_ratios"][key] < 1 for item in valid)/len(valid),
            "minimum_on_deletion":min(valid,key=lambda r:r["rate_ratios"][key])["left_out"],
            "maximum_on_deletion":max(valid,key=lambda r:r["rate_ratios"][key])["left_out"],
        } if valid else None
        for key in keys
    }
    return {
        "grouping":kind,
        "groups":len(units),
        "successful_refits":len(valid),
        "all_refits":fits,
        "ranges":ranges,
    }


def run(source: Path, output: Path):
    records = read_records(source)
    by_site = summarize(records, kind="site")
    by_bird = summarize(records, kind="bird")
    site07 = next((item for item in by_site["all_refits"] if item["left_out"] == "site_07"),None)
    result = {
        "analysis":"POST_OUTCOME_EXTENDED_MLE_SITE_BIRD_DELETION",
        "source_artifact_id":11293379572,
        "hummingbird_opportunities":len(records),
        "leave_site":by_site,
        "leave_bird":by_bird,
        "site_07_deletion":site07,
        "claim_boundary":(
            "These are leave-one-site and leave-one-species point sensitivity ranges, "
            "not confidence intervals, independent network replications or causal "
            "evidence. This extends post-outcome method diagnostics only."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "site":{"groups":by_site["groups"],"successful":by_site["successful_refits"],"ranges":by_site["ranges"]},
        "bird":{"groups":by_bird["groups"],"successful":by_bird["successful_refits"],"ranges":by_bird["ranges"]},
        "site_07":site07,
    },indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip",type=Path)
    parser.add_argument("output_json",type=Path)
    args=parser.parse_args()
    run(args.source_zip,args.output_json)
