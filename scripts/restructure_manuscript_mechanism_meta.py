"""Enforce the canonical Mechanism -> Pattern manuscript framing safely.

The manuscript has already been structurally split into Part I (mechanistic
mathematical theory) and Part II (meta-analysis/cross-study pattern synthesis).
This script is intentionally idempotent: it refreshes only the newly inserted
framing blocks with raw LaTeX-safe strings and verifies the two-part contract.
It does not modify canonical equations, numerical results, or empirical data.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"

NEW_TITLE = "# When are floral attraction and defence complementary? Mechanistic theory and meta-analytic patterns across mutualists and antagonists"

NEW_ABSTRACT = r"""## Abstract

Flowers must attract mutualists while remaining exposed to florivores, nectar robbers, pathogens, and other antagonists. We ask two linked questions: **what mechanism determines whether floral attraction and defence are locally complementary or substitutable, and what cross-system patterns recur in the empirical literature?** In Part I, we derive a local mechanistic theory for one declared attraction trait, one flower-specific antagonist-reducing trait, and one declared outcome scale. After an explicit orientation gate, the mixed partial is a balance among antagonist relief, pollinator interference, and direct joint-cost curvature, \(W_{AD}=\rho-\iota-\kappa\). The same total curvature can arise from different channel allocations, so total fitness alone does not identify mechanism. Endpoint-normalized sensitivity analysis produces both complementary and substitutable regimes across 2,592 declared evaluations. In Part II, we use the theory as a prediction and classification framework for a registered cross-study pattern synthesis, and use quantitative meta-analysis only where outcomes can be placed on defensible common scales. The evidence map contains 38 route-level records across 14 independent biological study clusters, including ten same-system multi-route clusters and eleven independent context/sign-switch clusters. A random-effects reanalysis of floral-larceny data shows recurrent reductions in female fitness (LRR \(-0.210\), 48 clusters), nectar standing crop (\(-0.483\), 28), and legitimate visitation (\(-0.291\), 22), while retaining extreme heterogeneity. A second 32-study-component synthesis of floral volatiles shows shared pollinator/florivore responsiveness but strong compositional and context dependence. Direct \(A\times D\) evidence remains restricted to one sign-unresolved cluster and direct joint-cost evidence to zero strict estimates. Thus the general cross-system pattern is **not a universal sign of \(W_{AD}\)**: constituent mechanisms recur, but their realized balance changes with context, exactly where the theory predicts sign switching. The paper therefore links mathematical mechanism to meta-analytic pattern without treating marginal evidence as empirical calibration of the mixed partial.

**Keywords:** attraction-defence interaction; floral defence; florivory; mechanism; meta-analysis; mutualism; pollination; trait integration
"""

NEW_CONTRIBUTIONS = r"""### 1.5 Two-part contribution: mechanism and pattern

The paper is deliberately organized as two linked but inferentially distinct parts.

**Part I — Mechanism.** We derive the local mathematical principle governing attraction-defence complementarity. The contribution is the mechanism-facing decomposition, orientation gate, non-identifiability result, environmental derivative criterion, and finite sensitivity analysis. This part asks **why and under what conditions the sign changes**.

**Part II — Pattern.** We then use those mechanism classes to organize cross-study evidence. Quantitative meta-analysis is used where compatible effect scales exist; otherwise source-adjudicated study clusters are used to map recurrence, same-system co-occurrence, conditionality, and identification gaps without manufacturing a common effect size. This part asks **which theory-predicted mechanisms recur across systems, which pattern is general, and where context changes the state**.

The key synthesis is therefore Mechanism \(\rightarrow\) Pattern, not theory \(\rightarrow\) validation. Cross-system recurrence is evidence for biological generality of the constituent processes; it is not a prevalence estimate and it does not empirically identify \(W_{AD}\).

### 1.6 Paper organization

Section 2 develops Part I, the mechanistic theory. Section 3 gives the corresponding theoretical results and sensitivity analysis. Section 4 defines Part II, the meta-analytic and cross-study pattern methods. Section 5 reports the recurrent empirical patterns and the two quantitative cross-study syntheses. Section 6 integrates mechanism and pattern, and Section 7 concludes.
"""

PART2_SYNTHESIS = r"""### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance

Taken together, Part II identifies a general empirical pattern that is narrower and more defensible than a universal attraction-defence sign. The constituent routes required by Part I recur across independent systems, and the two quantitative syntheses retain their principal direction under influence checks. At the same time, same-system evidence and eleven sign/state-switch clusters show that dose, resource context, exposure duration, consumer identity, response definition, and compound identity repeatedly alter whether a channel is expressed. Direct \(A\times D\) and direct joint-cost estimates remain sparse. The meta-analytic pattern is therefore **recurrent mechanism plus context-dependent balance**, not a universal value or sign of \(W_{AD}\).
"""


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + replacement.rstrip() + "\n\n" + text[j:]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    required_structure = (
        "## 2. Part I — Mechanistic theory: mechanism and principle",
        "## 3. Part I results — mechanistic sign regimes",
        "## 4. Part II — Meta-analysis and cross-study pattern synthesis",
        "## 5. Part II results — meta-analytic patterns across systems",
        "## 6. Integration — from mechanism to pattern",
        "## 7. Conclusions",
    )
    for token in required_structure:
        if token not in text:
            raise RuntimeError(f"Mechanism -> Pattern structure missing: {token}")

    lines = text.splitlines()
    if not lines:
        raise RuntimeError("Manuscript is empty")
    lines[0] = NEW_TITLE
    text = "\n".join(lines) + "\n"

    text = replace_between(text, "## Abstract", "## 1. Introduction", NEW_ABSTRACT)
    text = replace_between(
        text,
        "### 1.5 Two-part contribution: mechanism and pattern",
        "## 2. Part I — Mechanistic theory: mechanism and principle",
        NEW_CONTRIBUTIONS,
    )
    text = replace_between(
        text,
        "### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance",
        "## 6. Integration — from mechanism to pattern",
        PART2_SYNTHESIS,
    )

    required_latex = (
        r"\(W_{AD}=\rho-\iota-\kappa\)",
        r"\(A\times D\)",
        r"Mechanism \(\rightarrow\) Pattern",
        r"\(W_{AD}\)",
    )
    for token in required_latex:
        if token not in text:
            raise RuntimeError(f"LaTeX-safe framing token missing: {token}")

    corrupted = ("W_{AD}=\nho", "A\times D".replace("\\t", "\t"), "Mechanism \\(\nightarrow")
    for token in corrupted:
        if token in text:
            raise RuntimeError(f"Escape-corrupted framing survived: {token!r}")

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
