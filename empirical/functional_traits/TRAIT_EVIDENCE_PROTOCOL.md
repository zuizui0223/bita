# Functional-trait evidence protocol

## Purpose

The first theory-plus-global-data study will not treat all visible plant
characters as interchangeable defence traits. A candidate trait is retained only
when its **organ**, **putative function**, **consumer context**, **evidence
strength**, and **global-data availability** are recorded separately.

The active question is:

```text
How do mutualist and antagonist interaction regimes associate with
functionally interpretable plant-trait modules?
```

It is not:

```text
Which arbitrary collection of floral and leaf measurements can be collapsed into
one attraction score and one defence score?
```

## Evidence grades

| Grade | Meaning | Eligible model role |
|---|---|---|
| A | Direct manipulation or quantitative synthesis supports the trait--interaction mechanism in the relevant organ and consumer context. | Candidate primary module after coverage audit. |
| B | Repeated observational or comparative support, but no direct causal test in the relevant context. | Candidate secondary module; sensitivity analysis only. |
| C | Plausible mechanism but limited, conflicting, or taxonomically narrow support. | Hold; do not make a global main-effect claim. |
| U | Functional meaning is unresolved or multiple incompatible mechanisms remain. | Exclude from v1 model. |

A high evidence grade alone is insufficient. A trait also needs record-level
provenance, interpretable units, and enough coverage among plants in the network
backbone.

## Functional modules

### 1. Floral attraction and access: `A_flower`

This module includes traits that can alter pollinator detection, approach,
handling, or reward access:

- individual flower or capitulum size;
- inflorescence display size and flower number;
- floral depth, width, and accessibility;
- nectar quantity or sugar reward where measured;
- colour/contrast and scent only when they are direct measurements, not
  pollination-syndrome labels.

The empirical analyses retain these traits separately or as a predeclared,
source-supported submodule. They are never silently converted into a universal
"attractiveness" score.

### 2. Floral / reproductive-structure resistance: `B_flower`

This module is for barriers or deterrents located on flowers, inflorescences,
capitula, bracts, or reproductive structures, such as:

- involucral or bract spine density;
- bract toughness or structural barriers;
- floral trichomes;
- sticky secretions around reproductive structures;
- floral chemistry with an explicit florivore or seed-predator endpoint.

`B_flower` is the only defensive module that can enter the direct
attraction--defence interaction in the current score without an additional
bridge, because it can both reduce florivory and obstruct pollinator access.

### 3. Leaf resource quality: `Q_leaf`

This is not called defence by default. It represents leaf construction and
nutritional quality that can alter herbivore performance or choice:

- specific leaf area / leaf mass per area;
- leaf dry-matter content;
- leaf nitrogen concentration;
- leaf phosphorus concentration;
- carbon:nitrogen ratio when both measurements are available;
- leaf thickness.

These traits are often available across broad taxonomic scopes, but their effects
on herbivory can vary by herbivore guild and plant lineage. They therefore enter
as leaf-quality predictors, not as proof of resistance.

### 4. Leaf structural or chemical resistance: `B_leaf`

This module includes traits with a direct barrier or deterrence interpretation:

- leaf toughness or force-to-punch;
- trichome density/type;
- spine or prickle density;
- latex, resin, sticky exudates, or equivalent surface barriers;
- measured defensive compounds, only within chemically comparable clades or
  explicitly harmonised assays.

Availability of these records is expected to be patchier than `Q_leaf`; therefore
v1 treats them as conditional modules rather than assuming they can support a
single global analysis.

## Exclusions from the first model

| Trait family | Reason for exclusion from v1 |
|---|---|
| Leaf mottling / variegation | Visual pattern may affect herbivore detection, light use, physiology, or be a developmental by-product; functional direction is not established generally. |
| Leaf shape, lobing, area, or architecture | May affect exposure and microclimate, but are not resistance traits without an identified herbivore mechanism. They are covariates or future exposure modules. |
| Stem / wood traits | Wood density, bark, stem chemistry, and stem borers such as Cerambycidae constitute an organ-specific model, not a leaf-defence extension. |
| Nest-material suitability | Leaf-cutting bee use concerns cutting, transport, and nest-material performance; it is not automatically herbivory or defence. |
| Pollination syndrome | It encodes the interaction domain to be explained and is circular as a predictor of pollination-network structure. |

## Literature-first decision rule

A candidate trait advances from the evidence matrix into a primary v1 analysis
only if all conditions hold:

1. its functional mechanism has grade A or strong grade B support;
2. the affected organ and consumer layer are compatible;
3. the trait is directly observed or has a documented, non-circular proxy;
4. its unit can be harmonised across sources;
5. it reaches the network-backbone coverage threshold in the source audit; and
6. its inclusion was decided before fitting the focal interaction model.

Candidates that fail only the availability criterion remain biologically
interesting but are not used to claim absence of an effect.

## Relation to the simulation

The current model is deliberately more abstract than the data. Its variables are
functional channels, not mandatory one-to-one trait scores:

```text
A_flower  = floral attraction / access channel
B_flower  = floral barrier / florivore-resistance channel
Q_leaf    = leaf resource-quality channel
B_leaf    = leaf structural or chemical resistance channel
```

The existing `A`--`D` cross-partial applies most directly to `A_flower` and
`B_flower`. A relation between `A_flower` and either leaf channel needs an
explicit shared-cost, developmental, or herbivore-mediated bridge; it must not
be inferred merely because the traits co-occur in the same plant.

## Core literature seeds

These are starting points for the evidence matrix, not a claim that every
mechanism generalises globally.

- Carmona, D., Lajeunesse, M. J. & Johnson, M. T. J. (2011). *Plant traits that
  predict resistance to herbivores*. Functional Ecology 25, 358--367.
- Hanley, M. E., Lamont, B. B., Fairbanks, M. M. & Rafferty, C. M. (2007).
  *Plant structural traits and their role in anti-herbivore defence*.
  Perspectives in Plant Ecology, Evolution and Systematics 8, 157--178.
- McCall, A. C. & Irwin, R. E. (2006). *Florivory: the intersection of
  pollination and herbivory*. Ecology Letters 9, 1351--1365.
- Pérez-Harguindeguy, N. et al. (2013). *New handbook for standardised
  measurement of plant functional traits worldwide*. Australian Journal of
  Botany 61, 167--234.
- Kattge, J. et al. (2020). *TRY plant trait database -- enhanced coverage and
  open access*. Global Change Biology 26, 119--188.
