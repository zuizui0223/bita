# Targeted search for full attraction–defence channel-identification designs v1

## Question

Does the existing literature already contain a study that combines all of the following in one linked experiment?

1. an independently manipulated attraction axis `A`;
2. an independently manipulated antagonist-reducing defence/access axis `D`;
3. crossed antagonist and pollinator interventions suitable for channel contrasts;
4. a shared outcome allowing `Delta_AD W`;
5. information on the pollinator-absent `A×D` baseline interaction;
6. an independent A×D allocation/construction-cost assay.

This is a targeted high-information search, not a claim of exhaustive literature prevalence.

## Query families

The search combined variants of:

```text
floral attraction defence pollination herbivory full factorial
flower scent defence pollinator herbivore factorial transgenic
pollinator exclusion herbivore exclusion floral trait defence experiment
attraction defence pollinator herbivore trait interaction factorial
```

The aim was to find design structure, not merely papers discussing trade-offs.

## Closest trait-factorial anchor — Kessler et al. 2008

Kessler, Gase & Baldwin (2008; `10.1126/science.1160072`) independently blocked floral benzylacetone and nicotine production in all four combinations. This is the closest current trait-factorial match.

The published female outcrossing aggregate is sign-robustly compatible with a positive discrete A×D interaction. The accessible article reports 601 antherectomized flowers across five days, with 127 flowers on a no-pollinator wind day and 87 mature capsules from the remaining 474 flowers. The exact genotype-by-day values are referenced to supplementary Fig. S8A. Formal A×D uncertainty remains unrecovered, and the nicotine manipulation is systemic.

Most importantly, the study does not independently cross antagonist and pollinator presence/absence with the four trait states. It therefore identifies a trait interaction much more closely than it identifies the channel allocation.

## Closest consumer-factorial anchor — Egan et al. 2021

Egan et al. (2021; `10.1002/evl3.262`) manipulated herbivory presence/absence and pollination open/hand-pollination in a full factorial common-garden experiment in *Fragaria vesca*. The design was explicitly used to estimate herbivore- and pollinator-mediated selection on attraction- and defence-related traits.

This is unusually close on the consumer side, but it fails the complementary side of the new design:

```text
A traits: measured rather than independently manipulated
D traits: measured rather than independently manipulated
several defence metabolites: leaf-derived rather than flower-specific
reported models: trait × consumer context, not manipulated A × manipulated D × G × P
```

Thus Kessler 2008 and Egan 2021 occupy opposite halves of the desired design:

```text
Kessler 2008: strong A×D trait factorial, weak/missing G×P intervention structure
Egan 2021:    strong G×P agent factorial, weak/missing A×D manipulation structure
```

Their complementarity is exactly the empirical gap the new framework exposes.

## Other near designs recovered in the project

- Santangelo et al. 2019: whole-plant HCN defence crossed with herbivory/pollination context and floral-trait interactions, but A is not manipulated and D is not flower-specific.
- Kessler et al. 2015: genuine 2×2 floral phenotype experiment, but the second axis is nectar reward rather than independently justified D.
- Sun & Huang 2015: experimentally clean flower-associated D with consumer selectivity across seed predators versus pollinators/robbers, but no attraction manipulation.
- Soper Gorden & Adler 2018: linked A and D measurements plus observational A×D reproductive terms and randomized interaction-intensity additions, but A/D are not randomized and treatments are not selective consumer exclusions.

## Current result

The targeted search did **not** recover a study that combines the complete required structure in one experiment. The evidence gap is therefore more specific than “no attraction-defence studies exist”. Existing studies occupy different subsets of the design space.

The recurring missing intersection is:

```text
manipulated A×D trait factorial
        +
selective G×P intervention factorial
        +
M0 baseline characterization
        +
independent joint-cost assay
```

This result should be presented as an identification-coverage gap in the screened high-information literature, not as a literature-wide frequency estimate.

## Design implication

The new framework earns its value if it makes the missing intersection operational. A future study should be selected around a system where consumer interventions can be genuinely selective. Physical access barriers, body-size differences, attack-route differences, diel separation, or phenological separation are preferable to broad bags or insecticides that simultaneously alter both consumer channels.

The ideal experiment is therefore not merely a larger factorial. It is a factorial whose interventions have defensible causal selectivity and whose failure of separability is itself estimable through the A×D×G×P interaction.
