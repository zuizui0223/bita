# BITA Peucedanum Dryad import contract v1

## Purpose

`Peucedanum multivittatum` is treated as a **Japan-accessible observational / field anchor for partial functional differentiation**, not as a substitute for the canonical SCH -> BITA `R_state` experiment.

Two public Dryad datasets are currently registered:

```text
2021 Ecology and Evolution dataset
DOI: 10.5061/dryad.b5mkkwhcq
file: Kudo&Shibata_Ecol&Evol_DataSet.xlsx

later Peucedanum dataset
DOI: 10.5061/dryad.w3r2280v5
files:
  Data1_FloralGender.xls
  Data2_basedata20-21.xls
  Data3_FitnessAnal.xls
  README.md
```

The repository does **not** assume the original spreadsheet column names. The Dryad workbooks must first be inspected and mapped manually to the normalized contracts below.

## Normalized population table

Template:

```text
empirical/identification_design/PEUCEDANUM_POPULATION_PATTERN_TEMPLATE_V1.csv
```

Required fields:

```text
dataset_id
source_doi
year
population_id
mean_flowering_day
male_flower_mean
perfect_flower_mean
male_fraction
fruit_set_mean
seed_predation_rate
n_plants
```

Rules:

- `male_fraction = male flowers / (male + perfect flowers)` on the same aggregation basis used for the two flower-count means;
- `seed_predation_rate` and `fruit_set_mean` must be proportions on `[0,1]`;
- `mean_flowering_day` must use one consistent day scale within each dataset;
- no values are back-calculated from figures if the raw workbook provides the source values;
- source-specific missing values remain missing and must not be silently imputed.

## Registered observational estimands

The first-pass population analysis asks whether the published geographic pattern is recoverable without claiming causality:

```text
rho_1 = rank correlation(male_fraction, seed_predation_rate)
rho_2 = rank correlation(mean_flowering_day, seed_predation_rate)
rho_3 = rank correlation(perfect_flower_mean, seed_predation_rate)
rho_4 = rank correlation(male_flower_mean, seed_predation_rate)
```

Expected biological pattern from the published studies:

```text
rho_1 > 0    male-biased allocation is associated with stronger predation contexts
rho_2 < 0    later flowering is associated with lower predation pressure
```

The signs of `rho_3` and `rho_4` are treated as dataset-specific because individual-level and population-level associations differ in the source studies.

## Claim ceiling

A positive normalized-data receipt supports only:

```text
OBSERVATIONAL_GEOGRAPHIC_PARTIAL_DIFFERENTIATION_PATTERN
```

It does **not** identify:

```text
causal dimensional release
R_state
preferential loading caused by a manipulation
historical origin of andromonoecy
ancestral shared-trait -> differentiated-trait transition
```

## Promotion path

To move beyond the observational anchor:

1. validate a manipulation of male:perfect flower allocation while holding total display approximately constant;
2. measure pollinator visitation / pollen export or siring success;
3. measure oviposition, seed predation and intact-seed female fitness;
4. test whether changing flower-class allocation reduces antagonistic cost while retaining male-function performance.

This is a **partial differentiation experiment**, separate from the canonical Pedicularis `R_state` lane.
