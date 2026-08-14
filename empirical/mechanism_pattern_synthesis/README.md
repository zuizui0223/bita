# Mechanism-pattern empirical synthesis

This directory is the active empirical workspace for the theory-driven synthesis defined in `docs/MECHANISM_PATTERN_UNIVERSALITY_PROTOCOL_V1.md`.

The empirical target is **mechanism recurrence, same-system co-occurrence, direct `A x D` evidence, and context-dependent sign switching**. It is not one universal pooled coefficient for all floral attraction and defence traits.

## Current execution state

The workspace now contains both design contracts and source-audited empirical records.

```text
EVIDENCE_ARCHITECTURE_V1.csv
    fixed five-tier hierarchy

SEARCH_REGISTRY_V1.csv
    dedicated search families for direct A x D, same-system routes,
    each marginal mechanism, context switches and direct joint cost

MASTER_LEDGER_SCHEMA_V1.csv
    canonical row schema

MASTER_LEDGER_V1.csv
    first source-adjudicated seed records

LEDGER_BATCH_2_V1.csv
    direct-interaction and quantitative-route records recovered from
    historical reproducible branches / workflow artifacts

LEDGER_BATCH_3_V1.csv
    expanded quantitative / directional A-to-antagonist and
    D-to-antagonist records, including Cucurbita, Kessler Nicotiana,
    slippery-flower experiments and Asclepias cardenolide oviposition

SIGN_SWITCH_LEDGER_V1.csv
    within-study dose, reward, exposure, consumer and response-construct
    switches retained as dependent contrasts

DIRECT_AXD_AUDIT_V1.csv
    strict direct-interaction candidate adjudication

DIRECT_AXD_SEARCH_EXPANSION_READOUT_V1.md
    explicit taxonomy of why near-direct studies fail or pass the A x D gate

IMPATIENS_2018_DIRECT_AXD_REAUDIT_V1.md
    first verified Tier-1 observational direct A x D cluster

THEIS_2014_CUCURBITA_MULTIROUTE_READOUT_V1.md
    quantitative same-signal A-to-pollinator / A-to-antagonist pair

THEIS_ADLER_2012_FIGSHARE_ROUTE_READOUT_V1.md
    publisher-linked archive audit and directional main-experiment routes

KESSLER_2015_FACTORIAL_REAUDIT_V1.md
    closed strict-AxD orientation route plus retained same-system scent tracking

GELSEMIUM_2005_D_TO_ANTAGONISM_READOUT_V1.md
TAKEDA_2021_SLIPPERY_FLOWER_DEFENCE_READOUT_V1.md
    chemical and physical D-to-antagonist mechanism readouts

JOINT_COST_AUDIT_V1.csv
JOINT_COST_READOUT_V1.md
    direct-kappa search state; trait covariance is not treated as joint cost

SECONDARY_SYNTHESIS_MODULES_V1.csv
    existing published / deposited syntheses retained at their proper
    inferential level rather than pooled into the primary ledger

STATUS_AFTER_BATCH_2_V1.md
STATUS_AFTER_BATCH_3_V1.md
    completion-gate dashboards

COMPLETION_GATE_V1.md
    conditions that must be satisfied before manuscript reconstruction
```

## Current high-level result

The first three execution batches have established:

- one strict observational direct `A x D` cluster (`Impatiens capensis`), with opposite and individually unresolved point estimates across two reproductive components;
- eleven high-information direct-interaction candidates adjudicated under the strict flower-specific D gate, revealing distinct failure modes rather than one generic evidence shortage;
- two independent quantitative `A -> antagonism` anchors: exact-linked `Gymnadenia odoratissima` (`beta = 0.568`, `SE = 0.269`, `n = 1162`) and the source-reported *Cucurbita* sesquiterpenoid → cucumber-beetle coefficient (`beta = 2.91`, `SE = 1.28`);
- a same-*Cucurbita* quantitative attraction pair in which the same sesquiterpenoid axis also predicts squash-bee visitation (`beta = 0.096`, `SE = 0.034`);
- additional experimental attraction-tracking systems in Theis & Adler (2012) and Kessler et al. (2015), retained directionally when public source data do not support a defensible new effect reconstruction;
- chemical D-to-antagonist mechanisms in `Gelsemium` and `Asclepias` and a flower-specific physical-access mechanism in slippery `Codonopsis` / `Fritillaria` perianths;
- nine explicitly coded within-study conditionality patterns involving dose, reward, exposure duration, consumer identity, antagonist decision stage, outcome construct, and reproductive-component scale;
- zero verified studies directly measuring the theory's A+D allocation/construction cost `kappa`, despite several high-information joint-trait audits.

These are execution results, not prevalence estimates. Search saturation and metric-compatible multi-study quantitative synthesis remain incomplete.

## Active source audits

Two public-data audits are intentionally separated from biological inference:

- García et al. (2024), `Asclepias syriaca`: public Appendix I/II route for a same-individual floral-attraction + floral-latex panel. No `A x D` reanalysis is allowed until the source model and variable definitions are fixed from primary materials.
- Barlow et al. (2017), `Aconitum`: article-declared Figshare `10.6084/m9.figshare.5165350` for alkaloid and bumblebee bioassay data. This is the next priority for an uncertainty-bearing D-to-antagonist / D-to-pollinator module.

## Append-only evidence discipline

During active screening, new source-audited records are added in versioned batch ledgers. No historical source record is silently overwritten because a later audit changes its interpretation.

Before quantitative synthesis, batch ledgers will be validated and consolidated under the canonical master schema with unique `record_id` and study-independence checks.

## Relationship to existing branches

The workspace does not duplicate or erase earlier analyses.

- PR #124 remains the quantitative floral-antagonist-pressure / nectar-larceny environmental-gate module.
- PR #125 remains the source-audited `D -> pollinator` constituent-path module.
- Historical matched-panel and route-extraction branches are re-used only when their source linkage and analysis outputs are reproducible.
- `main` remains the frozen canonical theory/manuscript baseline until `COMPLETION_GATE_V1.md` is satisfied.

## Non-negotiable boundaries

```text
marginal routes != W_AD
same-system co-occurrence != direct A x D
one dual-function trait != two focal A and D axes
A x D reproductive component != total lifetime fitness
trait covariance != direct joint cost
publication count != model parameter
```

All subsequent extraction and synthesis work should preserve these boundaries.
