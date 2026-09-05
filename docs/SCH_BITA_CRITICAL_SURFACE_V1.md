# SCH–BITA critical surface v1

## Result

The two chapters contain **one common architecture critical surface**, but they also contain different intrinsic/empirical boundaries that must not be collapsed into it.

The clean distinction is:

```text
C0  SCH intrinsic conflict onset
    L_S* = 0

C1  BITA empirical geometric-release onset
    R_state = 0

C2  shared architecture-choice critical surface
    Phi = R-K = 0
```

Only C2 is literally the same critical surface viewed from the two chapter worlds.

## 1. Chapter 1 world: one-axis balance

SCH constrains both functions to one coordinate. In the quadratic benchmark,

```text
L_S* = [w1 w2/(w1+w2)] (theta1-theta2)^2.
```

`L_S*=0` is the intrinsic no-conflict boundary. With positive weights, any nonzero function-optimum separation gives positive conflict load.

But this does **not** create a shared-versus-differentiated transition inside SCH because the alternative architecture is absent from the Chapter-1 state space. In the current convex unbounded model, the shared optimum moves continuously with functional weights.

Thus SCH has an intrinsic conflict boundary, not an intrinsic architecture phase switch.

## 2. Chapter 2 world: architecture choice

BITA introduces a differentiated architecture and defines

```text
R = recoverable shared-axis loss before fixed architecture cost
K = extra architecture cost
Phi = R-K.
```

The architecture critical surface is

```text
Phi = 0.
```

In the quadratic baseline,

```text
R = s L_S*
```

so the common boundary is

```text
s L_S* = K.
```

## 3. Same surface, different coordinates

### Viewed from SCH

Import `s` and `K` from the differentiated world and ask how much one-axis conflict is required:

```text
L_S,crit* = K/s.
```

Or solve for critical function-optimum separation:

```text
|theta1-theta2|_crit
 = sqrt[
     K (w1+w2) (w1 w2 + lambda(w1+w2))
     / (w1^2 w2^2)
   ].
```

This is the Chapter-1 projection of the architecture boundary.

### Viewed from BITA

Hold the Chapter-1 conflict fixed and ask how costly or coupled differentiation can be:

```text
K_crit = s L_S*
s_crit = K/L_S*.
```

For `0<K<L_S*`, the critical residual coupling is

```text
lambda_crit
 = [w1 w2/(w1+w2)] (L_S*/K - 1).
```

These are coordinate transformations of the same `Phi=0` surface, not independent thresholds.

## 4. Reference calculation

Let

```text
w1=w2=1
K=0.1.
```

### SCH-side projection with lambda=1

```text
s = 1/3
L_S,crit* = 0.3
|theta1-theta2|_crit = sqrt(0.6)
                     = 0.7745966692...
```

### BITA-side projection with |theta1-theta2|=1

```text
L_S* = 0.5
s_crit = 0.2
lambda_crit = 2.
```

Both parameterizations satisfy

```text
R = s L_S* = K = 0.1.
```

The code regression tests this equivalence rather than relying on prose.

## 5. Why the raw empirical critical points are parallel, not yet identical

The direct SCH experiment outputs state-specific trait references such as

```text
z_P*, z_G*, z_C*.
```

The direct BITA dimensional-release analysis outputs

```text
R_state
 = |x0*-z_P*| - |x1*-z_P*|.
```

The empirical release boundary

```text
R_state = 0
```

is a **trait-distance boundary**. The architecture boundary

```text
R-K = 0
```

is a **fitness boundary**.

They become numerically comparable only after the paired biological system provides a mapping from trait displacement to common reproductive-fitness loss and an explicit cost/decoupling lane.

Therefore the current status is:

```text
THEORY C2:                 SAME CRITICAL SURFACE
SCH INTRINSIC C0:          DIFFERENT BOUNDARY
BITA EMPIRICAL C1:         DIFFERENT UNITS / PARALLEL PROJECTION
PAIRED EMPIRICAL C2:       NOT YET NUMERICALLY IDENTIFIED.
```

## 6. Conditions for empirical coincidence

To test whether both chapters cross the same *ecological context* critical point `e_c`, require all of the following in the same population/season or otherwise calibrated context:

1. SCH recovers a positive causal `z x P x G` compromise surface;
2. the same common reproductive-fitness scale is retained into BITA;
3. BITA recovers positive/negative `R_state` across a graded context or architecture treatment;
4. the shared-state fitness loss and differentiated-state fitness gain are commensurable;
5. additional architecture cost `K(e)` is independently declared/estimated;
6. residual coupling/decoupling `s(e)` is estimated rather than assumed;
7. the zero of `Phi(e)=R(e)-K(e)` is located with uncertainty.

Then define

```text
e_c,S = context where L_S*(e) = K(e)/s(e)
e_c,D = context where K(e) = s(e)L_S*(e).
```

Under a valid cross-world mapping these are algebraically the same `e_c`. A discrepancy larger than uncertainty would indicate that the two empirical worlds are not described by the same mapping—e.g. costs change with context, the second trait changes the functional objectives themselves, or the axes are not nested as assumed.

That discrepancy is scientifically informative rather than a model failure to hide.

## 7. A true parallel-world test

The strongest paired analysis should therefore fit two competing models:

### M_same — one latent critical surface

```text
one shared e_c
SCH projection and BITA projection constrained to cross at the same e_c.
```

### M_parallel — two world-specific critical points

```text
e_c,S and e_c,D estimated separately.
```

Compare the models using held-out predictive performance or a preregistered likelihood/information criterion appropriate to the eventual data structure. The quantity of interest is

```text
Delta_e_c = e_c,D - e_c,S.
```

Interpretation:

```text
Delta_e_c compatible with 0
-> same critical surface is empirically adequate

Delta_e_c persistently nonzero
-> parallel-world criticality: the effective threshold changes when the architecture itself changes.
```

This creates a direct empirical test of the user's "same point versus parallel worlds" idea.

## 8. Existing evidence and next executable closure

- Peucedanum provides positive real-world partial differentiation and context-dependent selection, but not causal `R_state` or architecture cost.
- Pedicularis has the strongest registered same-species SCH -> BITA route; both analyzers/contracts exist but the paired positive receipts are not yet produced.
- Current literature and route counts cannot identify `e_c` by themselves.

Thus the exact theory critical surface is recovered now; the numeric biological critical context remains a prospective paired-estimation target.

## Implementation

- `trait_architecture/criticality.py`
- `tests/test_criticality.py`

The test suite verifies both Chapter-1 and Chapter-2 coordinate projections land on the same quadratic boundary in the registered reference cases.
