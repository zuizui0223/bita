# L1/L2 evidence-yield meta-analysis v1

## Target

The primary analysis treats the L1/L2 literature corpus as the data object. It does not try to turn the small source-adjudicated registry into the sole analysis set.

The target is **direct-route evidence yield**: the probability that a candidate in a route and screen group directly measures the nominated route, conditional on being screenable in the frozen audit.

This is a meta-analysis of evidence availability and research asymmetry, not a biological effect-size meta-analysis.

## Inputs

- L1: all deduplicated Crossref candidates.
- L2: `priority_for_shallow_source_coding` and `biological_context_needs_route_screen` memberships.
- Frozen audit: route x screen-group direct-route outcomes among screenable records.

## Primary model

For route `r` and L2 screen group `g`:

```text
Y_rg ~ Binomial(n_rg, theta_rg)
theta_rg ~ group-level Beta(alpha_g, beta_g)
```

- `Y_rg`: source-adjudicated direct-route records in the frozen audit.
- `n_rg`: screenable audit records.
- `theta_rg`: calibrated direct-route evidence yield.
- Group-level beta priors provide partial pooling among the five route families within each L2 screen group.

The posterior of `theta_rg` is projected onto the fixed L2 route-membership universe. The output is explicitly an **equal-yield sensitivity projection**, never a count of confirmed included studies.

## Secondary methodological meta-analysis

For each route, compare direct-route audit yield in priority versus biological-nonpriority records as a log odds ratio. Pool the informative route comparisons with a DerSimonian-Laird random-effects model.

This tests whether the priority rule enriches direct empirical evidence. It does not estimate floral-trait effects.

## Non-negotiable boundaries

- Query-route memberships are retrieval strata, not independent biological studies.
- Unscreenable audit records remain unresolved; zero observed yield is not a biological null.
- L1/L2 do not contain treatment contrasts, effect sizes, or sampling variances, so they cannot produce a conventional biological-effect meta-analysis.
- The numerical-effect registry remains a separate downstream module, not a filter required for this analysis.
