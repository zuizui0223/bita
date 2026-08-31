# Kessler 2008 Stage-1 partial-identification receipt v2

## Decision

The published aggregate constraints identify substantially more than a positive total interaction, but they still stop short of strict Level-2/3 release.

Across all four registered denominator-balance profiles in GitHub Actions run `33357523448`:

```text
A0 = p10 - p00
identified set:  -0.0299275 to +0.0299275

A1 = p11 - p01
identified set:  +0.2001327 to +0.2398387

Delta_AD = A1 - A0
minimum:         +0.1710239
```

Therefore:

```text
A1 uniformly positive:                 YES
A0 sign identified:                    NO
Level 1 interaction relief:            STRONG SIGN ANCHOR
Level 2 constraint release:            NOT STRICTLY IDENTIFIED
Level 3 strict reversal:               NOT STRICTLY IDENTIFIED
stage1 partial-ID decision:            A1_POSITIVE_A0_SIGN_UNRESOLVED_PARTIAL_IDENTIFICATION
```

## What is now identified

The defended attraction effect is not merely positive at a convenient rounded point estimate. Under every aggregate-compatible allocation in the declared profiles,

```text
A1 > +0.2001
```

on the capsule-probability scale. Thus the attraction effect when nicotine is present is sign-identified as positive under the registered aggregate restrictions.

The only Stage-1 sign ambiguity is the undefended attraction effect:

```text
A0 in approximately [-0.030, +0.030].
```

The smallest descriptive epsilon for which every compatible allocation satisfies

```text
A0 <= epsilon
```

is `0.0299275`, or about 3 percentage points. This quantity is a partial-identification width. It is **not** a retrospectively chosen biological equivalence margin.

## Why Level 2 still fails closed

The registered Level-2 criterion is

```text
A0 <= 0 and A1 > 0.
```

`A1 > 0` is satisfied uniformly. `A0 <= 0` is not: aggregate-compatible allocations exist on both sides of zero. Consequently the strict Level-2 claim remains unresolved even though its uncertainty has been localized to a narrow baseline-effect interval.

The Level-3 criterion

```text
A0 < 0 and A1 > 0
```

fails for the same reason.

This is sharper than the previous status `Levels 2/3 unresolved`: the defended response is identified; only the sign of the undefended response is not.

## Total-interaction boundary

The same run preserved the previous total-interaction conclusions:

```text
minimum probability-scale Delta_AD:   +0.1710239
minimum naive probability z:          2.2960104
minimum auxiliary logit z:            1.5932234
minimum auxiliary logit CI lower:    -0.2048849
```

The positive total-interaction sign remains robust. Formal source/design uncertainty remains unresolved because the exact genotype-by-day values, plant clustering, and source ANOVA are not recovered.

## Estimand boundary

These are identified sets under the declared published proportion bands, total flower/capsule constraints, and denominator-balance profiles. They are not recovered original cell means and are not source confidence intervals.

The correct paper-facing statement is therefore:

> Kessler et al. (2008) robustly identifies a positive attraction effect when defence is present and a positive total attraction-by-defence interaction under the published aggregate constraints, while the attraction effect without defence remains confined to a narrow interval spanning zero. Strict nonpositive-to-positive release and strict sign reversal therefore remain unresolved without source-scale uncertainty or an independent replication.

## Provenance

```text
workflow run: 33357523448
head SHA:     a0ee9d04f312a715b0ad7360f314bb131a94494c
analysis:     kessler_2008_aggregate_bounds_v2
```
