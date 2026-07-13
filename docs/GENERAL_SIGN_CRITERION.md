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

This is a **diagnostic break-even criterion**. By itself it classifies competing local channel curvatures; it does not yet generate a directional environmental prediction. Treating the sign assumptions alone as a prediction would be circular.

## Where predictive content enters

A stronger model class specifies how ecological regime variables scale the local channel curvatures. Let

\[
M(A,D;P)=P\,m(A,D),\qquad G(A,D;H)=H\,g(A,D),
\]

with locally oriented per-unit curvatures

\[
m_{AD}<0,\qquad g_{AD}<0.
\]

Define

\[
i=-m_{AD}>0,\qquad r=-g_{AD}>0.
\]

Then

\[
W_{AD}=Hr-Pi-C_{AD}.
\]

This yields conditional comparative statics:

\[
\frac{\partial W_{AD}}{\partial H}=r>0,
\]

so greater antagonist pressure pushes the local interaction toward complementarity, whereas

\[
\frac{\partial W_{AD}}{\partial P}=-i<0,
\]

so greater mutualist service pushes it toward substitutability when defence interferes with the attraction-mediated mutualist return.

For fixed local rates and direct cross-cost, the break-even antagonist pressure is

\[
H^*=\frac{Pi+C_{AD}}{r}.
\]

These are the actual directional predictions of the framework. They are conditional on the local response rates and phenotype neighbourhood remaining comparable as `P` or `H` changes. If those rates themselves vary strongly with the regime, the derivative must include those dependencies explicitly.

## Why this is not just a tautology

The arithmetic decomposition alone is tautological. The biologically substantive content is layered:

1. **diagnostic layer:** declare and estimate the signs and magnitudes of the local channel curvatures;
2. **predictive layer:** specify how ecological regime variables scale those curvatures, yielding comparative statics and a break-even boundary.

The first layer organizes mechanisms. The second produces falsifiable directional predictions.

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
M_{AD}=P B'(A)Q'(D)\le 0,
\]

and

\[
G_{AD}=H F'(A)S'(D)\le 0.
\]

Thus

\[
I_P=-P B'(A)Q'(D),\qquad R_H=-H F'(A)S'(D),
\]

and the same break-even condition follows. This product structure is an interpretable sufficient construction, not a necessary assumption.

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

Thus the baseline directly exhibits the comparative statics above when the local rates are held fixed.

The numerical robustness sweep varies curvature around this corollary. It is a sensitivity analysis over selected functional forms, not a proof of the criterion and not an estimate of regime frequencies in nature.

## Empirical bridge

The literature layer currently supports only a narrower statement: defence/access limitation can reduce pollinator use in at least some systems. Under the product special case, this supports the plausibility of `Q'(D)<0`, one ingredient of the per-unit interference rate `i`.

It does **not** estimate `i`, `r`, the direct joint cost, or the complete mixed partial. A direct empirical test of the regime prediction would require comparable estimates across variation in `P` and/or `H`, ideally with the relevant local trait responses measured in the same biological context.
