# Theis et al. (2014) — *Cucurbita* A→pollinator / A→antagonist quantitative pair

## Source identity

```text
article DOI:  10.3732/ajb.1400171
Dryad DOI:   10.5061/dryad.1h189
Dryad API:   version archive recovered and audited in GitHub Actions
```

The study grew 20 Cucurbitaceae species/varieties in the field to measure pollinator and herbivore interactions and in the greenhouse to measure putative attractive and defensive traits. The paper reports a second analysis restricted to *Cucurbita* to reduce the possibility that the across-family pattern is simply a broad phylogenetic contrast.

## Public-data structure audit

The public Dryad version archive contains 21 files. A bounded schema audit recovered the key shared identifier `PlantID` across:

```text
Nectar and Flower Size.csv
  flower-level morphology/reward measurements

Volatiles ngflowerh.csv
  flower volatile emissions, including individual sesquiterpenoids

Pollinator Observation.csv
  Year / Date / Block / Plant / Variety / PlantID / Flower Sex
  #beetles at observation start
  pollinator visitor rows and approach/rejection fields
```

The field-observation documentation states that flower sex, ant number, and the number of *Acalymma vittatum* beetles were recorded at the beginning of an observation; each pollinator visitor has its own row. Pollinator observations were five minutes per flower in the article methods. Squash bee visits dominated the pollinator records and were the focal pollinator outcome.

This establishes a recoverable same-system trait–pollinator–floral-antagonist panel. The archive audit itself does not manufacture an individual-level join between greenhouse and field plants; the article's analysis is comparative across taxa/varieties.

## Source-reported quantitative effects

The article reports that within *Cucurbita*, sesquiterpenoid emission, rather than corolla length, explained both squash-bee and floral-beetle visitation. The source coefficients are:

```text
A = floral sesquiterpenoid emission

A → squash-bee floral visitation
  beta = +0.096
  SE   =  0.034
  95% CI = [0.029, 0.163]

A → cucumber-beetle flower use
  beta = +2.91
  SE   =  1.28
  95% CI = [0.40, 5.4]
```

The corresponding corolla-length intervals cross zero in that within-*Cucurbita* model. These coefficients are retained on their source-reported scales; they are not transformed into a common metric or pooled with the standardized *Impatiens* slopes or the *Gymnadenia* log-odds slope.

## Evidence classification

```text
same-system multi-route:      Tier 2
A_to_pollination quantitative: yes
A_to_antagonism quantitative:  yes
independence cluster:          one Theis-et-al.-2014 comparative panel
direct A x D:                  no
D axis:                        not required for these two A routes
```

This is the second independent quantitative `A_to_antagonism` anchor currently registered after *Gymnadenia odoratissima*.

## Biological interpretation

The result is particularly useful for the theory because the **same floral signal axis is positively associated with both a specialist pollinator and a specialist floral antagonist**. It therefore supplies direct empirical support for attraction tracking without requiring the two routes to be assembled from unrelated plant systems.

It does not show that sesquiterpenoids are universally attractive, that all floral scent increases herbivory, or that the two coefficients can be subtracted to estimate `W_AD`. The article itself notes multiple possible functions of sesquiterpenoids; for this synthesis their `A` role is anchored by the same-panel positive pollinator association rather than by assuming that every volatile is an attraction trait.
