# Kessler 2008 mechanism-bound handoff V1

## Decision

The registered aggregate sensitivity analysis supplies a robust probability-scale lower bound on the total attraction-by-defence interaction. Propagating only that lower bound through BITA's mechanism identity yields one additional quantitative result under an explicit channel restriction.

```text
DELTA_AD_W_LOWER_BOUND = +0.1710239
ASSUMPTION = kappa_delta >= 0
KESSLER_CONDITIONAL_BIOTIC_BALANCE_LOWER_BOUND = +0.1710239
RHO_DELTA = NOT_POINT_IDENTIFIED
IOTA_DELTA = NOT_POINT_IDENTIFIED
CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED
```

Because

```text
rho_delta - iota_delta = Delta_AD W + kappa_delta,
```

`kappa_delta >= 0` implies

```text
rho_delta - iota_delta >= +0.1710239.
```

This is a **conditional partial-identification bound** on the contrast between antagonist relief and pollinator interference. It is not a measured channel effect, and neither `rho_delta` nor `iota_delta` is separately bounded by this restriction alone.

## Why this is stronger than a sign statement

The previous Kessler result established that the total interaction remains positive over the registered aggregate-compatible denominator profiles. The handoff now carries the worst-case lower edge of that identified set into mechanism space. Under the declared `kappa_delta >= 0` restriction, the biotic balance must exceed the total-interaction floor rather than merely being positive.

## Claim ceiling

This result does **not** establish that `kappa_delta >= 0` is empirically measured in Kessler et al. (2008). The restriction is assumption-indexed. It also does not identify strict Level-2 constraint release, Level-3 reversal, or the individual ecological channels. Those claims remain governed by the existing Stage-1 and mechanism-identification gates.

## Provenance

```text
analysis: kessler_2008_mechanism_bound_handoff_v1
source analysis: kessler_2008_aggregate_bounds_v1
source workflow run: 33188639818
source file: KESSLER_2008_AGGREGATE_BOUNDS_V1.json
```
