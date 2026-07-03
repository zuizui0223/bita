# Public C4 readout for `d_A` source targets v1

## Scope

This readout evaluates the two public, source-specific `d_A` C4 targets already
registered in the evidence workflow. It uses the exact public XML routes, bounded
figure previews where available, and structured context checks. It does **not**
extract a numerical effect, digitize figures, or alter `part_b_arrow_effects.csv`.

```text
visual/display target  Parnassia wightiana, DOI 10.1002/ece3.70380
scent/reward target    Schiestl et al. 2015, DOI 10.7554/eLife.07641
```

## C4 gate

A source can move to manual B2 numerical extraction only if the same source context
supports all of the following:

```text
treatment and control definition
antagonist outcome denominator / unit
experimental unit and replication
uncertainty convention
recoverable numerical contrast with uncertainty, preferably a relevant table or
supplementary data locator
```

A plotted bar and error bar alone do not satisfy the final requirement.

## Parnassia: visual/display -> florivory

```text
public XML:                     recovered
intervention locators:          Staminodes Removal Experiments; Staminode Removal Experiments
antagonist locator:             Florivory Dynamics
figure locators:                FIGURE 1; FIGURE 3
relevant table locator:         none
control context:                located
outcome context:                located
experimental-unit context:      located
replication context:            located
uncertainty context:            located
model context:                  not located in the target sections
C4 decision:                    retain as directional or C4 evidence, not B2
```

The intervention-to-antagonist route is a viable public reading target, but the
registered source context supplies no relevant table locator for a recoverable
numerical comparison. It therefore adds **no** B2 effect row.

## Schiestl: scent/reward -> hawkmoth oviposition

```text
public XML:                     recovered
antagonist locator:             Oviposition trials
primary figure locator:         Figure 2
bounded Figure 1-2 previews:    rendered from exact public eLife assets
relevant table locator:         none
control context:                not located in the target section
outcome context:                located
experimental-unit context:      located
replication context:            not located in the target section
uncertainty context:            located
model context:                  not located in the target section
C4 decision:                    retain as directional or C4 evidence, not B2
```

Figure 2 visibly contains treatment-labelled panels and oviposition outcomes, but
the XML target context does not jointly provide a control mapping, replication, and
a table/supplement based numerical contrast. It therefore adds **no** B2 effect row.

## Consequence for Part B

```text
new B2 effects from the two public d_A C4 targets: 0
new exploratory quantitative d_A strata:            0
current appropriate role:                            source-specific C4 / directional evidence
```

This is a meaningful negative result. It prevents the project from converting
visually interpretable figures into unsupported effect sizes. The `d_A` visual and
scent tracks remain distinct and both require independently extractable,
compatibly coded numerical studies before a stratum-specific meta-analysis is
attempted.

## Boundary

The absence of a new B2 effect here is a statement about the registered public
source routes and the pre-registered extraction contract. It is not a claim that
these biological pathways are absent, null, or unimportant.
