# BITA: Non-pollen reward and floral shape differentiation, independent ecological source (2026-11-15)

**Status:** original-source morphological/phylogeny **reanalysis**, not a new biological observation, an independently evolved lineage count, or a source-independent replicate of the Dellinger group's published findings. Draft PR #369 is independent of the active nectar-robbery Letter.

## Main question and result

The pollen dilemma says pollen must serve both as reward to consumers and male gamete transport; differential anthers may alleviate that conflict. Is **stamen shape dimorphism** restricted to pollen-rewarded species? **No** in the 2024 Dellinger Merianieae trait source reused from earlier published flower studies.

Source archive: public Zenodo DOI **10.5281/zenodo.7659158**, original **skripts.zip**, size 135,861 bytes, SHA-256 `9d4013d470d1d201ef89196442614429a4146ba2958e1367b0a197ef50b03ed8`. Its `1_morphospaces_disparity/floraltraits.csv` has **145** unique species and SHA-256 `1f4fc947db34e31ed6f7e76642f19763d473419617aa6563c0f6421dc33394ae` (in the original UTF-8 source); the same bundle provides the author phylogenetic Newick `Marcelo_Meris.tre`. Exactly **139 species** join that tree by declared `x` tip label. The six excluded name keys are saved in the JSON.

At the **source 139-species tree-matched grain**, **77 reward types are missing**. The remaining **62** are known. With source original `confirmed.reward.type` codes `0=pollen`, `1=nectar`, `2=food body` and `stamen.shape.dimorphism` codes `0` versus `1/2` (we collapse nonzero shape-difference codes only), the measured table is:

| Reward source category | Shape code 0 | Shape code 1 or 2 | Total |
|---|---:|---:|---:|
| Pollen | **27** | **10** | **37** |
| Nectar | **10** | **3** | **13** |
| Food body | **0** | **12** | **12** |
| **Total known reward** | **37** | **25** | **62** |

Descriptive, **not phylogenetically independent**: nonpollen reward combined **15/25 (60.0%)** show code 1/2 versus pollen reward **10/37 (27.03%)**, difference **+0.3297** proportion units. This is a **source-selected subset, not a causal effect or meta-analysis**. It is especially sensitive to the bird/passerine food-body clade, *Axinaea*.

### Exposing phylogenetic/taxonomic confounding rather than hiding it

Within **Meriania** in the source tree-matched and reward-observed subset:

- Pollen: shape difference **8/22 (36.36%)**.
- Nectar: **3/13 (23.08%)**.
- Food body: **3/3 (100%)**.
- All nonpollen combined: **6/16 (37.5%)**, compared with pollen **8/22 (36.36%)**; descriptive difference **+1.14 percentage points**.

Among tree-matched *Axinaea*, all **9/9** known food-body-reward species have nonzero shape differentiation. Thus the **+33 percentage point** aggregate contrast largely collapses in the one genus with both pollen and nonpollen rewards; it cannot be promoted to a reward-caused dimorphism increase.

This exactly illustrates the distinction between **an architectural phenotype**, **the current ecological context where it occurs**, and **the selective pressure that historically originated it**. Multiple functions and context-dependent phenotypes do not uniquely imply a pollen-reward division-of-labour origin.

## Original research and scientific claim ceiling

The species-level floral trait data are **not independent** of earlier Dellinger Merianieae studies. The original 2021 *Evolution* paper **Dellinger et al.**, DOI **10.1111/evo.14260**, analyzed 63 species and already reported repeat de novo heteranthery in non-pollen reward lineages; its separate original phylogenetic correlated-evolution comparison reported likelihood ratio p≈0.09. Those 63 species plus the 2024 139-tip morphology data must **never** be counted as two independent taxa-level replications or as 202 newly established evolutionary origins. The source trait `stamen.shape.dimorphism` is one shape character; it is **not identical to** the broader composite 2021 heteranthery classification based on size, structure and colour.

Independent mechanistic alternative: *Kay et al.* (2020), DOI **10.1098/rspb.2020.2593**, reported that *Clarkia* anther diversity functions by **staggered pollen presentation** rather than distinct reward/pollination jobs. It is cited as a **separate published study**, but its original Dryad raw files are not reanalysed quantitatively here.

Independent microbial negative/boundary case: *Mridha & Kümmerli* (2022), DOI **10.1111/jeb.14001**. Engineered *Pseudomonas* siderophore specialists can complement under moderate iron limitation without outproducing WT, and may undermine group productivity under severe limitation, with frequency-dependent effects. Direct source **Dryad DOI 10.5061/dryad.2bvq83bs4** registers `Mridha_Kummerli_2022_JEB_raw_data_dryad.xlsx` (328,288 bytes, original SHA-256 `b64f8febcc72f30394169d593de5a9ab7cbc3b753d5253dd865a711bc77887f9`). The private download requirement/access gate was **not circumvented**, and **no new numeric Pseudomonas effect estimate is claimed** in this commit. This is a source-indexed future comparison, not a completed original workbook reanalysis.

## Method and reproducibility

Run:
    python -m scripts.analyze_bita_merianieae_reward_shape --source-zip original_merianieae_skripts.zip --output empirical/trait_architecture_history/dellinger2024_reward_shape_readout.json
    python -m pytest -q tests/test_bita_merianieae_reward_shape.py

The [GitHub Actions source audit](https://github.com/zuizui0223/bita/actions/runs/43700631856) reobtains the source ZIP from Zenodo, verifies SHA-256, joins names to the source tree without synthetic replacements and writes the frozen machine-readable readout. Published paper and source DOI are preserved in the readout. Missing reward is never coded as pollen or no dimorphism. No phylogenetic regression, ancestral state reconstruction, independent transition count, causal origin estimate or evolutionary success fraction is claimed. The observed contrast is entirely **descriptive and genus-dependent**, and must not be pooled with Fcy1 homomer rescue, Salmonella endpoint rescue or coGFP fluorescence.

**Release decision:** retain Draft, no merge, no external deposit or modification to the Ecology Letters Letter. The main next empirical discriminator is a genuinely **replicated matched-worldline experiment of specialist community performance versus intact generalist**, with explicit fitness currency and stable experimental replicates—not another uncontrolled binary association.
