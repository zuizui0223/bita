# Ecology Concepts & Synthesis upload package plan

Target: **Ecology — Concepts & Synthesis**

Guidance basis: Ecology Author Guidelines revised April 2026 and ESA Open Research Policy current on 2026-08-21.

## 1. Main Document

The generated Main Document uses the journal component order:

1. title page
   - journal name: Ecology
   - manuscript type: Concepts & Synthesis
   - manuscript title
   - publication author list and affiliations
   - corresponding author and email
   - Open Research statement
   - 6–12 alphabetized key words/phrases
2. Abstract on a new page
3. manuscript text
4. Acknowledgments
5. Author Contributions
6. Conflict of Interest Statement
7. References
8. Tables, each beginning on a new page
9. Figure captions, grouped together on a new page
10. Figures, one figure per page

Formatting target and current automated state:

- Word `.docx` Main Document;
- Letter 8.5 × 11 in, portrait;
- 1-inch margins;
- 12-pt Times New Roman;
- double-spaced manuscript prose, references, captions, and table captions/notes;
- 10-pt single-spaced table bodies;
- left-aligned text;
- page numbers from the title page onward;
- continuous line numbering beginning after the title page and continuing through the end of References, with explicit suppression outside that region for renderer parity;
- native Word/Pandoc equations rather than equation images;
- four compact journal-facing Main tables and three embedded main figures.

Concepts & Synthesis length rule:

- standard target: 30 manuscript pages;
- 31–50 pages: allowed only with the required two-part cover-letter justification;
- >50 pages: outside the stated allowable range.

**Measured review-package state (2026-08-21): 46 Main Document pages with all three figures rendered.** Table 1 now begins immediately after the post-References section break, so there is no duplicate blank page. The required two-part length justification is present in `submission/COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md`. The final page count must be rechecked after author-controlled title-page/backmatter fields are inserted.

## 2. Main-table compression

The canonical scientific tables remain in `manuscript/TABLES_THEORETICAL_ECOLOGY.md`. The Ecology review package uses `submission/ecology/ECOLOGY_MAIN_TABLES_COMPACT.md` as a journal-facing view:

- Table 1: mechanistic definitions and inference boundaries;
- Table 2: core theoretical verification results;
- Table 3: route recurrence and identification state;
- Table 4: quantitative/direct-factorial evidence and limitations.

No frozen value is changed. Exhaustive parameter rows, local cases, route ledgers, context records, direct audits, and stopping batches are supplied as machine-readable Open Research products instead of consuming Main Document pages.

## 3. Supporting Information

Use a single reader-facing file:

- `Appendix S1.pdf`
- uploaded as **Supporting Information for review and publication**
- no Appendix line numbering
- opening material includes authors, manuscript title, and journal name
- items use `Figure S#` / `Section S#`
- Main Document callouts use full forms such as `Appendix S1: Figure S2`
- Appendix references are repeated in the Appendix References section even when also cited in the Main Document.

For this paper, Appendix S1 contains the four reader-facing robustness/architecture figures (Figures S1–S4). Large machine-readable tables are not packaged as Appendix spreadsheets.

**Measured review-package state: Appendix S1 = 6 pages.**

## 4. Open Research package

ESA does not allow spreadsheets (`.csv`, `.xlsx`, etc.) or large machine-readable tables to be submitted as Supporting Information for this paper type. They belong in an external Open Research repository.

The generated deposition package renames the canonical supplementary-table CSVs descriptively:

- `model_parameters_and_scaling.csv`
- `finite_grid_local_cases.csv`
- `mechanism_pattern_route_ledger.csv`
- `conditionality_context_records.csv`
- `direct_identification_audits.csv`
- `pattern_expansion_screening.csv`

During peer review, novel code must be accessible in an external repository; the public GitHub repository supplies that review-stage access. Permanent archival deposition of the accepted exact data/code version is an acceptance-stage requirement rather than an initial-submission blocker. The accepted release should be frozen in a permanent versioned archive and cited in the final paper.

## 5. Human-controlled fields still required

The package builder intentionally does not infer:

- final author list/order/publication names;
- affiliations and present addresses;
- corresponding author and email;
- ORCIDs;
- final CRediT statement;
- funding statement;
- final acknowledgments beyond the existing AI disclosure/placeholders;
- final conflict-of-interest statement;
- portal-only reviewer fields if requested by ScholarOne;
- permanent archival DOI at the acceptance-stage freeze.

## 6. Automated package builder

Generate the actual review-package source with compact Main tables using:

```bash
python scripts/build_ecology_review_package_sources.py
```

`build_ecology_review_package_sources.py` delegates to the canonical parser while selecting the compact Ecology Main-table view and shortening the review-stage Open Research title-page statement. The underlying canonical builder remains `scripts/build_ecology_submission_sources.py`.

The workflow `.github/workflows/build-ecology-submission-package.yml`:

1. builds an Ecology-ordered Main Document source;
2. converts it to Word with native Pandoc equations;
3. applies Letter size, margins, Times New Roman, spacing, page numbers, and the requested line-number scope;
4. verifies the DOCX contains line-number OOXML, four Word tables, and embedded media;
5. builds a single Appendix S1 PDF;
6. separates machine-readable CSV data from Supporting Information;
7. renders Main and Appendix to PDF and records exact page counts;
8. fails above 50 Main Document pages and records whether the 31–50-page length justification is required;
9. uploads the review package as a workflow artifact.

The canonical scientific manuscript remains the source of truth. This packaging layer changes journal formatting, compact presentation, and file placement only; it does not change the frozen theorem, numerical results, Pattern counts, meta-analytic estimates, or inference boundaries.
