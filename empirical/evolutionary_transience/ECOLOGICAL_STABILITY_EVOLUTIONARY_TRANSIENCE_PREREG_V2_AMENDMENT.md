# Ecological stabilization–evolutionary transience test v2 amendment

Status: **AMENDED BEFORE NEW OUTCOME ANALYSIS**

Amendment date: 2026-10-07
Supersedes only the primary-outcome hierarchy in
`ECOLOGICAL_STABILITY_EVOLUTIONARY_TRANSIENCE_PREREG_V1.md`.
The v1 file remains immutable as the audit trail.

## Why this amendment was necessary before opening a new result

A closer source audit found that Colwell et al. (2023; doi:10.1086/726036)
already compared an equal-rates (ER) model with an all-rates-different (ARD)
model for hover-to-cling and cling-to-hover transitions. ER had lower AIC and
higher AIC weight. Therefore the v1 proposal to make asymmetric state dwell
time the primary test would partly recycle an already published analysis.

The same paper did **not** test whether clinging lineages have lower speciation
or diversification. It explicitly described the concentration of many origins
near the tips as a "puzzling lack of diversification and evolutionary
persistence" and left the explanation as a conjecture.

A second prior result sharpens the null prediction. Barreto et al. (2023;
doi:10.1098/rspb.2022.1793) found that shorter-billed hummingbirds tend to have
higher present-day speciation rates across several estimators. Colwell et al.
found clingers to be shorter-billed after phylogenetic/body-size/elevation
filtering. Thus a morphology-only explanation predicts clingers should, if
anything, have **higher**, not lower, speciation.

## Revised non-obvious hypothesis

### H1 — behavioural bypass reverses the morphology-based diversification expectation

After accounting for the known association of shorter bills with faster
hummingbird speciation, clinging / bypass-capable feeding states are associated
with **lower residual speciation**.

The important contrast is therefore:

~~~text
known morphology path:
short bill -> higher speciation
clinger   -> shorter bill
--------------------------------
naive expected sign:
clinger   -> higher speciation

transience hypothesis:
clinger / bypass state
          -> lower speciation after bill/body/niche adjustment
~~~

A negative residual clinger effect would be a sign reversal relative to the
trait-only expectation rather than a restatement that unusual feeding behavior
occurs near phylogenetic tips.

## Gate A — independent published speciation estimates

### Data

- frozen behavioural state: Colwell et al. Harvard Dataverse
  doi:10.7910/DVN/THDJCI, Supplemental Spreadsheet S1;
- independently estimated hummingbird speciation rates and covariates:
  Barreto et al. 2023 Royal Society Figshare article 22493044.

The two sources were assembled for different questions. State labels are not
derived from the speciation-rate dataset.

### Primary state

Source-defined **clinger** classification: any of the first four unorthodox
feeding modes pooled as clinger by Colwell et al. The primary contrast is the
published 66 known clingers versus 144 presumed non-clingers. The 10 species
documented only feeding through pierces while on the wing are a third
source-defined group and are excluded from the primary clinger contrast rather
than coded as non-clingers.

### Secondary state

**bypass-capable**: documented use of an existing floral opening or active
piercing, whether clinging or hovering. This state is secondary because it is
closer to innovative cheating but its absence is especially vulnerable to
observation error.

### Primary outcomes

Use every independently supplied present-day speciation-rate estimator in the
Barreto processed dataset that is available for the McGuire phylogeny
(expected families: BAMM, ClaDS and DR). No estimator may be selected on the
basis of its result.

### Frozen models

For each speciation-rate estimator, fit two nested models on the complete
joined species set.

Baseline:

~~~text
z(speciation_rate)
  ~ z(log_bill_length)
  + z(log_body_mass)
  + z(mid_elevation)
  + z(temperature_breadth)
  + z(precipitation_breadth)
  + major_clade
~~~

Test model:

~~~text
baseline + clinger
~~~

If the exact processed variable names differ, map only semantically identical
published variables. Do not substitute new covariates after inspecting the
clinger coefficient.

Primary statistic for each estimator:

~~~text
beta_clinger
~~~

Primary directional prediction:

~~~text
beta_clinger < 0
~~~

The Gate-A aggregate is the median standardized clinger coefficient across all
eligible speciation estimators. Gate A is considered directionally supportive
only if the median is negative and at least two independent estimator families
have negative coefficients.

### Permutation control

Within each named major hummingbird clade, permute the frozen clinger labels
while preserving the number of clingers in that clade. Refit the complete
baseline + clinger model for each permutation. Use 9,999 permutations and a
fixed seed of 20261007.

This clade-stratified permutation is the inferential control at Gate A. Nominal
OLS P values are descriptive only.

### Critical negative controls

1. Bill length must remain in the model: removing it would confound the
   hypothesis with the already published short-bill/speciation relationship.
2. Repeat excluding Coquettes.
3. Repeat on species with direct genetic placement only if the processed table
   identifies the 12 Colwell phylogenetically uncertain taxa.
4. Report join attrition and state counts before model fitting.
5. Do not promote a result supported by only one speciation estimator.

## Gate B — phylogenetic confirmation

Only if Gate A is directionally supportive, proceed to the source phylogenetic
ensemble.

Gate B will test whether the state effect survives explicit phylogenetic
control and a diversification method that does not rely on a single SSE fit.
Preferred hierarchy:

1. phylogenetic regression / structured permutation using species-level
   speciation estimates across alternative trees;
2. FiSSE or an equivalently robust nonparametric state-dependent diversification
   test where its assumptions match the data;
3. hidden-state SSE only as a sensitivity, never the sole evidence.

The published ER > ARD transition result is retained as prior evidence and is
not rerun as a novelty claim.

## Cross-scale interpretation if both gates pass

Duchenne et al. (2023; doi:10.1371/journal.pbio.3002434) showed that innovative
cheating can increase ecological community persistence under restricted
conditions, while explicitly leaving evolutionary stability unresolved.
Wechsler & Bascompte (2022; doi:10.1086/717865) instead provide evolutionary
theory in which cheating can promote diversity.

Therefore a robust negative clinger/bypass diversification effect would support
a genuinely non-trivial cross-scale result:

> A feeding innovation can expand ecological access and even stabilize
> communities while being associated with lower macroevolutionary lineage
> proliferation than expected from the morphology of its users.

This is an empirical sign reversal relative both to the short-bill expectation
within hummingbirds and to theory in which cheating promotes diversification.

## Kill rule

Do **not** promote this hypothesis if:

- the Gate-A median clinger coefficient is zero or positive;
- fewer than two speciation estimator families agree on a negative sign;
- the sign disappears when bill length is included;
- the apparent effect is entirely Coquette-driven; or
- Gate B fails to retain the direction under explicit phylogenetic control.

If killed, record the falsification and keep the current access-routing Letter
unchanged.
