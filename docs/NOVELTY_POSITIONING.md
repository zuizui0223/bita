# Novelty and positioning boundary

## What is not claimed as novel

The manuscript does not claim novelty for the general observations that floral traits can be shaped by both mutualists and antagonists, that attractive signals can also expose plants to enemies, or that defensive traits can carry collateral costs for beneficial visitors. Those biological ideas are established in the floral-evolution and plant–insect interaction literature.

The manuscript also does **not** claim novelty for the algebraic identity

```text
W_AD = M_AD - G_AD - C_AD
```

under an arbitrary decomposition `W = M - G - C`. Without biological restrictions on the channel curvatures, that identity is tautological.

## The narrower theoretical contribution

The contribution is a mechanistically oriented local criterion for floral attraction (`A`) and flower-specific defence/access limitation (`D`). The minimal local model class is defined by channel meanings and curvature signs:

```text
M_AD <= 0   mutualist interference
G_AD <= 0   antagonist relief after subtracting antagonist loss
C_AD >= 0   direct joint cost
```

Writing

```text
I_P = -M_AD
R_H = -G_AD
```

gives

```text
local A x D fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

Hence local complementarity occurs when `R_H > I_P + C_AD`, and local substitutability otherwise.

This framing does three things that verbal accounts can blur.

1. It does not assume an attraction–defence trade-off; the sign follows from competing ecological and direct-cost channels.
2. It distinguishes mutualist interference from a direct allocation or construction trade-off.
3. It gives a local break-even boundary while allowing nonseparable ecological response functions.

The product model

```text
W(A,D) = P B(A) Q(D) - H F(A) S(D) - C(A,D)
```

is a transparent sufficient construction, not a necessary assumption. The implemented exponential/linear model is one further corollary. The numerical robustness grid tests selected nonlinear response functions and parameter choices; it is not the source of the criterion.

## Relation to existing ecological theory

Existing work establishes the biological ingredients used here: non-pollinating organisms can select on floral traits; floral signals can affect both mutualists and antagonists; florivory can link pollination and herbivory; and defensive traits can impose collateral effects on beneficial visitors.

The framework should therefore be positioned as a **mechanistic synthesis and formalization** of these ingredients at the level of a two-trait local fitness interaction. The novelty claim should not rest on the existence of the ingredients themselves, nor on the unrestricted mixed-partial identity.

A defensible claim is:

> We identify the local curvature conditions under which antagonist relief outweighs mutualist interference and direct joint cost, making floral attraction and defence fitness complements rather than substitutes.

Whether this precise criterion is unprecedented in the literature remains a prior-art question and should be established by targeted literature review rather than asserted from the mathematics alone.

## What the criterion does not establish

The sign of the mixed partial is not, by itself, a prediction of population-level trait covariance, genetic correlation, correlated evolutionary response, coevolutionary history, a global optimum, or a stable evolutionary endpoint. Those require additional assumptions about the fitness landscape, genetic architecture, environmental variation, and evolutionary dynamics.

The criterion is also conditional on local channel signs. If defence facilitates mutualists, attraction and defence jointly amplify antagonist damage, or the direct cross-cost is negative, the corresponding channel must be reoriented rather than forced into the labels `interference`, `relief`, or `joint cost`.

## Empirical role of the literature layer

The literature layer is not a full empirical test of the criterion. Its present role is narrower: to show that defence/access limitation can reduce pollinator use in real systems.

That evidence supports the plausibility of one ingredient of mutualist interference. Under the product special case it corresponds to the plausibility of `Q'(D) < 0`; in a nonseparable model the full relevant quantity is the channel curvature `M_AD`. The current literature layer does not estimate that full curvature, the antagonist-relief term, or the complete mixed partial.

## Reviewer-facing positioning

A safer abstract-level sentence is:

> We identify a local break-even condition in which antagonist relief must exceed mutualist interference and direct joint cost for floral attraction and defence to function as fitness complements rather than substitutes.

Avoid stronger formulations such as:

- "We derive a completely general theorem for all attraction–defence systems."
- "We show for the first time that pollinators and herbivores jointly shape floral traits."
- "We predict positive or negative attraction–defence correlations from the mixed partial alone."
- "We empirically validate the complete complementarity–substitutability regime map."

These would overstate mathematical generality, prior-art novelty, or the current empirical evidence.