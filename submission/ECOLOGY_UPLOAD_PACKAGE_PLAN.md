# Ecology Concepts & Synthesis upload package plan — BITA mechanism identification

Target: **Ecology — Concepts & Synthesis**

Official submission contract checked against the Ecology Author Guidelines revised **April 2026**.

Active paper:

> **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**

Authoritative science source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Authoritative reader-facing artifact and receipt:

```text
bita-mechanism-identification-review-package
PACKAGE_QA_RECEIPT.txt
```

The receipt is the source of truth after every rebuild. Historical 29+12, 30+12, 30+38 and 36+12 packages are provenance only.

## 1. Ecology April 2026 manuscript gates

For the active Concepts & Synthesis submission:

- standard Main Document target: **<=30 pages**;
- a 31–50 page Main requires the journal's two-part detailed length justification in the cover letter; the current workflow therefore fails closed above 30 unless that policy is deliberately changed;
- title: **<=120 characters**;
- Abstract: **<=350 words**;
- keywords: **6–12, alphabetical**, semicolon-separated in the generated Main;
- Main Document: Word `.doc/.docx` for this non-LaTeX submission;
- page: Letter portrait, 8.5 × 11 in, 1-inch margins;
- text/references/captions: 12-pt Times New Roman, double-spaced, left aligned;
- continuous line numbering is required for initial submission;
- title page includes journal/manuscript type, title, author/affiliation placeholders until approved, corresponding-author placeholder, Open Research Statement, and keywords;
- Appendix is a separate file; **PDF is preferred**;
- ordinary research data/code follow ESA Open Research policy and are not routed as ordinary Supporting Information data files.

Current automated contract status:

```text
TITLE_LIMIT_GATE = PASS
ABSTRACT_LIMIT_GATE = PASS
KEYWORD_COUNT_AND_ORDER_GATE = PASS
TITLE_PAGE_OPEN_RESEARCH_GATE = PASS
FORMATTER_LETTER_1IN_TNR12_DOUBLESPACE = PASS
CONTINUOUS_LINE_NUMBERING = PASS
MAIN_STANDARD_PAGE_GATE = <=30_FAIL_CLOSED
```

## 2. Main Document

Active package builder:

```text
scripts/build_bita_mechanism_candidate_sources.py
```

Generated source directory:

```text
submission/ecology/mechanism_identification_candidate/generated/
```

The builder keeps science source and journal formatting separate. It validates the title/Abstract limits, extracts the canonical keyword set, alphabetizes and validates it, moves the keyword line to the title page, inserts the review-stage Open Research Statement and corresponding-author placeholder, then places the Ecology section break before the Abstract.

The formatter is:

```text
scripts/format_ecology_submission_docx.py
```

It enforces Letter page geometry, 1-inch margins, 12-pt Times New Roman, double-spaced prose/references/captions, continuous review line numbering and centered page numbering.

## 3. Scientific sequence

```text
four-cell A×D interaction
-> outcome promotion
   Level 1 interaction relief
   Level 2 constraint release
   Level 3 strict reversal
-> identified set of compatible channel allocations
-> assumption-indexed partial identification
-> selective A×D×antagonist×pollinator intervention
-> m0 handling + four-way separability diagnostic
-> consumer-channel allocation
-> independent remaining-channel assay
-> mechanism-resolved interpretation
```

Core accounting identity:

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

## 4. Main figures

1. Outcome promotion.
2. Identified-set geometry.
3. Crossed intervention and separability.
4. Fragmented empirical frontier: 56 routes / 25 clusters / 17-system audit.
5. SCH -> SLK transport plus orthogonal BITA mechanism-identification track.

The active builder and workflow fail closed if the source-backed empirical state or active figure contract drifts.

## 5. Appendix / Supporting Information

Active scientific source:

```text
manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md
```

Review artifact output:

```text
APPENDIX_S1.docx
rendered/APPENDIX_S1.pdf
```

For portal upload, use the separately rendered **Appendix PDF** unless the live portal requests another permitted format. Do not attach ordinary research data/code as Supporting Information merely because the internal review artifact bundles derived QA files.

## 6. Open Research routing

Current title-page statement:

> Review-stage identification code, source-adjudicated evidence products, derived analysis receipts, and the reader-facing mechanism-identification package are maintained in the public project repository. The accepted exact data/code release will be archived permanently and cited in the final article.

The internal review artifact bundles selected derived products so the package is auditable. Journal-facing Open Research routing is different: code/data remain in the public/archived repository route, subject to licence restrictions, and the final statement is copied to the submission form.

Acceptance-stage tasks include freezing the exact accepted release and adding its permanent archive DOI.

## 7. Automated review-package gate

Workflow:

```text
.github/workflows/build-bita-mechanism-review-package.yml
```

It runs focused scientific/formatting checks, rebuilds the 56/25 receipt and figures, builds Main and Appendix, validates DOCX structure/media, renders PDFs, measures fresh page counts, checks active title/56/25/17 tokens and stale-title exclusions, fails above the 30-page standard target, renders all pages to PNG, and uploads the review artifact plus QA receipt.

Latest independently reproduced pre-metadata state:

```text
MAIN_PDF = 21 pages
APPENDIX_PDF = 10 pages
MAIN_FIGURES = 5 embedded
LENGTH_STATE = WITHIN_30_PAGE_TARGET
ACTIVE_SUBMISSION = true
```

After the title-page compliance patch, the PR-gated workflow must regenerate this package. Any new page count in `PACKAGE_QA_RECEIPT.txt` supersedes the copied numbers above.

## 8. AI-use disclosure gate — author controlled

ESA's April 2026 guidance requires transparent disclosure when AI use goes beyond routine spelling/grammar/general editing. Before external upload, the authors must approve the exact disclosure and synchronize it across all required surfaces:

- relevant manuscript section describing how/which AI tool was used, when applicable;
- an additional disclosure in **Acknowledgments**;
- the **submission form**.

Repository provenance is not a substitute for the final journal disclosure. This remains an explicit pre-upload blocker.

## 9. Human-controlled fields before upload

- final author list/order/names and affiliations;
- corresponding author/e-mail;
- ORCIDs;
- CRediT;
- funding/no-funding statement;
- acknowledgments;
- competing interests;
- final repository/software/data licence wording;
- AI disclosure wording/placement where required;
- portal-only reviewer fields if requested;
- all-author approval and no-simultaneous-consideration confirmation;
- final exact post-metadata rebuild and page-by-page QA.
