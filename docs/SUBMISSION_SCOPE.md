# Submission scope

This repository supports one integrated **identification-design Concepts & Synthesis paper** with an explicit Mechanism → Pattern bridge and a partial-identification middle layer.

```text
Mechanism
measurable A×D interaction / channel allocation identity

Identification layer 1
identified set from the total interaction

Identification layer 2
partial identification under explicit biological/channel bounds

Pattern layer 1
cross-system recurrence of constituent ecological pathways

Pattern layer 2
fragmented identification frontier across existing studies

Endpoint
selective A×D×antagonist×pollinator design + m0 + separability + independent joint-channel assay
```

## Fixed identification core

For one declared attraction trait `A`, one declared flower-associated antagonist-reducing trait `D`, and one outcome scale `W`,

```text
Delta_AD W = W11 - W10 - W01 + W00
```

and

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

If `Delta_AD W = delta` is the only channel-allocation information, compatible mechanisms form

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}.
```

This is structural non-identification, not a sampling-power problem. Explicit restrictions can still shrink the set. The principal recovered bound is

```text
kappa_delta >= 0
=> rho_delta - iota_delta >= Delta_AD W.
```

For positive `Delta_AD W`, the biotic balance is therefore forced positive under the stated kappa restriction even when rho and iota remain individually unidentified. The restriction must be defended biologically; it is not treated as a universal law.

Point identification uses a 16-cell

```text
A × D × antagonist access × pollinator access
```

design with selective interventions and invariant A/D coordinates. Pollinator-independent reproduction is measured or justified through `m0_delta`. The apparent rho and iota cross-context invariance checks are the same `A×D×G×P` four-way contrast up to sign; a non-zero value rejects the simple separable-channel representation.

The residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

remains unallocated. It is not kappa by subtraction; kappa requires an independent A×D assay.

## Pattern layer 1 — constituent ecological recurrence

Retained source-adjudicated synthesis:

```text
56 route records
25 independent biological clusters
A -> pollination: 5
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system:      14
context switches: 17
```

These overlapping categories establish recurrence capacity only. The source-adjudicated route ledger is **not itself a grand meta-analysis**. They are not prevalence estimates and do not estimate `Delta_AD W`, rho, iota, or kappa.

## Pattern layer 2 — fragmented identification frontier

The 16-system high-information audit asks which dimensions of the identified set are already constrained by existing experiments. The main complementary faces are:

1. Kessler et al. 2008 — trait-factorial side;
2. Egan et al. 2021 — consumer-factorial side;
3. *Impatiens capensis* — observational A×D plus randomized context modification;
4. *Pedicularis rex* — selective flower-associated defence system anchor;
5. other systems exposing trait-orientation, organ-scope, intervention, baseline, or cost-assay gaps.

Screened-set facts remain:

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

but the stronger synthesis is not simply `0/16`. Constituent channels recur, but their joint allocation remains unidentified. Existing studies occupy complementary faces of the allocation problem. The practical question is therefore **which smallest additional measurement or intervention most shrinks the remaining identified set?**

## Required inference boundary

```text
marginal route recurrence
!= total A×D interaction
!= partial channel bounds
!= point-identified channel interaction
!= full mechanism allocation
```

Accordingly:

- route/context counts are not prevalence;
- finite-grid fractions are not natural frequencies;
- total `Delta_AD W` alone defines a set, not a unique mechanism;
- partial-identification claims must name their assumptions/bounds;
- randomized context modification is not selective exclusion;
- zero independent cost assays means kappa is unmeasured, not zero;
- `U_delta` is not kappa by subtraction;
- a non-zero four-way interaction rejects separability;
- the 2,592/77.2% finite-grid exercise remains technical Appendix sensitivity only.

## Active package

- Main: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- Figures 1–5: `manuscript/identification_figures/`
- Appendix S1: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- partial-identification derivation: `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md`
- bridge guardrail: `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md`
- release checklist: `submission/SUBMISSION_CHECKLIST.md`

Current validated pre-metadata package: **29 Main pages + 12 Appendix pages**, five Main figures, all 41 pages visually inspected.

## Remaining external-submission work

Only author-controlled fields/sign-off and the final post-metadata rebuild remain: author order/names/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, any portal-requested reviewer fields, all-author approval, no-simultaneous-submission confirmation, then exact rebuild and page-by-page QA.