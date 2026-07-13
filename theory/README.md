# Theory and simulation specification

## Objective

Identify when floral attraction and flower-specific defence/access limitation are **locally complementary versus locally substitutable in fitness**, without assuming a trade-off in advance and without turning a local fitness result into an unsupported prediction of evolutionary endpoints.

## Active empirical interpretation

```text
A = A_flower: floral display, nectar guide, flower size, nectar reward, orientation
D = B_flower: flower-specific defence or pollinator-access restriction
```

Examples of `D` include floral chemical deterrents, trichomes, spines, sticky structures, and other barriers measured on the attacked or visited flowering organ. Leaf toughness, LDMC, leaf chemistry, and stem resistance are not automatically observations of `D` in the active A--D result.

The current score retains reproductive assurance `R` and leaf-consumer pressure `L` as sensitivity terms. They are not part of the core A--D claim. Terms that do not depend jointly on both `A` and `D` vanish from the mixed partial and therefore do not alter the local A--D interaction criterion.

## Core local quantity

The central quantity is

\[
W_{AD}=\frac{\partial^2 W}{\partial A\,\partial D}.
\]

Its most direct biological interpretation is a **change in a local selection gradient**:

\[
W_{AD}
=
\frac{\partial}{\partial D}\left(\frac{\partial W}{\partial A}\right)
=
\frac{\partial}{\partial A}\left(\frac{\partial W}{\partial D}\right).
\]

Thus:

- `W_AD > 0`: increasing defence raises the local marginal fitness return to attraction, and equivalently increasing attraction raises the local marginal fitness return to defence;
- `W_AD < 0`: increasing one trait lowers the local marginal fitness return to the other;
- `W_AD = 0`: the local marginal returns are independent to first order at the evaluated point.

This is a local comparative-static statement about the fitness surface. It does **not** by itself specify a population-level covariance, genetic correlation, evolutionary trajectory, stable equilibrium, or global optimum.

## Diagnostic and predictive layers

For a broad decomposition

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

the mixed partial is algebraically

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

The manuscript does not claim novelty for that identity. Biological content enters by orienting the local channel curvatures and, for environmental predictions, specifying how regime variables scale those channels.

Under the active orientation,

```text
local A x D interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

The diagnostic break-even condition is that attraction and defence are locally complementary only when antagonist relief exceeds mutualist interference plus direct joint cost.

The predictive layer then asks how ecological regime variables change those channel contributions. Linear scaling is one special case; nonlinear monotone scaling and regime-dependent joint costs are treated in `docs/GENERAL_SIGN_CRITERION.md`.

## Baseline model as a corollary

For the implemented score,

\[
\frac{\partial^2 W}{\partial A\,\partial D}
=
H d_A e_F
- P b_A c_D e^{-c_DD}(1-c_RR)
- c_{AD}.
\]

The terms map onto the active criterion:

```text
H d_A e_F                                  antagonist relief
P b_A c_D exp(-c_D D) (1 - c_R R)         mutualist interference
c_AD                                       direct joint cost
```

The additional leaf-damage term is additive in `D` but not `A`, so its A--D mixed partial is zero. Likewise, terms involving only one focal trait or neither focal trait can alter absolute fitness or single-trait gradients without changing the local A--D interaction.

## Why the supplement does not optimize traits

A local mixed partial and an evolutionary optimum answer different questions.

To claim an optimum or evolutionary endpoint, the analysis would need additional structure, including at minimum:

- first-order conditions for all evolving traits;
- second-order or global conditions establishing the relevant optimum;
- assumptions about constraints and boundaries;
- and, for evolutionary trajectories, a genetic variance--covariance structure or another explicit dynamical rule.

Those assumptions are not needed for the present question: whether the local marginal fitness effects of attraction and defence reinforce or oppose each other, and how that interaction changes across ecological regimes. Adding an optimization or evolutionary-dynamics layer without empirical support would broaden the claim rather than strengthen the current result.

## Robustness analysis

The numerical sweep varies selected response-function curvature and parameter values around the baseline corollary. Its purpose is to ask whether the sign of the local mixed partial is stable within a declared family of models.

The grid is therefore a sensitivity analysis, not a proof of the criterion and not an empirical frequency distribution over nature.

## Falsifiable model-family predictions

1. Mutualist interference pushes the local interaction toward substitutability when defence reduces the pollination return to attraction.
2. Antagonist relief pushes the local interaction toward complementarity when antagonists track attraction and defence reduces the resulting damage.
3. Direct joint cost pushes the local interaction toward substitutability independently of mutualist interference.
4. Environmental effects on the interaction are conditional on how those environments scale the three channels; stronger antagonist pressure or mutualist service does not have a universal effect without those derivative conditions.
5. A sign switch occurs only where the regime-dependent channel balance crosses zero; nonlinear models may have no crossing, one crossing, or multiple crossings.
6. Positive or negative covariance among optima is a separate, model-dependent result and must not be inferred directly from the mixed partial.

## Link to literature evidence

The literature layer currently supports a narrower statement: a defence/access -> pollination cost exists in at least some systems. That supports the biological plausibility of one ingredient of the mutualist-interference pathway.

It does not establish the complete sign of `W_AD`, estimate the environmental derivative of `W_AD`, or identify an evolutionary endpoint in those systems.