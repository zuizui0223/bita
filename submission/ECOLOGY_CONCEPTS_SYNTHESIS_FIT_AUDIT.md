# Ecology Concepts & Synthesis fit audit

Checked against *Ecology* Author Guidelines current on 2026-08-21 (guidance revised April 2026) and the ESA Open Research Policy.

## Editorial fit

**PASS, with the manuscript framed as a conceptual synthesis rather than a universal floral sign rule.**

The manuscript's transferable contribution is the mechanism-first inference sequence:

```text
declare focal interaction
-> decompose causal channels
-> derive a one-sided exclusion
-> use theory-defined classes to organize heterogeneous evidence
-> identify the minimal falsification gate
-> calibrate only when needed
```

The floral theorem remains biologically bounded. The generalization is the inference workflow, not the claim that the same route signs apply outside flowers.

## Rendered review-package audit

The automated Ecology packaging workflow builds and renders actual review files rather than stopping at Markdown/source checks.

Current generated package state:

- Main Document: Word `.docx`, Letter portrait, 1-inch margins, 12-pt Times New Roman, double-spaced prose;
- title page: Ecology / Concepts & Synthesis / title / author-controlled fields / review-stage Open Research statement / six alphabetized key words;
- line-number target: Abstract through end of References only, with explicit suppression on title-page and post-References paragraphs for renderer parity;
- page numbers: present;
- Main tables: four compact journal-facing Word tables; exhaustive machine-readable records displaced to Open Research files;
- Main figures: Figures 1–5 embedded, one figure page each;
- Figures 4–5 are integrative visualizations of already frozen theory and empirical results, not additional analyses;
- Supporting Information: one `Appendix S1.pdf` containing Figures S1–S4 plus its own References section;
- spreadsheet-format supplementary records: separated into six descriptively named Open Research CSV products, not uploaded as Supporting Information;
- current measured Main Document length before final author metadata: **48 pages**, within the 31–50-page allowed range and therefore accompanied by the required two-part cover-letter justification;
- current Appendix S1 length: six pages.

The exact page count is remeasured by CI on every package build and must be rechecked after author-controlled metadata are inserted. The workflow fails if the Main Document exceeds 50 pages.

## Current Author-Guideline requirement audit

- Abstract ≤350 words — PASS
- Keywords 6–12 and alphabetical — PASS (6)
- Journal and manuscript type on title page — PASS in generated review source
- Open Research statement on title page — PASS in generated review source
- Acknowledgments / Author Contributions / Conflict of Interest / References order — PASS in generated review source
- Tables in Main Document, each beginning on a new page — PASS
- Figure captions grouped and five main figures placed after captions — PASS
- Word equations retained as native document math — PASS
- Continuous line-number OOXML present for the manuscript-through-References section — PASS structurally; rendered visual check required on the exact final human-metadata version
- Concepts & Synthesis ≤50-page absolute ceiling — PASS at 48 pages on current generated review package
- Required two-part justification for 31–50 pages — PASS in cover letter
- Appendix S1 naming/callout architecture — PASS
- Spreadsheet/large-table Open Research separation — PASS
- AI disclosure in relevant Methods section and Acknowledgments — PASS
- title/author-list consistency — author-controlled fields PENDING

## Open Research boundary

The review-stage public GitHub repository supplies access to novel code and versioned data products. A permanent archival DOI for the exact accepted data/code version is an **acceptance-stage publication requirement**, not an initial-submission blocker for this Concepts & Synthesis review package. The accepted version should be frozen in a permanent versioned repository and cited in the final paper.

## Reviewer-field boundary

The current published Author Guidelines do not support treating “exactly five suggested reviewers” as a fixed manuscript-level requirement. The author team should complete the number and fields requested by the live ScholarOne portal if reviewer suggestions are requested.

## Scientific invariants preserved

No change to the theorem, proof, 2,592 evaluations, 77.2% window precision, 56/25 Pattern architecture, Leal pooled results, Sasidharan boundaries, direct A×D state, joint-cost evidence state, or falsification/calibration distinction. Figures 4–5 only reorganize these frozen results visually.

## Literature-positioning state

PASS. Close prior work on attraction/defence conflict, defence-reproduction coupling, multi-agent selection, factorial ecological-agent manipulations, and ecological context dependence is explicit in the Introduction and Discussion. The manuscript does not claim those topics are new. It explicitly communicates that the theorem's algebra is elementary and positions the conceptual advance as a mechanism-defined exclusion plus an ordered falsification/calibration programme.

## Remaining submission blockers

These are human/review-version fields rather than scientific gaps:

- final publication author names/order and affiliations;
- corresponding author/email and ORCIDs;
- final CRediT, funding, acknowledgments, and competing-interest statements;
- any licence statement needed for deposited data/code;
- reviewer information if requested by ScholarOne;
- all-author approval and no-simultaneous-submission confirmation;
- final package rebuild, ≤50-page confirmation, and page-by-page visual QA after those fields are inserted.

## Fallbacks

1. Oikos Forum — excellent conceptual fit but requires its own presubmission format.
2. Theoretical Ecology Regular Article — conservative scope-fit fallback.