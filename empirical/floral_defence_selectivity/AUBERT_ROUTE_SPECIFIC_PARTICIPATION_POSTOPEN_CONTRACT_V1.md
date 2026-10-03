# Aubert / EPHI route-specific participation post-open contract v1

## Status

```text
AGGREGATE_PARTICIPATION_EFFECT = ALREADY_OPENED
ROUTE_SPECIFIC_EFFECTS = NOT_YET_OPENED_WHEN_THIS CONTRACT WAS WRITTEN
ANALYSIS_CLASS = POST_OPEN_DIAGNOSTIC
CONFIRMATORY_PREREGISTRATION = NO
```

## Why this diagnostic exists

The frozen aggregate participation outcome counts all resolved feeding records
retained by the Letter's primary route rule:

```text
primary_count = legitimate/non-robbing feeding + robbing feeding
```

It therefore measures resolved feeding visitation/participation, not robbery alone.
After the aggregate rate ratio was opened, this diagnostic was added to determine
which route component carries that increase.

The frozen first-open result and its hashes are not modified.

## Fixed data and model

Both route-specific outcomes use the exact existing opportunity matrix and barrier
definition. No opportunity edge is added or removed before route-specific
positive-margin pruning.

```text
robbing count:
    feeding_activity != no_feeding
    AND primary route status == yes

legitimate/non-robbing count:
    feeding_activity != no_feeding
    AND primary route status == no
    including the frozen missing-piercing-as-legitimate rule
```

For each outcome separately:

```text
log(mu_waypoint,bird)
    = alpha_waypoint
    + gamma_bird
    + beta_barrier * I[tube > culmen]
```

Uncertainty is the same delete-one-plant-species jackknife used for the aggregate
analysis. The script must verify that, edge by edge,

```text
robbing_count + legitimate_count == frozen primary_count.
```

## Interpretation fixed before route-specific effects are opened

Using the 95% plant-jackknife interval relative to 1:

1. **Robbing increases; legitimate does not increase.**
   The aggregate participation increase is robbery-specific or robbery-dominated.
   Wording may describe greater bypass exploitation, while keeping the analysis
   observational.

2. **Robbing increases; legitimate also increases.**
   The aggregate result is a broader feeding-visitation increase plus a
   route-composition shift toward robbery. Do not call the aggregate 1.772 rate
   ratio an exploitation-specific effect. The ecological conclusion is that the
   barrier state did not filter legitimate feeding visits in these observational
   data.

3. **Robbing does not increase; legitimate increases.**
   Withdraw any wording that uses the aggregate rate ratio as evidence for greater
   robbery/exploitation. Retain the separately established robbery-proportion
   routing result and interpret the aggregate participation effect as legitimate
   visitation.

4. **Neither route increases clearly.**
   Treat the aggregate decomposition as unstable to route splitting and remove it
   from the headline interpretation.

No branch is to be preferred after seeing the route-specific estimates.

## Reward-confounding boundary

Waypoint fixed effects absorb any time-invariant main effect shared by birds at a
waypoint, including plant identity, fixed reward differences, and camera effort.
Thus a simple plant-level correlation between tube length and average nectar reward
cannot by itself produce the barrier coefficient.

The public EPHI tables do not provide a direct nectar amount/concentration
covariate. Bird-specific reward responses and reward changes within a camera
deployment can therefore remain as interaction-level or temporal confounding.

## Threshold boundary audit

The already-opened threshold bootstrap is audited without changing its optimizer,
seed, search interval, or bootstrap count. Report the fractions of finite
replicates whose midpoint lands at the upper boundary, lower boundary, or in the
interior. If boundary mass is large, emphasize that mass rather than treating the
percentile interval as ordinary uncertainty around an interior threshold.
