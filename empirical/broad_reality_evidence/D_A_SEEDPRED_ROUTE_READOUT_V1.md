# Seed-predation `d_A` route readout v1

## Fixed source

```text
candidate:  dA_cand_conflicting_seedpred
PMID:       27325896
DOI:        10.1093/aob/mcw097
PMCID:      PMC4970362
```

## Public routes tested

```text
PMID -> NCBI id-conversion -> DOI and PMCID
PMCID -> Europe PMC fullTextXML      : HTTP 404
PMCID -> NCBI PMC EFetch XML         : recovered
```

The NCBI EFetch record was 8,783 bytes and did not contain an article `<body>`.
The workflow retained only structural location signals, not article prose.

## Route screen result

```text
article body present:              no
exsertion term location:           abstract only
seed-predation term location:      abstract only
model-term location:               abstract only
body-level shared section:         none
relevant table locator:            none
route signal:                      abstract_or_metadata_term_cooccurrence_only
```

An abstract-level co-mention is not a direct `floral exsertion -> seed predation`
model. It cannot supply an outcome denominator, experimental unit, uncertainty, or
a compatible effect metric.

## Decision

```text
C4 numerical readout:              stop
new B2 effect row:                 0
new B3 cluster:                    0
current role:                      public-route context only
```

This is not evidence that floral exsertion has no relationship with seed predation.
It is a source-access and extraction-contract result: the currently registered
public XML routes do not expose the article body or a direct model. Reconsideration
requires a separately located lawful full-text route that provides the model,
outcome definition, experimental unit or denominator, and uncertainty.
