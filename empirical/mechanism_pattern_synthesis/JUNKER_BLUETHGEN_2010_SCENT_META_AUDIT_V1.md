# Junker & Blüthgen 2010 floral-scent cross-synthesis audit v1

## Source

Junker RR, Blüthgen N. **Floral scents repel facultative flower visitors, but attract obligate ones.** *Annals of Botany* 105:777–782. DOI `10.1093/aob/mcq045`.

Primary article is available via Oxford Academic / PubMed Central.

## Pattern question

Can an independent synthesis universe reproduce consumer-dependent responses to floral volatiles?

This is a useful replication target for the current Sasidharan 2023 module, but the grouping variable differs:

```text
Junker & Blüthgen: obligate vs facultative floral-resource users
Sasidharan:         pollinator vs florivore roles
```

These categories overlap biologically but are not interchangeable.

## Data architecture

The published meta-analysis includes:

```text
18 publications
425 observations
83 individual substances from 7 chemical classes
floral scent bouquets from 31 plant species
24 obligate visitor species
16 facultative visitor species
```

Most obligate visitors were putative pollinators, but thrips were also included and their plant effect can be ambiguous.

Facultative visitors included ants, herbivorous beetles/bugs, and generalist Diptera. They were mainly antagonistic but the source explicitly warns that consumer dependency is not identical to the plant-centred mutualist/antagonist classification.

## Inclusion / effect treatment

The source included studies that contrasted a floral volatile against a scentless control and reported variance information for experimental and control conditions.

The published analysis uses weighted response metrics and explicitly addresses non-independence in two ways:

1. the full observation-level analysis;
2. a sensitivity analysis reducing each study to a single mean response per dependency category.

The study-reduced analysis still found a significant obligate/facultative difference (`F_1,18 = 4.9`, `P = 0.04`; study-category n = 13 obligate and 7 facultative).

## Published Pattern

The source reports:

- obligate flower visitors were on average attracted to floral scent;
- facultative flower visitors were on average negatively affected/repelled;
- negative effects on facultative visitors were much larger than the remaining response classes;
- the dependency contrast remained after removing toxicity tests;
- the dependency contrast also remained in trap-only data;
- assay design strongly affected response magnitude.

Thus the synthesis contains both a consumer-dependence Pattern and a methodological-context Pattern.

## Theory-facing mapping

Admitted Pattern classes:

```text
consumer dependency / functional role
shared floral-signal filtering
assay / response-context dependence
```

The module independently supports the broader idea that the same floral chemical space can be attractive to one consumer class and defensive/repellent to another.

## Critical classification boundary

Do **not** relabel:

```text
obligate visitor = pollinator
facultative visitor = antagonist
```

as deterministic identities.

The source itself notes exceptions and emphasizes that net mutualistic/antagonistic outcome can vary with the focal interaction. Accordingly, this module is stronger as a replication of **consumer-dependence** than as a direct estimate of `A -> pollinator` versus `A -> antagonist` effects.

## Relation to Sasidharan 2023

The two syntheses are not duplicate analyses.

Junker & Blüthgen asks whether dependency on floral resources predicts the sign of responses to scents. Sasidharan asks how pollinators and florivores respond to individual floral VOCs and shows strong study/compound composition limits.

Convergence between them would strengthen the Pattern class:

> floral volatile effects are consumer-dependent rather than universally attractive or repellent.

Differences between them are also informative because the role taxonomies and included study universes differ.

## Current adjudication

```text
primary source verified:        PASS
quantitative meta-analysis:     PASS
study-dependence sensitivity:   PASS
consumer-dependence axis:       DISTINCT AND RELEVANT
mutualist/antagonist identity:   PARTIAL, NOT EXACT
raw supplement reproduction:    NOT YET
current-ledger overlap audit:    NOT YET
```

### Decision

**ADMIT_AS_CROSS_SYNTHESIS_REPLICATION_CANDIDATE**

Promote to the manuscript only after overlap with Sasidharan/current route ledgers is documented and the supplementary study/species table is reconstructed far enough to quantify role-category composition.

## Conservative manuscript-ready claim if promoted

> An earlier independent meta-analysis of 18 publications and 425 floral-scent response observations found contrasting average responses between obligate and facultative floral-resource users, and the contrast persisted when data were reduced to study-level means. Because floral-resource dependency does not map perfectly onto mutualistic versus antagonistic plant effects, this result is best treated as independent evidence for consumer-dependent floral-signal filtering rather than a direct pollinator-versus-antagonist effect.
