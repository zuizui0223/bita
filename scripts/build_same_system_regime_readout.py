"""Validate and summarize the predeclared same-system regime ledger.

Counts are evidence-coverage descriptions of an information-rich source set, not
prevalence estimates. No route coefficients are combined.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

LEDGER = Path("empirical/mechanism_pattern_synthesis/SAME_SYSTEM_REGIME_LEDGER_V1.csv")
EXPECTED_CLUSTERS = {
    "Adler_Irwin_2005_Gelsemium",
    "Barlow_et_al_2017_Aconitum",
    "Galen_2011_Polemonium",
    "Gorden_Adler_2018_Impatiens_capensis",
    "Irwin_Adler_Brody_2004_Ipomopsis",
    "Jones_Agrawal_2016_Asclepias",
    "Kessler_Baldwin_2007_Nicotiana",
    "Kessler_et_al_2015_Nicotiana",
    "Theis_Adler_2012_Cucurbita",
    "Theis_et_al_2014_Cucurbitaceae",
}
A_ALLOWED = {
    "shared_tracking", "mutualist_biased", "antagonist_biased",
    "opposed_or_defensive_signal", "context_switching", "unresolved", "not_applicable",
}
D_ALLOWED = {
    "guarded", "guarded_window_then_interference", "pollinator_interference",
    "response_construct_mixed", "context_switching", "unresolved", "not_applicable",
}
CONF_ALLOWED = {"high", "moderate", "low"}


def _read() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _validate(rows: list[dict[str, str]]) -> None:
    clusters = [row["cluster_id"] for row in rows]
    if len(clusters) != len(set(clusters)):
        raise ValueError("duplicate cluster_id in same-system regime ledger")
    if set(clusters) != EXPECTED_CLUSTERS:
        raise ValueError(json.dumps({
            "missing": sorted(EXPECTED_CLUSTERS - set(clusters)),
            "unexpected": sorted(set(clusters) - EXPECTED_CLUSTERS),
        }))
    for row in rows:
        if row["a_regime"] not in A_ALLOWED:
            raise ValueError(f"invalid A regime: {row['a_regime']}")
        if row["d_regime"] not in D_ALLOWED:
            raise ValueError(f"invalid D regime: {row['d_regime']}")
        if row["confidence"] not in CONF_ALLOWED:
            raise ValueError(f"invalid confidence: {row['confidence']}")
        if row["a_regime"] == "not_applicable" and row["d_regime"] == "not_applicable":
            raise ValueError(f"cluster has no same-system regime: {row['cluster_id']}")


def _counter(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows if row[field] != "not_applicable").items()))


def _render(rows: list[dict[str, str]], report: dict[str, object]) -> str:
    lines = [
        "# Same-system mechanism regime readout v1",
        "",
        "## Scope",
        "",
        "Ten source-adjudicated biological study clusters contain at least two theory-relevant marginal routes in the same system. They are classified qualitatively under the preregistered regime protocol. **These counts describe recurrence in the current information-rich evidence set; they are not prevalence estimates for nature.**",
        "",
        "No coefficient from a pollinator endpoint is subtracted from an antagonist endpoint. No same-system regime is called complementarity or substitutability without a direct `A x D` reproductive interaction.",
        "",
        "## D-side regimes",
        "",
        "Among the seven systems with both `D_to_antagonism` and `D_to_pollination` information:",
        "",
    ]
    for label, count in report["d_regime_counts"].items():
        lines.append(f"- `{label}`: **{count}** independent system{'s' if count != 1 else ''}")
    lines += [
        "",
        "The key result is not that one D regime dominates. The source-adjudicated set already contains **multiple qualitatively distinct D architectures**:",
        "",
        "- `Ipomopsis`: a guarded state — robbery resistance without detected hummingbird deterrence;",
        "- `Polemonium` and `Aconitum`: ordered guarded windows — antagonist relief appears before strong pollinator interference;",
        "- `Gelsemium` and `Asclepias`: context switching across reward, dose, exposure duration or response stage;",
        "- `Nicotiana` 2007: response-construct mixing — fewer/shorter nectar-use interactions can coexist with more visits;",
        "- `Impatiens`: unresolved despite all four marginal routes being estimable.",
        "",
        "This directly rejects a synthesis strategy that would treat `D_to_pollination` as one context-free biological sign.",
        "",
        "## A-side regimes",
        "",
        "Among the four systems with both `A_to_pollination` and `A_to_antagonism` information:",
        "",
    ]
    for label, count in report["a_regime_counts"].items():
        lines.append(f"- `{label}`: **{count}** independent system{'s' if count != 1 else ''}")
    lines += [
        "",
        "These systems span the major attraction-side possibilities required by the theory:",
        "",
        "- `Theis et al. 2014 Cucurbita`: **shared tracking** — the same floral sesquiterpenoid axis positively predicts specialist pollinator and floral-herbivore use;",
        "- `Theis & Adler 2012 Cucurbita`: **antagonist-biased** — fragrance enhancement attracts florivores without a detected pollinator-attraction increase;",
        "- `Kessler et al. 2015 Nicotiana`: **context switching** — scent supports both pollination and oviposition for `Manduca`, whereas another hawkmoth pollinator shows little scent dependence;",
        "- `Impatiens`: unresolved marginal A routes.",
        "",
        "Thus attraction tracking itself is not a fixed pollinator-only process. Which consumer guild follows a floral signal is a repeated source of conditionality.",
        "",
        "## Study-level ledger",
        "",
        "| Study cluster | A regime | D regime | Context axis | Confidence | Direct A×D state |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['cluster_id']}` | `{row['a_regime']}` | `{row['d_regime']}` | "
            f"`{row['context_axis']}` | {row['confidence']} | `{row['direct_axd_state']}` |"
        )
    lines += [
        "",
        "## Theory-facing interpretation",
        "",
        "The same-system evidence supports three claims that are stronger than a universal-mean meta-analysis:",
        "",
        "1. **Antagonist relief can precede pollinator interference.** `Polemonium` and `Aconitum` independently show ordered expression/dose windows compatible with this mechanism ordering.",
        "2. **Pollinator cost is context dependent rather than obligatory.** `Ipomopsis` supplies a guarded counterexample; `Gelsemium`, `Asclepias` and `Nicotiana` show reward-, duration-, consumer- or response-dependent changes.",
        "3. **Attraction can expose plants to antagonists as well as mutualists.** Shared and antagonist-biased tracking both occur in independent `Cucurbita` systems, while `Nicotiana` shows consumer-specific shared tracking.",
        "",
        "These observations are compatible with the theoretical premise that the realized attraction–defence relationship depends on the relative strengths of antagonist relief and pollinator interference. They do **not** estimate `rho`, `iota`, `kappa`, or `W_AD` from incomparable endpoints.",
        "",
        "## Gate E decision",
        "",
        "**Gate E is now empirically satisfied for the current source-adjudicated evidence architecture.** Same-system linkage is explicit, dependence is retained at the study-cluster level, and guarded/interference/context-switching structures have been formally classified.",
        "",
        "This does not unfreeze the manuscript by itself. Gates A (direct `A x D` search saturation), C (a second compatible quantitative multi-study module), F (joint-cost search saturation), and G (synthesis-level robustness/bias) remain open.",
        "",
        "## Guardrail",
        "",
        "Regime counts are recurrence evidence within an information-rich screened set, not estimates of how common each regime is in nature. Same-system regimes remain distinct from the strict direct `A x D` layer, where `Impatiens capensis` is still the only accepted cluster and its interaction sign is unresolved.",
        "",
    ]
    return "\n".join(lines)


def run(output_json: str | Path, output_md: str | Path) -> dict[str, object]:
    rows = _read()
    _validate(rows)
    report = {
        "cluster_count": len(rows),
        "a_applicable_cluster_count": sum(row["a_regime"] != "not_applicable" for row in rows),
        "d_applicable_cluster_count": sum(row["d_regime"] != "not_applicable" for row in rows),
        "a_regime_counts": _counter(rows, "a_regime"),
        "d_regime_counts": _counter(rows, "d_regime"),
        "confidence_counts": dict(sorted(Counter(row["confidence"] for row in rows).items())),
        "direct_axd_cluster_count": sum(row["direct_axd_state"] != "not_tested" and row["direct_axd_state"] != "not_eligible_distinct_D" for row in rows),
        "warning": "Regime counts describe the source-adjudicated information-rich study set and must not be interpreted as prevalence in nature.",
    }
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(output_json).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    Path(output_md).write_text(_render(rows, report), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_json")
    parser.add_argument("output_md")
    args = parser.parse_args()
    report = run(args.output_json, args.output_md)
    print(json.dumps(report, indent=2, sort_keys=True))
