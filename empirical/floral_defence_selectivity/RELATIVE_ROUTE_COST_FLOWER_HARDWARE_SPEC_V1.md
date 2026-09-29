# Relative-route-cost artificial-flower hardware specification v1

## Status

~~~text
STATUS = PRE_BUILD_ENGINEERING_SPEC
BIOLOGICAL_OUTCOME_DATA = NONE
FINAL_LOW_HIGH_COST_LEVELS = NOT_YET_FROZEN
STAGE0_REQUIRED_BEFORE_CONFIRMATORY_CHOICE = YES
~~~

This document translates the preregistered relative-route-cost experiment into a buildable artificial-flower platform. It does not choose the final low/high route-cost levels. Those are selected only by Stage-0 handling-time calibration in the actual permitted bumblebee system.

## 1. Design objective

Build one artificial flower with:

1. one legitimate top entrance;
2. one lateral bypass entrance;
3. one shared reward reservoir;
4. independently exchangeable internal legitimate and bypass access-path inserts;
5. identical external visual entrances across low/high cost states.

The engineering target is:

~~~text
external flower appearance fixed
reward fixed
legitimate internal path variable
bypass internal path variable
~~~

The design tests route choice conditional on an already available bypass. It is analogous to secondary nectar robbing and does not model the biomechanics of creating a new primary robbing hole.

## 2. Literature-derived reference geometry

Leonard et al. (2013; DOI 10.1371/journal.pone.0055914) successfully elicited both legitimate and robbing behaviour from Bombus impatiens using artificial flowers with:

~~~text
floral-top diameter = 50 mm
floral-tube length  = 20 mm
nectar opening      = 2.5 mm diameter
reward              = 3.0 uL of 50% sucrose
~~~

Their flowers had separate top and side wells. BITA retains these dimensions only as an external feasibility reference and replaces the two wells with one shared reservoir reached through two independent channels.

Leadbeater & Chittka (2008; DOI 10.1098/rspb.2008.0270) further show that prior experience with robbed flowers changes later robbing behaviour. The BITA design therefore freezes balanced familiarization and blocked treatment order.

## 3. Flower body

### 3.1 External shell

Reference external dimensions:

~~~text
top-disc diameter              50.0 mm
visible tube length            20.0 mm
top entrance diameter           2.5 mm
lateral entrance diameter       2.5 mm
lateral entrance centreline     5.0 mm below top plane
~~~

The top and lateral entrances must retain the same diameter, colour, edge finish and external position across all four confirmatory conditions.

Allowed manufacturing tolerance before calibration:

~~~text
top-disc diameter           +/- 0.5 mm
visible tube length         +/- 0.5 mm
entrance diameter           +/- 0.1 mm
entrance-position offset    +/- 0.2 mm
internal path length        +/- 0.2 mm from manifest value
~~~

A module outside tolerance is rejected before bee exposure.

### 3.2 Shared reward reservoir

One central removable reservoir is loaded once per trial with:

~~~text
nominal volume = 3.0 uL
nominal sucrose concentration = 50% w/w
~~~

These values are the starting protocol because the Leonard et al. platform used 3.0 uL of 50% sucrose during foraging trials. They remain author-adjustable before the Stage-0 freeze if the permitted bee species requires a different absolute reward.

Both routes must terminate at the same physical reservoir. A route may not have a separate duplicate well.

The trial ends after the first successful acquisition. The reservoir is then cleaned/reloaded before reuse.

## 4. Internal path modules

### 4.1 Principle

Cost is altered by changing post-entry effective access distance, not entrance visibility.

Each entrance accepts a removable internal sleeve. The reward chamber remains fixed. The sleeve sets the length of the narrow guided tunnel through which the proboscis must travel immediately after crossing the externally identical 2.5-mm entrance. Thus the manipulated engineering quantity is guided-sleeve length, not the total straight-line distance from entrance to reward.

### 4.2 Engineering candidate grid

Before Stage 0, manufacture candidate inserts covering:

~~~text
guided sleeve length = 2, 3, 4, 5, 6, 7, 8, 9, 10 mm
~~~

in 1-mm steps for both routes.

The same candidate grid is available to legitimate and bypass channels. Stage 0 may select different absolute low/high distances for the two routes if necessary to make their handling-time increments comparable.

Do not define high cost from sleeve length alone. A candidate pair becomes low/high only if Stage-0 biological calibration shows the frozen handling-time increment.

### 4.3 Channel geometry

For every insert:

- entrance diameter remains 2.5 mm;
- internal channel centreline is fixed;
- channel material and surface finish are held constant;
- only effective access distance changes;
- no insert may protrude externally or create a visible colour/texture cue.

If a longer path requires a bend or taper, the same bend/taper must be present in both low and high variants except for the length increment. Prefer straight channels where possible.

## 5. Reward wetting / capillary-control requirement

Because both routes share one reservoir, liquid migration could accidentally shorten a route.

Before any bee calibration, each module/insert combination must pass:

~~~text
20 consecutive 3-uL bench loads
0 visible droplets at either entrance before probing
0 spontaneous overflow events
0 cross-route leakage events
~~~

After loading, inspect both entrances at the same fixed delay used in experiments.

If sucrose wets an entrance or channel wall far enough to alter effective access distance, that module fails and must be redesigned.

## 6. Route-isolation shutters

Stage 0 requires one route at a time.

Each entrance therefore needs an opaque internal shutter or plug that:

- blocks access without changing the visible external entrance;
- sits behind the entrance plane;
- uses the same exterior surface in open and closed states;
- cannot contact the reward reservoir.

The blocked route should look externally present but be physically inaccessible.

No Stage-0 flower presents simultaneous route choice.

## 7. Confirmatory four-state assembly

After one geometry version passes Stage 0, build four states from the frozen inserts:

~~~text
LL = legitimate low  + bypass low
HL = legitimate high + bypass low
LH = legitimate low  + bypass high
HH = legitimate high + bypass high
~~~

All four states must use interchangeable parts from the same manufacturing batch where possible.

At least four physical flower bodies should rotate among conditions so condition is not confounded with one unique flower module. Condition inserts are swapped according to the pre-generated randomization schedule.

## 8. Visual and olfactory controls

External route-choice cues are held constant:

- same top-disc colour;
- same tube colour;
- same entrance diameter;
- no condition-specific markings;
- no external spacer visibility;
- same illumination;
- same cleaning protocol;
- same elapsed time between cleaning and presentation.

Leonard et al. cleaned flowers between foraging trials to remove scent marks. BITA should likewise use one frozen cleaning protocol and record cleaning batch/time.

If the chosen manufacturing material is damaged by the cleaning solution, switch material before Stage 0 and issue a new geometry version.

## 9. Module identity and measurement

Every physical body and insert receives a unique identifier.

Before biological calibration, measure and record:

- body top diameter;
- visible tube length;
- top aperture diameter;
- lateral aperture diameter;
- lateral aperture vertical position;
- legitimate guided-sleeve length;
- bypass guided-sleeve length;
- module mass if useful for build QC;
- manufacturing batch;
- inspection date.

The manifest file is RELATIVE_ROUTE_COST_FLOWER_MODULE_MANIFEST_TEMPLATE_V1.csv.

A digital caliper with <=0.1-mm resolution is sufficient for the declared tolerance checks; finer optical measurement may be substituted.

## 10. Bench QC gate

No module enters Stage 0 unless all of the following are true:

~~~text
DIMENSION_TOLERANCE_PASS = YES
SHARED_RESERVOIR_PASS = YES
20_LOAD_CAPILLARY_TEST_PASS = YES
ROUTE_ISOLATION_SHUTTER_PASS = YES
EXTERNAL_CUE_IDENTITY_PASS = YES
CLEANING_COMPATIBILITY_PASS = YES
~~~

Bench QC is engineering validation only. It cannot replace Stage-0 biological handling-time calibration.

## 11. What remains intentionally unfrozen

Do not freeze until the actual permitted bee system and physical prototype exist:

- bee species;
- final low/high access distances;
- exact fabrication material;
- final cleaning solution;
- reward concentration/volume if the initial 50% / 3-uL reference proves unsuitable;
- exact Stage-0 geometry version.

Changing any of these after Stage 1 begins is prohibited.

## 12. Evidence boundary

The literature demonstrates that bumblebees can use artificial flowers via both legitimate top access and lateral robbery. It does not establish that the BITA 2 x 2 path-length manipulation will work.

The hardware therefore has three distinct gates:

~~~text
bench engineering QC
        ->
Stage-0 biological cost calibration
        ->
Stage-1 confirmatory route choice
~~~

Only the last stage can test the causal relative-route-cost prediction.
