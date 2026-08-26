# Ecology Concepts & Synthesis fit audit

Checked against *Ecology* Author Guidelines current on 2026-08-21 (guidance revised April 2026) and the ESA Open Research Policy.

## Editorial fit

**PASS, with the manuscript framed as an experimental identification synthesis rather than a universal floral sign rule.**

The transferable contribution is the identification sequence:

```text
measure a focal trait interaction
→ establish what channel allocation is not identified from that interaction
→ add selective antagonist and pollinator interventions
→ measure the pollinator-absent A×D baseline
→ test A×D×G×P separability
→ assay the remaining joint-cost channel independently
→ use the algebra only as a consistency/sign diagnostic
```

The floral notation is the case study. The intended generalization is the distinction between interaction detection and mechanism allocation, together with an operational route for closing that gap.

## Rendered review-package audit

The automated Ecology packaging workflow builds and renders actual review files rather than stopping at Markdown/source checks.

Current validated package state:

- Main Document: Word `.docx`, Letter portrait, 1-inch margins, 12-pt Times New Roman, double-spaced prose;
- title page: Ecology / Concepts & Synthesis / identification-design title / author-controlled fields / review-stage Open Research statement / alphabetized key words;
- line-number target: Abstract through end of References only, with explicit suppression outside that region for renderer parity;
- page numbers: present;
- Main figures: Figures 1–5 embedded as the identification-design figure set;
- Supporting Information: one `Appendix S1.pdf` containing technical sensitivity and identification-audit material;
- spreadsheet/large machine-readable products: separated into the Open Research package;
- current measured Main Document length before final author metadata: **27 pages**, within the standard 30-page Concepts & Synthesis target;
- current Appendix S1 length: **11 pages**.

The exact page count is remeasured by CI on every package build and must be rechecked after author-controlled metadata are inserted. The workflow fails if the Main Document exceeds 50 pages.

## Current Author-Guideline requirement audit

- Abstract ≤350 words — PASS
- Keywords 6–12 and alphabetical — PASS after canonical keyword synchronization
- Journal and manuscript type on title page — PASS in generated review source
- Open Research statement on title page — PASS in generated review source
- Acknowledgments / Author Contributions / Funding / Conflict of Interest / References order — PASS in generated review source
- Five main figures embedded — PASS
- Word equations retained as native document math — PASS
- Continuous line-number OOXML present for the manuscript-through-References section — PASS structurally; rendered visual check required on the exact final human-metadata version
- Concepts & Synthesis standard 30-page target — PASS at 27 pages on the current generated review package
- Concepts & Synthesis ≤50-page absolute ceiling — PASS
- >30-page two-part cover-letter justification — NOT REQUIRED at the present 27-page state
- Appendix S1 naming/callout architecture — PASS
- spreadsheet/large-table Open Research separation — PASS
- AI-assisted workflow disclosure — required in the manuscript/portal and retained in the canonical identification version
- title/author-list consistency — author-controlled fields PENDING

## Open Research boundary

The review-stage public GitHub repository supplies access to novel code, identification estimands, audit products, the aggregate *Impatiens* retrofit, and the screened identification-coverage matrix. A permanent archival DOI for the exact accepted data/code version is an **acceptance-stage publication requirement**, not an initial-submission blocker. The accepted version should be frozen in a permanent versioned repository and cited in the final paper.

## Reviewer-field boundary

The current published Author Guidelines do not support treating an arbitrary fixed number of suggested reviewers as a manuscript-level requirement. Complete the number and fields requested by the live ScholarOne portal if reviewer suggestions are requested.

## Identification invariants preserved

The canonical switch does not change the scientific identification claims already tested in the candidate manuscript:

- `Delta_AD W` is a discrete two-level trait interaction on declared coordinates;
- total `Delta_AD W` alone does not identify channel allocation;
- the proposed general design is `A × D × antagonist × pollinator` with selective interventions;
- the rho- and iota-invariance views are the same four-way contrast up to sign;
- pollinator-independent reproduction is measured/corrected rather than assumed zero;
- `U_delta` remains unallocated and is not called kappa by subtraction;
- kappa requires an independent A×D cost assay;
- Kessler 2008 and Egan 2021 occupy complementary trait-factorial and consumer-factorial design halves;
- the *Impatiens* retrofit reaches randomized context modification but not channel identification;
- no system in the 16-system high-information screen reaches full channel identification or an independent joint-cost assay;
- 2,592 and 77.2% remain technical Supplement material, not Main evidence.

Historical Leal, Sasidharan, and Mechanism → Pattern analyses remain versioned for provenance but do not define the Main identification argument.

## Remaining submission blockers

These are human/review-version fields rather than scientific gaps:

- final publication author names/order and affiliations;
- corresponding author/email and ORCIDs;
- final CRediT, funding, acknowledgments, and competing-interest statements;
- repository/software/data licence statement where applicable;
- reviewer information if requested by ScholarOne;
- all-author approval and no-simultaneous-submission confirmation;
- final package rebuild and page-by-page visual QA after those fields are inserted.

## Fallbacks

1. Oikos Forum — strong conceptual fit but requires its own presubmission format.
2. Theoretical Ecology Regular Article — conservative scope-fit fallback.
