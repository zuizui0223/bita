# Ecology 2026 portal handoff — BITA

This contract summarizes the live submission layer for the active mechanism-identification paper. Detailed April 2026 compliance logic already lives in the title-page builder, author metadata template, upload plan, fit audit, tests and package workflow; this file is a compact human handoff, not a competing source of truth.

## Target

```text
JOURNAL = Ecology
SUBMISSION_TYPE = Concepts & Synthesis
CANONICAL_MAIN = manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
ACTIVE_REVIEW_ARTIFACT = bita-mechanism-identification-review-package
ACTIVE_MAIN_PAGES = 21 at last verified render
ACTIVE_APPENDIX_PAGES = 10 at last verified render
```

The Main is within the 30-page Concepts & Synthesis target, so no >30-page cover-letter justification is currently needed.

## Portal-facing checks already automated on main

- title <=120 characters;
- Concepts & Synthesis abstract <=350 words;
- eight keywords within the 6–12 limit and alphabetized;
- continuous line numbering;
- generated title page routes journal, article type, title, author placeholders, corresponding-author placeholder, Open Research statement and keywords;
- active package remains the 21-page mechanism-identification Main with five figures rather than the historical 30+38 architecture package;
- Open Research and AI-disclosure gates are represented in the author/portal metadata workflow.

## Human-controlled fields still required

Before the final rebuild/upload, approve and synchronize:

- final author order/publication names;
- affiliations and present addresses;
- corresponding author and active email;
- ORCIDs;
- CRediT roles;
- funding/grants and acknowledgments;
- competing interests;
- final Open Research statement and repository/software/data licence wording;
- exact AI disclosure across the relevant manuscript section, Acknowledgments and submission form when applicable;
- reviewer/editor fields if requested by ScholarOne;
- all-author approval and no-simultaneous-submission confirmation.

## Cover letter

`submission/COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md` is the active cover letter. It must describe the current 21-page/10-page mechanism-identification package, not the obsolete statement that the package still needs rebuilding.

## Final gate

```text
SCIENCE = FROZEN
CURRENT_ECOLOGY_COMPLIANCE = IMPLEMENTED_AND_TESTED_ON_MAIN
MAIN_LENGTH = WITHIN_30_PAGE_TARGET
AUTHOR_METADATA = REQUIRED
OPEN_RESEARCH_FINAL_WORDING = AUTHOR_APPROVAL_REQUIRED
AI_DISCLOSURE_FINAL_WORDING = AUTHOR_APPROVAL_REQUIRED
ALL_AUTHOR_APPROVAL = REQUIRED
FINAL_POST_METADATA_REBUILD_AND_VISUAL_QA = REQUIRED
PORTAL_UPLOAD = REQUIRED
```
