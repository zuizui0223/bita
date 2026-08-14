# Mechanism-first universality readout v1

## Current decision frame

This is a **theory-prediction replication audit**, not a conventional pattern-discovery meta-analysis.

Part I fixes the admissible mechanism balance first. Part II asks whether the predicted constituent routes and state transitions recur independently across taxa, floral modalities, defence mechanisms, consumer guilds, and response stages.

Current source universe on PR #129:

```text
route records:                    56
independent biological clusters: 25
A -> pollination:                  5 clusters
A -> antagonism:                   8
D -> antagonism:                  18
D -> pollination:                 10
same-system multi-route:          14
context/sign-switch:              17
context-only programs:             7
```

These route counts overlap and are not prevalence estimates.

## U1 — antagonist cost / relief opportunity

**Status: RECURRENT_STRONG**

Quantitative support is strongest here. Leal et al. 2025 gives negative pooled log-response-ratio effects for female reproductive success `-0.210` (48 independent clusters), nectar standing crop `-0.483` (28), and legitimate visitation `-0.291` (22). Under REML + modified Hartung-Knapp sensitivity, female fitness and nectar remain clearly below zero; legitimate visitation remains negative but its upper interval endpoint nearly touches zero.

Haas-Desmarais et al. 2026 independently supports recurrent negative herbivory consequences across floral traits, pollinator attraction, and reproduction, with strong tissue/damage-mode heterogeneity.

**Interpretation:** antagonist pressure creates a recurrent biological opportunity for `rho`, but the downstream pollination component is less universal than reward/reproductive cost.

## U2 — shared attraction tracking

**Status: RECURRENT_PROVISIONAL**

Sasidharan et al. 2023 supports broad floral-volatile responsiveness in both florivores and pollinators across a conservative 32-study-component topology. Source-level systems independently extend antagonist tracking beyond scent to visual bracts, petal colour, and recombinant colour+scent axes (`Dalechampia`, `Raphanus`, `Silene`).

However, the Sasidharan assembled contrast is not a causal paired-role estimate and quantitative `A -> antagonism` effect-size coverage remains thinner than the direction-level recurrence.

**Interpretation:** the prediction that attraction is not mutualist-exclusive is recurrent across modalities, but needs more quantitative cross-study support.

## U3 — defensive efficacy

**Status: RECURRENT_STRONG at the route level**

`D -> antagonism` is represented by **18 independent biological clusters** and spans chemical and multiple physical/access mechanisms, including sticky/slippery surfaces, hairs, liquid barriers, and bract/access structures.

Independent manipulations repeatedly show antagonist deterrence/access reduction in systems including `Bejaria`, `Erica`, `Pedicularis`, slippery-perianth systems, `Menyanthes`, `Thunia`, and `Chrysothemis`.

**Interpretation:** flower-specific antagonist-reducing traits are not a one-mechanism phenomenon; defensive efficacy recurs across mechanistically distinct implementations.

## U4 — pollinator interference is conditional

**Status: CONDITIONAL_RECURRENT**

`D -> pollination` occurs in **10 independent clusters**, but the state is not uniformly negative.

Negative/interference-compatible examples include high 2PE in `Polemonium`, gelsemine in `Gelsemium`, extended-exposure cardenolides in `Asclepias`, and nectar repellents in `Nicotiana` on handling/residence-type outcomes.

Null/preserved-function examples include moderate 2PE states, `Ipomopsis` robber resistance without detected hummingbird deterrence, `Pedicularis` pollinator-null states, `Catalpa` thief deterrence without detected tested-pollinator consumption cost, and `Thunia` behavioural routing where arrival frequency is near-null while legitimate function changes strongly.

**Interpretation:** a universal negative defence-to-pollinator rule is contradicted by recurrent same-system and cross-system null/preserved-function states. The next question is which moderator explains the split.

## U5 — interaction selectivity / guarded defence

**Status: RECURRENT_QUANTITATIVE_PROVISIONAL; highest-priority universality test**

The same higher-level state now has **three independent matched numeric anchors across distinct defence implementations**:

1. `Catalpa speciosa` — chemical **consumer selectivity**. Nectar iridoids strongly suppress two potential-thief assays (`LRR=-1.2742`, `SE=0.2291`; `LRR=-0.9430`, `SE=0.2344`) while tested legitimate-pollinator consumption is approximately unchanged (`LRR=-0.0102`, `SE=0.0187`).
2. `Pedicularis rex` — physical **attack-mode selectivity**. The water barrier strongly reduces seed predation (`treatment beta=-0.072`, `SE=0.007`) while nectar-robber visitation (`-0.014`, `SE=0.225`) and legitimate pollinator visitation (`+0.012`, `SE=0.224`) are null-compatible; robbers bypass the barrier by piercing above the water.
3. `Thunia alba` — physical **functional-mode selectivity**. Intact bracts strongly reduce robbery (`LRR=-1.7663`, `SE=0.2039`), leave hourly arrival nearly unchanged (`LRR=+0.0370`, `SE=0.1630`), and increase pollinia removal (`+1.2953`, `SE=0.2532`), deposition (`+1.1520`, `SE=0.3532`), and fruit set (`+1.2556`, `SE=0.4207`). The same `Bombus` changes ecological function after bract removal.

`Ipomopsis aggregata` adds an independent observational replication: dilute nectar is associated with less robbing without a detected direct hummingbird deterrence effect, but it is not promoted into the manipulation-based matched quantitative registry.

The recurrence is therefore no longer supported only by direction counts and is not restricted to one chemical compound, one physical mechanism, or one pollinator guild.

**What is still missing:** these anchors cannot yet be collapsed into a formal cross-study effect or moderator meta-regression because their outcomes, link functions, sampling structures, and within-study covariance differ. A synthetic subtraction would manufacture precision.

**Interpretation:** interaction selectivity is now a quantitatively replicated candidate switching principle. The remaining test is whether additional matched systems preserve this higher-level state and whether enough scale-compatible contrasts can be recovered to test selectivity as a moderator rather than only as a replicated mechanism class.

## U6 — recurrent state transitions

**Status: RECURRENT_STRONG descriptively / CONDITIONAL_RECURRENT quantitatively**

Seventeen independent context/sign-switch clusters plus seven context-only programs repeatedly place transitions on a limited set of axes:

```text
consumer identity or function
dose / expression intensity
resource / exposure context
tissue / attack mode
response stage
space / time / access geometry
population / site
lifecycle stage
```

These are not isolated one-off moderators. Similar transition logic recurs across chemically and physically different systems.

**Interpretation:** heterogeneity is structured rather than purely idiosyncratic, but several axes still lack sufficient compatible effect sizes for a single moderator model.

## U7 — direct A x D sign

**Status: UNIDENTIFIED / WEAK**

One strict direct cluster is retained (`Impatiens capensis`), with reproductive-component interaction estimates whose confidence intervals overlap zero and whose point directions are not stable enough to define a general sign.

**Interpretation:** marginal recurrence cannot be used to fill this gap. The direct complementarity/substitutability sign remains empirically unresolved.

## U8 — direct joint cost

**Status: UNIDENTIFIED**

No strict direct joint-cost estimate is currently available.

**Interpretation:** `kappa` remains unidentified, not zero.

## Current universality picture

The strongest empirical structure is now sharper than generic context dependence:

> Attraction signals are repeatedly available to both mutualists and antagonists, while flower-specific defence repeatedly reduces antagonist access through diverse mechanisms. Whether that defence also suppresses legitimate pollination is conditional. Across independent chemical and physical systems, consumer-, attack-mode-, and functional-mode-selective defences repeatedly preserve legitimate pollination while reducing antagonistic use. Interaction selectivity is therefore a quantitatively replicated candidate axis separating complementarity-favouring from substitution-favouring states.

This is **not yet a proven universal law of `W_AD`**. The matched evidence concerns constituent routes, and direct `A x D` plus joint-cost evidence remains sparse or absent.

## Remaining scientific tasks, in order

1. Continue the 10-cluster matched-defence queue and recover both routes numerically for `Gelsemium`, `Polemonium`, `Asclepias`, `Nicotiana`, `Aconitum`, and the remaining systems where source structure allows it.
2. Keep manipulation-based quantitative anchors separate from observational replications and from source-model coefficients unless a common effect scale is defensible.
3. Determine whether at least one outcome lane reaches enough independent matched systems for a formal selectivity moderator/meta-regression; if not, document the exact missing covariance/effect cells.
4. Expand quantitative `A -> antagonism` coverage across signal modalities.
5. Run a targeted direct-design search for factorial/shared-unit `A x D` studies and strict joint-cost estimates.
6. Recompute U1-U8 statuses after each targeted batch; stop only when statuses stabilize or the missing design cells are exhaustively documented.

## Current scientific stop decision

```text
class saturation:                    reached
mechanism-first universality audit:  active
matched selectivity anchors:         3 independent numeric systems
selectivity moderator meta-analysis: not yet identified
U5 status:                           RECURRENT_QUANTITATIVE_PROVISIONAL
direct A x D:                        unresolved
direct joint cost:                   unidentified
scientific evidence work:            CONTINUE
```
