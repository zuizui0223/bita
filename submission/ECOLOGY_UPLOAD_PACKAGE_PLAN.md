# Ecology Concepts & Synthesis upload package plan

Target: **Ecology — Concepts & Synthesis**

Guidance basis: Ecology Author Guidelines revised April 2026 and ESA Open Research Policy current on 2026-08-21.

## 1. Main Document

The generated Main Document must use the journal component order:

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

Formatting target:

- Word `.docx` Main Document;
- Letter 8.5 × 11 in, portrait;
- 1-inch margins;
- 12-pt Times New Roman;
- double-spaced manuscript prose, references, captions, and table captions/notes;
- table bodies may use 10-pt Times New Roman and single spacing;
- left-aligned text;
- page numbers from the title page onward;
- continuous line numbering beginning after the title page and continuing through the end of References.

Concepts & Synthesis length target:

- standard maximum: 30 manuscript pages, including title page, body, References, tables, figure captions, and figures;
- if 31–50 pages, the cover letter must contain two numbered length-justification sections: broad ecological contribution and why the additional material cannot be moved adequately to Supporting Information;
- >50 pages is outside the stated allowable range.

## 2. Supporting Information

Use a single reader-facing file whenever possible:

- `Appendix S1.pdf`
- uploaded as **Supporting Information for review and publication**
- no appendix line numbering
- header material must include authors, manuscript title, and journal name
- items inside use `Figure S#`, `Table S#`, `Section S#`, etc.
- manuscript callouts use the full form such as `Appendix S1: Figure S2`
- Appendix references are repeated in a complete Appendix References section even when also cited in the Main Document.

For this paper, Appendix S1 contains the four reader-facing robustness/architecture figures (Figures S1–S4). Large machine-readable tables are not packaged as Appendix spreadsheets.

## 3. Open Research package

ESA does not allow spreadsheets (`.csv`, `.xlsx`, etc.) or large tables to be submitted as Supporting Information for a Concepts & Synthesis paper. They belong in an external Open Research repository.

The generated Open Research package therefore renames the canonical table CSVs descriptively for eventual archival deposition:

- `model_parameters_and_scaling.csv`
- `finite_grid_local_cases.csv`
- `mechanism_pattern_route_ledger.csv`
- `conditionality_context_records.csv`
- `direct_identification_audits.csv`
- `pattern_expansion_screening.csv`

During peer review, novel code must be accessible in an external repository; the existing public GitHub repository satisfies the review-access route. Permanent public archival deposition of the exact accepted data/code version is an acceptance-stage requirement, not a reason to delay initial submission of this manuscript type. The final accepted version should be frozen in a permanent versioned archive and cited in the paper.

## 4. Human-controlled fields still required

The package builder intentionally does not infer:

- final author list/order/publication names;
- affiliations and present addresses;
- corresponding author and email;
- ORCIDs;
- final CRediT statement;
- funding statement;
- acknowledgments beyond the existing AI disclosure and placeholders;
- final conflict-of-interest statement;
- portal-only reviewer fields if requested by ScholarOne;
- final immutable archive DOI after acceptance-stage freeze.

## 5. Automated package builder

Run:

```bash
python scripts/build_ecology_submission_sources.py
```

The GitHub workflow `.github/workflows/build-ecology-submission-package.yml` then:

1. builds an Ecology-ordered Main Document source;
2. converts it to Word with native Pandoc equations;
3. applies Letter size, margins, Times New Roman, spacing, page numbers, and the requested line-number scope;
4. builds a single Appendix S1 PDF;
5. separates machine-readable CSV data from Supporting Information;
6. renders the Main Document to PDF for page-count QA;
7. fails if the Main Document exceeds 50 pages and records whether a 31–50 page length justification is needed;
8. uploads the review package as a workflow artifact.

The canonical scientific manuscript remains the source of truth. This packaging layer changes journal formatting and file placement only; it does not change the frozen theorem, numerical results, Pattern counts, meta-analytic estimates, or inference boundaries.
