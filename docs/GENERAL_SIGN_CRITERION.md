# Local attraction–defence interaction criterion

## 1. Scope and focal variables

The theory concerns **one declared pair of floral traits at a time**:

- `A`: one focal floral attraction trait;
- `D`: one focal flower-specific barrier/defence trait.

Examples such as display size, scent, reward, trichomes, floral chemistry, or a physical barrier are alternative applications of the framework. They are **not** assumed to lie on one universal quantitative axis and should not be pooled as raw values of the same `A` or `D` variable.

`D` is defined by a flower-specific role in reducing antagonist exposure or damage. A pollinator cost is a possible collateral effect of that **same focal trait**. A trait that only obstructs pollinators but has no declared antagonist-reduction role does not, by itself, instantiate the complete `D` mechanism.

The local outcome surface `W(A,D)` is assumed to be twice continuously differentiable in the focal neighbourhood. The biological meaning and scale of `W` must be declared.

\[
W_{AD}
=\frac{\partial}{\partial D}\left(\frac{\partial W}{\partial A}\right)
=\frac{\partial}{\partial A}\left(\frac{\partial W}{\partial D}\right).
\]

## 2. What the mixed partial means

`W_AD` is a local change in a **marginal effect on the declared `W` scale**:

- `W_AD > 0`: increasing one focal trait raises the local marginal return to the other on that scale;
- `W_AD < 0`: increasing one focal trait lowers that local marginal return;
- `W_AD = 0`: the two local marginal effects are independent to first order at the evaluated point.

The term *selection gradient* is avoided unless `W` has been defined and scaled as the relevant relative-fitness quantity for a specific evolutionary model.

These statements do not, by themselves, imply trait covariance, a genetic correlation, an evolutionary trajectory, a stable equilibrium, or a global optimum.

## 3. Diagnostic channel decomposition, identifiability, and orientation

For mechanistic bookkeeping, write

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

where `M` is a declared mutualist-mediated contribution, `G` a declared antagonist-mediated loss, and `C` a declared direct investment or other joint-cost contribution. Then

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

This identity is algebra and is **not** the novelty.

### The decomposition is not identified by total `W` alone

A total response surface does not uniquely determine `M`, `G`, and `C`. For any sufficiently smooth function `K(A,D)`, for example,

\[
M'=M+K,\qquad C'=C+K
\]

leaves

\[
M'-G-C'=M-G-C=W
\]

unchanged while reallocating mixed curvature between the named channels.

Therefore:

- `W_AD` can be estimated from a sufficiently specified total response surface without identifying the three mechanism terms separately;
- `M_AD`, `G_AD`, and `C_AD` are **model- and measurement-dependent attributions** unless the corresponding channels are operationally defined and independently constrained;
- the three-term mechanism balance must not be presented as uniquely recoverable from total fitness data alone;
- empirical attribution requires channel-specific outcomes, manipulations, or additional structural assumptions.

The framework's mechanistic value lies in making those assumptions and missing measurements explicit, not in claiming that the decomposition is uniquely identified by algebra.

### Orientation gate

The biological roles of `A` and `D` do **not** by themselves determine the signs of the channel mixed curvatures. In particular:

- a defence trait reducing antagonist damage does not automatically imply `G_AD <= 0`; that sign additionally requires defence to reduce antagonist loss specifically associated with a marginal increase in `A`;
- a defence trait reducing pollinator use does not automatically imply `M_AD <= 0`; that sign additionally requires defence to reduce the mutualist return associated with a marginal increase in `A`;
- positive single-trait construction costs do not automatically imply `C_AD >= 0`; additive costs have `C_AD = 0`, and economies of joint construction could give `C_AD < 0`.

The sign-oriented magnitude decomposition is therefore applied only after an explicit biological model or local derivative argument establishes the relevant signs. In the oriented local hypothesis class used for the baseline mechanism,

\[
M_{AD}\le0,\qquad G_{AD}\le0,\qquad C_{AD}\ge0.
\]

Define

\[
I_P=-M_{AD}\ge0
\]

as **mutualist interference**, and

\[
R_H=-G_{AD}\ge0
\]

as **antagonist relief**. Then

\[
W_{AD}=R_H-I_P-C_{AD}.
\]

The diagnostic break-even condition is

\[
W_{AD}>0
\iff
R_H>I_P+C_{AD}.
\]

This condition organizes the oriented local mechanism class. It must not be used by forcing an opposite-signed curvature into a non-negative magnitude label. If an orientation condition fails, retain the original signed terms or derive a different biological model.

## 4. Where environmental predictions enter

Let `P` and `H` denote **exogenous reference-regime indices** for mutualist service and floral-antagonist pressure. They are not realised visitation or realised damage after `A` and `D` act; using those realised outcomes as `P` or `H` would double-count focal trait effects.

A local regime-scaled form is

\[
W_{AD}=a(H)r-b(P)i-C_{AD}(P,H),
\]

where `r>=0` and `i>=0` are local channel sensitivities for the declared focal pair after the orientation gate has been satisfied. At fixed focal `A` and `D`,

\[
\frac{\partial W_{AD}}{\partial H}
=a'(H)r-\frac{\partial C_{AD}}{\partial H},
\]

and

\[
\frac{\partial W_{AD}}{\partial P}
=-b'(P)i-\frac{\partial C_{AD}}{\partial P}.
\]

Therefore stronger antagonist pressure shifts the local interaction toward complementarity only when

\[
a'(H)r>\frac{\partial C_{AD}}{\partial H},
\]

and stronger mutualist service shifts it toward substitutability only when

\[
b'(P)i+\frac{\partial C_{AD}}{\partial P}>0.
\]

These are partial derivatives at the **same focal phenotype neighbourhood and outcome scale**. They are not derivatives along an environmental cline of evolved optima or observed population means.

The linear special case is

\[
W_{AD}=Hr-Pi-C_{AD},
\]

with `a(H)=H`, `b(P)=P`, and regime-invariant direct cross-cost curvature.

## 5. Break-even boundaries

A nonlinear break-even antagonist pressure satisfies

\[
a(H^*)r=b(P)i+C_{AD}(P,H^*).
\]

A unique threshold requires additional continuity and monotonicity conditions. Without them there may be no crossing, one crossing, or multiple sign switches.

In the linear special case with `r>0`,

\[
H^*=\frac{Pi+C_{AD}}{r}.
\]

If `r=0`, there is no unique finite antagonist-pressure threshold: either no `H` reaches break-even or every `H` is neutral when the opposing side is also zero.

## 6. Transparent product-form construction

A useful sufficient construction is

\[
W(A,D)=P\,B(A)Q(D)-H\,F(A)S(D)-C(A,D),
\]

with locally

\[
B'(A)\ge0,\quad Q'(D)\le0,\quad F'(A)\ge0,\quad S'(D)\le0.
\]

Then

\[
I_P=-P B'(A)Q'(D),
\]

and

\[
R_H=-H F'(A)S'(D).
\]

This product form is an interpretable sufficient construction that operationally defines the channels and passes the orientation gate. It is not a necessary assumption.

## 7. Implemented baseline corollary

For the implemented additive score,

\[
W(A,D,R)=
P(b_0+b_AA)e^{-c_DD}(1-c_RR)
+(1-P)a_RR
-H(f_0+d_AA)(1-e_FD)
-C(A,D,R),
\]

with direct joint cost `c_AD A D`,

\[
W_{AD}
=H d_Ae_F
-P b_Ac_De^{-c_DD}(1-c_RR)
-c_{AD}.
\]

The three terms are baseline instances of antagonist relief, mutualist interference, and direct joint-cost curvature because the baseline model explicitly assigns the corresponding processes. Their signs and attribution follow from that model, not merely from the names of `A` and `D` and not from total `W` alone.

`R` is an auxiliary moderator in this corollary because it changes the pollination-mediated channel. It is not a third focal trait in the attraction–defence claim.

## 8. Trait scale and fitness/output scale

The sign of a mixed partial belongs to both the declared trait coordinates and the declared `W` scale.

### Trait coordinates

Positive affine rescaling of `A` or `D` preserves the sign, but arbitrary nonlinear reparameterisation can change a cross-partial away from special cases. Therefore the biological trait definitions and scales must be declared, and raw mixed-partial magnitudes should not be compared across arbitrary transformations.

### Fitness or score scale

If

\[
\widetilde W=f(W),
\]

then

\[
\widetilde W_{AD}
=f'(W)W_{AD}+f''(W)W_AW_D.
\]

Thus an arbitrary monotone transformation such as taking log fitness does **not** generally preserve the sign of `W_AD`. A positive affine transformation of `W` does preserve the sign of a nonzero mixed partial.

Consequently:

- the biological outcome and its scale must be declared together with `A` and `D`;
- `fitness`, `relative fitness`, `log fitness`, and a qualitative score are not interchangeable curvature scales;
- a result derived for the implemented additive score is a property of that score formulation unless a stronger invariance argument is supplied;
- empirical comparison with correlational-selection coefficients requires the corresponding relative-fitness and trait-standardisation conventions.

## 9. Numerical sign classification

The mathematical neutral boundary is `W_AD = 0`. The numerical sweep uses an absolute `neutral_tolerance` only to classify values near zero on the declared score scale.

Because an absolute tolerance is scale dependent, generated metadata records both:

```text
neutral_tolerance
neutral_tolerance_scale = absolute_on_declared_score_scale
```

The tolerance is not a biological equivalence interval and is not invariant to rescaling `W`.

## 10. Empirical bridge

The current literature layer is narrower than the theory. It provides abstract-level directional evidence that flower-specific defence/barrier traits can reduce pollinator preference or foraging in some systems.

A negative `D -> pollinator use` effect alone does **not** identify `M_AD < 0`, because the mixed curvature additionally depends on how that defence effect changes the marginal mutualist return to the particular focal `A`. Likewise, evidence that `D` reduces antagonist damage does not by itself identify `G_AD < 0` without the corresponding attraction-linked interaction.

Most importantly, separate route records do not identify the three-term decomposition from total fitness. A full empirical mechanism test would require the relevant channel responses for the same focal `A`–`D` pair and biological context, measured on compatible trait and outcome scales, with enough design structure to distinguish mutualist, antagonist, and direct-cost contributions.
