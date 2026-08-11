# Villalona et al. 2020 raw-data audit

## Status

**Source complete; not a primary preference-pool effect. The manuscript remains frozen.**

This audit concerns Villalona et al. (2020; doi: `10.1007/s00442-020-04701-0`) and the public ScholarSphere deposit identified in the article (`10.26207/pgeq-he51`). The publisher supplement and all three preference-trial raw tables are now recovered. No values in this audit are read from a graph.

The study contributes one independent biological cluster:

```text
Villalona_2020_milkweed
```

It is kept in the **nectar-consumption lane**, because the pre-existing protocol explicitly separates nectar volume consumed from binary choice proportion, visit number, residence time, pollen transfer and reproduction.

## Source recovery

The public ScholarSphere record exposed three files. They were recovered through their verified public file-version routes and preserved in GitHub Actions artifact `9086314724` (run `31450988558`).

| Source file | SHA-256 | Role |
|---|---|---|
| `Raw_Data_Files_FieldPreferenceToxicity.xlsx` | `6b6bf17bd77ca6c6fe08eb2a5e64be1a25987e532e0d92abd6ea76da2e028a13` | workbook containing preference, toxicity and visitation tables |
| `OECO-D-20-00056R1_AssociatedData_Archival.zip` | `81071cd5385438eeb44de0d02c43d6e477c952d2413c2394633926e942aaa662` | lossless CSV archive used for this audit |
| `iNaturalistRecords.xlsx` | `700fc7aaea2a098cec5b5e46ff324facb166f68c7dba76bb4b75f370db012592` | external field-observation context |

`VILLALONA2020_SOURCE_RECEIPT_V1.json` records file sizes, checksums, CSV row counts and the exact experimental inventory.

## Experimental inventory

| Trial | Year | Species | Bees per species | Dose set (ng/uL) | Repeated measurements | Raw rows |
|---|---:|---|---:|---|---|---:|
| Trial 1 | 2018 | *B. griseocollis*, *B. impatiens*, *B. bimaculatus* | 10 | 0, 25, 100, 1000 | 24, 48, 72 h | 360 |
| Trial 2 | 2019 | same three species | 8 | 0, 25, 100 | 24, 48, 72 h | 216 |
| Trial 3 | 2019 | *B. griseocollis*, *B. impatiens* | 10 | 0, 1000 | 24, 48, 72 h | 120 |

Every bee has one record for every offered dose at every measurement time in its trial. Dose, species and time effects are therefore dependent within a study and must not be counted as independent replication.

## Source-model audit

The exact ANOVA and Tukey results in the recovered supplement, together with raw-data totals, are recorded in `VILLALONA2020_SOURCE_AUDIT_V1.csv`.

### Trial 1: 0, 25, 100 and 1000 ng/uL

- *B. griseocollis*: cardenolide effect `F(3,99)=62.20`, `p<0.0001`. The source groups 0, 25 and 100 ng/uL together and separates 1000 ng/uL.
- *B. impatiens*: `F(3,99)=9.73`, `p<0.0001`, with the same source grouping.
- *B. bimaculatus*: `F(3,99)=0.89`, `p=0.448`; no detected treatment effect.

The raw 72-h totals agree with that interpretation. For *B. griseocollis*, mean total consumption was 384.9 uL at control, 465.7 at 25, 372.3 at 100 and only 6.0 at 1000 ng/uL. For *B. impatiens*, the corresponding means were 169.8, 224.5, 235.3 and 52.8 uL. Thus the negative response occurs at 1000 ng/uL, not across the 0--100 ng/uL range.

### Trial 2: 0, 25 and 100 ng/uL

- *B. griseocollis*: `F(2,56)=0.57`, `p=0.6403`.
- *B. impatiens*: `F(2,56)=4.60`, `p=0.0141`; Tukey grouping is 25 ng/uL = A, 100 ng/uL = B and control = AB.
- *B. bimaculatus*: `F(2,56)=0.42`, `p=0.657`.

The source-supported natural-range result is therefore not a general monotonic deterrence effect. In *B. impatiens*, the significant treatment term reflects higher consumption at 25 than at 100 ng/uL, while the control is intermediate. The other two species show no detected treatment effect.

### Trial 3: 0 versus 1000 ng/uL

- *B. griseocollis*: `F(1,45)=646.49`, `p<0.0001`, with a dose-by-time interaction.
- *B. impatiens*: `F(1,45)=6.88`, `p=0.0119`, also with a dose-by-time interaction.

Mean 72-h consumption at 1000 ng/uL was approximately 3% of control in *B. griseocollis* and 60% of control in *B. impatiens*. These are elevated-dose results and are not used to characterize the sign expected at field-relevant concentrations.

## Toxicity context

The raw toxicity table codes 0 = dead, 1 = alive without recorded sickness and 2 = sick. That coding reproduces the mortality percentages stated in the primary article.

At 48 h:

| Species | Dose (ng/uL) | Alive | Sick | Dead | Mortality |
|---|---:|---:|---:|---:|---:|
| *B. impatiens* | 1000 | 6 | 5 | 9 | 45% |
| *B. impatiens* | 2000 | 0 | 2 | 18 | 90% |
| *B. griseocollis* | 1000 | 19 | 1 | 0 | 0% |
| *B. griseocollis* | 2000 | 10 | 7 | 3 | 15% |

The strong consumption reductions at 1000 ng/uL must therefore remain labelled as supra-natural/toxicity-range responses, especially for *B. impatiens*. `VILLALONA2020_TOXICITY_CONTEXT_V1.csv` preserves all available 48-h dose-by-species counts.

## Descriptive raw-data contrasts

`VILLALONA2020_72H_CONTRASTS_V1.csv` reports **every** non-zero dose against the simultaneous 0 ng/uL control after summing the three 24-h intervals within each bee. No contrast is selected as primary, no dose is counted as an independent study and no post-recovery significance claim is made. These raw-unit contrasts are retained only to make the source direction auditable.

Exact interval-level observations remain in the recovered public CSVs; the committed 72-h contrast table is the compact derived audit used here.

## What this study establishes

Villalona 2020 now supports a source-complete and narrower statement:

> Milkweed-associated cardenolide exposure does not produce a fixed negative pollinator-consumption response. Across 0--100 ng/uL, effects are absent or non-monotonic and differ among bumble-bee species. Strong reductions occur at 1000 ng/uL, a source-identified elevated range that overlaps sickness or mortality.

This is direct empirical support for context dependence in a constituent biological route. It is not evidence that attraction and defence are complementary or substitutable in a population, and it does not estimate `iota`, `rho`, `kappa` or `W_AD`.

## Pooling decision

```text
independent study clusters added:          1
outcome lane:                              nectar consumption
primary preference/choice pool eligible:   no
reason:                                    pre-existing outcome-lane separation
dose/species effects counted as studies:   no
raw source recovery complete:              yes
```

The correct next step is a different independent source with a compatible preference/choice or visitation endpoint. Further re-analysis of Villalona cannot increase the independent-study count.

## Manuscript decision

No manuscript text, figure, journal framing or submission material is changed. Manuscript work remains frozen under `ANALYSIS_COMPLETION_GATE.md`.
