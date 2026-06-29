# Public-package screen: *Dalechampia scandens*

## Source pair

- Pérez-Barrales, R. et al. (2013). *Pollinators and seed predators generate
  conflicting selection on Dalechampia blossoms*. **Oikos**.
  DOI: `10.1111/j.1600-0706.2013.20780.x`.
- Albertsen, E., Opedal, Ø. H. et al. (2020). *Using ecological context to
  interpret spatiotemporal variation in natural selection* [Dataset]. Dryad.
  DOI: `10.5061/dryad.0k6djh9xx`.

## What is publicly documented

The Dryad package visibly lists 16 small `.txt`/`.xlsx` tables, one for each
population-year panel:

```text
HZ 2015
LM 2006, 2007
PA 2014
PM 2006, 2007
PV 2014, 2015
```

Its public method/usage-note text documents the following columns or measures
for focal blossoms:

```text
population, year, date, patch, blossom
upper-bract area and dimensions
resin-gland area and dimensions
gland–stigma / anther–stigma distances
stigmatic pollen during female and bisexual phases
resin removal (0/1)
intact/germinable seeds, undeveloped seeds, seed-predated seeds, total seeds
```

The design marks focal blossoms, follows them through flowering, and collects
those same marked blossoms 3–4 weeks later. Thus the public package has a
strong declared **blossom-level linkage** between floral morphology, pollination
proxy, and seed-predation outcome.

## Current evidence state

```text
M0_high_information_public_package_pending_article_trait_screen
```

This status is intentionally not an M1/M2/D1 classification. The article full
text was not retrievable through the public publisher route during this screen,
so functional assignment of the floral traits cannot be completed from title and
repository metadata alone.

## Why it is not yet D1

The public usage notes identify traits used in the related selection work as
advertisement, reward, and pollen-transfer candidates. They do **not yet
establish a separately measured floral barrier/resistance trait** that could be
used as `B_flower` in the current Part I model.

For example:

```text
upper-bract area        → likely advertisement/display candidate
resin-gland area        → likely reward candidate
GSD / ASD               → pollen-transfer geometry candidates
resin removal           → interaction/reward-use measure, not automatically a plant barrier trait
seed predation          → antagonist response, not itself B_flower
```

A trait may be promoted to `B_flower` only after primary-source support shows
that it is a flower-specific barrier/resistance mechanism rather than an
attraction, reward, or pollen-transfer character.

## Concrete next evidence test

Obtain the article methods/supplement or inspect the public table headers in a
normal browser session. Then ask one constrained question:

> Does any independently measured blossom trait have a documented
> seed-predator-barrier function, separate from advertisement, reward, and
> pollen-transfer effects?

- **yes:** complete a D1 screen using the declared focal-blossom linkage;
- **no:** classify as an unusually strong `A_flower` + pollination + seed
  predation mechanism panel, but not as a direct `A_flower × B_flower` test.
