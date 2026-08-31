# Identification frontier and minimum augmentation — candidate v2

## Purpose

The canonical submission manuscript currently uses the validated 16-system V1 coverage audit. A separately versioned **17-system candidate frontier** asks a different question: what information does each near-target study already contribute, and what additional module would move it toward mechanism identification?

The 17-system candidate is stored in `HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv`; it does not silently change the canonical V1 denominator.

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

## Candidate frontier anchors

- **Kessler et al. 2008** — direct A×D-like trait-factorial anchor. The post-PR-153 registered result is authoritative: `A1` is uniformly positive under the declared aggregate restrictions, `A0` remains narrowly zero-compatible, Level 1 has a strong aggregate anchor, and Level 2/3 remain unresolved under source/design uncertainty.
- **Egan et al. 2021** — consumer-factorial anchor; pollination and herbivory are crossed, while focal floral A/D are not independently crossed and defence is leaf-derived.
- **Soper Gorden & Adler 2018** — observational A/D plus randomized context modification, not selective G/P access.
- **Sun & Huang 2015 / Pedicularis rex** — selective flower-associated D manipulation without independent A.
- **Theis & Adler 2012** — manipulated fragrance crossed with repeated beetle removal and supplemental hand pollination. This is `A × G × P_supplementation`, not a true pollinator-access toggle, and it has no independent D.

These anchors are deliberately complementary. None dominates the others across all information dimensions.

## Minimum-augmentation principle

For each system, the next question is not `does this study fully identify the mechanism?` but:

> What is the smallest biologically defensible addition that moves this existing design to a strictly more informative identification layer?

This is not a cell-count optimization. A technically small manipulation can be biologically invalid, whereas a larger experiment can be the minimum valid augmentation. The matrix therefore records missing modules rather than assigning an arbitrary scalar distance.

## Conditional partial-identification boundary

The candidate frontier preserves the older source-rounded Kessler `Delta_AD = +0.19 to +0.25` statement only as provenance for an assumption-indexed sensitivity calculation. It is not a confidence interval and must not replace the canonical registered A0/A1 result.

For the accounting identity

`Delta_AD W = rho_delta - iota_delta - kappa_delta`,

an explicit same-scale restriction `kappa_delta >= 0` implies

`rho_delta - iota_delta >= Delta_AD W`.

This remains a structural bound conditional on both the declared outcome scale and the auxiliary restriction. It does not identify `rho_delta`, `iota_delta`, or `kappa_delta` separately.

## Candidate-to-canonical promotion rule

A later promotion PR may replace the canonical 16-system V1 count with this 17-system candidate only if manuscript, Figure 4, supplement, references, target-journal package, and regression tests are updated together while preserving:

- the Level 1 / Level 2 / Level 3 outcome hierarchy;
- the registered Kessler A0/A1 partial-identification result;
- Theis & Adler as supplementation rather than P-access;
- `m0_delta = 0/17`, independent `kappa = 0/17`, and full allocation closure `= 0/17` as screened-set coverage rather than literature prevalence.

Until then, V2 is a validated candidate frontier and V1 remains the canonical submission input.
