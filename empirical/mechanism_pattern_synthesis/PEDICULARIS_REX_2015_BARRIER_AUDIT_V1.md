# Pedicularis rex 2015 water-bract barrier audit v1

## Source

Sun S-G, Huang S-Q. **Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower.** *AoB PLANTS* 7:plv019. DOI `10.1093/aobpla/plv019`.

The primary article is open access and reports a direct manipulation of water retention in cupulate bracts subtending the flowers.

## Why this study is high-value for Part II

Unlike many near-direct studies, this paper contains a clearly manipulable, flower-associated physical barrier with an experimentally demonstrated antagonist-reduction function:

```text
D = intact water-holding cupulate bract state
manipulation = drain water by cutting a hole at the base of the bract
```

The same study measures:

- legitimate pollinator visitation;
- nectar-robber visitation;
- seed predation;
- initial and final seed set.

This makes it a strong same-system Pattern study even though it does not contain a separate attraction-trait `A` manipulation.

## Pollinator response

Water removal did not change legitimate pollinator visitation.

Published GLM treatment term:

```text
pollinator visit rate
treatment beta = +0.012
SE = 0.224
chi-square = 0.003
P = 0.958
```

The year × treatment interaction was also unresolved (`P = 0.823`).

Pattern state:

```text
D -> pollination: no detected interference
```

## Nectar-robber response

The same water-barrier manipulation did not alter nectar-robber visitation.

Published GLM treatment term:

```text
nectar robber visit rate
treatment beta = -0.014
SE = 0.225
chi-square = 0.004
P = 0.951
```

The source explains that robbers pierced corolla tubes from above and avoided the water barrier.

Pattern state:

```text
D -> nectar-robber antagonism: no detected barrier effect
```

## Seed-predator response

Water removal strongly increased seed predation, so intact water-filled bracts reduced seed-herbivore damage.

Across six sites the published GLM reports:

```text
seed predation treatment beta = -0.072
SE = 0.007
chi-square = 92.808
P < 0.0001
site × treatment P < 0.0001
```

The sign of the source coefficient is retained as reported rather than reverse-engineered into a new effect metric because the treatment coding is not redefined here. The biological direction is unambiguous from the experiment and text: drained bracts had greater seed predation.

Five of six populations showed a significant treatment effect; the one unresolved population was Zhongdian. Final seed set also differed by treatment (`P < 0.0001`).

Pattern state:

```text
D -> seed-predator antagonism: protective
```

## Context structure

The same manipulated `D` therefore produces different states for different consumers:

```text
legitimate pollinators: no detected effect
nectar robbers:         no detected effect
seed predators:         strong protective effect
```

This is a particularly clean example of **consumer identity / attack mode opening and closing a defence channel**.

It also provides a guarded state: antagonist reduction can occur without a detected pollinator cost.

## Relationship to Sun et al. 2016

A later *Pedicularis rex* study (DOI `10.1093/aob/mcw097`) measured corolla exsertion, stigmatic pollen load, seed predation, and final seed production across populations. Greater exsertion was associated with both more pollen receipt and more seed predation.

That later study contains a composite attraction/protection geometry and is not a direct `A x D` design. It should be linked as same-species contextual evidence but not collapsed into the 2015 experimental effect or counted as an independent `D` manipulation without panel-overlap adjudication.

## Theory-facing mapping

Admitted:

```text
D -> antagonism can be strongly consumer-specific
D -> pollination cost can be absent in a system with demonstrable antagonist protection
same physical barrier can block one antagonist mode but not another
```

Not admitted:

```text
D -> seed predation effect = rho
D -> pollinator null = iota = 0
this study estimates W_AD
water-filled bract is an attraction trait A
```

The non-significant pollinator term is a study-specific guarded state, not proof that pollinator interference is universally absent.

## Current adjudication

```text
primary source:                    PASS
flower-specific D definition:     PASS
experimental D manipulation:      PASS
D -> seed predator:               PASS
D -> pollinator:                  PASS, no detected effect
D -> nectar robber:               PASS, no detected effect
same-system multi-route status:   PASS
direct A x D status:              NO
context/sign-state value:         HIGH
```

### Decision

**PROMOTE_TO_PATTERN_EXPANSION_LEDGER**
