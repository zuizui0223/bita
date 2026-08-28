# Kessler 2008 aggregate uncertainty bounds v1

## Scope

This is an assumption-indexed sensitivity analysis of the published aggregate constraints, **not** a reconstruction of Fig. S8A or the source ANOVA.

The registered analysis ran in GitHub Actions run `33188639818` and enumerated integer allocations compatible with:

```text
informative antherectomized flowers = 474
capsules                            = 87
EV A+,D+ fraction                   = 34.5–35.5%
PMT/CHAL/CP fractions               = 11.5–14.5%
```

The fraction bands deliberately widen the article's approximate 35% and 12–14% summaries to allow rounding.

## Result

| max denominator ratio | feasible allocations | min probability Δ | min naive z(Δ) | variance inflation to reduce min z to 1.96 | min logit β | min logit z | minimum logit 95% CI lower bound |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.25 | 137,477 | +0.1731 | 2.461 | 1.576 | +0.8914 | 1.763 | -0.0998 |
| 1.50 | 528,045 | +0.1719 | 2.431 | 1.539 | +0.8821 | 1.727 | -0.1193 |
| 2.00 | 1,455,471 | +0.1711 | 2.368 | 1.459 | +0.8766 | 1.686 | -0.1427 |
| 3.00 | 3,052,260 | +0.1710 | 2.296 | 1.372 | +0.8759 | 1.593 | -0.2049 |

Across all declared denominator-balance profiles, the probability-scale interaction remains positive. Thus the published aggregate constraints strongly protect the **sign** of the discrete A×D contrast.

Under a naive independent-flower binomial calculation, the worst probability-scale z remains above 1.96. That result is deliberately not promoted to source significance: the source experiment is organized by experimental day and multiple flowers per plant. At the broadest denominator profile, a variance inflation of only about `1.37` would reduce the worst nominal probability-scale z to 1.96.

The auxiliary logit interaction is also positive in point sign, but feasible allocations produce a 95% Wald lower bound as low as `-0.205`. Therefore the conclusion is intentionally asymmetric:

```text
factorial sign:                       ROBUSTLY POSITIVE
naive probability-scale significance: POSITIVE UNDER INDEPENDENT-FLOWER ASSUMPTION
logit auxiliary 95% interval:          CAN CROSS ZERO
source/design-based interaction CI:    NOT RECOVERED
```

## Combined interpretation with supplement probe

The registered Science supporting-material probe separately found all five current/legacy publisher routes returning HTTP 403. Thus Fig. S8A / exact day-by-genotype values remain unavailable through the declared public routes.

Taken together, these two analyses sharpen rather than blur the Kessler result:

> Kessler 2008 provides a genuinely manipulated attraction-by-defence-like 2×2 field factorial with a common reproductive outcome and a positive interaction sign that survives millions of aggregate-compatible integer allocations. What remains unidentified is the experiment's source/design-based interaction uncertainty, not the existence of the manipulated factorial or the direction of its published aggregate contrast.

## Identification ceiling

These are auxiliary pooled independent-binomial sensitivity calculations. They do not recover the source day-stratified ANOVA, plant-level clustering, or Fig. S8A values and therefore cannot be promoted to a source interaction CI.

The appropriate current label is:

```text
DIRECT_FACTORIAL_SIGN_POSITIVE
AGGREGATE_SIGN_ROBUST
FORMAL_SOURCE_UNCERTAINTY_UNRESOLVED
```
