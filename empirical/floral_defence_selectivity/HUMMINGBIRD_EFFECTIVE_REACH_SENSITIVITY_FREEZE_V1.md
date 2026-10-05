# Hummingbird effective-reach sensitivity — frozen before outcome opening

STATUS = POST_OPEN_MECHANISM_SENSITIVITY_FROZEN_BEFORE_RESULT

## Motivation

The production Aubert/EPHI routing analyses define mismatch as

```text
M = log(flower tube length / culmen length)
```

and the binary barrier as `tube > culmen`.

This is a useful morphology mismatch, but exposed culmen is not identical to
maximum nectar reach because hummingbirds protrude the tongue beyond the bill.

The purpose of this sensitivity is **not** to replace the production estimand or to
retroactively change the preregistered threshold analysis. It asks whether the
zero-inclusive participation decomposition changes qualitatively when the binary
barrier is reclassified using literature-motivated effective-reach multipliers.

## Literature-motivated multipliers

The analysis is restricted to rows classified as `bird_group = hummingbird`.
`Diglossa` flowerpiercers are excluded because their hooked-bill piercing behavior
is not represented by the same bill-plus-tongue legitimate-access model.

Three post-open reach multipliers are frozen:

```text
1.3333333333 = bill + one-third bill tongue correction
1.8          = bill + 80% tongue correction
2.0          = maximal-reach stress test
```

The 1.33 and 1.8 corrections have both been used in hummingbird–plant network
studies. The 2.0 value is a deliberately permissive maximum-reach sensitivity,
motivated by experimental and functional-morphology work showing that maximal
tongue protrusion can approach the bill length beyond the bill tip. It is **not**
treated as an efficient-foraging threshold.

## Frozen questions

For each multiplier k in {1, 4/3, 1.8, 2.0} define

```text
M_k = log(tube / (k * culmen)) = M_1 - log(k)
barrier_k = I(M_k > 0)
```

The following are opened once:

1. Plant-level route-composition result among hummingbirds only:
   - plant-aggregated Spearman rho;
   - paired plant barrier-minus-accessible robbery contrast.
2. Zero-inclusive waypoint × bird participation model among hummingbirds only:
   - pooled resolved-feeding RR;
   - legitimate/non-robbing RR;
   - robbery-only RR;
   - plant-cluster jackknife 95% intervals.
3. The ratio `RR_robbing / RR_legitimate` as a descriptive within-model
   route-composition contrast.
4. Barrier support counts under each multiplier.

## Threshold invariance rule

A constant reach multiplier translates every hummingbird mismatch by the same
constant `-log(k)`. Therefore it cannot, by itself, turn a threshold fitted at the
5–95% search boundary into an interior threshold: the data, fitted midpoint and
search support all translate together.

Accordingly this sensitivity does **not** rerun 999 threshold bootstraps as though a
constant rescaling could create new threshold information. It instead reports the
translated production midpoint relative to each reach scale and preserves the
original boundary classification. A species-specific tongue allometry could change
relative ranks/support, but no such validated species-level tongue dataset is
assumed here.

## Interpretation contract

- This is explicitly post-open.
- The production culmen-only analysis remains the primary frozen analysis.
- A multiplier that changes the binary participation RR is a sensitivity of the
  **barrier definition**, not evidence for a causal tongue-length mechanism.
- P1 and P2 are not treated as the same estimand. P1 is a plant-level
  route-composition association; P2 conditions on waypoint and bird fixed effects,
  so its barrier coefficient is identified from which bird species, within a fixed
  plant/waypoint, fall above versus below the chosen reach threshold.
- No result from this sensitivity may be described as preregistered or confirmatory.
