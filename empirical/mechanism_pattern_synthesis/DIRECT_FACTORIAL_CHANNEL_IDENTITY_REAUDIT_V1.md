# Direct factorial channel-identity re-audit v1

## Purpose

Re-evaluate whether newly recovered crossed floral-trait experiments identify total `W_AD` or only one component channel of the Part I decomposition.

Part I defines

`W = M - G - C`

and therefore

`W_AD = M_AD - G_AD - C_AD`.

A crossed `A x D` manipulation is not sufficient by itself to identify total `W_AD`; the outcome must be the declared total fitness/biological-outcome surface, or the component channels must be measured on compatible units and recombined without hidden pathways.

## Kessler et al. 2015

### Design strength

The experiment independently silenced floral benzylacetone emission and floral nectar production in all four combinations using otherwise isogenic RNAi lines. The source also reports that the targeted pathways were specifically silenced and plants were morphologically indistinguishable from controls.

This is therefore a strong **trait-factorial design**.

### D orientation

If `D` is oriented as increasing nectar restriction / decreasing floral nectar availability, the same floral axis reduces `Manduca sexta` oviposition. The source further reports no genotype differences in oviposition in non-flowering plants, supporting a floral rather than leaf-mediated antagonist route.

Thus nectar restriction can satisfy the project’s operational antagonist-reduction gate for a flower-specific access/reward-limitation axis.

### Outcome identity

The source-reported four-cell values used for the previously reconstructed sign reversal are **pollinator-mediated outcross seed production from antherectomized flowers**.

Those values are therefore primarily a mutualist-contribution outcome. They identify an `A x D` interaction in the pollination/outcrossing channel, i.e. an `M_AD`-like object on that declared scale. They do **not** by themselves contain the antagonist loss avoided by nectar restriction, nor a separately measured direct joint-cost channel.

The source-reported discrete interactions remain:

- native visitor community: `-0.790` relative-to-EV units;
- `Manduca sexta`: `-0.432`;
- `Hyles lineata`: `+0.8699`.

The sign reversal across pollinator context is therefore real for the **mutualist channel**, but it must not be described as a sign reversal of total `W_AD`.

### Antagonist channel

The same factorial architecture also measures `M. sexta` oviposition. However, the published article reports treatment means and omnibus/post-hoc tests rather than a source-reported `A x D` interaction coefficient with uncertainty. In principle this provides a crossed antagonist-channel experiment (`G_AD`-like information), but the current public data are insufficient to combine `M_AD` and `G_AD` on one common total-fitness scale.

### Current admission

`Kessler 2015 = DIRECT_TRAIT_FACTORIAL_CHANNEL_EVIDENCE`

not

`Kessler 2015 = identified total W_AD`.

## Kessler et al. 2008

The 2008 four-genotype experiment similarly crosses floral benzylacetone and nicotine-related state and reports positive descriptive factorial structure in pollinator-mediated female outcrossing and male siring.

Those reproductive readouts again primarily represent pollination/reproductive-service consequences and do not isolate the antagonist-loss and direct-cost channels on compatible units. In addition, nicotine silencing is systemic, so the intervention-specificity caveat is stronger than in 2015.

Current admission:

`Kessler 2008 = DIRECT_TRAIT_FACTORIAL_CHANNEL_CANDIDATE`

not total `W_AD`.

## Impatiens contrast

The existing `Impatiens capensis` cluster remains the cleaner candidate for a total reproductive-outcome `A x D` interaction because the reconstructed reproductive components are closer to the declared total outcome surface. Its estimated interactions remain sign-unresolved because confidence intervals cross zero and point directions differ across reproductive components.

## Consequence for U7

The correct U7 state is now:

`TOTAL_W_AD_DIRECT_EVIDENCE = UNRESOLVED / VERY_SPARSE`

with a nested stronger statement:

`DIRECT_TRAIT_FACTORIAL_CHANNEL_INTERACTIONS = PRESENT_AND_CONTEXT_DEPENDENT`.

This distinction strengthens rather than weakens the mechanism-first argument. Part I predicts structural non-identifiability from total outcomes and requires channel-aware evidence. The Kessler experiments show that crossed floral traits can produce context-dependent interaction structure in specific channels, but they do not eliminate the need to identify the full channel balance.

## Guardrail

Do not infer total complementarity/substitutability from a channel-specific crossed interaction. A positive or negative `M_AD`-like contrast can coexist with the opposite total `W_AD` if antagonist relief or direct joint costs dominate.
