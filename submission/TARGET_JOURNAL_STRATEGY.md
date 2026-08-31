# Target journal strategy

## Current first choice

**Theoretical Ecology — Regular Article**

The current manuscript is now an **identification-first theoretical ecology paper**, not the older theorem-led Mechanism → Pattern candidate and not an Ecology Concepts & Synthesis submission.

Primary contribution:

```text
measurable total A x D interaction
-> identified set of compatible channel allocations
-> partial identification under explicit restrictions
-> crossed consumer interventions for mechanism allocation
-> internal separability diagnostic
-> independent joint-cost assay before naming a residual as cost
```

Empirical material is used as identification stress tests, not as a prevalence survey:

- Kessler et al. 2008: direct manipulated A×D-like field surface; aggregate female sign robustly positive; source/design CI unresolved; systemic-nicotine scope caveat.
- *Impatiens capensis*: uncertainty-bearing observational A×D estimates; intervals cross zero; no causal escape claim.
- route/high-information ledgers: establish recurrence and locate missing intersections; not prevalence and not channel calibration.

## Why Theoretical Ecology fits

The paper develops a general ecological inference problem and turns it into:

- an experimentally measurable factorial estimand;
- an identified-set representation;
- sharp/assumption-indexed partial-identification bounds;
- selective-intervention estimands for antagonist relief and pollinator interference;
- a four-way diagnostic for failure of separability;
- a staged experimental program separating outcome identification from mechanism attribution.

The floral system provides biological substance, but the identification logic transfers to ecological phenotypes that affect several opposing pathways.

## Dedicated target-journal package

The old `build-ecology-submission-package` workflow remains a **legacy/fallback** Ecology Concepts & Synthesis artifact. It must not be used to claim Theoretical Ecology readiness.

The authoritative target workflow is:

```text
.github/workflows/build-theoretical-ecology-submission-package.yml
```

The authoritative target contract is:

```text
submission/THEORETICAL_ECOLOGY_SUBMISSION_CONTRACT_V2.md
```

The dedicated workflow generates and validates:

- main editable Word manuscript;
- companion main PDF;
- Online Resource 1 PDF;
- cover-letter PDF/source;
- five embedded identification-design figures;
- open-research data files;
- machine-readable QA receipt.

Registered green validation:

```text
source head:       add2b3634f39d878524c22eeac332c34d306ffa7
workflow run:      33239061128
artifact id:       9710804367
artifact sha256:   ff7acdaa421d66590d960f8190159da6dffd2e8d26a8b6f23c42236330c491c2
abstract:          201 words
keywords:          6
embedded figures:  5
automated status:  TECHNICALLY_READY
human status:      BLOCKED_AUTHOR_METADATA
```

The validation receipt is also frozen in `THEORETICAL_ECOLOGY_SUBMISSION_CONTRACT_V2.md` and revalidated whenever that contract or target package changes.

## Scientific promotion boundary

The target-journal package may say:

```text
Kessler aggregate sign is robustly positive on the declared female probability scale.
A manipulated attraction-by-defence-like surface exists.
The source/design-based interval is not recovered.
A positive total interval would decide the escape inequality without point-identifying all channels.
The full mechanism requires selective consumer interventions and an independent cost assay.
```

It may not say:

```text
Kessler formally identifies escape.
Systemic nicotine is a flower-exclusive D manipulation.
Positive total Delta identifies rho/iota/kappa.
The 56/25 route ledger is prevalence.
The arithmetic 16-cell extrapolation is mechanism power.
```

## Current blockers before actual portal upload

Only human/release-controlled fields remain outside the automated package:

- final author names and order;
- affiliations;
- corresponding-author contact;
- ORCIDs;
- approved Funding statement;
- approved Competing Interests statement;
- approved Author Contributions and acknowledgements;
- repository licence;
- final archival DOI/release;
- five real potential reviewers with conflict checks;
- all-author approval of the exact submitted package;
- authenticated portal upload.

None of these should be inferred automatically.

## Fallbacks

The legacy Ecology Concepts & Synthesis package is retained only as a fallback/provenance route. A fallback should be activated by an editorial/fit decision, not by weakening the current identification-first framing.

## Decision

```text
Theoretical Ecology scientific fit:    GO
Theoretical Ecology technical package: TECHNICALLY_READY
scientific overclaim gate:             PASS / FAIL-CLOSED
final author metadata:                 BLOCKED_AUTHOR_METADATA
portal submission:                     NOT YET AUTHORIZED
```
