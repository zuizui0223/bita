# Chapter 2 theory — from trade-off balance to trait differentiation

## Programme-level question

The SCH/BITA pair is framed around a general trait-architecture problem rather than around pollination and defence themselves.

```text
Chapter 1 / SCH — BALANCE
one trait axis is pulled by conflicting functions or selective demands
-> what compromise is maintained?

Chapter 2 / BITA — DIFFERENTIATION
the conflict need not remain on one axis
-> when is it worth partitioning the functions across differentiated traits?
```

Pollinator–antagonist floral systems remain a high-resolution empirical case, but they are not the definition of either chapter.

## 1. Shared-axis architecture

Let one trait coordinate `z` contribute to two functions. Write its loss relative to the function-specific ideal as

\[
L_S(z)=\ell_1(z)+\ell_2(z),
\]

and define the best shared-axis loss

\[
L_S^*=\min_z L_S(z).
\]

The associated fitness can be written as a constant minus loss, so the architecture comparison is unchanged by working on the loss scale.

When the two functions favour different regions of trait space, the minimizing `z*` is a compromise. This is the conceptual object of SCH: multiple consequences remain coupled on one measured coordinate.

## 2. Differentiated architecture and recoverable compromise loss

Now allow two trait coordinates `x` and `y`. Before charging any fixed cost of maintaining the extra architecture, write

\[
L_{D,0}(x,y;\lambda)
=
\ell_1(x)+\ell_2(y)+\lambda c(x,y),
\]

where `lambda >= 0` scales residual coupling and `c(x,y) >= 0` is a coupling/cross-talk penalty.

The differentiated architecture is assumed to **contain the shared architecture as its diagonal special case**:

\[
c(z,z)=0,
\]

so choosing `x=y=z` reproduces the one-axis phenotype before the extra fixed architecture cost is charged.

Define

\[
L_{D,0}^*(\lambda)=\min_{x,y}L_{D,0}(x,y;\lambda),
\]

and the recoverable shared-axis conflict loss

\[
R(\lambda)=L_S^*-L_{D,0}^*(\lambda).
\]

Let `K >= 0` be the additional fixed developmental, maintenance or regulatory cost of the differentiated architecture. Then

\[
L_D^*(\lambda,K)=L_{D,0}^*(\lambda)+K,
\]

and, on the corresponding fitness scale,

\[
\Delta_{arch}=W_D^*-W_S^*=R(\lambda)-K.
\]

This form is more general than the quadratic baseline below.

## 3. General structural propositions

### Proposition 1 — a nested differentiated architecture weakly dominates before fixed cost

If the differentiated architecture contains every shared phenotype on the diagonal, then

\[
L_{D,0}^*(\lambda)\le L_S^*
\]

for every finite `lambda >= 0`, because the differentiated optimizer can always choose `x=y=z*` and attain the shared optimum.

Therefore

\[
\boxed{R(\lambda)\ge0.}
\]

This statement does **not** require quadratic, convex or smooth loss functions. It is a feasible-set result.

It is weak rather than strict. `R=0` is possible when the two functions have the same optimum, when the expanded axes cannot exploit their additional degrees of freedom, or when other restrictions make every beneficial off-diagonal state inaccessible.

After adding the fixed architecture cost,

\[
\boxed{\Delta_{arch}=R-K,}
\]

so the exact architecture decision is

\[
\boxed{\Delta_{arch}>0\iff K<R.}
\]

The biological content is therefore not that adding a degree of freedom is intrinsically beneficial. It is whether the *recoverable* loss from the original compromise is large enough to pay the extra cost of maintaining that degree of freedom.

### Proposition 2 — stronger non-negative residual coupling cannot increase recoverable loss

Suppose residual coupling enters as `lambda c(x,y)` with `c(x,y) >= 0`. For `lambda_2 > lambda_1`,

\[
L_{D,0}(x,y;\lambda_2)
\ge
L_{D,0}(x,y;\lambda_1)
\]

for every feasible `x,y`. Taking minima preserves the inequality:

\[
L_{D,0}^*(\lambda_2)
\ge
L_{D,0}^*(\lambda_1).
\]

Hence

\[
\boxed{R(\lambda_2)\le R(\lambda_1).}
\]

This coupling monotonicity is also shape-independent within the declared nested architecture. The registered numerical sweep therefore serves as an implementation check for this structural result, not as its proof.

### What remains shape dependent

The structural propositions do **not** prove that `R` is strictly positive whenever function-specific optima differ, nor do they prove a universal quantitative relation between optimum distance and `R`. Strictness and conflict-distance scaling depend on the loss geometry and feasible architecture.

Those are the roles of the quadratic corollary and the declared nonquadratic robustness family.

## 4. Quadratic corollary: decoupling fraction and a closed-form threshold

Let the two functions have quadratic losses around preferred states `theta_1` and `theta_2`, with positive weights `w_1` and `w_2`.

Shared architecture:

\[
L_S(z)=w_1(z-\theta_1)^2+w_2(z-\theta_2)^2.
\]

The best compromise is

\[
z^*=\frac{w_1\theta_1+w_2\theta_2}{w_1+w_2},
\]

with shared-axis conflict load

\[
\boxed{
L_S^*=\frac{w_1w_2}{w_1+w_2}(\theta_1-\theta_2)^2.
}
\]

For the differentiated architecture use quadratic residual coupling:

\[
L_{D,0}(x,y)
=
w_1(x-\theta_1)^2
+w_2(y-\theta_2)^2
+\lambda(x-y)^2.
\]

Let

\[
Q=w_1w_2+\lambda(w_1+w_2).
\]

Then

\[
x^*=\frac{w_1w_2\theta_1+w_1\lambda\theta_1+w_2\lambda\theta_2}{Q},
\]

\[
y^*=\frac{w_1w_2\theta_2+w_1\lambda\theta_1+w_2\lambda\theta_2}{Q}.
\]

Their optimized separation is

\[
x^*-y^*=\frac{w_1w_2}{Q}(\theta_1-\theta_2).
\]

Define the **decoupling fraction**

\[
\boxed{
s
=
\frac{|x^*-y^*|}{|\theta_1-\theta_2|}
=
\frac{w_1w_2}{w_1w_2+\lambda(w_1+w_2)}.
}
\]

For nonzero functional conflict, `s` ranges from 1 under complete decoupling toward 0 as residual coupling becomes arbitrarily strong.

The optimized differentiated loss before `K` is

\[
L_{D,0}^*
=
\frac{w_1w_2\lambda}{w_1w_2+\lambda(w_1+w_2)}
(\theta_1-\theta_2)^2.
\]

Subtracting from the shared conflict load yields

\[
R
=
\frac{w_1^2w_2^2(\theta_1-\theta_2)^2}
{(w_1+w_2)[w_1w_2+\lambda(w_1+w_2)]}.
\]

A key quadratic identity follows:

\[
\boxed{R=sL_S^*.}
\]

Thus the same fraction that describes how much function-specific phenotypic separation survives residual coupling also describes how much of the one-axis compromise loss is recoverable before paying `K`.

The architecture gain becomes

\[
\boxed{\Delta_{arch}=sL_S^*-K,}
\]

and differentiation is favoured exactly when

\[
\boxed{K<sL_S^*.}
\]

This is the reader-facing Chapter 2 corollary.

## 5. Interpretation: complete, partial and ineffective differentiation

The quadratic model makes three states explicit.

### Complete decoupling

At `lambda = 0`, `s=1`. The two trait axes can reach their own function-specific optima and the entire shared-axis conflict load is recoverable before paying `K`.

### Partial differentiation

For finite positive `lambda`,

```text
0 < s < 1.
```

The organism has two structurally distinct axes, but residual genetic, developmental, biomechanical or ecological coupling prevents complete functional privatization. This is the biologically important intermediate state.

### Ineffective differentiation

As `lambda -> infinity`, `s -> 0`; the two axes are effectively locked together and the recoverable conflict loss tends to zero. A nominally multi-part phenotype can therefore behave like an integrated one-axis architecture.

Structural differentiation must not be equated with functional independence.

## 6. Nonquadratic robustness: what the registered finite design adds

The numerical robustness model replaces the quadratic losses with

\[
L_S(z)=w_1|z-\theta_1|^p+w_2|z-\theta_2|^p,
\]

\[
L_{D,0}(x,y)
=
w_1|x-\theta_1|^p
+w_2|y-\theta_2|^p
+\lambda|x-y|^q,
\]

for `p,q > 1`.

The registered matched-curvature design contains:

```text
functional powers p = 1.5, 2, 3, 4
three asymmetric/symmetric weight pairs
five residual-coupling values
five nonzero optimum distances
= 300 evaluations at K = 0
```

Additional mismatched-curvature checks use `(p,q)=(1.5,2),(2,4),(4,2)` and architecture costs immediately below and above the recovered-loss threshold.

Current finite-family results are:

- `R > 0` in 300/300 nonzero-conflict evaluations;
- larger optimum separation increases `R` in 60/60 declared fixed-shape/weight/coupling series;
- increasing residual coupling never increases `R` in 60/60 series, as required by Proposition 2;
- setting `K` just below versus just above `R` switches the preferred architecture in all registered mismatched-curvature checks, as required by Proposition 1 plus the additive-cost definition.

The finite sweep therefore has three roles:

1. verify the numerical implementation against the structural propositions;
2. show strict positive recovery throughout the declared convex nonzero-conflict family;
3. show that the intuitive conflict-distance comparison survives the declared nonquadratic family.

It is not a universal theorem over arbitrary nonconvex, frequency-dependent or dynamically changing fitness landscapes.

Implementation and readouts:

```text
trait_architecture/differentiation_robustness.py
scripts/analyze_trait_differentiation_robustness.py
docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json
docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md
```

## 7. Environmental loading and function weights

The weights `w_1` and `w_2` can represent ecological loading of the two functions. Environmental changes can therefore move the architecture boundary even without changing the developmental system.

If one function dominates, the best shared phenotype already lies near its preferred state, leaving less loss associated with the weaker function to recover. If ecological regimes become more balanced or the function-specific optima move apart, the shared conflict load can increase and make differentiation more valuable.

This is an architecture comparison, not yet an evolutionary-dynamics model. A full trajectory model would require explicit inheritance, mutational accessibility, genetic covariance, demographic feedback and transition dynamics.

## 8. Relation to the existing BITA `A x D` framework

The existing BITA analyses solve a second problem that begins after multiple trait axes exist.

The discrete interaction

\[
\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}
\]

asks whether one trait changes the return to another on a declared outcome scale. The associated identified-set framework asks which ecological channels can produce that total interaction.

This is a **mechanism-identification module inside a multi-axis architecture**. It does not establish that evolution moved from one ancestral shared trait to two differentiated traits.

```text
positive A x D interaction
!= trait differentiation
!= historical origin of a second trait axis
!= population divergence
```

The floral attraction/defence system is therefore retained as a worked case showing how to identify mechanism once two relevant axes exist.

## 9. Empirical architecture-state anchors and their ceiling

Two non-floral literatures demonstrate that the state space represented by the theory is biologically real.

- Cichlid oral and pharyngeal jaws show structural/function partitioning together with residual evolutionary and genetic integration: a natural analogue of partial rather than complete differentiation.
- *Dalechampia* comparative history shows redeployment/exaptation and addition of functional structures through evolutionary time.

Neither literature estimates `s`, `lambda`, `K` or `Delta_arch` for the BITA model. Neither is used as a causal demonstration that a measured one-axis compromise generated the historical transition.

## 10. Claim ceiling

The Chapter 2 theory may claim:

1. **structurally**, a differentiated architecture that contains the shared architecture as a zero-extra-variable-cost special case cannot have lower optimized pre-fixed-cost fitness;
2. **structurally**, stronger non-negative coupling cannot increase recoverable compromise loss when it enters as a non-negative scaled penalty;
3. **quadratically**, `R=sL_S*` and `Delta_arch=sL_S*-K`;
4. **within the registered convex family**, strict positive recovery and conflict-distance monotonicity persist across all declared evaluations;
5. **empirically**, partial architectures and historical functional reorganization exist, while the floral case demonstrates how multi-trait mechanism allocation remains an identification problem.

The paper must not claim:

- a first general theory of specialization or division of labour;
- universality of strict differentiation advantage across arbitrary landscapes;
- that optimized-state superiority proves an accessible evolutionary transition;
- that cichlid or *Dalechampia* evidence estimates the model parameters;
- that a positive floral `A x D` interaction reconstructs trait splitting.

## 11. Chapter pair

```text
SCH / Chapter 1 — BALANCE
When one trait performs conflicting functions, what compromise is maintained?

BITA / Chapter 2 — DIFFERENTIATION
When can enough of that compromise be recovered by partial functional separation
to pay for the additional architecture, and how is the resulting mechanism identified?
```

This is broader than pollination versus defence. Floral consumer conflict is one detailed empirical realization of the general architecture problem.
