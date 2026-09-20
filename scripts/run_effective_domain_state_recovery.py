"""Macro state-recovery analysis for the effective-domain BITA hypothesis.

This analysis uses the broader D->pollination evidence layer rather than only the
strict direction-supported Stage-2 subset. It distinguishes:
- NO_INTERFERENCE_OBSERVED: preserved/improved OR null-compatible/no detected change
- MIXED: dose/exposure/response-stage dependent
- IMPAIRED: direction-supported pollinator impairment

NO_INTERFERENCE_OBSERVED is explicitly not an equivalence claim.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows


OUTCOME_FAMILIES = (
    "NO_INTERFERENCE_OBSERVED",
    "MIXED",
    "IMPAIRED",
)


def classify_outcome_family(state: str) -> str | None:
    state = str(state or "").strip()
    if state in {"PRESERVED_OR_IMPROVED", "NO_DETECTED_CHANGE"}:
        return "NO_INTERFERENCE_OBSERVED"
    if state == "MIXED":
        return "MIXED"
    if state == "IMPAIRED":
        return "IMPAIRED"
    return None


def domain_prediction(domain: str) -> str | None:
    domain = str(domain or "").strip()
    return {
        "SEPARATED": "NO_INTERFERENCE_OBSERVED",
        "TRANSITIONAL": "MIXED",
        "OVERLAPPED": "IMPAIRED",
    }.get(domain)


def exact_alignment_probability(group_sizes: list[int]) -> float:
    """Probability of one perfect category allocation under fixed margins.

    This quantity is used only when the observed outcome-family counts exactly
    equal the domain-group sizes and every scored row matches the fixed domain
    rule. It is a descriptive randomization alignment probability, not a
    confirmatory p-value for a prospectively preregistered hypothesis.
    """
    group_sizes = [int(value) for value in group_sizes if int(value) > 0]
    total = sum(group_sizes)
    if total == 0:
        return math.nan
    denominator = math.factorial(total)
    numerator = 1
    for size in group_sizes:
        numerator *= math.factorial(size)
    return numerator / denominator


def _scored_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    scored: list[dict[str, str]] = []
    for row in rows:
        prediction = domain_prediction(row.get("pre_outcome_domain_code", ""))
        outcome = classify_outcome_family(row.get("pollinator_cost_state_derived", ""))
        if prediction is None or outcome is None:
            continue
        item = dict(row)
        item["_domain_prediction"] = prediction
        item["_outcome_family"] = outcome
        scored.append(item)
    return scored


def _majority_label(labels: list[str]) -> str | None:
    if not labels:
        return None
    counts = Counter(labels)
    max_count = max(counts.values())
    tied = sorted(label for label, count in counts.items() if count == max_count)
    return tied[0]


def _modality_loo_accuracy(rows: list[dict[str, str]]) -> tuple[int, int]:
    correct = 0
    for index, row in enumerate(rows):
        train = [candidate for i, candidate in enumerate(rows) if i != index]
        modality = row.get("defence_modality", "")
        same_modality = [
            candidate["_outcome_family"]
            for candidate in train
            if candidate.get("defence_modality", "") == modality
        ]
        prediction = _majority_label(same_modality)
        if prediction is None:
            prediction = _majority_label(
                [candidate["_outcome_family"] for candidate in train]
            )
        if prediction == row["_outcome_family"]:
            correct += 1
    return correct, len(rows)


def _modality_model(rows: list[dict[str, str]]) -> tuple[dict[str, str], str | None]:
    by_modality: dict[str, list[str]] = {}
    for row in rows:
        by_modality.setdefault(row.get("defence_modality", ""), []).append(
            row["_outcome_family"]
        )
    mapping = {
        modality: _majority_label(labels)
        for modality, labels in by_modality.items()
        if _majority_label(labels) is not None
    }
    fallback = _majority_label([row["_outcome_family"] for row in rows])
    return mapping, fallback


def _apply_modality_model(
    rows: list[dict[str, str]],
    mapping: dict[str, str],
    fallback: str | None,
) -> tuple[int, int]:
    correct = 0
    for row in rows:
        prediction = mapping.get(row.get("defence_modality", ""), fallback)
        if prediction == row["_outcome_family"]:
            correct += 1
    return correct, len(rows)


def _cohort_summary(
    all_rows: list[dict[str, str]],
    cohort: str,
    *,
    derivation_modality_model: tuple[dict[str, str], str | None] | None = None,
) -> dict[str, object]:
    cohort_rows = [
        row for row in all_rows if row.get("derivation_or_holdout", "") == cohort
    ]
    scored = _scored_rows(cohort_rows)
    correct = sum(
        row["_domain_prediction"] == row["_outcome_family"] for row in scored
    )
    result: dict[str, object] = {
        "total_rows": len(cohort_rows),
        "scored_n": len(scored),
        "unscored_n": len(cohort_rows) - len(scored),
        "domain_rule_correct": correct,
        "domain_rule_accuracy": (correct / len(scored)) if scored else None,
        "domain_counts": dict(
            sorted(Counter(row["pre_outcome_domain_code"] for row in scored).items())
        ),
        "outcome_family_counts": dict(
            sorted(Counter(row["_outcome_family"] for row in scored).items())
        ),
    }

    if scored and correct == len(scored):
        sizes = [
            sum(row["pre_outcome_domain_code"] == domain for row in scored)
            for domain in ("SEPARATED", "TRANSITIONAL", "OVERLAPPED")
        ]
        result["exact_perfect_alignment_probability"] = exact_alignment_probability(
            sizes
        )
    else:
        result["exact_perfect_alignment_probability"] = None

    if cohort == "derivation":
        loo_correct, loo_n = _modality_loo_accuracy(scored)
        result["modality_loo_correct"] = loo_correct
        result["modality_loo_n"] = loo_n
        result["modality_loo_accuracy"] = (loo_correct / loo_n) if loo_n else None
    elif derivation_modality_model is not None:
        mapping, fallback = derivation_modality_model
        modality_correct, modality_n = _apply_modality_model(
            scored, mapping, fallback
        )
        result["modality_from_derivation_correct"] = modality_correct
        result["modality_from_derivation_n"] = modality_n
        result["modality_from_derivation_accuracy"] = (
            modality_correct / modality_n if modality_n else None
        )

    return result


def summarize_state_recovery(rows: list[dict[str, str]]) -> dict[str, object]:
    derivation_scored = _scored_rows(
        [row for row in rows if row.get("derivation_or_holdout", "") == "derivation"]
    )
    modality_model = _modality_model(derivation_scored)

    pooled = _scored_rows(rows)
    pooled_correct = sum(
        row["_domain_prediction"] == row["_outcome_family"] for row in pooled
    )
    pooled_sizes = [
        sum(row["pre_outcome_domain_code"] == domain for row in pooled)
        for domain in ("SEPARATED", "TRANSITIONAL", "OVERLAPPED")
    ]

    return {
        "analysis_name": "effective_domain_pollinator_state_recovery",
        "outcome_family_definition": {
            "PRESERVED_OR_IMPROVED": "NO_INTERFERENCE_OBSERVED",
            "NO_DETECTED_CHANGE": "NO_INTERFERENCE_OBSERVED",
            "MIXED": "MIXED",
            "IMPAIRED": "IMPAIRED",
        },
        "domain_rule": {
            "SEPARATED": "NO_INTERFERENCE_OBSERVED",
            "TRANSITIONAL": "MIXED",
            "OVERLAPPED": "IMPAIRED",
        },
        "null_compatible_is_not_equivalence": True,
        "derivation": _cohort_summary(rows, "derivation"),
        "systematic_expansion": _cohort_summary(
            rows,
            "systematic_expansion",
            derivation_modality_model=modality_model,
        ),
        "holdout": _cohort_summary(
            rows,
            "holdout",
            derivation_modality_model=modality_model,
        ),
        "pooled_scored": {
            "scored_n": len(pooled),
            "domain_rule_correct": pooled_correct,
            "domain_rule_accuracy": (
                pooled_correct / len(pooled) if pooled else None
            ),
            "exact_perfect_alignment_probability": (
                exact_alignment_probability(pooled_sizes)
                if pooled and pooled_correct == len(pooled)
                else None
            ),
            "domain_counts": dict(
                sorted(
                    Counter(
                        row["pre_outcome_domain_code"] for row in pooled
                    ).items()
                )
            ),
            "outcome_family_counts": dict(
                sorted(
                    Counter(row["_outcome_family"] for row in pooled).items()
                )
            ),
        },
        "derivation_modality_rule": {
            "mapping": modality_model[0],
            "fallback": modality_model[1],
        },
        "claim_boundary": (
            "This is state-recovery across heterogeneous pollinator outcomes, not "
            "a pooled effect-size meta-analysis. NO_DETECTED_CHANGE means no "
            "interference was detected and is not evidence of equivalence. "
            "Historical derivation rows contributed to rule formation, so exact "
            "alignment probabilities are descriptive rather than confirmatory."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = load_csv_rows(args.input)
    result = summarize_state_recovery(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
