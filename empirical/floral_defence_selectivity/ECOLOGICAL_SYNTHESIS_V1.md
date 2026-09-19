# BITA ecological synthesis v1

## Active biological claim

> **Floral interaction architecture is governed by access and exposure domains: separation can preserve mutualistic function while suppressing antagonists, overlap can impose mutualist costs, increasing exposure can close the selective window, and inaccessible rewards reroute cheating toward bypass rather than eliminating exploitation.**

This is the ecological main line of the refocused BITA. It replaces the warning-style headline without deleting the earlier identification work.

## Evidence layer 1 — broad D-side route macro corpus

After deduplicating the repeated Takeda 2021 study identity, the legacy D-side evidence contains 17 unique study programs:

~~~text
chemical      9
physical      7
reward/access 1

antagonist EFFECTIVE   16
antagonist UNRESOLVED   1
~~~

Ten of the 17 programs also contain same-study D-to-pollination evidence.

~~~text
CONTEXT_DEPENDENT  4
NULL_COMPATIBLE    3
IMPROVED           1
INTERFERENCE       1
UNRESOLVED         1
~~~

Pollinator-side follow-up is unevenly distributed:

~~~text
chemical  7 / 9
physical  2 / 7
Fisher p = 0.1262
~~~

Interpretation: the broad D-side corpus establishes implementation breadth and heterogeneous mutualist consequences. It also reveals a study-design gap: physical defences are common in antagonist studies but rarely receive pollinator-side follow-up comparable to chemical systems.

These counts are not prevalence estimates because D-role admission depends on antagonist-reduction evidence.

## Evidence layer 2 — same-defence matched systems

Current matched-D corpus:

```text
independent systems:               17
effective antagonist route:        15
strict direct Stage-2 systems:      3
null-compatible Stage-2 systems:    4
transition systems:                 4
explicit bypass/null-D system:      1
```

Broader macro state-recovery pattern:

~~~text
historical derivation:
  9 / 9 scorable systems match the fixed domain-state rule

systematic expansion:
  2 / 2 scorable systems match the fixed domain-state rule

pooled scored:
  11 / 11
~~~

Fixed mapping:

~~~text
SEPARATED    -> NO_INTERFERENCE_OBSERVED
TRANSITIONAL -> MIXED
OVERLAPPED   -> IMPAIRED
~~~

A coarse modality-only leave-one-out classifier recovers 6/9 historical systems, and the derivation modality rule recovers 1/2 systematic-expansion systems.

Historical exact fixed-margin perfect-allocation probability: 1/630 = 0.0015873.
Pooled historical + expansion fixed-margin perfect-allocation probability: 1/2310 = 0.0004329.

These are descriptive alignment probabilities, not confirmatory p-values, because historical systems contributed to theory formation. NO_INTERFERENCE_OBSERVED includes null-compatible outcomes and does not mean equivalence-supported preservation.

Strict direct pattern:

```text
SEPARATED:  2 preserved/improved, 0 impaired
OVERLAPPED: 0 preserved/improved, 1 impaired
```

Four additional separated systems are null-compatible for pollinator change rather than equivalence-supported preservation. They are kept separate from the strict binary result.

Interpretation: the broader ecological-state analysis shows a sharp domain-state organization across all 11 currently scorable historical + expansion systems. The strict cross-system sample remains too small for a high-dimensional moderator model. Exact analysis gives Fisher two-sided p = 0.333 for the strict 2×2 table. A sensitivity that groups four null-compatible separated systems with the compatible side gives p = 0.143, but null compatibility is not equivalence. In the strict subset, domain relation and broad defence modality are perfectly confounded, so the current data cannot show that domain structure explains more than chemical-versus-physical class.

## Evidence layer 3 — within-system state switching

Eight independent defence-side conditionality clusters show that the same nominal defence/access axis changes realised state with dose, exposure duration, reward context, consumer identity, response stage, or temporal expression.

Four ordered exposure systems particularly support a selective-window pattern in which antagonist response can occur before strong pollinator interference, and the window closes as exposure increases.

Interpretation: selectivity is a **state of trait × consumer × context**, not a fixed property of a chemical or physical defence category.

## Evidence layer 4 — independent community-scale routing

Sakhalkar et al. 2023 provides an independently assembled Afrotropical community dataset. The BITA reanalysis aggregates visits to plant species and tests whether floral tube length predicts the balance between two cheating routes.

```text
analysed visit records: 14,383
visited species:          183
cheating species with tube length: 57

Spearman rho(tube length, robbing-vs-thieving balance) = 0.346786
two-sided permutation p = 0.0086

median tube length:
  robber-only = 2.0893
  thief-only  = 0.6766
```

Interpretation: increasing tube length is associated with more **robbing/bypass** relative to **thieving through the normal opening**. A source-defined multitrait sensitivity does not isolate tube length as a unique partial predictor (full-model permutation p = 0.202; tube-length block p = 0.211), so the broader conclusion is that floral access geometry is associated with interaction routing at community scale rather than that tube length alone is causal.

## Preserved earlier BITA results

The refocus does not discard the previous theory or empirical work:

- 56 directional route records / 25 independent biological clusters;
- 17-system high-information identification audit;
- direct and near-direct A×D results;
- Kessler interaction bounds and partial identification;
- Kessler 2015 consumer-context sign switching;
- larceny quantitative synthesis;
- identification ladder and crossed-intervention design logic.

Kessler 2015 is retained as a bridge/sensitivity result and does not inflate the 17-system matched-D count.

## What is now nontrivial

The paper no longer argues merely that `interaction != mechanism`.

It now has four linked ecological observations:

1. **route-level breadth** — 17 unique D study programs span chemical, physical and reward/access implementations, with heterogeneous pollinator consequences in the 10 same-study follow-ups;
2. **state-recovery pattern** — 9/9 historical and 2/2 systematic-expansion systems fall into the predicted separated / transitional / overlapped pollinator-state families;
3. **switching rule** — the same D changes state with exposure, consumer and response stage;
4. **network consequence** — access geometry predicts which exploitation route animals use across a multispecies community.

The common ecological candidate is **effective access/exposure domain**. Recurrence across chemical, physical and reward-access implementations argues against treating one defence class as the whole explanation, but a formal domain-versus-modality comparison is not yet identified in the strict Stage-2 subset.

## Current claim ceiling

Supported now:

> access/exposure structure is a recurrent organizer of floral antagonist–mutualist outcomes and exploitation mode across case-level, within-system and community-scale evidence.

Not yet licensed:

- a universal causal coefficient for domain separation;
- a prevalence estimate for selective floral defence;
- a pooled effect size across heterogeneous biological outcomes;
- a claim that all layers identify one microscopic mechanism;
- a final high-dimensional matched-D meta-regression.

## Next decisive task

Continue focused matched-D retrieval only if it fills strict Stage-2 cells. Do not reopen broad literature harvesting.

The main cross-system result is now the 11-system state-recovery analysis. Additional independent **OVERLAPPED + direct pollinator outcome** and **SEPARATED + direction-supported pollinator outcome** systems remain the priority for converting the high-specificity Stage-2 subset into a formal moderator test. The Sakhalkar network result is analysis-complete and should remain in the main Results.
