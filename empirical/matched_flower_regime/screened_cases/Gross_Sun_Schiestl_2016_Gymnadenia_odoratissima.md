# Gross, Sun & Schiestl (2016) — *Gymnadenia odoratissima* exact Dryad audit

```text
article DOI:       10.1371/journal.pone.0147975
public dataset DOI:10.5061/dryad.dj40r
package title:      Data from: Why do floral perfumes become different?
                    Region-specific selection on floral scent in a terrestrial orchid
archive status:     9-file manifest; 8 table headers recovered
```

## Provenance status

The prior full-text screen records that the article declares the Dryad DOI. The
Dryad package title begins with `Data from:` and gives the matching study title.
However, DataCite records the article with the relation type `IsCitedBy`, which
is not a qualifying supplement/derivation relation under the repository's strict
relation-only rule.

```text
article-declared dataset DOI:          recorded in prior full-text screen
matching Data from: title:              yes
DataCite qualifying relation:           no (IsCitedBy)
current identity status:                title-validated, relation-type pending
```

This is sufficient to inspect package structure, but not to silently treat the
archive as a formally verified original supplement under the relation-only rule.

## Header-level evidence

Individual `PlantID`, `Year`, `Population`, and `NrFlowers` fields recur across
key tables:

```text
FloralTraitDifferences
  → individual scent compounds, total scent, flower number, display traits

HerbivoryDifferences
  → PlantID, NrFlowersEaten, AphidLoad

ReproductiveSuccessDifferences / SelectionAnalysis
  → PlantID, NrFlowers, NrFruits, proportional or relative female success

PollinatorLimitation
  → PlantID, treatment, NrFlowers, NrFruits, proportional female success

PollinatorFamiliesPerH / NoPollinators_PollinatorFamilyRichness
  → population-date pollinator observations, not individual-plant outcomes
```

## What this can support next

The archive is now a high-information source for a **bounded row-linkage audit**:

1. verify overlap of `PlantID + Year + Population` between floral traits,
   herbivory, and reproductive-success tables;
2. verify whether `NrFlowersEaten` has the linked `NrFlowers` denominator in the
   same defined observation context;
3. confirm sampling timing and variable definitions from article methods; and
4. formalize the article-to-dataset identity contract from the article-declared
   DOI and dataset title.

If those conditions hold, the floral-scent/display variables may contribute an
`A_to_antagonism` analysis. They do **not** yet provide an individual
`A_to_pollination` effect, because the observed pollinator measures are at the
population-date level. No independently justified `B_flower` trait is present.

## Current classification

```text
status:             high-information multichannel A-panel; not M2 or D1
four-path registry: no effect registered yet
blocking items:      row linkage, outcome denominator/timing, identity contract,
                     and absence of an independent B_flower module
```
