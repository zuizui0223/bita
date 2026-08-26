# Submission scope

This repository supports one integrated **identification-design Concepts & Synthesis paper** with an explicit Mechanism → Pattern bridge.

```text
Mechanism
measurable A×D interaction / channel non-identifiability / intervention-defined estimands

Pattern layer 1
cross-system recurrence of constituent ecological pathways

Pattern layer 2
identification coverage: where existing studies stop before joint allocation

Endpoint
an executable A×D×antagonist×pollinator design with internal failure diagnostics
```

The paper is not “theory plus illustrative literature,” and the Pattern synthesis is not empirical calibration of the full interaction. The recurrence layer asks whether the biological ingredients of the decomposition recur; the identification layer asks whether those ingredients have been jointly manipulated on common trait coordinates.

## Mechanism: fixed identification core

For one declared attraction trait `A`, one declared flower-associated antagonist-reducing trait `D`, and one declared outcome scale `W`, the primary experimental estimand is the two-level secant interaction

```text
Delta_AD W = W11 - W10 - W01 + W00
```

A total `Delta_AD W` does not identify channel allocation.

The proposed general experiment is

```text
A × D × antagonist access × pollinator access
```

with 16 cells. Its causal interpretation requires selective consumer interventions and unchanged A/D coordinates across consumer states.

Antagonist-relief and pollinator-increment contrasts are estimated from the crossed intervention surface. Pollinator-independent reproduction must be measured or justified through `m0_delta`; it is not assumed away.

The two apparent invariance tests are one structural diagnostic: the A×D dependence of the antagonist contrast across pollinator states and the A×D dependence of the pollinator contrast across antagonist states are the same `A×D×G×P` four-way interaction up to sign. A non-zero four-way term rejects the simple separable-channel representation.

The remaining residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

is kept unallocated. `U_delta` is not kappa by definition. Kappa requires an independent A×D construction/allocation-cost assay under standardized or suppressed biotic channels.

The elementary algebra is used only after measurement as a consistency or hidden-channel sign diagnostic.

## Pattern layer 1 — constituent ecological recurrence

The retained route synthesis contains:

```text
56 source-adjudicated route records
25 independent biological clusters
A -> pollination: 5
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system:      14
context switches: 17
```

These categories overlap. Their role is to establish **recurrence capacity of the constituent biological channels**. They are not natural-prevalence estimates and do not estimate `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

## Pattern layer 2 — identification coverage

A 16-system high-information audit asks whether the recurrent ingredients are jointly crossed in one design. The main near-miss classes are:

1. trait factorial without consumer factorial — Kessler et al. 2008;
2. consumer factorial without independently manipulated floral A×D — Egan et al. 2021;
3. observational A×D with randomized context modification rather than exclusion — *Impatiens capensis*;
4. selective flower-associated defence without independent attraction manipulation — *Pedicularis rex*;
5. other systems that fail organ, trait-orientation, intervention, baseline, or cost-assay requirements.

Current screened-set result:

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

The exact cross-system synthesis is:

> **Constituent channels recur, but their joint allocation remains unidentified.**

## Required inference boundary

The active repository must preserve:

```text
marginal route recurrence
!= total A×D interaction
!= channel interaction
!= full mechanism allocation
```

Accordingly:

- route/context counts are not prevalence;
- finite-grid fractions are not natural frequencies;
- marginal route evidence is not rho/iota;
- same-system evidence is not automatically direct A×D;
- randomized context modification is not selective exclusion;
- zero independent cost assays means kappa is unmeasured, not zero;
- `U_delta` is not kappa by subtraction;
- a non-zero four-way interaction rejects separability;
- the 2,592/77.2% finite-grid exercise remains technical Supplement sensitivity only.

## Historical material

The historical theorem-led manuscript, Leal and Sasidharan quantitative modules, and earlier figure/table architectures remain versioned for provenance. They do not define the canonical Main argument.

## Active submission package

- Main source: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- Main Figures 1–5: `manuscript/identification_figures/`
- Appendix S1: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- Pattern/identification guardrail: `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md`
- live release checklist: `submission/SUBMISSION_CHECKLIST.md`

Current validated pre-metadata package: **29 Main pages + 11 Appendix pages**, within the Ecology Concepts & Synthesis standard 30-page target.

## What remains before external submission

Only author-controlled fields and final release QA remain: authors/order/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence statement, any portal-requested reviewer fields, all-author approval, and one final rebuild/page-by-page QA after those fields are inserted.