# Mechanism-pattern synthesis completion status v4

## Scope and source of truth

This file records the scientific state of the fixed Mechanism paper plus the saturated Pattern-expansion candidate.

```text
canonical integration PR:   #126
canonical branch:           agent/mechanism-pattern-universality-v1
expanded candidate PR:      #129
expanded candidate branch:  analysis/pattern-expansion-v1
```

Part I theory remains fixed. PR #129 changes Part II evidence capacity and manuscript-facing Pattern synthesis; it does not change any equation, theorem, theoretical parameter, or finite-sensitivity result.

## A–H scientific gate

| Gate | Status | Basis | Expansion effect |
|---|---|---|---|
| **A — direct `A x D`** | **PASS as bounded gap** | `DIRECT_AXD_SATURATION_RECEIPT_V1.md` | unchanged: one strict cluster, sign unresolved |
| **B — four marginal mechanism families** | **PASS** | canonical ledgers + `EXPANSION_LEDGER_BATCH_*_V1.csv` | saturated route evidence expands to 25 independent systems |
| **C — quantitative modules** | **PASS** | Leal 2025 + Sasidharan 2023 reproduced modules | three additional secondary contextual syntheses retained with different status |
| **D — conditionality** | **PASS** | canonical + expansion sign-switch ledgers and context programs | 17 sign/state-switch clusters plus 7 context-only programs |
| **E — same-system linkage** | **PASS** | canonical + expansion route ledgers | 14 same-system multi-route clusters |
| **F — direct joint cost** | **PASS as documented gap** | `JOINT_COST_SATURATION_RECEIPT_V1.md` | zero strict estimates; `kappa` unidentified |
| **G — robustness/bias** | **PASS** | reproduced-module audits + source/access receipts | evidence-status and source-access distinctions remain explicit |
| **H — theory/empiricism boundary** | **PASS** | boundary audit + manuscript/figure/table regression tests | 25-system candidate retains all inference prohibitions |

## Saturated Pattern architecture

```text
route-ledger records:               56
independent biological clusters:    25
A -> pollination clusters:           5
A -> antagonism clusters:            8
D -> antagonism clusters:           18
D -> pollination clusters:          10
same-system multi-route clusters:   14
context/sign-switch clusters:       17
context-only programs:               7  (excluded from route-ledger N)
direct A x D strict clusters:        1  (sign unresolved)
direct joint-cost strict estimates:  0  (kappa unidentified)
```

Route counts overlap. They are evidence-capacity diagnostics within the screened architecture, not prevalence estimates and not additive independent-study totals.

## What the expansion added

The expansion targeted weak or empty mechanism/context cells under the same focal-trait and flower-specific-defence rules rather than maximizing article count.

### Attraction-side recurrence

Independent signal systems now include volatile, visual-bract, colour, and multidimensional colour/scent axes. New examples include *Dalechampia scandens*, *Raphanus sativus*, and a recombinant *Silene latifolia × S. dioica* signal system linking floral sensory dimensions to antagonist host choice.

### Flower-specific defence diversity

Independent D systems now include water-filled bracts/calyces, floral surface stickiness, slippery epicuticular wax, dense petal hairs, spur-enclosing floral bracts, and floral nectar chemistry. These are counted at independent study-cluster level rather than per species, population, treatment cell, or assay.

### New recurrent state classes

- **guarded defence** — antagonist reduction without a universally detected pollinator penalty;
- **spatial / temporal / attack-mode filtering** — defence works only for particular access routes, consumer sizes, attack modes, or reproductive windows;
- **pollinator functional-mode routing** — the same visitor can shift between legitimate pollination and robbery without a change in identity or arrival rate;
- **lifecycle-stage role reversal** — one consumer taxon can be a mutualist at one life stage and an antagonist at another;
- response-stage, resource/exposure, trait-class, population/site, and compound/mechanism dependence.

## Registered expansion stopping gate

`PATTERN_EXPANSION_COMPLETION_GATE_V1.md` records:

```text
Batch 7: new theory-facing class found -> stopping counter reset
Batch 8: no new admissible Pattern class
Batch 9: distinct candidate set, again no new admissible Pattern class
quantitative expansion search: no sixth synthesis with a distinct theory-facing axis
```

Therefore the current Pattern expansion is **saturated for the manuscript’s registered theory-facing purpose**. Additional broad searching is not a default blocker.

## Quantitative synthesis modules

### Reproduced module 1 — Leal et al. 2025

Immutable dependency:

```text
commit: ed33b25593c0d90ad6657753f6f5501d9efc7b82
```

```text
female reproductive success  LRR -0.210  48 clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

Extreme heterogeneity and declared influence/dependence sensitivities remain explicit.

### Reproduced module 2 — Sasidharan et al. 2023

```text
florivore physiological detection   84/103
pollinator physiological detection 151/220
assembled risk difference            +0.129
LOCO direction                       positive 32/32
paired both-role components          3; all paired differences 0
```

The assembled contrast is not a causal paired consumer-role effect.

### Secondary contextual syntheses

These are not pooled with the two reproduced modules and their study/observation counts are not added to the 25 route clusters.

1. **Haas-Desmarais et al. 2026** — 171 studies / 1,348 study cases. Publisher supplement package independently retrieved and hashed. Herbivory is not relabelled focal floral `D`.
2. **Caruso et al. 2019** — main published analysis 755 gradients with SE from 36 articles. Dryad landing/API metadata and workbook identities verified; file-byte access currently blocked, so no false local-reanalysis claim is made.
3. **Junker & Blüthgen 2010** — 18 publications / 425 floral-scent observations. Visitor-dependence categories support consumer filtering but are not equated with pollinator-versus-antagonist roles.

## Manuscript-facing integration

PR #129 contains a complete candidate canonical integration:

- `README.md` synchronized to 56 / 25 / 14 / 17 / 7;
- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` updated in Part II only;
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md` Tables 3–4 synchronized;
- `manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg` regenerated from the saturated evidence state;
- bibliography expanded to 20 cited references and alphabetically ordered;
- cover letter, portal abstract, submission scope, audits, checklist, figure/table plan, and supplement manifest synchronized;
- Part I equations and numerical sensitivity outputs unchanged.

The main-text expansion is deliberately selective: representative systems illustrate new Pattern classes while the full study architecture remains in supplement ledgers/context programs.

## Reproducibility and vector-export state

The dedicated Pattern-expansion workflow passes the candidate contract, 56/25 readout regeneration, expanded Figure 3 generation, byte-reproducibility, submission narrative/scope checks, and 20-reference regressions.

A full figure-content checkpoint was then validated at:

```text
figure-content head: 8d0df837535efaf2d31a9909e9dac5cbbf492ea1
CI Python 3.10:      PASS
CI Python 3.11:      PASS
CI Python 3.12:      PASS
submission-scope:    PASS
EPS export:          PASS
workflow run:        31566025924
EPS artifact:        9129476142
artifact sha256:     014cc4f7d17541fb91d3637201013ccc391d7858a4d26779214294829e7cd27f
```

The export receipt is recorded in `submission/FIGURE_EXPORT_RECEIPT_V1.md`. Subsequent commits after that checkpoint are status/receipt/checklist text only and do not change the manuscript figures or evidence ledgers; they still undergo ordinary PR CI.

## Theory/empiricism boundary

```text
marginal route evidence != W_AD
same-system evidence != direct A x D
context-only programs != extra marginal-route N
secondary-synthesis study counts != route-ledger N
publication/study counts != model parameters
screened/deposit fractions != prevalence in nature
finite-grid occupancy != prevalence in nature
one direct A x D cluster != universal interaction sign
zero direct joint-cost studies != kappa = 0
herbivory treatment != focal D
whole-reproductive-module defence != flower-specific D unless the organ gate passes
```

## Remaining before external submission

Scientific evidence hunting and expanded-vector validation are closed. Remaining items are bounded formatting/archive and author-controlled submission information:

1. apply the final target-journal house style and one last citation consistency pass after author-controlled wording is frozen;
2. supply author order, affiliations, ORCIDs, CRediT, funding, acknowledgements, and competing-interest confirmation;
3. choose repository licence/licence statement;
4. create the final release/tag and archival DOI;
5. obtain all-author approval of the exact submission version;
6. upload through the authenticated journal portal.

## Merge decision

```text
scientific A-H gate:             PASS
Pattern expansion gate:         PASS / SATURATED
25-system manuscript package:   COMPLETE
candidate-specific CI:          GREEN
figure-content PR checks:        5/5 GREEN
expanded EPS export:            GREEN / digest recorded
PR #129:                        KEEP DRAFT pending author/licence/release decisions
PR #126:                        KEEP DRAFT; it remains the pre-expansion base
merge to main:                  NOT YET AUTHORIZED
portal submission:              NOT YET
```

If final source verification exposes a material evidence error or a genuinely new strict direct-design candidate, the relevant gate can be reopened. Otherwise, additional broad searching should not displace final packaging.
