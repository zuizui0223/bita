# Biotic Interaction Trait Architecture

BITA is the **Chapter 2 / trait-differentiation** half of the SCH–BITA programme.

```text
SCH / Chapter 1 — BALANCE
conflicting functions remain coupled on one trait coordinate z
-> best shared phenotype z*
-> residual shared conflict load L_S*

BITA / Chapter 2 — DIFFERENTIATION
allow partly independent trait coordinates x,y
-> recover R from the Chapter 1 conflict load L_S*
-> pay the additional architecture cost K
-> Delta_arch = R-K
-> identify the ecological mechanism once multiple axes exist
```

The programme is about **trait trade-offs and architecture**, not specifically pollination versus defence. Floral mutualist–antagonist conflict is BITA's detailed mechanism-identification worked case.

## Exact Chapter 1 -> Chapter 2 interface

The sister relationship is a mathematical handoff rather than only shared biological motivation.

Chapter 1 keeps architecture fixed:

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin_z L_S(z)
L_S*   = L_S(z*)
```

`z*` is the best phenotype attainable while the functions remain on one shared axis. `L_S*` is the residual shared-axis conflict load on the declared scale.

BITA begins from that baseline. Let `R` be the part of the Chapter 1 conflict load recoverable after enlarging the phenotype space and let `K` be the additional fixed architecture cost:

```text
Delta_arch = R - K
Delta_arch > 0  <=>  K < R.
```

For the quadratic baseline shared with the SCH Chapter 1 framing,

```text
z* = (w1 theta1 + w2 theta2)/(w1+w2)
L_S* = [w1w2/(w1+w2)](theta1-theta2)^2

BITA:
R = s L_S*
Delta_arch = s L_S* - K.
```

Thus SCH asks **how functions optimize while they remain coupled**, whereas BITA asks **whether relaxing that shared-axis constraint pays and how the resulting multi-trait phenotype works**. SCH's shared-cue system and BITA's attraction × defence system are empirical realizations of those two architectural stages, not their general definitions.

## Canonical Chapter 2 result

### General nested-architecture result

If the differentiated architecture contains every shared phenotype on its diagonal before the extra fixed architecture cost is charged, optimizing over the larger phenotype space gives

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0  <=>  K < R
```

where `R` is the shared-compromise loss recoverable by the differentiated architecture and `K` is its additional fixed cost.

If residual coupling is represented by a non-negative scaled penalty, stronger coupling cannot increase `R`.

### Quadratic corollary

For two function-specific optima `theta1` and `theta2`, the quadratic baseline gives

```text
shared conflict load       L_S*
decoupling fraction        s = |x_opt-y_opt| / |theta1-theta2|
recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K
```

Thus differentiation is favoured when the part of the one-trait compromise that can actually be released by partial decoupling exceeds the cost of the extra architecture.

More trait axes do **not** imply complete functional independence.

## Nonquadratic robustness

Registered convex-family design:

```text
300 nonzero-conflict evaluations
strict positive pre-cost recovery:                 300 / 300
recovery increases with optimum separation:         60 / 60 series
coupling monotonicity implementation check:          60 / 60 series
```

The finite sweep tests strictness and distance dependence; coupling monotonicity is already a structural consequence of the declared non-negative coupling penalty. No universality claim is made for arbitrary nonconvex, multimodal, frequency-dependent or evolutionary-dynamic landscapes.

Core files:

- `trait_architecture/differentiation.py`
- `trait_architecture/differentiation_robustness.py`
- `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json`

## Prior-art boundary

BITA does **not** claim to invent specialization, division of labour, modularity or reduced pleiotropy under trade-offs. The closest theoretical anchors include Rüffler, Hermisson & Wagner (2012), Guillaume & Otto (2012), and Sack & Buckley (2020).

The contribution is the bridge:

```text
measurable one-axis ecological compromise
-> architecture gain with explicit partial decoupling
-> causal mechanism identification after multiple axes exist
```

## Empirical architecture-state anchors

- **Cichlid oral + pharyngeal jaws:** function partitioning with residual evolutionary/genetic integration; an empirical analogue of incomplete differentiation.
- **Dalechampia:** historical redeployment, exaptation and addition of functional/defensive structures.

Neither system estimates `s`, `lambda`, `K` or `Delta_arch`, and neither is treated as proof that the modeled trade-off caused the historical transition.

## Floral BITA: mechanism identification after differentiation

For two focal trait axes,

```text
Delta_AD W = W11 - W10 - W01 + W00
```

but the total interaction does not uniquely identify the ecological channels that generated it. The retained inference ladder is

```text
interaction detection
-> identified set
-> partial identification
-> selective A x D x antagonist x pollinator intervention
-> four-way separability diagnostic
-> independent remaining-channel assay
```

The empirical layer contains **56 source-adjudicated route records / 25 independent biological clusters** and an authoritative **17-system high-information frontier**. The result is recurrent constituent biology plus **fragmented identification**, not prevalence of trait differentiation.

Strict boundary:

```text
positive A x D interaction
!= trait differentiation
!= historical splitting

structural separation
!= functional independence

route recurrence
!= prevalence
```

## Canonical manuscript graph

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — canonical scientific source
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` — focused reference pool
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md` — figure captions
- `manuscript/trait_differentiation_figures/` — Figures 1–5
- `manuscript/CLAIM_FREEZE.md` — scientific claim ceiling
- `docs/SUBMISSION_SCOPE.md` — canonical submission scope
- `scripts/build_ecology_review_package_sources.py` — canonical package builder

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains versioned as the mature mechanism-identification component/provenance source. It is no longer the canonical article.

## Validated package state

Canonical pre-metadata package:

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
```

Theory, robustness, manuscript, figure, identification, formatter and package regressions pass. The Main is within the standard 30-page Ecology Concepts & Synthesis target. A LibreOffice OMML superscript-star rendering defect found during visual QA is normalized to explicit `opt` superscripts before PDF export.

## Submission state

**Science and pre-metadata package: GO.** Remaining blockers are author-controlled metadata/declarations/sign-off: final author list/order, affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, portal-requested reviewer information if any, all-author approval and no-simultaneous-submission confirmation.

After those fields are supplied, rebuild the exact canonical package and visually inspect every Main and Appendix page before upload.
