# BITA Peucedanum Stage-B common-support gate v1

## Why this gate is necessary

The proposed Stage-B manipulation creates a target perfect-flower fraction

```text
q = perfect / (perfect + male)
```

by retaining a fixed number of already sex-classified floral units after the common male phase.

That manipulation can only remove floral units. It cannot create perfect flowers in a naturally male-biased umbel or create male flowers in a naturally perfect-biased umbel.

Therefore a unit's natural sex composition can determine which q treatments are physically reachable.

If q is randomized from treatment-specific eligibility pools, the causal contrast is contaminated because:

```text
natural sex allocation -> treatment eligibility -> assigned q.
```

Stage B therefore uses a **common-support subset**: only plants capable of receiving every registered q treatment enter q randomization.

## Common-support rule

For retained total `R` and ordered targets

```text
q1 < q2 < q3
```

all q targets must correspond to integer retained flower counts.

For each target:

```text
perfect retained = q * R
male retained    = R - perfect retained.
```

A plant is common-support eligible only if it contains at least:

```text
max(perfect retained across q targets)
max(male retained across q targets)
```

before the manipulation.

Thus every eligible plant can, in principle, be randomized to every q level.

## Why the earlier synthetic q levels must not be frozen

Synthetic development tests used:

```text
R = 40
q = 0.25, 0.50, 0.75.
```

That design requires every randomized plant to have at least:

```text
30 perfect flowers
30 male flowers.
```

The published 2025 focal experiment reports mean perfect-flower number near 15.1 and mean male-flower number near 46.8. Those published means do not identify the full joint distribution, but they make the 30-perfect common-support requirement an obvious feasibility risk.

Therefore the synthetic 0.25/0.50/0.75 design is a software test, **not** a field recommendation.

## Presurvey workflow

Before the manipulation pilot, record untreated terminal umbels using:

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_PRESURVEY_TEMPLATE_V1.csv
```

Fields:

```text
unit_id
perfect_available
male_available
total_available.
```

Then evaluate candidate designs with:

```text
python -m scripts.plan_peucedanum_stage_b_common_support \
  presurvey.csv \
  --retained-total 20 \
  --q-targets 0.2,0.4,0.6
```

The example values above are illustrative only.

The tool returns:

- exact perfect/male count requirements for each q,
- number and fraction of common-support eligible units,
- Wilson lower 95% bound for the observed eligibility fraction,
- IDs of common-support eligible plants,
- the shift in mean natural q between the full screen and eligible subset,
- screening counts needed to obtain pilot or confirmatory eligible pools under the conservative Wilson-lower eligibility probability.

## Pilot use

For the manipulation pilot, a useful first target is still approximately:

```text
8 randomized plants / q level
x 3 q levels
= 24 common-support eligible plants.
```

The presurvey should be larger than 24 because common-support filtering occurs before q randomization.

The common-support planner can translate the empirical eligibility fraction into a screening requirement for obtaining 24 eligible plants with a declared coverage probability.

## Confirmatory use

The current operational sampling plan targets approximately:

```text
189 common-support eligible pre-G candidates
-> 156 qualified and G-randomized
-> >=108 observed outcomes.
```

This means `189 initial candidates` should be interpreted as **189 common-support eligible candidates**, not 189 arbitrary plants encountered in the population.

If the common-support eligibility fraction is `e`, the number that must be screened in nature can be substantially larger than 189.

The common-support planner reports a conservative screening count using the Wilson lower 95% bound on `e`.

## Choice of retained total and q range

There is an unavoidable design trade-off:

```text
larger retained total / wider q span
-> stronger manipulation and larger post-manipulation display
-> lower common-support eligibility

smaller retained total / narrower q span
-> more eligible plants
-> potentially weaker causal separation and more drastic display reduction.
```

Do not choose the design solely by maximizing eligibility.

A candidate confirmatory design should jointly satisfy:

1. enough common support for recruitment,
2. meaningful q separation,
3. integer-realizable q targets,
4. acceptable mechanical removal burden,
5. adequate retained female opportunities at all q levels,
6. Stage-B manipulation-validation gates,
7. sufficient outcome coverage after G randomization.

The final q levels must be frozen **after presurvey and technical manipulation pilot but before confirmatory outcomes are observed**.

## External-validity boundary

Common-support restriction solves treatment-assignment confounding inside the eligible subset. It does not make the eligible subset representative of the whole population.

The causal estimand is therefore:

> effect of randomized q and antagonist state among plants capable of receiving all registered q treatments.

The natural distribution of sex allocation outside that support remains a separate ecological generalization question.

## Claim boundary

Common-support qualification is a design-validity step only. It does not support functional differentiation, an optimum shift, or any fitness claim by itself.
