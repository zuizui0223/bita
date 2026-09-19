# Effective-domain pollinator-state recovery v1

## Question

Can the effective-domain architecture recover the **qualitative pollinator state** across a broader set of floral defence/access systems than the strict direction-supported Stage-2 subset?

This analysis deliberately changes the outcome from a binary preservation claim to an ecological state family.

## Fixed state mapping

Architecture prediction:

```text
SEPARATED   -> NO_INTERFERENCE_OBSERVED
TRANSITIONAL -> MIXED
OVERLAPPED  -> IMPAIRED
```

Observed pollinator-state family:

```text
PRESERVED_OR_IMPROVED -> NO_INTERFERENCE_OBSERVED
NO_DETECTED_CHANGE    -> NO_INTERFERENCE_OBSERVED
MIXED                 -> MIXED
IMPAIRED              -> IMPAIRED
UNRESOLVED            -> unscored
```

Important:

```text
NO_DETECTED_CHANGE != equivalence-supported preservation
```

The state-recovery analysis therefore asks whether the expected **type of response** is recovered, not whether every separated system proves zero pollinator cost.

## Historical derivation set

The derivation cohort contains 14 matched systems, of which 9 have both:

1. a scorable architecture state among SEPARATED / TRANSITIONAL / OVERLAPPED; and
2. a scorable pollinator outcome family.

Observed architecture counts:

```text
SEPARATED    4
TRANSITIONAL 4
OVERLAPPED   1
```

Observed outcome-family counts:

```text
NO_INTERFERENCE_OBSERVED 4
MIXED                    4
IMPAIRED                 1
```

Result:

```text
domain-rule correct = 9 / 9
accuracy            = 1.000
```

The fixed-margin probability of one perfect category allocation is:

[
1 / 630 = 0.0015873.
]

This is **not** treated as a confirmatory p-value because the historical systems contributed to theory formation. It is a descriptive measure of how sharply the derived rule organizes the corpus.

## Coarse modality comparator

As a deliberately simpler alternative, broad defence modality was used as a leave-one-out majority classifier within the same 9 historical systems.

Result:

```text
modality LOO correct = 6 / 9
accuracy             = 0.667
```

The derivation-set modality rule is:

```text
chemical      -> MIXED
physical      -> NO_INTERFERENCE_OBSERVED
reward_access -> NO_INTERFERENCE_OBSERVED
fallback      -> MIXED
```

Thus broad modality does recover some structure, but it misses three historical systems that the effective-domain state rule recovers.

This does **not** establish a statistically significant superiority test between the two predictors.

## Systematic expansion

Two post-rule systematic-expansion systems are scorable:

```text
Caryopteris  SEPARATED -> PRESERVED_OR_IMPROVED
Phlox        SEPARATED -> NO_DETECTED_CHANGE
```

Effective-domain rule:

```text
correct = 2 / 2
```

Derivation-trained modality rule:

```text
correct = 1 / 2
```

The physical Caryopteris system is recovered by both rules. The chemical Phlox system is recovered by the domain rule but not by the derivation chemical-majority rule.

Because both expansion architecture codes are source-mechanistic/post hoc rather than prospectively blinded, this remains **post-rule corroboration**, not a prospective validation trial.

## Registered hold-out

The Erica 2026 system is prospectively coded as SEPARATED / geometry.

Its pollination direction is positive but retained as:

```text
DIRECTION_ONLY / UNRESOLVED
```

Therefore:

```text
holdout scored n = 0
holdout unscored n = 1
```

The hold-out is directionally compatible but is not promoted merely to complete the table.

## Pooled scored pattern

Across historical derivation + systematic expansion:

```text
scored systems = 11

SEPARATED    6 -> NO_INTERFERENCE_OBSERVED 6
TRANSITIONAL 4 -> MIXED                    4
OVERLAPPED   1 -> IMPAIRED                 1

domain-rule correct = 11 / 11
```

The fixed-margin probability of one perfect category allocation is:

[
1 / 2310 = 0.0004329.
]

Again, this is a descriptive alignment statistic, not a prospective confirmatory p-value.

## Why this is more macro-ecological than the strict Stage-2 test

The strict Stage-2 gate asks a narrow causal-style question:

> Do direction-supported separated systems preserve/improve pollinator function while overlapped systems impair it?

That gate has only (n=3).

The present analysis asks a broader ecological-state question:

> Does access/exposure architecture predict whether a defence state is non-interfering, context-dependent, or pollinator-impaired?

This recovers 11 scorable independent systems while preserving uncertainty classes.

Therefore the paper now has two distinct cross-system results:

1. **strict Stage-2 exact result** — narrow, high-specificity, (n=3);
2. **macro ecological-state recovery** — broader, heterogeneous-outcome state analysis, (n=11).

They must not be conflated.

## Main ecological interpretation

The recurrent pattern is not simply:

```text
chemical = costly
physical = safe
```

Instead:

```text
separated exposure
    -> no pollinator interference observed / preserved function

changing dose, exposure, stage or consumer dependence
    -> mixed state

strong overlap
    -> pollinator impairment
```

This is the strongest current cross-system macro pattern in BITA.

## Claim ceiling

Supported:

> **Across the scorable cross-system corpus, effective-domain architecture perfectly recovers the observed qualitative pollinator-state family, including two post-rule expansion systems.**

Required qualifier:

> Historical systems contributed to theory formation, null-compatible results are not equivalence, the post-rule sample is small, and the registered hold-out remains unresolved.

Not supported:

- universal causal coefficient;
- prevalence of states in nature;
- formal proof that domain architecture outperforms every coarse predictor;
- pooled effect size across heterogeneous pollinator outcomes.

Machine-readable result:

`empirical/floral_defence_selectivity/results/effective_domain_state_recovery.json`
