# Observation-first discovery protocol

## Why this branch exists

The initial literature-first pilot was too sparse for plant-level records. A direct-action search of Japanese observation sources was more productive: one checked source reports *Megachile tsurugensis* cutting a **Lespedeza** species in Hyogo, and also documents leaf transport/cutting in Saga; a second checked source documents *M. nipponica nipponica* carrying a cut leaf but does not identify the plant.

This changes the workflow from:

```text
species name -> literature -> host plant
```

to:

```text
observation source -> direct material action -> review -> plant identification when available
```

## Two linked evidence layers

### 1. Material-action ledger

Use this for any observation that identifies a bee and shows or explicitly describes a material-use action:

```text
leaf_cutting_direct
leaf_transport_direct
petal_cutting_direct
resin_collection_direct
nest_lining_direct
nest_material_delivery_direct
```

A plant name is optional here. This layer answers: *which bee taxa have direct evidence of leaf/petal/resin material use in Japan?*

### 2. Plant-use ledger

Use only when the plant is identified in the source text or image review. This layer feeds the plant trait analysis.

A record can be strong material-action evidence but unusable for plant-trait analysis because the plant is not named. Such records are retained as biology/context, not discarded.

## Source tiers

```text
T1: peer-reviewed article, museum/institutional record, curated taxonomic-natural-history source
T2: expert natural-history site with original image, locality, date, and explicit behaviour description
T3: public observation/photo with direct action visible but uncertain taxon or plant identity
T4: generic damage photo, repost, or untraceable statement
```

T1--T2 can seed review. T3 stays as discovery evidence until independently checked. T4 is excluded.

## Triage rules

A candidate can be marked:

```text
material_action_confirmed
plant_identified
plant_unidentified
species_unresolved
needs_image_review
needs_source_review
excluded
```

Only records with `material_action_confirmed` and `plant_identified` can enter the primary host-plant universe.

## Pilot stopping rule

Search one structured natural-history source with species pages plus two broad image/observation searches. If at least three direct-action records and at least one plant-identified record are found, continue observation-first expansion. If not, pivot to a different source class rather than merely adding more keywords.
