# Caruso 2019 primary-study index protocol v1

## Purpose

Caruso, Eisen, Martin & Sletvold (2019; DOI `10.1111/evo.13639`) is retained only
as a possible index to **primary systems** for the `d_A` literature. Its floral
selection gradients are not trait-to-antagonism effects and must never enter
`part_b_arrow_effects.csv`.

## Stage C3-I: index-route probe

The reproducible probe checks only public, URL-level routes:

```text
Crossref article metadata
Unpaywall article locations
OpenAlex article locations
DataCite dataset records explicitly related to the article DOI
publisher landing-page links pointing to a recognized dataset host
```

The output consists of access receipts and dataset/index candidate URLs. It does
not download a database, retain article HTML or prose, or extract any study row.

## Decision rule

```text
No candidate dataset/index route recovered
    -> retain Caruso as a system seed only; stop this route.

Candidate route recovered
    -> resolve dataset metadata and verify that it exposes primary-study
       bibliographic identifiers, not effect values alone.

Verified primary-study identifiers recovered
    -> create one C3 receipt per primary study and apply the normal d_A C4 gate:
       direct attraction trait -> floral antagonism route;
       treatment/predictor definition;
       outcome denominator and experimental unit;
       uncertainty; compatible effect metric/design/trait stratum.
```

## Prohibitions

```text
- Never code a Caruso selection gradient as d_A.
- Never treat a meta-analysis database row as a primary-study effect.
- Never infer a trait -> antagonism route from herbivore-mediated selection alone.
- Never pool primary studies merely because they occur in the same source database.
- Never use a dataset-host URL as evidence that the data are extractable.
```

## Expected contribution

A successful route can efficiently identify independent primary studies. It cannot
by itself increase the B2 evidence count. Only source-audited primary-study effects
in exact compatibility strata may do that.
