# Novelty and positioning boundary

## What is not claimed as novel

The manuscript does not claim novelty for the general observations that floral traits can be shaped by both mutualists and antagonists, that attractive signals can also expose plants to enemies, or that defensive traits can carry collateral costs for beneficial visitors. Those biological ideas are established in the floral-evolution and plant–insect interaction literature.

The manuscript also does **not** claim novelty for the algebraic identity

```text
W_AD = M_AD - G_AD - C_AD
```

under an arbitrary decomposition `W = M - G - C`. Without additional biological structure, that identity is tautological.

## The narrower theoretical contribution

The contribution is a mechanistically structured local criterion for floral attraction (`A`) and flower-specific defence/access limitation (`D`). For the model class

```text
W(A,D) = P B(A) Q(D) - H F(A) S(D) - C(A,D),
```

with attraction increasing mutualist return and antagonist exposure, and defence reducing both retained mutualist return and residual antagonist damage, the mixed partial becomes

```text
local A x D fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

This framing does three things that verbal accounts can blur.

1. It does not assume an attraction–defence trade-off. The sign follows from explicit ecological channels.
2. It distinguishes mutualist interference from a direct allocation or joint-cost trade-off.
3. It gives a break-even boundary within the stated model class: local complementarity occurs when antagonist relief exceeds mutualist interference plus direct joint cost.

The implemented exponential/linear model is one corollary. The numerical robustness grid tests selected nonlinear response functions and parameter choices; it is not the source of the criterion.

## Relation to existing ecological theory

Existing work establishes the biological ingredients used here: non-pollinating organisms can select on floral traits; floral signals can affect both mutualists and antagonists; florivory can link pollination and herbivory; and defensive traits can impose collateral effects on beneficial visitors.

The framework should therefore be positioned as a **mechanistic synthesis and formalization** of these ingredients at the level of a two-trait local fitness interaction. The novelty claim should not rest on the existence of the ingredients themselves, nor on an unrestricted mixed-partial identity.

A defensible claim is:

> Within an explicit model class linking attraction to mutualist return and antagonist exposure, and defence to mutualist obstruction and antagonist suppression, we derive the local break-even condition separating fitness complementarity from fitness substitutability.

Whether this precise criterion is unprecedented in the literature remains a prior-art question and should be established by targeted literature review rather than asserted from the mathematics alone.

## What the criterion does not establish

The sign of the mixed partial is not, by itself, a prediction of population-level trait covariance, genetic correlation, correlated evolutionary response, coevolutionary history, a global optimum, or a stable evolutionary endpoint. Those require additional assumptions about the fitness landscape, genetic architecture, environmental variation, and evolutionary dynamics.

The criterion is also conditional on local derivative signs. If defence facilitates mutualists or attraction reduces antagonist exposure, the corresponding channel changes sign and the labels `interference` and `relief` must be revised rather than imposed.

## Empirical role of the literature layer

The literature layer is not a full empirical test of the criterion. Its present role is narrower: to show that defence/access limitation can reduce pollinator use in real systems.

That evidence supports the plausibility of `Q'(D) < 0`, an ingredient of the mutualist-interference term. It does **not** by itself estimate the full interference term, because that term also depends on the attraction response and ecological scaling. The complete mixed partial would require all relevant channel strengths to be estimated on compatible scales and contexts.

## Reviewer-facing positioning

A safer abstract-level sentence is:

> We derive, for a mechanistically explicit class of attraction–defence fitness models, a local break-even condition under which antagonist relief outweighs mutualist interference and direct joint cost, making the two traits fitness complements rather than substitutes.

Avoid stronger formulations such as:

- "We derive a completely general theorem for all attraction–defence systems."
- "We show for the first time that pollinators and herbivores jointly shape floral traits."
- "We predict positive or negative attraction–defence correlations from the mixed partial alone."
- "We empirically validate the complete complementarity–substitutability regime map."

These would overstate mathematical generality, prior-art novelty, or the current empirical evidence.