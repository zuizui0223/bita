# BITA: Genetic background, partner history, and architecture-dependent fitness signs

Date: 2026-11-15. One primary Bacillus subtilis EPS/TasA programme. **One research programme, not an independent meta-analysis or experimentally observed origin of a new trait architecture.** This note records previously published experiments and newly audited source provenance, without claiming discovery of the experiment.

## Primary original-source custody

1. Dragoš et al. 2018, *Nature Microbiology*, DOI **10.1038/s41564-018-0263-y**, [institutional accepted manuscript](https://backend.orbit.dtu.dk/ws/portalfiles/portal/176479224/Dragos_et_al_NatMicrobiol_Accepted_version_with_Figures.pdf). Original PDF: **30 pages, 2,401,378 bytes**, SHA-256 `5cf82d20baf805432c7a0afda748f67689d71c5614bb0a90f6baf54bc040d6af`.
2. [Official Springer Supplementary Information](https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-018-0263-y/MediaObjects/41564_2018_263_MOESM1_ESM.pdf). Original PDF: **23 pages, 3,001,326 bytes**, SHA-256 `d5a62567ab0818926f51892ac5750757d9f4e83c37d015664e1cfd4a4ec7e05c`. Supplementary Figure 5 contains matched EPS-present productivities (**n=4 biological replicates per group**), surface hydrophobicity and BslA-deletion images; Supplementary Figure 11 shows **three histories × six parallel experimental populations**.
3. Related original mutation dataset was verified in parent [Draft PR #371](https://github.com/zuizui0223/bita/pull/371), at official Nature original XLSX SHA-256 `ec916667dbd7a288246737979e3b0d2e4336acfcc8dd98d641339973361d9a43`. This dataset does **not** include the longitudinal CFU measurement series.

The two PDFs were acquired and SHA verified via the [read-only source-access Actions run](https://github.com/zuizui0223/bita/actions/runs/43710047288), archived without republishing copyrighted PDF bytes in the Git repo. The new `bita-bacillus-conditional-original-pdfs.yml` workflow separately fetches and fails closed on changed source bytes, then checks exact text cues and the codebook. Source files were rendered and figure interpretations checked against the displayed original Supplementary Figures 5 and 11 and manuscript Figure 6.

## A direct contextual genetic interaction: the same TasA substitutions

The parent experiment originally evolved independent EPS-deficient populations **e4** and **e6**, each with one substitution in remaining protein TasA. e4 has **Y124C**; e6 has **G183C**. Three independently picked clones e4A/B/C from e4 and e6A/B/C from e6 are **six isolates but only two original evolved lineages**.

In a reconstructed **EPS-absent** background (double deletion ΔepsΔtasA, followed by ectopic ancestral or mutated tasA), each substitution allowed pellicle formation and raised measured productivity relative to the same construct expressing native TasA (accepted Fig. 2a–c; Fig. 2b productivity **n=3 biological replicates per construct**). Authors also compared them to the ancestral Δeps in fitness assays with **n=4** per group (Fig. 2c).

In an **EPS-present** background (ΔtasA complemented with tasA; WT also plotted), the original Nature Supplementary Fig. 5a and Results 1 report **no improvement** in productivity for the cysteine-containing proteins, and **G183C appeared to decrease productivity versus WT**; only the G183C group carries the shown significance star in the supplementary figure, for a t test against WT (*p<0.05*, two-sided). **Do not call Y124C EPS-present productivity significantly negative**: that overstates the source. Both EPS-present mutants lost surface water repellency (supplementary 5c; droplet sank instantly) and showed limited spreading on solid medium (supplementary 6).

The directional comparison is:

| TasA change | EPS absent (matched ancestral TasA construct) | EPS present (WT and native-TasA controls) |
|---|---|---|
| Y124C (e4) | Pellicle rescue and increased growth | **No demonstrated productivity benefit**; strong loss of water repellency |
| G183C (e6) | Pellicle rescue and increased growth | **Reported negative productivity versus WT**; strong loss of water repellency |

This is an **experimentally manipulated genotype-background** difference. It is compatible with a sign change in the benefit of G183C, but the positive and negative panels have **different genetic comparators** and no four-cell numeric raw fitness table was recovered. Therefore, **do not fit a formal interaction coefficient, claim direct numerical antagonistic epistasis, or equate this with BITA's K(u) and fold/entry thresholds**.

### Two independent routes have different third-component dependencies

Supplementary Fig. 5d and Supplementary Results 2 independently delete the hydrophobin gene **bslA** from evolved Δeps strains:

- **e4A, Y124C**: `bslA` deletion **abolishes pellicle formation**.
- **e6A, G183C**: `bslA` deletion **does not eliminate pellicle formation** (reported performance unaltered).

Thus **two evolved molecules that recover the same broader biofilm function show different dependence on an additional matrix component**. The authors offer possible interaction with BslA for Y124C, and self-oligomerization for G183C, but this mechanism is **not** a quantified residual genetic coupling parameter (λ); the comparison includes full e4 versus e6 evolved genetic backgrounds, not necessarily isolated variants matched on every other mutation.

## Reciprocal partner-history transplant experiment

The accepted paper Fig. 6 reconstructs four combinations at the **same pellicle productivity assay**:

| Δeps partner | ΔtasA partner | Source-supported result relative to ancestral pair |
|---|---|---|
| Ancestral | Ancestral | Reference baseline (n=22) |
| Ancestral | **Evolved** | Productivity **lower in nearly all** source combinations |
| **Evolved** | Ancestral | **Similar or higher tendency** |
| **Evolved** | **Evolved** | **Heterogeneous**, several combinations above ancestral pair |

Original Fig. 6 indicates **n=2, 3, or 6 biological replicates for particular evolved pairings**, not a common n=22 for all swaps. This is direct **partner-preadaptation asymmetry**, not the number of successful/failed independently evolved histories. Because the source provides boxplots rather than reusable per-pair CFU values, **no pair-specific mean effects, confidence intervals, regression coefficients or new p values are extracted**.

Critically, the authors tested a falsifier: engineered EPS overproduction by ΔtasA **without its other evolved mutations** improved total mixed productivity and benefited Δeps. Therefore, the harmful preadapted ΔtasA combinations cannot be ascribed to **EPS overproduction alone**. Additional genetic changes, linked physiology or partner interactions must be considered. This matters for BITA: simply assigning a more pronounced functional trait to one specialist does not determine joint fitness.

## Observed evolutionary histories (fixed cohort denominators)

The original paper includes **six independent starting mixed populations**, **six Δeps monocultures**, and **six ΔtasA monocultures**. In the six initially mixed cultures, Δeps went **extinct in four**, rate 4/6 = 66.7%; descriptive 95% Wilson interval **[0.3000, 0.9032]**, not a cross-lineage prevalence estimate. In Δeps-alone evolution, **2/6** independent populations achieved productive surface colonization; in ΔtasA-alone evolution, **6/6** improved surface colonization. These are different evolutionary treatments and different genotype starting states, not evidence that the six outcomes are a single matched multinomial experiment.

The original accepted manuscript further says ΔtasA from co-evolution reached similar final productivity but **its improvement was delayed relative to monoculture evolution**. This is an experimentally observed effect of **selection history on the timing of adaptation**, but does **not** demonstrate an alternative stable structure at identical current conditions or a loop of BITA-style hysteresis. Both partner roles and source genotypes differ across evolution regimes, and the raw timepoint-matched CFU values have not been recovered.

Supplementary Fig. 11 replants **three preadaptation regimes**, each as **six parallel cultures**: ancestor+ancestor, evolved Δeps+ancestral ΔtasA, and evolved Δeps+evolved ΔtasA. Productivities and ΔtasA fractions were observed every fifth transfer; the publicly available figure is image-based. Counting each time point or each plotted clone as a new independent evolutionary replicate is incorrect. This is a source-backed history contrast, but the released mutation spreadsheet samples only Mix1/3/4 and selected times, and **does not provide a joined per-line phenotype/genotype table**. We retain the exact observational/assay distinction.

## Biological interpretation and literature novelty ceiling

The paper itself already discovered these conditional responses; BITA's contribution is **source-audited evidence coding and explicit separation of the estimands**:
1. Current architectural/genetic background-dependent functional effects.
2. Evolved-partner compatibility asymmetry in the same assay.
3. Selection-history-dependent adaptation speed and long-term population replacement.

These are **more concrete than merely correlating natural morphology with the current environment**, but they are still only one engineered Bacillus programme. They do not identify the original historical transition from a shared two-function architecture to a heritable differentiated architecture, a globally beneficial architecture over WT in the same evolutionary experiment, or the specific exponential startup-cost function, entry/global/persistence thresholds or a general meta-analytic effect.

To estimate numeric interaction benefits or compare lineage-specific evolutionary paths, the next source requirement is the authors' original individual CFU replicate vectors for Figs. 1, 2, 5, 6 and Supplementary 11 **keyed to evolved line IDs**. Publisher sources provide figures and a separate mutation XLSX; do not invent or pixel-read observations as exact source values.

Keep this PR **Draft**. No merge, public publication, third-party source republishing, journal submission or editing the active Ecology Letters Letter.
