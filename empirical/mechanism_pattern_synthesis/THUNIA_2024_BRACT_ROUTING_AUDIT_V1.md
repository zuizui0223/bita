# Thunia alba 2024 bract-routing audit v1

## Source

Wu S-M, Gao J-Y. **The conspicuously large bracts influence reproductive success in Thunia alba (Orchidaceae).** *Journal of Plant Ecology* 17:rtad036. DOI `10.1093/jpe/rtad036`.

The primary article is open access and reports a direct bract-removal experiment conducted over the 2022–2023 reproductive seasons.

## Why this is a high-value floral-D system

Each large curly bract encloses the pedicel and nectar spur of a flower. The experiment removes these bracts while leaving the flowers otherwise available to visitors.

```text
D = large spur-enclosing floral bract
manipulation = intact versus removed bracts
pollinator/robber = Bombus breviceps
```

The same bumblebee is the only effective pollinator at the site and can also act as a nectar robber when the protective bract is removed.

## D -> antagonism: bracts suppress nectar robbery

Bract removal strongly increased robbery.

Published observations:

```text
intact treatment visits by B. breviceps:
  16 normal visits
   3 nectar-robbing visits

removed-bract treatment:
   5 normal visits
  21 nectar-robbing visits

robbery-behaviour comparison:
chi-square = 18.62, df=1, P<0.0001
```

The proportion of robbed flowers also increased from:

```text
intact:          15.43% ± 3.13% SE, n=40 inflorescences
removed bracts:  90.25% ± 1.88% SE, n=43
P < 0.0001
```

Pattern state:

```text
D -> antagonism: strong protection against nectar robbery
```

## D -> pollination: the defence routes the same consumer into a legitimate functional state

Bract removal did not reduce the hourly visit frequency of *B. breviceps*:

```text
intact:          2.48 ± 0.31, n=21
removed bracts:  2.39 ± 0.25, n=23
t=0.21, P=0.83
```

Instead, removing the bract changed **how the same visitor used the flower**. With intact bracts the bee usually entered through the labellum passage and contacted reproductive structures. With bracts removed, it pierced the spur and robbed nectar, failing to carry pollinia during those visits.

Bract removal also shortened visit time per flower:

```text
intact:          5.53 ± 0.49 s, n=15
removed bracts:  3.06 ± 0.21 s, n=16
t=4.60, P<0.001
```

and increased flowers visited per inflorescence:

```text
intact:          2.54 ± 0.16, n=37
removed bracts:  3.54 ± 0.21, n=39
t=3.72, P<0.001
```

The relevant `D -> pollination` Pattern is therefore not a change in attraction frequency, but routing between legitimate and antagonistic foraging modes.

## Reproductive consequences

Male and female pollination outcomes were lower after bract removal:

```text
pollinia removal:
  intact 56.50% ± 2.65%
  removed 15.47% ± 3.85%
  chi-square = 78.74, P<0.001

pollinia deposition:
  intact 30.79% ± 2.13%
  removed 9.73% ± 3.37%
  chi-square = 28.72, P<0.001

fruit set:
  intact 28.71% ± 2.08%
  removed 8.18% ± 3.39%
  chi-square = 27.38, P<0.001
```

Both treatments remained strongly pollinator-limited relative to hand cross-pollination.

## New Pattern class: pollinator functional-mode routing

This study adds a useful state beyond the simple question "does D deter pollinators?":

```text
D present:
  same consumer behaves mainly as legitimate pollinator

D removed:
  same consumer shifts mainly to nectar robbery

visit frequency:
  unchanged
```

A floral defence can therefore change the **functional role** of a visitor without reducing its arrival rate.

This complements the Anemone context, where a glaphyrid beetle simultaneously occupies pollinator and florivore roles, and the Iris program, where florivore-created holes induce a Bombus pollinator-to-robber switch.

## Theory-facing mapping

Admitted:

```text
flower-associated D strongly reduces nectar robbery
D state can route the same consumer between mutualistic and antagonistic behaviours
pollinator arrival frequency can remain unchanged while pollination function changes
D-mediated change in visitor mode can translate into male and female reproductive effects
```

Not admitted:

```text
fruit-set difference = W_AD
robbery reduction = rho
pollinator visit-frequency null = iota = 0
large bract = attraction A in this system
```

The article explicitly reports no detectable effect of bract removal on pollinator visit frequency; the bract is therefore not promoted as a focal attraction trait here.

## Current adjudication

```text
primary full text:                PASS
flower-associated D:              PASS
direct D manipulation:            PASS
D -> antagonism:                  PASS
D -> pollination function:        PASS
same-consumer role switching:     PASS
same-system multi-route:          PASS
direct A x D:                     NO
```

### Decision

**PROMOTE_TO_PATTERN_EXPANSION_LEDGER AND CONDITIONALITY LAYER**
