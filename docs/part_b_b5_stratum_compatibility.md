# Part B B5: compatible-stratum sign interpretation

B5 is a research-priority layer, not a meta-analysis. It summarizes the four
marginal arrows after B1–B4 and decides what evidence should be collected next.

## Compatibility rule

A B2-compatible evidence stratum is defined by:

```text
trait class × outcome class × effect metric × design class
```

The same tuple is used in B5 before any opposite signs are called a conflict.

| Observed pattern | B5 state | Collection action |
|---|---|---|
| no eligible effect | `absent` | collect the first independent effect |
| one independent cluster | `single_anchor` | collect compatible independent clusters |
| all signs agree but fewer than 3 clusters | `consistent` | collect compatible independent clusters |
| all signs agree with >= 3 clusters | `poolable_consistent` | pool B2 envelope, then consider B3 |
| positive and negative effects within one compatibility stratum | `within_stratum_conflict` | code the declared B3 moderator |
| positive and negative effects only across different strata | `cross_stratum_heterogeneity` | retain strata and collect within-stratum clusters before B3 |

## Why `d_A` is heterogeneity now

The verified visual Impatiens effect and scent Gymnadenia effect differ in trait
class and metric. Their opposite signs do not test one shared empirical stratum.
They cannot establish an arrow-wide sign reversal and do not yet identify
`pollination_generalization` as its explanation.

This does not change the Part I model parameter `d_A`; it changes only the
honesty of the evidence-to-parameter bridge. `d_A` remains a high-leverage evidence
gap, but the next sources must be collected in visual/display and scent/reward
tracks separately.
