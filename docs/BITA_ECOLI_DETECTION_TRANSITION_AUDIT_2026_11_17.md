# E. coli auxotrophy: first detection, re-detection, and consecutive detection (2026-11-17)

**Single-source, exploratory continuation of PRs #376–377.** The parent research programme is D'Souza & Kost (2016), *PLOS Genetics*, DOI [10.1371/journal.pgen.1006364](https://doi.org/10.1371/journal.pgen.1006364). The parent branch recovered original publisher Figure 2 (SHA-256 `71da8f3c1707d1ade887d4030446d1869f9fd33b05fa8cfed6fb3cd49823bd8b`) and classified **96 observed cells** from **16 independently evolved populations** (8/arm). That original source audit reports two unresolved source discrepancies, kept intact here.

## Core result: the phenotype-detection signal is not equivalent to sustained genotype persistence

| Among successive sampled generations | AA supplied (8 populations) | No-AA (8 populations) |
|---|---:|---:|
| Not detected → detected (0→1) | **10** | **3** |
| Detected → detected (1→1) | **2** | **0** |
| Detected → not detected (1→0) | **4** | **3** |
| Not detected → not detected (0→0) | **24** | **34** |
| **Total observed adjacent transitions** | **40** | **40** |
| Populations detected at any time | 7/8 | 3/8 |
| Populations detected on ≥2 sampled generations | **4/8** | **0/8** |
| Populations with ≥1 consecutive positive pair | **1/8** | **0/8** |
| Positive at generation 2,000 | 6/8 | 0/8 |

The first two columns are **counts of status transitions, not independent experimental replicates**. They each represent five time-interval assessments of the same eight evolving populations.

The complete partition of positive inspection cells is:

- **AA supplied: 12 positive inspections = 7 first observed detections of distinct populations + 3 re-detections after an intervening observed negative + 2 positives immediately following a previous positive.**
- **No-AA: 3 positive inspections = 3 first observed detections + 0 re-detections + 0 consecutive positives.**
- The two 1→1 pairs both arise from **the same AA R3 population** (positive at generations 1,000, 1,500, and 2,000). They are not two independent cases of persistence.
- The three gap-following re-detections occur in AA **R2, R4, and R8** (positive at 1,000, negative at 1,500, positive at 2,000). These patterns can arise through frequency fluctuations around a detection threshold; they do not demonstrate extinction and de novo reappearance of a genotype.

This makes the prior wording **"persistent auxotrophic mutants" inappropriate** for the reconstructed figure. The defensible observation is *detectable phenotype at repeated or late sampled generations*.

## Whole-population exact tests and widened multiplicity sensitivity

For each outcome, **all C(16, 8) = 12,870 whole-population arm reallocations** were enumerated. No colony, timepoint, or transition is used as an independently reallocated unit. Two-sided tests assume exchangeable population treatment labels; the experiment has only one independently published programme.

| Population-level score | AA sum | No-AA sum | Raw exact two-sided p | Eight-view max-|T| p |
|---|---:|---:|---:|---:|
| Positive inspections across six generations (parent) | 12 | 3 | 0.023776 | **0.061072** |
| Positive inspections at generations 1000, 1500, 2000 (parent) | 12 | 2 | 0.012121 | **0.020513** |
| Ever detected population (parent) | 7 | 3 | 0.118881 | 0.240870 |
| Final generation 2000 (parent) | 6 | 0 | 0.006993 | **0.013986** |
| 0→1 transition count | 10 | 3 | 0.039161 | **0.066667** |
| 1→1 transition count | 2 | 0 | 1.000000 | 1.000000 |
| 1→0 transition count | 4 | 3 | 1.000000 | 1.000000 |
| ≥2 positive inspections per evolved population | 4 | 0 | 0.076923 | 0.120280 |

The max-|T| sensitivity standardizes each of the eight between-arm mean-score differences by its finite-population permutation SD and uses the maximum absolute standardized difference over the same eight outcomes in each whole-population relabeling. Its numerator counts (table order) are **786, 264, 3,100, 180, 858, 12,870, 12,870, 1,548** of 12,870.

**Consequential correction:** Parent PR #377's four-view adjusted p for *all positive inspections* was 0.027972. Widening to these **eight displayed, post-source-selected views** yields **0.061072**. The new 0→1 effect likewise has unadjusted p 0.039161 but eight-view adjusted p 0.066667. Neither result is promoted as a confirmatory positive. The late-inspection and final-generation differences stay below 0.05 within the eight-view sensitivity, but this is **still exploratory, not a prospective familywise analysis over all possible endpoints**. The eight-view family was itself selected after source inspection; maxT cannot remove that selection bias or create independent replication.

## Why the transitions cannot identify mutation or persistence mechanisms

1. **0→1 means first detectable among the sampled colony set**, not a new mutation. If an auxotroph existed below detection at the previous inspection, its subsequent detection could be an increase in frequency.
2. **1→0 does not mean extinction**, for the same reason.
3. **1→1 does not establish continuity of the same evolved genotype.** The sampled population may include multiple genotypes and strains; no complete genotype-to-population longitudinal tracking was available from the original Figure 2.
4. Sampled generation intervals are **250, 250, 500, 500, 500**. Thus observed transition counts are not a common-rate hazard per generation, and transition opportunity is conditioned on the prior observed state.
5. Parent Dryad raw workbook was not retrieved (official anonymous download previously returned HTTP 401); no exact within-population auxotroph frequency, origin time, mutation supply, competition coefficient, or clone extinction was estimated here.
6. The original article assigns the non-AA generation-500 positive to **R3** in Results prose but to **R2** in Figure 2. Reassigning just that positive cell between R2 and R3 leaves all arm-level transition counts and eight-view max-|T| extreme counts unchanged. This remains an unresolved source identity conflict, **not a repaired original**.

## Connection to architecture-evolution theory

The strongest warranted cross-scale interpretation is **environment-dependent detectability of function-loss phenotypes**, a constraint on *ecological availability versus metabolic independence*. This experiment does **not** identify the historical origin of a complementary two-function split, reciprocal division of labour, independently measured functional trade-off, source-specific startup cost `K(u)`, or ecological mechanism allocation in the active BITA paper.

The contrast is thus useful as an **environment-contingent dependency** vignette within the historical Chapter 2 / SLK provenance. **Stop additional exploratory slicing of this same Figure 2** here: another independent experimental programme with full lineage denominators, parent genotype and functional controls would be needed to strengthen generality. Do not fold these rows into a meta-analysis as independent effects.

## Reproduction and repository boundaries

```bash
python -m scripts.analyze_bita_ecoli_detection_transitions \
  --output /tmp/dsouza2016_aa_auxotrophy_transition_audit.json
python -m pytest -q tests/test_bita_ecoli_detection_transitions.py
```

The source code recomputes PR #377's parent frozen result, checks it matches the original-source frozen 96-cell readout, audits complete 8×(8+8) whole-population permutations and validates all new rows against the frozen `empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_transition_audit.json`. The original publisher's image was externally source-verified in PR #376; this continuation *reuses* its checksum-locked derived source and does not claim to redownload it.

**Scope:** Additive Draft PR only; no edits to `main`, manuscript, SLK, theory, parent figures, existing estimates, or submission materials. No merge and no publication action.
