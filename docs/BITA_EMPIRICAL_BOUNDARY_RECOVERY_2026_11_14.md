# Real empirical recovery after the BITA threshold model

Date: 2026-11-14. Status: exploratory source re-extraction, not a new biological experiment, systematic review, completed meta-analysis or test of hysteresis. Theory PR #363 is unchanged.

## Finding

Theoretical differentiation is not the only way to satisfy competing functional demands. A newly retrieved published experiment supplies a **genetic-background/accessibility contrast**, not a history-matched contrast. The numerical outcome below is physiological growth rescue, not the frequency of trait differentiation or measured biochemical equivalence.

In Nasvall & Abdalaal (2026), experiment 2 started 24 populations in each genetic background under a common selection regime. The published endpoint reported 21 versus 10 rescued populations. Table 1 lists those 31 positive outcomes; this extraction keeps **all 48 started populations** in denominators and retains the unresolved rescued case. No individual growth curves or supplementary ZIP were downloaded.

## Recomputed results

| Published endpoint | Mutator background | Nonmutator background | Difference in proportion (95% Newcombe interval) | Two-sided Fisher p | Holm p, three outcomes |
|---|---:|---:|---:|---:|---:|
| Any physiological rescue | 21/24 | 10/24 | +0.4583 [0.1895, 0.6487] | 0.002049 | 0.004678 |
| hisA-associated route | 9/24 | 0/24 | +0.3750 [0.1611, 0.5729] | 0.001559 | 0.004678 |
| trpA-associated route | 11/24 | 10/24 | +0.0417 [-0.2233, 0.2986] | 1.000000 | 1.000000 |

Rescue risk ratio: **2.1000**, approximate log-Wald 95% interval **[1.2776, 3.4517]**. A zero-reference hisA probability is not repaired with a pseudocount: its RR and log interval are left undefined in the JSON. Lack of a detected trpA difference is not equivalence.

The 11-population difference partitions arithmetically into nine hisA, one trpA and one unresolved rescued population. This is a count decomposition, **not an estimate of a mediated fraction**. All three contrasts reuse the same populations and are not independent effects for a meta-analysis. These tests were selected after the paper was available and are exploratory, not preregistered confirmation.

## What this adds to BITA

Recovered: a source-backed association between genetic background and which functional routes become available under the same declared selection conditions. It is partial evidence relevant to **accessibility**, alongside the theory of architectural benefit. Multiple-function retention and structural specialization must remain separate possible outcomes.

Not recovered: the three BITA thresholds, K(u), a matched historical contrast, genotype-to-phenotype step sizes, a shared-versus-divided absolute fitness comparison, or a bidirectional hysteresis loop. Mutator background is not a proxy for independently documented adaptation history or a scalar change in mutation rate alone. This result neither confirms nor falsifies the specific exponential-cost hysteresis mechanism.

Amplification: the source identifies one amplified population with no detected divergence among copies. Whole-genome sequencing and targeted sequencing have different ascertainment. We therefore **do not calculate a duplication/divergence prevalence over all 48 populations** or turn absence of a report into verified absence.

## Boundary sources and dependence

The companion publication ledger records four papers, **not four independent biological replications**. Nasvall et al. (2012) documents both specialized copies and improved generalists. Newton et al. (2017) follows the same evolved material and is linked to that programme rather than counted as another evolutionary experiment. Lundin et al. (2020) describes a selected mutational panel with 3/16 variants retaining the ancestral function; its 16 variants include a previously reported reconstructed variant. Its variant counts are not population frequencies. The 2026 endpoint contrast is the only newly quantified experiment in this package.

All records belong to a related Salmonella gene-function research family. The 2012 and 2026 designs differ in starting genotype/construct, selection regime and duration. Their different outcomes cannot identify a causal effect of intermittent versus continuous selection. No cross-study pooled estimate or taxonomic generality is claimed.

## Source and audit trail

- Nasvall & Abdalaal 2026, G3, DOI **10.1093/g3journal/jkag167**, first online 6 July 2026, October 2026 issue. Extraction: Results, experiment 2; **Table 1 and footnotes a-f**. Publisher: https://academic.oup.com/g3journal/advance-article/doi/10.1093/g3journal/jkag167/8725334?searchresult=1 ; full-text mirror: https://pmc.ncbi.nlm.nih.gov/articles/PMC13643763/ . Publisher-indexed table rows and PMC-indexed text were cross-checked. They are mirrors of one source, not independent verification studies.
- Nasvall et al. 2012, Science, DOI **10.1126/science.1226521**, Results and Figure 4 caption: https://pmc.ncbi.nlm.nih.gov/articles/PMC4392837/ . Only textual findings were admitted; no quantitative figure digitization.
- Newton et al. 2017, PNAS, DOI **10.1073/pnas.1618552114**, abstract/provenance: https://pubmed.ncbi.nlm.nih.gov/28416687/ . Dependence flag only.
- Lundin et al. 2020, Frontiers in Microbiology, DOI **10.3389/fmicb.2020.588235**, Results and Table 1: https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2020.588235/full . Context only, not a poolable effect here.

Runtime DNS prevented direct source downloads; the publisher supplementary link also failed to fetch. The available primary indexed text supports endpoint extraction, but **raw-source-byte verification and assay-level reanalysis remain incomplete**. This limitation does not erase the distinction between the published table and invented raw observations.

## Reproduction and uncertainty

Run `python -m scripts.analyze_bita_history_empirical_recovery`, then `pytest -q tests/test_bita_history_empirical_recovery.py`.

Production is standard-library-only. Fisher probabilities use integer hypergeometric weights; difference intervals use Wilson-Newcombe; RR intervals use an approximate log method. Local independent scipy/statsmodels checks agree to <3e-16 across 625 Fisher tables and seven interval cases. This verifies numerical calculation, not scientific source coding by an independent reviewer.

Intervals assume independently founded populations remain independent; the authors note possible cross-contamination cannot be entirely excluded. The endpoint is assay- and duration-specific. Unrescued populations are not evidence of absolute evolutionary impossibility. Supplementary continuous phenotypes and an independently coded broader corpus remain unexamined here.

Retain the empirical PR in Draft. No main merge, manuscript edit, publication, or deposition.
