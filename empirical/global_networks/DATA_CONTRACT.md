# Global interaction-network backbone: data contract

## Purpose

This module tests whether public plant--animal interaction networks can serve as the empirical backbone for the attraction--defence--assurance regime model.

The first empirical claims are deliberately narrow:

\[
A \longleftrightarrow \text{mutualist interaction structure}
\]

\[
D \longleftrightarrow \text{antagonist interaction structure}
\]

\[
\operatorname{Cov}(A,D) \longleftrightarrow \text{interaction regime}
\]

They are not direct claims about fitness, selection, or causal defence efficacy.

## Standard interaction contract

All source data must be converted to one row per plant--animal interaction with these required fields:

```text
network_id
interaction_type
plant_taxon
animal_taxon
```

Optional but strongly preferred fields:

```text
weight                # count, frequency, or standardised interaction intensity
sampling_period
citation_id
source_dataset_id
site_id
country
latitude
longitude
```

`interaction_type` may be `pollination`, `herbivory`, `florivory`, `seed_predation`, `plant_ant`, or another declared class. Different interaction types are separate layers by default.

## Network metadata contract

One row per `network_id`:

```text
network_id
region
country
latitude
longitude
sampling_period
sampling_effort
source_dataset_id
citation_id
```

A network without region is not usable for a geographic backbone analysis, even if its edge list is available.

## Trait contract

One row per accepted plant taxon:

```text
plant_taxon
trait_name
trait_value
trait_unit
trait_source
trait_observation_level
imputation_flag
```

At this stage, attraction and defence are trait *modules*, not fixed individual variables. For example, flower display, floral morphology, reward, spinescence, leaf toughness, LDMC, pubescence, and chemical information should never be silently collapsed into one score.

## Data-source roles

- **Web of Life / other network repositories**: candidate source for pollination, plant-herbivore, and related networks. The live site currently exposes network categories and download controls, but its download generation returned an error during the initial audit; therefore it is a candidate source, not yet an adopted pipeline dependency. citeturn338016view1turn598902view0turn598902view1
- **Published network supplements**: likely the most stable source for original weights, sampling metadata, and citations.
- **GloBI / broad interaction aggregators**: discovery and provenance expansion; do not treat pooled edges as a local network unless the original dataset and locality are retained.
- **TRY / trait repositories / primary trait supplements**: trait lookup; each trait requires its source and observed-versus-imputed status.

## Acceptance test

Run `examples/audit_network_backbone.py` after normalisation.

A source becomes a **backbone candidate** only if it supplies:

```text
>= 30 independent networks
>= 3 regions
>= 60% unique plant-taxon trait match rate
network metadata matched to edges
interaction type retained
```

Weighted interactions are needed for the model's interaction-intensity tests. Presence-only networks can support architecture and degree tests, but not intensity claims.

## Current decision

No public source has been adopted yet. The code is an ingestion-and-audit layer designed to make that decision reproducibly once a candidate bulk download or study collection is available.
