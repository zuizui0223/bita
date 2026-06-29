# Functional-trait request scope

## Goal

Request **record-level** trait data for the oriented Web of Life plant manifest,
then let the receipt audit decide which traits are usable. The request is not a
promise that all listed traits will enter the first analysis.

## Priority 1: likely global functional-trait backbone

These are the first traits to request because they map to predeclared modules
and have the clearest path to broad cross-taxon coverage.

| Trait-role ID | Functional channel | Request concept | First empirical use |
|---|---|---|---|
| `flower_size` | `A_flower` | individual flower, corolla, or capitulum size with exact measurement label and unit | pollination-network structure; florivory sensitivity |
| `inflorescence_display` | `A_flower` | flower number, inflorescence length/area, or other display quantity with exact definition | pollination-network structure |
| `sla` | `Q_leaf` | specific leaf area or leaf mass per area, preserving which quantity was supplied | leaf-herbivore structure |
| `ldmc` | `Q_leaf` | leaf dry matter content | leaf-herbivore structure |
| `leaf_n_mass` | `Q_leaf` | leaf nitrogen concentration on a dry-mass basis | leaf-herbivore structure |
| `leaf_thickness` | `Q_leaf` | leaf thickness and its unit/protocol | leaf-herbivore structure |

`leaf_p_mass` is a Priority 1 extension if the receipt audit shows enough direct
coverage after taxonomic reconciliation.

## Priority 2: scientifically valuable but expected to be sparse or heterogeneous

| Trait-role ID | Functional channel | Why conditional |
|---|---|---|
| `floral_access` | `A_flower` | geometry measures are not automatically unit-compatible across sources |
| `nectar_reward` | `A_flower` | volume, concentration, and sugar amount are distinct quantities |
| `floral_colour_contrast` | `A_flower` | categorical labels are not equivalent to reflectance/contrast measurements |
| `leaf_toughness` | `B_leaf` | force/area/protocol must be harmonised |
| `leaf_trichomes` | `B_leaf` | type, location, and glandular state matter |
| `secondary_metabolites` | `B_leaf` | compound classes and assays are not globally interchangeable |

These may enter a predeclared sensitivity, clade-specific, or source-specific
analysis only after a separate harmonisation decision.

## Not requested as first global predictors

Do not promote these into the first global request merely because they are
biologically interesting:

- pollination syndrome;
- leaf mottling/variegation;
- generic leaf area, lobing, or shape as a defence proxy;
- floral/involucral spines, floral sticky secretions, or flower trichomes as a
  presumed global layer;
- leaf spines as a generic insect-defence proxy;
- stem/wood resistance traits for borers;
- leaf-cutting-bee material suitability.

They remain focused future cases or conditional modules, as recorded in the
trait-role evidence matrix.

## Request and normalisation requirements

For each provider export, retain or recover:

```text
provider trait label
value and unit
record identifier / dataset / publication provenance
observation level
measurement method where available
taxon name returned by provider
provider accepted name / synonym mapping where available
```

Normalise only after retaining the raw export. Map values to the stable
`trait_id` values using `trait_receipt_template.csv`; retain provider labels and
conversion notes in the optional provenance fields. Do not impute missing values
before running `audit_trait_receipt_coverage.py`.
