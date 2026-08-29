# Theoretical Ecology submission contract v2

## Target

Journal: **Theoretical Ecology**  
Article type: **Regular Article**  
Scientific source: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`

This contract supersedes the old theorem-led upload narrative for the identification-first manuscript. The existing Ecology Concepts & Synthesis package remains a fallback/legacy artifact and must not be used as evidence that the Theoretical Ecology package is compliant.

## Current publisher requirements checked 2026-08-29

The current Springer Nature instructions for *Theoretical Ecology* require or state that:

- a Word manuscript should be accompanied by a PDF version;
- all relevant editable source files must be supplied;
- the title page contains author names, affiliations, corresponding-author e-mail and ORCID when available;
- the abstract is 150–250 words;
- 4–6 keywords are supplied;
- manuscripts are submitted in Word, with LaTeX also supported for mathematical content;
- `Statements and Declarations` are required after the References section, including Funding and Competing Interests, with Author Contributions encouraged;
- LLM use that goes beyond copy editing is documented in Methods or an equivalent section;
- five potential reviewers should be suggested in the cover letter;
- figures should be cited consecutively, captions remain in the manuscript rather than inside the illustration, and vector artwork is preferably EPS with fonts embedded;
- supplementary text is preferably supplied as PDF, while spreadsheets may be CSV/XLSX.

## Scientific framing for this target

The paper is not submitted as a theorem paper and not as a broad empirical prevalence review.

Primary contribution:

```text
measurable total A x D interaction
-> identified set of compatible channel allocations
-> assumption-indexed partial identification
-> selective crossed interventions for channel allocation
-> four-way diagnostic for non-separability
-> independent cost assay before naming residual cost
```

Empirical stress tests:

```text
Kessler 2008:
  manipulated A x D-like field factorial
  aggregate female sign robustly positive
  source/design uncertainty unresolved

Impatiens 2018:
  uncertainty-bearing observational A x D
  intervals cross zero
  no causal escape claim
```

Prospective closure:

```text
Stage 1  total sign with design-based uncertainty
Stage 2  pilot channel effects
Stage 3  re-powered 16-cell mechanism allocation + independent cost assay
```

## Main-manuscript promotion rules

### Main text

Retain:
- discrete factorial estimand;
- identified-set interpretation;
- partial-identification logic;
- crossed intervention design and separability diagnostic;
- Kessler as the strongest manipulated total-sign anchor;
- Impatiens as the complementary uncertainty-bearing observational boundary;
- staged experimental programme.

Do not promote:
- Kessler aggregate sensitivity to a recovered source CI;
- a systemic nicotine manipulation to a flower-exclusive defence intervention;
- route counts to literature prevalence;
- 16-cell arithmetic budgets to mechanism power;
- positive total interaction to identified `rho`, `iota` or `kappa`.

### Supplementary / online resource

Move detailed:
- route and high-information ledgers;
- Kessler supplement-access receipt and aggregate-allocation sensitivity;
- Impatiens model receipts;
- Stage-1 power and cluster-allocation grids;
- field-data contracts and machine-readable analysis receipts;
- historical theorem/grid sensitivity material not required for the identification-first argument.

## Technical submission gates

A generated package is `TECHNICALLY_READY` only if all automated gates pass:

1. target journal = `Theoretical Ecology`;
2. article type = `Regular Article`;
3. abstract word count in `[150, 250]`;
4. keyword count in `[4, 6]`;
5. title in cover letter matches manuscript title;
6. exactly five reviewer placeholders are present;
7. Methods contains the AI/LLM disclosure;
8. `Statements and Declarations` appears after `References`;
9. Funding, Competing Interests, Author Contributions, and Data and code availability sections exist;
10. generated Word and PDF contain the manuscript title and identification-first framing;
11. five identification-design figures are embedded in the Word manuscript and present in the review package;
12. the main package contains no Ecology-specific 30/50-page decision rule.

## Registered successful package validation

The dedicated target-journal workflow has now completed successfully.

```text
source head:       add2b3634f39d878524c22eeac332c34d306ffa7
workflow:          build-theoretical-ecology-submission-package
run id:            33239061128
run number:        4
conclusion:        success
artifact:          theoretical-ecology-submission-package
artifact id:       9710804367
artifact sha256:   ff7acdaa421d66590d960f8190159da6dffd2e8d26a8b6f23c42236330c491c2
```

The successful package validates:

```text
abstract:                 201 words
keywords:                 6
main Word manuscript:     generated
companion main PDF:       generated
Online Resource 1 PDF:    generated
cover-letter PDF:         generated
embedded main figures:    5
Statements/Declarations:  after References
technical status:         TECHNICALLY_READY
human status:             BLOCKED_AUTHOR_METADATA
```

The workflow does not turn placeholders into approved author metadata and does not authorize portal submission.

## Human-controlled blockers

Even a technically valid generated package remains `BLOCKED_AUTHOR_METADATA` until authors approve:

- final author names and order;
- affiliations;
- corresponding-author e-mail;
- ORCIDs;
- funding statement;
- competing-interest statement;
- author contributions;
- acknowledgements;
- repository licence and archival DOI;
- five real reviewer suggestions and conflict checks;
- exact submitted version.

No tool should infer these fields.

## Current target decision

```text
scientific framing:         GO / IDENTIFICATION_FIRST
historical Kessler sign:    POSITIVE_AGGREGATE / SOURCE_CI_UNRESOLVED
Stage-1 design:             EXECUTABLE
mechanism allocation:       NOT YET EMPIRICALLY IDENTIFIED
Theoretical Ecology fit:    GO
technical package:          TECHNICALLY_READY / WORKFLOW GREEN
final portal submission:    BLOCKED_AUTHOR_METADATA
```
