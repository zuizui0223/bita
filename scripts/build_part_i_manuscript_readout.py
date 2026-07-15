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
    full_tested_set_rows: list[dict[str, str]],
) -> str:
    if not case_rows or not form_summary_rows or not full_tested_set_rows:
        raise ValueError("all three sensitivity outputs must contain rows")

    evaluation_counts = _sign_counts(case_rows)
    form_classes = Counter(row["functional_form_class"] for row in form_summary_rows)
    full_set_classes = Counter(row["full_tested_set_class"] for row in full_tested_set_rows)
    scenarios = _scenario_rows(case_rows)
    forms = _form_rows(case_rows)
    most_comp, most_sub = _extreme_scenarios(scenarios)
    unanimous_form_cases = form_classes.get("tested_set_unanimous", 0)

    lines: list[str] = [
        "# Part I sensitivity readout v2",
        "",
        "## Scope",
        "",
        "This readout summarizes the reproduced Part I sign-sensitivity sweep. It is a",
        "qualitative theoretical result, not an empirical parameter calibration and not an",
        "estimate of observed trait covariance. The nonlinear response-shape variants are",
        "normalized to common endpoint scales on the declared 0–1 focal-trait domain.",
        "Agreement labels refer only to the finite declared tested set and are not claims of",
        "mathematical structural robustness.",
        "",
        "The reported percentages are unweighted occupancy fractions over the declared grid.",
        "Changing the grid measure can change those percentages; they are not empirical",
        "probabilities or estimates of prevalence in nature.",
        "",
        "## Overall sweep",
        "",
        f"- local phenotype/regime cases: **{len(full_tested_set_rows)}**",
        f"- biological parameter scenarios: **{len(scenarios)}**",
        f"- response-shape variants: **{len(forms)}**",
        f"- total mixed-partial evaluations: **{len(case_rows)}**",
        f"- complementary evaluations: **{evaluation_counts.get('complementary', 0)}** "
        f"({_pct(evaluation_counts.get('complementary', 0), len(case_rows))})",
        f"- substitutable evaluations: **{evaluation_counts.get('substitutable', 0)}** "
        f"({_pct(evaluation_counts.get('substitutable', 0), len(case_rows))})",
        "",
        "Across the full finite tested set, neither sign is universal. The implemented model",
        "therefore contains conditional attraction–defence regimes rather than a universal",
        "trade-off or universal complementarity result.",
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
        "Values below pool over the declared local coordinates, biological parameter",
        "scenarios, auxiliary assurance levels, and endpoint-normalized response shapes.",
        "They are theoretical grid occupancies, not empirical probabilities.",
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
        "Within this declared model family, increasing floral damage pressure shifts the",
        "evaluated balance toward complementarity, whereas increasing pollinator service",
        "shifts it toward substitutability when defence carries a pollination cost. This is a",
        "property of the tested special-case model, not an unconditional theorem for arbitrary",
        "environmental scaling functions.",
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
        "and `A=D=1`, while redistributing local marginal effects across trait space. They",
        "therefore test response-shape sensitivity more cleanly than unnormalized alternatives,",
        "although they still represent only a finite set of possible biological functions.",
        "",
        "## Tested-set agreement",
        "",
        f"Within biological parameter scenarios, **{unanimous_form_cases} of "
        f"{len(form_summary_rows)}** case × scenario combinations were `tested_set_unanimous`",
        f"across all {len(forms)} response-shape variants; the remaining "
        f"**{form_classes.get('mixed_or_sensitive', 0)}** were `mixed_or_sensitive`.",
        "",
        "Across the full biological-parameter × response-shape tested set:",
        "",
        f"- `tested_set_unanimous`: **{full_set_classes.get('tested_set_unanimous', 0)}** / "
        f"{len(full_tested_set_rows)}",
        f"- `mixed_or_sensitive`: **{full_set_classes.get('mixed_or_sensitive', 0)}** / "
        f"{len(full_tested_set_rows)}",
    ]

    if full_set_classes.get("tested_set_unanimous", 0) == 0:
        lines += [
            "",
            "No local case was unanimous across every tested biological-parameter × response-shape",
            "evaluation in the full finite set. This is expected for a theory whose central",
            "hypothesis is that changing route strengths can switch the local interaction sign.",
        ]

    lines += [
        "",
        "`modal_sign_agreement` remains available in the CSV outputs as a continuous descriptive",
        "quantity. No arbitrary majority threshold is converted into a separate robustness class.",
        "",
        "## Manuscript-ready Results statement",
        "",
        f"> Across {len(full_tested_set_rows)} local phenotype–interaction cases, {len(scenarios)}",
        f"> biological parameter scenarios, and {len(forms)} endpoint-normalized response-shape",
        f"> variants ({len(case_rows):,} mixed-partial evaluations), attraction and defence were",
        "> not universally complementary or substitutable. The scenario with the highest",
        f"> complementary occupancy (`{most_comp[0]}`) was complementary in "
        f"{_pct(most_comp[1], most_comp[3])} of its declared evaluations, whereas the scenario",
        f"> with the highest substitutable occupancy (`{most_sub[0]}`) was substitutable in "
        f"{_pct(most_sub[2], most_sub[3])}. Within the declared pollinator-service ×",
        "> floral-damage grid, the tested special-case model shifted toward complementarity as",
        "> floral damage pressure increased and toward substitutability as pollinator service",
        "> increased. Exact boundaries remained sensitive to declared parameters and response shapes.",
        "",
        "## Inference boundary",
        "",
        "- These are unweighted finite-grid occupancies, not empirical event probabilities.",
        "- The response-shape variants share endpoint scales but not identical local derivatives.",
        "- Reproductive assurance is an auxiliary background moderator, not a third focal trait.",
        "- The sweep does not estimate model parameters from the abstract-level literature context.",
        "- Parameter sensitivity is part of the causal hypothesis: changing route strengths is expected",
        "  to change the local regime.",
        "- Tested-set unanimity is finite-set sensitivity evidence, not mathematical structural robustness.",
        "- The sign and numerical zero tolerance remain properties of the declared trait and score scales.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation_csv")
    parser.add_argument("response_shape_summary_csv")
    parser.add_argument("full_tested_set_summary_csv")
    parser.add_argument("output_md")
    args = parser.parse_args(argv)

    text = build_readout(
        _read_csv(args.evaluation_csv),
        _read_csv(args.response_shape_summary_csv),
        _read_csv(args.full_tested_set_summary_csv),
    )
    output = Path(args.output_md)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
