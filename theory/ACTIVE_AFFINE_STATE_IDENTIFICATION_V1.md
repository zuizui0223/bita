# BITA active affine-state identification theorem v1

## Purpose

Clarify what **is** identifiable from the coupling value function after the latent-mechanism observational-equivalence theorem established what is not.

For a finite affine latent-state model, the complete latent mechanism is not generally identifiable from optimized fitness. However, at a differentiable coupling context, the affine plane of the **currently active optimized latent state** is identifiable from the value and gradient.

This gives BITA a sharp local identification boundary.

## Setup

Let latent states `r=1,...,m` have affine differentiated-loss planes

\[
D_r(\boldsymbol\lambda)
=
B_r+
\boldsymbol\lambda^\top\mathbf c_r,
\qquad
\mathbf c_r\ge0.
\]

The optimized differentiated loss is the lower envelope

\[
D^*(\boldsymbol\lambda)
=
\min_rD_r(\boldsymbol\lambda).
\]

With fixed shared benchmark `L_S*`, recoverable fitness is

\[
R(\boldsymbol\lambda)
=L_S^*-D^*(\boldsymbol\lambda).
\]

## Theorem 1 — local active penalty identification

Suppose the optimizer is unique at `lambda_0`, with active state `r*`, and `D*` is differentiable there.

Then by the envelope theorem,

\[
\boxed{
\nabla_{\boldsymbol\lambda}D^*(\boldsymbol\lambda_0)
=
\mathbf c_{r^*}.
}
\]

Equivalently,

\[
\boxed{
-\nabla_{\boldsymbol\lambda}R(\boldsymbol\lambda_0)
=
\mathbf c_{r^*}.
}
\]

Thus the current active residual-coupling penalty vector is locally identified from the coupling-response slope.

## Theorem 2 — local active baseline identification

At the same point,

\[
D^*(\boldsymbol\lambda_0)
=
B_{r^*}+
\boldsymbol\lambda_0^\top\mathbf c_{r^*}.
\]

Since both `D*(lambda_0)` and `c_r*` are identified,

\[
\boxed{
B_{r^*}
=
D^*(\boldsymbol\lambda_0)
-
\boldsymbol\lambda_0^\top
\nabla D^*(\boldsymbol\lambda_0).
}
\]

Using `R` directly,

\[
\boxed{
B_{r^*}
=
L_S^*-R(\boldsymbol\lambda_0)
+
\boldsymbol\lambda_0^\top
\nabla R(\boldsymbol\lambda_0).
}
\]

Therefore the complete affine plane parameters

\[
\boxed{(B_{r^*},\mathbf c_{r^*})}
\]

of the active optimized state are locally identifiable.

## Corollary 2a — local extrapolation of the active plane

Once `(B_r*, c_r*)` is identified, the loss that this same latent state would have at another coupling vector is

\[
\widehat D_{r^*}(\lambda)
=
B_{r^*}+\lambda^\top c_{r^*}.
\]

This is an identified **state-specific affine continuation**, not necessarily the optimized loss there: another latent state may become lower and take over the envelope.

Thus local plane identification does not justify extrapolating active-state identity across a switch.

## Theorem 3 — inactive latent states remain non-identifiable

Knowing `D*` and all of its derivatives in a neighbourhood where `r*` remains uniquely active does not identify any state `s` whose affine plane stays strictly above the active plane throughout that neighbourhood.

Such inactive states can be changed, added or removed without affecting the local value function.

Hence active-plane identification and complete mechanism identification are fundamentally different claims.

## Theorem 4 — kink identification gives a compatible active-face set

At a coupling point where several affine states tie,

\[
A(\lambda_0)
=
\{r:D_r(\lambda_0)=D^*(\lambda_0)\},
\]

`D*` is generally nondifferentiable.

Its subdifferential is

\[
\boxed{
\partial D^*(\lambda_0)
=
\operatorname{conv}
\{\mathbf c_r:r\in A(\lambda_0)\}
}
\]

under the finite affine-envelope model.

Therefore static response identifies the convex hull of active penalty vectors, not a unique active state, unless additional information separates them.

The corresponding baseline for each candidate depends on its candidate penalty vector through

\[
B_r=D^*(\lambda_0)-\lambda_0^\top c_r.
\]

## Theorem 5 — biological mechanism label requires an injective interpretation map

Suppose each registered biological mechanism label `m` maps to affine parameters

\[
\psi(m)=(B_m,c_m).
\]

If `psi` is injective on the candidate mechanism set and the active affine plane is uniquely identified, then the biological label is identified **conditional on that registered map**.

If two biological mechanisms share the same `(B,c)`, optimized coupling-fitness data cannot distinguish their labels even though the active affine plane is exactly known.

Thus a unique plane is not automatically a unique biology.

## Example

For one coupling coordinate, let

\[
D_1(\lambda)=\lambda,
\qquad
D_2(\lambda)=1.
\]

For `lambda<1`, state 1 is uniquely active:

\[
D^*(\lambda)=\lambda.
\]

Hence

\[
\frac{dD^*}{d\lambda}=1,
\]

so

\[
c_1=1,
\qquad
B_1=D^*-\lambda c_1=0.
\]

For `lambda>1`, state 2 is uniquely active and

\[
c_2=0,
\qquad
B_2=1.
\]

At `lambda=1`, both tie and the subgradient interval is

\[
[0,1],
\]

which identifies the active penalty hull but not a unique state.

## Theory -> causal bridge

This result gives three different evidential targets:

```text
coupling-response value + slope
    -> active affine plane (B,c) under the affine model
loading / structure / ecological mechanism assay
    -> biological interpretation of that plane
additional coupling regions
    -> expose previously inactive planes when they become optimal
```

A well-designed multi-level coupling experiment can therefore recover more than a net fitness gain, but it still cannot infer latent states that never become active on the tested domain.

## Relation to architecture cost K

The active-plane identification concerns differentiated loss and recoverable fitness. It does not identify architecture cost `K` unless `K` is independently measured or included in a separately identified cost model.

Thus the two nested non-identification boundaries remain:

1. `Delta_W=R-K` does not separate `R` and `K`;
2. complete `R(lambda)` does not identify inactive latent states or biological labels that share the same active affine parameters.

## Claim ceiling

The theorem assumes a finite affine latent-state representation and a unique differentiable active envelope region for point identification. Smooth nonlinear latent states require corresponding local derivative models rather than global affine extrapolation. Biological mechanism labels require a validated interpretation map. PAYOFF invasion and coexistence remain separate.