# Final submission audit — canonical paperization state

## Audit purpose

This audit records the **current main-line scientific and submission state** for the Mechanism → Pattern paper. It is a live audit, not a historical PR receipt. Historical branch/PR chronology remains available in Git history and source-specific provenance files.

The canonical manuscript is:

> **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

The governing scientific claim is a **one-sided mechanistic theorem plus a recurrent but context-dependent empirical Pattern**.

## Integrated scientific spine

For one declared floral attraction trait `A`, one declared flower-specific antagonist-reducing trait `D`, and one declared outcome scale `W`, the local `A × D` mixed partial is interpreted only after explicit channel definitions and an orientation gate.

The signed bookkeeping identity is

```text
W_AD = M_AD - G_AD - C_AD
```

and, after orientation,

```text
W_AD = rho - iota - kappa
```

where `rho` is antagonist relief, `iota` is pollinator/mutualist interference, and `kappa` is direct joint-cost curvature. The identity is bookkeeping rather than the novelty.

The strongest result is one-sided:

```text
W_AD > 0  =>  rho > iota     when kappa >= 0
```

Thus complementarity cannot occur outside the selectivity window under non-negative joint-cost curvature. The converse is false: across the declared 2,592 evaluations, the forward implication has zero counterexamples, while window precision is 77.2% and approximately 23% of in-window evaluations remain substitutable. At `kappa = 0`, the window becomes the exact sign criterion.

Outside-window complementarity in the declared family requires negative joint-cost curvature and, for an actual violation, a value sufficiently negative relative to `rho - iota`. Direct joint-cost curvature has no strict empirical estimate in the admitted evidence layer, so `kappa` remains **unidentified**, not zero.

## Scientific completion gates

All registered scientific gates are closed for the present paper:

```text
Gates A-H:                    PASS
original completion gate:     PASS
Pattern expansion gate:       PASS / SATURATED
one-sided theorem regression: PASS
broad evidence searching:     NOT A DEFAULT BLOCKER
```

The canonical Pattern architecture remains:

```text
56 source-adjudicated route records
25 independent biological study clusters
A -> pollination:       5 clusters
A -> antagonism:        8
D -> antagonism:       18
D -> pollination:      10
same-system:           14 clusters
context/sign switch:   17 clusters
context-only programs:  7, excluded from route-ledger N
direct A x D:           1 strict cluster, sign unresolved
direct joint cost:      0 strict estimates; kappa unidentified
```

These counts document evidence capacity and recurrence, not prevalence in nature.

### Direct interaction and same-system evidence

The direct `A × D` search is saturated with one strict total reproductive-outcome cluster, *Impatiens capensis*, whose reproductive-component interactions remain sign-unresolved. Same-system recurrence is kept inferentially separate from a direct mixed partial.

A crossed floral-trait programme additionally shows consumer-context-dependent channel interaction signs, but those channel-specific contrasts are not promoted to a universal total `W_AD`.

### Quantitative module 1 — floral larceny

The Leal et al. (2025) reanalysis retains the canonical pooled log response ratios:

```text
female reproductive success  -0.210  48 independent clusters
nectar standing crop          -0.483  28
legitimate visitation         -0.291  22
```

For female fitness, 35/48 clusters are negative and the 95% prediction interval spans approximately `-1.13` to `+0.71`. Six declared moderators explain only 0–8% of the heterogeneity. The supported interpretation is therefore an antagonist-pressure gate that is open on average but not universal.

The apparent nectar → visitation → female-fitness sequence remains **constituent-path evidence** rather than an end-to-end mechanism: only five clusters measured all three outcomes, two showed all three negative, and the shared nectar-visitation subset has `r = -0.17`.

### Quantitative module 2 — floral volatiles

The Sasidharan et al. (2023) reconstruction retains the conservative 32-study-component topology. Physiological detection is 84/103 for florivore units and 151/220 for pollinator units; the assembled risk difference is `+0.129` and remains positive in 32/32 leave-one-study-component-out refits. Only three components contain both physiological roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect.

### Secondary contextual syntheses

Haas-Desmarais et al. (2026), Caruso et al. (2019), and Junker & Blüthgen (2010) remain secondary contextual/cross-synthesis modules. Their different scales and source-access states are preserved rather than pooled with the two reproduced modules or added to route-ledger N.

### Conditionality and saturation

The saturated Pattern records guarded defence, spatial/temporal/attack-mode filtering, consumer identity and functional-role dependence, visitor routing between legitimate pollination and robbery, lifecycle-stage role reversal, response-stage dependence, population/site dependence, and trait/compound-class dependence.

The registered expansion stopping rule was met after a new lifecycle-role class reset the counter and two subsequent distinct targeted batches produced no new admissible Pattern class. A parallel quantitative search produced no additional synthesis with a distinct theory-facing axis.

## Reproductive assurance boundary

Reproductive assurance `R` remains an auxiliary background moderator in the implemented corollary. Changing `R` from `0.0` to `0.5` changes the local sign in **16 of 1,296** otherwise matched scenario × response-shape evaluations.

`R` is not a third focal trait, and the manuscript must not be reframed as a **three-trait theory**.

## Theory–empiricism boundary

The active paper preserves:

```text
marginal route evidence
!= same-system evidence
!= direct A x D evidence
!= complete W_AD decomposition
```

Therefore:

- finite-grid occupancy is not prevalence;
- route counts are not prevalence;
- Leal pooled effects do not estimate `rho`, `iota`, `kappa`, or `W_AD`;
- Sasidharan's assembled contrast is not a causal paired-role effect;
- secondary-synthesis counts are not route-ledger N;
- zero strict joint-cost estimates do not imply `kappa = 0`;
- total `W_AD` alone does not identify channel allocation, trait covariance, genetic correlation, evolutionary trajectories, or equilibria.

## Reader-facing and visual QA

Repository-source reader QA is complete:

- title, Abstract, Introduction, Integration, and Conclusion are synchronized around the one-sided theorem;
- main-text callouts cover Figures 1–3, Tables 1–4, Supplementary Figures S1–S4, and Tables S1–S6;
- all seven main/supplementary figure sources were rendered and visually inspected;
- presentation collisions found in Fig. 2, Fig. S1, Fig. S2, and Fig. S4 were corrected and re-rendered;
- Figure 2 is now regenerated and diff-checked against its committed SVG in the active theory-validation workflow;
- Supplementary Figures S1–S4 and Tables S1–S6 are rebuilt on the current PR state and diff-checked against committed assets.

These are presentation/reproducibility changes only; no scientific value was altered.

## Current submission decision

**Scientific conclusion: GO / FROZEN. Reader-facing repository-source QA: PASS. External journal submission: NOT YET.**

Remaining blockers are human/release controlled rather than scientific:

1. final author order/publication names, affiliations, corresponding author, e-mail, ORCIDs, and CRediT roles;
2. funding/acknowledgements and competing-interest confirmation;
3. repository licence/licence statement;
4. exactly five conflict-checked reviewer suggestions and any justified exclusions;
5. all-author approval and confirmation that the manuscript is not under consideration elsewhere;
6. freeze the exact final release commit and create an immutable release/tag;
7. archive the release and insert its DOI;
8. rerun final CI, submission-scope, figure export, supplement rebuild/diff, and reference checks from that release commit;
9. render and visually inspect the final release-version manuscript and supplementary upload files;
10. submit through the authenticated journal portal.

The governing rule remains: improve presentation and reproducibility while keeping the distinction between **theoretical mixed curvature** and **empirical constituent-path Pattern evidence** explicit. New broad discovery is out of scope unless the frozen claim is specifically falsified or a concrete provenance/reviewer issue requires correction.
