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

Biological content enters by specifying the local signs of the channel curvatures:

\[
M_{AD}\le 0,\qquad G_{AD}\le 0,\qquad C_{AD}\ge 0.
\]

These conditions mean, locally:

- defence/access limitation reduces the marginal mutualist return to attraction (`M_AD <= 0`);
- defence reduces antagonist damage more strongly when attraction creates more antagonist exposure (`G_AD <= 0`);
- attraction and defence have a non-negative direct joint cost (`C_AD >= 0`).

Define the non-negative oriented magnitudes

\[
I_P=-M_{AD}\ge 0
\]

for **mutualist interference**, and

\[
R_H=-G_{AD}\ge 0
\]

for **antagonist relief**. Then

\[
W_{AD}=R_H-I_P-C_{AD}.
\]

Therefore,

\[
W_{AD}>0
\iff
R_H>I_P+C_{AD}.
\]

This is the local break-even criterion used in the manuscript.

## Why this is not just a tautology

The arithmetic decomposition alone is tautological. The substantive model class is the set of systems satisfying the stated **channel meanings and local curvature signs**. Those restrictions are biological assumptions that can fail and therefore generate testable alternatives.

The criterion does **not** require the mutualist and antagonist channels to be multiplicatively separable. Product forms are sufficient constructions that make the mechanism transparent, but they are not necessary.

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
I_P=-P B'(A)Q'(D),
\]

\[
R_H=-H F'(A)S'(D),
\]

and the same break-even condition follows. This product structure is an interpretable example, not the most general admissible model.

## Interpretation

- `W_AD > 0`: **local fitness complementarity**. Increasing defence raises the marginal fitness return to attraction.
- `W_AD < 0`: **local fitness substitutability**. Increasing defence lowers the marginal fitness return to attraction.
- `W_AD = 0`: local neutrality at the evaluated point.

These statements concern local curvature of the declared fitness surface. They do **not** by themselves imply population-level trait covariance, genetic correlation, coevolution, a global optimum, or the prevalence of either regime in nature.

The oriented labels are conditional. If defence facilitates mutualists (`M_AD > 0`), if attraction and defence jointly amplify antagonist damage (`G_AD > 0`), or if the direct cross-cost is negative, the relevant channel changes sign and must not be forced into the labels `interference`, `relief`, or `joint cost`.

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
W_{AD}
=
H d_Ae_F
-
P b_Ac_De^{-c_DD}(1-c_RR)
-
c_{AD}.
\]

The mapping is

\[
R_H=Hd_Ae_F,
\]

\[
I_P=Pb_Ac_De^{-c_DD}(1-c_RR),
\]

and

\[
C_{AD}=c_{AD}.
\]

The numerical robustness sweep varies curvature around this corollary. It is a sensitivity analysis over selected functional forms, not a proof of the criterion and not an estimate of regime frequencies in nature.

## Empirical bridge

The literature layer currently supports only a narrower statement: defence/access limitation can reduce pollinator use in at least some systems. At the nonseparable level, this makes a negative mutualist channel curvature `M_AD < 0` biologically plausible only when the attraction-dependent return is also defined for the same context. Under the product special case, it supports the plausibility of `Q'(D) < 0`, one ingredient of `I_P`.

It does **not** estimate `I_P` by itself, nor the complete mixed partial. The antagonist-relief and direct joint-cost terms are not jointly estimated on compatible scales and contexts.