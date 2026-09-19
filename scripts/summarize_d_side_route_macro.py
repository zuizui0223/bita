"""Summarize the deduplicated D-side route-level macro corpus."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows


def _hypergeom_prob(a: int, row1: int, row2: int, col1: int, total: int) -> float:
    col2 = total - col1
    b = row1 - a
    c = col1 - a
    d = row2 - c
    if min(a, b, c, d) < 0:
        return 0.0
    return math.comb(col1, a) * math.comb(col2, b) / math.comb(total, row1)


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    row1, row2 = a + b, c + d
    col1, total = a + c, a + b + c + d
    lower = max(0, row1 - (total - col1))
    upper = min(row1, col1)
    observed = _hypergeom_prob(a, row1, row2, col1, total)
    return min(
        1.0,
        sum(
            prob
            for x in range(lower, upper + 1)
            if (prob := _hypergeom_prob(x, row1, row2, col1, total))
            <= observed + 1e-15
        ),
    )


def summarize_registry(rows: list[dict[str, str]]) -> dict[str, object]:
    ids = [row.get("study_program_id", "").strip() for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate study_program_id in route macro registry")
    if any(not value for value in ids):
        raise ValueError("blank study_program_id in route macro registry")

    modality_counts = Counter(row["broad_modality"] for row in rows)
    antagonism_counts = Counter(row["antagonist_state"] for row in rows)

    followup = [row for row in rows if row["pollination_followup"] == "yes"]
    state_counts = Counter(row["pollination_state_family"] for row in followup)

    followup_by_modality: dict[str, dict[str, int]] = {}
    for modality in sorted(modality_counts):
        subset = [row for row in rows if row["broad_modality"] == modality]
        followup_by_modality[modality] = {
            "measured": sum(row["pollination_followup"] == "yes" for row in subset),
            "total": len(subset),
        }

    chem = followup_by_modality.get("chemical", {"measured": 0, "total": 0})
    phys = followup_by_modality.get("physical", {"measured": 0, "total": 0})
    chem_yes, chem_no = chem["measured"], chem["total"] - chem["measured"]
    phys_yes, phys_no = phys["measured"], phys["total"] - phys["measured"]
    coverage_p = (
        fisher_two_sided(chem_yes, chem_no, phys_yes, phys_no)
        if chem["total"] and phys["total"]
        else None
    )

    return {
        "unique_study_programs": len(rows),
        "antagonist_state_counts": dict(sorted(antagonism_counts.items())),
        "modality_counts": dict(sorted(modality_counts.items())),
        "pollination_followup_programs": len(followup),
        "pollination_followup_fraction": len(followup) / len(rows) if rows else None,
        "pollination_followup_by_modality": followup_by_modality,
        "chemical_vs_physical_followup_fisher_p": coverage_p,
        "pollination_state_counts": dict(sorted(state_counts.items())),
        "fixed_interference_programs": state_counts.get("INTERFERENCE", 0),
        "context_dependent_programs": state_counts.get("CONTEXT_DEPENDENT", 0),
        "null_compatible_programs": state_counts.get("NULL_COMPATIBLE", 0),
        "improved_programs": state_counts.get("IMPROVED", 0),
        "unresolved_programs": state_counts.get("UNRESOLVED", 0),
        "claim_boundary": (
            "Corpus composition is conditional on D-role admission and is not a prevalence "
            "estimate for nature. Pollinator follow-up coverage is a study-design property."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = summarize_registry(load_csv_rows(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
