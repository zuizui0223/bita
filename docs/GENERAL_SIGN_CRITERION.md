# Local attraction–defence interaction criterion

## 1. Scope and focal variables

The theory concerns **one declared pair of floral traits at a time**:

- `A`: one focal floral attraction trait;
- `D`: one focal flower-specific barrier/defence trait.

Examples such as display size, scent, reward, trichomes, floral chemistry, or a physical barrier are alternative applications of the framework. They are **not** assumed to lie on one universal quantitative axis and should not be pooled as raw values of the same `A` or `D` variable.

`D` is defined by a flower-specific role in reducing antagonist exposure or damage. A pollinator cost is a possible collateral effect of that **same focal trait**. A trait that only obstructs pollinators but has no declared antagonist-reduction role does not, by itself, instantiate the complete `D` mechanism.

The local fitness or fitness-score surface `W(A,D)` is assumed to be twice continuously differentiable in the focal neighbourhood. This smoothness assumption is required when writing

\[
W_{AD}
=\frac{\partial}{\partial D}\left(\frac{\partial W}{\partial A}\right)
=\frac{\partial}{\partial A}\left(\frac{\partial W}{\partial D}\right).
\]

## 2. What the mixed partial means

`W_AD` is a local change in a **marginal fitness gradient on the declared `W` scale**:

- `W_AD > 0`: increasing one focal trait raises the local marginal return to the other on that scale;
- `W_AD < 0`: increasing one focal trait lowers that local marginal return;
- `W_AD = 0`: the two local marginal effects are independent to first order at the evaluated point.

The term *selection gradient* is avoided unless `W` has been defined and scaled as the relevant relative-fitness quantity for a specific evolutionary model.

These statements do not, by themselves, imply trait covariance, a genetic correlation, an evolutionary trajectory, a stable equilibrium, or a global optimum.

## 3. Diagnostic channel decomposition and the orientation gate

For bookkeeping, write

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

where `M` is the mutualist-mediated contribution, `G` is antagonist-mediated loss, and `C` is direct investment or other joint cost. Then

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

This unrestricted identity is algebra and is **not** the novelty.

The biological roles of `A` and `D` do **not** by themselves determine the signs of these mixed curvatures. In particular:

- a defence trait reducing antagonist damage does not automatically imply `G_AD <= 0`; that sign additionally requires defence to reduce the antagonist loss specifically associated with a marginal increase in `A` in the focal neighbourhood;
- a defence trait reducing pollinator use does not automatically imply `M_AD <= 0`; that sign additionally requires the defence effect to reduce the mutualist return associated with a marginal increase in `A`;
- positive single-trait construction costs do not automatically imply `C_AD >= 0`; additive costs have `C_AD = 0`, and economies of joint construction could in principle give `C_AD < 0`.

Therefore the sign-oriented magnitude decomposition is applied only after an explicit biological model or local derivative argument establishes the relevant signs. In the oriented local hypothesis class used for the baseline mechanism,

\[
M_{AD}\le0,\qquad G_{AD}\le0,\qquad C_{AD}\ge0.
\]

Define

\[
I_P=-M_{AD}\ge0
\]

as the magnitude of **mutualist interference**, and

\[
R_H=-G_{AD}\ge0
\]

as the magnitude of **antagonist relief**. Then

\[
W_{AD}=R_H-I_P-C_{AD}.
\]

The diagnostic break-even condition is therefore

\[
W_{AD}>0
\iff
R_H>I_P+C_{AD}.
\]

This condition organizes the oriented local mechanism class. It must not be used by forcing an empirically or mechanistically opposite-signed curvature into a non-negative magnitude label. If any sign condition fails, retain the original signed terms `M_AD`, `G_AD`, and `C_AD` or derive a different biologically appropriate orientation.

The sign assumptions alone do not predict how the interaction changes across environments.

## 4. Where environmental predictions enter

Let `P` and `H` denote **exogenous reference-regime indices** for mutualist service and floral-antagonist pressure. They are not realised visitation or realised damage after `A` and `D` act; using those realised outcomes as `P` or `H` would double-count the focal trait effects.

A general local regime-scaled form is

\[
W_{AD}=a(H)r-b(P)i-C_{AD}(P,H),
\]

where `r>=0` and `i>=0` are local channel sensitivities for the declared focal trait pair after the orientation gate has been satisfied. At fixed focal `A` and `D`,

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
a'(H)r>\frac{\partial C_{AD}}{\partial H}.
\]

Stronger mutualist service shifts it toward substitutability only when

\[
b'(P)i+\frac{\partial C_{AD}}{\partial P}>0.
\]

These are partial derivatives at the **same focal phenotype neighbourhood**. They are not derivatives along an environmental cline of evolved optima or observed population means.

The linear model

\[
W_{AD}=Hr-Pi-C_{AD}
\]

is the special case `a(H)=H`, `b(P)=P`, and regime-invariant direct cross-cost curvature.

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

This product form is an interpretable sufficient construction that passes the orientation gate. It is not a necessary assumption.

## 7. Implemented baseline corollary

For the implemented score,

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

The three terms are the baseline instances of antagonist relief, mutualist interference, and direct joint-cost curvature. Their signs follow from the explicit baseline functional form and non-negative parameter restrictions, not merely from naming `A` as attraction and `D` as defence.

`R` is an auxiliary moderator in this corollary because it changes the pollination-mediated channel. It is not a third focal trait in the attraction–defence claim.

## 8. Trait scale and fitness/output scale

The sign of a mixed partial belongs to both the declared trait coordinates and the declared `W` scale.

### Trait coordinates

Positive affine rescaling of `A` or `D` preserves the sign, but arbitrary nonlinear reparameterisation can change a cross-partial away from special cases such as stationary points. Therefore:

- the biological trait definition and scale must be declared;
- raw mixed-partial magnitudes should not be compared across differently transformed trait scales;
- the framework should be applied to interpretable focal traits rather than an unspecified latent composite.

### Fitness or score scale

A nonlinear transformation of the outcome can also alter the cross curvature. If

\[
\widetilde W=f(W),
\]

then

\[
\widetilde W_{AD}
=f'(W)W_{AD}+f''(W)W_AW_D.
\]

Thus an arbitrary monotone transformation such as taking log fitness does **not** generally preserve the sign of `W_AD`. A positive affine transformation of `W` does preserve the sign.

Consequently:

- the biological outcome and its scale must be declared together with `A` and `D`;
- `fitness`, `relative fitness`, `log fitness`, and a qualitative score must not be treated as interchangeable curvature scales;
- a result derived for the implemented additive score is a property of that score formulation unless a stronger invariance argument is supplied;
- empirical comparison with correlational-selection coefficients requires the corresponding relative-fitness and trait-standardisation conventions to be stated explicitly.

This output-scale boundary is another reason the supplement does not claim a transformation-free universal sign.

## 9. Empirical bridge

The current literature layer is narrower than the theory. It asks whether flower-specific defence/barrier traits can reduce pollinator use in some systems. That supports the plausibility of one ingredient of mutualist interference.

A negative `D -> pollinator use` effect alone does **not** identify `M_AD < 0`, because the mixed curvature additionally depends on how that defence effect changes the marginal mutualist return to the particular focal attraction trait `A`. Likewise, evidence that `D` reduces antagonist damage does not by itself identify `G_AD < 0` without the corresponding attraction-linked interaction.

The literature layer therefore does **not** estimate the full `M_AD` curvature, the antagonist-relief curvature, the direct joint-cost curvature, the complete mixed partial, or the environmental derivatives of the mixed partial. A full empirical test would require the relevant channel responses for the same focal `A`–`D` pair and biological context, measured on compatible trait and outcome scales.
