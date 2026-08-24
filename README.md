# Biotic Interaction Trait Architecture

A reproducible **Mechanism → Pattern** study of when one focal floral attraction trait (`A`) and one focal flower-specific antagonist-reducing trait (`D`) are locally complementary or substitutable on a declared outcome scale (`W`). The repository couples a **fixed theoretical core** to a **mechanism-pattern empirical synthesis** while keeping the two inferentially separate: Part II tests recurrence, gate opening, switching, and identification gaps rather than relabelling marginal evidence as the total mixed partial.

## Scientific result

After an explicit orientation gate, the local mixed partial is organized as

```text
W_AD = rho - iota - kappa

rho   = antagonist-relief magnitude
iota  = pollinator-interference magnitude
kappa = direct joint-cost curvature
```

The decomposition is bookkeeping, not the main novelty. The strongest structural result is one-sided:

```text
if kappa >= 0 and W_AD > 0, then rho > iota
```

So **complementarity cannot occur outside the selectivity window** where antagonist relief exceeds pollinator interference. Across the declared 2,592 endpoint-normalized evaluations and four response-shape variants there are zero counterexamples. The converse is false: window precision is 77.2%, so about 23% of in-window evaluations remain substitutable. At zero joint cost the window becomes the exact sign criterion.

The bound has one escape route in the declared family: joint-cost curvature must be negative, and sufficiently negative, for complementarity to occur outside the window. Direct `c_AD` is not measured in the strict empirical layer, making its sign the minimal biological applicability/falsification gate for the theorem.

## Cross-system Pattern

Part II asks whether the mechanism classes derived in Part I recur in nature without forcing incompatible outcomes into one grand effect size. The saturated source-adjudicated architecture contains:

```text
56 route-level records
25 independent biological study clusters
A -> pollination:        5 clusters
A -> antagonism:         8
D -> antagonism:        18
D -> pollination:       10
same-system multi-route:14
context/sign switch:    17
context-only programs:   7  (excluded from route-ledger N)
```

The cross-system conclusion is:

> **recurrent constituent mechanisms + context-dependent balance inside a one-sided selectivity window**

The Leal et al. floral-larceny reanalysis shows that antagonist pressure can be costly on average (female-fitness LRR about `-0.210`, 48 independent clusters), but the sign is not universal: 35/48 clusters are negative and the 95% prediction interval spans approximately `-1.13` to `+0.71`. Declared moderators explain only 0–8% of the heterogeneity. The antagonist-pressure gate is therefore open on average but its location is not yet predictable from the tested coarse context axes.

The apparent nectar → visitation → female-fitness sequence is retained only as constituent-path evidence, not as a demonstrated within-study causal chain. Direct total `A × D` evidence remains sparse, and direct joint-cost curvature remains unidentified rather than zero.

## Canonical paper

The manuscript is now the repository's scientific source of truth:

- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` — canonical article text
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md` — main tables
- `manuscript/figures/` — canonical main-figure sources
- `manuscript/supplementary/` — reproducible supplementary material
- `docs/MECHANISM_PATTERN_STORY_BOUNDARY.md` — frozen story boundary
- `docs/NOVELTY_POSITIONING.md` — novelty and non-novelty boundary
- `docs/SELECTIVITY_WINDOW_BOUND.md` — theorem statement and falsification logic
- `docs/REPOSITORY_STRUCTURE.md` — source-of-truth and archive policy

The paper is deliberately split into:

```text
Part I — Mechanism
local theory / non-identifiability / one-sided bound / finite sensitivity

Part II — Pattern
meta-analysis / cross-study recurrence / switching / identification gaps
```

The intended argument is **Mechanism → Pattern**, not “theory → empirical validation.” Part II establishes recurrence and conditionality of the constituent biology; it does not calibrate or validate a universal total `W_AD`.

## Reproducibility core

Core model and theorem implementation:

- `trait_architecture/model.py`
- `trait_architecture/sign_criterion.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `tests/test_selectivity_bound.py`

Canonical manuscript-facing reproduction scripts include the Part I robustness run, empirical mechanism-coverage/readout builders, Leal and Sasidharan reconstruction/sensitivity code, supplementary builders, and figure export scripts under `scripts/`.

Important distinction: source-recovery and audit scripts are retained as provenance when they support an admitted empirical module, but one-off scripts that only mutated manuscript prose or relabelled already-frozen figures are not part of the scientific reproduction path.

Repository graph integrity is guarded by
`tests/test_repository_graph_integrity.py`: active Python surfaces may not
import retired local modules, workflows may not call missing scripts, and active
workflows may not write to retired research branches.

## Inference boundaries

The repository must preserve these distinctions:

```text
marginal route evidence
!= same-system evidence
!= direct A x D evidence
!= complete W_AD decomposition
```

Therefore:

- route counts are not prevalence estimates;
- finite-grid fractions are not probabilities of natural regimes;
- Leal pooled effects do not estimate `rho`, `iota`, `kappa`, or `W_AD`;
- Sasidharan's assembled contrast is not a causal within-study consumer-role effect;
- a direct channel interaction is not automatically total `W_AD`;
- zero strict joint-cost studies means `kappa` is unidentified, not zero;
- `W_AD` does not by itself predict trait covariance, genetic correlation, an evolutionary trajectory, or a stable optimum.

## Current research boundary

The scientific story is considered closed for this paper. Additional broad evidence searching is not a default blocker. The next empirical programme generated by the paper has two distinct tests:

1. **Applicability/falsification gate:** a 2 × 2 allocation design (`neither`, `A only`, `D only`, `A + D`) to determine the sign of joint-cost curvature.
2. **Full calibration:** a harder `A × D` factorial with mutualist, antagonist, direct-cost, and total-fitness outcomes to estimate total interaction and channel allocation.

## Submission state

The repository is in paperization mode. Scientific conclusions are frozen; current work should focus on manuscript clarity, reviewer-risk reduction, reproducible submission assets, and author-controlled metadata. Author order, affiliations, ORCIDs, CRediT roles, funding, competing interests, repository licence, archival DOI, and authenticated journal submission remain human-controlled release items and must not be guessed.
