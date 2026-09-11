# Repository structure and source-of-truth policy

BITA is now the **mechanism-identification paper** in the SCH–SLK–BITA programme.

Its active claim boundary is:

```text
trait interaction != ecological mechanism
```

The older integrated architecture-plus-mechanism Chapter 2 package is retained as provenance but is no longer a competing source of truth.

## 1. Active canonical graph

### Main science source

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Current paper question:

> When two traits interact on fitness, what does that interaction identify, which ecological mechanisms remain compatible with it, and what additional interventions are required to identify the mechanism?

### Live submission scope

```text
docs/SUBMISSION_SCOPE.md
```

### Active review-package route

```text
scripts/build_bita_mechanism_candidate_sources.py
.github/workflows/build-bita-mechanism-review-package.yml
```

### Active figures / supplement / evidence

```text
manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md
manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md
manuscript/mechanism_identification_figures/
empirical/identification_design/
empirical/mechanism_pattern_synthesis/
```

The mature longer identification manuscript `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains a provenance and reusable scientific source, not a second active submission main.

## 2. Programme ownership

```text
SCH
multifunctionality != conflict
        |
        v
identified shared-coordinate conflict when justified
        |
        v
SLK
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
        |
        v
BITA
trait interaction != mechanism
```

### BITA owns

- the Level 1/2/3 outcome hierarchy for an observed trait interaction;
- identified sets and partial identification;
- selective crossed consumer interventions;
- four-way separability diagnostics;
- independent remaining-channel assays;
- source-adjudicated recurrence of constituent ecological routes;
- the fragmented mechanism-identification frontier.

### BITA does not own as active novelty

- architecture value `R`, `K`, `Phi` or population-realization transport;
- historical origin of a second trait axis;
- prevalence of differentiated architectures;
- a universal ecological mechanism inferred from interaction sign.

Those architecture-value questions are routed to SLK; older differentiation derivations remain versioned as technical provenance.

## 3. Active empirical order

BITA follows:

```text
mathematical identification mechanism
-> observable route / identification signatures
-> source-adjudicated literature synthesis
-> compatible quantitative route lanes
-> residual mechanism-identification gap
-> focal crossed causal experiment last
```

The current literature-pattern spine is:

```text
56 directional route records
25 independent biological clusters
14 same-system multi-route clusters
17 context/sign-switch clusters
17 high-information systems
0 systems closing full mechanism allocation + independent remaining-channel assay
```

These counts establish recurrence within the screened evidence universe and a fragmented identification frontier. They are not natural prevalence estimates.

## 4. Quantitative evidence policy

Route-level quantitative synthesis is allowed only within compatible biological/statistical strata with independent biological clusters, compatible effect definitions, valid sampling variance and dependence handling.

Current registered route lanes include nectar-larceny female fitness, visitation, reward and male-fitness summaries. These quantify constituent ecological channels only.

They do not identify the allocation

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

for a focal two-trait system.

The strict mechanism-allocation lane remains empty until one same system closes the required crossed interaction, channel interventions, separability diagnostic and independent remaining-channel assay.

## 5. Fail-closed claim policy

Keep the following distinctions explicit:

```text
positive interaction
!= functional release
!= ecological mechanism

marginal route recurrence
!= total interaction identification
!= channel allocation
!= prevalence

structural separation
!= functional independence

unmeasured residual
!= biological joint cost
```

A quantitative pool whose admission rule already requires a directional pattern is interpreted as conditional on that admission, not as an unbiased design-wide mean or an independent recurrence test.

## 6. Legacy package policy

`docs/CHAPTER2_SUBMISSION_SCOPE_V1.md` is an archived receipt for the former integrated architecture-plus-mechanism package.

The former package builders are retained only as provenance code:

```text
scripts/build_trait_differentiation_candidate_package_sources.py
scripts/build_ecology_review_package_sources.py
```

The former workflow filenames:

```text
.github/workflows/build-trait-differentiation-candidate.yml
.github/workflows/build-ecology-submission-package.yml
```

are legacy routing guards. They must not rebuild or validate the stale architecture submission package.

The active review artifact is built only through `build-bita-mechanism-review-package.yml`.

## 7. Tests and reproducibility graph

Current high-value regression surfaces include:

- active manuscript claim/narrative guards;
- mechanism-identification figure guards;
- identified-set and partial-identification tests;
- high-information identification-coverage tests;
- literature-pattern/meta-analysis layer guards;
- submission-scope and active review-package guards.

Historical theory tests remain useful when they protect still-valid technical results, but they do not determine the active paper ownership.

## 8. Change policy

Classify changes before implementation:

- **Editorial** — wording, flow, labels, captions, reference formatting.
- **Reproducibility** — tests, deterministic builders, provenance receipts, workflow routing.
- **Scientific correction** — changed estimate, derivation, admitted evidence or claim ceiling; requires downstream revalidation.
- **New discovery** — a new model or empirical programme; admit only if it directly advances the active mechanism-identification question or is explicitly routed to a companion repository.

## 9. Current endpoint

The active paper currently supports:

```text
interaction detection
-> outcome hierarchy
-> identified mechanism set
-> partial identification
-> source-adjudicated recurrence of constituent routes
-> fragmented identification frontier
-> design of the next identifiable crossed experiment
```

The focal experiment is the final identification upgrade. It is not the empirical entry point and is not a blocker for the present theory + literature-pattern synthesis.

```text
STATUS = SINGLE_ACTIVE_SOURCE_GRAPH
ACTIVE_MAIN = manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
ACTIVE_SCOPE = docs/SUBMISSION_SCOPE.md
ACTIVE_PACKAGE_WORKFLOW = build-bita-mechanism-review-package.yml
```
