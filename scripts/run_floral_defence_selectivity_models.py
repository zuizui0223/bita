"""Low-dimensional Stage-2 model gate for BITA floral-defence selectivity."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows

STRICT_STATES = {"PRESERVED_OR_IMPROVED", "IMPAIRED"}
CORE_DOMAINS = {"SEPARATED", "OVERLAPPED"}


def _hypergeom_prob(a: int, row1: int, row2: int, col1: int, total: int) -> float:
    col2 = total - col1
    b = row1 - a
    c = col1 - a
    d = row2 - c
    if min(a, b, c, d) < 0:
        return 0.0
    return (
        math.comb(col1, a) * math.comb(col2, b) / math.comb(total, row1)
    )


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Fisher exact two-sided p using the probability-ordering definition."""
    row1 = a + b
    row2 = c + d
    col1 = a + c
    total = row1 + row2
    if total == 0:
        return math.nan
    lower = max(0, row1 - (total - col1))
    upper = min(row1, col1)
    observed = _hypergeom_prob(a, row1, row2, col1, total)
    p = 0.0
    for candidate in range(lower, upper + 1):
        prob = _hypergeom_prob(candidate, row1, row2, col1, total)
        if prob <= observed + 1e-15:
            p += prob
    return min(1.0, p)


def _empty_table(value_label: str) -> dict[str, dict[str, int]]:
    return {
        "SEPARATED": {value_label: 0, "impaired": 0},
        "OVERLAPPED": {value_label: 0, "impaired": 0},
    }


def _domain_modality_confounding(rows: list[dict[str, str]]) -> tuple[str, bool]:
    if not rows:
        return "NO_STRICT_ROWS", False
    modalities = {str(row.get("defence_modality", "")).strip() for row in rows}
    domains = {str(row.get("pre_outcome_domain_code", "")).strip() for row in rows}
    if len(modalities) < 2:
        return "NO_MODALITY_VARIATION", False
    if len(domains) < 2:
        return "NO_DOMAIN_VARIATION", False

    domain_to_modality: dict[str, set[str]] = {}
    modality_to_domain: dict[str, set[str]] = {}
    for row in rows:
        domain = str(row.get("pre_outcome_domain_code", "")).strip()
        modality = str(row.get("defence_modality", "")).strip()
        domain_to_modality.setdefault(domain, set()).add(modality)
        modality_to_domain.setdefault(modality, set()).add(domain)

    perfect = (
        all(len(values) == 1 for values in domain_to_modality.values())
        and all(len(values) == 1 for values in modality_to_domain.values())
    )
    if perfect:
        return "PERFECT_IN_CURRENT_STRICT_SET", False
    return "NOT_PERFECT", True


def summarize_stage2_model_gate(rows: list[dict[str, str]]) -> dict[str, object]:
    eligible = [
        row
        for row in rows
        if str(row.get("defence_efficacy_state", "")).strip() == "EFFECTIVE"
        and str(row.get("pre_outcome_domain_code", "")).strip() in CORE_DOMAINS
    ]

    strict_rows = [
        row
        for row in eligible
        if str(row.get("pollinator_cost_state_derived", "")).strip() in STRICT_STATES
    ]
    strict_table = _empty_table("compatible")
    for row in strict_rows:
        domain = str(row["pre_outcome_domain_code"]).strip()
        state = str(row["pollinator_cost_state_derived"]).strip()
        if state == "PRESERVED_OR_IMPROVED":
            strict_table[domain]["compatible"] += 1
        elif state == "IMPAIRED":
            strict_table[domain]["impaired"] += 1

    a = strict_table["SEPARATED"]["compatible"]
    b = strict_table["SEPARATED"]["impaired"]
    c = strict_table["OVERLAPPED"]["compatible"]
    d = strict_table["OVERLAPPED"]["impaired"]
    strict_p = fisher_two_sided(a, b, c, d) if strict_rows else math.nan

    sensitivity_rows = [
        row
        for row in eligible
        if str(row.get("pollinator_cost_state_derived", "")).strip()
        in {"PRESERVED_OR_IMPROVED", "NO_DETECTED_CHANGE", "IMPAIRED"}
    ]
    sensitivity_table = _empty_table("compatible_or_null")
    for row in sensitivity_rows:
        domain = str(row["pre_outcome_domain_code"]).strip()
        state = str(row["pollinator_cost_state_derived"]).strip()
        if state in {"PRESERVED_OR_IMPROVED", "NO_DETECTED_CHANGE"}:
            sensitivity_table[domain]["compatible_or_null"] += 1
        elif state == "IMPAIRED":
            sensitivity_table[domain]["impaired"] += 1

    sa = sensitivity_table["SEPARATED"]["compatible_or_null"]
    sb = sensitivity_table["SEPARATED"]["impaired"]
    sc = sensitivity_table["OVERLAPPED"]["compatible_or_null"]
    sd = sensitivity_table["OVERLAPPED"]["impaired"]
    sensitivity_p = (
        fisher_two_sided(sa, sb, sc, sd) if sensitivity_rows else math.nan
    )

    confounding, can_compare = _domain_modality_confounding(strict_rows)

    # The design spec predeclares <15 independent strict systems as too sparse
    # for a high-dimensional moderator meta-regression.
    model_decision = (
        "FORMAL_LOW_DIMENSIONAL_MODEL_ALLOWED"
        if len(strict_rows) >= 15 and can_compare
        else "DESCRIPTIVE_EXACT_ONLY"
    )

    return {
        "strict_stage2_n": len(strict_rows),
        "strict_table": strict_table,
        "strict_fisher_two_sided_p": None if math.isnan(strict_p) else strict_p,
        "compatibility_sensitivity_n": len(sensitivity_rows),
        "compatibility_sensitivity_table": sensitivity_table,
        "compatibility_sensitivity_fisher_two_sided_p": (
            None if math.isnan(sensitivity_p) else sensitivity_p
        ),
        "null_compatible_is_not_equivalence": True,
        "strict_domain_modality_confounding": confounding,
        "can_compare_domain_vs_modality": can_compare,
        "model_decision": model_decision,
        "claim_boundary": (
            "Exact tables are descriptive evidence. Null-compatible rows are used only "
            "in sensitivity analysis and are not promoted to equivalence-supported preservation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = load_csv_rows(args.input)
    result = summarize_stage2_model_gate(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
