# Floral defence selectivity — premodel ecological readout v1

## Status

This is a reproducible **premodel ecological readout** from the current matched-D corpus.

It is not yet the final macro-regression because the strict Stage-2 binary lane remains sparse. Its purpose is to state the observed ecological pattern before adding more systems or fitting a higher-dimensional model.

Authoritative machine-readable summary:

`results/premodel_pattern_summary.json`

## Current corpus

```text
independent matched-system clusters: 17
strict EFFECTIVE defence clusters:    15
strict Stage-2 clusters:               3
null-compatible Stage-2 systems:       4
transition systems:                    4
bypass/null-defence systems:           1
```

Cohorts remain separated:

```text
historical derivation:       14
hold-out:                     1
systematic expansion:         2
```

## Result 1 — the strict direct Stage-2 pattern is directionally aligned with effective-domain separation

Among effective-defence systems with a direct, direction-supported pollinator state:

```text
SEPARATED domains
    pollination preserved/improved: 2
    pollination impaired:           0

OVERLAPPED domains
    pollination preserved/improved: 0
    pollination impaired:           1
```

The two separated strict systems are `Thunia alba` and `Caryopteris divaricata`.

The overlapped strict interference system is the high-gelsemine `Gelsemium sempervirens` state.

This is the first compact ecological pattern for the refocused paper, but **n = 3 is too small for the final comparative model**.

## Result 2 — four additional separated systems show no detected pollinator change, but they are not equivalence evidence

Four effective separated systems have a source-supported antagonist effect plus a null-compatible pollinator contrast:

- `Catalpa speciosa`;
- `Pedicularis rex`;
- `Ipomopsis aggregata`;
- `Phlox paniculata`.

These systems strengthen the qualitative non-impairment pattern, but they remain:

```text
NO_DETECTED_CHANGE
!=
PRESERVED_OR_IMPROVED
```

They therefore do not increase the strict Stage-2 count.

## Result 3 — state transitions recur within defence systems

All four currently coded `TRANSITIONAL` systems show a mixed pollinator state across dose, exposure duration, or response stage:

- `Polemonium viscosum`;
- `Aconitum lycoctonum`;
- `Asclepias` spp.;
- `Nicotiana attenuata` 2007.

This supports the ecological proposition that selectivity is not an immutable property of a defence class. A system can move from guarded/null-compatible to pollinator-interfering as exposure or response stage changes.

The transition result is retained as a separate outcome class rather than forced into the strict binary Stage-2 model.

## Result 4 — bypass predicts failure of the focal antagonist-reduction route

The current explicit `BYPASS_TOLERANCE` boundary is `Salvia`, where the putative barrier can be bypassed and the focal antagonist response is null-compatible.

This is consistent with the Stage-1 prediction that a conspicuous floral structure is not an effective defence when the antagonist does not have to traverse its effective domain.

One boundary system is not a prevalence estimate; further bypass/tolerance systems are still needed.

## Result 5 — the first independent hold-out points in the predicted direction but is deliberately not promoted

The 2026 `Erica` hold-out was coded as geometrically separated before using its focal outcome direction.

The source reports:

```text
longer corolla -> lower bee robbing
longer corolla -> positive pollination-rate direction
```

The pollination estimate lies at the source-reported significance boundary and is therefore coded `DIRECTION_ONLY / UNRESOLVED`, not strict preservation.

Thus the hold-out is directionally consistent with the rule but does not close the confirmatory gate.


## Result 6 — independent community-scale access routing is quantitatively supported

The Sakhalkar et al. 2023 public network dataset provides an external scale check that is independent of the matched-D case compilation.

After source-script cleaning, the deposited workbook contains 14,383 analysed visit records across 183 visited plant species. Species-level aggregation avoids treating visits as independent biological replicates.

For 57 cheating-exposed plant species with tube-length data:

```text
tube length vs cheating-mode balance:
Spearman rho = 0.346786
permutation p = 0.0086

median tube length:
robber-only species = 2.0893
thief-only species  = 0.6766
```

where cheating-mode balance is `(robbing - thieving)/(robbing + thieving)` using source-normalized visitation frequencies.

This independently supports the access-routing prediction: longer, less directly accessible flowers shift exploitation toward bypass by **robbing**, whereas more accessible flowers permit more **thieving through the legitimate opening**.

This network result does not estimate defence efficacy or pollinator cost, so it is not counted as another matched-D cluster.
## Ecological interpretation at the current evidence ceiling

The current corpus is better summarized as:

> **Defence selectivity tracks ecological access and exposure structure more closely than a fixed chemical-versus-physical dichotomy. Separated systems repeatedly retain pollinator-compatible states, overlapping high-exposure systems can impose pollinator costs, transitional systems switch state with exposure or response stage, and bypass can eliminate the focal antagonist-reduction function.**

This statement is still a structured comparative result, not the final cross-system causal estimate.

## Why this is not the old warning paper

The result is no longer:

```text
trait interaction != mechanism
```

The active empirical target is:

```text
effective-domain architecture
-> realised defence efficacy
-> pollinator cost state
```

The old identification framework remains preserved as the reason for requiring matched same-D evidence, explicit uncertainty states, and independent provenance.

## Prior-art ceiling

The paper must not claim novelty for the generic fact that floral cues can attract pollinators and repel other visitors, or that herbivory can alter pollination.

The novelty target is the **paired same-defence cross-system explanation**:

> which ecological architecture predicts whether an antagonist-reducing floral trait is selective rather than pollinator-costly?

See `PRIOR_MACRO_SYNTHESIS_POSITIONING_V1.md`.

## Decision

```text
ecological signal:                    PRESENT
strict cross-system model capacity:   NOT_READY
generic literature expansion:         NO
focused matched-D expansion:          CONTINUE
independent network validation:       PASS_SAKHALKAR_2023
legacy BITA results:                  PRESERVE
```
