# Theory and simulation specification

## Objective

Identify when **one focal floral attraction trait** (`A`) and **one focal flower-specific barrier/defence trait** (`D`) reinforce versus oppose each other's local marginal fitness effects.

The supplement does not assume an attraction–defence trade-off in advance and does not turn a local fitness result into an unsupported prediction of trait covariance or evolutionary endpoints.

## Focal-trait rule

Each concrete application chooses one biologically defined `A`–`D` pair.

```text
A = one focal attraction trait
D = one focal flower-specific barrier/defence trait
```

Display size, scent, reward, nectar guides, trichomes, floral chemistry, and physical barriers are examples of possible focal traits. They are not values on one universal shared axis.

`D` is defined by its flower-specific antagonist-reduction role. A pollinator-access or pollinator-use cost is a possible collateral effect of that **same focal trait**. Evidence from unrelated `D` traits may establish mechanism plausibility, but it cannot be combined as though it estimated one system-specific mixed partial.

## Core local quantity

Assume the declared score or fitness surface is twice continuously differentiable around the focal point. The central quantity is

\[
W_{AD}=\frac{\partial^2W}{\partial A\partial D}
=\frac{\partial}{\partial D}\left(\frac{\partial W}{\partial A}\right).
\]

Its direct interpretation is a change in a **local marginal fitness gradient**:

- `W_AD > 0`: increasing one focal trait raises the local marginal fitness return to the other;
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
- direct joint cost.
```

This gives the diagnostic condition

```text
local complementarity
iff antagonist relief > mutualist interference + direct joint cost.
```

If an explicit model or empirical response surface gives the opposite sign for one of those curvatures, that result must remain signed. It must not be forced into a non-negative mechanism magnitude merely because `A` was called attraction or `D` was called defence.

Environmental prediction requires more structure. `P` and `H` are treated as **exogenous reference-regime indices**, not realised visitation or damage after the focal traits act. In the general local form

\[
W_{AD}=a(H)r-b(P)i-C_{AD}(P,H),
\]

stronger antagonist pressure shifts the interaction toward complementarity only when the increase in relief scaling exceeds any countervailing increase in direct cross-cost. The mutualist-service prediction is likewise conditional on its local derivative inequality.

These are partial derivatives at the same focal `A,D` coordinates, not changes traced along an evolving optimum or an observed environmental trait cline.

## Baseline corollary

The implemented baseline gives

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
c_AD                                       direct joint cost
```

Here the orientation follows from the explicit baseline functional form and non-negative parameter restrictions; it does not follow from the trait names alone.

`R` is retained only as an auxiliary moderator of the pollination-mediated channel. It is not a third focal trait in the submission claim.

## Trait scale

The sign of the mixed partial belongs to the declared trait coordinates. Positive affine rescaling preserves the sign, but arbitrary nonlinear reparameterisation can change a cross-partial away from special cases. Every application must therefore declare the focal traits and their scales; raw mixed-partial magnitudes are not portable across arbitrary transformations.

## Why the supplement does not optimise traits

A local mixed partial and an evolutionary optimum answer different questions. An optimum or evolutionary trajectory would require additional assumptions about first-order conditions, curvature or global optimality, constraints and boundaries, and a genetic variance–covariance structure or another explicit dynamical rule.

Those assumptions are not needed for the present question and are not added merely to make the model look more evolutionary.

## Sensitivity analysis

The numerical sweep varies selected response-function curvature and parameter values around the baseline corollary. Its purpose is to ask whether the sign of the local mixed partial is stable within a finite, declared family of models.

`tested_set_unanimous` means unanimity across that finite predeclared set only. It is not a proof of mathematical structural robustness. The grid is a sensitivity analysis, not a proof of the criterion and not an empirical frequency distribution over nature.

## Model-family implications and empirical failure conditions

1. The oriented magnitude decomposition is applicable only when the local mixed curvatures satisfy the declared sign conditions. Opposite-signed curvatures are evidence that the active orientation is incomplete or inappropriate for that focal pair.
2. A negative `D -> pollinator use` effect alone does not identify mutualist interference `M_AD < 0`; the test must determine whether `D` changes the marginal mutualist return to the specific focal `A`.
3. A protective `D -> antagonist damage` effect alone does not identify antagonist relief `G_AD < 0`; the test must determine whether `D` changes the antagonist loss associated with marginal `A`.
4. Environmental effects are conditional on how the regime changes the channel contributions; more antagonists or more mutualists do not have universal effects without the derivative conditions.
5. A sign switch occurs only where the regime-dependent channel balance crosses zero; nonlinear models may have no crossing, one crossing, or multiple crossings.
6. A direct empirical test of the focal theory requires a compatible response surface or factorial design for the same `A`–`D` pair and biological context; separate route records from different systems cannot identify the complete mixed partial.

## Link to literature evidence

The literature layer supports only a narrower mechanism-plausibility statement: flower-associated defence/barrier traits can reduce pollinator use in some systems.

That evidence does not identify `M_AD < 0` by itself and does not estimate the complete `A`–`D` mixed partial or its environmental derivative, because the full channel interactions are not measured for the same focal trait pair on compatible scales.
