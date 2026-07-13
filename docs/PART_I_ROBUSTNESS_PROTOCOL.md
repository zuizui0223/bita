# Part I sensitivity contract

## Purpose

Part I is a qualitative local sensitivity analysis for a declared focal floral trait pair. It is not a calibrated fitness estimator, a distribution over natural systems, an evolutionary-optimum analysis, or a proof of mathematical structural robustness.

The baseline corollary is

\[
W(A,D,R)=
P(b_0+b_AA)e^{-c_DD}(1-c_RR)
+(1-P)a_RR
-H(f_0+d_AA)(1-e_FD)
-\mathrm{cost}(A,D,R),
\]

with local mixed partial

\[
\frac{\partial^2W}{\partial A\partial D}
=H d_Ae_F
-Pb_Ac_De^{-c_DD}(1-c_RR)
-c_{AD}.
\]

A positive value is **local complementarity**, a negative value **local substitutability**, and a near-zero value **locally neutral**. These labels refer to the declared trait coordinates and score surface. They do not assert observed trait covariance or an evolutionary endpoint.

## Focal-trait and regime rules

Each application must declare:

```text
A  one focal floral attraction trait and its scale
D  one focal flower-specific barrier/defence trait and its scale
P  exogenous reference intensity of pollinator service
H  exogenous reference intensity of floral-antagonist pressure
```

Different attraction or defence traits are alternative applications, not interchangeable measurements of one universal axis.

`P` and `H` must not be defined as realised visitation or realised damage after the focal traits act, because that would reuse trait-mediated outcomes as exogenous regime variables.

## Sensitivity question

For each declared local phenotype and regime case, ask:

```text
Does the sign of the A x D mixed partial remain the same across
this finite, predeclared set of response-function and parameter variants?
```

The answer is summarized as:

```text
tested_set_unanimous
conditional_majority
mixed_or_sensitive
```

`tested_set_unanimous` means exactly what its name says: every evaluation in the summarized finite tested set has the same non-neutral sign. It must not be described as a proof that the sign is structurally robust to all admissible model formulations.

## Functional-form families

The active sweep varies three curvature choices while retaining the same focal mechanisms.

### 1. Pollination return to attraction

```text
baseline:      b_A A
saturating:    b_A A / (1 + q_A A)
```

### 2. Defence reduction of floral-antagonist damage

```text
baseline:      e_F D
saturating:    e_F D / (h_D + D)
```

### 3. Direct attraction–defence joint cost

```text
baseline:      c_AD A D
curved:        c_AD A D [1 + k_AD(A + D)]
```

These variants are sensitivity choices. They are not estimated from the current literature layer, and they do not exhaust all biologically possible functional forms.

## Required dimensions

The sweep varies at minimum:

```text
P     exogenous reference pollinator service
H     exogenous reference floral-antagonist pressure
R     auxiliary reproductive-assurance moderator
A,D   local focal-trait coordinates
b_A   attraction-mediated mutualist response
d_A   attraction-mediated antagonist tracking
e_F   defence-mediated antagonist reduction
c_D   defence-mediated pollinator obstruction
c_AD  direct A x D cross-cost
q_A   attraction saturation
h_D   defence half-saturation
k_AD  shared-cost curvature
```

The parameter names describe mechanisms in the baseline corollary. Current literature records do not calibrate their magnitudes.

## Numerical procedure

For every parameter-regime case, evaluate the analytic mixed partial for each predeclared functional form.

```text
sign agreement = non-neutral evaluations with modal sign / non-neutral evaluations

tested_set_unanimous agreement = 1.00 and no neutral/discordant evaluation
conditional_majority agreement >= 0.80 without full unanimity
mixed_or_sensitive otherwise
```

An exact tie between complementary and substitutable evaluations is reported with `modal_sign = mixed`; it is not broken in favour of either sign.

The neutral tolerance must be fixed before classification and recorded in the generated metadata.

## Empirical bridge

The active literature layer has a narrower purpose than parameter calibration. It asks whether declared biological pathways occur in real systems.

At present, the route-level evidence supports the plausibility that a flower-specific defence/barrier can reduce pollinator use in some systems. This is relevant to the mutualist-interference mechanism, but it does not estimate:

- the full local mutualist curvature for one focal `A`–`D` pair;
- antagonist relief for that same pair;
- direct joint cost;
- any baseline parameter magnitude;
- the complete mixed partial or its environmental derivative.

No direction-only record or heterogeneous cross-system record is inserted as a raw model parameter.

## Primary deliverables

```text
part_i_robustness_cases.csv
  one row per functional-form / parameter / regime case

part_i_robustness_envelope.csv
  modal sign, agreement, and tested-set classification by local case

part_i_functional_form_summary.csv
  within-scenario summaries across the declared functional-form family
```

## Interpretation boundary

A `tested_set_unanimous` region means only:

> under every score function and parameter variant actually included in the stated finite tested set, the local `A x D` mixed partial has the same non-neutral sign.

It does not establish that the region is common in nature, that parameter values are universal, that a measured trait covariance is adaptive, that the sign survives every admissible functional form, or that the same sign survives a different nonlinear parameterisation of the focal traits.
