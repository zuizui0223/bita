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
BITA species-level reanalysis: PASS
```

## BITA reanalysis result

A successful GitHub Actions run `35365789840` retrieved the public Zenodo archive, read the source workbook, reproduced the source-script cleaning rule that excludes `behavior == "visiting"`, aggregated normalized cheating frequencies to plant species, and then tested the predeclared access-routing contrast.

Observed aggregate structure:

```text
raw cheater_data rows:      18,440
rows after visiting filter: 14,383
touching records:           13,348
robbing records:               731
thieving records:              304

visited plant species:         183
trait-matched species:         182
species with robbing:           26
species with thieving:          39
species with cheating + tube length: 57
```

The 14,383 filtered rows are eight fewer than the 14,391 visits stated in the paper summary. The repository reanalysis reports the deposited workbook as it exists now and does not silently force the published count.

For the 57 plant species with at least one robbing/thieving frequency and measured tube length:

```text
cheating-mode balance =
    (robbing frequency - thieving frequency)
    / (robbing frequency + thieving frequency)

Spearman rho = 0.346786
two-sided permutation p = 0.0086
permutations = 9,999
seed = 20260919
```

The positive association means increasing tube length shifts cheating toward **robbing** relative to **thieving**.

A second descriptive contrast points in the same direction:

```text
median tube length, robber-only species = 2.0893
median tube length, thief-only species  = 0.6766
```

Thus robber-only plants have roughly threefold greater median tube length in the deposited trait scale.

## Ecological interpretation

This is an independent community-scale result, not another matched-D replication:

> **Floral access geometry predicts which cheating route is realised. Longer, less directly accessible flowers shift exploitation from entry through the legitimate floral opening toward bypass through nectar robbing.**

That result provides a macro-ecological bridge to the matched-D defence corpus. In both layers the key object is not “physical versus chemical” defence but whether a consumer can use the legitimate access domain, is blocked by it, or bypasses it.

## Statistical boundary

The BITA statistic is a species-level aggregate association, not a causal manipulation. It deliberately avoids treating the 14,383 visit records as independent replicates.

It does not estimate a direct pollinator cost, `rho/iota/kappa`, or the prevalence of defence selectivity. Its role is independent validation of the **access-routing mechanism** at community scale.

Machine-readable result:

`empirical/floral_defence_selectivity/results/sakhalkar2023_network_result.json`
