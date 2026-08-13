# Theoretical Ecology / Springer upload package plan

## Purpose

This file maps the saturated 25-system Mechanism → Pattern candidate to the current journal upload roles. It is a packaging plan, not a replacement for the journal portal and not a final author-approval record.

## Current scientific package

```text
Part I — Mechanism: fixed theory, Figures 1–2, Tables 1–2
Part II — Pattern:   56 route records / 25 systems, Figure 3, Tables 3–4
same-system:         14 clusters
context/sign switch: 17 clusters
context-only:         7 programs, excluded from route N
direct A x D:         1 strict sign-unresolved cluster
direct joint cost:    0 strict estimates; kappa unidentified
```

The empirical expansion is saturated under the registered stopping rule. Additional broad literature searching is not a packaging requirement.

## 1. Main manuscript upload

### Author/title-page fields that must be resolved first

Do not render the final manuscript until the authors have supplied/approved:

- final publication names and author order;
- affiliations;
- corresponding author and active e-mail;
- ORCID identifiers where available;
- funding statement or explicit no-funding statement;
- competing-interest statement;
- author-contribution statement / CRediT mapping;
- acknowledgements;
- all-author approval of the exact manuscript version.

The Markdown manuscript intentionally contains explicit placeholders for these fields rather than inferred values.

### Content already normalized for the target journal

- title and saturated Mechanism → Pattern framing;
- 150–250-word abstract;
- six keywords;
- Methods disclosure of non-copyediting LLM assistance;
- name-year reference architecture;
- `Statements and Declarations` after `References`;
- Funding, Competing interests, Author contributions, and Data/code availability headings;
- figure captions outside the illustrations using `Fig. n` form.

### Upload-format route

Choose one final production route after author metadata are supplied.

**Word route**

```text
Main manuscript: editable DOCX
Companion manuscript PDF: include alongside the Word file
```

The final DOCX/PDF pair must be generated from the same frozen source commit and checked for equations, symbols, table wrapping, captions, references, and declaration placement.

**LaTeX route**

Use only if the authors choose the supported Springer LaTeX workflow. The fixed theory contains substantial mathematical notation, but this plan does not switch production formats automatically.

Do not maintain parallel Word and LaTeX submission sources after the final route is chosen unless needed for archival purposes.

## 2. Main figure uploads

Submission-form vector files:

```text
Fig1.eps
Fig2.eps
Fig3.eps
```

Canonical scientific sources remain the committed SVG files under `manuscript/figures/`. The submission exporter:

1. removes exactly one visible outer figure-title line from each illustration;
2. retains panel labels, equations, and scientific annotations;
3. exports EPS vector graphics;
4. converts text to paths to prevent font substitution;
5. validates the PostScript header and BoundingBox.

Current submission-form validation receipt:

```text
source head:       fe274a91349931c08b8d820f99dc7b3ab5d8f725
workflow run:      31666278452
artifact id:       9168041835
artifact sha256:   f4fb42b7421958a5a5251f24f03c666de2735b28bbded739286e65e9705090fd
submission files:  Fig1.eps, Fig2.eps, Fig3.eps
```

Core CI and submission-scope were also green at that same source head. This Actions artifact validates the workflow; it is not the permanent archival package. Re-export from the final release commit if any canonical figure or caption requirement changes.

## 3. Main tables

Tables 1–4 are manuscript tables rather than image files unless the portal specifically requests separate table uploads.

```text
Tables 1–2: Part I Mechanism
Tables 3–4: Part II Pattern
```

Tables 3–4 must remain synchronized to the saturated 56/25 evidence universe. Route counts overlap and cannot be summed as independent-study totals.

## 4. Supplementary package

The supplement now has a reproducible reader-facing source plus machine-readable figures/tables. It should make the full evidence architecture auditable without forcing every system into the main text.

### Supplementary reader-facing source

```text
manuscript/supplementary/SUPPLEMENTARY_MATERIAL.md
```

Current generated figure set:

```text
Fig. S1  analytic-versus-finite-difference derivative agreement
Fig. S2  scenario-specific mechanistic sign maps
Fig. S3  same-system route architecture across 14 linked systems
Fig. S4  quantitative robustness for Leal + Sasidharan modules
```

Fig. S4 now preserves the canonical DerSimonian–Laird Leal estimates and adds a separate REML + modified Hartung–Knapp sensitivity inset from `LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json`. Female reproductive success and nectar standing crop remain clearly below zero; legitimate visitation remains below zero but is explicitly labelled borderline to zero because the mHK upper endpoint is approximately `-0.00018`. This is robustness presentation only and does not replace the canonical estimates or reduce the declared heterogeneity.

The supplementary build workflow reproduces Part I evaluations, generates Figures S1–S4 and Tables S1–S6, augments Fig. S4 from the machine-readable Gate G receipt, regression-tests the package, and commits generated assets only when they change.

### Supplementary PDF

Prepare one reader-facing supplementary PDF after final numbering and author/release metadata are frozen. It should contain/cite:

- Supplementary Figures S1–S4;
- narrative methods needed to interpret supplementary ledgers;
- direct `A x D` and joint-cost saturation summaries;
- Pattern-expansion stopping-gate summary;
- source/access-status notes for secondary syntheses;
- explanatory notes required for supplementary tables.

The final supplement PDF should carry the exact release commit and archival DOI. Do not mint a misleading final PDF while those release-controlled fields are still unknown.

### Supplementary tabular files

Retain machine-readable tabular products in appropriate CSV/XLSX form rather than converting them into screenshots.

```text
Table S1  complete parameter definitions / scaling
Table S2  all 162 local cases and sign classifications
Table S3  full canonical + expansion mechanism/Pattern route ledger
Table S4  canonical + expansion sign-switch/context ledgers and 7 context programs
Table S5  direct A x D and joint-cost search decisions / exclusion classes
Table S6  Pattern-expansion screening and stopping batches
```

The exact portal filenames can be frozen at release time, but supplementary numbering must match all in-text citations.

## 5. Cover letter and reviewer fields

The cover-letter draft already uses the saturated 56/25 framing.

Before upload, authors must provide **exactly five** potential reviewers with:

- name;
- institution;
- active e-mail;
- relevant expertise;
- conflict check.

Reviewer names must not be inferred from citations or generated merely because a researcher is prominent in the field. Any opposed reviewers should be listed only for a specific defensible conflict.

## 6. Portal metadata

Source: `submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md`.

Already synchronized:

- title;
- article type;
- target journal;
- running title;
- 150–250-word abstract;
- six keywords;
- repository URL;
- draft data/code statement;
- five-reviewer requirement.

Still author-controlled:

- author list/order;
- affiliations;
- corresponding-author fields;
- ORCIDs;
- CRediT;
- funding;
- acknowledgements;
- competing interests;
- reviewer names;
- all-author approval.

## 7. Repository release and archive

Do not mint the final release before the author-controlled fields and repository licence are resolved.

Final sequence:

```text
freeze author-approved manuscript + declarations
-> choose repository licence/licence statement
-> choose final manuscript production route
-> generate final manuscript upload files
-> regenerate submission EPS if figure/caption requirements changed
-> render final supplementary PDF from the same release source
-> run exact-release CI / house-style / main-figure export / supplementary-package validation
-> create release/tag
-> archive and obtain DOI
-> insert archival DOI and exact commit into manuscript/portal/supplement metadata
-> all-author approval check
-> upload to authenticated journal portal
```

The Actions artifacts are never substituted for the final permanent archive.

## 8. Exact pre-upload QA

Before portal upload, verify from the **same release commit**:

- [ ] author/title page complete and identical in manuscript and portal;
- [ ] abstract and six keywords identical in manuscript and portal;
- [ ] Funding / Competing interests / Author contributions finalized;
- [ ] AI-assistance disclosure retained in Methods;
- [ ] 20-reference spine still citation-consistent after final edits;
- [ ] all equations and Greek symbols render correctly;
- [ ] Tables 3–4 still report 56 / 25 / 5 / 8 / 18 / 10 / 14 / 17 / 7 correctly;
- [ ] Fig1.eps–Fig3.eps contain no visible outer figure title;
- [ ] figure captions remain outside illustrations;
- [ ] Fig. S4 retains canonical DL estimates and the separate REML/mHK sensitivity inset;
- [ ] legitimate-visitation mHK interval remains labelled borderline to zero unless source JSON changes;
- [ ] supplement numbering and in-text citations agree;
- [ ] Tables S1–S6 regenerate byte/content-consistently from authoritative inputs;
- [ ] full CI and house-style tests pass;
- [ ] supplementary-package workflow passes;
- [ ] final EPS export passes;
- [ ] release/tag and archive DOI resolve;
- [ ] repository licence statement is explicit;
- [ ] exactly five reviewer suggestions are conflict-checked;
- [ ] all authors approve the exact submitted package;
- [ ] manuscript is not simultaneously under consideration elsewhere.

## Current decision

```text
scientific evidence gate:          GO
Pattern expansion gate:           CLOSED / SATURATED
journal structural house style:    PASS
main submission-form EPS pipeline: PASS
supplementary source package:      PASS / REPRODUCIBLE
Gate G modern-estimator display:   SYNCHRONIZED
main manuscript final render:      BLOCKED by author-controlled title/declaration fields
supplement final PDF render:       BLOCKED by author + release metadata freeze
release / archival DOI:            BLOCKED by author + licence decisions
portal upload:                      BLOCKED by author metadata/reviewers and authentication
```
