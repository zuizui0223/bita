# Supplement manifest — active BITA mechanism-identification paper

> **STATUS — PRESERVED LEGACY MECHANISM-IDENTIFICATION PACKAGE; NOT THE CURRENT BITA SUBMISSION ROUTE.**
>
> This file records the pre-2026-09-20 Ecology / mechanism-identification package. The current canonical forward paper is `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`, routed first through the Ecology Letters Synthesis proposal. Any words such as “active” or “canonical” below describe the historical package state and must not override `README.md`, `docs/PUBLICATION_STATUS.md`, or `docs/SUBMISSION_SCOPE.md`.

## 1. Active submission identity

Canonical title:

> **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**

Target class: **Ecology — Concepts & Synthesis / conceptual-methodological ecology**.

Canonical science source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Authoritative reader-facing artifact:

```text
bita-mechanism-identification-review-package
```

Authoritative render receipt:

```text
PACKAGE_QA_RECEIPT.txt
```

The receipt, not a hard-coded historical page count, is the source of truth for the current Main/Appendix page counts, source commit and embedded-figure count.

## 2. Scientific core

The active inference sequence is:

```text
measured trait interaction
        ↓
identified set of compatible mechanisms
        ↓
partial identification
        ↓
selective crossed consumer intervention
        ↓
four-way separability diagnostic
        ↓
independent remaining-channel assay
        ↓
mechanism-resolved interpretation
```

For a two-level attraction-by-defence surface,

```text
Delta_AD W = W11 - W10 - W01 + W00
A0 = W10 - W00
A1 = W11 - W01
```

and the paper distinguishes:

```text
Level 1  Delta_AD W > 0     positive interaction relief
Level 2  A0 <= 0 < A1       functional constraint release
Level 3  A0 < 0 < A1        strict reversal
```

The mechanism accounting identity is

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

so a measured total interaction identifies a set of compatible channel allocations rather than a unique mechanism. The remaining channel is not labelled biological cost by subtraction alone.

## 3. Empirical synthesis

The active source-adjudicated evidence layer contains:

```text
56 directional route records
25 independent biological clusters
17 high-information systems
```

All four constituent marginal pathways recur, but no retained system closes the full allocation design plus an independent remaining-channel assay. The empirical conclusion is therefore:

```text
RECURRENT_CONSTITUENT_BIOLOGY
+
FRAGMENTED_IDENTIFICATION
```

The route counts are recurrence evidence, not prevalence estimates.

## 4. Main figures

The active five-figure sequence is:

1. outcome hierarchy: interaction relief versus release/reversal;
2. identified-set geometry and partial identification;
3. selective crossed intervention, baseline handling and separability;
4. recurrent pathways plus the fragmented empirical frontier;
5. SCH -> SLK conflict transport, orthogonal BITA mechanism identification, and the BITA promotion ladder.

Figure 5 must not imply `SLK -> BITA`. SLK owns evolutionary transport of an identified conflict budget; BITA owns mechanism allocation for an observed multi-trait interaction.

## 5. Appendix S1

The active Appendix retains the technical material needed to audit the mechanism-identification claims, including:

- identified-set and partial-identification algebra;
- crossed-intervention estimands and separability logic;
- pollinator-absent baseline handling;
- independent remaining-channel requirement;
- Kessler aggregate reconstruction;
- public-data retrofit materials;
- 56/25 recurrence provenance;
- the 17-system high-information frontier;
- historical sensitivity products only where explicitly labelled as provenance.

## 6. Open Research package

The review artifact bundles the current Open Research manifest and permitted derived products. The public repository retains code, source-audit receipts, route ledgers and reproducible aggregate analyses. The exact accepted version should be frozen in a permanent archive at acceptance stage.

## 7. Current validated render

Latest independently reproduced active render:

```text
Main Document: 21 pages
Appendix S1:   10 pages
Main figures:   5 embedded
Length state:   WITHIN_30_PAGE_TARGET
```

These values were reproduced by the PR-gated `Build BITA mechanism review package` workflow. For any later scientific or formatting change, use the newly generated `bita-mechanism-identification-review-package/PACKAGE_QA_RECEIPT.txt` rather than copying these numbers forward.

## 8. Historical/provenance packages

The former integrated architecture paper,

> **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**

and its `R-K`, quadratic `sL-K`, finite-family robustness and architecture-state synthesis remain in the repository as provenance/companion-programme material. The earlier 30-page Main + 38-page Appendix render is not the active BITA submission package.

Likewise, `legacy-identification-candidate-package` is retained only as a regression/provenance artifact and explicitly records `active_submission=false`.

## 9. External-submission boundary

Remaining upload-stage fields are author-controlled: final author list/order, affiliations, corresponding-author contact, ORCIDs, CRediT roles, funding, acknowledgments, competing interests, licence statements, any portal-requested reviewer fields, all-author approval and no-simultaneous-submission confirmation.

After any author-metadata insertion, rebuild the active package and verify the exact new `PACKAGE_QA_RECEIPT.txt` before upload.
