# Silene 2014 floral-signal × seed-predation audit v1

## Source

Page P, Favre A, Schiestl FP, Karrenberg S. **Do Flower Color and Floral Scent of Silene Species affect Host Preference of Hadena bicruris, a Seed-Eating Pollinator, under Field Conditions?** *PLOS ONE* 9:e98755. DOI `10.1371/journal.pone.0098755`.

The primary article is open access (PMCID `PMC4048206`).

## Pattern question

Do floral signal traits belonging to the attraction/display phenotype also alter antagonist host choice in an independent nursery-pollination system?

The experiment used field-transplanted recombinant F2 hybrids between white-flowered *Silene latifolia* and pink-flowered *S. dioica*, together with within-species crosses. Recombinant hybrids break up the parental association among colour and scent traits, allowing those signal dimensions to enter a joint seed-predation model.

## Source-verified Pattern

The primary response was seed predation / host attack by the seed-eating pollinator *Hadena bicruris*.

In the F2 analysis:

```text
pinker S. dioica-like flower colour -> lower odds of primary seed predation
alpha-pinene emission               -> lower odds of primary seed predation
benzyl acetate emission             -> higher odds of primary seed predation
6-methyl-5-hepten-2-one emission    -> higher odds of primary seed predation
```

Thus antagonist host choice is associated with multiple floral sensory dimensions rather than one universal scent direction.

The source interprets the colour result as consistent with moth attraction to the white flowers of its preferred host *S. latifolia*. The scent compounds associated with predation were not species-specific and may act as more general deterrents, attractants, or host-quality cues.

Pattern state:

```text
A (flower colour / floral scent phenotype) -> antagonist host choice / seed predation
```

## Why this is an A-side route

Flower colour and floral scent are sensory floral traits used in host/flower location by *H. bicruris* and other flower visitors. The F2 design separates these signal dimensions enough to model their joint association with attack.

The route is therefore admitted as a floral-signal `A -> antagonism` record.

Colour and individual volatile compounds nevertheless remain separate measured axes. They are not averaged into one synthetic attraction score.

## Nursery-pollinator boundary

*Hadena bicruris* is a seed-eating pollinator: adult moths can pollinate while offspring consume developing seeds. That dual natural history does **not** make this study a same-study `A -> pollination` estimate.

The analysed response here is seed predation/host choice. No pollination-response coefficient for the same F2 signal axes is extracted from this paper.

Accordingly:

```text
A -> antagonism: PASS
A -> pollination: not identified in this study
same-system multi-route: NO for the current ledger
direct A x D: NO
```

## Theory-facing mapping

Admitted:

```text
floral sensory/display traits can predict antagonist host choice outside Cucurbita, Dalechampia and Raphanus
A -> antagonism recurrence spans colour and multiple volatile dimensions
antagonist response to floral scent is compound-specific rather than universally positive or negative
```

Not admitted:

```text
seed-predation coefficient = W_AD
adult moth pollination natural history = same-study A -> pollination effect
all floral volatiles = equivalent A units
nursery pollination = direct A x D
```

## Independence value

This adds a distinct plant lineage and antagonist life history to the A-side route architecture. It is kept independent from the *Silene stellata* lifecycle-stage context program because the species, study, and focal inference differ.

## Current adjudication

```text
primary source:                PASS
floral A/signal basis:         PASS
A -> antagonism:               PASS
same-study A -> pollination:   NOT IDENTIFIED
direct A x D:                  NO
```

### Decision

**PROMOTE_TO_PATTERN_EXPANSION_LEDGER**
