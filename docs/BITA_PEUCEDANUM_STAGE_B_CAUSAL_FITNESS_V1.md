# BITA Peucedanum Stage-B causal fitness experiment v1

## Goal

Stage A randomizes antagonist context while floral sex allocation `q` remains naturally expressed. Stage B is the stronger causal experiment: first validate a post-male-phase manipulation of `q`, then cross that randomized composition with randomized antagonist treatment.

```text
q = perfect flowers / (perfect + male flowers)
G0 = predator eggs removed before hatching
G1 = predator eggs retained
```

The design therefore asks whether an experimentally altered degree of seed-bearing investment changes predator attraction, realized predation and the female-fitness optimum while earlier male opportunity is preserved.

## Mandatory same-dataset validation

The Stage-B fitness analyzer does not accept a free-floating prior validation receipt. It re-runs:

```text
scripts/evaluate_peucedanum_stage_b_manipulation.py
```

on the same outcome rows using the preregistered validation thresholds.

If that manipulation does not return:

```text
PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED
```

fitness inference is blocked before outcome analysis.

## Registered files

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_FITNESS_TEMPLATE_V1.csv
empirical/identification_design/PEUCEDANUM_STAGE_B_FITNESS_CONFIG_TEMPLATE_V1.json
scripts/analyze_peucedanum_stage_b_fitness.py
```

The design declaration is:

```text
WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL.
```

Every block must contain exactly one unit for every registered `q_target x G` combination.

## Biological sequence

```text
common male phase completed
-> validate / randomize q at female transition
-> allow predator host selection to occur on manipulated composition
-> record eggs_before_g_treatment
-> randomize eggs removed versus retained
-> record initial fruits
-> record intact and predated fruits
-> estimate male fitness by paternity or the preregistered male-fitness endpoint.
```

Because eggs are counted after randomized q manipulation but before G treatment, the q effect on oviposition is itself causal.

## Primary estimand: causal optimum shift

For each antagonist state, fit the final intact-fruit surface across the registered q levels:

```text
W_f(q | G0)
W_f(q | G1).
```

Recover:

```text
q0* = optimum under eggs removed
q1* = optimum under eggs retained
Delta_q* = q1* - q0*.
```

Primary prediction:

```text
Delta_q* < 0.
```

This means seed predation causally shifts the best female allocation toward a lower proportion of seed-bearing perfect flowers.

## Mechanism chain

A positive claim additionally requires the following registered sequence.

### 1. Female opportunity increases with q

Before predation damage, high-q treatments must produce more initial female opportunity than low-q treatments:

```text
initial_high_vs_low_gain_z > preregistered minimum.
```

### 2. G does not alter initial female opportunity

Egg removal occurs after oviposition and before larval damage. Matched-q differences in initial fruit production must remain inside the equivalence tolerance.

### 3. Randomized q increases predator oviposition

Because `q` is randomized and `eggs_before_g_treatment` is measured before G:

```text
high q -> more predator eggs
```

is a causal treatment effect when its preregistered gate passes.

### 4. Egg removal reduces predation

Across q levels:

```text
mean predation rate under G1 - mean predation rate under G0
```

must exceed the preregistered minimum.

### 5. Predation cost increases with q

Define:

```text
Delta_pred_q =
  [pred(high q,G1)-pred(low q,G1)]
- [pred(high q,G0)-pred(low q,G0)].
```

A positive value shows that the antagonist cost of carrying seed-bearing perfect flowers increases specifically when predator damage is allowed.

### 6. Male function remains preserved

Because q is manipulated after the common male phase, male fitness should not materially differ among q x G cells. The analyzer uses the range of cell means on the observed male-fitness SD scale and requires its block-bootstrap upper interval to remain below the preregistered equivalence tolerance.

## Bootstrap

All inferential intervals resample entire `block_id` sets. Each block is a complete q x G factorial, so block resampling preserves the randomized matched design.

## Positive receipt

All gates must pass before returning:

```text
CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_SUPPORTED.
```

The result would support a contemporary causal architecture claim:

```text
more perfect-flower investment
-> more female opportunity
-> more predator attraction
-> more predator-dependent loss
-> lower optimal q under antagonism

while earlier male fitness remains preserved.
```

## Claim ceiling

Even this experiment does not show complete modularity. Perfect flowers still carry male and female functions, so the architecture is intrinsically partially coupled.

It also does not establish the natural developmental or historical origin of andromonoecy. Those require separate developmental and phylogenetic evidence.
