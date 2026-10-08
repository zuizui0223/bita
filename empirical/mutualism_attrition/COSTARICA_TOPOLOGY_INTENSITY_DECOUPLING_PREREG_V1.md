# Costa Rica cheating topology–intensity decoupling validation v1

Status: **FROZEN BEFORE COSTA RICA OUTCOME OPENING**
Date: 2026-10-08
Branch: `analysis/costarica-topology-intensity-decoupling-v1`

## Why this is an independent validation

The Ecuador cross-fit was already opened on 2026-10-08. It showed a post-outcome
pattern in which cheating share was strongly reproducible across disjoint camera
subsets, zero-inclusive interaction occupancy was positive, while total event flux
was weakly negative.

Costa Rica has not been opened for this cross-fit question in BITA. It is sampled in
a different country and set of sites within the same EPHI programme and is therefore
used as the independent geographic validation dataset.

Fixed public sources:
- `Interactions_data_Costa-Rica.txt`
- `Cameras_data_Costa-Rica.txt`
- common `Plant_traits.txt`
- common `Hummingbird_traits.txt`
from Zenodo 10.5281/zenodo.14185547.

## Prior-art boundary

Already known:
- binary and weighted ecological networks can yield different structural conclusions;
- nectar robbers can add links and alter network topology;
- Duchenne et al. (2023, doi:10.1371/journal.pbio.3002434) showed theoretically that
  innovative cheating can increase community persistence under restricted conditions;
- that study parameterized empirical networks using a binary mutualistic backbone,
  while cheating frequency was a proportion of illegitimate interactions.

Not claimed as new:
- the binary-versus-weighted network distinction;
- first evidence of nectar robbery;
- first evidence that cheaters alter topology;
- direct measurement of species persistence.

## Hypothesis

### H1 — cheating topology–intensity decoupling

A plant can become more broadly used in a binary/topological sense while its weighted
interaction throughput does not increase and can decline, because cheating opens
additional routes that are individually weak and displace legitimate interactions.

In a disjoint-sample cross-fit:

~~~text
higher cheating share in predictor fold
  -> higher zero-inclusive ANY-interaction occupancy in outcome fold
  -> lower total interaction flux per camera-hour in outcome fold
~~~

Route decomposition:

~~~text
higher cheating share
  -> lower legitimate flux
  -> higher robbery flux
~~~

This is a cross-scale property of interaction realization, not a claim about plant
fitness or species persistence.

## Frozen sample split

Use exactly the prior Ecuador cross-fit rule:

~~~text
FNV1a32(raw waypoint UTF-8)
fold A if hash mod 2 == 0
fold B if hash mod 2 == 1
~~~

No waypoint can contribute to predictor and outcome in the same directional test.

Primary target animals:
- Trochilidae hummingbirds;
- no additional taxon is added if absent in Costa Rica.

Primary route coding:
- `piercing=yes` = robbery;
- `piercing=no` and blank/NA = legitimate, matching source metadata;
- nonbinary route states excluded;
- explicit `feeding_activity=no_feeding` excluded.

Clean-camera and valid-date rules are unchanged from the frozen EPHI participation
denominator audit.

## Plant eligibility

For each directional test A->B and B->A require:

1. >=2 clean predictor-fold waypoints;
2. >=2 clean outcome-fold waypoints;
3. >=5 resolved feeding events in predictor fold;
4. positive outcome camera-hours;
5. at least one trait-matched zero-inclusive opportunity in the outcome fold.

The primary validation requires >=20 eligible plants in both directions. If either
direction has fewer than 20, the validation is underpowered and no claim is promoted.

## Predictor

For plant i in predictor fold:

~~~text
C_i = robbery / (robbery + legitimate)
~~~

## Two co-primary outcome axes

Both are calculated in the disjoint outcome fold.

### Topological / occupancy response

~~~text
O_i =
number of locally-available bird x waypoint opportunities
with >=1 resolved feeding event
/
number of locally-available bird x waypoint opportunities
~~~

This is zero-inclusive.

### Weighted / intensity response

~~~text
F_i =
(resolved robbery + legitimate events)
/
clean camera sampling hours
~~~

Use `log1p(F_i)` for rank correlation as in the Ecuador preregistration.

## Directional statistics

For each A->B and B->A:

~~~text
rho_O = Spearman(C_predictor, O_outcome)
rho_F = Spearman(C_predictor, log1p(F_outcome))
~~~

Combine directions separately with equal-fold Fisher-z means:

~~~text
rho_OX
rho_FX
~~~

Define the decoupling statistic on Fisher-z scale:

~~~text
D =
mean_z(rho_O_AtoB, rho_O_BtoA)
-
mean_z(rho_F_AtoB, rho_F_BtoA)
~~~

where positive D means cheating share predicts relatively more topological occupancy
than weighted flux.

## Frozen primary prediction

### FULL_TOPOLOGY_INTENSITY_DECOUPLING

Require all:

1. `rho_OX > 0`;
2. `rho_FX < 0`;
3. D > 0;
4. both route-decomposition equal-fold statistics satisfy:
   - `rho_legitimate_X < 0`
   - `rho_robbery_X > 0`;
5. both signs `rho_OX > 0` and `rho_FX < 0` survive the >=10 predictor-event sensitivity.

Anything less is not a confirmatory replication of the Ecuador-discovered pattern.

## Primary inference

Use 99,999 permutations, seed 20261008.

Within each directional plant set, permute the predictor cheating-share labels
relative to the paired outcome vectors. For every permutation calculate both rho_O
and rho_F and then D using the same paired permutation.

Primary one-sided test:

~~~text
P_D = Pr(D_perm >= D_obs)
~~~

with plus-one correction.

Also report:
- one-sided p for `rho_OX > 0`;
- one-sided p for `rho_FX < 0`;
- 9,999 global plant-species bootstrap intervals for rho_OX, rho_FX and D.

The sign-based replication gate is frozen above; p-values quantify evidence strength
and must be shown regardless of whether the gate passes.

## Prespecified sensitivities

1. predictor minimum >=10 resolved events;
2. >=3 clean waypoints in each fold;
3. explicit yes/no piercing only;
4. within-site centered-rank versions of rho_O and rho_F.

No alternative waypoint split, event threshold, or occupancy denominator may replace
the primary analysis after outcome opening.

## Interpretation if supported

Allowed:

> Cheating can expand the realized binary interaction topology while weighted
> interaction throughput contracts. New cheating links therefore need not represent
> quantitative compensation for lost mutualistic interaction.

Stronger theoretical connection, allowed only as discussion:

> A binary interaction backbone can register ecological access that is not equivalent
> to strong interaction flux; models in which innovative cheating stabilizes
> communities should therefore distinguish link realization from interaction weight.

Not allowed:
- that Duchenne et al. (2023) is wrong;
- that binary networks are generally invalid;
- that reduced interaction flux means reduced plant fitness;
- that cheating causes the weighted contraction;
- that this establishes lower species persistence.

## Kill rule

If `rho_OX <= 0` or `rho_FX >= 0`, classify the Ecuador topology–intensity pattern
as not independently replicated in Costa Rica. Preserve the null/opposite result and
do not redefine topology or flux after opening.
