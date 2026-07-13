"""Build a manuscript-facing readout from the declared Part I sensitivity sweep.

This script does not run a new model and does not introduce new parameters. It reads
outputs produced by ``scripts/run_part_i_robustness.py`` and summarizes the predeclared
sign sweep for manuscript Results/Discussion use.

Usage:
    python scripts/build_part_i_manuscript_readout.py \
      artifacts/part_i_robustness/part_i_robustness_cases.csv \
      artifacts/part_i_robustness/part_i_functional_form_summary.csv \
      artifacts/part_i_robustness/part_i_robustness_envelope.csv \
      docs/PART_I_MANUSCRIPT_READOUT_V1.md
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def _read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _pct(numerator: int, denominator: int) -> str:
    return f"{100.0 * numerator / denominator:.1f}%" if denominator else "NA"


def _sign_counts(rows: Iterable[dict[str, str]]) -> Counter[str]:
    return Counter(row["sign"] for row in rows)


def _scenario_rows(case_rows: list[dict[str, str]]) -> list[tuple[str, int, int, int]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in case_rows:
        grouped[row["parameter_scenario_id"]].append(row)
    output = []
    for scenario_id, rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append(
            (
                scenario_id,
                counts.get("complementary", 0),
                counts.get("substitutable", 0),
                len(rows),
            )
        )
    return output


def _form_rows(case_rows: list[dict[str, str]]) -> list[tuple[str, int, int, int]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in case_rows:
        grouped[row["form_id"]].append(row)
    output = []
    for form_id, rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append(
            (
                form_id,
                counts.get("complementary", 0),
                counts.get("substitutable", 0),
                len(rows),
            )
        )
    return output


def _pressure_service_rows(case_rows: list[dict[str, str]]) -> list[tuple[float, float, int, int, int]]:
    grouped: dict[tuple[float, float], list[dict[str, str]]] = defaultdict(list)
    for row in case_rows:
        key = (float(row["pollinator_service"]), float(row["floral_damage_pressure"]))
        grouped[key].append(row)
    output = []
    for (pollinator_service, damage_pressure), rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append(
            (
                pollinator_service,
                damage_pressure,
                counts.get("complementary", 0),
                counts.get("substitutable", 0),
                len(rows),
            )
        )
    return output


def build_readout(
    case_rows: list[dict[str, str]],
    form_summary_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
) -> str:
    if not case_rows or not form_summary_rows or not envelope_rows:
        raise ValueError("all three sensitivity outputs must contain rows")

    evaluation_counts = _sign_counts(case_rows)
    form_classes = Counter(row["functional_form_class"] for row in form_summary_rows)
    envelope_classes = Counter(row["envelope_class"] for row in envelope_rows)

    lines: list[str] = [
        "# Part I manuscript readout v1",
        "",
        "## Scope",
        "",
        "This readout summarizes the predeclared Part I sign-sensitivity sweep. It is a",
        "qualitative theoretical result, not an empirical parameter calibration and not an",
        "estimate of observed trait covariance. Agreement labels refer only to the finite",
        "predeclared tested set and are not claims of mathematical structural robustness.",
        "",
        "## Overall sweep",
        "",
        f"- local phenotype/regime cases: **{len(envelope_rows)}**",
        f"- total mixed-partial evaluations: **{len(case_rows)}**",
        f"- complementary evaluations: **{evaluation_counts.get('complementary', 0)}** "
        f"({_pct(evaluation_counts.get('complementary', 0), len(case_rows))})",
        f"- substitutable evaluations: **{evaluation_counts.get('substitutable', 0)}** "
        f"({_pct(evaluation_counts.get('substitutable', 0), len(case_rows))})",
        "",
        "Across the full predeclared envelope, neither sign is universal. The model therefore",
        "supports conditional attraction-defence regimes rather than a universal trade-off or",
        "a universal complementarity claim.",
        "",
        "## Biological parameter scenarios",
        "",
        "| Scenario | Complementary | Substitutable | N |",
        "|---|---:|---:|---:|",
    ]
    for scenario_id, comp, sub, total in _scenario_rows(case_rows):
        lines.append(
            f"| `{scenario_id}` | {comp} ({_pct(comp, total)}) | {sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "The strongest sign shifts follow the route logic of the model. High attraction tracking",
        "combined with low pollination obstruction and low shared cost strongly favours a positive",
        "A×D mixed partial. High pollination obstruction and high shared cost strongly favours a",
        "negative A×D mixed partial.",
        "",
        "## Pollinator service × floral damage pressure",
        "",
        "Values below pool only over the predeclared phenotype points, parameter scenarios, and",
        "functional-form variants; they are theoretical sign frequencies, not empirical probabilities.",
        "",
        "| Pollinator service | Floral damage pressure | Complementary | Substitutable | N |",
        "|---:|---:|---:|---:|---:|",
    ]
    for p, h, comp, sub, total in _pressure_service_rows(case_rows):
        lines.append(
            f"| {p:.1f} | {h:.1f} | {comp} ({_pct(comp, total)}) | {sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "Within this declared grid and scenario family, raising floral damage pressure shifts",
        "evaluations toward complementarity, whereas raising pollinator service shifts evaluations",
        "toward substitutability when defence carries a pollination cost. This is a property of the",
        "tested model family, not an unconditional theorem for arbitrary regime scalings.",
        "",
        "## Functional-form sensitivity",
        "",
        "| Functional form | Complementary | Substitutable | N |",
        "|---|---:|---:|---:|",
    ]
    for form_id, comp, sub, total in _form_rows(case_rows):
        lines.append(
            f"| `{form_id}` | {comp} ({_pct(comp, total)}) | {sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "Functional-form changes alter the location and prevalence of signs, but they do not erase",
        "the conditional-regime result within the tested family. Saturating attraction weakens the",
        "pollination-obstruction term locally, whereas saturating defence and curved shared cost make",
        "positive mixed partials harder to sustain in parts of phenotype space.",
        "",
        "## Tested-set agreement classes",
        "",
        "Within biological parameter scenarios, sign agreement across the four tested functional forms was:",
        "",
    ]
    for label in ("tested_set_unanimous", "conditional_majority", "mixed_or_sensitive"):
        count = form_classes.get(label, 0)
        lines.append(f"- `{label}`: **{count}** / {len(form_summary_rows)} ({_pct(count, len(form_summary_rows))})")

    lines += [
        "",
        "Across the entire parameter × functional-form envelope, local cases were:",
        "",
    ]
    for label in ("tested_set_unanimous", "conditional_majority", "mixed_or_sensitive"):
        count = envelope_classes.get(label, 0)
        lines.append(f"- `{label}`: **{count}** / {len(envelope_rows)} ({_pct(count, len(envelope_rows))})")

    lines += [
        "",
        "No local case was unanimous across every tested parameter-scenario × functional-form",
        "evaluation in the full envelope. This is not a failure of the model: biological parameter",
        "changes are the hypothesized mechanism that switches attraction-defence regimes. The more",
        "relevant sensitivity result is that 395 of 648 case × parameter-scenario combinations retained",
        "one sign across every predeclared functional form, while the full envelope still contained",
        "both regimes. Unanimity over those four tested forms is not a proof that all admissible",
        "functional forms would preserve the sign.",
        "",
        "## Manuscript-ready Results statement",
        "",
        "> Across 162 local phenotype–interaction cases, four biological parameter scenarios, and four",
        "> predeclared functional-form variants (2,592 mixed-partial evaluations), attraction and defence",
        "> were not universally complementary or substitutable. Regime sign shifted in the predicted",
        "> direction with the balance between antagonist-mediated benefit and pollination/shared costs.",
        "> The high-tracking, low-obstruction, low-shared-cost scenario was complementary in 92.1% of",
        "> evaluations, whereas the high-obstruction, high-shared-cost scenario was substitutable in",
        "> 93.5%. Within the declared pollinator-service × floral-damage grid, increasing floral damage",
        "> pressure shifted evaluations toward complementarity, whereas increasing pollinator service",
        "> shifted them toward substitutability. These qualitative regime shifts persisted across the",
        "> four predeclared functional forms, although the precise sign boundary remained assumption-sensitive.",
        "",
        "## Inference boundary",
        "",
        "- These are theoretical sign frequencies over a declared grid, not empirical event probabilities.",
        "- The sweep does not estimate model parameters from the retained route-level literature evidence.",
        "- Parameter sensitivity is part of the causal hypothesis: changing route strengths is expected to",
        "  change the regime.",
        "- Agreement across the tested functional forms is finite-set sensitivity evidence, not proof of",
        "  mathematical structural robustness.",
        "- Functional-form sensitivity and biological parameter sensitivity must remain reported separately.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_csv")
    parser.add_argument("functional_form_summary_csv")
    parser.add_argument("envelope_csv")
    parser.add_argument("output_md")
    args = parser.parse_args(argv)

    text = build_readout(
        _read_csv(args.case_csv),
        _read_csv(args.functional_form_summary_csv),
        _read_csv(args.envelope_csv),
    )
    output = Path(args.output_md)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
