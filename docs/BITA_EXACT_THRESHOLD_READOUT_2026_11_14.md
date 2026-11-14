# BITA: exact cost and conflict-distance thresholds

**Status:** theory-only continuation of Draft PR #363, based on source model commit `c30aa3331eceaa657f779626ff2d2efdf22a0b18`. No natural-data estimates, manuscript text, or main branch changed. The previous `tau<s` existence theorem is retained; this note makes its upper cost bound computable and interprets its two distinct conflict thresholds.

## 1. Exact reduction to one bounded maximization

Use the existing model

    Phi(u) = d^2[2hu-(h+lambda)u^2] - c(1-exp(-u/tau)),  0 <= u <= 1
    h=w1*w2/(w1+w2), s=h/(h+lambda), R=h*s*d^2.

Let `r=tau/s`, `v=u/s`. Then

    Q_r(v) = v(2-v)/(1-exp(-v/r)),  Q_r(0)=2r
    Ccrit(d) = R max_{0<=v<=1} Q_r(v).

Although `u<=1` formally permits `v<=1/s`, the maximum is never improved past `v=1`: the gross gain decreases there while the cost denominator increases, and negative gross gains cannot beat the positive maximum.

For `0<r<1`, the unique positive maximizing point `v*` satisfies

    H(v) = 2r(1-v)(exp(v/r)-1)-v(2-v) = 0,
    1-r < v* < 1.

Indeed `H'(v)=2(1-v-r)(exp(v/r)-1)`, so H increases from zero to `v=1-r`, decreases thereafter, and H(1)=-1. This proves uniqueness and supplies a grid-free bisection bracket. For `r>=1`, H is negative for v>0, so the maximum is the limiting value at zero: `Ccrit=2hd^2*tau`.

**Thus a specified cost cap c, not merely some unspecified cap, produces positive global gain with negative initial slope exactly when**

    2hd^2*tau < c < Ccrit(d).

The interval exists iff `tau<s`. All strict inequalities matter.

## 2. Two thresholds as ecological conflict changes

Keep weights, residual coupling, startup cost c>0 and tau fixed; vary the distance d between the two functional optima. Write `Ccrit(d)=d^2*Ccrit(1)`. Define

    d_global = sqrt(c/Ccrit(1))
    d_local  = sqrt(c/(2h*tau)).

- `d<d_global`: no differentiated phenotype has higher modeled score than the optimized shared state.
- `d_global<d<d_local`, possible only for `tau<s`: some differentiated phenotype is better, but the shared state's initial slope is negative.
- `d>d_local`: the initial slope is positive, so arbitrarily small positive separation improves the modeled score.

At `d=d_global`, the maximum gain ties zero; it is not a strict benefit. At `d=d_local`, the initial slope equals zero. In particular when `tau<s`, the second derivative is positive, so small separation can already be advantageous at second order: a zero slope is **not** proof of evolutionary impossibility.

For `tau<s`, the globally optimal positive-separation state at the benefit boundary has `u*=s*v*>0`: the optimum changes discontinuously as d passes that boundary. For `tau>=s`, both distance thresholds coincide and the onset is continuous. These are properties of the prescribed phenotype-score landscape, **not genetic fixation, evolutionary historical transitions, or speciation**.

## 3. Reproducible synthetic example

Parameters: `w1=w2=1`, `lambda=.5`, `h=s=.5`, `tau=.30`, `c=.315`.

| Quantity | Computed value |
|---|---:|
| Lower cap for negative initial slope at d=1 | 0.300000000000 |
| Upper cap for positive global benefit at d=1 | 0.332285925448 |
| d_global | 0.973642008794 |
| d_local | 1.024695076596 |
| Positive separation at the global benefit boundary | 0.287829804463 |
| Phi(0.30) at d=1 | +0.010882023969 |

The `u*=0.2878298` value is the **tangency at the global-benefit boundary**, not the best separation at d=1 with c=.315. All values are dimensionless model values, not estimates from a species.

The previous hand-entered conversational graph is superseded by `example.gain_curve` in the JSON readout. Every point is regenerated from the equation. No hand-edited quantitative chart is used.

## 4. Verification and numerical limits

- 31 targeted tests cover reference values, strict/boundary conditions, parameter validation, unit scaling, the existing 540-cell count, and regeneration.
- The exact-threshold calculation reproduces **205 shared-optimum, 175 global-gain/local-trap, 160 positive-initial-slope** classifications on the same frozen 540 hypothetical cells. These are not independent biological replications.
- A separate 70-decimal-digit mpmath calculation on 95 deterministic test conditions yielded maximum normalized-cap relative difference `3.34e-16` and maximum separation absolute difference `2.40e-15` (rounded upward). This is an independent numerical method, **not an independent scientific reviewer**.
- Nine near-boundary cases have a theoretically positive window too narrow for reliable float subtraction. The API retains `exists_in_model=true`, reports `EXISTS_BELOW_FLOAT_RESOLUTION`, and does not call them absent.
- Production code uses only the Python standard library. A small-argument series and a negative-exponential expression avoid catastrophic cancellation and positive-exponential overflow. Unrepresentable input scales fail with ValueError.

Reproduce:

    python -m scripts.analyze_startup_thresholds
    pytest -q tests/test_startup_thresholds.py

Code: `trait_architecture/startup_thresholds.py`.
Machine-readable output: `docs/BITA_STARTUP_THRESHOLDS_READOUT_2026_11_14.json`.

## 5. Empirical boundary: what this does and does not advance

This completes a numerical bridge from the **existing conditional model** to testable separation of architectural benefit and initial accessibility. It adds **zero** independent biological studies. Peucedanum allocation data and cichlid morphology covariance do not measure these startup curves, the common-score counterfactual R-K, or historical origins. They remain contextual observations, not calibration data for c or tau.

The empirical discriminator is now explicit: an adequate dataset must distinguish (i) the cost/benefit of established separation, (ii) the cost of the first increments, and (iii) residual interference. Detecting a conflict or separated morphology alone cannot estimate the two distance thresholds. No claim of first discovery of specialization, evolutionary valleys or cost-curvature effects is made: see Rueffler, Hermisson & Wagner (2012), *PNAS*, DOI 10.1073/pnas.1110521109, and Guillaume & Otto (2012), *Genetics*, DOI 10.1534/genetics.112.143214.

**Release state:** retain Draft pending scientific review; do not merge or submit externally. Local tests cover the additive files only; full-repository CI must be verified separately at the final commit.
