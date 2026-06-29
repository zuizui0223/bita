# Evidence-first data pipeline for leaf-material-use synthesis

## Why the metadata-first design is insufficient

A bibliographic metadata search is only a **seed generator**. It is not the data pipeline.

The usable scientific object is not a paper. It is a verified, linkable **evidence unit**:

\[
(\text{bee/material guild},\; \text{plant taxon},\; \text{place-time},\; \text{action or cut mark},\; \text{sampling denominator},\; \text{source}) .
\]

A paper can contain zero, one, or many such units; one evidence unit can also be supported by a supplement, repository dataset, photo, field table, and original citation simultaneously.

## Endpoint-first separation

The pipeline produces three different data products. They must not be pooled before their denominators are compatible.

| Product | Required evidence | Permitted question |
|---|---|---|
| **E1: direct material-use event ledger** | direct cutting, transport, nest-material, or diagnostic cut mark; plant ID; locality or study | Which plant taxa are documented as used? |
| **E2: study-level use panel** | E1 plus plant-level count or binary response and sampling effort | How does observed use vary among plant taxa within studies? |
| **E3: selection panel** | E2 plus a defined available/background plant pool or inspected-but-unused plants | Which plant traits predict use relative to local availability? |

E1 is evidence discovery. E2 supports comparative models with study effects. E3 is the only product that supports a preference/avoidance claim.

## Source graph rather than one search route

Each seed item is expanded through a source graph:

```text
seed publication / repository / interaction record
  ├─ full text and supplement
  ├─ cited references
  ├─ citing studies
  ├─ linked dataset DOI / accession
  ├─ author project page / institutional repository
  ├─ original natural-history source
  └─ taxonomic synonym and material-mode terms
```

The source classes are intentionally complementary.

1. **Structured study datasets**: published surveys, trap nests, DNA barcoding, standardised damage surveys.
2. **Literature graph**: seed papers plus backward/forward citation chasing, not keyword search alone.
3. **Repositories and supplements**: Dryad, Zenodo, Figshare, institutional archives, appendices, machine-readable tables.
4. **Curated interaction sources**: discovery only unless provenance, location, and action type are retained.
5. **Citizen-science photographs**: discovery/calibration only unless bee, plant, direct action, time, place, and license are retained.
6. **Targeted new field data**: a standardised sentinel-plant + local flora + trap-nest design if E3 cannot be built from public data.

## Screening is active, not passive

The next source is chosen by expected information gain, not raw hit count.

### Study card fields

Every candidate becomes a study card before detailed extraction:

```text
source_id
seed_type
source_route
study_landscape_id
region
sampling_period
bee/material resolution
plant resolution
action/cut-mark criterion
response type
sampling denominator
availability/background definition
raw-table status
linked-data status
citation-neighbour status
E1/E2/E3 eligibility
uncertainty and exclusion reason
```

### Adaptive route policy

For each route, screen 15 **high-information** candidates rather than 25 arbitrary metadata hits.

A candidate is high-information when title/abstract/repository metadata indicates at least one of:

- plant-level table or supplement,
- quantified cut marks / material occurrences,
- explicit flora or availability survey,
- trap-nest material identification,
- DNA/metabarcoding material identification,
- study-level locality and sampling design.

After 15 cards:

- **>= 3 E2/E3 studies**: expand the route and citation-chase every eligible study.
- **1–2 E2/E3 studies**: retain as a secondary route; harvest linked datasets and author contacts; move to the next route.
- **0 E2/E3 studies but >= 3 E1 sources**: retain as an interaction ledger route only.
- **0 useful sources**: stop the route.

## Data acquisition ladder

For an eligible study, acquisition must proceed in this order:

1. downloadable table / supplementary spreadsheet;
2. linked repository or accession;
3. machine-readable appendix or PDF table extraction;
4. author contact requesting the plant-level table and availability data;
5. figure digitisation only for a clearly defined aggregate response, marked as digitised;
6. exclusion if the response or denominator cannot be recovered.

A study does not become E2 or E3 merely because it reports a qualitative plant list.

## Meta-analysis readiness is a design question

Readiness is not defined only by total record count. The registry must show:

- enough independent study-landscapes;
- within-study plant contrasts;
- trait coverage after taxonomic reconciliation;
- denominators or availability for the desired endpoint;
- variation in region and study design;
- no single study contributing most records.

Before any pooled model, run a simulation using the observed registry structure to estimate whether a plausible trait effect can be separated from study heterogeneity. If the simulation shows the current structure cannot identify the effect, collect more E3 data or switch to a descriptive E1/E2 synthesis.

## Immediate next experiment

Start with three deliberately different seed sets in parallel:

A. known community-level cut-mark survey papers;
B. trap-nest / nest-material identification papers;
C. studies with DNA or microscopy identification of nest material.

Build 15 high-information study cards per set, extract E1/E2/E3 status, then choose the first route to expand. Crossref/OpenAlex-style metadata search is only one way to generate seeds for A–C; it is never the entire discovery process.
