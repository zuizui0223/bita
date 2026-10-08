# Route-replacement compensation moderator test v1

Status: **FROZEN BEFORE SITE-LEVEL MODERATOR OUTCOME**
Date: 2026-10-08
Branch: `analysis/route-compensation-moderators-v1`

## Starting observation already opened

Independent split-sample analyses in Ecuador and Costa Rica agree on route
replacement but disagree on total throughput:

~~~text
                     Ecuador        Costa Rica
legitimate flux       -0.162          -0.156
robbery flux          +0.668          +0.824
total flux             -0.042          +0.115
~~~

The country contrast is already known and is therefore **not** a confirmatory
outcome of this analysis.

## Prior-art boundary and competing mechanisms

Duchenne et al. (2023; doi:10.1371/journal.pbio.3002434) already showed in
simulation that the effect of cheating on community persistence depends on
network structure; more connected, nested and modular initial mutualistic
networks tended to make cheating less negative / more positive. They did not
test whether network structure predicts empirical **weighted compensation**
of lost legitimate interactions.

The same paper deliberately used a binary mutualistic backbone for its
empirical parameterization because interaction frequencies were considered
strongly abundance-dependent.

The present analysis therefore freezes two competing, source-motivated
moderators of whether route replacement preserves total interaction flux:

### H1 — structural redundancy

Within a site, higher legitimate-network connectance should make the
cheating-share -> total-flux slope more positive.

Prediction:
`beta_connectance > 0`.

### H2 — consumer supply

Within a site, higher route-independent bird activity should make the
cheating-share -> total-flux slope more positive, because more available
consumers can supply enough robbery events to compensate for lost legitimate
feeding.

Route-independent consumer activity is frozen as explicit
`feeding_activity=no_feeding` target-bird detections per clean camera-hour.
It is treated only as a local activity / encounter proxy, not as an abundance
estimate.

Prediction:
`beta_activity > 0`.

The goal is not to force a country explanation. Either, both, or neither
moderator may be supported.

## Data

Use all currently public EPHI raw camera and interaction data:

- Ecuador: `Interactions_data_Ecuador.txt`,
  `Cameras_data_Ecuador.txt`;
- Costa Rica: `Interactions_data_Costa-Rica.txt`,
  `Cameras_data_Costa-Rica.txt`;
- common plant and hummingbird trait tables from Zenodo 10.5281/zenodo.14185547.

Primary animals: Trochilidae only in both countries, so flowerpiercers do not
create a country-specific guild difference.

## Frozen cross-fit split

For every raw waypoint:

~~~text
FNV1a32(raw waypoint UTF-8)
A if hash mod 2 == 0
B otherwise
~~~

Each directional analysis uses predictor variables from one fold and total
feeding flux from the disjoint fold.

## Plant-site eligibility

For a site x plant row in direction A->B or B->A require:

1. >=2 clean predictor-fold waypoints;
2. >=2 clean outcome-fold waypoints;
3. >=5 resolved predictor-fold feeding interactions;
4. positive outcome camera-hours.

A site enters moderator inference only when it has >=5 eligible plant rows in
that direction. Primary support requires >=8 eligible sites in each country
in at least one direction and >=20 sites total in each direction.

## Predictor at plant-site scale

Cheating share:

~~~text
C_is = robbery / (robbery + legitimate)
~~~

measured only in the predictor fold.

Outcome:

~~~text
F_is = (robbery + legitimate events) / clean camera-hours
~~~

measured only in the outcome fold.

Within each site, convert C and log1p(F) to midranks and center each rank on its
site mean. Call these `x_is` and `y_is`.

## Frozen site moderators

### M1 legitimate connectance

Using only predictor-fold resolved feeding events within a site:

- node set = all plant and hummingbird species with >=1 resolved feeding
  interaction in that fold/site;
- legitimate link = plant-bird pair with >=1 legitimate interaction;
- `connectance = L_legit / (N_plants * N_birds)`.

The metric is calculated before using outcome-fold flux.

### M2 nonfeeding bird activity

Using only predictor-fold clean-camera observations within a site:

~~~text
activity =
number of target-hummingbird rows with feeding_activity=no_feeding
/
total clean camera-hours
~~~

Use `log1p(activity)`.

Within each direction, z-standardize site connectance and log1p(activity)
across eligible sites.

## Primary joint model

For each direction separately, fit OLS to all eligible within-site centered
plant rows:

~~~text
y_is =
    beta_C * x_is
  + beta_conn * x_is * z(connectance_s)
  + beta_act  * x_is * z(activity_s)
  + beta_country * x_is * I[CostaRica]
  + error
~~~

No site-level main effects are needed because x and y are centered within site.

Primary reported moderator effects are equal-direction arithmetic means:

~~~text
B_conn = mean(beta_conn_AtoB, beta_conn_BtoA)
B_act  = mean(beta_act_AtoB,  beta_act_BtoA)
B_country = mean(beta_country_AtoB, beta_country_BtoA)
~~~

The country term is a residual slope contrast after both moderators; it is
diagnostic, not a third mechanistic hypothesis.

## Inference

99,999 permutations, seed 20261008.

Within every site and direction, permute `x_is` among eligible plants while
holding y and both site moderators fixed. Refit the full model and recompute
B_conn and B_act.

One-sided tests:
- H1: `Pr(B_conn_perm >= B_conn_obs)`;
- H2: `Pr(B_act_perm >= B_act_obs)`.

Also report two-sided values and 9,999 site-cluster bootstrap intervals,
resampling sites within country.

## Frozen interpretation rules

### STRUCTURE_SUPPORTED
Require:
- B_conn > 0;
- beta_conn positive in both A->B and B->A;
- one-sided permutation p < 0.05;
- 95% site-bootstrap interval excludes 0.

### ACTIVITY_SUPPORTED
Same four requirements for B_act.

### BOTH_SUPPORTED
Both sets pass.

### NEITHER_SUPPORTED
Neither passes.

Do not choose a winner merely because one p-value is smaller.

## Prespecified secondary checks

1. rerun with >=10 predictor interactions;
2. rerun with >=3 waypoints in each fold;
3. report model omitting country term to show whether moderator signs depend on
   explicitly absorbing the already-known country contrast.

No alternative activity proxy, connectance denominator, site threshold or
network metric may replace a failed primary result.

## Claim boundary

If H1 is supported:
> The quantitative compensation of cheating-driven route replacement depends
> on redundancy in the pre-existing legitimate interaction network.

If H2 is supported:
> The quantitative compensation of route replacement depends on local consumer
> supply, not only on the relative frequency of cheating.

If neither is supported, the Ecuador-Costa Rica throughput contrast remains
unexplained by these two predeclared mechanisms and must be retained as
heterogeneity rather than narrated post hoc.

No result here directly measures community persistence, plant fitness, or
causal effects of cheating.
