from __future__ import annotations

import argparse
import json
from pathlib import Path

from trait_architecture.critical_definition_concordance import analyze_definitions


DEFAULT_CONTEXTS = ("HA", "HL", "HC", "KD", "HD")


def analyze(receipt: dict) -> dict:
    source_order = tuple(receipt["source"]["plots_in_phenological_order"])
    if source_order != DEFAULT_CONTEXTS:
        raise ValueError(
            f"unexpected Peucedanum plot order: {source_order!r}; expected {DEFAULT_CONTEXTS!r}"
        )

    beta = receipt["final_fruit_set_selection_gradient_on_perfect_flower_number"]
    differential = receipt["final_fruit_set_selection_differential_on_perfect_flower_number"]
    exponent = receipt["published_female_gain_exponent"]

    definitions = {
        "final_fruit_selection_gradient_beta": {
            context: float(beta[context]["beta"]) for context in DEFAULT_CONTEXTS
        },
        "final_fruit_selection_differential_S": {
            context: float(differential[context]["S"]) for context in DEFAULT_CONTEXTS
        },
        "female_gain_exponent_b_minus_1": {
            context: float(exponent[context]["b"]) - 1.0 for context in DEFAULT_CONTEXTS
        },
    }
    result = analyze_definitions(DEFAULT_CONTEXTS, definitions)

    return {
        "analysis": "peucedanum_critical_definition_concordance",
        "system": receipt["system"],
        "source_receipt_version": receipt["receipt_version"],
        "ordered_contexts": list(DEFAULT_CONTEXTS),
        "definition_semantics": {
            "final_fruit_selection_gradient_beta": "zero = no direct standardized selection gradient on perfect-flower production for final fruit set",
            "final_fruit_selection_differential_S": "zero = no univariate standardized selection differential on perfect-flower production for final fruit set",
            "female_gain_exponent_b_minus_1": "zero = female-gain exponent b equals 1, the boundary between decelerating and accelerating female gain",
        },
        "brackets": [
            {
                "definition": bracket.definition,
                "left_context": bracket.left_context,
                "right_context": bracket.right_context,
                "left_margin": bracket.left_margin,
                "right_margin": bracket.right_margin,
                "numeric_critical_context": bracket.numeric_critical_context,
                "status": bracket.status,
            }
            for bracket in result.brackets
        ],
        "classification": result.classification,
        "common_contexts": list(result.common_contexts),
        "numeric_critical_context": None,
        "numeric_nonidentification_reason": (
            "The published contexts are ordered categorical phenology/predation states; "
            "no preregistered common scalar environmental coordinate is available for interpolation."
        ),
        "interpretation": (
            "Three operational definitions independently place their coarse transition in the HL-HC bracket. "
            "This is evidence for a concordant observational critical region, not identification of the common SCH-BITA architecture surface C2."
        ),
        "claim_ceiling": (
            "same_coarse_observational_bracket_only; not_same_numeric_critical_point; "
            "not_causal_C2; not_calibrated_functional_weight; not_historical_modularization"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    result = analyze(receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
