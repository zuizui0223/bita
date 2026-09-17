# BITA reviewer quantitative request triage V1

## Purpose

This document classifies likely reviewer requests by whether they add genuine identification information. `DO_NOW` means the request can strengthen the registered claim using current data/assumptions; `DO_IF_REQUESTED` means it is useful only if a reviewer challenges feasibility or a specific boundary; `DECLINE` means the requested number would not identify mechanism and would risk overpromotion.

| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |
|---|---|---|---|
| Run a Kessler reconstruction sensitivity analysis over the registered admissible aggregate constraints. | `DO_NOW` | Tests whether the sign of `Delta_AD W` and the zero-compatibility of `A0` survive the allowed reconstruction range. | The gain is robustness of **Level-1** interaction identification. It must not silently promote to strict **Level-2/3** release. |
| Report partial-identification bounds under each biologically defensible restriction separately. | `DO_NOW` | Shows exactly how much a restriction such as `kappa_delta >= 0` shrinks the compatible mechanism set. | State every restriction explicitly; bounds are conditional and do not become point estimates of individual channels. |
| Add a crossed-intervention power calculation for a concrete prospective design. | `DO_IF_REQUESTED` | Quantifies whether a planned `A x D x antagonist x pollinator` experiment could distinguish candidate allocations at plausible noise/sample sizes. | This addresses design feasibility only. It does not identify channel allocation in the existing evidence set. |
| Add uncertainty propagation for source-level reconstruction inputs if a reviewer challenges interval width. | `DO_IF_REQUESTED` | Can replace deterministic admissible ranges with an explicit uncertainty envelope while preserving the same estimand hierarchy. | Use only source-supported uncertainty; do not invent sampling distributions where source covariance is unavailable. |
| pool 56/25/17 into prevalence of mechanisms or interactions in nature. | `DECLINE` | None: `56 directional route records`, `25 independent biological clusters`, and `17 systems` are evidence-structure counts, not a probability sample. | `NATURAL_PREVALENCE = NOT_ESTIMATED`. More precise fractions would still be the wrong estimand. |
| Infer a residual-by-subtraction mechanism and label the remainder `kappa_delta`. | `DECLINE` | No independent identifying information is added by subtraction. | `CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED_FROM_TOTAL_INTERACTION`; a residual is not a measured mechanism. |
| Add more literature systems that do not add a new intervention/measurement dimension. | `DECLINE` | Increases citation volume but does not shrink the identified set. | Accept new systems only when they contribute a missing identification dimension or materially test recurrence at the registered frontier. |

## Revision rule

Prioritize analyses that either (1) test robustness of the observed total interaction, or (2) shrink the identified set under transparent assumptions. Decline analyses that merely make `Delta_AD W` more precise while leaving the mechanism allocation underidentified.

```text
NATURAL_PREVALENCE = NOT_ESTIMATED
CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED_FROM_TOTAL_INTERACTION
```

The current quantitative anchor supports **Level-1** positive interaction under the registered reconstruction. Because `A0` remains zero-compatible, strict **Level-2/3** release remains outside the licensed claim.
