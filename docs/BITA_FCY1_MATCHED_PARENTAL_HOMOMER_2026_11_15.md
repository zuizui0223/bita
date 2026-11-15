# BITA Fcy1 matched parental-homomer comparisons (2026-11-15)

Status: exploratory original-data reanalysis from one engineered yeast programme. The 2024 Science paper DOI 10.1126/science.ado5719 already demonstrated constructive-neutral-compatible compensation and evaluated best-parental-homomer models. This is a new, source-audited denominator/readout for BITA, not discovery of new molecular compensation, historical evolution, independent replication or cross-study meta-analysis.

## Prespecified comparator and corrected source exclusion

For different Fcy1 alleles A and B in the same cytosine growth assay, define

    delta_g(A,B) = g(A/B) - max[g(A/A), g(B/B)]   (OD/hour).

Strict eligible cases require g(A/B), g(A/A), g(B/B) to be **measured**, and each parental same-allele construct to fall below the original authors' 0.02 OD/hour functional threshold. A rescue requires g(A/B) >= 0.02. This is a near-term growth phenotype contrast relative to damaged components, **not** the whole-organism fitness advantage of a new architecture relative to an ancestral wild-type complex.

Original peer-reviewed Methods explicitly exclude M93G/M93G due to diploid-stock **cross-contamination**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10888846/ . The raw measurement, apparent 0.13188 OD/hour, is an excluded QC datum, never an eligible parental-homomer value. That resolves the former notebook/source discrepancy; the all-171 subset agrees with author's saved classification (167 measured, 4 unavailable; 24 TP, 3 FP, 3 FN, 137 TN).

Pinned source: author repository https://github.com/Landrylab/Despres_et_al_2024 , exact author commit f124cef96a3b5806a096b679b2bd57b68aec6514; screen-positive data blob 36839a3fd2eb05a521a070d11e60cde1748a682e. The earlier draft PR #367 recomputes 22 original growth XLSX quadrants, preserving missing plate_6_C.xlsx and plate_6_D.xlsx rather than synthesizing their results. The original methods explicitly use the median of five maximal 15-minute optical density differences and exclude anomalous data.

## Measured positive and negative outcomes

- Eighteen preselected validation alleles: 171 unordered combinations (18 identical-allele controls and 153 different-allele pairs).
- 152/153 different-allele pairs measured growth; 27 different-allele pairs cross 0.02 OD/hour.
- Three same-allele controls unavailable (H62C/H62C, L74P/L74P, and source-excluded contaminated M93G/M93G). Thus 15 observed below-threshold parental homomers yield **105 fully matched different-allele comparisons**.
- Among the 105 strict eligible pairs, **22 rescued** despite both same-allele parental constructs being functionally below threshold, and **83 did not**. All 22 rescued pairs had both reciprocal A/B assay orientations.
- Another 5 growth-positive distinct-allele pairs cannot be classified as strictly parental-homomer matched because at least one parental-homomer measurement is unavailable: A97F/M93G, E64C/L74P, E64S/L74P, E64V/L74P, H62C/M100W. They remain UNKNOWN, not negative or proven false-positive.
- Descriptive median gain relative to the stronger parental same-allele control among all 105: **+0.00144 OD/hour**; mean **+0.02033 OD/hour**. 70 pairs exceed the stronger parent by some positive amount, and 20 pairs exceed it by at least 0.02 OD/hour. No p value is calculated from pair-as-independent sampling.
- Illustrative strong positive example E64C + M100W: heteromer g=0.13196 vs each self-control g≈0.00380, observed increment **+0.12816 OD/hour**.

### Threshold robustness, same preselected panel

| OD/hour threshold | Matched eligible | Matched rescues | Other positives lacking at least one self-control |
|---|---:|---:|---:|
| 0.010 | 105 | 28 | 6 |
| 0.015 | 105 | 22 | 5 |
| **0.020** (author) | **105** | **22** | **5** |
| 0.030 | 105 | 19 | 5 |
| 0.050 | 105 | 18 | 4 |

These five thresholds are re-readouts of the SAME data, not five replications. At the primary threshold, the 22 confirmed compatible pair types form one connected positive network of **13 alleles and 22 edges**. M100W has 9 confirmed partners; R73G has 6; Y79S has 5. Thirteen strict rescued edges remain after removal of the largest hub M100W. Edge connectivity is molecular cofunctionality, **not** an accessible one-mutant adaptive walk through genotype space.

## What this supports and does not support

Direct growth comparison demonstrates a functional **complementarity between impaired component alleles**, including genuine matched negative cases. It does not establish adaptation-driven selection for duplication, new trait splitting, greater organismal fitness than the ancestral one-gene homodimer, or the theoretical BITA startup curve K(u). It is compatible with published constructive-neutral evolution: an obligate multisubunit architecture may maintain a prior function without improving it.

The 105 pairs share alleles; their apparent rescue frequency is not an unbiased natural frequency nor a binomial k=105 evolutionary study. Original positive screening filters and later validation-panel choices further constrain inference. The Fcy1 experiment still represents **one** programme in the 5-family heterogeneous evidence map. Do not pool this growth phenotype with Salmonella physiological rescue, E. coli coGFP fluorescence, Peucedanum allocation, or cichlid morphology covariance.

## Repeatability and release

The new source-pinned Github Actions audit reruns the author's 22 original XLSX growth sheets and applies the peer-reviewed contamination exclusion, then executes scripts/analyze_bita_fcy1_matched.py and tests/test_bita_fcy1_matched.py. Machine-readable per-pair values and the full matched readout are archived as Actions artifacts with the source commit and 22 original input checksums.

This continuation stays Draft. No main merge, journal submission, data deposit or modifications to the active nectar-robbery Letter.
