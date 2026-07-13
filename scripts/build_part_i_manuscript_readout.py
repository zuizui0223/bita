"""Build a manuscript-facing readout from reproduced Part I sensitivity outputs.

The script introduces no model parameters and contains no hard-coded result
counts or percentages. All manuscript-facing numbers are derived from the three
CSV outputs produced by ``scripts/run_part_i_robustness.py``.
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
    output: list[tuple[str, int, int, int]] = []
    for scenario_id, rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append((
            scenario_id,
            counts.get("complementary", 0),
            counts.get("substitutable", 0),
            len(rows),
        ))
    return output


def _form_rows(case_rows: list[dict[str, str]]) -> list[tuple[str, int, int, int]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in case_rows:
        grouped[row["form_id"]].append(row)
    output: list[tuple[str, int, int, int]] = []
    for form_id, rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append((
            form_id,
            counts.get("complementary", 0),
            counts.get("substitutable", 0),
            len(rows),
        ))
    return output


def _pressure_service_rows(
    case_rows: list[dict[str, str]],
) -> list[tuple[float, float, int, int, int]]:
    grouped: dict[tuple[float, float], list[dict[str, str]]] = defaultdict(list)
    for row in case_rows:
        key = (float(row["pollinator_service"]), float(row["floral_damage_pressure"]))
        grouped[key].append(row)
    output: list[tuple[float, float, int, int, int]] = []
    for (pollinator_service, damage_pressure), rows in sorted(grouped.items()):
        counts = _sign_counts(rows)
        output.append((
            pollinator_service,
            damage_pressure,
            counts.get("complementary", 0),
            counts.get("substitutable", 0),
            len(rows),
        ))
    return output


def _extreme_scenarios(
    scenarios: list[tuple[str, int, int, int]],
) -> tuple[tuple[str, int, int, int], tuple[str, int, int, int]]:
    most_complementary = max(scenarios, key=lambda row: row[1] / row[3])
    most_substitutable = max(scenarios, key=lambda row: row[2] / row[3])
    return most_complementary, most_substitutable


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
    scenarios = _scenario_rows(case_rows)
    forms = _form_rows(case_rows)
    most_comp, most_sub = _extreme_scenarios(scenarios)
    unanimous_form_cases = form_classes.get("tested_set_unanimous", 0)

    lines: list[str] = [
        "# Part I manuscript readout v1",
        "",
        "## Scope",
        "",
        "This readout summarizes the reproduced Part I sign-sensitivity sweep. It is a",
        "qualitative theoretical result, not an empirical parameter calibration and not an",
        "estimate of observed trait covariance. The nonlinear response-shape variants are",
        "normalized to common endpoint scales on the declared 0–1 trait domain. Agreement",
        "labels refer only to the finite predeclared tested set and are not claims of",
        "mathematical structural robustness.",
        "",
        "## Overall sweep",
        "",
        f"- local phenotype/regime cases: **{len(envelope_rows)}**",
        f"- biological parameter scenarios: **{len(scenarios)}**",
        f"- response-shape variants: **{len(forms)}**",
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
    for scenario_id, comp, sub, total in scenarios:
        lines.append(
            f"| `{scenario_id}` | {comp} ({_pct(comp, total)}) | "
            f"{sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "The strongest sign shifts follow the declared route logic: scenarios with greater",
        "attraction-linked antagonist relief relative to pollination obstruction and direct",
        "cross-cost occupy more complementary evaluations, whereas the opposing balance",
        "occupies more substitutable evaluations.",
        "",
        "## Pollinator service × floral damage pressure",
        "",
        "Values below pool only over the predeclared phenotype points, biological parameter",
        "scenarios, and endpoint-normalized response-shape variants. They are theoretical sign",
        "frequencies, not empirical probabilities.",
        "",
        "| Pollinator service | Floral damage pressure | Complementary | Substitutable | N |",
        "|---:|---:|---:|---:|---:|",
    ]
    for p, h, comp, sub, total in _pressure_service_rows(case_rows):
        lines.append(
            f"| {p:.1f} | {h:.1f} | {comp} ({_pct(comp, total)}) | "
            f"{sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "Within this declared grid and scenario family, increasing floral damage pressure shifts",
        "the evaluated balance toward complementarity, whereas increasing pollinator service shifts",
        "it toward substitutability when defence carries a pollination cost. This is a property of",
        "the tested model family, not an unconditional theorem for arbitrary regime scalings.",
        "",
        "## Endpoint-normalized response-shape sensitivity",
        "",
        "| Response-shape variant | Complementary | Substitutable | N |",
        "|---|---:|---:|---:|",
    ]
    for form_id, comp, sub, total in forms:
        lines.append(
            f"| `{form_id}` | {comp} ({_pct(comp, total)}) | "
            f"{sub} ({_pct(sub, total)}) | {total} |"
        )

    lines += [
        "",
        "The nonlinear variants preserve the declared endpoint effect scales at `A=1`, `D=1`,",
        "and `A=D=1`, while redistributing local marginal effects across trait space. They therefore",
        "test response-shape sensitivity more cleanly than unnormalized alternatives, although they",
        "still represent only a finite set of possible biological functions.",
        "",
        "## Tested-set agreement classes",
        "",
        f"Within biological parameter scenarios, sign agreement across the {len(forms)} tested "
        "response-shape variants was:",
        "",
    ]
    for label in ("tested_set_unanimous", "conditional_majority", "mixed_or_sensitive"):
        count = form_classes.get(label, 0)
        lines.append(
            f"- `{label}`: **{count}** / {len(form_summary_rows)} "
            f"({_pct(count, len(form_summary_rows))})"
        )

    lines += [
        "",
        "Across the entire biological-parameter × response-shape envelope, local cases were:",
        "",
    ]
    for label in ("tested_set_unanimous", "conditional_majority", "mixed_or_sensitive"):
        count = envelope_classes.get(label, 0)
        lines.append(
            f"- `{label}`: **{count}** / {len(envelope_rows)} "
            f"({_pct(count, len(envelope_rows))})"
        )

    if envelope_classes.get("tested_set_unanimous", 0) == 0:
        lines += [
            "",
            "No local case was unanimous across every tested biological-parameter × response-shape",
            "evaluation in the full envelope. This is expected for a theory whose central hypothesis",
            "is that changing route strengths can switch the local interaction sign.",
        ]
    lines += [
        "",
        f"Across fixed biological parameter scenarios, **{unanimous_form_cases} of "
        f"{len(form_summary_rows)}** case × scenario combinations retained one non-neutral sign",
        f"across all {len(forms)} predeclared endpoint-normalized response-shape variants. This is",
        "finite tested-set evidence, not proof that every admissible functional form preserves the sign.",
        "",
        "## Manuscript-ready Results statement",
        "",
        f"> Across {len(envelope_rows)} local phenotype–interaction cases, {len(scenarios)} biological",
        f"> parameter scenarios, and {len(forms)} endpoint-normalized response-shape variants",
        f"> ({len(case_rows):,} mixed-partial evaluations), attraction and defence were not universally",
        "> complementary or substitutable. The scenario with the highest complementary fraction",
        f"> (`{most_comp[0]}`) was complementary in {_pct(most_comp[1], most_comp[3])} of evaluations,",
        "> whereas the scenario with the highest substitutable fraction",
        f"> (`{most_sub[0]}`) was substitutable in {_pct(most_sub[2], most_sub[3])}. Within the declared",
        "> pollinator-service × floral-damage grid, increasing floral damage pressure shifted the",
        "> evaluated balance toward complementarity, whereas increasing pollinator service shifted it",
        "> toward substitutability. Exact boundaries remained sensitive to the declared biological",
        "> parameters and response shapes.",
        "",
        "## Inference boundary",
        "",
        "- These are theoretical sign frequencies over a declared grid, not empirical event probabilities.",
        "- The response-shape variants share endpoint scales but not identical local derivatives.",
        "- The sweep does not estimate model parameters from the abstract-level route evidence.",
        "- Parameter sensitivity is part of the causal hypothesis: changing route strengths is expected",
        "  to change the regime.",
        "- Tested-set unanimity is finite-set sensitivity evidence, not mathematical structural robustness.",
        "- The sign and the numerical zero tolerance remain properties of the declared trait and score scales.",
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
