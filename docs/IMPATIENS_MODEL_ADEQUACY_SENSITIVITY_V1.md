# *Impatiens capensis* pollinator-rate model adequacy sensitivity

## Trigger

The primary response-scale pollinator model is a robust quasi-Poisson log-link
regression of the documented 60-minute-standardized integer outcome
`Pollinators_Per_Hour`. In the first empirical-core rerun, the complete-case panel
had:

```text
n = 81 individual plants
zero visit counts = 52
Pearson dispersion = 23.18
```

The robust sandwich interval remains the primary rate-model uncertainty estimate,
but this much zero mass and overdispersion makes a single mean-rate process an
inadequate sole description of the data.

## Sensitivity specification

The following two-part analysis is labelled **post-primary model-adequacy
sensitivity**, not a replacement confirmatory test and not a source of model
selection.

```text
Part 1: any pollinator visit (0/1) ~ A + D + treatments + phenology
        fractional-logit/binomial mean model; robust sandwich SE

Part 2: pollinator count conditional on count > 0 ~ A + D + treatments + phenology
        quasi-Poisson log-link; robust sandwich SE
```

The covariate set, trait transformations, and individual-plant unit are identical
to the primary rate model. The `count > 0` rule is the only new conditioning step.

## Interpretation boundary

- Part 1 describes association with a visit being observed during the standardized
  observation window.
- Part 2 describes association with standardized visit intensity among plants where
  a visit was observed.
- Neither part identifies a causal effect of floral redness or floral tannins.
- The sensitivity cannot be used to choose whichever result favors a theory. Its
  only role is to reveal whether a primary mean-rate association is concentrated in
  zeros, positive intensity, both, or neither.
