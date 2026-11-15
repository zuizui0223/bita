# BITA independent programme map — 15 November 2026

**Status:** source-audited evidence map; theory PR #363 and experimental Salmonella PR #364 are preserved. **Not** a finished quantitative meta-analysis or proof of the historical origin of new trait axes.

## Result of widening beyond one enzyme family

The catalogue now has **eight publication rows / seven research-programme families**. Six publication records belong to **five distinct primary programme families**; two further publications are relevant context but excluded from the primary two-function architecture synthesis. The two Näsvall publications come from one related Salmonella research family and do not constitute independent evolutionary-origin replications. An additional **independent source experiment** (Mihajlovic 2025) now contributes two non-poolable replicate-line contrasts extracted from original Figure 2/3 workbooks. No matched-history/hysteresis test is identified.

| Family / primary source | Independent evidence actually supported | Status and inference boundary |
|---|---|---|
| *Salmonella* HisA/TrpF — Näsvall 2012 and Näsvall & Abdalaal 2026 | Both specialized copies and improved bifunctional gene variants described in the older programme; 2026 experiment 2 shows genotype-background-associated physiological rescue (21/24 vs 10/24) and alternative gene route usage | **Already quantified in PR #364**, but different starting constructs/selection designs are not exchangeable; not a historical-origin fitness threshold |
| *E. coli* coGFP — Mihajlovic et al. 2025 | Experimental one- vs two-functional-copy contrast; duplication increases mutational robustness and diversity, but normalized green-fluorescence improvement is not faster; blue/green copy specialization not detected in assayed dual-colour variants | **Independent negative/boundary case**; figure 2/3 original source XLSX links known, original publisher XLSX bytes verified and n=3+3 independent-line contrasts recovered: robustness final +0.05517 (two-sided exact p=0.10), ancestor-normalized fluorescence final -0.07598 log10 (p=0.50) |
| *S. cerevisiae* Fcy1 — Després et al. 2024 | Engineered homodimer-to-heteromer compensation between two individually loss-of-function copies; **207 selected functional variant pairs among at least 613 independent crossing events**, with structural evidence for heteromerization | **Independent architecture-possibility case**. 207 pairs are not evolutionary transitions, and 613 selected events are **not** an unbiased denominator for natural frequency. Does not establish that a conflict favoured or historically caused this architecture |
| *Peucedanum multivittatum* — Kudo & Shibata 2025 | Within-phenotype floral allocation versus seed-predation opportunity; number of perfect flowers explains much of apparent egg association | **Previous independent data reanalysis in PR #361**; five plots, not independent organ-origin events |
| Cichlid oral/pharyngeal jaws — Conith & Albertson 2021 | Anatomically distinct modules retain phylogenetically adjusted morphological covariance: RV5=0.145319 over 87 PIC vectors from 88 species | **Previous independent source/tree reanalysis in PR #361**; not a measured genetic cross-talk parameter nor an independent origin per species |

Two documented context-only rows are **excluded from the core denominator**: Tong et al. (2025) on whole-genome duplication and multicellularity (whole-genome dosage, not assignment of two functions to two trait coordinates) and Fragata et al. (2014) on convergence of life-history traits under laboratory selection (history effects without two-function architecture coding).

## Why no pooled effect

A gene-background rescue probability, dual-colour protein fluorescence, reconstituted Fcy1 enzyme activity, number of predator eggs and morphometric PIC covariance are **five different estimands**. Their raw numbers cannot be converted into a biologically interpretable common trade-off coefficient, specialization effect, or shared-vs-separated fitness margin. A study count of five is not meta-analytic replication, and repeated generations/variants/populations within one study must not increment cross-study k.

The source list is **not** a systematic search or representative sample of natural strategies: cases were purposefully retrieved to challenge a universal narrative. Null/negative cases are retained. No cross-system positive fraction is computed.

## Mechanistic reading allowed

- Functional conflict does **not** imply new permanent modules.
- Additional copies can change the **accessible variation** without accelerating the measured phenotype or yielding copy specialization.
- Two distinct subunits can support a function through complementarity, potentially via a near-neutral architecture path rather than net adaptive improvement.
- Allocation and residual integration are distinct evidence layers; neither identifies an ancestral single axis converting to a novel heritable architecture.

None of the above estimates the exponential startup cost `K(u)`, its shape `tau`, the experimental BITA entry/fold/global thresholds, or a history-matched lineage effect. Previous theoretical thresholds remain conditional model results only.

## Primary sources, provenance and next data gate

1. Näsvall et al. 2012: https://doi.org/10.1126/science.1226521 . 2026 experiment 2: https://doi.org/10.1093/g3journal/jkag167 . Source-table reanalysis and dependence ledger in PR #364.
2. Mihajlovic et al. 2025: https://doi.org/10.7554/eLife.97216.3 . Published figures source page: https://elifesciences.org/articles/97216/figures . Original author data URLs: `https://cdn.elifesciences.org/articles/97216/elife-97216-fig2-data1-v1.xlsx` and `...fig3-data1-v1.xlsx`. The isolated `.github/workflows/source-intake-elife-97216.yml` retrieved original SHA-256-pinned files and retained source XLSX + worksheet-cell artifacts. Source SHA-256: Figure2 `d8ab8a5cd012654e32cd1bac2059bd423ea2731f0e3a00ee39134ce632138bee`, Figure3 `8c9e9c84b4e2ed49684c580fc26863a871628a9a41125e9ead89f1c788c8bf32`. Extracted 30 and 36 cell-level replicates respectively; machine-readable source data CSV is in `empirical/trait_architecture_history/mihajlovic2025_fig2_fig3_replicates.csv`. Results and all original bytes remain source-auditable.
3. Després et al. 2024: https://doi.org/10.1126/science.ado5719 . Author computation repository: https://github.com/Landrylab/Despres_et_al_2024 . The reported variant-pair counts arise from a selected experimental screening design; they are not natural prevalences.
4. Kudo & Shibata 2025: https://doi.org/10.1111/1365-2745.70130 . Original HUSCAP deposit https://doi.org/10.14943/hu95572 .
5. Conith & Albertson 2021: https://doi.org/10.1038/s41467-021-25755-5 .
6. Context only — Tong et al. 2025: https://doi.org/10.1038/s41586-025-08689-6 ; Fragata et al. 2014: https://doi.org/10.1371/journal.pone.0096227 (Dryad https://doi.org/10.5061/dryad.kn03t).

Reproduce the source independence audit:

```bash
python -m scripts.audit_bita_cross_system_registry
pytest -q tests/test_bita_cross_system_registry.py
```

**Decision:** keep the empirical and theoretical PRs as Draft. Original source workbook bytes were recovered for eLife Figures 2/3; the next admissible quantitative work is replicate-line inference and independent-source extension with common outcome boundaries. Independent original-source review and claim coding remain necessary. This registry does not alter the active nectar-robbery Letter or imply manuscript submission.
