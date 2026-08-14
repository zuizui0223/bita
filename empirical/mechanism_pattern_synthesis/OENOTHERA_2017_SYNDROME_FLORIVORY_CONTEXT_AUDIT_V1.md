# Oenothera section Calylophus 2017 pollination-syndrome × florivory context audit v1

## Source

Rios RS, Marquis RJ, Flunker JC. **Pollination syndromes and florivory: implications for floral evolution.** *AoB PLANTS* 9:plw088. DOI `10.1093/aobpla/plw088`.

The primary article is open access and reports a comparative field study of five species in *Oenothera* section *Calylophus*.

## Pattern question

Does antagonist pressure differ systematically among floral trait combinations associated with different pollination syndromes?

This is a trait-class / syndrome-level Pattern question. It is **not** a clean single-axis `A -> antagonism` test because multiple floral dimensions covary with pollination syndrome.

## Data architecture

The study reports:

```text
525 individual plants
5 Oenothera section Calylophus species
bee- versus hawkmoth-pollinated floral syndromes
Mompha moth florivory measured as proportion of buds/flowers infested or damaged
multiple floral traits including floral-tube length and corolla flare
```

## Published Pattern

Hawkmoth-pollinated species with longer, narrower floral tubes experienced more *Mompha* florivory than bee-pollinated species.

Source-reported scale translations include approximately:

```text
hawkmoth-pollinated syndrome: ~13% greater florivory than bee-pollinated syndrome
+18.2 mm floral-tube length:  ~13% increase in infested buds
-2.5 mm corolla flare width: ~6.3% increase in Mompha florivory
```

The study therefore links a pollination-syndrome trait complex to antagonist exposure across closely related plant species.

## Theory-facing mapping

Admitted Pattern classes:

```text
trait-class / syndrome dependence of antagonist exposure
floral morphology can jointly shape mutualist adaptation and antagonist vulnerability
signal/access architecture matters beyond floral chemistry
```

This provides a cross-species morphological analogue to the source-level shared-tracking cases in *Dalechampia* and *Raphanus*.

## Why this is NOT promoted to the route ledger

The syndrome contrast bundles several traits and species-level differences. It does not isolate one declared attraction axis while holding the remaining floral phenotype fixed.

Accordingly:

```text
hawkmoth syndrome != one focal A
long floral tube != automatically attraction A
higher Mompha damage != direct A -> antagonism coefficient
species contrast != within-study direct A x D design
```

The study remains in the environmental/trait-class Pattern layer.

## Current adjudication

```text
primary source:               PASS
trait-class context:          PASS
quantitative source summary:  PASS
single focal A route:         NO
single focal D route:         NO
direct A x D:                 NO
```

### Decision

**PROMOTE_TO_TRAIT_CLASS_CONTEXT_LAYER_ONLY**
