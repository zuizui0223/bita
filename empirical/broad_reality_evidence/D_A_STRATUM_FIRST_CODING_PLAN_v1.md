# d_A stratum-first coding plan v1

## Trigger

B5 previously summarized the two verified `A_to_antagonism` anchors as an arrow-
level sign conflict. That interpretation was invalid because the anchors occupy
different B2 compatibility strata:

| Verified anchor | Trait class | Outcome | Effect metric | Sign |
|---|---|---|---|---:|
| Impatiens 2018 | visual signal | floral damage proportion | standardized beta | negative |
| Gymnadenia 2016 | scent | floral damage proportion | log odds ratio | positive |

They therefore cannot be pooled or interpreted as a shared-parameter sign reversal.
The correct evidence state is `cross_stratum_heterogeneity`.

## What is to be collected

The next `d_A` effects must be coded into **separate** evidence tracks. No new
route is introduced.

```text
track 1: visual/display A -> floral antagonism H
  acceptable trait classes: visual_signal, display
  required outcomes: floral damage / florivory / oviposition / seed-predation
  only pool after trait × outcome × metric × design compatibility is satisfied

track 2: scent/reward A -> floral antagonism H
  acceptable trait classes: scent, nectar_reward
  required outcomes: floral damage / florivory / oviposition / seed-predation
  only pool after trait × outcome × metric × design compatibility is satisfied
```

A candidate must report a direct trait-to-antagonist estimate with a traceable
denominator or model coefficient, its uncertainty or recoverable sample size, and
a source locator. Agent-of-selection gradients, trait descriptions, and studies of
florivory -> pollination are not `d_A` effects.

## Priority order

1. **Scent/reward track:** resolve Schiestl et al. 2015 (`10.7554/eLife.07641`) and
   other public leads for a direct scent/nectar -> hawkmoth oviposition estimate.
2. **Visual/display track:** resolve only studies with a direct visual/display ->
   floral antagonism estimate; retain the existing Impatiens anchor as its first
   cluster.
3. Stop treating `pollination_generalization` as a B3 moderator target until either
   track has at least three compatible independent clusters and the moderator level
   is actually coded.

## Boundary

This plan does not assert that scent and visual signals have different biological
signs. It only prevents an unsupported arrow-level aggregation. The same Part I
symbol `d_A` remains the model's marginal attraction-to-antagonism channel; its
empirical calibration awaits compatible, stratum-specific evidence.
