"""Promote the saturated Pattern expansion into manuscript-facing artifacts.

This is deliberately heading-scoped: Part I theory and its numerical results are
not rewritten. The script updates only Part II framing/results, Tables 3–4,
Figure 3 captioning, data-availability text, and the small set of references used
for representative expansion examples.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
TABLES = ROOT / "manuscript" / "TABLES_THEORETICAL_ECOLOGY.md"


def replace_section(text: str, start_heading: str, next_heading: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(?ms)^{re.escape(start_heading)}\n.*?(?=^{re.escape(next_heading)}\n)"
    )
    new_text, count = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace section {start_heading!r}; matches={count}")
    return new_text


def replace_abstract(text: str) -> str:
    abstract = (
        "Flowers must attract mutualists while remaining exposed to florivores, nectar robbers, pathogens, and other antagonists. "
        "We ask two linked questions: **what mechanism determines whether floral attraction and defence are locally complementary or substitutable, and what cross-system patterns recur in the empirical literature?** "
        "In Part I, we derive a local mechanistic theory for one declared attraction trait, one flower-specific antagonist-reducing trait, and one declared outcome scale. After an explicit orientation gate, the mixed partial is a balance among antagonist relief, pollinator interference, and direct joint-cost curvature, \\(W_{AD}=\\rho-\\iota-\\kappa\\). "
        "The same total curvature can arise from different channel allocations, so total fitness alone does not identify mechanism. Endpoint-normalized sensitivity analysis produces both complementary and substitutable regimes across 2,592 declared evaluations. "
        "In Part II, we use the theory as a prediction and classification framework for a registered cross-study Pattern synthesis, and use quantitative meta-analysis only where outcomes can be placed on defensible common scales. The saturated evidence architecture contains 56 route-level records across 25 independent biological study clusters, including 14 same-system multi-route clusters and 17 independent context/sign-switch clusters; seven additional context programs are tracked without being added to route-ledger N. "
        "A random-effects reanalysis of floral-larceny data shows recurrent reductions in female fitness (LRR \\(-0.210\\), 48 clusters), nectar standing crop (\\(-0.483\\), 28), and legitimate visitation (\\(-0.291\\), 22), while retaining extreme heterogeneity. A second 32-study-component synthesis of floral volatiles shows shared pollinator/florivore responsiveness but strong compositional and context dependence. Secondary published syntheses independently reinforce tissue, consumer, trait-class, and selection-context dependence without being pooled with the two reproduced modules. "
        "Direct \\(A\\times D\\) evidence remains restricted to one sign-unresolved cluster and direct joint-cost evidence to zero strict estimates. Thus the general cross-system pattern is **not a universal sign of \\(W_{AD}\\)**: constituent mechanisms recur, but their realised balance changes with context."
    )
    pattern = re.compile(r"(?ms)(^## Abstract\n\n).*?(?=\n\n\*\*Keywords:\*\*)")
    new_text, count = pattern.subn(r"\1" + abstract, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace abstract; matches={count}")
    return new_text


def update_manuscript(text: str) -> str:
    text = replace_abstract(text)
    text = text.replace(
        "Section 5 reports the recurrent empirical patterns and the two quantitative cross-study syntheses.",
        "Section 5 reports the recurrent empirical patterns, the two reproduced quantitative syntheses, and three secondary contextual syntheses."
    )

    section_41 = r'''### 4.1 Theory-to-pattern evidence map

The empirical synthesis was organized around the theoretical channels rather than around one taxon, one compound class, or one universal effect-size metric. Evidence was admitted only when the focal floral context, the putative attraction or defence axis, the biological response, and study identity could be source-adjudicated. The four marginal route families were \(A\rightarrow\)pollination, \(A\rightarrow\)antagonism, \(D\rightarrow\)antagonism, and \(D\rightarrow\)pollination. Same-system studies were tracked separately from unrelated marginal studies, and direct \(A\times D\) designs were held to a stricter contract requiring a distinct attraction axis, a flower-specific antagonist-reducing defence/access axis, and an interaction on a common outcome.

After the initial completion gate, we ran a registered Pattern-expansion stage that targeted empty or weakly replicated mechanism/context cells rather than maximizing article count. Expansion records were added only as independent biological clusters under the same route definitions and organ boundary. Studies that changed environmental pressure, damage, pollination syndrome, or a broader reproductive module without a clean focal \(A\) or flower-specific \(D\) were retained as context programs and excluded from route-ledger N. The expansion stopped after two consecutive targeted screening batches yielded no new admissible theory-facing Pattern class; a parallel quantitative search likewise yielded no sixth synthesis with a distinct Pattern axis beyond the admitted module set.

Within-study or within-system state changes were retained rather than averaged away. The expanded ontology includes trait intensity/expression, resource/exposure context, consumer identity and functional role, response definition/stage/scale, compound or mechanism identity, guarded defence states, spatial/temporal/attack-mode filtering, visitor functional-mode switching, lifecycle-stage role reversal, and population/site or trait-class dependence. Because the underlying outcomes include visitation, handling, consumption, residence time, floral damage, reproduction, physiological detection, and other non-equivalent constructs, we did not fit a cross-outcome grand moderator coefficient.

The synthesis completion gate therefore requires explicit empirical states for all four marginal families, saturation of the direct-interaction and direct joint-cost searches, same-system linkage, conditionality mapping where possible, two reproduced quantitative cross-study modules, transparent status labels for secondary contextual syntheses, module-appropriate robustness checks, and explicit validation of the boundary between marginal evidence and the theoretical mixed partial.'''
    text = replace_section(text, "### 4.1 Theory-to-pattern evidence map", "### 4.2 Quantitative meta-analytic modules", section_41)

    # Insert secondary-module methods before Part II results while preserving the two reproduced modules.
    marker = "## 5. Part II results — meta-analytic patterns across systems"
    if "#### 4.2.3 Secondary cross-synthesis/context modules" not in text:
        insert = r'''#### 4.2.3 Secondary cross-synthesis/context modules

Three additional syntheses were retained as independent contextual modules rather than promoted to co-equal reproduced meta-analyses. Haas-Desmarais et al. (2026) provide a published multilevel synthesis of 171 studies and 1,348 study cases on herbivory effects on floral traits, pollinator attraction, and reproduction; we independently retrieved and hashed the publisher supplementary package, but did not reconstruct its raw effect-size table locally, and herbivory treatment is not equated with the focal floral defence trait \(D\). Caruso et al. (2019) provide a published selection synthesis whose main uncertainty-bearing analysis uses 755 directional selection gradients with standard errors from 36 articles; the Dryad landing record and workbook identities were verified, but current file-byte access was blocked, so the study remains a published selection-context module rather than a local reanalysis. Junker and Blüthgen (2010) synthesize 18 publications and 425 floral-scent response observations; their visitor-dependence categories provide an independent consumer-filtering pattern but are not treated as identical to pollinator-versus-antagonist roles.

These modules are used to test recurrence of tissue, trait-class, consumer, assay, and selection-context dependence. Their study or observation counts are never added to the route-ledger cluster total, and their effect scales are not pooled with the Leal or Sasidharan modules.

'''
        text = text.replace(marker, insert + marker, 1)

    section_51 = r'''### 5.1 Pattern scaffold: mechanism recurrence and same-system architecture

The saturated source-adjudicated route ledger contained 56 effect or directional records across 25 independent biological study clusters. All four marginal route families had explicit empirical states. Independent cluster counts were five for \(A\rightarrow\)pollination, eight for \(A\rightarrow\)antagonism, eighteen for \(D\rightarrow\)antagonism, and ten for \(D\rightarrow\)pollination. These overlapping counts describe evidence capacity in the screened architecture and are not estimates of mechanism prevalence in nature.

Fourteen study clusters contained at least two theory-relevant marginal routes in the same biological system. The expansion broadened both mechanism and taxonomic coverage. Attraction-side recurrence now includes visual and colour/scent signal axes associated with antagonist use as well as shared mutualist-antagonist tracking; a recombinant *Silene* signal system independently links floral colour and scent dimensions to seed-predator host choice (Page et al. 2014). Defence-side recurrence spans chemical deterrence and several distinct physical solutions, including liquid-filled bracts or calyces, sticky corolla surfaces, slippery wax-covered perianths, petal hairs, and spur-enclosing bracts. In *Pedicularis rex*, a water-filled bract strongly reduced seed predation while showing no detected effect on legitimate pollinator or nectar-robber visitation, because robbers could bypass the barrier's attack geometry (Sun and Huang 2015). In *Thunia alba*, removing a spur-enclosing bract shifted the same *Bombus* visitor from legitimate pollination toward nectar robbery without increasing hourly arrival frequency, while pollinia transfer and fruit set declined (Wu and Gao 2024).

The same-system panel therefore supports guarded defence, shared signal tracking, attack-mode filtering, and visitor functional-mode routing as recurrent biological states. It still does not identify the full mixed partial because the component routes are generally not estimated on a common outcome scale.'''
    text = replace_section(text, "### 5.1 Pattern scaffold: mechanism recurrence and same-system architecture", "### 5.2 Identification-gap pattern: direct interaction scarcity and joint cost", section_51)

    section_53 = r'''### 5.3 Conditionality pattern: mechanism channels open, close, and change role

Seventeen independent study clusters contained source-verified changes in sign or biological state across contexts. Seven additional context programs were retained outside route-ledger N because their focal manipulation was environmental pressure, damage, pollination syndrome, or a broader reproductive module rather than a clean marginal \(A\) or flower-specific \(D\) route.

The resulting ontology is broader than a list of positive-versus-negative reversals. Trait intensity, reward or exposure context, consumer identity, response stage, compound identity, and population context can change effect state. Physical defences can also be spatially or temporally gated: body size, floral position, attack mode, or the pollinator-critical stage determines which consumer can cross a barrier. Guarded states recur in which antagonist reduction is strong but a pollinator penalty is not detected on the tested response. Conversely, the same visitor can change ecological function without a change in identity: floral access architecture can route a visitor between legitimate pollination and robbery. A separate *Silene stellata* system extends this principle across the consumer lifecycle, with adult *Hadena* contributing pollination while larvae impose seed-predation costs and selection differs through male and female fitness pathways (Zhou et al. 2020).

Conditionality therefore occurs as true direction changes, as threshold-like opening or closing of channels, and as changes in the ecological role carried by the same consumer taxon. This is the empirical Pattern most directly aligned with the Part I balance criterion.'''
    text = replace_section(text, "### 5.3 Conditionality pattern across five theory-facing classes", "### 5.4 Meta-analysis 1: floral larceny imposed recurrent costs with extreme heterogeneity", section_53)

    section_56 = r'''### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance

Taken together, Part II identifies a general empirical pattern that is narrower and more defensible than a universal attraction-defence sign. The four constituent route families recur across 25 independent source-adjudicated biological systems, including repeated visual/scent attraction signals and chemically or physically distinct antagonist-reducing traits. Fourteen same-system clusters show that routes can co-occur, while 17 sign/state-switch clusters and seven context-only programs show that trait intensity, resources, exposure, consumer identity, attack geometry, response stage, population, visitor functional mode, and even consumer lifecycle can change which channel is expressed.

The two reproduced quantitative syntheses retain their principal direction under their declared influence checks. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale. Direct \(A\times D\) remains one sign-unresolved strict cluster, and direct joint-cost evidence remains zero strict estimates. The meta-analytic Pattern is therefore **recurrent mechanisms plus context-dependent balance**, not a universal value or sign of \(W_{AD}\).'''
    text = replace_section(text, "### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance", "## 6. Integration — from mechanism to pattern", section_56)

    section_61 = r'''### 6.1 A conditional sign boundary is biologically necessary, not merely mathematically possible

Part I shows that local complementarity requires antagonist relief to exceed pollinator interference plus direct joint-cost curvature. Part II shows, through meta-analysis and the saturated Pattern synthesis, why each side of that inequality must remain open. Independent systems include guarded states in which antagonist reduction occurs with little detected pollinator cost, signal axes tracked by both mutualists and antagonists, physical barriers whose efficacy depends on consumer size or attack mode, and cases in which the same visitor changes from legitimate pollinator to robber while its arrival rate stays similar. Consumer role can even reverse across life stages.

The combined result is stronger than simply observing literature heterogeneity. The relevant heterogeneity has mechanism structure: ecological conditions determine whether a channel is expressed, how strongly it is expressed, and what ecological function a consumer performs. A universal attraction-defence sign would therefore erase precisely the biological variation that the theory says is decisive.'''
    text = replace_section(text, "### 6.1 A conditional sign boundary is biologically necessary, not merely mathematically possible", "### 6.2 Constituent-path evidence is not validation of the mixed partial", section_61)

    section_62 = r'''### 6.2 Constituent-path evidence is not validation of the mixed partial

The empirical synthesis supports the biological reality and recurrence of several components required by the model, but it does not calibrate \(W_{AD}\). The Leal larceny module demonstrates that one class of floral antagonists can impose substantial reward, visitation, and female-fitness costs. The Sasidharan volatile module demonstrates that floral signals can be detected or behaviorally tracked by both pollinators and florivores, with repeated context-dependent disagreement. The secondary Haas-Desmarais, Caruso, and Junker-Blüthgen syntheses add independent evidence that tissue, trait class, consumer identity, assay context, and selection environment matter, but their different scales and evidence statuses are intentionally not pooled.

Same-system studies further show that antagonist relief and pollinator interference can coexist, separate, or be routed through different consumer functions. None of these marginal, same-system, or secondary-synthesis results is algebraically equivalent to the direct attraction-defence mixed partial. That distinction is the empirical version of Proposition 1. More observations of total fitness or more unrelated route studies cannot identify the channel allocation unless the same focal traits and channel outcomes are linked within a design that supports the required cross-curvatures.'''
    text = replace_section(text, "### 6.2 Constituent-path evidence is not validation of the mixed partial", "### 6.3 Direct evidence scarcity is itself informative", section_62)

    conclusion = r'''## 7. Conclusions

Floral attraction and defence are locally complementary when antagonist relief exceeds pollinator interference and direct joint-cost curvature, and locally substitutable when the opposing contributions dominate. The value of this criterion lies less in naming a mixed partial than in making its mechanism, orientation assumptions, environmental derivatives, and inference limits explicit.

The saturated Pattern synthesis shows that the constituent mechanisms are biologically real and recurrent across multiple floral signal modalities and multiple chemical and physical defence mechanisms. It also shows that conditionality is structured: guarded defence, spatial and temporal filtering, attack-mode dependence, visitor functional-mode switching, lifecycle-stage role reversal, and response- or population-level dependence all recur. Two reproduced quantitative synthesis modules strengthen the evidence that antagonist pressure and shared floral signals matter, while three secondary contextual syntheses reinforce tissue, consumer, trait-class, assay, and selection-context dependence without being treated as equivalent effect scales.

The literature remains weakest exactly where the theory demands the strongest identification. Direct attraction × defence interactions remain rare, and direct joint-cost curvature remains unidentified. The integrated result is therefore a division of labour between mechanism and Pattern: Part I identifies the sign boundary and the measurements required to cross it; Part II shows which channels recur, how ecological state reallocates them, and which quantities are still missing. The highest-value next empirical test is a factorial design on distinct focal attraction and flower-specific defence axes with channel-specific outcomes, not another undifferentiated marginal literature average.'''
    text = replace_section(text, "## 7. Conclusions", "## Figure captions", conclusion)

    old_caption = "**Figure 3. Meta-analytic pattern architecture and identification boundary.** Source-adjudicated evidence is organized as four marginal route families, same-system multi-route regimes, context/sign-switch classes, two quantitative synthesis modules, the saturated direct \\(A\\times D\\) layer, and the direct joint-cost search. Counts indicate evidence capacity in the screened architecture rather than prevalence. Marginal and same-system evidence terminate at the inference boundary and are not combined into an estimate of \\(W_{AD}\\)."
    new_caption = "**Figure 3. Meta-analytic pattern architecture and identification boundary.** Source-adjudicated evidence is organized as four marginal route families, same-system multi-route regimes, context/sign-switch and context-only programs, two reproduced quantitative synthesis modules, three secondary contextual syntheses, the saturated direct \\(A\\times D\\) layer, and the direct joint-cost search. Counts indicate evidence capacity in the screened architecture rather than prevalence. Guarded defence, spatial/temporal filtering, visitor functional-mode switching, and lifecycle-role reversal are shown as recurrent state classes. Marginal, same-system, and secondary contextual evidence terminate at the inference boundary and are not combined into an estimate of \\(W_{AD}\\)."
    if old_caption not in text:
        raise RuntimeError("Figure 3 caption anchor not found")
    text = text.replace(old_caption, new_caption, 1)

    data_pattern = re.compile(r"(?ms)^## Data and code availability\n\n.*?(?=^## Author contributions\n)")
    data_text = r'''## Data and code availability

All code, declared configurations, generated readouts, source-adjudication products, saturation receipts, and validation tests required for the fixed theory, finite sensitivity analysis, and saturated mechanism-Pattern synthesis are maintained in the associated repository. The completed Leal et al. (2025) larceny module is pinned to immutable repository commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`; the Sasidharan et al. (2023) module uses the 32-component citation topology as its canonical dependence structure. Pattern-expansion ledgers, context programs, stopping-gate records, the Haas-Desmarais supplement receipt, and the Caruso Dryad access-state receipt are versioned with the manuscript branch. A versioned archival DOI will be added before submission.

'''
    text, count = data_pattern.subn(data_text, text, count=1)
    if count != 1:
        raise RuntimeError("Data availability section anchor not found")

    # Curated representative expansion references used in the main text.
    refs = [
        "Page P, Favre A, Schiestl FP, Karrenberg S (2014) Do flower color and floral scent of *Silene* species affect host preference of *Hadena bicruris*, a seed-eating pollinator, under field conditions? *PLoS ONE* 9:e98755. https://doi.org/10.1371/journal.pone.0098755",
        "Sun SG, Huang SQ (2015) Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019. https://doi.org/10.1093/aobpla/plv019",
        "Wu SM, Gao JY (2024) The conspicuously large bracts influence reproductive success in *Thunia alba* (Orchidaceae). *Journal of Plant Ecology* 17:rtad036. https://doi.org/10.1093/jpe/rtad036",
        "Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB (2020) Variable and sexually conflicting selection on *Silene stellata* floral traits by a putative moth pollinator selective agent. *Evolution* 74:1321–1334. https://doi.org/10.1111/evo.13965",
    ]
    for ref in refs:
        if ref not in text:
            text = text.rstrip() + "\n\n" + ref + "\n"
    return text


def update_tables(text: str) -> str:
    table3 = r'''## Table 3. Cross-study pattern scaffold: mechanism recurrence, conditionality, and identification gaps

| Evidence layer | Current independent study clusters / state | Main empirical Pattern | Inference boundary |
|---|---:|---|---|
| \(A\rightarrow\)pollination | 5 clusters | Attraction can increase pollinator use or pollinator-mediated reproduction; visitor identity and functional mode can change the realised return | Does not identify \(M_{AD}\) without the same focal \(D\) |
| \(A\rightarrow\)antagonism | 8 clusters | Floral signals are also tracked by antagonists across volatile, visual-bract, colour, and multidimensional colour/scent systems | Does not estimate antagonist-relief curvature by itself |
| \(D\rightarrow\)antagonism | 18 clusters | Flower-specific chemical and physically distinct barriers reduce antagonist entry, use, oviposition, or damage | Marginal defence efficacy is not \(G_{AD}\) unless linked to the marginal value of the same \(A\) |
| \(D\rightarrow\)pollination | 10 clusters | Pollinator effects include guarded nulls, interference, reward compensation, consumer specificity, and changes in legitimate-versus-robbing function | A marginal pollinator effect is not automatically \(M_{AD}\) |
| Same-system multi-route | 14 clusters | Guarded defence, shared tracking, attack-mode filtering, functional-mode routing, response dependence, and unresolved regimes recur | Same-system marginal routes are stronger linkage evidence but are not direct \(A\times D\) estimates |
| Context/sign switching | 17 clusters | Channels open, close, or change role across trait intensity, resource/exposure, consumer identity, response stage, population, attack geometry, and lifecycle | Counts are recurrence within the screened architecture, not prevalence |
| Context-only programs | 7 programs, excluded from route N | Environmental damage, pollination syndrome, reproductive-module defence, temporal ant exclusion, and lifecycle-linked selection add context without pretending to be clean marginal routes | Program count is not added to the 25 route-ledger clusters |
| Direct \(A\times D\) | 1 strict cluster | *Impatiens capensis*: two reproductive-component interactions are estimable but both CIs cross zero and point signs differ | No general direct sign is identified |
| Direct joint cost \(\kappa\) | 0 strict estimates after saturated registered search | Marginal costs, covariance, and ecological interference exist, but no strict simultaneous A+D intrinsic-cost estimate was found | \(\kappa\) is unidentified, not zero |

**Pattern-scaffold note.** The saturated architecture contains 56 source-adjudicated effect/directional records across 25 independent biological study clusters. Route-specific cluster counts overlap because the same study may contribute to several linked routes. Seven additional context programs and all study/case counts from secondary syntheses are excluded from route-ledger N. The expansion stopped after two consecutive targeted screening batches produced no new admissible Pattern class. This table maps recurrence onto Part I mechanism classes; it is not a grand meta-analysis and its counts are not prevalence estimates.'''
    text = replace_section(text, "## Table 3. Cross-study pattern scaffold: mechanism recurrence, conditionality, and identification gaps", "## Table 4. Quantitative meta-analytic patterns and admitted inference", table3)

    table4 = r'''## Table 4. Quantitative meta-analytic patterns and admitted inference

| Module | Data structure and scale | Quantitative / published Pattern | Robustness / limitation | Admitted role in the Mechanism → Pattern paper |
|---|---|---|---|---|
| **Reproduced meta-analysis 1 — Leal et al. 2025 floral larceny** | Secondary reanalysis of deposited study-level group data; one aggregate effect per independent cluster and outcome stratum; log response ratio | Female reproductive success: \(-0.210\), 48 clusters; nectar standing crop: \(-0.483\), 28; legitimate visitation: \(-0.291\), 22 | Direction stable to declared within-cluster correlation, quarantined-row sensitivity, and leave-one-cluster-out; very high heterogeneity | Establishes recurrent realised antagonist costs across fitness, reward, and visitation |
| **Reproduced synthesis 2 — Sasidharan et al. 2023 FVOCs** | Deposited categorical synthesis reconstructed into 32 conservative study components | Physiological detection: florivore 84/103 vs pollinator 151/220; assembled risk difference \(+0.129\); positive in 32/32 leave-one-study-component-out refits | Only three components contain both physiological roles and all paired differences are zero; behavioral and source-version discrepancies retained | Establishes shared consumer responsiveness plus composition/context dependence without claiming a causal paired role effect |
| **Secondary context — Haas-Desmarais et al. 2026** | Published multilevel meta-analysis; 171 studies, 1,348 study cases; Hedges-type effect scale | Overall negative herbivory-associated response with strong tissue, damage-type, response, and interaction dependence | Publisher supplement package independently retrieved and hashed; raw effect table not locally reconstructed; herbivory treatment is not focal \(D\) | Independent large-scale support for antagonist-pressure and tissue/context dependence |
| **Secondary context — Caruso et al. 2019** | Published selection synthesis; main analysis 755 directional gradients with SE from 36 articles | Selection depends on environmental agent, floral trait class, and pollinator guild | Dryad landing/API metadata and workbook identities verified; current file-byte access blocked; selection gradient is not \(W_{AD}\) | Independent selection-context support without relabelling other-biotic treatments as \(H\) |
| **Secondary cross-synthesis — Junker & Blüthgen 2010** | Published floral-scent synthesis; 18 publications, 425 observations | Visitor response differs with dependence on floral resources and remains different after study-level reduction | Visitor-dependence categories do not equal pollinator-versus-antagonist roles | Independent support for consumer-filtering and assay/context dependence |

**Boundary for all modules.** None estimates \(\rho\), \(\iota\), \(\kappa\), or \(W_{AD}\). Only the first two are reproduced quantitative modules in the current repository; the remaining three are explicitly secondary contextual/cross-synthesis modules. Together with Table 3, the Part II result is **recurrent mechanisms plus context-dependent balance**, not a universal sign of `W_AD`.'''
    pattern = re.compile(r"(?ms)^## Table 4\. Quantitative meta-analytic patterns and admitted inference\n.*\Z")
    text, count = pattern.subn(table4.rstrip() + "\n", text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace Table 4")
    return text


def main() -> None:
    manuscript = update_manuscript(MANUSCRIPT.read_text(encoding="utf-8"))
    tables = update_tables(TABLES.read_text(encoding="utf-8"))
    MANUSCRIPT.write_text(manuscript, encoding="utf-8")
    TABLES.write_text(tables, encoding="utf-8")
    print("promoted saturated Pattern expansion into manuscript and Tables 3–4")


if __name__ == "__main__":
    main()
