# BITA: Independent publisher-data recovery of coGFP duplication (2026-11-15)

**State: original-source numerical reanalysis, post-publication exploratory.** Neither a new laboratory experiment nor a pooled meta-analysis nor a validated evolutionary-origin mechanism.

## Original source and provenance

Mihajlovic et al. (2025), *eLife*, DOI 10.7554/eLife.97216.3, “A direct experimental test of Ohno's hypothesis”, compared single-copy and duplicated coGFP fluorescence evolution in *Escherichia coli*. The publication reports increased mutational robustness and variation under gene duplication, without a demonstrated acceleration in green-fluorescence improvement or blue/green copy specialization in tested variants. Figures 2 and 3 are different endpoints; the blue/green test is not numerically reconstructed here.

- Figure 2 original [publisher XLSX](https://cdn.elifesciences.org/articles/97216/elife-97216-fig2-data1-v1.xlsx): 11,684 bytes, SHA-256 d8ab8a5cd012654e32cd1bac2059bd423ea2731f0e3a00ee39134ce632138bee.
- Figure 3 original [publisher XLSX](https://cdn.elifesciences.org/articles/97216/elife-97216-fig3-data1-v1.xlsx): 15,762 bytes, SHA-256 8c9e9c84b4e2ed49684c580fc26863a871628a9a41125e9ead89f1c788c8bf32.
- [GitHub source-acquisition run #43681104303](https://github.com/zuizui0223/bita/actions/runs/43681104303) succeeded. Its source artifact includes XLSX bytes, worksheet-cell records and manifest. The separate reanalysis workflow reproduces the numeric readout.
- Source-cell CSV includes 30 Figure 2 values (5 generations × 3 independently evolved replicate lines × 2 copy-number conditions) and 36 Figure 3 values (6 generations × 3 lines × 2 conditions). Each record stores original worksheet and row.

**Independent unit: an evolved replicate line.** Generations, cells, alleles and variant observations are not new independent population replicates. The X/Y/Z naming is within each group; the group-label permutation treats six trajectories as exchangeable, conditional on the actual design. Its two-sided p values need not equal the source's Mann–Whitney p values.

## Results recalculated from the 66 original values

The exact two-sided label permutation enumerates 20 three-versus-three allocations, with smallest nonzero p = 0.10 for complete separation.

| Endpoint | Single copy | Two copies | Difference two minus single | Two-sided p |
|---|---:|---:|---:|---:|
| Figure 2 final generation: fraction of fluorescence-positive observations | 0.412978 | 0.468150 | +0.055172 | 0.10 |
| Figure 2 repeated-line trapezoid mean across generations 1–5 | 0.272876 | 0.362224 | +0.089348 | 0.10 |
| Figure 3 final generation: ancestor-normalized log10 fluorescence improvement | 1.452842 | 1.376865 | −0.075977 | 0.50 |
| Figure 3 repeated-line trapezoid mean across generations 0–5 | 0.548337 | 0.508966 | −0.039371 | 0.50 |

For the trajectory contrast, calculate one trapezoid time-average **within each line first**, and only then permute copy-number labels across six line-level summaries. Thus repeated generations do not inflate replication.

The direction of Figure 2 is positive for the two-copy group in all five sampled generations, while Figure 3 does not show a consistent two-copy improvement. Neither two-sided p value meets 0.05 with this sample size. **Absence of a detected improvement is not proof of equivalence or no possible fitness benefit.** The source's separately reported blue/green specialization result is not estimated from Figures 2 and 3. Neither endpoint is direct absolute organismal fitness.

## Biological inference and safeguards

An added copy may expand accessible mutational variants without guaranteeing faster improvement in the assayed phenotype, successful functional division, or an adaptive origin of two modules. This is **one independent experimental programme**, with two endpoints that are not interchangeable meta-analytic effect sizes.

Separate source-bound programmes remain:
- PR #364 Salmonella HisA/TrpF: 21/24 versus 10/24 physiological growth rescue by genetic background, unrelated measurement scale.
- PR #361 Peucedanum and cichlid analyses: ecological allocation and between-module morphology covariance, not architecture-origin transitions.
- Després et al. (2024) yeast Fcy1: engineered heteromeric restoration among selected mutant pairs, not a natural replication frequency.
- PR #363: mathematical differentiation benefit/entry/persistence conditions valid only in its specified exponential activation-cost model.

Cross-system registry: 8 publications, 7 research-programme families, 6 primary publication records representing 5 distinct research families, plus 2 contextual exclusions. This expansion newly quantifies **one experimental research programme** (Mihajlovic) and two source endpoints, but does not identify any matched-current-environment adaptation-history contrast, heritable organ-origin event, common empirical cost function K(u), or pooled BITA coefficient.

## Reproducibility

Source file: empirical/trait_architecture_history/mihajlovic2025_fig2_fig3_replicates.csv.

Frozen JSON: empirical/trait_architecture_history/mihajlovic2025_replica_reanalysis.json.

Code: scripts/analyze_bita_elife2025_replica_analysis.py.

Run from repository root:

    python -m scripts.analyze_bita_elife2025_replica_analysis
    python -m pytest -q tests/test_bita_elife2025_replica_analysis.py tests/test_bita_cross_system_registry.py

The original source XLSX bytes are retained as a GitHub Actions artifact. Verified code/tests and source-cell provenance do not substitute for independent biological replication or independently blinded coding.

**Publication boundary:** no update to the active nectar-robbery Letter, no merged PR and no external journal submission.
