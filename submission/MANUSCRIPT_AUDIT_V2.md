# Manuscript audit — active mechanism-identification state

> **STATUS — PRESERVED LEGACY MECHANISM-IDENTIFICATION PACKAGE; NOT THE CURRENT BITA SUBMISSION ROUTE.**
>
> This file records the pre-2026-09-20 Ecology / mechanism-identification package. The current canonical forward paper is `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`, routed first through the Ecology Letters Synthesis proposal. Any words such as “active” or “canonical” below describe the historical package state and must not override `README.md`, `docs/PUBLICATION_STATUS.md`, or `docs/SUBMISSION_SCOPE.md`.

## Verdict

**Scientific conclusion: GO. Canonical manuscript: mechanism-identification Concepts & Synthesis paper. External submission: pending author-controlled metadata/sign-off only.**

Canonical title:

> **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**

Canonical inference sequence:

```text
interaction detection
-> identified set
-> partial identification
-> selective crossed intervention
-> consumer-channel allocation
-> separability diagnostic
-> independent remaining-channel assay
-> mechanism-resolved interpretation
```

## 1. Identification core — PASS

```text
Delta_AD W = W11 - W10 - W01 + W00
Delta_AD W = rho_delta - iota_delta - kappa_delta
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

The total interaction does not uniquely identify its channel allocation. The active paper distinguishes structural non-identification from **partial identification** and from stronger outcome claims.

```text
Level 1  Delta_AD W > 0     positive interaction relief
Level 2  A0 <= 0 < A1       functional constraint release
Level 3  A0 < 0 < A1        strict reversal
```

A positive Level-1 interaction is not by itself Level 2, Level 3, or mechanism identification.

Under an explicit biological restriction such as

```text
kappa_delta >= 0
```

one obtains an assumption-indexed lower bound on `rho_delta - iota_delta`. This is a partial-identification statement, not a universal theorem.

Point identification of the consumer-mediated channels uses a selective `A x D x antagonist x pollinator` 16-cell experiment. Consumer selectivity, comparable trait contrasts, pollinator-absent baseline handling, the four-way separability diagnostic, and independent evidence for the remaining joint channel are explicit requirements. `U_delta` remains unallocated and is not `kappa_delta` by definition.

## 2. Mechanism -> Pattern bridge — PASS

Retained recurrence synthesis:

```text
56 directional route records
25 independent biological clusters
A -> pollination: 5
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system:      14
context switches: 17
```

These counts establish recurrence capacity only; they are not prevalence estimates.

The authoritative high-information audit retains **17 systems**. Kessler 2008, Egan 2021, *Impatiens capensis*, *Pedicularis rex* and the remaining audited systems occupy complementary design faces. No retained system closes the entire sequence from trait interaction through selective consumer allocation to an independent remaining-channel assay. The strongest cross-system conclusion is therefore:

```text
RECURRENT_CONSTITUENT_BIOLOGY
+
FRAGMENTED_IDENTIFICATION
```

## 3. Existing-data anchors — PASS with boundaries

- **Kessler 2008:** closest trait-factorial anchor; aggregate positive discrete interaction; formal uncertainty/systemic-nicotine caveats retained.
- **Egan 2021:** complementary consumer-factorial anchor; no independently manipulated floral A-by-D pair.
- **Impatiens:** observational A-by-D plus randomized context modification; all eight target HC3 intervals cross zero.
- **Pedicularis rex:** selective-access defence anchor without independent attraction manipulation.

No study-specific `rho/iota/kappa` point allocation is invented.

## 4. Programme ownership — PASS

The active Main explicitly separates adjacent programmes:

```text
SCH  identifies whether multifunctionality has become an identified conflict / L
SLK  transports identified conflict through value -> accessibility -> invasion -> fixation -> occupancy
BITA starts from an observed multi-trait fitness interaction and asks which ecological mechanism generated it
```

The old visual implication `SLK -> BITA` is not part of the active Figure 5.

## 5. Novelty boundary — PASS

The paper does not claim novelty for pollinator-antagonist conflict, floral attraction costs, defence effects, factorial experiments, context dependence, or partial identification as a general statistical concept.

Paper-specific novelty is the integrated ecological identification architecture:

1. measurable discrete trait interaction;
2. explicit identified set for unresolved allocation;
3. assumption-indexed partial-identification bounds;
4. intervention-defined consumer-channel estimands;
5. internal four-way separability diagnostic;
6. explicit non-zero pollinator-absent baseline handling;
7. independent remaining-channel evidence rather than residual naming;
8. source-adjudicated recurrence plus a 17-system fragmented identification frontier.

## 6. Active reader-facing package — PASS before human metadata

Source of truth:

```text
artifact: bita-mechanism-identification-review-package
receipt:  PACKAGE_QA_RECEIPT.txt
```

Latest independently reproduced render:

```text
Main Document: 21 pages
Appendix S1:   10 pages
Main figures:   5 embedded
Length state:   WITHIN_30_PAGE_TARGET
```

The PR-gated active workflow rebuilds source-backed evidence, the five figures, Main/Appendix DOCX files, both PDFs, all page PNGs, and the receipt. The PDF guards verify the active title, 56/25/17 empirical frontier, Figure-5 programme boundary, absence of the superseded architecture title, and the <=30-page Main target.

The older `legacy-identification-candidate-package` is provenance/regression only and records `active_submission=false`.

## 7. Inference-boundary audit — PASS

```text
marginal route recurrence
!= total A x D interaction
!= assumption-indexed partial identification
!= point-identified consumer-channel interaction
!= full mechanism allocation
```

Further boundaries: route counts are not prevalence; randomized context modification is not selective exclusion; absence of a joint-cost assay is not `kappa=0`; `U_delta` is not `kappa`; non-zero four-way coupling rejects the proposed separability allocation.

## 8. Historical/provenance analyses — RETAINED, NOT ACTIVE

The former integrated architecture paper, `R-K` / `sL-K` derivations, registered 300-condition robustness exercise, earlier 16-system state, and older 29+12 / 30+12 / 30+38 reader-facing renders remain reproducible provenance only. They are not the active title, claim spine, audit count, or submission package.

## 9. External-submission blockers

Only human-controlled fields remain: final authors/order/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, reviewer fields only if requested, all-author approval/no-simultaneous-submission confirmation, then final exact post-metadata rebuild and page-by-page QA.

## Final decision

**The active BITA paper is scientifically coherent as a mechanism-identification Concepts & Synthesis manuscript whose strongest inference sequence is `interaction detection -> partial identification -> mechanism allocation`. Additional broad evidence hunting is not a default blocker.**
