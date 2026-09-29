# Relative-route-cost factorial experiment preregistration v1

## Status

~~~text
STATUS = PRE_OUTCOME_CAUSAL_DESIGN
PRIMARY_THEORY = RELATIVE_ROUTE_COST
SYSTEM = ARTIFICIAL_FLOWER_ROUTE_CHOICE
VISITOR = BUMBLEBEE_FORAGER
PRIMARY_UNIT = INDIVIDUAL_BEE
PRIMARY_GOAL = PROSPECTIVE_SIGN_REVERSAL_TEST
BENCH_HARDWARE_GATE_REQUIRED = YES
CALIBRATION_COMPLETED_BEES_MIN = 20
CALIBRATION_SUCCESSFUL_TRIALS_PER_STATE_PER_BEE = 5
CONFIRMATORY_CHOICE_SAMPLE = 60_COMPLETED_BEES
CONFIRMATORY_COLONIES_MIN = 3
MAX_COMPLETED_BEES_FROM_ONE_COLONY = 30
TRIALS_PER_CONDITION_PER_BEE = 10
PERMUTATIONS = 9999
~~~

This protocol turns the current BITA mechanistic interpretation into a prospective
causal test. It does **not** alter the observational Ecology Letters Letter.

## 1. Theory to be tested

Let

~~~text
C_L = cost of the legitimate access route
C_B = cost of the bypass route
D   = C_L - C_B
~~~

The relative-route-cost model predicts that bypass propensity increases with
`D`, not simply with absolute barrier strength.

The decisive 2 x 2 predictions are:

~~~text
L low,  B low   -> baseline route composition
L high, B low   -> bypass increases
L low,  B high  -> bypass decreases
L high, B high  -> route composition returns near baseline if cost increments match
~~~

The first two contrasts are the primary sign-reversal test. The fourth condition
is the strongest diagnostic against an absolute-barrier interpretation.

## 2. Experimental platform

Use an artificial flower with one reward reservoir that can be reached by two
simultaneously available routes:

- **legitimate route:** entry from the floral top/opening;
- **bypass route:** entry from a lateral port that avoids the legitimate opening.

The two routes must access the same reward reservoir, so treatment effects cannot
be created by reward quantity or quality.

Route entrances should retain the same visible colour and external cue geometry
across low- and high-cost states. Cost manipulation should occur primarily in the
post-entry access geometry (for example reach distance or internal path length),
rather than by making one route visually easier to discover.

The platform is motivated by prior artificial-flower work in which bumblebees
could choose legitimate top access or lateral nectar robbery. BITA adds independent
manipulation of the two route costs.

The confirmatory platform uses an already available lateral bypass. It therefore
tests **route choice conditional on bypass availability**, analogous to secondary
nectar robbing, and does not identify the separate decision or mechanics of creating
a new primary robbing hole. Balanced familiarization is required because prior
experience with robbed flowers can itself alter later robbing behaviour.

## 3. Stage -1 — hardware bench QC

Before any bee is exposed to a prototype, the physical platform must pass the
engineering gate defined in:

- RELATIVE_ROUTE_COST_FLOWER_HARDWARE_SPEC_V1.md;
- RELATIVE_ROUTE_COST_FLOWER_MODULE_MANIFEST_TEMPLATE_V1.csv;
- RELATIVE_ROUTE_COST_FLOWER_BENCH_QC_SCHEMA_V1.csv;
- scripts/validate_relative_route_cost_hardware.py.

The hardware gate requires:

~~~text
>=4 measured flower bodies
dimension tolerance pass for every referenced body and insert
>=20 repeated reward loads for every assembly entering Stage 0
0 entrance wetting events
0 spontaneous overflow events
0 cross-route leakage events
shared reservoir confirmed
both route-isolation shutters pass
external cue identity pass
cleaning compatibility pass
~~~

Passing Stage -1 establishes engineering readiness only. It does not establish that
the nominal low/high path lengths create matched biological route costs.

No Stage-0 bee may be exposed until the hardware validator returns:

~~~text
passes_stage0_hardware_gate = true
~~~

## 4. Stage 0 — outcome-blind biological calibration

All Stage-0 flowers are route-isolated. No Stage-0 bee ever sees simultaneous route
choice, and no Stage-0 bee may enter Stage 1.

### 4.1 Stage 0A — full candidate sweep

Stage 0A maps the biological handling cost of the engineering distance grid before
any low/high pair is chosen.

Use two disjoint calibration cohorts:

~~~text
legitimate-route cohort: >=12 bees
bypass-route cohort:     >=12 different bees
~~~

Each bee experiences only its assigned route and must receive at least three attempts
at every candidate effective access distance:

~~~text
2, 3, 4, 5, 6, 7, 8, 9, 10 mm
~~~

Distance order is randomized or counterbalanced within bee. Success/failure and
handling time are recorded for every attempt.

Stage-0A candidate data are stored in
RELATIVE_ROUTE_COST_CANDIDATE_SWEEP_SCHEMA_V1.csv and opened only through
scripts/select_relative_route_cost_candidates.py.

### 4.2 Deterministic low/high selection

Candidate selection is mechanical rather than analyst-chosen.

For each route, a candidate low/high pair must satisfy:

~~~text
high distance > low distance
>=12 eligible bees
screening success rate >=0.80 at both distances
mean high-minus-low log handling time >=0.20
~~~

Cross-route pairs must also satisfy:

~~~text
0.80 <= Delta_L / Delta_B <= 1.25
~~~

If multiple joint pairs remain, select exactly one using this frozen order:

1. minimize absolute log(Delta_L / Delta_B);
2. maximize the minimum success rate across the four selected states;
3. minimize the sum of the two high distances;
4. break any remaining tie lexicographically by L-low, L-high, B-low, B-high.

The selected pair is still an engineering candidate, not a frozen manipulation.

### 4.3 Stage 0B — fresh-bee freeze validation

Re-test only the selected four states on at least 20 new calibration bees that were
not used in Stage 0A and will never enter Stage 1.

Each Stage-0B bee contributes at least five successful trials in each state:

~~~text
legitimate low
legitimate high
bypass low
bypass high
~~~

State order is randomized or counterbalanced so handling-time increments are not
confounded with experience.

Primary engineering cost proxy:

~~~text
log handling time from first physical route contact to reward acquisition
~~~

For each bee, compute high-minus-low log handling-time differences and aggregate:

~~~text
Delta_L = high - low cost increment for legitimate route
Delta_B = high - low cost increment for bypass route
~~~

### 4.4 Freeze gate

A geometry version can be frozen only if Stage 0B independently confirms:

1. Delta_L >= 0.20 log-time units;
2. Delta_B >= 0.20 log-time units;
3. success rate >=0.90 in all four isolated-route states;
4. 0.80 <= Delta_L / Delta_B <= 1.25.

If Stage 0B fails, the geometry version fails. Do not choose a second-best Stage-0A
pair after seeing the failed Stage-0B result. A redesign requires a new geometry
version and a new Stage-0A sweep.

Freeze before Stage 1:

- selected low/high dimensions for both routes;
- all physical dimensions;
- reward concentration and volume;
- route-cue colours/materials;
- Stage-0A input/result hashes;
- Stage-0B calibration input/result hashes;
- flower CAD/design-file hash if applicable;
- final Delta_L and Delta_B.

## 5. Stage 1 — confirmatory route-choice experiment

### 5.1 Experimental units

Primary inferential unit: **individual bee**.

Target:

~~~text
60 completed bees
10 valid choice trials per condition per bee
4 conditions
40 valid choice trials per completed bee
2400 valid choice trials total
~~~

Recruitment continues until 60 bees satisfy the completion rule. Bees excluded
under the predeclared rules are replaced, but their exclusion reasons remain in the
audit table.

### 5.1.1 Sample-size planning

The frozen planning simulation is
`RELATIVE_ROUTE_COST_FACTORIAL_POWER_PLAN_V1.json`. Under 10 trials per condition,
baseline bypass probability 0.40 and a bee-level random-intercept SD of 0.8 on the
logit scale, a symmetric logit shift of 0.45 generated mean route-share contrasts of
approximately +0.097 and -0.092 and an approximate 0.887 probability that both
primary contrasts passed the planning criterion. A shift of 0.55 generated
approximately +0.119 and -0.111 with pass probability 0.982.

These values are **planning sensitivity only**. They do not define an expected effect
size, do not enter confirmatory inference, and do not justify post-outcome sample-size
changes.

Use at least three colonies. No single colony may contribute more than 30 of the
60 completed bees. Colony identity is retained for a prespecified descriptive
sensitivity; the primary estimand remains the within-bee treatment effect. This
design licenses inference to the sampled foragers, not a population-level estimate
of among-colony heterogeneity.

### 5.2 Familiarization

Before confirmatory trials, each bee receives four successful legitimate and four successful bypass familiarization trials using low-cost route-isolated training flowers. Route order is counterbalanced across bees.

No high/low treatment comparison is shown during familiarization.

### 5.3 Choice treatments

Each confirmatory flower has both routes open.

~~~text
condition  L cost  B cost
LL         low     low
HL         high    low
LH         low     high
HH         high    high
~~~

Each bee receives 10 valid trials in every condition.

Treatment order is randomized within 10 blocks with exactly one presentation of
each of the four conditions per block. The schedule is generated before route-choice
outcomes with `scripts/generate_relative_route_cost_randomization.py`. Physical
flower position and flower-module identity are counterbalanced.

Reward volume, concentration, replenishment state, odour, illumination and external
visual route cues are held constant.

### 5.4 Primary route outcome

For each valid trial:

~~~text
Y = 1  first successful reward acquisition is through bypass
Y = 0  first successful reward acquisition is through legitimate route
~~~

A bee may inspect or contact both routes before success. First contact is recorded
as a secondary behavioural variable and does not replace the primary acquisition
route.

### 5.5 Trial exclusions

Exclude a trial only if one of the following is logged before route outcome is
opened for analysis:

- reward delivery failure;
- flower-module mechanical failure;
- video loss preventing route coding;
- bee does not contact either route within the predeclared trial timeout;
- external disturbance requiring experimenter intervention.

Do not exclude a trial because the bee chose an unexpected route, switched routes,
or had a long handling time.

## 6. Primary bee-level estimands

For each bee, calculate bypass proportion in each condition:

~~~text
p_LL, p_HL, p_LH, p_HH
~~~

Primary causal contrasts:

~~~text
C_L = mean_bee(p_HL - p_LL)
C_B = mean_bee(p_LH - p_LL)
~~~

Predictions:

~~~text
C_L > 0
C_B < 0
~~~

Inference uses bee-level sign-flip randomization with 9,999 permutations.

Because two directional primary contrasts are tested, each must pass:

~~~text
one-sided p < 0.025
~~~

The mechanism passes the primary sign-reversal test only if **both** directional
contrasts pass.

## 7. Compensation diagnostic

Secondary predeclared contrast:

~~~text
C_HH = mean_bee(p_HH - p_LL)
~~~

The matched-cost prediction is approximate equivalence rather than a point null.

Equivalence margin:

~~~text
-0.10 <= C_HH <= +0.10
~~~

A 95% bee-level bootstrap interval is reported. The compensation diagnostic is
supported only if the entire interval lies inside the +/-0.10 route-share margin.

Failure of this equivalence diagnostic does not retroactively erase a successful
primary sign reversal; it indicates imperfect cost matching, interaction between
routes, or an incomplete relative-cost model.

## 8. Secondary outcomes

Report, without promoting them to primary endpoints:

- route first contacted;
- number of route switches before reward acquisition;
- handling time;
- acquisition failure / abandonment;
- trial order;
- bout number;
- flower module;
- colony.

A useful suppression prediction is that `HH` may increase total handling time or
abandonment even when route composition is similar to `LL`.

## 9. Confirmatory decision rule

~~~text
PRIMARY_RELATIVE_ROUTE_COST_SUPPORT =
    (C_L > 0 and one-sided p_L < 0.025)
    AND
    (C_B < 0 and one-sided p_B < 0.025)
~~~

Report the result even if one or both signs fail.

No geometry, exclusion rule, equivalence margin, minimum trial count, or primary
contrast may be changed after the first Stage-1 route-choice outcome is observed.

## 10. Interpretation ladder

If both primary contrasts pass:

> Independent manipulation of legitimate- and bypass-route costs caused opposite
> shifts in route choice, supporting relative route cost as a causal determinant of
> interaction routing in this experimental system.

If only the legitimate-route contrast passes:

> Increasing legitimate-route cost increased bypass use, but the experiment did not
> establish the predicted sign reversal when bypass cost itself was increased.

If the signs fail:

> The relative-route-cost mechanism was not supported under the frozen manipulation.

Even a full pass does not license a universal law across taxa or interaction types.

## 11. Relation to the current Letter

This experiment is a prospective mechanism test, not a hidden requirement for the
current Ecology Letters submission.

The current Letter remains:

~~~text
STANDARDIZED_OBSERVATIONAL_NETWORK_K = 2
CASE_PUBLISHED_DIRECTIONAL_CORROBORATION = YES
CAUSAL_ROUTE_COST_SIGN_REVERSAL = NOT_YET_TESTED
~~~

A completed experiment can be reported later as direct causal validation or as a
separate mechanism paper.


## 12. Experimental precedent

- Leonard AS, Brent J, Papaj DR, Dornhaus A (2013) Floral Nectar Guide Patterns
  Discourage Nectar Robbing by Bumble Bees. *PLoS ONE* 8:e55914.
  DOI 10.1371/journal.pone.0055914. Artificial flowers allowed legitimate top
  access and lateral robbery in the same foraging system.
- Leadbeater E, Chittka L (2008) Social transmission of nectar-robbing behaviour
  in bumble-bees. *Proceedings of the Royal Society B* 275:1669–1674.
  DOI 10.1098/rspb.2008.0270. Artificial flowers with pre-cut robbing holes
  demonstrate that route experience can alter later robbing behaviour.

These studies establish platform feasibility. They do not test the BITA
independent `C_L x C_B` manipulation.
