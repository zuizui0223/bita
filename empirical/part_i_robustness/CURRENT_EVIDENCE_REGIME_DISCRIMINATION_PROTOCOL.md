# Current evidence regime-discrimination audit

## Question

Given the current Part I scenario grid and the registered broad direction map,
which declared biological scenarios can the existing empirical evidence exclude?

This audit uses **only** existing repository inputs:

```text
configs/part_i_robustness_grid.json
Part I functional-form summaries regenerated from that config
registered broad direction map regenerated from 13 route records
```

It adds no retrieval, no taxa, no new biological prediction, and no numerical
parameter calibration.

## What counts as an empirical constraint

A broad direction stratum becomes a sign constraint only if the registered
direction map already classifies it as one of:

```text
mostly_compatible_with_channel_assumption
mostly_contradictory_to_channel_assumption
```

Under the current directional-map contract, this requires at least three
evaluable independent study clusters. Strata marked
`insufficient_directional_clusters` remain visible but do not screen scenarios.

## Scenario mapping

The audit maps direct route signs only to their existing Part I channel
coefficients:

| Route | Part I coefficient | Positive coefficient predicts |
|---|---|---|
| A_to_pollination | `attraction_gain` | positive A→P |
| A_to_antagonism | `attraction_tracking` | positive A→H |
| B_to_antagonism | `floral_defence_efficacy` | negative B→H |
| B_to_pollination | `defence_pollinator_cost` | negative B→P |

A resolved empirical sign can exclude a declared scenario only when that
scenario's corresponding coefficient predicts a different sign or a neutral
channel. It cannot distinguish two positive coefficients of different size.

## What the audit deliberately cannot do

```text
- estimate the A×D mixed partial from route records;
- infer a universal sign from one trait/outcome/design stratum;
- estimate low versus high defence_pollinator_cost from direction-only evidence;
- estimate attraction_defence_shared_cost from any direct route record;
- choose complementarity or substitutability when surviving scenarios retain
  both types of regime map.
```

## Interpretation

The output is a **discrimination audit**, not a parameter fit. A result saying
that several scenarios survive means current evidence is insufficient to choose
between them, not that the scenarios are equally biologically likely.