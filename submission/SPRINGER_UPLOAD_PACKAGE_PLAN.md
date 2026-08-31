# Theoretical Ecology / Springer upload package plan — LEGACY

> **Superseded for the current identification-first submission.** This document records the older saturated Mechanism → Pattern / theorem-led package and must not be used as the current Theoretical Ecology readiness contract. The authoritative target-journal contract is `submission/THEORETICAL_ECOLOGY_SUBMISSION_CONTRACT_V2.md`; the authoritative package workflow is `.github/workflows/build-theoretical-ecology-submission-package.yml`. The older Ecology Concepts & Synthesis workflow remains a fallback/legacy package only.

## Purpose

This file maps the saturated 25-system Mechanism → Pattern candidate to the historical journal upload roles. It is retained for provenance, not as a replacement for the current identification-first package, journal portal, or final author-approval record.

## Historical scientific package

```text
Part I — Mechanism: fixed theory, Figures 1–2, Tables 1–2
Part II — Pattern:   56 route records / 25 systems, Figure 3, Tables 3–4
same-system:         14 clusters
context/sign switch: 17 clusters
context-only:         7 programs, excluded from route N
direct A x D:         1 strict sign-unresolved cluster
direct joint cost:    0 strict estimates; kappa unidentified
```

The empirical expansion was saturated under the historical registered stopping rule. These counts remain provenance but are no longer the lead submission framing.

## Current replacement

The current Theoretical Ecology Regular Article is organized around:

```text
measurable total A x D interaction
-> identified set
-> partial identification
-> selective crossed interventions
-> separability diagnostic
-> independent cost assay
```

with Kessler 2008 as the strongest manipulated sign-positive aggregate anchor, Impatiens as the uncertainty-bearing observational boundary, and a staged Stage-1 → mechanism-pilot → re-powered mechanism experiment.

Current automated package source and gate:

```text
submission/THEORETICAL_ECOLOGY_SUBMISSION_CONTRACT_V2.md
scripts/build_theoretical_ecology_submission_sources.py
.github/workflows/build-theoretical-ecology-submission-package.yml
```

Current target-package policy:

- Word main manuscript + companion PDF;
- 150–250-word abstract;
- 4–6 keywords;
- Statements and Declarations after References;
- five identification-design figures embedded in the Word manuscript;
- Online Resource PDF;
- five author-controlled reviewer suggestions in the cover letter;
- machine-readable QA must be `TECHNICALLY_READY`;
- final status remains `BLOCKED_AUTHOR_METADATA` until all author-controlled fields are approved.

## Historical upload-format route

The historical Word/LaTeX and EPS discussion below is retained only as provenance. It may still inform final production choices, but any conflict with the V2 contract is resolved in favor of V2.

### Author/title-page fields that remain human-controlled

Before actual portal submission the authors must still supply/approve:

- final publication names and author order;
- affiliations;
- corresponding author and active e-mail;
- ORCID identifiers where available;
- funding statement or explicit no-funding statement;
- competing-interest statement;
- author-contribution statement / CRediT mapping;
- acknowledgements;
- repository licence and archival DOI;
- exactly five potential reviewers with institution, active e-mail, expertise and conflict check;
- all-author approval of the exact manuscript version.

Do not infer any of these values.

## Current decision

```text
historical Mechanism -> Pattern package:  LEGACY / PROVENANCE ONLY
current scientific framing:              IDENTIFICATION_FIRST
Theoretical Ecology article type:        Regular Article
current target workflow:                 build-theoretical-ecology-submission-package
technical package gate:                  TECHNICALLY_READY when workflow is green
human metadata gate:                     BLOCKED_AUTHOR_METADATA
portal upload:                           BLOCKED until human fields and authentication are complete
```
