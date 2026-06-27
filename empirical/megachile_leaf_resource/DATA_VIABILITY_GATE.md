# Megachile leaf-material data viability gate

## Purpose

Do not promote a discovery route because it produces interesting anecdotes. A route is adopted only when it can support the intended estimand:

\[
\Pr(\text{leaf-material use} \mid \text{plant traits},\;\text{availability},\;\text{site}) .
\]

This is not a species-specific host-preference claim unless bee species is independently resolved.

## Minimum analysis-ready standard

A passive-data route must provide all of the following:

1. at least **50 independent plant species** with a species-level positive or negative/use-availability outcome;
2. at least **five spatially distinct sites or study regions**, or a single explicitly replicated experiment;
3. an explicit denominator: surveyed/available plants, not positives alone;
4. direct material use or a validated leaf-cut signature;
5. a record-level or site-by-plant table, rather than only prose summaries;
6. site and observation metadata sufficient for a random-effect or stratified analysis.

A set of plant-use anecdotes cannot be treated as an availability-corrected trait analysis.

## Tests completed

| Route | Outcome | Decision |
|---|---|---|
| species-specific English literature queries | sparse behaviour information; no verified plant-by-use table | reject as primary route |
| Japanese structured natural-history pages | direct material action recovered, but plant identities usually absent or genus-only | retain only for material-mode classification |
| broad genus/common-name web search | generic information and taxonomic noise; no verified trait-ready record in the tested set | reject |
| claimed published community surveys | candidate citations exist, but no independently verified raw record table and availability denominator has yet been recovered | keep as lead list, not data |

## Consequence

Passive sources have not passed the analysis-ready gate. Do **not** lower the thresholds just to keep the retrospective project alive.

## Pivot: standardized sentinel-plant experiment

The viable primary route is a replicated field experiment in which availability is designed rather than inferred.

### Unit

A plant individual or clipped leaf panel of a known species, exposed for a fixed time window beside occupied/likely Megachile nesting habitat.

### Minimal layout

```text
6 sites
× 10 plant species (trait-stratified panel)
× 8 replicate plants or panels per site
× 3 repeated survey windows
= 1,440 exposure units
```

Record for every unit:

```text
site, date window, plant species, replicate,
leaf area offered, visible leaf-cut discs, disc area removed,
bee observation/photo when available,
other herbivore damage, plant phenology, microhabitat
```

The primary response is not a post hoc host list:

\[
Y_{isr} = \text{presence/area/count of diagnostic leaf cuts}
\]

with plant traits as fixed effects and site/window/species as structured terms as appropriate.

### Validation subset

At every site, pair a subset of panels with time-lapse imaging or direct observation. This estimates the positive predictive value of the diagnostic damage signature and keeps non-Megachile herbivory from silently becoming response data.

## Adoption rule

Adopt the field route once a 2-site pilot demonstrates both:

- diagnostic leaf-cut observations or camera confirmations in at least 10 exposure units; and
- at least 80% agreement between panel damage classification and the validation subset.

If this pilot fails, the question is revised from leaf-material choice to material-use mode / nesting ecology rather than forcing a trait-selection analysis.
