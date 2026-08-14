# Acacia floral ant-repellence context audit v1

## Sources

This context module links several primary studies of floral ant-repellence in *Acacia* / *Vachellia* systems:

- Willmer & Stone 1997, **How aggressive ant-guards assist seed-set in Acacia flowers**, *Nature* 388:165–167.
- Raine, Willmer & Stone 2002, **Spatial structuring and floral avoidance behavior prevent ant–pollinator conflict in a Mexican ant-acacia**, *Ecology* 83:3086–3096.
- Nicklen & Wagner 2006, **Conflict resolution in an ant-plant interaction: Acacia constricta traits reduce ant costs to reproduction**, *Oecologia* 148:81–87. DOI `10.1007/s00442-006-0359-6`.
- Willmer et al. 2009, **Floral volatiles controlling ant behaviour**, *Functional Ecology*. DOI `10.1111/j.1365-2435.2009.01632.x`.

## Pattern question

Can a defensive floral state be expressed only during the narrow time window when pollinator access is most valuable?

These systems are useful because the antagonists are resident ant guards that benefit the plant outside the flower but can interfere with reproductive interactions when present on newly opened flowers.

## Source-verified state pattern

Across the Acacia studies:

```text
outside pollen-dehiscence / reproductive window:
  resident ants patrol the plant and can provide anti-herbivore defense

during pollen dehiscence / young-flower window:
  newly opened flowers emit ant-repellent cues
  resident ants avoid or rapidly leave inflorescences
  pollinator activity overlaps with this temporary ant exclusion

after pollen is removed / flowers age:
  repellence declines and ants can return
```

The 2009 multispecies work reports that young-flower volatile repellence is common across Acacia species, varies among plant and resident-ant species, and is strongest around pollen dehiscence. In *Vachellia seyal fistula*, ant response covaried with pollen availability; experimentally retaining polyads by bagging prolonged repellence relative to normally visited flowers.

The 2006 *A. constricta* experiment similarly found ants avoided secondary contact with newly opened inflorescences and pollen relative to buds/older flowers, while pollinator activity followed the daily dehiscence period.

## Theory-facing Pattern class

This is a clean **temporal guarded-window** example:

```text
defensive/repellent floral state ON  -> during pollinator-critical reproductive window
repellent state OFF / weaker         -> outside that window
```

It strengthens the idea that defence–mutualist conflict need not be resolved by one static trait optimum. The plant can temporally gate an antagonist-reducing floral function to the stage when pollinator interference would otherwise be most costly.

## Why this is context-only rather than a new route-ledger N

The primary studies strongly establish ant repellence and temporal/spatial separation from pollinators, but most do not experimentally remove the floral volatile cue and then estimate a common pollination outcome under cue-present versus cue-absent states.

Accordingly, this audit is **not** promoted as a new independent `D -> pollination` effect record.

It contributes to the conditionality matrix only.

## Inference boundary

Not admitted:

```text
ant repellence = measured iota
pollinator temporal overlap = direct D -> pollination effect size
ant guards = floral antagonists in every ecological context
Acacia VOCs = attraction trait A
repellence window = direct W_AD estimate
```

Admitted:

> floral antagonist-reducing functions can be temporally gated to a pollinator-critical stage, providing an independent biological realization of a guarded-window regime.

## Current adjudication

```text
multiple primary sources:        PASS
floral antagonist-repellent cue: PASS
temporal state switching:        PASS
pollinator-window linkage:       PASS
new direct route effect:         NO
context Pattern value:           HIGH
```

### Decision

**PROMOTE_TO_CONDITIONALITY_LAYER_ONLY**
