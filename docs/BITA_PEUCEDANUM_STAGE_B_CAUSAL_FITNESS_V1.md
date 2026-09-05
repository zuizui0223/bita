# BITA Peucedanum Stage-B causal fitness experiment v2

## Goal

Stage A randomizes antagonist context while floral sex allocation `q` remains naturally expressed. Stage B is the stronger causal experiment: first validate a post-male-phase manipulation of `q`, then cross that randomized composition with randomized antagonist treatment.

```text
q = perfect flowers / (perfect + male flowers)
G0 = predator eggs removed before hatching
G1 = predator eggs retained
```

The design asks whether experimentally altered seed-bearing investment changes predator attraction, realized predation and the female-fitness optimum while earlier male opportunity is preserved.

## Core design rule: complete at randomization, not necessarily complete at outcome

The randomized design must be complete **when G is assigned**:

```text
every randomization block
contains exactly one unit
for every registered q_target x G combination.
```

That complete assignment is frozen in:

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_ASSIGNMENT_LEDGER_TEMPLATE_V1.csv
```

The outcome file is different. Biological loss, failed paternity assignment or other post-randomization missingness may make an outcome block incomplete. A single missing unit must therefore **not** cause the other five randomized units in that block to be discarded.

Thus:

```text
complete assignment block
!= required complete outcome block.
```

The analyzer keeps all observed randomized units, audits attrition against the frozen assignment ledger and resamples observed block clusters in the bootstrap.

## Why whole-block deletion is prohibited

With three q levels and two G states there are six randomized units per block. If unit-level retention is `r`, the probability that an entire six-unit block remains complete is:

```text
r^6.
```

For example, at 90% unit retention:

```text
0.9^6 = 0.531441.
```

Requiring complete outcome blocks would therefore throw away nearly half of otherwise informative blocks even under only 10% unit attrition. It would also make the analyzed sample depend on post-randomization survival.

## Mandatory pre-G manipulation validation

The fitness analyzer does not accept a free-floating prior validation receipt. It re-runs:

```text
scripts/evaluate_peucedanum_stage_b_manipulation.py
```

on **all randomized units in the assignment ledger**, using preregistered validation thresholds.

If that manipulation does not return:

```text
PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED
```

fitness inference is blocked before outcome analysis.

This keeps manipulation validity upstream of post-randomization outcome availability.

## Registered files

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_ASSIGNMENT_LEDGER_TEMPLATE_V1.csv
empirical/identification_design/PEUCEDANUM_STAGE_B_FITNESS_TEMPLATE_V1.csv
empirical/identification_design/PEUCEDANUM_STAGE_B_FITNESS_CONFIG_TEMPLATE_V1.json
scripts/analyze_peucedanum_stage_b_fitness.py
```

The design declaration is:

```text
WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL.
```

## Assignment ledger and attrition audit

Every randomized unit receives:

```text
unit_id
block_id
q_target
q_realized
pre-G validation fields
g_state
outcome_observed.
```

`outcome_observed=1` means the registered outcome row exists; `0` means it is absent. The analyzer requires an exact identity match between the ledger and outcome file and checks that q, G and retained floral composition have not changed between them.

Before any positive claim it reports:

```text
randomized_n
observed_n
overall attrition fraction
minimum observed fraction across q x G cells
maximum difference in attrition rate across q x G cells
assigned and observed n for every cell.
```

Promotion requires all preregistered attrition bounds to pass:

```text
overall attrition <= frozen maximum
between-cell attrition-rate difference <= frozen maximum
observed fraction in every cell >= frozen minimum.
```

These are inference guards, not assumptions that missingness is harmless. Differential post-randomization loss remains a reason to withhold the confirmatory claim.

## Biological sequence

```text
common male phase completed
-> validate / randomize q at female transition
-> assign every qualified unit to G within a complete block
-> freeze assignment ledger
-> allow predator host selection on manipulated composition
-> record eggs_before_g_treatment
-> apply eggs removed versus retained treatment
-> record initial fruits
-> record intact and predated fruits
-> estimate male fitness by paternity or the preregistered endpoint
-> mark outcome availability in the assignment ledger.
```

Because eggs are counted after randomized q manipulation but before G treatment, the q effect on oviposition is itself causal.

## Primary estimand: causal optimum shift

For each antagonist state, fit the final intact-fruit surface across registered q levels using all observed randomized outcomes that pass the attrition audit:

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

## Outcome coverage

Attrition passing does not replace minimum information requirements. Every q x G cell must still satisfy the registered observed-unit minimum and the registered fraction with a defined predation endpoint. At least the registered number of blocks and q levels must remain represented.

## Bootstrap

Inferential intervals resample `block_id` clusters from the observed outcome dataset. Blocks may be incomplete after randomization. A bootstrap replicate that lacks a required q x G cell fails closed; the analysis itself requires at least 80% of requested bootstrap replicates to remain estimable.

This preserves the local blocking structure without deleting all information from a block merely because one randomized member is missing.

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

Explicit attrition auditing does not prove that missing outcomes are missing at random. It only prevents silent deletion and requires the observed pattern to stay within prospectively frozen bounds.

The experiment also does not establish the natural developmental or historical origin of andromonoecy. Those require separate developmental and phylogenetic evidence.
