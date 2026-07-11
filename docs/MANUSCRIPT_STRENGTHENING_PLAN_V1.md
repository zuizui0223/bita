# Manuscript strengthening plan v1

## Purpose

This document fixes how to make the manuscript stronger without overclaiming or
inflating weak evidence. The goal is not to make every component equally strong.
The goal is to assign each component the right role.

## Strongest manuscript architecture

```text
Main engine:        route-based conditional theory
Empirical anchor:   Impatiens asymmetric case study
General support:    route-level literature patterns
Not the claim:      universal meta-analysis or complete causal proof
```

The strongest version of the paper should not sell the literature synthesis as an
evidence-gap result. It should use the literature only to show that the route types
implied by the model recur across biological systems and to motivate why the
Impatiens case is a useful linked panel.

## Central contribution

The central contribution is the route-based causal logic:

```text
Floral attraction-defence/access relationships are not fixed trade-offs or fixed
synergies. They emerge from the balance among:

1. attraction-mediated pollination gains;
2. attraction-mediated antagonist exposure;
3. defence/access-mediated antagonist suppression;
4. defence/access-mediated pollination costs;
5. shared attraction-defence costs.
```

This is a theory claim. It does not require the empirical case study to identify every
route. Instead, the empirical case study asks which predicted routes are visible,
unresolved, or not identified in one linked system.

## Role of the Impatiens case study

The Impatiens analysis should be presented as an asymmetric empirical anchor:

```text
Visible:
  D/chemistry candidate -> lower pollinator use
  imposed florivory -> lower CH fruit production

Not resolved:
  D/chemistry candidate -> lower natural floral damage
  flower redness -> pollinator use
  flower redness -> natural floral damage
  A x D candidate -> seed component
```

This does not prove complementarity or substitutability. Its strength is that it
shows a biologically important asymmetric configuration: a defence/access-like floral
chemistry candidate has a pollination-cost-like association without a resolved
protective benefit in the same panel, while experimental florivory confirms that
floral damage can reduce a reproductive component.

## Role of literature synthesis

The literature synthesis should be described as route-level pattern support, not as a
universal parameter estimator.

Safe role:

```text
We use the literature synthesis to ask whether route-like patterns implied by the
model recur across systems, especially defence/access costs to pollinator use and
floral damage costs to reproduction.
```

Unsafe role:

```text
We estimate universal causal parameters for all four routes.
We treat failure to estimate those parameters as the main result.
```

The literature component should therefore move toward concise background, a compact
pattern table, and supplementary details. It should not dominate the Results.

## Claims that strengthen the paper

Use these claims:

```text
1. The framework explains why attraction-defence relationships can switch sign
   across ecological regimes.
2. The Impatiens case reveals an asymmetric route configuration: pollination-cost-like
   chemistry association without resolved protective benefit.
3. Randomized imposed florivory demonstrates that floral damage can reduce a
   reproductive component in the same study system.
4. The combined result shows why attraction-defence evolution needs route-level
   measurement rather than one pooled trait-fitness association.
```

## Claims that weaken the paper

Avoid these claims:

```text
1. Floral tannins causally reduce pollinator visitation.
2. Floral tannins are proven defensive traits in this panel.
3. The Impatiens case directly proves complementarity or substitutability.
4. The A x D seed component estimates the theoretical mixed partial.
5. c_AD is empirically calibrated.
6. Existing literature supports universal pooled route parameters.
7. The main novelty is simply that the literature is incomplete.
```

## Data-strength framing

The Impatiens dataset should be framed as:

```text
moderately sized but unusually linked
```

Strengths:

```text
- pre-treatment floral redness and floral tannin candidates;
- pollinator observations;
- natural floral damage;
- raw flower-level and fruit-level records with plant-cluster inference;
- reproductive components;
- flowering phenology;
- randomized 2 x 2 x 2 robbing x florivory x pollination assignment.
```

Limitations:

```text
- trait predictors are observational, not manipulated;
- primary pollinator model has many zero-visit plants;
- reproductive outcomes are components, not total lifetime fitness;
- this is a single system, not a general causal estimate.
```

## Recommended Results order

The Results should emphasize theory first, not literature gaps first:

```text
1. Conditional route model identifies regimes where A and D become complementary,
   substitutable, or unresolved.
2. Route-level literature patterns support the biological plausibility of key route
   types, especially pollination costs and damage costs, but are not treated as
   universal parameters.
3. Impatiens response-scale channel map shows pollination-cost-like D association but
   no resolved protective association.
4. Pollinator hurdle sensitivity diagnoses zero-heavy response structure.
5. Impatiens A x D reproductive component is unresolved.
6. Randomized imposed florivory reduces CH fruit production.
7. Synthesis ledger: visible routes, unresolved routes, and non-identifiable routes.
```

## Recommended Discussion spine

```text
1. Route logic clarifies why simple attraction-defence correlations are insufficient.
2. The Impatiens case is informative precisely because it is asymmetric.
3. A cost-like D -> pollinator route without a resolved D -> antagonist-suppression
   benefit is a biologically meaningful regime, not a failed result.
4. Literature patterns should be used to motivate generality, not to replace direct
   route measurement.
5. Future tests should manipulate both attraction and defence/access traits while
   measuring pollination, antagonism, and reproductive components jointly.
```

## Practical next steps

```text
1. Revise manuscript skeleton to make theory the first Results object.
2. Rewrite Methods v1 around three roles: theory, route-pattern support, Impatiens.
3. Rewrite Results v2 so the literature section is shorter and does not lead as the
   main result.
4. Build Discussion v1 using the asymmetric Impatiens result as the empirical anchor.
5. Keep the claim boundary table in the supplement or final Discussion.
```
