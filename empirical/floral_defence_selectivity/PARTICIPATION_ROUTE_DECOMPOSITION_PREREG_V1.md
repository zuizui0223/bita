# Participation-versus-routing decomposition preregistration v2

## Status

~~~text
STATUS = FROZEN_BEFORE_MISMATCH_PARTICIPATION_EFFECT
SOURCE = EPHI_ZENODO_10.5281/zenodo.14185547
PRIMARY_QUESTION = DOES_ACCESS_BARRIER_CHANGE_TOTAL_EXPLOITATION_RATE
ROUTING_RESULT = ALREADY_ESTABLISHED_OBSERVATIONALLY
PARTICIPATION_EFFECT = NOT_YET_OPENED
~~~

The current Letter establishes that, conditional on observed exploitation, greater
legitimate-route mismatch is associated with greater bypass use. That result alone
cannot show whether total exploitation is preserved, reduced or increased.

This analysis freezes the missing participation layer before its mismatch effect is
computed.

## 1. Opportunity denominator

No global bird x plant cross-product is allowed.

The primary opportunity unit is:

~~~text
clean camera waypoint
x
target bird species locally available in the same site
during a valid clean-camera interval
~~~

### 1.1 Clean-camera gate

Use only camera rows with:

- nonblank waypoint, site and plant species;
- parseable start and end dates;
- positive finite `duration_sampling_hours`;
- `camera_problem = no`.

Source metadata define `no` as no camera problem. All other camera-problem states,
including blank/unknown, are excluded from the primary denominator.

`camera_flowers_count` is not imputed because the source metadata explicitly state
that it is unavailable for Ecuador.

### 1.2 Local bird availability

A target bird is locally available for a focal waypoint when the species was
observed at any **clean-camera waypoint** in the same site during at least one valid
focal-waypoint interval.

Availability ignores piercing outcome and feeding outcome. Thus the response cannot
define its own zero set.

Target birds are Trochilidae plus *Diglossa*, matching the Letter.

### 1.3 Trait matching

Use the same trait definitions as the Letter:

~~~text
M = log(flower tube cm / bird culmen cm)
Barrier = M > 0
~~~

Plant tube length uses the site-specific mean with species-level fallback. Bird
culmen uses the species mean in mm divided by 10.

Only trait-matched opportunities enter effect estimation.

## 2. Participation response

The primary exploitation count for each opportunity is the number of target-bird
records at the focal waypoint during its valid clean-camera interval satisfying:

- `feeding_activity != no_feeding`;
- piercing status `yes` or `no`, with blank/NA recoded to `no` under the same
  source-metadata rule used by the Letter;
- distinct `maybe`, `thief` and `not_interacting` states excluded.

This makes the participation numerator the total count underlying the same
legitimate-versus-robbery route universe used by the Letter, except that explicit
nonfeeding observations are removed from exploitation.

Two point-estimate sensitivities are frozen:

1. **strict feeding** — feeding activity must be explicitly `hoverflying`,
   `perching`, or `perching,hoverflying`;
2. **broad feeding** — count feeding records including `maybe` and `thief`, but
   exclude explicit `no_feeding` and `not_interacting`.

Sensitivities do not determine the primary conclusion class.

## 3. Primary two-way fixed-effect model

For waypoint (w) and locally available bird species (b),

[
Y_{wb} sim mathrm{Poisson}(mu_{wb}),
]

[
log mu_{wb}
=
alpha_w + gamma_b + eta X_{wb},
]

where:

- (alpha_w) is a waypoint fixed effect;
- (gamma_b) is a bird-species fixed effect;
- (X_{wb}=1) if tube length exceeds culmen and 0 otherwise.

The waypoint effect absorbs camera effort, flower abundance, plant individual,
plant species, site and other waypoint-level intensity differences. Because every
bird opportunity within one waypoint shares the same camera exposure, no additional
camera-hours offset is needed after conditioning on (alpha_w).

The bird effect absorbs overall species abundance and baseline interaction
propensity.

The estimand is

[
RR_P = exp(eta),
]

the barrier/access ratio in **total route-resolved exploitation rate** after
controlling waypoint and bird main effects.

Structural opportunities outside the frozen local bird pool are absent from the
matrix rather than encoded as zeros.

The model is fit by iterative proportional fitting / log-linear maximum likelihood.

## 4. Fail-closed support gate

Before the effect is emitted, the constructed primary matrix must contain at least:

~~~text
trait-matched opportunity edges >= 10,000
positive-count edges >= 3,000
zero-count edges >= 3,000
clean waypoints >= 1,000
bird species >= 20
plant-species clusters >= 30
barrier edges > 0
accessible edges > 0
~~~

The model must converge with finite (eta).

Failure yields `RESULT_NOT_OPENED_SUPPORT_GATE_FAILED`; no alternative denominator
is searched after seeing mismatch effects.

## 5. Dependence and uncertainty

The point estimate includes waypoint and bird fixed effects.

Uncertainty is clustered at **plant species**, matching the current Letter's primary
inferential grain. A delete-one-plant-species jackknife is applied to (eta).

Every delete-one-plant fit must converge. Otherwise the equivalence decision is
withheld as `JACKKNIFE_UNSTABLE`.

Report:

- 95% jackknife-Wald CI for (RR_P);
- 90% jackknife-Wald CI for the prespecified equivalence test.

## 6. Frozen equivalence margin and outcome classes

Before opening the effect, define a material-change margin:

~~~text
participation-rate equivalence = 0.80 to 1.25
~~~

This 20% rate margin is a pragmatic manuscript decision threshold, not a universal
biological constant.

Classification:

### ROUTING_WITHOUT_MATERIAL_PARTICIPATION_LOSS

The 90% CI for (RR_P) lies wholly inside [0.80, 1.25].

### PARTICIPATION_REDUCTION_PLUS_ROUTING

The 95% CI lies wholly below 1.

Also flag `MATERIAL_SUPPRESSION` when the 95% upper bound is below 0.80.

### PARTICIPATION_INCREASE_PLUS_ROUTING

The 95% CI lies wholly above 1.

Also flag `MATERIAL_ENHANCEMENT` when the 95% lower bound exceeds 1.25.

### PARTICIPATION_UNRESOLVED_ROUTING_ESTABLISHED

None of the above.

The already frozen routing result remains positive regardless of participation class.

## 7. Manuscript language gate

If `ROUTING_WITHOUT_MATERIAL_PARTICIPATION_LOSS` is recovered, the Ecuador result
may be described as rerouting without a material loss of total exploitation over the
prespecified margin.

If `PARTICIPATION_REDUCTION_PLUS_ROUTING` is recovered, wording such as
"reroute rather than eliminate exploitation" must be replaced by **suppression plus
rerouting**.

If `PARTICIPATION_INCREASE_PLUS_ROUTING` is recovered, wording becomes
**amplification plus rerouting**.

If participation is unresolved, the Letter retains the routing result but states
that the total-exploitation consequence is unresolved.

No class licenses a causal evolutionary defence claim.

## 8. Outcome-blind denominator audit

Before this freeze, the clean-camera audit established feasibility without computing
a mismatch-participation effect:

~~~text
clean eligible waypoints = 5,254
trait-matched potential dyads = 20,270
trait-matched positive dyads = 6,519
trait-matched zero dyads = 13,751
camera_flowers_count for Ecuador = unavailable
~~~

The final model rebuilds the matrix under the stricter clean-camera local-pool rule
above before opening (eta).

## 9. Claim boundary

This is an observational decomposition of interaction intensity and route
composition. It does not establish why birds choose routes, that geometry was
selected as defence, or the prospective causal route-cost mechanism.
