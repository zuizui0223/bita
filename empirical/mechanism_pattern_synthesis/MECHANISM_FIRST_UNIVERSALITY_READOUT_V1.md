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

Quantitative support is strongest here.

Leal et al. 2025 gives negative pooled log-response-ratio effects for:

```text
female reproductive success  -0.210  (48 independent clusters)
nectar standing crop          -0.483  (28)
legitimate visitation         -0.291  (22)
```

Under REML + modified Hartung-Knapp sensitivity, female fitness and nectar remain clearly below zero; legitimate visitation remains negative but its upper interval endpoint nearly touches zero.

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

Negative/interference-compatible examples include high 2PE in `Polemonium`, natural-range gelsemine in `Gelsemium`, extended-exposure cardenolides in `Asclepias`, and nectar repellents in `Nicotiana` on handling/residence-type outcomes.

Null/preserved-function examples include moderate 2PE states, `Ipomopsis` robber resistance without detected hummingbird deterrence, `Pedicularis` pollinator-null states, `Catalpa` thief deterrence without detected tested-pollinator consumption cost, and `Thunia` behavioural routing where arrival frequency need not increase while legitimate function changes.

**Interpretation:** a universal negative defence-to-pollinator rule is contradicted by recurrent same-system and cross-system null/preserved-function states. The next question is which moderator explains the split.

## U5 — interaction selectivity / guarded defence

**Status: RECURRENT_PROVISIONAL; highest-priority quantitative test**

Independent guarded/selective states recur across distinct mechanism classes:

- physical/access selectivity: `Pedicularis`;
- chemical consumer selectivity: `Catalpa`;
- temporal ant exclusion: `Acacia/Vachellia` context program;
- visitor functional-mode routing: `Thunia`;
- additional same-system resistance-without-detected-pollinator-cost states such as `Ipomopsis` strengthen the candidate class.

The recurrence is therefore not restricted to one chemical compound or one pollinator guild.

But no formal matched-study moderator meta-analysis yet shows that selectivity systematically predicts a larger antagonist-benefit / pollinator-cost contrast.

**Interpretation:** this is currently the strongest candidate universal *switching principle*, but it remains a prediction awaiting quantitative matched-route testing.

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

The strongest empirical structure is no longer merely:

> recurrent mechanisms + context-dependent balance

A sharper working synthesis is now justified as a **candidate to test**:

> Attraction signals are repeatedly available to both mutualists and antagonists, while flower-specific defence repeatedly reduces antagonist access through diverse mechanisms. Whether that defence also suppresses legitimate pollination is conditional. Recurrent guarded/selective defence states suggest that interaction selectivity — consumer, attack-mode, spatial, temporal, or functional — may be a major axis separating complementarity-favouring from substitution-favouring states.

This is **not yet promoted to a proven universal rule** because the matched quantitative selectivity test has not been completed.

## Remaining scientific tasks, in order

1. Build a matched same-study table for all systems with both `D -> antagonism` and `D -> pollination` evidence.
2. Recover compatible numerical effects/uncertainty for both routes wherever possible.
3. Define within-lane oriented selectivity contrasts only where effect scales permit.
4. Test selectivity moderators: chemical/physical, consumer-selective/non-selective, attack-mode, space/time, dose, response stage, pollinator guild.
5. Expand quantitative `A -> antagonism` coverage across signal modalities.
6. Run a targeted direct-design search for factorial/shared-unit `A x D` studies and strict joint-cost estimates.
7. Recompute U1-U8 statuses after each targeted batch; stop only when statuses stabilize or the missing design cells are exhaustively documented.

## Current scientific stop decision

```text
class saturation:                    reached
mechanism-first universality audit:  active
selectivity moderator test:          not yet complete
direct A x D:                        unresolved
direct joint cost:                   unidentified
scientific evidence work:            CONTINUE
```
