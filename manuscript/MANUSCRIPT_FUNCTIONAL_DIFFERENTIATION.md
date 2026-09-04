# From compromise to modularity: functional differentiation as an escape from multifunctional constraint

## Abstract

Multifunctional traits are constrained when distinct functional demands act on one shared phenotype. Chapter 1 / SCH identifies this constraint experimentally through state-specific reproductive optima and causal optimum shifts. Chapter 2 asks whether an additional trait dimension lets the functions become more independently tunable. We define functional differentiation as a move from one shared coordinate `z` toward partially distinct coordinates `x` and `y` with preferentially different functional loading. The default empirical cross-chapter test uses the SCH function-1-facing state optimum `z_P* = argmax W10(z)` as the release reference; it does not relabel that state optimum as the pure theoretical `z_F1*` unless SCH independently identifies the direct/background pathways needed for that stronger claim. BITA then tests whether adding `y` moves the optimum of `x` toward the declared SCH reference, improves the intended function-2 outcome and total fitness, and can be explained by selective mechanism allocation. In the floral implementation, attraction `A` and antagonist-reducing trait `D` are the first concrete `x,y` system. Existing `A x D`, `A0/A1`, partial-identification, and `A x D x antagonist x pollinator` machinery remain the operational core. Literature provides real-world evidence for component partitioning, conditional gating, route separation, and guarded function, while historical modularization remains a separate claim requiring ancestral-state evidence.

## 1. The Chapter-2 problem

Chapter 1 begins with one shared phenotype:

```text
function 1 ---\
               >--- trait z ---> compromise / balance
function 2 ---/
```

Chapter 2 asks whether the architecture gains another dimension:

```text
function 1 -> trait x
function 2 -> trait y.
```

The central question is:

> **Does functional differentiation release the measured constraint created when multiple functional demands were forced to share one trait coordinate?**

## 2. What counts as functional differentiation

Two observed traits are not automatically two functional modules. A differentiated architecture requires:

1. distinct measurable coordinates `x` and `y`;
2. preferential functional loading rather than two equally pleiotropic traits;
3. dimensional release of the retained coordinate relative to the declared SCH reference;
4. improved joint outcome on a common scale;
5. mechanism evidence showing why the added dimension helps.

Cross-loading need not be zero, but it must be measured.

## 3. Theory benchmark versus empirical release reference

At the theory level, pure function-specific objectives may have optima:

```text
z_F1*
z_F2*.
```

Under an ideal local quadratic benchmark, forcing both functions onto one coordinate produces the mismatch penalty:

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

An ideal differentiated architecture with added cost `K` has theoretical gain:

```text
Delta_mod,theory
  = [a b / (a + b)] (z_F1* - z_F2*)^2 - K.
```

This is a theory benchmark, not an automatically identified empirical quantity.

The crossed SCH experiment directly identifies:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Because direct/background effects can remain in `W10` and `W01`,

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The default Chapter-2 release target is therefore `z_P*`.

## 4. The strongest cross-chapter test: dimensional release

Let `x` retain most of the original function-1-facing role and let `y` carry more of function 2.

Estimate:

```text
x0* = argmax W(x | y0)
x1* = argmax W(x | y1).
```

With default state-specific reference `z_ref = z_P*`, define:

```text
R_state
  = |x0* - z_P*| - |x1* - z_P*|.
```

Positive `R_state` means the added dimension releases `x` toward the state favored when the competing function was suppressed in SCH.

If SCH independently identifies the pure `z_F1*`, a stricter second lane may report:

```text
R_pure
  = |x0* - z_F1*| - |x1* - z_F1*|.
```

State-specific and pure-function release must not be silently conflated.

## 5. Floral implementation: attraction and defence

The current mapping is:

```text
function 1 = pollinator-mediated reproductive gain
function 2 = avoidance / reduction of antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

Functional differentiation does not require antagonists to stop detecting `A`. `D` can act at access, handling, ingestion, oviposition, damage, or another later pathway while `A` remains publicly detectable.

## 6. Existing BITA outcome hierarchy

For two declared levels of attraction and defence:

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0
           = W11 - W10 - W01 + W00.
```

Retain the nested claims:

```text
Level 1 — positive interaction relief
Delta_AD W > 0

Level 2 — constraint release
A0 <= 0 < A1

Level 3 — strict reversal
A0 < 0 < A1.
```

These are local outcome claims. They do not by themselves establish preferential loading, dimensional release, mechanism allocation, or historical modularization.

## 7. Preferential functional loading

A strong Chapter-2 result should estimate all four trait-to-function arrows:

```text
x -> function 1
x -> function 2
y -> function 1
y -> function 2.
```

The intended architecture has stronger within-function loading than cross-loading. In the floral implementation, attraction should retain a strong pollinator-facing effect, while defence should reduce antagonist-mediated loss without an equivalent pollinator penalty.

Perfect selectivity is not required; residual coupling is part of the result.

## 8. Mechanism allocation and residual coupling

The complete floral mechanism design crosses:

```text
A x D x antagonist x pollinator
```

in 16 cells.

The total interaction is not enough to identify the mechanism uniquely. Retain the existing channel logic:

```text
rho_delta   antagonist relief
iota_delta  pollinator interference
m0_delta    pollinator-independent baseline interaction
U_delta     remaining unallocated residual.
```

`U_delta` is not renamed as a joint construction cost without an independent assay.

The four-way interaction is also a diagnostic of residual functional coupling. A non-zero value indicates partial rather than complete modularity.

## 9. Real-world evidence

Existing systems show multiple forms of partial differentiation. Petunia scent components can carry different ecological roles; conditional floral cue induction changes when shared cues are deployed; spatial, temporal, chemical, and geometric route separation can preserve legitimate pollination while reducing antagonism. The BITA synthesis also recovers overlapped and bypassable cases, showing that extra trait complexity does not automatically create effective modularity.

Kessler et al. (2008) provides the strongest existing manipulated `A x D`-like reproductive surface in *Nicotiana attenuata*. It is an interaction-level release anchor, not a complete demonstration of functional differentiation from an identified SCH compromise.

## 10. Experimental hierarchy

```text
Stage 0 — inherit positive SCH receipt
          z_P*, z_G*, z_C* by default
          optional pure z_F1*, z_F2* only if independently identified

Stage 1 — validate x and y as stable, manipulable coordinates

Stage 2 — estimate preferential functional loading

Stage 3 — test multi-level dimensional release
          default: x* moves toward z_P*
          optional strict lane: x* moves toward pure z_F1*

Stage 4 — test local A x D outcome hierarchy
          and full 16-cell mechanism allocation

Stage 5 — test stable developmental/genetic modularity or historical transition.
```

## 11. Architecture-level gain

Within-BITA improvement is reported as:

```text
within_bita_optimum_fitness_gain.
```

It is not called `Delta_mod` unless shared and differentiated architectures have explicitly commensurable fitness scales and the added construction, maintenance, regulatory, and pleiotropic costs are included.

Thus a positive `R_state` can support dimensional release even when architecture-level `Delta_mod` remains unidentified.

## 12. Functional-differentiation ladder

```text
D0  distinct measured trait coordinates
D1  preferential functional loading
D2  dimensional release toward declared SCH reference
D3  mechanism-resolved differentiation
D4  stable ecological / developmental modularity across contexts
D5  historical modularization from an ancestral integrated state.
```

Existing evidence reaches parts of D0-D2 across different systems. No screened system currently closes D0-D3 in one complete chain anchored to a directly identified SCH compromise.

## 13. Main predictions

1. A valid differentiated architecture should show preferential functional loading.
2. Adding the function-2-facing coordinate should move the retained `x` optimum toward the declared SCH reference.
3. By default that reference is state-specific `z_P*`, not pure `z_F1*`.
4. Functional release should be greatest when cross-loading and residual coupling are small.
5. Large `A x D` interaction relief without preferential loading is insufficient evidence of modularity.
6. Contemporary differentiation and historical modularization are separate claims.

## 14. Current claim ceiling

Current evidence supports real-world partial functional separation and a manipulated interaction-level release anchor. What remains missing is one complete cross-chapter demonstration:

```text
identified SCH causal compromise
+
validated x,y coordinates
+
preferential functional loading
+
uncertainty-bearing dimensional release toward the declared SCH reference
+
mechanism allocation
+
independent architecture cost for Delta_mod.
```

Current status:

```text
REAL_WORLD_FUNCTIONAL_SEPARATION_RECOVERED
INTERACTION_LEVEL_RELEASE_ANCHOR_RECOVERED
STATE_SPECIFIC_DIMENSIONAL_RELEASE_ANALYZER_READY
PURE_FUNCTION_RELEASE_REQUIRES_STRONGER_SCH_INPUT
COMPLETE_DIFFERENTIATION_CHAIN_NOT_YET_IDENTIFIED.
```

## 15. Conclusion

Functional differentiation should not be inferred merely because two traits exist or because their interaction is favorable. Chapter 1 first identifies a one-dimensional causal compromise. Chapter 2 then asks whether a second dimension makes the functions more independently tunable, whether the retained trait moves toward the correct Chapter-1 reference, and which mechanisms and costs determine the gain. Keeping state-specific and pure-function references separate makes the cross-chapter test more rigorous and prevents a clean theoretical symbol from being mistaken for an experimentally identified biological optimum.
