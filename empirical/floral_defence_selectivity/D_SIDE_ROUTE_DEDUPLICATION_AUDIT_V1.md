# D-side route-level macro deduplication audit v1

## Purpose

Before promoting the legacy 56-route ledger into a broader macro-comparative analysis, re-check the independence grain of all D-side study clusters.

The legacy mechanism-first readout reported:

```text
D -> antagonism clusters = 18
D -> pollination clusters = 10
```

The current audit finds one duplicate study identity in the D -> antagonism lane.

## Duplicate detected

DOI:

```text
10.1093/aob/mcaa168
```

appears under two independence-cluster labels:

```text
Takeda_Kadokawa_Kawakita_2021
Takeda_2021_slippery_perianths
```

Both labels contain the same two source systems:

```text
Codonopsis lanceolata
Fritillaria koidzumiana
```

and the same slippery-perianth ant-entry experiment.

The duplicate arises because the study entered the canonical ledger once through an earlier ledger batch and again through a later expansion ledger.

## Corrected macro-analysis grain

For route-level macro analysis, cluster identity is collapsed at the primary study-program DOI when the same experiment has been duplicated across ledger-ingestion paths.

Therefore:

```text
legacy D -> antagonism cluster labels: 18
unique D -> antagonism study programs: 17

D -> pollination study programs:        10
```

The old ledger is not deleted or rewritten because it remains provenance for historical analyses. The new macro layer explicitly deduplicates the duplicate pair.

## Consequence for previous language

Any new manuscript text should use:

> **17 unique study programs with admitted D-to-antagonism evidence**

rather than “18 independent D-to-antagonism clusters”.

Historical files that state 18 are retained as provenance but should not be used as the current independence count.

## Claim boundary

The 17-study D-to-antagonism corpus is strongly selected by the D-role admission criterion itself.

It can support:

- implementation breadth;
- consumer/guild breadth;
- mechanism-coordinate breadth;
- coverage of pollinator-side follow-up;
- conditionality structure.

It cannot provide an unbiased estimate of:

> the probability that an arbitrary flower-associated trait is an effective defence.

Testing defence efficacy prevalence would require a denominator of candidate D traits screened independently of antagonist outcome.
