# Mechanism-pattern synthesis completion status v3

## Scope and source of truth

This file records the scientific state of the fixed Mechanism paper plus the saturated Pattern-expansion candidate.

Repository lines:

```text
canonical integration PR:   #126
canonical branch:           agent/mechanism-pattern-universality-v1
expanded candidate PR:      #129
expanded candidate branch:  analysis/pattern-expansion-v1
```

Part I theory remains fixed. PR #129 changes the Part II evidence capacity and manuscript-facing Pattern synthesis; it does not change any equation, theorem, theoretical parameter, or finite-sensitivity result.

## A–H scientific gate

| Gate | Status | Basis | Expansion effect |
|---|---|---|---|
| **A — direct `A x D`** | **PASS as bounded gap** | `DIRECT_AXD_SATURATION_RECEIPT_V1.md` | unchanged: one strict cluster, sign unresolved |
| **B — four marginal mechanism families** | **PASS** | canonical ledgers + `EXPANSION_LEDGER_BATCH_*_V1.csv` | saturated route evidence expands to 25 independent systems |
| **C — quantitative modules** | **PASS** | Leal 2025 + Sasidharan 2023 reproduced modules | three additional secondary contextual syntheses retained with different status |
| **D — conditionality** | **PASS** | canonical + expansion sign-switch ledgers and context programs | expands to 17 sign/state-switch clusters plus 7 context-only programs |
| **E — same-system linkage** | **PASS** | canonical + expansion route ledgers | expands to 14 same-system multi-route clusters |
| **F — direct joint cost** | **PASS as documented gap** | `JOINT_COST_SATURATION_RECEIPT_V1.md` | unchanged: zero strict estimates; `kappa` unidentified |
| **G — robustness/bias** | **PASS** | reproduced-module audits + source/access receipts | expansion keeps evidence-status and source-access distinctions explicit |
| **H — theory/empiricism boundary** | **PASS** | boundary audit + manuscript/figure/table regression tests | 25-system candidate retains all inference prohibitions |

## Saturated Pattern architecture

The final candidate source-adjudicated route architecture is:

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

The expansion was not an exercise in maximizing article count. It targeted weak or empty mechanism/context cells under the same focal-trait and flower-specific-defence rules.

### Attraction-side recurrence

Independent signal systems now include volatile, visual-bract, colour, and multidimensional colour/scent axes. New examples include *Dalechampia scandens*, *Raphanus sativus*, and a recombinant *Silene latifolia × S. dioica* signal system linking floral sensory dimensions to antagonist host choice.

### Flower-specific defence diversity

Independent D systems now include:

- water-filled bracts/calyces;
- floral surface stickiness;
- slippery epicuticular wax;
- dense petal hairs;
- spur-enclosing floral bracts;
- floral nectar chemistry.

These are counted at independent study-cluster level rather than per species, population, treatment cell, or assay.

### New recurrent state classes

The expanded Pattern matrix now makes explicit:

- **guarded defence** — antagonist reduction without a universally detected pollinator penalty;
- **spatial / temporal / attack-mode filtering** — defence works only for particular access routes, consumer sizes, attack modes, or reproductive windows;
- **pollinator functional-mode routing** — the same visitor can shift between legitimate pollination and robbery without a change in taxonomic identity or arrival rate;
- **lifecycle-stage role reversal** — one consumer taxon can be a mutualist at one life stage and an antagonist at another;
- response-stage, resource/exposure, trait-class, population/site, and compound/mechanism dependence.

## Registered expansion stopping gate

`PATTERN_EXPANSION_COMPLETION_GATE_V1.md` records the stopping decision.

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

Canonical Patterns:

```text
female reproductive success  LRR -0.210  48 clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

Extreme heterogeneity and declared influence/dependence sensitivities remain explicit.

### Reproduced module 2 — Sasidharan et al. 2023

Canonical dependence topology: 32 study components.

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

1. **Haas-Desmarais et al. 2026** — published multilevel meta-analysis, 171 studies / 1,348 study cases. Publisher supplement package independently retrieved and hashed. Herbivory treatment is not relabelled as focal floral `D`.
2. **Caruso et al. 2019** — published selection meta-analysis; main uncertainty-bearing analysis uses 755 gradients with SE from 36 articles. Dryad landing/API metadata and workbook identities verified; current file-byte access is blocked, so no false local-reanalysis claim is made.
3. **Junker & Blüthgen 2010** — 18 publications / 425 floral-scent response observations. Visitor-dependence categories support consumer filtering but are not equated with pollinator-versus-antagonist roles.

## Manuscript-facing integration

PR #129 now contains a complete **candidate canonical integration**, not only exploratory ledgers:

- `README.md` synchronized to 56 / 25 / 14 / 17 / 7;
- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` updated in Part II only;
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md` Tables 3–4 updated;
- `manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg` regenerated from the saturated evidence state;
- bibliography expanded to 20 cited references and alphabetically ordered;
- Part I equations and numerical sensitivity outputs unchanged.

The main-text expansion is deliberately selective: representative systems illustrate new Pattern classes, while the full study architecture remains in the supplement ledgers/context programs.

## Reproducibility state

Dedicated Pattern-expansion workflow at the 25-system candidate successfully completed:

```text
Pattern expansion contract             PASS
56/25 readout regeneration             PASS
expanded Figure 3 generation           PASS
Figure 3 byte-reproducibility          PASS
submission narrative regressions       PASS
submission scope regressions           PASS
20-reference manuscript regressions    PASS
```

The candidate still requires a clean run of the full pull-request workflow suite and a fresh EPS export from the exact final expanded figure commit before it is called a final submission checkpoint.

## Theory/empiricism boundary

The candidate package regression-tests the following:

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

Scientific evidence hunting is closed under the registered saturation rule. Remaining work is package validation and author-controlled submission information:

1. pass the complete PR workflow suite on the exact expanded candidate head;
2. export Figures 1–3 to EPS from the exact expanded candidate head and record artifact provenance;
3. run the final citation/formatting pass against the exact target-journal style;
4. supply author order, affiliations, ORCIDs, CRediT, funding, acknowledgements, and competing-interest confirmation;
5. choose the repository licence/licence statement;
6. create the final release/tag and archival DOI;
7. upload through the authenticated journal portal.

## Merge decision

```text
scientific A-H gate:          PASS
Pattern expansion gate:      PASS / SATURATED
25-system manuscript package: COMPLETE AS CANDIDATE
candidate-specific CI:       GREEN
full PR CI:                  PENDING EXACT-HEAD VALIDATION
expanded EPS export:         PENDING EXACT-HEAD VALIDATION
PR #129:                     KEEP DRAFT until full-package validation
PR #126:                     KEEP DRAFT; do not claim it contains 56/25 until PR #129 is promoted
merge to main:               NOT YET
portal submission:           NOT YET
```

If final source verification exposes a material evidence error or a genuinely new strict direct-design candidate, the relevant gate can be reopened. Otherwise, additional broad searching should not displace final package validation.
