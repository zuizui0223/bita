# Pineau 2024: original Figure 2 competition workbook audit

## Purpose and source
This continuation is a single-publication within-study sensitivity based on Pineau et al. (2024), Nature Ecology & Evolution, DOI https://doi.org/10.1038/s41559-024-02367-y. It does not create independent forward-evolution replicates and does not change the active BITA mechanism-identification manuscript or SLK theory.

Original author repository: https://github.com/Ratcliff-Lab/coexistence-paper . Fixed commit 071affa79f16f0a469f099058372a7488c35c0c2. Source workbook data_used_to_generate_figs_in_coexistence_paper.xlsx, Git blob SHA1 8f7d01b388489374aba210db96495f387d4338e2, separately SHA256-verified b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f, exact size 1,535,384 bytes. Authors' F2.m source Git blob SHA1 4b5dba14b244b335294ca28be52a77c5dc278d79.

Original MATLAB reads workbook worksheets F2A (standard oxygen) and F2C (high oxygen). It loops through 8 and 7 plot series respectively. Figure 2 caption reports n=8 and n=6; high-oxygen Methods describe five starting populations. These are not interchangeable denominators; biological and numeric distinctions must be source-audited.

## Scientific units
The 5 independent obligately aerobic founder evolution populations in the parent PR #380 produce the forward-phenotypic-divergence observation (3/5 positive). Competition Figure 2 uses a selected already-differentiated Small/Large PO-4 isolate pair. Each Figure 2 time series is a competition assay, not another independent evolved origin, not another research programme, and not a genotype-independent replicate.

## Audit specification
1. Verify original XLSX Git and SHA256 fingerprints. Parse author workbook cached XML cell values in ephemeral GitHub Actions; do not commit full source rows or raw workbook.
2. Recover F2A/F2C worksheet names, Excel numeric rows, active column counts, complete series counts and missingness.
3. Fit standard-oxygen large-frequency change against initial Large frequency, and compare with the author's fixed fitted equation: intercept +0.095083, slope -1.0274, zero crossing about 0.09255. Do not call recovery of an already published regression an independent experiment.
4. Recover F2C values and identify whether n=5, 6 or 7 can be distinguished from source cells. Where experimental labels are missing, do not invent them.
5. Preserve a separate confidence boundary for within-PO4 competition versus independently evolved founder lines. There is no uniform forward evolutionary origin probability or BITA startup K(u) estimate.

## Execution and no-promotion scope
Code: scripts/audit_bita_pineau2024_f2_workbook.py
Tests: tests/test_bita_pineau2024_f2_workbook.py
Actions: .github/workflows/bita-pineau2024-original-f2-workbook-cell-reanalysis.yml

Numerical readout requires an original-source success and frozen JSON roundtrip before any updated claim. The parent PR #380 verified the binary file but did not examine workbook cells. This is the missing cell-level audit, on an additive draft branch without manuscript changes, merge or submission.

## Source-verified numerical result (original workbook, 2026-11-19)

The original XLSX passes its SHA-256 and Git-object fingerprint gates. Its **actual F2A/F2C cells** were independently extracted: 12 total worksheets, 6 numeric rows in each of the two F2 source sheets (Excel rows 3–8), and two preceding title/header rows.

| Statistic | Standard O2 F2A | Supplemental O2 F2C |
|---|---:|---:|
| Complete individually labelled competition time series | **8** | **7** |
| Numeric missingness | 0 | 0 |
| Mean final Large proportion | **0.086606822375** | **0.856453980000** |
| First-last fitted intercept (Large frequency change) | 0.095083250789 | 0.960034108718 |
| First-last fitted slope | −1.027356337328 | −1.400728238925 |
| Fitted R-squared | 0.969136507334 | 0.656185604887 |
| Zero-change Large frequency | **0.092551383911** | **NOT interpreted as equilibrium** |

The standard-O2 raw-cell regression independently reconstructs the author script's previously frozen +0.095083 and −1.0274 coefficients. Its equilibrium is **9.255% Large**, and the range across eight leave-one-whole-competition-out fits is **7.877–11.349%**, a descriptive sensitivity rather than additional independent evolved populations.

The supplemental-O2 raw-cell average of **85.645% Large** agrees with the paper's approximately 86%. The F2C workbook columns are individually labelled highO2_1 through highO2_7, and all seven contain values in each of six observation rows. Therefore the published high-O2 n=6 (Figure 2 caption) versus n=5 (Methods) cannot be explained simply by excluding a blank column. There is no source-proven assignment of a pilot, duplicate, or exclusion, so this discrepancy is retained as **unresolved**.

### Exhaustive unknown-exclusion sensitivity

For any six of the seven complete high-O2 series, their mean final Large frequency ranges **0.837056–0.872289** (7 possible six-series subsets). For any five of seven, it ranges **0.820700–0.884273** (21 subsets). The pronounced increase in Large endpoint proportion is thus descriptively robust to arbitrary one/two-series omission. These are bounds over *hypothetical subsets*, not evidence identifying the actually published n=6 or n=5 groups. The observed difference of means from all seven high-O2 versus eight standard-O2 competition endpoints is **+0.76984716**, without a claim of independent evolution-population replication.

### High-oxygen extrapolation warning

A simple fitted high-O2 first-last regression gives a mathematical zero crossing near 0.6854, but the original high-O2 initial frequencies cover only **0.156–0.302**. This crossing is outside observed starting-frequency support, so it **does not estimate the high-O2 equilibrium** and cannot replace the directly observed endpoint mean 0.85645. The oxygen treatment tests composition and maintenance of an *already-diverged* PO-4 Small/Large pair, not the initial creation of two specialist architectures.

### Reproducibility trail

- First complete F2 source-cell reconstruction: [Actions #44479660022](https://github.com/zuizui0223/bita/actions/runs/44479660022), SUCCESS.
- Complete source refit plus n5/n6 exhaustive subset bounds: [Actions #44480077320](https://github.com/zuizui0223/bita/actions/runs/44480077320), original-source data and numerical generation succeeded, but the old synthetic testing fixture failed when a new LOO subroutine expected at least four complete series.
- The synthetic fixture was corrected. [Actions #44480179972](https://github.com/zuizui0223/bita/actions/runs/44480179972), SUCCESS.
- Exact derived JSON frozen under empirical/trait_architecture_history/pineau2024_f2_workbook_source_reanalysis.json; further CI requires an exact original-source-to-frozen roundtrip.

**Ceiling:** This cell-level audit is a new *analysis within one source*, not a new publication, independent founder-line success, genetic module duplication, historical two-function architecture divergence origin rate, or independently calibrated BITA/SLK K(u) parameter. The forward origin-level denominator remains 3/5 original aerobic evolution populations, and the competition analyses remain within a selected PO-4 pair.
