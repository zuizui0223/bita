# Theory and simulation specification

## Objective

Identify when **one focal floral attraction trait** (`A`) and **one focal flower-specific barrier/defence trait** (`D`) reinforce versus oppose each other's local marginal effects on one declared biological outcome or score scale `W`.

The supplement does not assume an attraction–defence trade-off in advance and does not turn a local mixed-curvature result into an unsupported prediction of trait covariance or evolutionary endpoints.

## Focal-trait and outcome-scale rule

Each concrete application chooses one biologically defined `A`–`D` pair and one declared `W` scale.

```text
A = one focal attraction trait and its scale
D = one focal flower-specific barrier/defence trait and its scale
W = one declared fitness, relative-fitness, or score scale
```

Display size, scent, reward, nectar guides, trichomes, floral chemistry, and physical barriers are examples of possible focal traits. They are not values on one universal shared axis.

`D` is defined by its flower-specific antagonist-reduction role. A pollinator-access or pollinator-use cost is a possible collateral effect of that **same focal trait**. Evidence from unrelated `D` traits may establish mechanism plausibility, but it cannot be combined as though it estimated one system-specific mixed partial.

Fitness, relative fitness, log fitness, and an additive qualitative score are also not interchangeable curvature scales. The sign of a mixed partial is a property of the declared trait coordinates **and** the declared `W` scale.

## Core local quantity

Assume the declared `W(A,D)` surface is twice continuously differentiable around the focal point. The central quantity is

\[
W_{AD}=\frac{\partial^2W}{\partial A\partial D}
=\frac{\partial}{\partial D}\left(\frac{\partial W}{\partial A}\right).
\]

Its direct interpretation is a change in a **local marginal effect on the declared `W` scale**:

- `W_AD > 0`: increasing one focal trait raises the local marginal return to the other on that scale;
- `W_AD < 0`: increasing one focal trait lowers that return;
- `W_AD = 0`: the two marginal effects are locally independent to first order.

This is not automatically a quantitative-genetic selection gradient, trait covariance, genetic correlation, evolutionary trajectory, stable equilibrium, or global optimum.

## Diagnostic and predictive layers

For bookkeeping,

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

so algebraically

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

The manuscript does not claim novelty for that identity.

The three non-negative magnitude labels are used only after an **orientation gate** has been passed. The focal biological roles alone do not guarantee the required mixed-curvature signs. The active orientation requires locally

```text
M_AD <= 0  defence reduces the mutualist return specifically associated with marginal A
G_AD <= 0  defence reduces antagonist loss specifically associated with marginal A
C_AD >= 0  the direct joint-cost curvature is non-negative
```

Only then is it valid to write

```text
local A x D interaction
= antagonist relief
- mutualist interference
- direct joint-cost curvature.
```

This gives the diagnostic condition

```text
local complementarity
iff antagonist relief > mutualist interference + direct joint-cost curvature.
```

If an explicit model or empirical response surface gives the opposite sign for one of those curvatures, that result must remain signed. It must not be forced into a non-negative mechanism magnitude merely because `A` was called attraction or `D` was called defence.

Environmental prediction requires more structure. `P` and `H` are treated as **exogenous reference-regime indices**, not realised visitation or damage after the focal traits act. In the general local form

\[
W_{AD}=a(H)r-b(P)i-C_{AD}(P,H),
\]

stronger antagonist pressure shifts the interaction toward complementarity only when the increase in relief scaling exceeds any countervailing increase in direct cross-cost curvature. The mutualist-service prediction is likewise conditional on its local derivative inequality.

These are partial derivatives at the same focal `A,D` coordinates and `W` scale, not changes traced along an evolving optimum or an observed environmental trait cline.

## Baseline corollary

The implemented additive score gives

\[
W_{AD}
=H d_Ae_F
-P b_Ac_De^{-c_DD}(1-c_RR)
-c_{AD}.
\]

The terms are, respectively:

```text
H d_A e_F                                  antagonist relief
P b_A c_D exp(-c_D D) (1 - c_R R)         mutualist interference
c_AD                                       direct joint-cost curvature
```

Here the orientation follows from the explicit baseline functional form and non-negative parameter restrictions; it does not follow from the trait names alone.

`R` is retained only as an auxiliary moderator of the pollination-mediated channel. It is not a third focal trait in the submission claim.

## Trait coordinates and outcome scale

### Trait coordinates

Positive affine rescaling of `A` or `D` preserves the sign of the mixed partial, but arbitrary nonlinear reparameterisation can change it away from special cases. Every application must therefore declare the focal traits and their scales.

### Outcome scale

A nonlinear transformation of `W` can also change the mixed curvature. If

\[
\widetilde W=f(W),
\]

then

\[
\widetilde W_{AD}=f'(W)W_{AD}+f''(W)W_AW_D.
\]

Therefore an arbitrary monotone transformation such as log transformation does not generally preserve the sign. Positive affine rescaling of `W` does preserve the mathematical sign of a nonzero mixed partial.

The implemented result is consequently a property of the declared additive score formulation. Empirical comparison with correlational-selection coefficients requires the relevant relative-fitness and trait-standardisation conventions to be specified.

## Why the supplement does not optimise traits

A local mixed partial and an evolutionary optimum answer different questions. An optimum or evolutionary trajectory would require additional assumptions about first-order conditions, curvature or global optimality, constraints and boundaries, and a genetic variance–covariance structure or another explicit dynamical rule.

Those assumptions are not needed for the present question and are not added merely to make the model look more evolutionary.

## Sensitivity analysis

The numerical sweep varies biological parameter scenarios and a finite family of nonlinear response shapes around the baseline corollary.

The nonlinear response shapes are **endpoint-normalized on the declared `A,D in [0,1]` domain** so that attraction gain at `A=1`, antagonist protection at `D=1`, and direct joint-cost scale at `A=D=1` match the corresponding baseline endpoints. This reduces confounding between response shape and a simple change in endpoint effect magnitude.

`tested_set_unanimous` means unanimity across that finite predeclared set only. It is not a proof of mathematical structural robustness. The configured `neutral_tolerance` is an absolute numerical zero threshold on the declared score scale and is recorded in run metadata; it is not a biologically invariant neutrality band.

## Model-family implications and empirical failure conditions

1. The oriented magnitude decomposition is applicable only when the local mixed curvatures satisfy the declared sign conditions. Opposite-signed curvatures are evidence that the active orientation is incomplete or inappropriate for that focal pair.
2. A negative `D -> pollinator use` effect alone does not identify mutualist interference `M_AD < 0`; the test must determine whether `D` changes the marginal mutualist return to the specific focal `A`.
3. A protective `D -> antagonist damage` effect alone does not identify antagonist relief `G_AD < 0`; the test must determine whether `D` changes the antagonist loss associated with marginal `A`.
4. Environmental effects are conditional on how the regime changes the channel contributions; more antagonists or more mutualists do not have universal effects without the derivative conditions.
5. A sign switch occurs only where the regime-dependent channel balance crosses zero; nonlinear models may have no crossing, one crossing, or multiple crossings.
6. A direct empirical test of the focal theory requires a compatible response surface or factorial design for the same `A`–`D` pair, biological context, trait scales, and outcome scale; separate route records from different systems cannot identify the complete mixed partial.
7. A claim that the sign is invariant to transformation requires an explicit invariance argument. Neither arbitrary nonlinear trait transformations nor arbitrary nonlinear `W` transformations are automatically sign preserving.

## Link to literature evidence

The literature layer supports only a narrower abstract-level mechanism-plausibility statement: one predeclared three-cluster manipulation stratum is directionally consistent with flower-associated chemical barriers reducing pollinator preference or foraging.

That evidence does not identify `M_AD < 0` by itself and does not estimate the complete `A`–`D` mixed partial or its environmental derivative, because the full channel interactions are not measured for the same focal trait pair on compatible trait and outcome scales.
