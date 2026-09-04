# BITA end-to-end execution spine v1

## One-line programme

```text
SCH identifies a one-dimensional shared-trait compromise
-> BITA adds a second functional coordinate
-> test preferential loading
-> test x-optimum release toward SCH function-1 optimum
-> test joint fitness improvement
-> allocate the mechanism with the selective 16-cell design
-> keep historical modularization separate.
```

## Gate B0 — positive SCH handoff

BITA starts only after SCH supplies a positive causal-compromise receipt:

```text
MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE.
```

Required imported quantities include:

```text
z_function1
z_shared_combined
causal optimum-shift evidence.
```

BITA does not re-estimate or redefine the Chapter-1 optimum after seeing Chapter-2 data.

## Gate B1 — trait-coordinate identity

Declare:

```text
x = retained / refined coordinate corresponding to the SCH shared trait
y = added coordinate intended to carry more of function 2.
```

If x is not measured on the exact SCH z scale, preregister an affine mapping:

```text
x_SCH = offset + multiplier * x.
```

Do not choose the mapping after observing whether release improves.

## Gate B2 — preferential functional loading

Measure both declared functions separately across x and y.

Required reporting:

```text
y effect on function 2
cross-effect of y on function 1
x-associated response range for function 1
x-associated response range for function 2.
```

The current first-pass outcome analyzer requires y to improve function 2 while preserving function 1 within a predeclared tolerance.

Perfect selectivity is not required; cross-loading is reported rather than hidden.

## Gate B3 — empirical dimensional release

Use multiple x levels and at least two y states.

Data template:

```text
empirical/identification_design/BITA_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv
```

Run:

```bash
python scripts/analyze_bita_dimensional_release.py \
  <bita_surface.csv> \
  <sch_receipt.json> \
  <frozen_config.json> \
  --output <bita_release_receipt.json>
```

The analyzer estimates:

```text
x0* = optimum under y0
x1* = optimum under y1
R   = |x0* - z_function1| - |x1* - z_function1|.
```

Positive `R` means the extra y dimension releases x toward the function-1 optimum identified in SCH.

Registered analysis details are in:

```text
docs/BITA_EMPIRICAL_DIMENSIONAL_RELEASE_ANALYSIS_V1.md
trait_architecture/dimensional_release.py
```

## Gate B4 — outcome-level functional differentiation

The status:

```text
FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED
```

requires:

```text
y targets function 2
y preserves function 1 within tolerance
x optimum moves toward SCH z_function1
best y1 fitness exceeds best y0 fitness by the declared amount
released y1 surface retains an interior optimum.
```

This is an outcome-level architecture result, not yet mechanism allocation.

## Gate B5 — do not misuse Delta_mod

Within-BITA improvement is reported as:

```text
within_bita_optimum_fitness_gain.
```

It is not called `Delta_mod` unless the shared and differentiated architectures have explicitly commensurable fitness scales and added construction / maintenance / regulatory costs are included.

Default output therefore remains:

```text
Delta_mod: NOT_IDENTIFIED.
```

## Gate B6 — local A x D outcome hierarchy

The existing special-case hierarchy remains:

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0

positive interaction relief: Delta_AD W > 0
constraint release:          A0 <= 0 < A1
strict reversal:             A0 < 0 < A1.
```

These local results complement the multi-level x-optimum release test. They do not replace it.

## Gate B7 — mechanism-resolved differentiation

Run the selective crossed design:

```text
x x y x function-2 environment x function-1 environment.
```

Floral implementation:

```text
A x D x antagonist x pollinator
= 16 cells.
```

Estimate the existing mechanism channels:

```text
rho_delta
  antagonist relief

iota_delta
  pollinator interference

m0_delta
  pollinator-independent baseline interaction

U_delta
  remaining unallocated residual.
```

Do not rename `U_delta` as a construction / joint-cost mechanism without an independent assay.

The mechanism result should explain the direction and magnitude of the multi-level release already identified at Gate B3/B4.

## Gate B8 — residual coupling / partial modularity

Use the registered four-way interaction as an internal residual-coupling diagnostic:

```text
x x y x E1 x E2
```

or, in the floral implementation:

```text
A x D x G x P.
```

A non-zero four-way interaction means the functions remain state-dependent after trait differentiation. Interpret this as partial modularity, not automatic failure.

## Stop rules

### Stop B1 — no preferential loading

If y improves function 2 only by causing an equally large loss in function 1, report two-trait interaction / trade-off, not functional differentiation.

### Stop B2 — no optimum release

If x1* does not move toward the SCH function-1 optimum, do not call the second dimension an escape from Chapter-1 compromise even if total fitness changes.

### Stop B3 — release without fitness gain

If x moves in the predicted direction but total reproductive performance does not improve, report coordinate release without architecture-level benefit.

### Stop B4 — outcome supported, mechanism unresolved

If B2-B4 pass but the selective crossed design does not close mechanism allocation, report:

```text
FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED
MECHANISM_ALLOCATION_UNRESOLVED.
```

## Historical promotion

Contemporary functional differentiation is not historical modularization.

Historical promotion still requires:

```text
ancestral shared architecture
-> derived increase in dimensionality / functional independence
-> reconstructed repeated transition(s)
-> tests of alternative developmental / phylogenetic histories.
```

## Full SCH -> BITA chain

```text
SCH
shared z
-> z_function1, z_function2, z_combined
-> causal compromise

BITA
add y
-> preferential functional loading
-> x optimum moves toward z_function1
-> joint fitness improves
-> 16-cell mechanism explains why
-> residual coupling quantifies partial modularity.
```

This is the operational meaning of:

```text
compromise / balance
-> functional differentiation / modularization.
```
