# Menyanthes trifoliata 2018 petal-hair defence audit v1

## Source

Tagawa K. **Repellence of nectar-thieving ants by a physical barrier: Adaptive role of petal hairs on Menyanthes trifoliata (Menyanthaceae).** *Journal of Asia-Pacific Entomology* 21:1211–1214. DOI `10.1016/j.aspen.2018.09.006`.

The publisher abstract and author-posted primary article agree on the experimental design and direction of results.

## Floral-D definition

The focal structure is located directly on petals:

```text
D = dense petal hairs
antagonist = nectar-thieving Lasius japonicus ants
manipulation = trim petal hairs with a small hair trimmer
```

This is a clean flower-specific physical barrier and does not require extending `D` to leaves, stems, or whole-plant defence.

## Source-verified Pattern

Ants encountering intact petal hairs stopped advancing and had difficulty maintaining balance.

The hair-trimming experiment showed:

- ants entered floral tubes more successfully when petal hairs were trimmed;
- intact hairs significantly reduced floral-tube entry success;
- even among successful entries, ants took approximately twice as long to enter tubes with intact hairs.

Pattern state:

```text
D -> antagonism: protective
```

The response is access to floral nectar rather than plant fitness, so the study remains a constituent-route result.

## Theory-facing mapping

Admitted:

```text
flower-specific physical microstructure can reduce nectar-thief access
physical D recurs across hair, sticky-surface, slippery-surface, and water-barrier mechanisms
ant body size / locomotion provides a plausible access-mode filter
```

Not admitted:

```text
petal hairs = attraction A
ant exclusion = rho
ant access reduction = W_AD
absence of a pollinator experiment = no pollinator cost
```

## Pollinator boundary

The study discusses other known functions of floral hairs in pollinator attraction, nectar secretion, or footholds in other plant systems, but it does not experimentally estimate the effect of trimming *M. trifoliata* petal hairs on legitimate pollination.

Accordingly, no `D -> pollination` record is created.

## Independence value

This is independent of the current physical-D systems:

```text
Pedicularis: water-filled bract barrier
Bejaria/Erica: adhesive floral surfaces
Takeda: slippery wax-covered perianths
Menyanthes: dense petal hairs restricting ant locomotion
```

It therefore strengthens cross-mechanism recurrence of physical floral defence rather than merely adding another taxon with the identical physical mechanism.

## Current adjudication

```text
source identity:               PASS
flower-specific D:             PASS
direct D manipulation:         PASS
D -> antagonism:               PASS
D -> pollination:              NOT IDENTIFIED
direct A x D:                  NO
```

### Decision

**PROMOTE_TO_PATTERN_EXPANSION_LEDGER**
