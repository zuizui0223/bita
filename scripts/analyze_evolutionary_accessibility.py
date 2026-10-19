"""Run explicitly hypothetical BITA architecture-accessibility parameter contrasts.

No source taxa, experimental observations or natural mutation distributions are
estimated here. Count frequencies refer ONLY to declared simulation grid.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

from trait_architecture.evolutionary_accessibility import example_readout, landscape

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "BITA_EVOLUTIONARY_ACCESSIBILITY_READOUT_V1.json"


def build_readout() -> dict:
    readout = example_readout()
    weights = ((1.0, 1.0), (0.5, 2.0), (2.0, 0.5))
    couplings = (0.0, 0.2, 0.5, 1.5)
    costs = (0.03, 0.15, 0.4)
    activation_scales = (0.01, 0.05, 0.2)
    distances = (0.3, 0.7, 1.0, 1.5, 2.0)

    classified: Counter[str] = Counter()
    sufficient_tested = 0
    strict_violation_count = 0
    excluded_near_boundary = 0

    for (w1, w2), coupling, cap, tau, d in product(
        weights, couplings, costs, activation_scales, distances,
    ):
        result = landscape(
            distance=d, weight_1=w1, weight_2=w2,
            coupling=coupling, activation_cost_cap=cap,
            activation_scale=tau,
        )
        classified[result.classification] += 1
        h = w1/(1.0+w1/w2)
        s = h/(h+coupling)
        global_sufficient_margin = s*h*d*d-cap
        local_trap_margin = cap-2*h*d*d*tau
        # Mathematically the positive margins guarantee global advantage
        # and negative small-step gradient. Omit near-machine-zero cases
        # from strict numerical certification, report them separately.
        if global_sufficient_margin > 1e-9 and local_trap_margin > 1e-9:
            sufficient_tested += 1
            if result.classification != "GLOBAL_GAIN_BUT_LOCAL_TRAP":
                strict_violation_count += 1
        elif global_sufficient_margin > 0 and local_trap_margin > 0:
            excluded_near_boundary += 1

    n = len(weights)*len(couplings)*len(costs)*len(activation_scales)*len(distances)
    if sum(classified.values()) != n or strict_violation_count:
        raise AssertionError("simulation grid or sufficient-bound regression failed")
    readout["registered_grid"] = {
        "weights": weights,
        "couplings": couplings,
        "activation_cost_caps": costs,
        "activation_scales": activation_scales,
        "optimum_distances": distances,
        "n": n,
    }
    readout["counts_hypothetical_parameter_cells"] = dict(sorted(classified.items()))
    readout["analytic_sufficient_valley_condition"] = (
        "2*h*d**2*tau < Kcap < s*h*d**2; s=h/(h+lambda)"
    )
    readout["analytic_sufficient_valley_strict_tests"] = {
        "passed": sufficient_tested,
        "violations": strict_violation_count,
        "near_boundary_cases_not_classified_as_strict": excluded_near_boundary,
        "margin_requirement": "both strict analytic margins > 1e-9",
    }
    readout["claim_boundary"] = (
        "A finite theoretical grid is not an estimate of natural strategy prevalence. "
        "No evolutionary fixation, historical architecture origin, genetics, empirical "
        "cost function, ecological parameter mapping or cross-world fitness comparator "
        "has been measured."
    )
    return readout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    receipt = build_readout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output),
        "grid_n": receipt["registered_grid"]["n"],
        "counts": receipt["counts_hypothetical_parameter_cells"],
        "sufficient_valley_tests": receipt["analytic_sufficient_valley_strict_tests"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
