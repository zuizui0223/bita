# Mechanistic local sign criterion for attraction and defence

## Scope of the result

The central theoretical result is a **local fitness-interaction criterion**, not a direct prediction of trait covariance.

An unrestricted decomposition

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D)
\]

implies the identity

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

That identity alone is algebra and is **not** claimed as a theorem or as the source of novelty. Biological content enters only after the mutualist and antagonist contributions are given an explicit mechanistic structure.

## Mechanistic model class

Consider the local model class

\[
W(A,D)=P\,B(A)Q(D)-H\,F(A)S(D)-C(A,D),
\]

where:

- `B(A)` is the mutualist-mediated return associated with attraction;
- `Q(D)` is the fraction of that return retained under defence/access limitation;
- `F(A)` is antagonist exposure associated with attraction;
- `S(D)` is the residual antagonist damage retained under defence;
- `C(A,D)` is direct construction, allocation, or other joint cost;
- `P,H >= 0` scale mutualist service and antagonist pressure.

The biologically oriented region used in this project assumes locally that

\[
B'(A)\ge 0,\quad Q'(D)\le 0,\quad F'(A)\ge 0,\quad S'(D)\le 0.
\]

Thus attraction can increase mutualist return and antagonist exposure, while defence/access limitation can obstruct mutualist return and reduce residual antagonist damage.

For this model class,

\[
W_{AD}
=
P B'(A)Q'(D)
-
H F'(A)S'(D)
-
C_{AD}.
\]

Define non-negative, locally oriented ecological channel magnitudes

\[
R_H=-H F'(A)S'(D)\ge 0
\]

for **antagonist relief**, and

\[
I_P=-P B'(A)Q'(D)\ge 0
\]

for **mutualist interference**. Then

\[
W_{AD}=R_H-I_P-C_{AD}.
\]

If `C_AD >= 0` represents a direct joint cost, the sign-switch condition is

\[
W_{AD}>0
\iff
R_H>I_P+C_{AD}.
\]

This is the substantive criterion used in the manuscript. It is not obtained by merely renaming an arbitrary mixed partial: `R_H` and `I_P` are induced by the stated compositional structure and derivative-sign assumptions.

## Interpretation

- `W_AD > 0`: **local fitness complementarity**. Increasing defence raises the marginal fitness return to attraction.
- `W_AD < 0`: **local fitness substitutability**. Increasing defence lowers the marginal fitness return to attraction.
- `W_AD = 0`: local neutrality at the evaluated point.

These statements concern local curvature of the declared fitness surface. They do **not** by themselves imply population-level trait covariance, genetic correlation, coevolution, a global optimum, or the prevalence of either regime in nature.

The criterion is also conditional on the oriented biological region above. If, for example, defence facilitates rather than obstructs mutualists (`Q' > 0`), or attraction reduces rather than increases antagonist exposure (`F' < 0`), those channels change sign and must not be forced into the labels `interference` or `relief`.

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

The numerical robustness sweep varies curvature around this corollary. It is a sensitivity analysis over selected functional forms, not a proof of the mechanistic criterion and not an estimate of regime frequencies in nature.

## Empirical bridge

The literature layer currently supports only a narrower statement: a negative defence/access -> pollinator-use pathway exists in at least some systems. Within the model class above, that supports the biological plausibility of `Q'(D) < 0`, one ingredient of `I_P`.

It does **not** estimate `I_P` by itself, because the full term also depends on the attraction response `B'(A)` and the relevant ecological scaling. Nor does it establish the sign of the complete mixed partial, because `R_H` and `C_AD` are not jointly estimated on a compatible scale.