# Novelty and positioning boundary

## What is not claimed as novel

The manuscript does not claim novelty for the general observations that floral traits can be shaped by both mutualists and antagonists, that attractive signals can also expose plants to enemies, or that defensive traits can carry collateral costs for beneficial visitors.

It also does **not** claim novelty for the algebraic identity

```text
W_AD = M_AD - G_AD - C_AD
```

or for merely assuming `M_AD <= 0`, `G_AD <= 0`, and `C_AD >= 0`. Those sign restrictions define a biological hypothesis class; by themselves they do not predict how the interaction changes across environments.

## The narrower theoretical contribution

The framework has two layers.

### Diagnostic layer

Oriented local channel curvatures give

```text
local A x D fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

This provides a break-even accounting identity within the declared biological hypothesis class.

### Predictive layer

When mutualist service `P` and antagonist pressure `H` scale locally comparable channel sensitivities,

```text
W_AD = H * relief_rate - P * interference_rate - joint_cost.
```

Then the model predicts, conditionally,

```text
more antagonist pressure -> W_AD increases -> toward complementarity
more mutualist service    -> W_AD decreases -> toward substitutability
```

and the break-even antagonist pressure is

```text
H* = (P * interference_rate + joint_cost) / relief_rate.
```

This comparative-static result is more substantive than simply naming the mixed-partial components. It is falsifiable, but conditional on local response rates and the phenotype neighbourhood remaining comparable across the regime contrast.

The product model

```text
W(A,D) = P B(A) Q(D) - H F(A) S(D) - C(A,D)
```

is a transparent sufficient construction, not a necessary assumption. The implemented exponential/linear model is one further corollary.

## Relation to existing ecological theory

Existing work establishes the biological ingredients used here: non-pollinating organisms can select on floral traits; floral signals can affect both mutualists and antagonists; florivory can link pollination and herbivory; and defensive traits can impose collateral effects on beneficial visitors.

The framework should therefore be positioned as a **mechanistic synthesis and formalization** of these ingredients, with its strongest theoretical contribution being the regime-scaled comparative statics and explicit break-even boundary—not the existence of the biological ingredients or an unrestricted mixed-partial identity.

A defensible claim is:

> Under a locally regime-scaled attraction–defence model, increasing antagonist pressure shifts the fitness interaction toward complementarity, whereas increasing mutualist service shifts it toward substitutability when defence interferes with attraction-mediated mutualist return; the model gives the explicit break-even boundary between these regimes.

Whether this precise formulation is unprecedented remains a prior-art question and should be established by targeted literature review rather than asserted from the mathematics alone.

## What the criterion does not establish

The sign of the mixed partial is not, by itself, a prediction of population-level trait covariance, genetic correlation, correlated evolutionary response, coevolutionary history, a global optimum, or a stable evolutionary endpoint.

The comparative statics are also conditional. If local relief or interference rates change with `P`, `H`, phenotype, or other environmental variables, those dependencies must be modelled rather than ignored.

## Empirical role of the literature layer

The literature layer is not a full empirical test of the regime prediction. Its present role is narrower: to show that defence/access limitation can reduce pollinator use in real systems.

That supports the plausibility of one ingredient of mutualist interference. It does **not** estimate the full interference rate, antagonist-relief rate, joint cost, or the response of `W_AD` to `P` or `H`.

A direct empirical test would compare matched biological contexts across variation in mutualist service and/or antagonist pressure while estimating the relevant attraction–defence fitness interaction.

## Reviewer-facing positioning

A safer abstract-level sentence is:

> We derive conditional comparative statics for a regime-scaled attraction–defence fitness model: stronger antagonist pressure shifts the local interaction toward complementarity, whereas stronger mutualist service shifts it toward substitutability when defence obstructs attraction-mediated mutualist return, with an explicit break-even boundary between the regimes.

Avoid stronger formulations such as:

- "We derive a completely general theorem for all attraction–defence systems."
- "We show for the first time that pollinators and herbivores jointly shape floral traits."
- "We predict positive or negative attraction–defence correlations from the mixed partial alone."
- "We empirically validate the complete complementarity–substitutability regime map."

These would overstate mathematical generality, prior-art novelty, or the current empirical evidence.
