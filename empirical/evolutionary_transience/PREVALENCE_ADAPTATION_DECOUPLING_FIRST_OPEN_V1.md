# Prevalence–adaptation decoupling first-open result v1

Status: **FALSIFIED / DO NOT PROMOTE**

Frozen preregistration:
`PREVALENCE_ADAPTATION_DECOUPLING_PREREG_V1.md`

First opened: 2026-10-07

## Data recovered

- EPHI interaction rows: 54,471
- EPHI camera rows: 6,198
- Trochilidae observation rows: 52,429
- eligible clean waypoint units: 5,254
- hummingbird species with zero-inclusive opportunities: 49
- Colwell morphology species: 220
- species with both Colwell triple-filtered bill/hallux traits: 220
- direct EPHI × Colwell species matches entering primary test: **37**
- clingers among matched species: 22
- presumed non-clingers: 15

The analysis used the frozen metadata-informed route rule, clean waypoint ×
temporally available hummingbird opportunity denominator, summed camera hours, and
the preregistered bypass morphology index:

```text
M_bypass =
z(triple-filtered hallux claw)
-
z(triple-filtered exposed culmen)
```

## Primary result

Prediction:

```text
rho(M_bypass, absolute robbery rate)
>
rho(M_bypass, conditional robbery share)
```

Observed:

```text
rho_abs   = +0.07035
rho_share = +0.10227

Delta_rho = rho_abs - rho_share
          = -0.03193
```

The direction is opposite the preregistered prediction.

Species-bootstrap over the paired difference (3,000 deterministic-seed replicates):

```text
median Delta_rho = -0.02718
95% bootstrap interval = [-0.12813, +0.04067]
fraction Delta_rho > 0 = 0.202
```

Thus the data do not support stronger alignment of the bypass morphology with
zero-inclusive absolute robbery rate than with conditional robbery share.

## Frozen clinger-state corroboration

Cliff's delta, clingers minus presumed non-clingers:

```text
absolute robbery rate:
delta_abs = +0.30909

conditional robbery share:
delta_share = +0.34545

delta_abs - delta_share = -0.03636
```

Again, the difference is opposite the prediction.

Descriptively:

```text
median absolute robbery events per 1000 available camera-hours:
clinger     = 0.26834
non-clinger = 0

median conditional robbery share:
clinger     = 0.01132
non-clinger = 0
```

Clingers do show more robbery on both scales, but the absolute-rate contrast is not
stronger than the conditional-share contrast.

## Prespecified sensitivity analyses

### >=10 resolved feeding events

```text
n = 26
rho_abs = +0.17709
rho_share = +0.25303
Delta_rho = -0.07594

Cliff delta_abs = +0.13889
Cliff delta_share = +0.19444
```

### >=20 resolved feeding events

```text
n = 24
rho_abs = +0.18047
rho_share = +0.29580
Delta_rho = -0.11533

Cliff delta_abs = +0.06250
Cliff delta_share = +0.12500
```

### Explicit yes/no piercing only

```text
n = 32
rho_abs = +0.22632
rho_share = +0.29297
Delta_rho = -0.06665

Cliff delta_abs = +0.30000
Cliff delta_share = +0.37500
```

### >1 eligible waypoint

All 37 primary species already passed this filter; result unchanged.

Every frozen sensitivity retains the direction opposite the hypothesis.

## Component diagnostics

```text
triple-filtered hallux:
rho with absolute robbery = +0.23723
rho with robbery share    = +0.24745

triple-filtered culmen:
rho with absolute robbery = +0.01621
rho with robbery share    = -0.01671
```

The morphology-index failure is therefore not an artifact of an obvious cancellation
between a strongly absolute-associated hallux signal and a share-associated bill signal.

## Interpretation boundary

The preregistered claim is **not supported**.

Do not argue that conditional robbery prevalence is more evolutionarily important on
the basis of this result either. The cross-dataset test is small (37 direct matches),
observational, and the Colwell phenotype describes broad clinging/unorthodox feeding
rather than a robbery-exclusive adaptation.

The valid conclusion is narrower:

> In the available Ecuador × Colwell overlap, bypass-associated hummingbird morphology
> is not more strongly associated with zero-inclusive absolute robbery rate than with
> conditional robbery share.

This failure cannot be used to rescue or reject the separate
ecological-stability/evolutionary-transience hypothesis.

## Post-open taxonomy note

Ten EPHI hummingbird names with >=5 resolved events did not directly match the 220-name
Colwell table. No post-open synonym remapping is used in the primary result. Any
taxonomic reconciliation performed later must be labeled sensitivity-only and cannot
replace this first-open result.
