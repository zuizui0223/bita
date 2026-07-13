# Mechanistic local sign criterion for attraction and defence

## Scope of the result

The central theoretical result is a **local fitness-interaction criterion**, not a direct prediction of trait covariance.

For a broad decomposition

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

the identity

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}
\]

is algebra. It is **not** itself the novelty.

Biological orientation defines a hypothesis class in which, locally,

\[
M_{AD}\le 0,\qquad G_{AD}\le 0,\qquad C_{AD}\ge 0.
\]

These signs mean that defence lowers the marginal mutualist return to attraction, defence reduces antagonist loss more strongly where attraction raises antagonist exposure, and attraction and defence have a non-negative direct joint cost.

Define

\[
I_P=-M_{AD}\ge 0,\qquad R_H=-G_{AD}\ge 0.
\]

Then

\[
W_{AD}=R_H-I_P-C_{AD},
\]

and

\[
W_{AD}>0\iff R_H>I_P+C_{AD}.
\]

This is a **diagnostic break-even criterion**. By itself it classifies competing local channel curvatures; it does not yet generate a directional environmental prediction.

## Where predictive content enters

The linear regime-scaled model used previously,

\[
W_{AD}=Hr-Pi-C_{AD},
\]

is transparent but stronger than necessary. The more general local predictive form is

\[
W_{AD}=a(H)r-b(P)i-C_{AD}(P,H),
\]

where:

- `a(H)` scales antagonist relief with antagonist pressure;
- `b(P)` scales mutualist interference with mutualist service;
- `r>0` and `i>0` are local per-unit channel sensitivities at the focal phenotype neighbourhood;
- the direct cross-cost may itself vary with the ecological regime.

The local comparative statics are

\[
\frac{\partial W_{AD}}{\partial H}
=
a'(H)r-\frac{\partial C_{AD}}{\partial H},
\]

and

\[
\frac{\partial W_{AD}}{\partial P}
=
-b'(P)i-\frac{\partial C_{AD}}{\partial P}.
\]

Therefore, increasing antagonist pressure pushes the interaction toward complementarity only when

\[
a'(H)r>\frac{\partial C_{AD}}{\partial H}.
\]

Likewise, increasing mutualist service pushes the interaction toward substitutability when

\[
b'(P)i+\frac{\partial C_{AD}}{\partial P}>0.
\]

The linear model is the special case `a(H)=H`, `b(P)=P`, and regime-invariant `C_AD`. Under that restriction,

\[
\frac{\partial W_{AD}}{\partial H}=r>0,
\qquad
\frac{\partial W_{AD}}{\partial P}=-i<0.
\]

Thus the previous directional predictions are **not** consequences of the diagnostic sign criterion alone. They require monotone regime scaling and sufficiently weak countervailing change in the direct cross-cost.

## Break-even boundaries under nonlinear scaling

A break-even antagonist pressure satisfies

\[
a(H^*)r=b(P)i+C_{AD}(P,H^*).
\]

Unlike the linear special case,

\[
H^*=\frac{Pi+C_{AD}}{r},
\]

the nonlinear equation need not have a closed-form solution. A unique threshold requires additional conditions, for example that the left-minus-right side is continuous and strictly increasing in `H` over the domain of interest.

If that monotonicity fails, there may be no threshold, one threshold, or multiple sign switches. Multiple thresholds are therefore a possible prediction of richer nonlinear models rather than a numerical pathology.

## Why this is not just a tautology

The theoretical content is layered:

1. **diagnostic layer:** define and estimate the local channel curvatures;
2. **predictive layer:** specify how ecological regime variables change those curvatures or their scaling;
3. **threshold layer:** add monotonicity conditions if a unique break-even boundary is claimed.

The first layer organizes mechanisms. The second produces local directional predictions. The third is needed before speaking of a unique ecological threshold.

## A transparent sufficient construction

A convenient special case is

\[
W(A,D)=P\,B(A)Q(D)-H\,F(A)S(D)-C(A,D),
\]

with

\[
B'(A)\ge 0,\quad Q'(D)\le 0,\quad F'(A)\ge 0,\quad S'(D)\le 0.
\]

Then

\[
I_P=-P B'(A)Q'(D),\qquad R_H=-H F'(A)S'(D),
\]

and the linear comparative statics follow if the local response derivatives and direct cross-cost are held fixed. This product structure is an interpretable sufficient construction, not a necessary assumption.

## Interpretation

- `W_AD > 0`: **local fitness complementarity**. Increasing defence raises the marginal fitness return to attraction.
- `W_AD < 0`: **local fitness substitutability**. Increasing defence lowers the marginal fitness return to attraction.
- `W_AD = 0`: local neutrality at the evaluated point.

These statements concern local curvature of the declared fitness surface. They do **not** by themselves imply population-level trait covariance, genetic correlation, coevolution, a global optimum, or the prevalence of either regime in nature.

The oriented labels are conditional. If defence facilitates mutualists, attraction and defence jointly amplify antagonist damage, or the direct cross-cost is negative, the relevant channel changes sign and must not be forced into the labels `interference`, `relief`, or `joint cost`.

## Baseline model as a corollary

For the implemented baseline score,

\[
W(A,D,R)=
P(b_0+b_AA)e^{-c_DD}(1-c_RR)
+(1-P)a_RR
-H(f_0+d_AA)(1-e_FD)
-C(A,D,R),
\]

with direct joint cost term `c_AD A D`,

\[
W_{AD}=H d_Ae_F-P b_Ac_De^{-c_DD}(1-c_RR)-c_{AD}.
\]

The mapping is

\[
r=d_Ae_F,
\]

\[
i=b_Ac_De^{-c_DD}(1-c_RR),
\]

and

\[
C_{AD}=c_{AD}.
\]

Thus the baseline is the linear, regime-invariant-cost special case. The numerical robustness sweep varies selected response-function curvature around this corollary; it is not a proof of the general monotone conditions and not an estimate of regime frequencies in nature.

## Empirical bridge

The literature layer currently supports only a narrower statement: defence/access limitation can reduce pollinator use in at least some systems. Under the product special case, this supports the plausibility of `Q'(D)<0`, one ingredient of the per-unit interference rate `i`.

It does **not** estimate `i`, `r`, the regime-scaling functions, the regime dependence of direct joint cost, or the complete mixed partial. A direct empirical test of the environmental predictions would require comparable estimates across variation in `P` and/or `H`, ideally with the relevant local trait responses measured in the same biological context.
