# Identification-frontier design v1

## Purpose

The 16-system audit should not end at `full identification = 0`. Existing studies carry different pieces of the required information. This document defines an auditable, non-scalar way to represent those pieces and to ask what additional intervention would move each study to the next identification layer.

## Information layers

The layers are ordered by what the data can identify, not by study quality.

1. `route_or_axis` — one or more constituent ecological pathways or trait axes are documented, but no focal A×D total interaction is identified.
2. `joint_trait_observation` — A and D are observed on a common system/outcome, but no experimentally crossed focal A×D interaction is available.
3. `total_interaction` — a focal A×D interaction is directly estimable or tightly approximated on a declared scale.
4. `randomized_context_modification` — a total/observational A×D term is paired with randomized manipulation of interaction intensity or consumer context, but not selective consumer-channel toggles.
5. `consumer_factorial` — antagonist/herbivory and pollination environments are experimentally crossed, but the focal A and D traits are not independently crossed on the same coordinates.
6. `channel_partial_identification` — at least one selective channel contrast or independent channel bound constrains the identified set for the same A×D contrast.
7. `biotic_point_identification` — crossed selective A×D×G×P interventions, baseline handling, and a successful separability diagnostic identify `rho_delta` and `iota_delta`.
8. `full_allocation_closure` — an independent commensurate A×D joint-cost assay additionally constrains/closes `kappa_delta`.

The layers form an information frontier rather than a scalar quality score. A study can contain a strong consumer factorial while lacking the trait factorial, or a strong trait factorial while lacking consumer interventions.

## Canonical frontier anchors in the current screened set

- **Kessler et al. 2008** — strongest direct trait-factorial anchor; direct discrete A×D sign is positive under published aggregate constraints, but D has a systemic-scope caveat and no crossed selective consumer toggles are present.
- **Egan et al. 2021** — strongest consumer-factorial anchor; pollination and herbivory are experimentally crossed, but the focal attraction and defence traits are measured rather than independently crossed and defence is leaf-derived.
- **Soper Gorden & Adler 2018** — randomized-context anchor; an observational A×D term can be tested for randomized robbing/florivory/pollination modification, but the traits are not randomized and treatments are intensity additions rather than selective exclusions.
- **Sun & Huang 2015 / Pedicularis rex** — selective-D system anchor; a physical flower-associated defence manipulation selectively affects seed predation without a detected visitation effect, but no independent attraction manipulation exists.

These four anchors are deliberately complementary. None dominates the others across all information dimensions.

## Minimum-augmentation principle

For each system, the next question is not `does this study fully identify the mechanism?` but:

> What is the smallest biologically defensible addition that moves this existing design to a strictly more informative identification layer?

This is not a cell-count optimization. A technically small manipulation can be biologically invalid, whereas a larger experiment can be the minimum valid augmentation. The matrix therefore records missing *modules* rather than assigning an arbitrary scalar distance.

## Conditional partial identification from existing total-interaction anchors

When a total interaction is available, it can constrain the identified set before full crossed interventions. For

`Delta_AD W = rho_delta - iota_delta - kappa_delta`,

`kappa_delta >= 0` implies

`rho_delta - iota_delta >= Delta_AD W`.

For Kessler et al. 2008, the published rounded probability-scale interaction range is `+0.19 to +0.25`. Conditional on treating that rounded range as the available aggregate constraint and on the explicit same-scale restriction `kappa_delta >= 0`, the biotic balance is bounded below by `+0.19`. This is **not a confidence bound** because formal A×D uncertainty is unrecovered, and it is **not an empirical estimate of kappa**. It is an assumption-indexed partial-identification consequence of the published aggregate interaction range.

The break-even interpretation is also useful: a negative hidden joint channel would need to be at least as large in magnitude as the positive total interaction to erase the positive biotic balance. Under the rounded probability-scale constraints, that threshold lies between `-0.19` and `-0.25`, again as an aggregate-constraint sensitivity statement rather than a sampling interval.

## Output boundary

The companion frontier matrix preserves the original audit columns and adds only transparent derived labels:

- `frontier_face`
- `next_major_augmentation`
- `remaining_gates_after_next_step`
- `conditional_partial_id_note`

No study-specific `rho_delta`, `iota_delta`, or `kappa_delta` point values are inferred. No scalar study ranking is produced.
