# BITA: Same-condition specialist mixtures versus a generalist wildtype in Pseudomonas

**Date:** 2026-11-15. **Status:** original published article statistics recovered and checked against original JATS; **not** the underlying Dryad XLSX or a new biological experiment. Draft empirical PR only.

## Exact scientific contrast

Mridha & Kümmerli (2022), *Journal of Evolutionary Biology*, DOI [10.1111/jeb.14001](https://doi.org/10.1111/jeb.14001), mixed engineered *Pseudomonas aeruginosa* specialists that produce only one of two siderophores: pyochelin (PAO1 delta-pvdD) or pyoverdine (PAO1 delta-pchEF), at initial pyochelin proportions 0, 5, 25, 50, 75, 95, 100%. The intact PAO1 generalist produces both siderophores. Four media differ in iron availability. Source original full-text JATS **PMC9323447**, [Europe PMC XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9323447/fullTextXML), SHA-256 **ff26c2e12bcd44bc7137656a7290ac9944ebc6823e8aae405e7a7f4ce999d55e**.

**Main community outcome:** relative productivity = 24-hour OD600 growth-curve integral of specialist culture divided by the WT growth integral in the same medium. Author design: **four experimental blocks**, 8 independent monoculture replicates and 12 mix replicates per medium × ratio, analyzed in the same study. T-test degrees of freedom below imply 74 or 72 analyzed treatment values; they are **neither 74 independent studies nor 74 independent origins of specialization**.

## Published test statistics re-extracted + newly calculated standardized departures

The original source gives a one-sample t test against WT-relative productivity = 1 for each iron condition. The new standardized value is **t / sqrt(df+1)**, a descriptive one-sample standardization inferred from the publication's t statistic and analyzed count, **not raw mean fold change or an independent pooled effect**.

| Medium | Author one-sample t vs WT=1 | Reported p | Derived standardized departure | Interpretation |
|---|---:|---:|---:|---|
| CAA + 100 μM FeCl3 (iron-replete) | t(73) = +12.17 | <0.0001 | **+1.41473** | Specialist cultures outperform WT, but neither siderophore is needed much |
| Plain CAA (moderate iron limitation) | t(73) = +1.819 | 0.0730 | **+0.21145** | No resolved WT/specialist difference, **not equivalence** |
| CAA + 100 μM 2,2'-bipyridyl | t(73) = −12.89 | <0.0001 | **−1.49843** | Specialist cultures underperform WT |
| CAA + 300 μM 2,2'-bipyridyl | t(71) = −6.745 | <0.0001 | **−0.79491** | Specialist cultures underperform WT |

The published Results section also reports a significant **medium × starting pyochelin fraction interaction** on community productivity: **F(3,286)=26.58, p<0.0001**. Within-medium authors' reported slopes of specialist relative productivity against initial pyochelin composition are **+0.0002, −0.0008, −0.0011 and −0.0054** (iron-replete, plain CAA, chelator 100, chelator 300). Thus adding more of the lower-iron-affinity pyochelin producer progressively reduces community performance under iron limitation.

**The key non-equivalence:** individual specialist **coexistence** is not a group **productivity gain**. The authors report negative frequency-dependence of pyochelin producer relative fitness under all four media (slopes **−0.0129, −0.0048, −0.0070, −0.0075**). Fitted within-experiment equilibrium percentages of pyochelin producers are **69.80%, 38.99%, 22.29%, 30.09%**. These fitted equilibria do **not** prove long-term genetic stability or superior specialist-group productivity. The study used fluorescent marker controls to correct fitness-measurement bias.

## Strong negative test for unconditional division-of-labour benefit

At **high iron availability**, the specialists save residual production cost and outperform WT; however, the iron-acquisition tasks are almost unnecessary. At **moderate iron scarcity**, the two specialist types can complement one another but do not show a significant superiority over the regulatory generalist. Under **strong iron scarcity**, the community pays a high cost when it contains many weak-affinity pyochelin producers despite frequency-dependent coexistence.

This is source-backed evidence that **interacting specialists + negative frequency dependence are insufficient to infer beneficial division of labor**, and that an intact generalist's **within-cell regulation** can compete against an externally assembled team of genetic specialists. It does not establish whether the regulatory mechanism actually evolved in response to this specific engineered specialization treatment, how adaptive costs are distributed at the gene-expression level, or which *historical* structural change was favoured.

### Comparison to opposite-condition published evidence: do not pool

- **Dragoš et al. (2018), *Bacillus subtilis***, [Curr. Biol. DOI 10.1016/j.cub.2018.04.046](https://doi.org/10.1016/j.cub.2018.04.046): engineered Δeps and ΔtasA mixture can **outperform WT pellicle productivity** near an intermediate mixing ratio (~30% TasA producers). Distinct organism and biofilm measurement, not a comparable Pseudomonas t effect.
- **Dragoš et al. (2018), same Bacillus research system**, [Nat. Microbiol. DOI 10.1038/s41564-018-0263-y](https://doi.org/10.1038/s41564-018-0263-y): during long-term evolutionary passaging, the earlier division-of-labour association can collapse as mutants evolve autonomy. **Not** a second independent structural origin.
- **Yang et al. (2020), *E. coli* chemostat ecotypes**, [AEM DOI 10.1128/AEM.00051-20](https://doi.org/10.1128/AEM.00051-20): evolved crossfeeding ecotype consortia can exceed the common ancestor in fitness and yield, but this is one shared evolutionary lineage, not independently replicated origins, and a different performance currency.

These **three organism-specific experimental programmes**, including an overlapping Bacillus follow-up, support **context-dependent benefits and maintenance constraints**, not a meta-analytically estimated probability of specialization or a universal common-effect coefficient.

## Original Dryad byte-level access audit

Official source: [Dryad DOI 10.5061/dryad.2bvq83bs4](https://doi.org/10.5061/dryad.2bvq83bs4), version ID **167943**. It advertises `Mridha_Kummerli_2022_JEB_raw_data_dryad.xlsx`, **328,288 bytes**, expected SHA-256 `b64f8febcc72f30394169d593de5a9ab7cbc3b753d5253dd865a711bc77887f9`, plus a 5,576-byte README.

Public file metadata **was** obtained, but anonymous retrieval of both official file APIs returned **HTTP 401**. The official UI file stream returned **HTTP 403** and a dataset-wide download returned **HTTP 401**. These are explicit authorization/access barriers, not evidence that the dataset or file is absent. No authenticated retrieval or anti-bot circumvention was attempted. **No direct raw replicate-level differences, mean productivity ratios, block-aware SE, original raw XLSX digest verification or original-data paired test can be reported.** The expected SHA listed in Dryad is not a verified local digest.

### Reproduction of *published statistic* layer only

- `scripts/analyze_bita_pseudomonas_published_stats.py` re-fetches exact primary-source Results from the SHA-pinned JATS and extracts four t statistics, two independent endpoint slope families and four fitted equilibria.
- `empirical/trait_architecture_history/mridha2022_published_stats_readout.json` freezes the derived readout and the HTTP access-gate statuses.
- `tests/test_bita_pseudomonas_published_stats.py` checks all four source conditions and fails closed on edited/missing source values.
- GitHub Actions audit `bita-pseudomonas-published-stats-audit.yml` recalculates the readout and compares it to the frozen JSON; separate source-intake workflow logs blocked retrieval **without creating fake biological observations**.

## Scientific boundary and next gate

Relative within-study t statistics, slopes and fitted coexistence are **evidence about the consequences of imposed specialization**. They do **not** estimate BITA's historical shared-to-specialist transition, the initial structure cost `K(u)`, genetic accessibility or the three conditional theoretical thresholds. Mixed communities may contain frequency-dependent exploitative specialists without an overall fitness dividend; the necessary criteria for division-of-labour advantage require separate measurement and appropriate comparison. A long-term adaptive origin additionally requires independent evolution history.

The raw Dryad original must be lawfully supplied/connected to rerun replicate-level matched comparisons; until then, retain the published-statistics evidence tier and no raw-data effect claim. No merge, no manuscript modification, no external data deposit or journal submission.
