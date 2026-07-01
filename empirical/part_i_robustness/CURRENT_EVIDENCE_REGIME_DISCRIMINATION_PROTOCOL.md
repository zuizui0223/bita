# Current evidence regime-discrimination audit

## Question

Given the currently declared Part I scenarios and the currently registered broad
direction map, which scenarios can existing empirical evidence exclude?

The audit uses only repository inputs already present before the audit:

```text
Part I configuration
regenerated Part I functional-form summaries
regenerated registered broad direction map
```

No new retrieval, taxon, mechanism, or numerical calibration is introduced.

## Constraint rule

A route stratum is used as a sign constraint only after the existing direction
map has already classified it as one of:

```text
mostly_compatible_with_channel_assumption
mostly_contradictory_to_channel_assumption
```

Under the existing map contract, that requires at least three evaluable,
independent study clusters. Everything else remains visible but cannot screen a
Part I scenario.

## Existing model-channel mapping

| Route | Part I coefficient | Sign with a positive coefficient |
|---|---|---|
| A_to_pollination | `attraction_gain` | positive |
| A_to_antagonism | `attraction_tracking` | positive |
| B_to_antagonism | `floral_defence_efficacy` | negative |
| B_to_pollination | `defence_pollinator_cost` | negative |

The audit only asks whether a scenario predicts the same sign as the resolved
empirical stratum. It does not use sign agreement to estimate a coefficient.

## Interpretation boundary

A negative B_to_pollination stratum can rule out a declared scenario with a zero
or opposite pollination-cost channel. It cannot distinguish a low positive cost
from a high positive cost. It also says nothing by itself about antagonism
tracking or shared attraction–defence allocation cost.

Therefore a surviving complementary scenario and a surviving substitutable
scenario mean that the present evidence has **not** chosen a regime. It does not
mean the two scenarios are equally likely, nor that their parameters were fitted.
