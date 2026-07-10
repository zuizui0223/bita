# Manuscript skeleton v1

## Working title

Conditional attraction–defence regimes in flowers: a formal framework, evidence map,
and an *Impatiens capensis* empirical case study

## One-sentence contribution

This manuscript shows that attraction and defence/access traits need not be a fixed
trade-off or fixed synergy: their relationship depends on pollination costs,
antagonism-suppression benefits, and shared costs; available literature supports
only part of this structure, while a linked *Impatiens* case study reveals a
pollination-cost-like floral chemistry association and a randomized cost of imposed
florivory on fruit production.

## Paper architecture

```text
Part A: formal theory
Part B: literature evidence map and limits of pooled inference
Part C: Impatiens empirical case study
Part D: synthesis and future empirical design
```

## Abstract skeleton

### Background

Flower attraction traits can increase pollinator service but may also increase
detection by antagonists. Defence or access-restriction traits can reduce floral
damage, but may impose pollination costs. These opposing routes imply that
attraction and defence should not be expected to show a universal trade-off or a
universal positive association.

### Theory

We derive a conditional framework in which the sign of the attraction–defence
interaction depends on the product of attraction-mediated antagonism and defence-
mediated antagonism suppression, the product of attraction-mediated pollination
benefit and defence-mediated pollination cost, and any shared cost of expressing
both trait modules.

### Evidence synthesis

A literature evidence map shows that directly comparable effect estimates are too
sparse and heterogeneous for a universal pooled four-arrow meta-analysis. The
clearest directional literature support is that defence/access traits can reduce
pollinator use in some chemical-barrier systems.

### Empirical case study

Using a title-validated *Impatiens capensis* archive, we fit response-scale models
linking early flower redness and floral condensed tannins to pollinator use,
natural floral damage, and reproductive components, and separately estimate
randomized effects of supplemental robbing, florivory, and pollination.

### Results

The floral-tannin candidate was negatively associated with pollinator use, but did
not show a resolved protective association with natural floral damage. Flower
redness and the A × D candidate seed surface were unresolved. In contrast,
randomized imposed florivory reduced chasmogamous fruit production.

### Conclusion

The framework is best treated as a conditional identification problem rather than a
search for universal attraction–defence effects. Current evidence supports some
cost and downstream-damage components but does not yet identify the full
complementarity/substitutability regime.

## Introduction outline

1. Start with the biological problem: flowers are simultaneously signals to mutualists
   and resources/targets for antagonists.
2. State the conceptual failure of simple expectations: attraction and defence need
   not be universally opposed or universally coupled.
3. Introduce the conditional framework: attraction, defence, pollination benefit,
   antagonism cost, and shared cost.
4. State why existing literature is hard to pool: different trait classes, outcome
   units, effect metrics, and designs.
5. Present the empirical pivot: rather than forcing a universal meta-analysis, use a
   linked *Impatiens* panel to demonstrate what can and cannot be identified in one
   system.

## Methods outline

### Formal model

Use the fixed Part A expression and explain each term in biological language. Do not
introduce new parameters beyond the established framework.

### Evidence map

Describe the literature synthesis as an evidence map and compatibility audit. State
that effect pooling requires compatible trait class, outcome class, effect metric,
design, and independent clusters. Present the failure to obtain a universal pooled
parameter as a result about literature structure, not a failed analysis.

### Empirical archive

Use the *Impatiens capensis* Dryad archive. Emphasize title validation, raw-in-memory
reanalysis, and aggregate-only outputs.

### Response-scale channel models

Describe:

```text
pollinator use: robust Poisson mean model on 60-minute-standardized visit counts
natural floral damage: flower-level fractional-logit model with plant-cluster robust SE
seed component: CH-fruit count model with plant-cluster robust SE
```

State that flower redness and floral tannins are observational predictors.

### Pollinator hurdle sensitivity

Describe as post-primary adequacy sensitivity prompted by zero mass and
overdispersion, not model selection.

### Randomized factorial treatment models

Describe the complete 2×2×2 `Robbing × Florivory × Pollination` assignment, effect
coding, full interaction retention, and pre-treatment phenology adjustment.

## Results outline

### R1. Literature map constrains generality

- Universal pooled four-arrow meta-analysis is not currently justified.
- `c_D`-like pollinator cost from chemical barriers is the clearest cross-study
  directional support.
- Many candidate `d_A` routes fail because they are abstract-only, reverse-route,
  fruit-set predictor, or otherwise not direct trait-to-antagonism models.

### R2. Impatiens response-scale channel map

Use numbers from `IMPATIENS_RESULTS_LOCK_V1.md`.

Key sentence:

> The tannin candidate showed a pollinator-cost-like association but did not show a
> resolved natural-florivory suppression benefit.

### R3. Pollinator rate is zero-heavy

Report that the primary model has 52/81 zero observations and high Pearson
dispersion, motivating hurdle sensitivity. Do not replace primary result.

### R4. Randomized florivory reduces fruit component

Report the full-factorial imposed florivory result for CH fruits/day and the strong
phenology association.

### R5. Channel ledger

Use `IMPATIENS_CHANNEL_LEDGER.svg` as the main empirical figure.

## Discussion outline

### D1. What is supported

- Defence/access traits can carry pollination costs.
- In *Impatiens*, a floral-tannin candidate is associated with lower pollinator use.
- Imposed florivory can reduce chasmogamous fruit production.

### D2. What is not supported or not identified

- No resolved protective tannin association against natural floral damage.
- No resolved flower-redness route to pollination or antagonism.
- No resolved A × D reproductive-component surface.
- No total-fitness mixed partial or shared-cost estimate.

### D3. Why this matters

The result is not a weak null; it shows which parts of the theoretical regime are
visible in one linked empirical system and which parts require direct manipulation,
higher precision, or different designs.

### D4. Future data design

Recommend future studies that jointly manipulate or measure attraction, defence,
pollination, antagonism, and total fitness in the same individuals, with phenology
as a central axis.

## Core figures and tables

```text
Figure 1: Part A conceptual/regime diagram.
Figure 2: Literature evidence-map summary and compatibility gaps.
Figure 3: Impatiens channel ledger SVG.
Table 1: Literature channel support and insufficiency table.
Table 2: Impatiens response-scale channel coefficients.
Table 3: Randomized factorial reproductive-component coefficients.
Supplement: archive audit, variable definitions, treatment-cell audit, hurdle sensitivity.
```

## Final claim boundary

The manuscript should end with:

```text
Attraction–defence complementarity remains a conditional theoretical possibility,
but current empirical evidence identifies only parts of the route structure. The
Impatiens case shows a pollination-cost-like chemistry association and an
experimental cost of floral damage, while the protective benefit and A×D fitness
surface remain unresolved.
```
