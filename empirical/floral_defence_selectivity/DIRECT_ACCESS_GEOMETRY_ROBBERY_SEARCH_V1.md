# Direct access-geometry → robbery bounded search ledger v1

Search date: **2026-09-24**

Status: **bounded discovery search; not a systematic-review denominator**

## Question

Outside the two standardized access-routing networks, which independent empirical
studies directly test whether floral access geometry predicts bypass / nectar robbery?

## Search anchors

The search was seeded from:

1. the current BITA access-routing Letter references;
2. papers cited by Sakhalkar et al. for floral traits and cheating route;
3. Rojas-Nossa et al. (2016), a multi-community study explicitly centered on
   accessibility constraints and robbery;
4. forward/current searches through 2026-09-24 for corolla/tube length, floral
   access, mismatch, nectar robbing, robbery, thieving, flowerpiercers, sunbirds,
   hummingbirds and bumblebees.

## Query families

The bounded search used combinations equivalent to:

~~~text
"nectar robbing" AND ("corolla length" OR "tube length" OR morphology)
"nectar robbery" AND ("corolla length" OR "floral morphology")
"accessibility constraints" AND "nectar robbing"
"long corolla" AND "nectar robbing"
"effective corolla length" AND "robbing frequency"
"flowerpiercer" AND "corolla length" AND robbing
"sunbird" AND "long-tubed" AND robbing
"bumblebee" AND "corolla length" AND robbing
"Campsidium valdivianum" AND robbing AND morphology
"Lonicera implexa" AND robbing AND corolla
~~~

Backward citation chasing was used only to identify direct tests; every retained row
must satisfy the independent inclusion contract in
`DIRECT_ACCESS_GEOMETRY_ROBBERY_CONTRACT_V1.md`.

## Included discovery programs

The current bounded inventory contains 18 study programs spanning 2001–2026:

- Lara & Ornelas 2001 — experimental/natural hummingbird route switching;
- Urcelay, Morales & Chalcoff 2006 — bumblebee robbery across two
  `Campsidium` populations;
- Navarro & Medel 2009 — flower-level robbery in `Duranta erecta`;
- Geerts & Pauw 2009 — 13-species Cape sunbird guild;
- Lázaro, Vignolo & Santamaría 2015 — three `Lonicera implexa` populations;
- Rojas-Nossa, Sánchez & Navarro 2016 — 88 species across four communities;
- Castro, Silveira & Navarro 2009 — three `Polygala vayredae` populations;
- Carrió & Güemes 2019 — population flower-size test in `Antirrhinum valentinum`;
- Cuta-Pineda, Arias-Sosa & Pelayo 2021 — 16 Andean ornithophilic plants and
  four flowerpiercers;
- Valdivia, Carroza & Orellana 2016 — geographic trait-mediated `Fuchsia magellanica`
  robbery by `Bombus terrestris`;
- Stanley & Cosnett 2021 — flower-level `Fuchsia magellanica` robbery in Ireland;
- Tie et al. 2023 — individual-level `Caryopteris divaricata` variation;
- Valdivia, Orellana & Gantz 2025 — Chilean `Campsidium` direct null test;
- Coetzee et al. 2026 — 12 bird-pollinated `Erica` species across 27 populations;
- Navarro & Gómez 2026 — Galápagos `Kalanchoe pinnata`;
- Irwin & Adler 2006 — five-population `Gelsemium sempervirens` morphology null;
- Irwin, Warren, Carper & Adler 2014 — replicated suburban/wild `Gelsemium`
  field study with longer corollas receiving more robbery;
- Adler, Leege & Irwin 2016 — reciprocal-common-garden `Gelsemium` floral-size null.

## Important negative / non-promoted findings

The 2025 Chilean `Campsidium` study directly tested the predicted geometry effect
and found no significant association of corolla length with either small or large
robbery perforations. It is retained as `NULL`.

The 2009 `Polygala vayredae` study found a positive flower-size/robbery relation
in only one of three populations and is retained as `MIXED`.

The 2026 South African `Erica` study provides a genuine boundary-condition result:
in its primary population-level LMM, robbery was significantly **lower** in
longer-corolla populations (t = -2, p = 0.04), while a sensitivity model replacing
conspicuousness with discriminability rendered predictors non-significant. It is
retained as `OPPOSITE`, with the model-sensitivity caveat explicit.

Several potentially useful datasets were **not** promoted to the frozen network
statistic:

- community/pollination datasets without route-resolved robbery;
- datasets with <5 visitor species;
- one-plant systems;
- studies measuring only consequences of robbery rather than geometry → route use;
- the Rojas-Nossa 88-species study, because its response is plant-level robbery and
  it lacks the frozen visitor×plant mismatch estimand.

## Current descriptive inventory

~~~text
study programs = 18
positive        = 12
null            = 4
opposite        = 1
mixed           = 1

network-k contribution from this corpus = 0
primary standardized joint network k    = 2
~~~

These counts describe the current bounded inventory only. Three additional programs
were recovered in Stage-U batch 1 under the unchanged geometry contract. They are not
a success rate, prevalence estimate, sign test, or meta-analytic result.

Stage-U batch 1 also retains non-promoted records, including a duplicate 38-species
Andean precursor to the later Rojas-Nossa four-community program, studies of visual
nectar guides or nectar chemistry rather than access geometry, studies measuring
geometry without testing it in the robbery model, and comparative robber datasets
without flower-specific access mismatch. See
`DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv`.

## Next escalation gate

A formal directional recurrence test can be opened only after a separate finite search
frame is frozen, deduplicated, and audited for outcome-independent eligibility. Until
then this layer is mechanistic/direct empirical support only.
