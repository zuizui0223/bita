# Network-scale validation candidate — Aubert et al. 2026

## Purpose

Record an independent macro-ecological validation lane for the BITA effective-domain hypothesis without pretending that it is another matched-D study.

## Source

Aubert S, Duchenne F, Tinoco BA, Santander T, Guevara EA, Graham CH. 2026.
**Trait matching affects the probability of nectar robbing in plant-pollinator networks.**
*Oikos* 2026(3):e11552.
DOI: `10.1002/oik.11552`.

Public data deposit:
Dryad DOI `10.5061/dryad.rn8pk0pqx`.

The deposit contains:

```text
Interactions_data_Ecuador.txt
Cameras_data_Ecuador.txt
Plant_traits.txt
README.md
script.R
```

The repository documentation states that interaction rows are independent bird-plant interactions recorded by time-lapse cameras. The published analysis uses three Ecuadorian sites from a broader 18-site camera dataset.

## Why this is valuable for BITA

The study defines two trait-based mechanisms before outcome classification:

```text
trait complementarity = continuous difference between bird bill length and flower tube length
trait barrier         = binary physical-access condition based on bill vs flower tube length
```

The response is whether a bird-flower interaction is legitimate or nectar robbing.

Published result:

```text
nectar robbing = 7% of sampled interactions
robbing concentrated where bird bill < flower tube
trait barrier strongly predicts robbing route
```

This is almost exactly an interaction-level test of the general BITA idea:

> when legitimate access is blocked by trait mismatch, the same consumer can switch from mutualistic access to an antagonistic/cheating route.

## Distinction from the matched-D synthesis

This dataset does **not** provide a manipulated plant defence trait and should not be inserted into the Stage-1/Stage-2 matched-D counts.

Instead it tests a more general mechanism at network scale:

```text
effective access-domain mismatch
-> route switching
-> legitimate interaction versus robbing
```

That makes it a strong independent macro-validation lane, especially because the unit is individual interaction records across a multispecies network rather than one floral case study.

## Planned BITA reanalysis

Primary replication:

1. restrict to the Ecuador sites used by the source study;
2. retain bird-flower interactions with resolved robbing status;
3. reconstruct trait complementarity and binary trait barrier from the deposited data/source script;
4. reproduce the published direction that trait barrier predicts robbing;
5. report bird family/genus and site structure.

BITA-specific extension, only if supported by the deposited variables:

1. test whether the barrier effect differs between hummingbirds and specialised flowerpiercers;
2. test whether the continuous mismatch adds information beyond the binary barrier;
3. estimate route-switch probability with site / species dependence handled explicitly;
4. map the result onto the same `SEPARATED / OVERLAPPED / BYPASS` language used in the matched-D synthesis without changing the original variables.

## Current execution status

Direct anonymous Dryad file-byte access remains blocked in CI, but an accessible public EPHI Zenodo mirror (DOI 10.5281/zenodo.14185547) exposes the underlying Ecuador interaction, camera, plant-trait and hummingbird-trait tables.

BITA therefore completed an **independent all-18-site Ecuador extension** using the source paper's access-mismatch definition rather than claiming an exact three-transect replication.

Status:

```text
source suitability:          PASS
direct Dryad bytes:          BLOCKED_403_IN_CI
public EPHI Zenodo mirror:   PASS
mirror schema/unit audit:    PASS
all-18-site BITA extension:  PASS
role in paper:               SECOND_INDEPENDENT_NETWORK_VALIDATION
```

Frozen extension result:

```text
resolved target interactions: 21,114
trait-matched interactions:   20,572
bird x plant x site units:     1,378
sites:                            18

mean robbery rate:
  flower tube > bill barrier = 0.30698
  accessible                 = 0.08139

difference = +0.22560
pair-site permutation p = 0.0001

Spearman rho[log(T/B), robbery rate] = 0.41826
permutation p = 0.0001

within-site:
  eligible sites = 17
  positive sites = 15
  mean difference = +0.14399
  sign-test p = 0.00235
  site-stratified permutation p = 0.0001
```

This is an independent extension over all 18 Ecuador mirror sites, not an exact numerical replication of the published three-transect Aubert model.

Primary readout:

`AUBERT_ZENODO_EXTENSION_V1.md`

Machine-readable result:

`results/aubert2026_zenodo_extension.json`
