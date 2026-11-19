# Pineau 2024: Figure 5 competition-removal evolutionary replay — source-denominator audit

**2026-11-19.** This is a stacked, additive follow-up to [PR #381](https://github.com/zuizui0223/bita/pull/381). Active BITA mechanism-identification and SLK architecture theory remain frozen and untouched.


## Source-data identity correction and conservative primary result

**A critical original-data duplicate was verified.** In the unchanged, hash-verified author workbook Fig5A, Excel column 6 (large l1, Day40) and column 24 (small s1, Day40) contain exactly the same 164 (Excel row, numerical cluster area) pairs. This is an exact repeated measurement vector under two different putatively independent population labels, not an accidental match in derived means. The authors' R source loader names different raw microscopy image files for the two populations, but those original separate image files are not available in the connected GitHub source. There is no source-backed way to decide which Day40 column is correct. **Both are quarantined**, rather than arbitrarily accepting one.

| Original independent replay | Founding type | Direct Day40 minus initial mean radius (μm) | Source QA |
|---|---|---:|---|
| l1 | Large | −12.0681 | Quarantined: Day40 source duplicate |
| l3 | Large | −5.4960 | Pass |
| l4 | Large | −6.4551 | Pass |
| s1 | Small | +32.2666 | Quarantined: Day40 source duplicate |
| s2 | Small | +12.5977 | Pass |
| s3 | Small | +7.9403 | Pass |
| s4 | Small | +6.4985 | Pass |

**Primary source-validated endpoint after quarantine:** among three independently verified Small replays, mean Day40 minus initial radius **+9.0122 μm** (range +6.4985 to +12.5977 μm); among two verified Large replays, **−5.9756 μm** (range −6.4551 to −5.4960 μm). These **five** available independent population endpoints all move toward intermediate size under competitor removal. The raw unfiltered Small +14.8258 μm and Large −8.0064 μm means are demoted to *source-QA diagnostics*, not the main scientific result.

**No inference about the two excluded Day40 endpoints:** l1 had a Day20 minus initial decrease of −18.6142 μm, while s1 had a Day20 minus initial change of −0.4227 μm, approximately unchanged. Therefore one may not rescue the claim that all seven lines moved toward the middle at Day40 by substituting observations from Day20.

**No overconfident p value:** the seven-line exploratory 1/35 absolute label permutation reference includes the two duplicated Day40 source values; Small versus Large founding genotypes also were not randomized. It is an invalid confirmatory test of the current post-QA claim. The article's F(1,38) ANCOVA interaction similarly uses repeated time points and cannot be interpreted as 40 independent replay evolutions.

**Source figure and preprocessing boundary:** Fig5A is 42 population-time columns containing 44,910 original cluster-area numeric cells. The science code converts each positive area to radius and volume and computes a direct biomass-weighted mean radius. It is not exactly the same as the original R code's 1,500-bin midpoint approximation; the known s2 Day10 >100-μm trimming is recorded as a sensitivity only, not silently applied to the Day40 primary endpoint. Original Figure 5 caption 5/5 versus Methods 4/4 versus R plotted 3 Large+4 Small remains unresolved.

Reproduction: scripts/analyze_bita_pineau2024_f5_replay.py and the SHA-verified GitHub Actions workflow regenerate empirical/trait_architecture_history/pineau2024_f5_original_replay_readout.json. The tests assert the exact 164-row duplicate and the n=3 Small/n=2 Large conservative evidence gate. This remains a Draft branch and one research programme, with no merge or changes to the active BITA manuscript and SLK theory.

## Biological question

Does removing the ecological competitor from the already-diverged PO-4 Small and Large snowflake yeast isolate pair produce directional evolution back toward intermediate group sizes? This is a **direct evolutionary replay under competitor removal** within the Pineau et al. (2024) programme, DOI [10.1038/s41559-024-02367-y](https://doi.org/10.1038/s41559-024-02367-y). It is stronger mechanistic evidence for competition-mediated character displacement than an equilibrium frequency alone, but no more than *one source programme with a few independent replay cultures*. It does not prove the historical genomic origin of an individual-level architecture or an independently measured trade-off between two within-organism functional modules.

## Original publisher / author-source denominator audit

The published [PMC manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC11090753/) and author workbook/code disagree over the number of monoculture replay lines:

| Source | Small founder replays | Large founder replays | Interpretation |
|---|---:|---:|---|
| Article Methods, “Testing for character displacement” | 4 | 4 | Published experimental description |
| Article Figure 5 caption | 5 | 5 | Caption description, **not supported by author code** |
| Original author's F5 R code | **4** | **3** | Actually named independent replay population trajectories in the plotted analysis |
| Original XLSX sheet `Fig5A` | **4** | **3** | Exactly seven distinct population blocks, six sampled times each |

The pinned author Git repository is [Ratcliff-Lab/coexistence-paper](https://github.com/Ratcliff-Lab/coexistence-paper), immutable commit `071affa79f16f0a469f099058372a7488c35c0c2`. Original source Git blob SHA-1 values:

- Raw author workbook `data_used_to_generate_figs_in_coexistence_paper.xlsx`: `8f7d01b388489374aba210db96495f387d4338e2` (SHA-256 `b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f`, 1,535,384 bytes).
- Source data loader `F5_load-data.R`: `77844c9c336d01ea264a0b2b30229f61191a7ff7`.
- Source plot and analysis `F5_plot_mean_versus_time_biomass_transformed.R`: `9ec49af81ba1805277223149644c9fe35ab47f0f`.

The original R scripts list Small population IDs `s1,s2,s3,s4` and Large `l1,l3,l4`. Their Figure 5 plot matrix is **7 lineage rows × 6 repeated times**, not 42 independent evolution events. The R code's ordinary ANCOVA uses repeated population-time means and reports interaction *F*₁,₃₈ ≈ 14.95, *p* ≈ 0.000418. That is a published source-model result, **not** a population-clustered replicate-level inferential test for 7 independently evolved cultures. Do not treat 38 residual degrees of freedom as evidence from 38 independent evolutionary origins.

### Direct source workbook verification

The immutable `Fig5A` worksheet contains **42 measurement columns and 44,910 numeric original cluster-area cells**; the seven population-specific six-day blocks agree with the R code. Excel labels are `Day1, Day5, Day10, Day15, Day20, Day40`, while the author R analysis treats those six observations as days `0,5,10,15,20,40`. We preserve this time-origin discrepancy explicitly. The author R code references further local microscopy data directories not all available as separate files in the author repository; the `Fig5A` deposited source instead makes it possible to reconstruct the cluster-size distribution from original numeric area measurements without claiming access to the nondeposited local image files.

### Direct reconstruction to source-reported phenotype scales

Code `scripts/analyze_bita_pineau2024_f5_replay.py` uses original measured cluster areas and the R source's geometrical transforms:

- radius = square root(area / π)
- cluster-volume weight = 4π radius³ / 3
- one **direct volume-weighted mean radius per independently evolved population per sampled time**

Our direct continuous-volume estimator is not exactly equal to the author's 1,500-bin midpoint-based biomass-weighted approximation, which should be recorded as a numerical sensitivity rather than concealed. Source code specifically removes radius bins above 100 μm for Small replicate s2 Day10; we calculate a named parallel QC sensitivity while keeping the *untrimmed original area-based* readout intact.

For each replay line, summarize Day40 minus initial mean radius and a population-specific six-point linear slope. The inference unit is the **evolved replay culture** (4 Small, 3 Large); all 42 timepoints, thousands of area measurements, and image tiles are nested observations. Enumerate exactly C(7,3)=35 reassigned population-origin labels for a **descriptive** contrast only: the founder phenotypes were **not randomized to Small versus Large**, so this is not a randomized-treatment test or a general probability of specialization.

## Research claim scope

An independently supported directional shift in both line types under competitor removal would be consistent with **competition-mediated ecological character displacement** and evolutionary reversion towards intermediate phenotype size. It would not identify:
- a two-trait within-organism cross-fitness interaction or BITA antagonist/pollinator mechanism allocations;
- de novo gene duplication, simultaneous independent module formation, genetic fixation of complementary social roles or BITA/SLK K(u);
- generalized repeated independent publication-level support (still only one Pineau 2024 programme);
- convergence under other environmental treatments that were never replay-evolved.

The author Figure 5 Methods versus caption versus code/workbook replicate-number conflict must remain visible after any scientific result.

## Reproduction and status

- `scripts/audit_bita_pineau2024_f5_source.py`: author code and original Fig5A source provenance inventory.
- `scripts/analyze_bita_pineau2024_f5_replay.py`: original source cluster-to-radius weighting and seven-line directional replay calculation.
- `tests/test_bita_pineau2024_f5_source.py` and `tests/test_bita_pineau2024_f5_replay.py`: source-unit and source-transform integrity.
- `.github/workflows/bita-pineau2024-f5-original-source-lineage-audit.yml`: read-only exact source fetch and reproducibility.

The branch is Draft only. No change to `main`, parent source studies, the active BITA manuscript, SLK, or journal submission.
