# Biotic Interaction Trait Architecture (BITA)

BITA is the **mechanism-identification paper** in the SCH–SLK–BITA programme.

Its central claim boundary is:

```text
trait interaction != ecological mechanism
```

The architecture-value spine now belongs to [SLK](https://github.com/zuizui0223/slk):

```text
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
```

BITA begins after multiple trait axes are empirically relevant and asks what biological route generated their joint fitness effect.

## Canonical question

> When two traits interact on fitness, what does that interaction actually identify, which mechanisms remain compatible with it, and what additional interventions are required to identify the ecological route?

## Main inference ladder

For two focal traits `A` and `D`,

```text
Delta_AD W = W11 - W10 - W01 + W00
```

is a measurable total interaction. It does not uniquely identify its ecological allocation.

The retained ladder is:

```text
interaction detection
-> identified set
-> partial identification
-> selective A x D x antagonist x pollinator intervention
-> four-way separability diagnostic
-> independent remaining-channel assay
```

The mechanism accounting identity is

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

but an unmeasured residual is **not** called `kappa_delta` by subtraction. A biological joint-cost interpretation requires an independent assay.

## Nested outcome claims

BITA also distinguishes three outcome levels:

```text
Level 1  positive interaction relief: Delta_AD W > 0
Level 2  functional constraint release: A0 <= 0 < A1
Level 3  strict reversal: A0 < 0 < A1
```

A positive interaction does not automatically establish Levels 2 or 3.

## Empirical synthesis

The source-adjudicated empirical layer contains:

- **56 directional route records**,
- **25 independent biological clusters**,
- **17 high-information systems** in the strict identification frontier.

All four constituent marginal route families recur, but no screened high-information system closes the full channel-allocation design plus independent joint-channel assay.

The empirical conclusion is therefore:

```text
RECURRENT_CONSTITUENT_BIOLOGY
+
FRAGMENTED_IDENTIFICATION
```

not prevalence of trait differentiation and not a recovered universal mechanism.

## Programme ownership

```text
SCH
multifunctionality != identified functional conflict
        |
        v
identified conflict / L when justified
        |
        v
SLK
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
        |
        v
multiple trait axes / observed interaction
        |
        v
BITA
trait interaction != mechanism
```

### SCH owns

- multifunctionality-versus-conflict inference;
- state-specific versus pure-function optima;
- the causal promotion gate for shared-coordinate conflict.

### SLK owns

- `R`, `K`, and `Phi = R-K` as the architecture-value spine;
- the quadratic bridge `R=sL` where applicable;
- accessibility, invasion, fixation, occupancy, and INV1.

### BITA owns

- interaction-versus-mechanism inference;
- identified sets and partial identification;
- selective crossed consumer interventions;
- separability diagnostics;
- independent remaining-channel assays;
- the 56-route / 25-cluster synthesis and 17-system identification frontier.

The older BITA architecture derivations remain preserved as technical provenance and supporting modules. They are not the novelty center of the active full paper.

## Canonical manuscript graph

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — **canonical active full-paper science source**; now refocused on mechanism identification
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — mature longer provenance/source text for the identification framework
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` — focused reference pool
- `manuscript/CLAIM_FREEZE.md` — active scientific claim ceiling
- `docs/SUBMISSION_SCOPE.md` — active submission scope
- `docs/PUBLICATION_STATUS.md` — programme-level publication status
- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` — detailed identification supplement

## Package status

The previously validated 30-page Main + 38-page Appendix package belonged to the older integrated architecture-plus-mechanism manuscript and is now **historical, not submission-current**.

```text
SCIENCE_SOURCE_REFOCUSED
OLD_PACKAGE_STALE
REBUILD_REQUIRED
```

Do not submit the old generated package after the canonical manuscript refocus. Rebuild figures, captions, supplement routing, cover letter, and page-count checks around the new mechanism-identification manuscript before any journal upload.

## Testing

A fresh checkout should install the package and development dependencies before running tests:

```bash
python -m pip install -e '.[dev]'
pytest -m "not prose_contract"   # blocking code / numerical tests
pytest -m prose_contract         # advisory Markdown/document contracts
```

The `prose_contract` suite is retained to audit synchronization among manuscripts, readouts, and repository claims, but it is reported separately from core code validation because wording-only edits must not masquerade as computational regressions.

## Strict boundaries

```text
positive A x D interaction
!= mechanism
!= trait differentiation
!= historical splitting

structural separation
!= functional independence

route recurrence
!= prevalence

residual by subtraction
!= identified joint cost
```

BITA does not claim to invent ecological interaction theory, specialization, modularity, or causal inference. Its contribution is the explicit promotion ladder showing what increasingly strong experimental information is required before a trait interaction can be interpreted as an ecological mechanism.
