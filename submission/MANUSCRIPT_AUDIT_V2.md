# Manuscript audit v5 — saturated Mechanism → Pattern pre-submission check

## Verdict

**YES: the PR #129 candidate is structurally and inferentially a two-part paper: fixed mathematical Mechanism first, saturated meta-analytic Pattern second.**

Current order:

```text
1 Introduction
2 Part I — Mechanistic theory: mechanism and principle
3 Part I results — mechanistic sign regimes
4 Part II — Meta-analysis and cross-study pattern synthesis
5 Part II results — meta-analytic patterns across systems
6 Integration — from mechanism to pattern
7 Conclusions
```

## Part I — Mechanism: PASS / unchanged

Part I retains:

```text
W_AD = M_AD - G_AD - C_AD
orientation gate:
M_AD <= 0, G_AD <= 0, C_AD >= 0
W_AD = rho - iota - kappa
W_AD > 0 iff rho > iota + kappa
```

Also unchanged are the focal A/D/outcome declarations, Proposition 1 non-identifiability, environmental derivative balances, break-even inequalities, and the canonical 2,592-evaluation endpoint-normalized sensitivity analysis.

Figures 1–2 and Tables 1–2 remain the Mechanism half. No theory equation, parameter, theorem, or Part I numerical result was changed to obtain the expanded Pattern synthesis.

## Part II — Pattern: PASS as saturated candidate

Part II asks which mechanism-derived Patterns recur across systems and where ecological state changes the realised balance.

### Reproduced meta-analysis 1 — Leal et al. 2025: PASS

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

Direction survives declared sensitivity/influence checks and extreme heterogeneity remains part of the result.

### Reproduced synthesis 2 — Sasidharan et al. 2023: PASS with paired-role boundary

```text
florivore physiological detection  84/103
pollinator physiological detection 151/220
assembled risk difference           +0.129
LOCO direction positive             32/32
```

Only three components contain both physiological roles and all three paired differences are zero. The assembled contrast is not a causal within-study pollinator-versus-florivore effect.

### Secondary contextual syntheses: PASS with status separation

- **Haas-Desmarais et al. 2026:** published 171 studies / 1,348 cases; publisher supplement package verified, no local raw-effect reconstruction claim; herbivory is not focal D.
- **Caruso et al. 2019:** published main analysis 755 gradients with SE / 36 articles; Dryad metadata/workbook identity verified but file bytes currently blocked; selection gradients are not `W_AD`.
- **Junker & Blüthgen 2010:** 18 publications / 425 floral-scent response observations; resource dependence is not identical to pollinator-versus-antagonist identity.

These modules broaden recurrence/context evidence without being pooled with the two reproduced quantitative modules or added to route-ledger N.

### Saturated theory-to-Pattern scaffold: PASS

```text
56 source-adjudicated route records
25 independent biological study clusters
A -> pollination    5 clusters
A -> antagonism     8
D -> antagonism    18
D -> pollination   10
same-system        14
context switches   17
context-only programs 7, excluded from route N
direct A x D        1 strict cluster, sign unresolved
direct joint cost   0 strict estimates
```

The scaffold is deliberately **not** pooled into one grand effect. Route-specific counts overlap and are not additive study totals or prevalence estimates.

### Pattern-class expansion: PASS

The expanded candidate moves beyond a five-bin conditionality summary. It explicitly records:

- guarded defence;
- spatial / temporal / body-size / attack-mode filtering;
- visitor functional-mode routing between legitimate pollination and robbery;
- lifecycle-stage mutualist/antagonist role reversal;
- response-stage, resource/exposure, consumer, population/site, trait-class, and compound/mechanism dependence.

Representative examples are kept in the main text; the full system list remains in supplement ledgers/context programs.

### Expansion saturation: PASS

Batch 7 found a new lifecycle-stage role-reversal class, resetting the stopping counter. Batches 8 and 9 then used distinct candidate sets and produced no new admissible Pattern class. The parallel quantitative search found no sixth synthesis with a distinct theory-facing axis. This satisfies the registered expansion stopping rule.

## Mechanism → Pattern linkage: PASS

The manuscript now reads as:

```text
derive mechanism
→ derive conditional predictions
→ quantify compatible cross-study effects
→ map saturated recurrence and conditionality without cross-outcome pooling
→ identify direct interaction and joint-cost gaps
```

The supported cross-system conclusion is:

> **recurrent constituent mechanisms + context-dependent balance**

not a universal positive or negative `W_AD`.

## Inference-boundary audit: PASS

```text
marginal route evidence != W_AD
same-system evidence != direct A x D
context programs != extra route N
secondary-synthesis study counts != route N
route counts != prevalence
finite-grid occupancy != prevalence
Leal pooled effects != rho/iota/kappa
Sasidharan assembled contrast != causal paired role effect
herbivory treatment != focal D
whole reproductive-module defence != strict flower-specific D without organ gate
zero joint-cost studies != kappa = 0
```

## Figure/table audit: PASS as candidate

- Figures 1–2 / Tables 1–2 remain Mechanism.
- Figure 3 / Tables 3–4 now use the saturated 56/25 evidence universe.
- Figure 3 is generated from canonical + expansion ledgers and explicitly shows 14 same-system clusters, 17 switch clusters, seven context programs, two reproduced modules, three secondary syntheses, and the direct-identification boundary.
- Quantitative robustness panels remain Supplementary Figure S4.

## Reference audit: PASS as candidate

The manuscript bibliography has expanded from the earlier 13-entry spine to **20 cited entries**. The new entries cover the representative expansion systems and the three secondary syntheses. Known Stevenson metadata corrections and legacy-reference pruning remain protected by regression tests. Final journal-house formatting remains pending.

## Reviewer-facing assessment

The strongest contribution is the **Mechanism → Pattern connection**:

- a local mathematical mechanism gives a conditional sign principle;
- two reproduced quantitative syntheses establish recurrent constituent effects and strong heterogeneity/context dependence;
- a saturated 25-system source-adjudicated scaffold demonstrates recurrence across distinct signal and defence mechanisms;
- same-system and conditionality evidence reveals guarded, filtered, functional-mode, and lifecycle-dependent states;
- direct interaction and joint-cost evidence remain sparse exactly where the mathematical decomposition says identification requires them.

The expansion strengthens empirical generality without converting the paper into an omnibus prevalence survey.

## Remaining non-scientific / package blockers

- complete PR workflow suite must pass on the exact final expanded head;
- EPS Figures 1–3 must be regenerated from that exact head and provenance recorded;
- final author order/publication names and affiliations;
- corresponding author/email and ORCIDs;
- CRediT, funding, acknowledgements, competing-interest confirmation;
- repository licence choice;
- final target-journal reference/house style;
- exact release/tag and archival DOI;
- authenticated journal portal submission.

## Decision

```text
Mechanism half:                 PASS
saturated Pattern half:         PASS
Mechanism -> Pattern link:      PASS
registered expansion gate:      PASS / SATURATED
candidate-specific CI:          PASS
full exact-head PR CI:          pending final validation
expanded exact-head EPS:        pending final validation
scientific submission gate:     GO
portal submission:              not yet
```
