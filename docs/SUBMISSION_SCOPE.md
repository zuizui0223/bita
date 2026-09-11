# Submission scope — BITA mechanism-identification paper

Primary target class: **Ecology — Concepts & Synthesis** or a comparable conceptual/methodological ecology venue.

## Canonical question

> **When two traits interact on fitness, what does that interaction identify, which ecological mechanisms remain compatible with it, and what additional interventions are required to identify the mechanism?**

The active paper is no longer the general architecture-value paper. The architecture-value spine (`L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy`) is owned by SLK.

## 1. Primary estimand

For two focal trait contrasts `A` and `D`,

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

Define

```text
A0 = W10 - W00
A1 = W11 - W01
```

so `Delta_AD W = A1 - A0`.

The active paper separates:

```text
Level 1  Delta_AD W > 0                 positive interaction relief
Level 2  A0 <= 0 < A1                   functional constraint release
Level 3  A0 < 0 < A1                    strict reversal
```

Level 1 does not imply Levels 2 or 3.

## 2. Mechanism non-identification

Use the bookkeeping decomposition

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

where the terms represent antagonist relief, pollinator interference, and a remaining direct/allocation channel on a common declared scale.

A measured total interaction `delta` defines

```text
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

rather than a unique mechanism.

The paper's methodological progression is:

```text
interaction detection
-> identified set
-> partial identification under explicit restrictions or channel measurements
-> selective A x D x antagonist x pollinator intervention
-> baseline handling + four-way separability diagnostic
-> independent assay of the remaining joint channel
```

## 3. Empirical pattern layer

The source-adjudicated route synthesis contains:

```text
56 directional route records
25 independent biological clusters
```

These establish recurrence of constituent pathways, not prevalence and not point identification of the total mechanism.

The strict high-information audit contains:

```text
17 systems
0 systems closing the full allocation design + independent joint-channel assay
```

The conclusion is **fragmented identification**, not absence of relevant biology.

## 4. Strongest current system-level anchor

Kessler et al. (2008) supplies the strongest direct attraction-by-defence-like factorial anchor.

Under the registered aggregate constraints:

```text
A1 approximately +0.200 to +0.240
A0 approximately -0.030 to +0.030
Delta_AD remains positive
```

This supports strong Level-1 evidence and asymmetric partial identification of the stronger release claim. It does not identify strict Level 2/3 because `A0` remains zero-compatible, and it does not allocate the ecological mechanism.

## 5. Required claim boundaries

```text
positive A x D interaction
!= ecological mechanism
!= trait differentiation
!= historical splitting

marginal route recurrence
!= total interaction identification
!= channel allocation
!= prevalence

structural separation
!= functional independence

unmeasured residual
!= biological joint cost
```

BITA does not claim the historical origin of differentiated traits, prevalence of differentiated architectures, or a universal route by which trait interactions arise.

## 6. Relationship to the other programme papers

```text
SCH
multifunctionality != conflict
        |
        v
identified L when justified
        |
        v
SLK
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
        |
        v
BITA
trait interaction != mechanism
```

The older `R=sL`, architecture-cost, nonquadratic differentiation, and partial-decoupling derivations remain preserved in the repository as provenance and technical support. They are not active submission novelty claims.

## 7. Canonical source graph

- active Main science source: `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- mature longer identification provenance source: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- active claim freeze: `manuscript/CLAIM_FREEZE.md`
- focused references: `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`
- detailed identification supplement: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- publication programme status: `docs/PUBLICATION_STATUS.md`

## 8. Submission-package status

The previously validated `30 Main pages + 38 Appendix pages` package belongs to the older integrated architecture-plus-mechanism manuscript.

It is now explicitly stale:

```text
OLD_PACKAGE_STALE
NEW_CANONICAL_SCIENCE_SOURCE_ACTIVE
REBUILD_REQUIRED_BEFORE_SUBMISSION
```

The next package must rebuild title, abstract, figures, captions, supplement routing, cover letter, page count, and visual QA around the mechanism-identification manuscript. Author metadata remains an external final step after scientific packaging is green.
