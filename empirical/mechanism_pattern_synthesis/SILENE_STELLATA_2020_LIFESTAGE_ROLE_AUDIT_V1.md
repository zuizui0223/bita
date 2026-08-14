# Silene stellata 2020 lifecycle-stage role-reversal audit v1

## Source

Dudash MR, Hassler C, Stevens PM, Fenster CB. **Variable and sexually conflicting selection on Silene stellata floral traits by a putative pollinator–seed predator, Hadena ectypa.** *Evolution* 74:1321–1336. DOI `10.1111/evo.13965`.

The primary article analyses taxon-specific selection through both male and female reproductive function in the nocturnally pollinated *Silene stellata*–*Hadena ectypa* system.

## Pattern question

Can one consumer taxon switch ecological function across its lifecycle, such that the same floral phenotype is associated with mutualistic service at one life stage and antagonistic cost at another?

## Lifecycle-dependent consumer roles

The biological interaction is intrinsically stage structured:

```text
adult Hadena ectypa:
  nocturnal flower visitor / pollinator
  females may pollinate while ovipositing
  males can contribute pollination without oviposition

larval Hadena ectypa:
  seed predator developing from eggs laid by adult females
```

Thus mutualistic and antagonistic functions are not merely performed by different guilds. They are linked through the lifecycle of the same moth taxon.

## Selection pattern

The study decomposes selection on floral traits through male and female fitness components and identifies sex-specific conflict in the consequences of petal dimensions.

The key pattern is that larger petal/display dimensions can be favoured through male function while being selected against through female function when attraction/oviposition by the nursery moth increases subsequent seed predation.

The source therefore supplies a biological realization of:

```text
same floral display trait
+ same consumer taxon
+ different life stages / fitness pathways
-> opposite or sex-specific selection contributions
```

The exact trait/fitness coefficients remain source-specific and are not collapsed into a synthetic A coefficient here.

## New Pattern class: lifecycle-stage functional-role reversal

This differs from the other dual-role systems already in the expansion.

```text
Thunia:
  same adult Bombus individual/guild switches legitimate pollination <-> robbery depending on bract state

Anemone:
  same adult glaphyrid guild both pollinates and scratches petals

Iris:
  a florivore-created access hole can switch an adult Bombus visitor from legitimate pollination to robbery

Silene stellata:
  adult Hadena pollination is linked across generations/life stages to larval seed predation
```

The Silene case therefore adds an **ontogenetic / lifecycle** dimension to consumer-role conditionality.

## Theory-facing mapping

Admitted:

```text
mutualistic and antagonistic functions can be linked through one consumer lifecycle
floral attraction/display consequences can differ across male versus female fitness pathways
consumer functional role is not a fixed taxonomic property
selection on one floral trait can change direction across reproductive components
```

Not admitted:

```text
sex-specific selection gradient = W_AD
Hadena adult/larval lifecycle = focal defence D
female seed-predation cost = rho
male pollination benefit = A -> pollination coefficient on the same scale used in the focal theory
```

## Route-ledger boundary

This study is retained in the conditionality layer rather than being forced into a marginal route record. Its main value is the linked taxon-specific selection decomposition, not a single focal pathway coefficient compatible with the current route ledger.

It therefore does not increment route-ledger N.

## Current adjudication

```text
primary source identity:              PASS
same-consumer lifecycle dual role:    PASS
male/female fitness decomposition:    PASS
new conditionality class:             PASS
focal D route:                        NO
direct A x D:                         NO
route-ledger increment:               NO
```

### Decision

**PROMOTE_TO_CONDITIONALITY LAYER AS LIFECYCLE-STAGE ROLE REVERSAL**
