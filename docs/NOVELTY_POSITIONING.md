# Novelty and positioning boundary

## What is not claimed as novel

The manuscript does not claim novelty for the general observations that floral traits can be shaped by both mutualists and antagonists, that attractive signals can also expose plants to enemies, or that defensive traits can carry collateral costs for beneficial visitors.

It also does **not** claim novelty for the algebraic identity

```text
W_AD = M_AD - G_AD - C_AD
```

or for merely assuming oriented channel signs. Those restrictions define a biological hypothesis class; by themselves they do not predict how the interaction changes across environments.

## The narrower theoretical contribution

The framework has three layers.

### Diagnostic layer

Oriented local channel curvatures give

```text
local A x D fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

This provides local channel accounting within the declared biological hypothesis class.

### Predictive layer

The linear special case is

```text
W_AD = H * relief_rate - P * interference_rate - joint_cost.
```

But linear scaling is not required. A broader local form is

```text
W_AD = a(H) * relief_rate
       - b(P) * interference_rate
       - joint_cost(P, H).
```

The directional predictions are therefore conditional:

- increasing antagonist pressure moves the interaction toward complementarity when the increase in antagonist-relief scaling exceeds any increase in direct joint cost;
- increasing mutualist service moves the interaction toward substitutability when mutualist-interference scaling rises sufficiently strongly relative to any offsetting cost change.

### Threshold layer

A unique break-even boundary requires additional monotonicity conditions. In a strongly nonlinear system there may be no threshold, one threshold, or multiple sign switches.

Thus the framework does not claim that more antagonists or more mutualists always move the system in one direction. The predictions are local and conditional on regime-response derivatives.

## Relation to existing ecological theory

Existing work establishes the biological ingredients used here: non-pollinating organisms can select on floral traits; floral signals can affect both mutualists and antagonists; florivory can link pollination and herbivory; and defensive traits can impose collateral effects on beneficial visitors.

The framework should therefore be positioned as a **mechanistic synthesis and formalization** of these ingredients at the level of local attraction–defence fitness interactions. The novelty claim should not rest on the existence of the ingredients themselves, nor on the unrestricted mixed-partial identity.

A defensible claim is:

> We separate diagnostic channel accounting from the additional regime-response assumptions needed to generate directional predictions and ecological break-even boundaries for local attraction–defence fitness interactions.

Whether this precise formalization is unprecedented remains a prior-art question and should be established by targeted literature review rather than asserted from the mathematics alone.

## What the criterion does not establish

The sign of the mixed partial is not, by itself, a prediction of population-level trait covariance, genetic correlation, correlated evolutionary response, coevolutionary history, a global optimum, or a stable evolutionary endpoint.

The comparative statics are conditional. If channel sensitivities or direct cross-costs change with `P`, `H`, phenotype, or other environmental variables, those dependencies must be modelled rather than ignored.

## Empirical role of the literature layer

The literature layer is not a full empirical test of the regime prediction. Its present role is narrower: to show that defence/access limitation can reduce pollinator use in real systems.

That supports the plausibility of one ingredient of mutualist interference. It does **not** estimate the full interference rate, antagonist-relief rate, regime-scaling functions, regime-dependent joint cost, or the response of `W_AD` to `P` or `H`.

A direct empirical test would compare matched biological contexts across variation in mutualist service and/or antagonist pressure while estimating the relevant attraction–defence fitness interaction.

## Reviewer-facing positioning

A safer abstract-level sentence is:

> We derive local conditions under which antagonist relief can outweigh mutualist interference and direct joint cost, and show that environmental predictions require additional assumptions about how those channels scale with antagonist pressure and mutualist service.

Avoid stronger formulations such as:

- "We derive a completely general theorem for all attraction–defence systems."
- "More antagonists always favour complementarity and more pollinators always favour substitutability."
- "We predict positive or negative attraction–defence correlations from the mixed partial alone."
- "We empirically validate the complete complementarity–substitutability regime map."

These would overstate mathematical generality, comparative-statics scope, prior-art novelty, or the current empirical evidence.
