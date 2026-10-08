# Bypass rescue-window test v1

Status: **FROZEN BEFORE ZERO-INCLUSIVE SHAPE OUTCOME**
Date: 2026-10-08
Branch: `analysis/bypass-rescue-window-v1`

## Question

Does access mismatch generate a transient ecological **bypass window** before
consumer-resource interaction disappears?

The already opened BITA results establish two different facts:

1. conditional robbery share increases with flower-tube / bird-access mismatch;
2. under the literature-motivated 1.8x hummingbird effective-reach correction,
   zero-inclusive legitimate feeding is strongly reduced under severe barriers while
   absolute robbery is not detectably increased.

These facts do not determine the continuous shape of **absolute robbery rate**.
A rising conditional robbery share can coexist with a hump-shaped absolute robbery
rate if total interaction disappears at extreme mismatch.

## Prior-art boundary

This analysis does **not** claim:
- first mismatch-associated nectar robbing;
- first evidence that long flowers are more frequently robbed;
- first route switching;
- first non-linear plant-pollinator interaction.

Close prior work generally tests robbery occurrence/share among flowers or observed
visits. Lara & Ornelas (2001) and Aubert et al. (2026) predict increasing robbery
with increasing legitimate-access difficulty. The earlier BITA threshold analysis
tested upper turnover in conditional plant-level robbery rate and found no supported
interior turnover.

The new estimand is narrower and different: **zero-inclusive absolute route-specific
feeding rate across all locally available bird x clean-camera waypoint
opportunities**.

## Biological hypothesis

### H1 — interaction-rescue window

As effective mismatch increases:

~~~text
accessible
  -> legitimate feeding dominates

moderate effective mismatch
  -> legitimate access is impaired
  -> bypass/robbery temporarily rescues feeding
  -> absolute robbery rate peaks

severe effective mismatch
  -> even bypass is insufficient/unprofitable
  -> total feeding and absolute robbery decline
~~~

Therefore robbery is predicted to be maximal at an **intermediate** mismatch,
not at maximal mismatch.

This is a stronger and less intuitive prediction than
`more mismatch -> higher robbery share`.

## Frozen population and mismatch scale

Use the existing Aubert/EPHI clean-camera x locally-available-bird opportunity
matrix.

Primary population:
- Trochilidae hummingbirds only;
- exclude `Diglossa` flowerpiercers;
- use the same route coding and missing-piercing-as-legitimate rule as the current
  archive.

Primary effective mismatch:

~~~text
M_eff = log[tube / (1.8 * culmen)]
~~~

The 1.8 multiplier is not selected from this outcome. It is the already committed
literature-motivated effective-reach sensitivity used in the current Letter.

## Frozen three-state bins

Reuse the already preregistered 25% proximity width from
`AUBERT_ROUTING_THRESHOLD_PREREG_V1.md`:

~~~text
delta = log(1.25)

ACCESSIBLE:
    M_eff <= 0

MODERATE_MISMATCH:
    0 < M_eff <= delta

SEVERE_MISMATCH:
    M_eff > delta
~~~

No quantile or result-dependent cut point may replace these bins.

## Responses

Fit the same zero-inclusive opportunity edges separately for:

1. legitimate/non-robbing feeding counts;
2. robbery-only feeding counts;
3. pooled route-resolved feeding counts (secondary).

Zero opportunity edges remain in the denominator.

## Model

For each response:

~~~text
log(mu_wb) =
    alpha_waypoint
  + gamma_bird
  + theta_moderate * I[MODERATE]
  + theta_severe   * I[SEVERE]
~~~

where ACCESSIBLE is the reference.

Waypoint fixed effects absorb sampling effort and all time-invariant waypoint-level
plant/reward main effects. Bird fixed effects absorb baseline bird use.

The three-state indicators are non-additive functions of tube x bird reach, so they
remain identifiable even though a continuous linear log(tube/reach) term is exactly
collinear with waypoint and bird fixed effects.

Uncertainty:
- delete-one-plant-species jackknife;
- 95% intervals on log-rate contrasts, exponentiated to rate-ratio intervals.

## Primary contrasts

For robbery:

~~~text
R_MA = robbery rate MODERATE / ACCESSIBLE
R_SM = robbery rate SEVERE / MODERATE
~~~

For legitimate feeding:

~~~text
L_MA = legitimate rate MODERATE / ACCESSIBLE
L_SM = legitimate rate SEVERE / MODERATE
~~~

## Frozen decision rule

### FULL_BYPASS_RESCUE_WINDOW

Require all:

1. robbery `R_MA > 1` with 95% CI entirely > 1;
2. robbery `R_SM < 1` with 95% CI entirely < 1;
3. legitimate `L_MA < 1` OR `L_SM < 1` with the corresponding 95% CI entirely < 1;
4. the robbery ordering remains `MODERATE > max(ACCESSIBLE, SEVERE)` after
   delete-one-plant jackknife in at least 90% of plant deletions.

### DIRECTIONAL_WINDOW_ONLY

Point estimates show

~~~text
robbery MODERATE > ACCESSIBLE
robbery MODERATE > SEVERE
~~~

but the full 95% rule is not met.

### NO_BYPASS_RESCUE_WINDOW

The intermediate robbery maximum is absent or reverses.

Only FULL_BYPASS_RESCUE_WINDOW is eligible for promotion as the main new result.
DIRECTIONAL_WINDOW_ONLY remains exploratory.

## Support gate before interpretation

Before model coefficients are interpreted, require:
- at least 10,000 hummingbird opportunity edges total;
- all three mismatch states represented;
- at least 200 opportunity edges in each state;
- at least 20 bird species and 30 plant species overall.

If a route has complete count separation in one state, report
`RATE_SEPARATED_AT_ZERO` rather than smoothing or changing bins.

## Sensitivities

Only after the primary result:
- repeat using reach multipliers 4/3 and 2.0 with the **same** 25% excess margin;
- report, do not optimize, state counts and route-rate ordering.
- no alternative margin scan is allowed.

## Claim boundary

Even a supported window is observational. It would show that absolute feeding is
rerouted through robbery over an intermediate mismatch range, not that morphology
causally induces robbing or that the route is adaptive.

A supported result may be phrased:

> Morphological mismatch does not simply convert mutualism monotonically into
> exploitation. In this network, bypass use is concentrated in an intermediate
> access window before interaction itself is filtered.

A failed result must be retained and this hypothesis abandoned without redefining
the window.
