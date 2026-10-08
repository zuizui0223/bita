# Gate A corrected final decision — source-defined behavior states

Status: **GATE A FAILED, confirmatory escalation stopped.**
Prepared: 2026-10-08.
Scope: analysis-only branch `analysis/ecological-stability-evolutionary-transience-v1`.
No changes to the Ecology Letters primary Letter or main branch.

## Outcome-run provenance

**Source-faithful corrected run (the decision run):**
- workflow https://github.com/zuizui0223/bita/actions/runs/37642072241
- head commit `1a3d353ec7`
- artifact https://github.com/zuizui0223/bita/actions/runs/37642072241/artifacts/11493771125
- completed successfully (source-count audit and trait/covariate mapping passed).

**Superseded initial uncorrected run:**
- https://github.com/zuizui0223/bita/actions/runs/37639638223
- originally mixed the 10 on-wing-only piercing species into the orthodox reference group.
- its original numerical output and `GATE_A_FIRST_OPEN_KILL_RECEIPT_V1.md` are retained strictly as an audit trail, not authoritative primary conclusions.

## Exact source class partition (Colwell et al. 2023)

- 220 species total
- 66 clingers
- 144 presumed orthodox hover-feeders
- 10 non-clinging pierce-while-hovering species
- 44 species with source-documented bypass behavior under secondary state coding

The corrected primary contrast uses only clingers versus presumed orthodox
hover feeders; the 10 on-wing piercers are **not** coded as orthodox.

## Gate A corrected results

- Barreto speciation source: 362 species; Colwell overlap: 178 species.
- Overlap contains 64 clingers, 105 presumed orthodox, and 9 on-wing-only piercers.
- Primary complete-case n = 159 species per eligible estimator.

| Test | Standardized clinger coefficient | One-sided within-clade permutation p |
|---|---:|---:|
| BAMM Lambda McGuire | -0.02028779422349938 | 0.1229 |
| ClaDS Lambda McGuire | -0.14091013293164284 | 0.0937 |
| Median (2 estimator families) | -0.08059896357757111 | Not a pooled p |
| Median excluding Coquettes | **+0.02083887160371186** | Not a pooled p |

Secondary bypass state (a more direct measure of source-documented
flower-opening use): median coefficient **+0.018383508599939292**
(0/2 estimator families negative). Excluding Coquettes:
**+0.06896256639727304**.

Frozen decisions from the successful corrected run:

~~~text
gate_a_pass                     = false
cross_scale_cheating_claim_eligible = false
decision = KILL_TRANSIENCE_HYPOTHESIS_UNDER_FROZEN_GATE
~~~

## Biological interpretation

The primary predicted negative clinger association is not supported robustly.
The sign turns positive when Coquettes are removed. In the biologically closer
bypass phenotype, the prediction has the opposite sign already at the full-data
point estimate. This does not prove equivalent rates, higher rates, or a causal
effect of cheating on diversification.

**Important distinction:** Clinging is not the same ecological role as cheating.
Colwell's state includes legitimate clinging, whereas bypass-capable records
measure capacity, not actual route-use frequency. Duchenne et al. (2023)
modelled ecological **community** persistence, not clinger lineage
diversification. These quantities cannot be called direct cross-scale
observations of the same process.

## Decision and next permissible route

1. **Stop** the tested clinger/bypass diversification paradox. No Gate B or
   post-hoc dependent-variable substitution to force a positive result.
2. **Preserve** this analysis branch and both immutable workflow artifacts.
3. **Preserve** primary access-routing Letter. This failed side-hypothesis
   is not evidence against its independently established descriptive results.
4. A new non-obvious ecological prediction needs a separate literature
   falsification audit and its own preregistered, truly independent outcome
   test before any promotion.

Relevant primary literature:
- Colwell et al. 2023, doi:10.1086/726036
- Barreto et al. 2023, doi:10.1098/rspb.2022.1793
- Duchenne et al. 2023, doi:10.1371/journal.pbio.3002434
