# Source-corrected trajectory sensitivity: evolved metabolic dependency (2026-11-16)

**Status:** Draft, post-source exploratory sensitivity. Parent [PR #376](https://github.com/zuizui0223/bita/pull/376) remains the **one-experiment** source of truth for the original Figure 2. This analysis adds **no independent research programme** and does **not** change the canonical BITA mechanism-identification paper, the Ecology Letters Letter, or SLK.

## Question

Is the environment-associated contrast in **detectably auxotrophic evolved E. coli populations** restricted to the 2,000-generation endpoint, or also visible when repeated source timepoints are summarized with the *evolved population* (not the assay cell or colony) as the independent unit?

Source: D'Souza & Kost (2016), [doi:10.1371/journal.pgen.1006364](https://doi.org/10.1371/journal.pgen.1006364), original Figure 2 [publisher](https://journals.plos.org/plosgenetics/article/figure/image?size=large&id=10.1371/journal.pgen.1006364.g002). Parent source identity SHA-256: `71da8f3c1707d1ade887d4030446d1869f9fd33b05fa8cfed6fb3cd49823bd8b`.

## Denominator, estimand, and exact method

- Eight independently evolving populations in amino-acid-supplemented conditions and eight independently evolving populations without supplementary amino acids.
- Six observations per population at generations **0, 250, 500, 1,000, 1,500, 2,000**. Thus **96 categorical figure cells**, but **only 16 independently evolved lineages**.
- Binary heatmap encoding: **detected** versus **not detected among ~1,000 assayed colonies per population per sampled generation**. The published colour categories cannot be converted into precise per-population CFU frequencies from the image.
- Each statistic is first reduced to *one score per evolved population*. We enumerate all **C(16,8) = 12,870** whole-population arm-label reallocations, recording the two-sided tail of the absolute between-arm difference of mean population scores. No individual colonies or repeated-time cells are permuted.
- Exact label permutation is a finite-sample *exchangeability-based* sensitivity calculation, not proof that experimental arm allocation was randomized, not a longitudinal model, and not an independent new experiment.

## Four exploratory views of the same 16 populations

| Unit-level score | AA supplied | AA absent | Mean population-score difference | Exact two-sided p | Four-view maxT p |
|---|---:|---:|---:|---:|---:|
| Positive sampled generations per population (6 inspections) | 12 detections over 8 population histories | 3 over 8 | **+1.125 inspections/population** | **0.023776** | **0.027972** |
| Positive inspections at generations 1,000/1,500/2,000 | 12 over 8 | 2 over 8 | **+1.250 inspections/population** | **0.012121** | **0.019580** |
| Population ever detected positive (one score per population) | 7/8 | 3/8 | **+0.500** | **0.118881** | **0.202797** |
| Population positive at 2,000 generations (original endpoint) | 6/8 | 0/8 | **+0.750** | **0.006993** | **0.013054** |

Source-by-generation positive-population counts are **AA supplied versus absent**: 0/0 (generation 0), 0/0 (250), 0/1 (500), 4/0 (1,000), **2/2 (1,500)**, 6/0 (2,000). The pattern is **not monotonically separated at every sampling time**; the 1,500-generation treatment contrast is zero.

**Multiplicity check for the four displayed outcomes.** We additionally enumerated the very same 12,870 whole-population allocations, standardized each between-arm contrast by its exact finite-population permutation SD, and compared each observed absolute standardized contrast against the **maximum** over all four contrasts in each allocation (max-|T|). The adjusted exact extreme-allocation numerators are **360, 252, 2,610, 168**, respectively. The adjusted p values are valid as a *within-these-four-views* permutation sensitivity under exchangeability; these four estimands were chosen after inspecting the source, so the analysis does **not** provide prospective familywise error control over all conceivable outcomes or reframe an exploratory test as confirmatory. No assumption of independent longitudinal samples is made.

The six-inspection count includes two inspection times (0 and 250) where both groups are zero. Those zeros do not change the count-difference permutation p. Among just the four post-250 sampled opportunities, positive inspection fractions are **12/32 = 37.50%** versus **3/32 = 9.375%**; these fractions summarize repeated observed opportunities, **not 32 independent populations**, and their difference does not estimate an evolving population's continuous-time residence time. The 500–1,000-generation interval is longer than the early 250-generation intervals, so equal-inspection counts are **not** a time-integrated area-under-curve.

## Dependence and provenance sensitivity

1. Leave out each of the 16 *entire independent populations* in turn, recomputing the all-inspection exact label permutation with 7-versus-8 (or 8-versus-7) populations. All 16 mean-score differences remain positive, ranging **+0.9107 to +1.3393**, with two-sided p values ranging **0.00544 to 0.04242**. These correlated sensitivity results are **not 16 additional hypothesis tests**.
2. The source results prose identifies the non-AA positive 500-generation isolate as **R3**, whereas the original figure places it in **R2**. Relabeling only that cell from R2 to R3 leaves the four exact permutation results unchanged, because the arm-level distribution of population detection scores is unchanged. The primary source discrepancy remains unresolved; this is **not** an arbitrary correction to the data.
3. The original report's independently documented **473-versus-483** selected-AA-isolate discrepancy also remains unresolved. No raw colony counts or raw Dryad workbook were invented or inferred.

## Scientific interpretation and promotion boundary

**Supported by this one source:** In the available Figure 2 binary detection readout, an amino-acid-rich growth environment is associated with more repeated sampling occasions on which evolved populations contain detectable auxotrophic cells. This source-level tendency is **not solely a consequence of choosing the final observation**. The endpoint contrast is stronger than the less selective 'ever detected' contrast, emphasizing the difference between *a genotype being observed at least once* and *being detectable at a given later time*.

**Not supported:** An evolved population with a zero cell is not proven to lack auxotrophy mutations, and a positive cell is not proof of fixation. The analysis cannot estimate time of origin, disappearance/extinction, continuous-time persistence, mutation rate, distinct genetic histories, isolated selection coefficients, reciprocal division of labour, a two-functional-coordinate ancestral split, startup cost `K(u)`, or between-species/meta-analytic generality. Availability of amino acids also changes density and mutation supply. All four outcomes were inspected after viewing the original source; the displayed **four-view maxT permutation adjustment** does not correct for unreported alternative choices, and no prospective confirmatory claim is made. With only **one source research programme**, this is an exploratory single-study *sensitivity*, not meta-analysis.

## Reproduce

```bash
python -m scripts.analyze_bita_ecoli_trajectory_sensitivity \
  --input empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_fig2_readout.json \
  --output /tmp/dsouza2016_aa_auxotrophy_trajectory_sensitivity.json
python -m pytest -q tests/test_bita_ecoli_trajectory_sensitivity.py
```

Script and tests use Python standard library (and pytest for tests). Output is checked against frozen `empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_trajectory_sensitivity.json`. The source-colour and original-PLOS binary fingerprint are already verified by parent PR #376's source-locked independent workflow.

**Manuscript ownership remains frozen:** The active BITA mechanism-identification source `manuscript/CLAIM_FREEZE.md` does not receive evolved trait-architecture claims. These evolutionary observations are a segregated technical provenance route for the historical Chapter 2 / SLK evolutionary-accessibility programme. No publication or merge action follows automatically.
