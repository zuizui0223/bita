# Sakhalkar 2023 BITA network reanalysis protocol v1

## Status

Registered on the BITA feature branch before reading the output of the new BITA-specific network analysis workflow.

This analysis is an **independent macro-ecological validation lane**. It does not increment the matched-D study count and it does not replace the source publication's RLQ/RDA analyses.

## Source

Sakhalkar et al. 2023, *Ecosphere*, DOI `10.1002/ecs2.4696`.

Public reproducibility source:

- Zenodo DOI `10.5281/zenodo.8398202`;
- public source repository `SaileeSakhalkar/cheaters-among-pollinators-ecosphere`;
- focal workbook `input/cheaters_visitation_and_trait_data.xlsx`;
- source analysis `scripts/cheaters_analysis.R`.

The source R script reads:

```text
sheet = cheater_data
sheet = plant_traits
```

and excludes records with `behavior == "visiting"`.

## BITA question

Does floral access architecture route exploitation mode across a whole plant–visitor community?

The source paper reports that long/specialized flowers reduce thieving but are more susceptible to robbing. BITA translates that into one predeclared directional test.

## Primary estimand

For each plant species (i), sum source `freq_fm_per_species` separately over:

```text
R_i = robbing frequency
T_i = thieving frequency
```

For species with (R_i + T_i > 0), define

```text
cheating_mode_balance_i = (R_i - T_i) / (R_i + T_i)
```

Interpretation:

```text
-1 = entirely thieving
 0 = balanced robbing/thieving
+1 = entirely robbing
```

The primary statistic is Spearman's rho between plant `tube_length` and `cheating_mode_balance`.

### Frozen prediction

```text
rho > 0
```

Longer tubes should shift exploitation from thieving toward robbing.

## Inference

- species is the aggregation unit;
- only plant species with a finite `tube_length` and at least one robbing or thieving frequency enter the primary correlation;
- Spearman rho is tested by a two-sided permutation test;
- permutations = 9,999;
- random seed = 20260919;
- no alternative trait is substituted as the primary predictor after results are observed.

## Descriptive companion quantities

Report without treating them as independent confirmatory tests:

- raw source row count;
- row count after the source-script `visiting` exclusion;
- counts by behavior;
- number of visited plant species;
- number with matched tube length;
- number with robbing;
- number with thieving;
- median tube length among robber-only species;
- median tube length among thief-only species.

## Claim ceiling

This lane can support:

> access geometry predicts which cheating route is used across a plant–visitor community.

It cannot by itself support:

- causal evolution of tube length;
- floral defence efficacy in the narrow conventional-defence sense;
- pollinator preservation/cost;
- a direct attraction-by-defence interaction;
- prevalence outside the sampled community.

The matched-D synthesis remains the primary test of defence selectivity; this network analysis is an independent scale-up of the access-domain mechanism.
