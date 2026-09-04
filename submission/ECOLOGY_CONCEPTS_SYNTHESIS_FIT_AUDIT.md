# Ecology Concepts & Synthesis fit audit

Checked against *Ecology* Author Guidelines current on 2026-08-21 (guidance revised April 2026) and the ESA Open Research Policy.

## Editorial fit

**PASS, with the manuscript framed as a balance → differentiation → identification synthesis.**

Transferable sequence:

```text
measure or characterize a shared-trait compromise
→ compare the best shared architecture with a differentiated architecture
→ quantify recoverable compromise loss R
→ account for residual coupling and extra architecture cost K
→ determine whether differentiation pays
→ once several axes exist, measure their total interaction
→ represent compatible ecological channel allocations as an identified set
→ add selective interventions and an independent remaining-channel assay
```

The floral attraction/defence notation is a detailed worked case. The broader contribution is the connection among **shared-axis balance**, **partial trait differentiation**, and **causal mechanism identification**.

## Rendered review-package audit

Current validated canonical state:

- Main Document: Word `.docx`, Letter portrait, 1-inch margins, 12-pt Times New Roman, double-spaced prose;
- title page / review numbering / native equations / five embedded Main figures — PASS structurally;
- one Appendix S1;
- current Main length before final author metadata: **30 pages**;
- current Appendix length: **38 pages**;
- Main status: **within the standard 30-page target exactly**.

Full-page visual QA of all **30 Main + 38 Appendix = 68 pages** found no blank pages, clipping, overlap, missing figure content, or broken equations. A LibreOffice OMML fallback for superscript `*` was found during QA and corrected by rendering optimized quantities with explicit `opt` superscripts; the corrected package retains the 30-page Main count.

## Current Author-Guideline audit

- Abstract ≤350 words — PASS
- Keywords 6–12 — PASS
- Journal/manuscript type on title page — PASS
- Open Research statement — PASS structurally
- Acknowledgments / Author Contributions / Funding / Conflict of Interest / References order — PASS structurally; author content pending
- five Main figures embedded — PASS
- native equations — PASS after renderer-specific `opt` normalization
- review line numbering — PASS structurally
- standard 30-page target — PASS at 30 pages
- ≤50-page absolute ceiling — PASS
- >30-page cover-letter justification — NOT REQUIRED
- Appendix architecture — PASS at 38 pages
- final author-list consistency — PENDING author input

## Architecture synthesis fit

The general nested-architecture result is

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0 <=> K < R
```

under the declared assumption that the differentiated architecture contains the shared phenotype before its additional fixed architecture cost is charged. With a non-negative scaled residual-coupling penalty, stronger coupling cannot increase `R`.

The quadratic corollary is

```text
R = s L_S*
Delta_arch = s L_S* - K
```

where `s` is the retained fraction of function-specific separation after residual coupling. The manuscript explicitly does not treat `R=sL_S*` as a shape-independent identity or claim that every trade-off evolves toward modularity.

The registered convex-family analysis gives strict positive pre-cost recovery in 300/300 nonzero-conflict evaluations and increasing recovery with optimum separation in 60/60 declared series. The 60/60 coupling result is an implementation check of the structural monotonicity proposition.

Cichlid oral/pharyngeal jaws and *Dalechampia* establish biological plausibility of incomplete differentiation and historical architecture reorganization without estimating BITA parameters or proving a historical causal transition.

## Mechanism-identification fit

Once multiple trait axes exist, the floral worked case retains the measurable interaction

```text
Delta_AD W = W11 - W10 - W01 + W00
```

and the allocation identity

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

A total interaction therefore defines a compatible set rather than a unique mechanism. Selective crossed interventions, baseline handling, the four-way separability diagnostic and an independent remaining-channel assay are required for stronger allocation.

The source-adjudicated route layer contains **56 route records / 25 independent biological clusters** and establishes recurrence only. The authoritative high-information audit contains **17 systems** occupying complementary design faces. The empirical synthesis is therefore a **fragmented identification frontier**, not a prevalence estimate and not a 0/17 claim about the biology.

## Identification invariants preserved

- total interaction alone defines a set, not unique channel allocation;
- partial bounds are conditional on declared restrictions;
- point-ID design is `A × D × antagonist × pollinator` with selective interventions;
- `m0_delta` is measured/corrected rather than assumed zero;
- `U_delta` is unallocated and not kappa by subtraction;
- the remaining joint channel requires independent evidence;
- marginal route recurrence is not channel identification or prevalence;
- positive A×D interaction is not evidence of historical trait splitting;
- historical 2,592 / 77.2% results remain technical Appendix/provenance material only.

## Open Research boundary

The canonical package preserves the historical mechanism/Pattern machine-readable products and adds the trait-differentiation robustness readout plus authoritative identification outputs. Permanent archival DOI remains an acceptance-stage requirement.

## Remaining submission blockers

Only author-controlled fields and final post-metadata QA: publication names/order/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, reviewer information if requested, all-author approval/no-simultaneous-submission confirmation, then exact rebuild and page-by-page inspection.

## Fallbacks

1. The American Naturalist — strongest alternative for a more evolution-theory presentation.
2. Evolution — stronger if direct transition/phylogenetic evidence is added.
3. The previously validated Theoretical Ecology identification-only package — provenance/alternative only if the integrated Chapter 2 is deliberately split back into a narrower mechanism paper.
