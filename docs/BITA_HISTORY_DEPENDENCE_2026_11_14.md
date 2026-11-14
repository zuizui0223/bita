# BITA: persistence is not the same as origin or global advantage

**Status:** additive theory-only continuation of Draft #363, based on `924a2338dc253db4818648d9e550fdbec74de775`. No manuscript, existing biological results, or original model edited. No new independent biological study. Scientific review remains pending.

## 1. Frozen landscape; an explicitly additional dynamic assumption

Keep the previously specified landscape:

    Phi(u;d) = d^2 [2 h u - (h+lambda)u^2] - c[1-exp(-u/tau)],
    0 <= u <= 1, h=w1*w2/(w1+w2), s=h/(h+lambda), c>0.

Hold weights, lambda, c and tau fixed while varying d, the distance between functional optima. The cost is a **state-dependent cost** with front-loaded marginal cost. It is not a one-off sunk expense that disappears after an organ has developed. Also u is normalized separation; the physical trait-coordinate split is u*d. Keeping K(u) fixed as d changes is a modeling assumption, not a measurement.

A static fitness landscape does not itself define an evolutionary trajectory. For the history-dependent prediction below add **quasi-static projected-gradient ascent**: at fixed d, du/dt is proportional to partial Phi/partial u, projected into [0,1], and d changes slowly relative to trait-state relaxation. No stochastic escape, finite jumps, mutation supply, genetic constraints, population structure, or fixation is inferred. The old forward-only mutation walk cannot test reversals and is not used here.

## 2. An exact third boundary: persistence of a separated local maximum

Put A=h+lambda. At a positive stationary point,

    d^2 = c exp(-u/tau) / [2 A tau (s-u)],  0<u<s.

The logarithmic derivative of its right-hand side is -1/tau+1/(s-u). If tau<s, the minimum occurs at

    u_fold = s-tau,
    d_fold^2 = c exp(1-s/tau) / [2 A tau^2].

At this fold, Phi'=Phi''=0. Above it, two positive stationary branches can coexist: the lower-u branch is an unstable minimum, the upper-u branch a locally stable maximum. The boundary u=0 remains a local maximum until the previous entry threshold d_entry=sqrt(c/(2h tau)). Thus, with r=tau/s,

    d_fold/d_entry = sqrt(exp(1-1/r)/r),  0<r<1.

The previous global-benefit threshold lies strictly between them:

    d_fold < d_global < d_entry.

Proof of ordering: at the fold, Phi' is nonpositive everywhere and only touches zero at u_fold, so every positive separation still has negative gain; the global threshold is therefore larger. At d_entry with tau<s, Phi'(0)=0 and Phi''(0)>0, so sufficiently small positive separation already has positive gain; the global threshold is therefore smaller. No finite grid is needed for these inequalities.

For tau>=s, the stationary curve is monotone on u>0. There is no positive-separation fold or bistable interval: onset is continuous at the common entry/global threshold. Zero startup cost is another no-hysteresis control.

## 3. Three thresholds in the same synthetic example

Parameters are unchanged from the preceding example: w1=w2=1, lambda=.5, tau=.30, c=.315.

| Boundary | Dimensionless conflict distance d |
|---|---:|
| Loss of differentiated local maximum on downward continuation | 0.9478818271847161 |
| Equal global score of shared and differentiated architectures | 0.9736420087943984 |
| Loss of local stability of shared state on upward continuation | 1.0246950765959600 |

At **d=1**, a shared starting state remains at u=0 under local ascent, while a previously differentiated state converges to **u=0.3182809732583526**. The states occupy the same current landscape but different basins. This is not a measured biological difference.

At **d=.96**, the differentiated local maximum at **u=0.2626427179897355** still persists, even though its relative score is **-0.0052724598839576**, below the shared optimum. Local persistence is therefore not evidence of a current global advantage. Conversely, between d_global and d_entry, remaining shared is not evidence that differentiation lacks a global advantage.

A discrete quasi-static up/down ramp from .9 to 1.1 in .001 increments first leaves the shared state at **1.025** and first returns to it at **.947**. These grid events bracket the analytic thresholds; they are not substitutes for them. Exactly at a fold or local marginal boundary the API refuses to assign strict stability. Eventual reversal below the fold means this is **not permanent irreversibility**.

The dimensionless persistence/entry ratio depends only on r=tau/s. Cost c rescales all distance thresholds as sqrt(c) without changing their ratios. Increasing residual coupling at fixed weights and tau raises r and narrows the relative history-dependent interval, until it disappears at r=1. This is conditional on all the declared assumptions, not a universal ecological prediction.

## 4. Numerical implementation and independent checks

`trait_architecture/startup_hysteresis.py` adds a grid-free solver without modifying the existing modules. It uses t=-log(1-u/s) and solves

    ell(t)=t+expm1(-t)/r=log(d^2/d_entry^2).

For r<1 the minimum is at t=-log(r); bisection is bracketed separately on its two sides. A small-t series avoids cancellation. Underflowing folds retain their logarithm and a missing numeric value, not a false zero. Very narrow theoretical intervals are marked unresolved rather than absent.

Local verification: **24 new tests plus the previous 31 tests passed**. The new 120-cell finite audit obeys d_fold<d_global<d_entry in 120/120 synthetic configurations. These are not frequencies of natural strategies.

An independent 80-digit mpmath calculation uses the stationary roots

    u=s+tau*W_branch(-c exp(-s/tau)/(2 A tau^2 d^2)),

rather than the production bisection. It compared 120 fold values and 240 stationary roots: maximum relative fold difference <5e-16; maximum absolute root difference <3e-14. Eight separate fixed-environment projected-gradient ODE runs (two starting states at d=.94,.96,1,1.03) agree with the basin predictions to <6e-16. These are independent numerical methods, not an independent reviewer or biological replication.

Reproduce with `python -m scripts.analyze_startup_hysteresis` and `pytest -q tests/test_startup_hysteresis.py tests/test_startup_thresholds.py`. The JSON readout freezes the equations, parameters, numerical boundaries, ramp events and claim limits. Full-repository CI must be inspected at the final pushed commit, separately from this partial-source local verification.

## 5. Empirical translation without demanding complete K(u) data

The next empirical prediction is **different trait architecture at comparable current conditions conditional on independently documented histories**. Measuring K(u) is required for calibrating these exact thresholds, but it is not required to retain a study in a broader pattern synthesis. Do not narrow the full corpus to rare studies that measure every theoretical parameter.

Retain three distinct evidence levels: (1) context-associated architecture patterns, (2) current-environment-matched historical contrasts, and (3) bidirectional, relaxation-checked transitions identifying persistence versus entry. Levels 1 and 2 can recover partial predictions but cannot establish this particular cost mechanism. Include null/opposite contrasts and record source/lineage dependence; do not select cases for observed persistence.

The companion `empirical/trait_architecture_history/evidence_status_v1.csv` audits only the existing analysis lanes, not all available raw data. Plant allocation, cichlid cross-module covariance, and floral routing remain useful upstream observations. None of those archived analyses identifies a matched history contrast or the persistence threshold; their quantitative effects must not be relabelled as hysteresis effects. Their lack of identification is **not** an empirical null. No new meta-analytic estimate is reported.

A same-condition history effect must be separated from fixed lineage differences, unmeasured environments, plastic carry-over and finite relaxation delays. Bidirectional perturbations repeated at slower rates discriminate persistent quasistatic differences from transient lag; genetic inheritance and historical origin require further evidence. These are downstream tests, not experiments claimed completed here.

## 6. Prior art and scope

Functional specialization, residual pleiotropy and nonlinear fitness landscapes have established theory; this note does not claim first discovery of them or of hysteresis. Relevant primary precedents include Rueffler, Hermisson & Wagner (2012), *Evolution of functional specialization and division of labor*, PNAS, DOI 10.1073/pnas.1110521109; and Guillaume & Otto (2012), *Gene functional trade-offs and the evolution of pleiotropy*, Genetics, DOI 10.1534/genetics.112.143214. The contribution here is an exact, reproducible persistence/entry/global-benefit separation within BITA's already specified exponential-cost family.

Retain Draft pending scientific review. No main merge, external deposit or journal submission is authorized or performed by this update.
