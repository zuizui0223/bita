# Trait-barrier hysteresis / cross-species breach test v1

Status: **FROZEN BEFORE TEMPORAL OUTCOME OPENING**

Frozen on: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Question

Is bird–flower trait mismatch a fixed interaction barrier, or can an earlier visitor
change the effective barrier faced by later species?

The focal mechanism is persistent floral damage. Primary nectar robbers create an
access hole that remains until the flower wilts; later visitors can use the existing
hole as secondary robbers. That mechanism is old. The unresolved prediction tested
here is stronger:

> a trait barrier should have **memory**. After another species breaches the flower,
> the same bill–tube mismatch should no longer imply the same effective access state.

This is a temporal/hysteretic alternative to a static trait-matching model.

## Prior-literature boundary

Already known and therefore not claimable:
- primary and secondary nectar robbery exist;
- holes made by primary robbers can facilitate later secondary robbers;
- cross-species use and social transmission of robbing routes occur in bees;
- Aubert et al. 2026 show bill–tube mismatch predicts bird robbery.

The source Aubert study explicitly states that it is unknown how much flowerpiercers
facilitated hummingbird robbery and that its sampling/analysis did not distinguish
primary from secondary robbery.

## Frozen data

EPHI Ecuador public camera and interaction tables:
Zenodo 10.5281/zenodo.14185547 / Dryad 10.5061/dryad.rn8pk0pqx.

Trait definitions remain identical to BITA:
- flower tube = site-specific mean `Tubelength` in cm, species mean fallback;
- bird bill = species mean `culmen_length` in mm / 10;
- mismatch = `log(tube / bill)`;
- trait barrier = tube > bill.

Route coding remains identical to the current metadata-informed BITA primary rule:
- `piercing=yes` = robbing route;
- `piercing=no` = legitimate route;
- blank/NA piercing = legitimate;
- nonbinary route states excluded;
- `feeding_activity=no_feeding` excluded.

## Deployment construction

Use clean camera deployments only:
- `camera_problem=no`;
- parseable start and end date/time;
- positive `duration_sampling_hours`;
- a unique waypoint/site/plant identity;
- interaction timestamp falls within the deployment interval.

If more than one camera row produces overlapping candidate intervals for one
interaction, exclude the ambiguous interaction rather than assigning it post hoc.

Primary analysis includes all eligible deployments.
A prespecified high-specificity sensitivity uses only deployments with
`camera_flowers_count = 1`.

## Breach event

The treatment time `t0` is the **first observed Diglossa feeding interaction with
`piercing=yes`** within an eligible deployment.

This is a proxy for observed breach availability, not proof that this exact visit
created the first physical hole. The manuscript must retain that distinction.

Eligibility for the primary temporal comparison:
- at least 12 h of observed clean-camera time before t0;
- at least 12 h after t0;
- no earlier observed Diglossa `piercing=yes` in that deployment.

Primary symmetric window:
```text
[t0 - 12 h, t0) versus (t0, t0 + 12 h]
```

Frozen sensitivities:
- +/- 6 h;
- +/- 24 h when camera coverage permits;
- `camera_flowers_count = 1`.

The event at t0 itself is not part of the hummingbird outcome.

## Primary outcome

Restrict outcomes to Trochilidae, excluding Diglossa.

For every deployment/window, count **barrier hummingbird robbery events**:
Trochilidae feeding events for bird–plant pairs with tube > bill and route =
`piercing=yes`.

Because pre and post windows have equal duration, define

```text
Delta_R_barrier =
N(post barrier hummingbird robbery)
-
N(pre barrier hummingbird robbery)
```

Primary hypothesis:

```text
Delta_R_barrier > 0
```

If prior breach changes the effective access state, robbery by morphologically
mismatched hummingbirds should become more frequent immediately after the observed
flowerpiercer breach.

## Primary negative-control event

Construct the same +/-12 h statistic around the **first observed legitimate Diglossa
feeding event (`piercing=no`) in deployments with no observed Diglossa piercing
event before or within the +12 h outcome window**.

Define:

```text
Delta_R_barrier_control
```

The primary contrast is the difference in temporal changes:

```text
H =
mean(Delta_R_barrier | Diglossa breach)
-
mean(Delta_R_barrier_control | Diglossa legitimate control)
```

Prediction:

```text
H > 0
```

This negative control distinguishes a generic "Diglossa appeared / time passed"
effect from a breach-specific temporal signature.

## Inference

Primary randomization unit = deployment.

Pool the eligible breach and control deployments, preserve the observed number of
breach deployments within site, and permute breach/control labels within site
(99,999 fixed-seed permutations, seed 20261007).

Primary one-sided p-value:
fraction of permuted H >= observed H, with plus-one correction.

Also report:
- two-sided permutation p;
- bootstrap 95% interval over deployments;
- median and mean deployment-level changes;
- number of sites, plant species, deployments, pre/post hummingbird events.

If too few sites contain both breach and control deployments for the site-stratified
permutation, report the gate failure. Do not replace it with an unplanned pooled test
as the primary analysis.

## Mechanistic secondary outcomes

These are ordered and cannot replace a failed primary result.

### S1 — route specificity

Repeat the temporal difference-in-differences for:
- barrier hummingbird legitimate events;
- accessible hummingbird robbery events.

Expected physical-breach signature:
- strongest positive shift in barrier hummingbird robbery;
- no matching positive shift required for legitimate visits.

### S2 — conditional route choice

Among resolved hummingbird feeding interactions in the same windows, compare change
in robbery share before versus after. This is secondary because it conditions on an
interaction and can be denominator-driven.

### S3 — cross-species evidence

For each breach deployment, flag whether at least one post-breach robbery event is
made by a hummingbird species different from every bird taxon recorded robbing before
t0. This is descriptive evidence for a community-level route opening, not proof of
secondary robbery.

### S4 — participation

Using the existing zero-inclusive site/date availability rule, test whether the number
of barrier hummingbird species with >=1 feeding interaction increases after breach.
This is supportive only because local availability is coarsely inferred.

## Falsification / claim rule

Promote trait-barrier hysteresis only if:
1. primary H > 0;
2. the direction persists in the single-flower sensitivity whenever that sensitivity
   has >=10 breach deployments;
3. the breach effect is larger for barrier hummingbirds than for accessible
   hummingbirds.

If those conditions fail, do not claim a history-dependent trait barrier from these
data.

Allowed claim if supported:

> Floral access is not determined solely by current bird and flower traits. A prior
> visitor can leave a persistent access route that changes how later, morphologically
> mismatched species interact with the same floral resource.

Prohibited claims:
- direct identification of primary versus secondary robbery for individual EPHI events;
- causal proof that the first observed Diglossa piercing created the used hole;
- social learning unless directly observed;
- calling a temporal association a manipulated causal effect.
