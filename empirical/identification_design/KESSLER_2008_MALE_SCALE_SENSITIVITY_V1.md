# Kessler 2008 male-fitness scale sensitivity v1

## Purpose

The Kessler 2008 female capsule result is a positive discrete interaction on the declared probability scale under the published aggregate constraints. The source also reports male seed-siring ratios. Those ratios provide an independent check on a central BITA rule: **interaction sign is outcome-scale dependent and must not be treated as transformation-invariant.**

## Published male ratios

The article reports that EV plants sired approximately:

```text
1.9 x more seeds than CHAL
2.2 x more seeds than PMT
4.7 x more seeds than CP
```

Normalize EV male fitness to `1`. The implied relative cell means are then:

```text
EV   A+,D+ = 1.0000
PMT  A+,D- = 1 / 2.2 = 0.4545
CHAL A-,D+ = 1 / 1.9 = 0.5263
CP   A-,D- = 1 / 4.7 = 0.2128
```

## Additive-scale interaction

On the raw relative-count scale:

```text
Delta_AD = EV - PMT - CHAL + CP
         = 1 - 0.4545 - 0.5263 + 0.2128
         = +0.2319
```

The reported male ratios are therefore compatible with positive non-additivity on an additive relative-count scale.

## Multiplicative/log-scale interaction

On the log scale the same four reported ratios imply:

```text
beta_AD = log(EV) - log(PMT) - log(CHAL) + log(CP)
        = -0.1173

interaction ratio = (EV * CP) / (PMT * CHAL)
                  = 0.8894
```

Thus the reported male pattern is slightly negative relative to multiplicative independence.

## Interpretation

This is not a contradiction. It is exactly why BITA declares the outcome scale before interpreting `Delta_AD W`.

```text
female capsule probability scale: robust positive aggregate interaction sign
male relative-count additive scale: positive interaction sign
male multiplicative/log scale:       slightly negative interaction sign
```

The male ratios are rounded published summaries and do not supply uncertainty for either reconstructed interaction. They must not be pooled with the female capsule analysis or used to manufacture a scale-invariant escape claim.

## Claim boundary

> Kessler 2008 strongly supports the existence of attraction-by-defence-like reproductive non-additivity, but the numerical sign of that non-additivity is estimand- and scale-specific. The strict BITA escape decision must therefore name the reproductive endpoint and scale whose uncertainty is being used.

This sensitivity strengthens the case for retaining a discrete declared-scale estimand rather than presenting a generic positive `W_AD` as a property of the system independent of measurement scale.
