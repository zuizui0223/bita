# Sakhalkar et al. 2023 — independent network validation candidate

## Source

Sakhalkar SP, Janeček Š, Klomberg Y, Mertens JEJ, Hodeček J, Tropek R. 2023.
**Cheaters among pollinators: Nectar robbing and thieving vary spatiotemporally with floral traits in Afrotropical forests.**
*Ecosphere* 14:e4696.
DOI: `10.1002/ecs2.4696`.

Public data and code:

- Zenodo record: `10.5281/zenodo.8398202`
- archive: `SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip`

## Why this is useful for refocused BITA

This is **not** a matched-D experimental study and must not increment the matched-defence cluster count.

It is an independent community-scale validation dataset for the broader access-architecture prediction:

> floral geometry can selectively block one exploitation mode while exposing the flower to another.

The paper records flower visitors across an elevational gradient on Mount Cameroon and classifies interactions as legitimate visits, nectar robbing, or nectar thieving.

Published corpus:

```text
flower visits:          14,391
studied plants:         194
robbing visits:         ~4.3%
thieving visits:        ~2.1%
plants robbed:          29
plants thieved:         39
```

## Published ecological result

The source reports a trade-off across floral architectures:

```text
specialized / long tubes or spurs
    -> restrict thieving through the floral opening
    -> increase susceptibility to nectar robbing through holes

more open / accessible flowers
    -> lower need for robbing
    -> greater opportunity for thieving
```

Thus floral access architecture does not merely change total antagonist pressure. It **routes exploitation mode**.

This is directly relevant to BITA's effective-domain framework because the focal ecological object is whether an animal can access the reward through the legitimate route or must bypass it.

## Relationship to Aubert 2026

The two network datasets test complementary versions of access filtering:

### Aubert 2026 — Northern Andes bird–plant networks

```text
bird bill length relative to flower tube length
-> legitimate access versus nectar robbing
```

### Sakhalkar 2023 — Afrotropical flower-visitor communities

```text
floral specialization / accessibility
-> legitimate use versus thieving versus robbing
```

Together they can provide a geographically and taxonomically independent network-scale test of the proposition that floral access geometry routes mutualistic and antagonistic interaction modes.

## Analysis target

The first reproducibility gate is intentionally modest:

1. retrieve the public Zenodo archive;
2. inventory raw-data and R-code files;
3. identify the interaction and floral-trait tables used in the paper;
4. reproduce published corpus counts where the deposited schema permits;
5. reconstruct trait–behavior associations only after the source's coding is understood.

No row from this dataset is counted as an independent matched-D experiment.

## Claim boundary

This dataset can support:

- community-scale recurrence of access-mediated exploitation modes;
- a geometry/trait association with robbing versus thieving;
- external validation of the access-routing concept.

It cannot by itself support:

- causal defence efficacy;
- direct pollinator cost of a manipulated D;
- `rho/iota/kappa` allocation;
- prevalence of defence selectivity among plant species globally.

## Reproducibility audit completed

The public Zenodo archive was retrieved successfully in GitHub Actions and the workbook/schema were audited without emitting raw biological rows.

Verified primary workbook:

```text
cheaters_visitation_and_trait_data.xlsx

metadata       A1:C41
cheater_data   A1:J18441
species_details A1:C182
plant_traits   A1:K198
```

Thus the primary visitation sheet contains 18,440 data rows before the source-script exclusion of `behavior == "visiting"`, and the trait sheet contains 197 data rows.

The source R script explicitly reads:

```text
sheet = "cheater_data"
sheet = "plant_traits"
```

and uses `tube_length` in both parsimonious cheating-mode models:

```text
robbers: tube_length + shape + tube_width
thieves: brightness + shape + tube_length
```

The BITA reanalysis therefore has a source-defined trait axis and does not need to invent a post hoc geometry variable.

## Current analysis target

The BITA-specific reanalysis now operates at the **plant-species level**, not at the 18,440-row visit level, to avoid pseudoreplication.

For each plant species with tube-length data:

```text
R = summed source-normalized robbing frequency
T = summed source-normalized thieving frequency

cheating-mode balance = (R - T) / (R + T)
```

for species with `R + T > 0`.

The primary external-validation statistic is the species-level Spearman association between tube length and cheating-mode balance, with a fixed-seed permutation test. A positive association means longer/tubular flowers route cheating toward **robbing through a bypass hole**, whereas shorter/more accessible flowers route cheating toward **thieving through the legitimate opening**.

This is deliberately separate from the matched-D causal corpus.

## Current status

```text
public data/code:              VERIFIED AND RETRIEVED
workbook/schema audit:         PASS
source analysis model audit:   PASS
matched-D cluster:             NO
network validation role:       HIGH
BITA species-level reanalysis: IN EXECUTION
```
