# Relative-route-cost factorial experiment preregistration v1

## Status

~~~text
STATUS = PRE_OUTCOME_CAUSAL_DESIGN
PRIMARY_THEORY = RELATIVE_ROUTE_COST
SYSTEM = ARTIFICIAL_FLOWER_ROUTE_CHOICE
VISITOR = BUMBLEBEE_FORAGER
PRIMARY_UNIT = INDIVIDUAL_BEE
PRIMARY_GOAL = PROSPECTIVE_SIGN_REVERSAL_TEST
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

## 3. Stage 0 — outcome-blind engineering calibration

Calibration uses bees that will never enter the confirmatory choice experiment.

### 3.1 Route-isolated flowers

For calibration, only one route is available at a time. Four engineering states
are therefore measured:

~~~text
legitimate low
legitimate high
bypass low
bypass high
~~~

No flower in Stage 0 presents a route choice. Use at least 20 completed calibration bees, each contributing at least five successful trials in each of the four isolated-route states. Randomize or counterbalance the order of route and cost states so calibration increments are not confounded with experience.

### 3.2 Calibration response

Primary engineering cost proxy:

~~~text
log handling time from first physical route contact to reward acquisition
~~~

Only successful acquisitions enter the handling-time calibration. Failure rate is
recorded separately.

For each bee, compute high-minus-low log handling-time differences for the route
it experienced. Aggregate across calibration bees to obtain:

~~~text
Delta_L = high - low cost increment for legitimate route
Delta_B = high - low cost increment for bypass route
~~~

### 3.3 Freeze gate

A geometry version can be frozen only if:

1. `Delta_L > 0`;
2. `Delta_B > 0`;
3. success rate is at least 0.90 in all four isolated-route states;
4. the matched-cost ratio satisfies

~~~text
0.80 <= Delta_L / Delta_B <= 1.25
~~~

If the gate fails, geometry may be adjusted using Stage-0 data only. Each geometry
revision receives a new version identifier. No confirmatory bee may be observed
until one version passes and is frozen.

Freeze before Stage 1:

- all physical dimensions;
- reward concentration and volume;
- route-cue colours/materials;
- calibration dataset hash;
- flower CAD/design-file hash if applicable;
- the final `Delta_L` and `Delta_B`.

## 4. Stage 1 — confirmatory route-choice experiment

### 4.1 Experimental units

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

Use at least three colonies. No single colony may contribute more than 30 of the
60 completed bees. Colony identity is retained for a prespecified descriptive
sensitivity; the primary estimand remains the within-bee treatment effect. This
design licenses inference to the sampled foragers, not a population-level estimate
of among-colony heterogeneity.

### 4.2 Familiarization

Before confirmatory trials, each bee receives four successful legitimate and four successful bypass familiarization trials using low-cost route-isolated training flowers. Route order is counterbalanced across bees.

No high/low treatment comparison is shown during familiarization.

### 4.3 Choice treatments

Each confirmatory flower has both routes open.

~~~text
condition  L cost  B cost
LL         low     low
HL         high    low
LH         low     high
HH         high    high
~~~

Each bee receives 10 valid trials in every condition.

Treatment order is randomized within blocks with equal representation of all four
conditions. Physical flower position and flower-module identity are counterbalanced.

Reward volume, concentration, replenishment state, odour, illumination and external
visual route cues are held constant.

### 4.4 Primary route outcome

For each valid trial:

~~~text
Y = 1  first successful reward acquisition is through bypass
Y = 0  first successful reward acquisition is through legitimate route
~~~

A bee may inspect or contact both routes before success. First contact is recorded
as a secondary behavioural variable and does not replace the primary acquisition
route.

### 4.5 Trial exclusions

Exclude a trial only if one of the following is logged before route outcome is
opened for analysis:

- reward delivery failure;
- flower-module mechanical failure;
- video loss preventing route coding;
- bee does not contact either route within the predeclared trial timeout;
- external disturbance requiring experimenter intervention.

Do not exclude a trial because the bee chose an unexpected route, switched routes,
or had a long handling time.

## 5. Primary bee-level estimands

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

## 6. Compensation diagnostic

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

## 7. Secondary outcomes

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

## 8. Confirmatory decision rule

~~~text
PRIMARY_RELATIVE_ROUTE_COST_SUPPORT =
    (C_L > 0 and one-sided p_L < 0.025)
    AND
    (C_B < 0 and one-sided p_B < 0.025)
~~~

Report the result even if one or both signs fail.

No geometry, exclusion rule, equivalence margin, minimum trial count, or primary
contrast may be changed after the first Stage-1 route-choice outcome is observed.

## 9. Interpretation ladder

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

## 10. Relation to the current Letter

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
