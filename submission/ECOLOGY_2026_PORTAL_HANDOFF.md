# Ecology 2026 portal handoff — BITA

This contract freezes the live submission-layer requirements for the active mechanism-identification paper. It does not change the scientific claim ceiling.

## Target

```text
JOURNAL = Ecology
SUBMISSION_TYPE = Concepts & Synthesis
CANONICAL_MAIN = manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
ACTIVE_REVIEW_ARTIFACT = bita-mechanism-identification-review-package
ACTIVE_MAIN_PAGES = 21 at last verified render
ACTIVE_APPENDIX_PAGES = 10 at last verified render
```

The current Main is within the 30-page Concepts & Synthesis target, so the special >30-page cover-letter length justification is not required.

## Live initial-submission requirements locked from the April 2026 author guidance

- continuous line numbering through the manuscript;
- manuscript title and author list must exactly match ScholarOne;
- Main Document title page must include journal name, manuscript type, title, authors/affiliations, corresponding author/email, Open Research statement, and keywords;
- title must be no more than 120 characters including spaces;
- Concepts & Synthesis abstract limit is 350 words;
- provide 6–12 keywords/phrases, alphabetized and separated by semicolons;
- Main Document should be Word unless the manuscript is prepared in LaTeX;
- appendices/supporting information are uploaded separately and do not count toward the 30-page Main limit;
- data/code governed by the Open Research policy should be archived externally rather than duplicated as Supporting Information.

The active title is 101 characters and therefore within the 120-character limit.

## Exact keyword order for the title page and portal

Use this alphabetized sequence:

```text
antagonism; causal identification; ecological mechanism; factorial experiment; floral defence; partial identification; pollination; trait interaction
```

Do not use the older unsorted sequence in portal metadata.

## Open Research statement

The title page must contain the author-approved Open Research statement before upload. The current review-stage wording is maintained in `submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md`; before submission it must be reconciled with the exact archived/public files and any source-data licence restrictions.

The final statement must distinguish:

- repository-hosted analysis/code and source-audit products that can be shared;
- source materials that cannot legally be redistributed;
- the exact version/tag/commit submitted for review;
- the permanent archive/DOI when created.

## AI disclosure gate

Ecology requires disclosure when AI tools are used in manuscript writing beyond ordinary spelling/grammar/general editing, image production, or data collection/analysis. The use must be disclosed:

1. in the manuscript section to which the use pertains;
2. additionally in the Acknowledgments;
3. in the manuscript submission form.

The repository already records AI-assisted coding, structured literature triage, reproducibility checking and drafting/editing. Before submission, authors must approve exact wording that accurately describes actual use; AI output is not treated as empirical evidence or as an autonomous inclusion/statistical decision.

## Human-controlled metadata

Complete `submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md` and the machine-readable author metadata template before the final rebuild:

- final author order/publication names;
- affiliations and present addresses;
- one corresponding author and email;
- ORCIDs;
- CRediT roles;
- funding/grants;
- acknowledgments;
- competing interests;
- final Open Research statement;
- exact AI disclosure;
- reviewer/editor fields only if requested by the live portal;
- all-author approval and no-simultaneous-submission confirmation.

## Cover letter state

`submission/COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md` is the active letter. Because the Main is 21 pages at the last verified render, do not include a >30-page length justification unless a later rebuild crosses the journal threshold.

## Final upload gate

```text
SCIENCE = FROZEN
MAIN_LENGTH = WITHIN_30_PAGE_TARGET
TITLE_120_CHAR_LIMIT = PASS
KEYWORD_COUNT = PASS_8
KEYWORD_ORDER = USE_ALPHABETIZED_PORTAL_SEQUENCE
OPEN_RESEARCH_STATEMENT = AUTHOR_APPROVAL_REQUIRED
AI_DISCLOSURE = AUTHOR_APPROVAL_REQUIRED
AUTHOR_METADATA = REQUIRED
ALL_AUTHOR_APPROVAL = REQUIRED
FINAL_POST_METADATA_REBUILD = REQUIRED
FINAL_PAGE_BY_PAGE_QA = REQUIRED
PORTAL_UPLOAD = REQUIRED
```
