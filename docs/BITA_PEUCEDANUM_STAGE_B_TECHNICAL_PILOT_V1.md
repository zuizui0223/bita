# BITA Peucedanum Stage-B technical pilot v1

## Purpose

Before freezing the confirmatory randomized `q x G` experiment, Stage B requires a small technical pilot that answers only whether the post-male-phase sex-composition manipulation is operationally feasible.

The pilot is **not** a miniature fitness experiment and should not be used to choose favorable confirmatory effect thresholds.

## Biological timing window

Primary studies establish the relevant sequence.

- Perfect and male flowers overlap during the male phase for roughly 4-5 days.
- Perfect flowers are protandrous: after anthers are shed, pistils elongate and the terminal umbel enters the female phase.
- Predator moths often oviposit during that female stage.

Sources:

```text
Kudo & Shibata 2021, Ecology and Evolution, doi:10.1002/ece3.7468
Kudo & Shibata 2025, Journal of Ecology, doi:10.1111/1365-2745.70130
```

Thus a biologically plausible manipulation window exists:

```text
common male phase completed
-> perfect/male identity becomes diagnosable at female transition
-> q manipulation
-> verify eggs_before_manipulation is negligible
-> only then proceed to later G assignment in the confirmatory design.
```

The literature does not guarantee that every plant is egg-free at this transition. The pilot must measure that directly.

## Common support comes first

The pilot may use only plants identified by:

```text
BITA_PEUCEDANUM_STAGE_B_COMMON_SUPPORT_V1
```

as capable of receiving every registered q treatment.

This prevents natural sex allocation from determining q-treatment eligibility.

## Pilot scale

A practical first technical pilot is:

```text
9 attempted manipulations / q level
x 3 q levels
= 27 attempts
```

with a target of at least:

```text
8 qualified manipulations / q level
= 24 validated units.
```

Those numbers are an operational starting point, not formal power. They allow the pilot to estimate q-manipulation qualification failure while retaining approximately eight validated units per q for the manipulation-quality audit.

The thresholds themselves remain preregistered inputs rather than repository constants.

## Attempt ledger

Every common-support eligible plant assigned to a q treatment must appear in:

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_PILOT_ATTEMPT_LEDGER_V1.csv
```

with:

```text
unit_id
q_target
common_support_eligible
manipulation_attempted
manipulation_qualified
failure_reason.
```

Failed attempts remain in the ledger. Do not delete them and report only successful manipulations.

This makes the quantity

```text
pre-G qualification failure fraction
```

observable rather than assumed.

## Qualified-manipulation measurements

Manipulation-qualified plants are recorded using the existing Stage-B validation schema and evaluated by:

```text
scripts/evaluate_peucedanum_stage_b_manipulation.py
```

Required validation domains include:

```text
q realization and separation
sex-classification accuracy
negligible eggs before manipulation
fixed retained total display
matched handling load
pretreatment covariate balance
mechanical damage control
male phase completed before manipulation.
```

The validation CSV must contain exactly the units marked `manipulation_qualified=1` in the attempt ledger.

## Pilot assembly

The complete pilot is assembled with:

```text
scripts/assemble_peucedanum_stage_b_pilot_readiness.py
```

Inputs:

```text
common-support receipt
attempt ledger
qualified-unit validation CSV
Stage-B manipulation validation config
pilot qualification config.
```

A positive receipt is:

```text
PEUCEDANUM_STAGE_B_TECHNICAL_PILOT_PASSED.
```

It requires:

1. every attempted unit belongs to the common-support set,
2. pilot q targets exactly match the common-support design,
3. enough attempts and qualified units exist at every q,
4. overall qualification rate exceeds its preregistered minimum,
5. each q level has an adequate qualification rate,
6. qualification failure is not strongly q-dependent,
7. the qualified subset passes the full manipulation-validation gate.

## Recruitment update after the pilot

The pilot receipt reports:

```text
observed_pre_g_qualification_failure_fraction
```

and a more conservative planning quantity:

```text
1 - Wilson lower 95% bound on qualification success.
```

That conservative failure fraction can replace the provisional 10% assumption in:

```text
scripts/plan_peucedanum_stage_b_sampling.py
```

when updating confirmatory recruitment.

Separately, the untreated presurvey/common-support receipt provides the fraction of encountered plants that can receive every q treatment. Therefore the full field recruitment chain becomes:

```text
plants screened in nature
-> common-support eligible
-> q manipulation attempted
-> q manipulation qualified
-> G randomized
-> outcomes observed.
```

Each loss process is recorded separately.

## What may be changed after the pilot

The pilot may legitimately inform:

- final integer-realizable q targets,
- retained total flower count,
- common-support screening burden,
- expected pre-G qualification failure,
- handling procedure,
- sex-classification protocol,
- expected technical mechanical-damage rate,
- expected post-randomization attrition for operational recruitment planning,
- measurement logistics for paternity and fruit outcomes.

It should not be used to choose the confirmatory direction or minimum effect after looking at final fitness outcomes, because the technical pilot is not intended to estimate the confirmatory causal `Delta_q*` reliably.

## GO / NO-GO logic

### GO

Proceed toward confirmatory freeze only if:

```text
common-support q design is feasible
+ pilot qualification rate is acceptable
+ failure rate is not concentrated at one q level
+ manipulation validation passes
+ eggs-before-manipulation gate confirms the timing window is usable.
```

### REDESIGN

If common support is poor but manipulation quality is otherwise good:

```text
reduce retained total and/or narrow q range
-> repeat presurvey/common-support evaluation
-> repeat pilot.
```

### STOP / retain Stage A only

If no useful q range can be manipulated after the male phase without substantial pre-existing oviposition, classification error, mechanical damage, or q-dependent technical failure, do not force Stage B.

The already implemented Stage-A randomized egg-removal experiment remains the causal antagonist-selection lane without a causal q manipulation.

## Claim ceiling

A positive technical pilot validates field feasibility only. It does not show:

```text
q causes female fitness
q causes predator attraction
antagonism shifts q*
partial functional differentiation
historical origin of andromonoecy.
```

Those are reserved for the subsequent randomized fitness experiment and, for historical claims, independent evolutionary evidence.
