"""Restructure the canonical manuscript into an explicit Mechanism -> Pattern paper.

Part I is the fixed mathematical mechanism/principle. Part II is the empirical
pattern layer, using quantitative meta-analysis where outcomes are compatible
and source-adjudicated cross-study pattern synthesis where they are not.

This script deliberately does not change any canonical theoretical equation or
quantitative result. It changes manuscript organization and framing only.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"

OLD_TITLE = "# When are floral attraction and defence complementary? A local mechanistic diagnostic and mechanism-pattern synthesis across mutualists and antagonists"
NEW_TITLE = "# When are floral attraction and defence complementary? Mechanistic theory and meta-analytic patterns across mutualists and antagonists"

NEW_ABSTRACT = """## Abstract

Flowers must attract mutualists while remaining exposed to florivores, nectar robbers, pathogens, and other antagonists. We ask two linked questions: **what mechanism determines whether floral attraction and defence are locally complementary or substitutable, and what cross-system patterns recur in the empirical literature?** In Part I, we derive a local mechanistic theory for one declared attraction trait, one flower-specific antagonist-reducing trait, and one declared outcome scale. After an explicit orientation gate, the mixed partial is a balance among antagonist relief, pollinator interference, and direct joint-cost curvature, \(W_{AD}=\rho-\iota-\kappa\). The same total curvature can arise from different channel allocations, so total fitness alone does not identify mechanism. Endpoint-normalized sensitivity analysis produces both complementary and substitutable regimes across 2,592 declared evaluations. In Part II, we use the theory as a prediction and classification framework for a registered cross-study pattern synthesis, and use quantitative meta-analysis only where outcomes can be placed on defensible common scales. The evidence map contains 38 route-level records across 14 independent biological study clusters, including ten same-system multi-route clusters and eleven independent context/sign-switch clusters. A random-effects reanalysis of floral-larceny data shows recurrent reductions in female fitness (LRR \(-0.210\), 48 clusters), nectar standing crop (\(-0.483\), 28), and legitimate visitation (\(-0.291\), 22), while retaining extreme heterogeneity. A second 32-study-component synthesis of floral volatiles shows shared pollinator/florivore responsiveness but strong compositional and context dependence. Direct \(A\times D\) evidence remains restricted to one sign-unresolved cluster and direct joint-cost evidence to zero strict estimates. Thus the general cross-system pattern is **not a universal sign of \(W_{AD}\)**: constituent mechanisms recur, but their realized balance changes with context, exactly where the theory predicts sign switching. The paper therefore links mathematical mechanism to meta-analytic pattern without treating marginal evidence as empirical calibration of the mixed partial.

**Keywords:** attraction-defence interaction; floral defence; florivory; mechanism; meta-analysis; mutualism; pollination; trait integration
"""

NEW_CONTRIBUTIONS = """### 1.5 Two-part contribution: mechanism and pattern

The paper is deliberately organized as two linked but inferentially distinct parts.

**Part I — Mechanism.** We derive the local mathematical principle governing attraction-defence complementarity. The contribution is the mechanism-facing decomposition, orientation gate, non-identifiability result, environmental derivative criterion, and finite sensitivity analysis. This part asks **why and under what conditions the sign changes**.

**Part II — Pattern.** We then use those mechanism classes to organize cross-study evidence. Quantitative meta-analysis is used where compatible effect scales exist; otherwise source-adjudicated study clusters are used to map recurrence, same-system co-occurrence, conditionality, and identification gaps without manufacturing a common effect size. This part asks **which theory-predicted mechanisms recur across systems, which pattern is general, and where context changes the state**.

The key synthesis is therefore Mechanism \(\rightarrow\) Pattern, not theory \(\rightarrow\) validation. Cross-system recurrence is evidence for biological generality of the constituent processes; it is not a prevalence estimate and it does not empirically identify \(W_{AD}\).

### 1.6 Paper organization

Section 2 develops Part I, the mechanistic theory. Section 3 gives the corresponding theoretical results and sensitivity analysis. Section 4 defines Part II, the meta-analytic and cross-study pattern methods. Section 5 reports the recurrent empirical patterns and the two quantitative cross-study syntheses. Section 6 integrates mechanism and pattern, and Section 7 concludes.
"""

PART2_OPEN = """## 4. Part II — Meta-analysis and cross-study pattern synthesis

Part II asks whether the mechanism classes derived in Part I recur across independent biological systems and whether their realized state changes systematically with context. We use **meta-analysis** only where study outcomes can be expressed on a defensible common quantitative scale. Where outcome scales are intrinsically non-equivalent, we retain a source-adjudicated cross-study pattern map rather than pooling incompatible quantities. Accordingly, cross-system generality here means recurrence across independent systems and robustness within the admitted synthesis, not prevalence in nature.

"""

PART2_SYNTHESIS = """
### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance

Taken together, Part II identifies a general empirical pattern that is narrower and more defensible than a universal attraction-defence sign. The constituent routes required by Part I recur across independent systems, and the two quantitative syntheses retain their principal direction under influence checks. At the same time, same-system evidence and eleven sign/state-switch clusters show that dose, resource context, exposure duration, consumer identity, response definition, and compound identity repeatedly alter whether a channel is expressed. Direct \(A\times D\) and direct joint-cost estimates remain sparse. The meta-analytic pattern is therefore **recurrent mechanism plus context-dependent balance**, not a universal value or sign of \(W_{AD}\).
"""


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + replacement + "\n" + text[j:]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if OLD_TITLE not in text and NEW_TITLE not in text:
        raise RuntimeError("Unexpected manuscript title")
    text = text.replace(OLD_TITLE, NEW_TITLE, 1)

    # Replace the abstract/keywords as one unit so the two-part logic is visible
    # before the reader reaches the Methods.
    abstract_start = text.index("## Abstract")
    intro_start = text.index("## 1. Introduction")
    text = text[:abstract_start] + NEW_ABSTRACT + "\n" + text[intro_start:]

    # Replace the contributions + organization block.
    contrib_start = text.index("### 1.5 Contributions")
    theory_start = text.index("## 2. Model and analytical framework")
    text = text[:contrib_start] + NEW_CONTRIBUTIONS + "\n" + text[theory_start:]

    # Split the original mixed Methods/Results into an explicit Part I and Part II.
    theory_start = text.index("## 2. Model and analytical framework")
    empirical_methods_start = text.index("### 2.7 Mechanism-pattern empirical synthesis")
    results_start = text.index("## 3. Results")
    empirical_results_start = text.index("### 3.4 Mechanism recurrence and same-system architecture")
    discussion_start = text.index("## 4. Discussion")
    conclusion_start = text.index("## 5. Conclusions")

    prefix = text[:theory_start]
    theory_methods = text[theory_start:empirical_methods_start]
    empirical_methods = text[empirical_methods_start:results_start]
    all_results = text[results_start:discussion_start]
    split_result = all_results.index("### 3.4 Mechanism recurrence and same-system architecture")
    theory_results = all_results[:split_result]
    empirical_results = all_results[split_result:]
    discussion = text[discussion_start:conclusion_start]
    conclusion_and_rest = text[conclusion_start:]

    theory_methods = theory_methods.replace(
        "## 2. Model and analytical framework",
        "## 2. Part I — Mechanistic theory: mechanism and principle",
        1,
    )
    theory_results = theory_results.replace(
        "## 3. Results",
        "## 3. Part I results — mechanistic sign regimes",
        1,
    )

    empirical_methods = empirical_methods.replace(
        "### 2.7 Mechanism-pattern empirical synthesis",
        "### 4.1 Theory-to-pattern evidence map",
        1,
    ).replace(
        "### 2.8 Quantitative synthesis modules",
        "### 4.2 Quantitative meta-analytic modules",
        1,
    ).replace(
        "#### 2.8.1 Floral-larceny antagonist-pressure module",
        "#### 4.2.1 Meta-analysis 1: floral-larceny antagonist-pressure pattern",
        1,
    ).replace(
        "#### 2.8.2 Floral-volatile pollinator/florivore module",
        "#### 4.2.2 Meta-analytic synthesis 2: floral-volatile consumer-response pattern",
        1,
    )

    empirical_results = empirical_results.replace(
        "### 3.4 Mechanism recurrence and same-system architecture",
        "### 5.1 Pattern scaffold: mechanism recurrence and same-system architecture",
        1,
    ).replace(
        "### 3.5 Direct interaction scarcity and direct joint-cost gap",
        "### 5.2 Identification-gap pattern: direct interaction scarcity and joint cost",
        1,
    ).replace(
        "### 3.6 Conditionality recurred across five theory-facing classes",
        "### 5.3 Conditionality pattern across five theory-facing classes",
        1,
    ).replace(
        "### 3.7 Quantitative module 1: floral larceny imposed realised costs but did not explain most heterogeneity",
        "### 5.4 Meta-analysis 1: floral larceny imposed recurrent costs with extreme heterogeneity",
        1,
    ).replace(
        "### 3.8 Quantitative module 2: floral volatile responses were shared but composition-dependent",
        "### 5.5 Meta-analytic synthesis 2: floral volatile responses were shared but composition-dependent",
        1,
    )

    # Make the empirical Results an explicit Pattern half.
    empirical_results = "## 5. Part II results — meta-analytic patterns across systems\n\n" + empirical_results
    empirical_results = empirical_results.rstrip() + "\n\n" + PART2_SYNTHESIS.strip() + "\n\n"

    discussion = discussion.replace(
        "## 4. Discussion",
        "## 6. Integration — from mechanism to pattern",
        1,
    )
    for old, new in (
        ("### 4.1", "### 6.1"),
        ("### 4.2", "### 6.2"),
        ("### 4.3", "### 6.3"),
        ("### 4.4", "### 6.4"),
        ("### 4.5", "### 6.5"),
        ("### 4.6", "### 6.6"),
    ):
        discussion = discussion.replace(old, new)
    discussion = discussion.replace(
        "The theory shows that local complementarity requires antagonist relief to exceed pollinator interference plus direct joint-cost curvature. The empirical synthesis shows why each side of that inequality must remain open.",
        "Part I shows that local complementarity requires antagonist relief to exceed pollinator interference plus direct joint-cost curvature. Part II shows, through meta-analysis and cross-study pattern synthesis, why each side of that inequality must remain open.",
        1,
    )

    conclusion_and_rest = conclusion_and_rest.replace("## 5. Conclusions", "## 7. Conclusions", 1)
    conclusion_and_rest = conclusion_and_rest.replace(
        "The empirical synthesis independently shows that the constituent mechanisms are biologically real, recur across systems, and change state across dose, resource, exposure, consumer, response, and compound contexts.",
        "The meta-analytic pattern synthesis independently shows that the constituent mechanisms are biologically real, recur across systems, and change state across dose, resource, exposure, consumer, response, and compound contexts.",
        1,
    )
    conclusion_and_rest = conclusion_and_rest.replace(
        "The integrated result is therefore a division of labour between theory and evidence. Theory identifies the sign boundary and the measurements required to cross it; empirical synthesis shows which channels recur, where conditionality enters, and which quantities are still missing.",
        "The integrated result is therefore a division of labour between mechanism and pattern. Part I identifies the sign boundary and the measurements required to cross it; Part II uses meta-analysis and cross-study synthesis to show which channels recur, where conditionality enters, and which quantities are still missing.",
        1,
    )
    conclusion_and_rest = conclusion_and_rest.replace(
        "**Figure 3. Empirical mechanism-pattern architecture and identification boundary.**",
        "**Figure 3. Meta-analytic pattern architecture and identification boundary.**",
        1,
    )
    conclusion_and_rest = conclusion_and_rest.replace(
        "**Table 3. Source-adjudicated empirical mechanism coverage, same-system architecture, conditionality, direct-interaction state, and direct joint-cost evidence state.**",
        "**Table 3. Cross-study pattern scaffold: source-adjudicated mechanism recurrence, same-system architecture, conditionality, direct-interaction state, and direct joint-cost evidence state.**",
        1,
    )
    conclusion_and_rest = conclusion_and_rest.replace(
        "**Table 4. Quantitative synthesis modules and their admitted inferences, robustness checks, and prohibited interpretations.**",
        "**Table 4. Quantitative meta-analytic modules, recurrent patterns, robustness checks, and prohibited interpretations.**",
        1,
    )

    rebuilt = (
        prefix
        + theory_methods
        + theory_results
        + PART2_OPEN
        + empirical_methods
        + empirical_results
        + discussion
        + conclusion_and_rest
    )

    required = (
        "## 2. Part I — Mechanistic theory: mechanism and principle",
        "## 3. Part I results — mechanistic sign regimes",
        "## 4. Part II — Meta-analysis and cross-study pattern synthesis",
        "## 5. Part II results — meta-analytic patterns across systems",
        "## 6. Integration — from mechanism to pattern",
        "## 7. Conclusions",
        "W_{AD}=\\rho-\\iota-\\kappa",
        "38 route-level records across 14 independent biological study clusters",
        "LRR \\(-0.210\\), 48 clusters",
        "32-study-component synthesis",
    )
    for token in required:
        if token not in rebuilt:
            raise RuntimeError(f"Required mechanism-pattern token missing after rebuild: {token}")

    # Guard against the old interleaved structure returning.
    forbidden = (
        "## 2. Model and analytical framework",
        "### 2.7 Mechanism-pattern empirical synthesis",
        "## 3. Results",
        "### 3.7 Quantitative module 1",
        "## 4. Discussion",
        "## 5. Conclusions",
    )
    for token in forbidden:
        if token in rebuilt:
            raise RuntimeError(f"Old interleaved structure survived: {token}")

    PATH.write_text(rebuilt, encoding="utf-8")


if __name__ == "__main__":
    main()
