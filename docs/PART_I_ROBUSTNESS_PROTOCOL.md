# Part I sensitivity contract

## Purpose

Part I is a qualitative local sensitivity analysis for one declared floral attraction trait `A`, one declared flower-specific barrier/defence trait `D`, and one declared outcome scale `W`. It is not a calibrated fitness estimator, a distribution over natural systems, an evolutionary-optimum analysis, or a proof of mathematical structural robustness.

The implemented corollary is

\[
W(A,D,R)=
P(b_0+b_AA)e^{-c_DD}(1-c_RR)
+(1-P)a_RR
-H(f_0+d_AA)(1-e_FD)
-\mathrm{cost}(A,D,R),
\]

with local mixed partial

\[
W_{AD}=H d_Ae_F-Pb_Ac_De^{-c_DD}(1-c_RR)-c_{AD}.
\]

`R` is an auxiliary reproductive-assurance moderator in this corollary. It is not a third focal trait in the manuscript claim.

## Interpretation

- `W_AD > 0`: local complementarity on the declared `W` scale.
- `W_AD < 0`: local substitutability on the declared `W` scale.
- `W_AD = 0`: mathematical neutrality on that scale.

The numerical sweep additionally uses an absolute `neutral_tolerance` to avoid floating-point residue. This threshold is a numerical convention on the declared score scale, not a biological equivalence interval.

## Declared variables

Each application must define:

```text
A  one focal floral attraction trait and its scale
D  one focal flower-specific barrier/defence trait and its scale
W  one biological outcome or score and its scale
P  exogenous reference intensity of pollinator service
H  exogenous reference intensity of floral-antagonist pressure
R  optional auxiliary background moderator in the implemented corollary
```

`P` and `H` must not be realised visitation or realised damage measured after the focal traits act, because that would reuse trait-mediated outcomes as exogenous regime variables.

## Finite tested set

For every local phenotype/regime case, the analysis asks whether the sign remains the same across the declared finite set of biological parameter scenarios and endpoint-normalized response shapes.

The only categorical agreement labels are:

```text
tested_set_unanimous
mixed_or_sensitive
```

`tested_set_unanimous` requires the same non-neutral sign in every evaluation supplied to that summary. All other cases, including exact sign ties and any neutral evaluation, are `mixed_or_sensitive`. The continuous field `modal_sign_agreement` retains the descriptive fraction of non-neutral evaluations carrying the modal sign.

No intermediate majority threshold is used.

## Endpoint-normalized response shapes

On `A,D in [0,1]`, the nonlinear variants preserve common endpoint scales while changing local derivatives.

### Attraction response

```text
baseline:    b_A A
saturating:  b_A (1 + q_A) A / (1 + q_A A)
```

### Defence reduction of antagonist damage

```text
baseline:    e_F D
saturating:  e_F (1 + q_D) D / (1 + q_D D)
```

### Direct joint cost

```text
baseline:    c_AD A D
curved:      c_AD A D [1 + k_AD(A + D)] / (1 + 2 k_AD)
```

The variants match at `A=1`, `D=1`, and `A=D=1`, respectively. This reduces—but does not eliminate—confounding between response shape and effect magnitude.

## Numerical procedure

For each case, scenario, and response shape:

1. evaluate the analytic mixed partial;
2. classify its sign using the declared absolute tolerance;
3. write the three mechanism contributions and total mixed partial;
4. summarize sign agreement within each scenario;
5. summarize sign agreement across the full finite tested set.

The analytic expressions are regression-tested against independently written finite-difference derivatives of the explicit score functions.

## Canonical V2 outputs

```text
part_i_sensitivity_cases.csv
part_i_response_shape_summary.csv
part_i_full_tested_set_summary.csv
part_i_sensitivity_report.json
PART_I_MANUSCRIPT_READOUT_V2.md
FIGURE_2_THEORY_REGIME_MAP.svg
```

The canonical run identifier is `endpoint_normalized_grid_v2`.

## Literature boundary

The retained literature registry provides preliminary abstract-level context that a flower-associated defence/barrier can reduce pollinator use in some systems. It does not identify the focal `M_AD` curvature, calibrate any model coefficient, estimate the complete `W_AD`, or validate environmental regime derivatives.

## Permitted manuscript claim

> Within the declared model family and score parameterization, the local attraction–defence interaction is complementary when antagonist relief exceeds mutualist interference and direct joint-cost curvature, and substitutable when the opposing contributions dominate. The boundary is conditional on the declared traits, score scale, ecological regime, and mechanism strengths.

The analysis does not establish universal trait covariance, a universal trade-off, a universal complementarity law, an evolutionary endpoint, or prevalence in nature.