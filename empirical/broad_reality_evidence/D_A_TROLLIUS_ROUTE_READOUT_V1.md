# Trollius d_A route readout v1

## Fixed source

```text
candidate:  dA_cand_trollius
DOI:        10.1371/journal.pone.0118299
PMCID:      PMC4334720
PMID:       25692295
```

## What the screen did

The screen resolved the fixed DOI through Europe PMC and searched the public
full-text XML using the registered heading-based `d_A` route contract. It retained
only accession identifiers, term families, section titles, and table labels. It did
not retain article prose or extract a numerical result.

## Result

```text
full-text XML access:       recovered
trait-term family:          present
antagonist-term family:     present (beetle)
shared sections:            Materials and Methods; Study species;
                            Pollinator Observations and Flower Measures
relevant table locator:     none
trait-intervention heading: none
antagonist-outcome heading: none
route signal:               term_cooccurrence_without_experiment_link
```

The appearance of floral-trait terms and beetle terms in the same source is not a
verified `flower trait -> floral antagonism` estimate. The section headings do not
show either a floral-trait intervention or an antagonist-outcome analysis, so the
public XML screen does not establish the required direct route.

## Decision

```text
d_A numerical extraction:   stop
B2 effect row:              none
B3 cluster contribution:    none
retained role:              generalized-pollination system context only
```

This is not a claim that no trait-antagonist relationship exists biologically. It is
a source-contract decision: no direct model was located in the public full-text
structure under the registered C3/C4 screen. Any later reconsideration requires a
separately located direct trait-to-antagonist model with an outcome definition,
experimental unit or denominator, and uncertainty.
