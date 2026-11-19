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
