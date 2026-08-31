# Analysis completion gate before manuscript work resumes

## Status

Manuscript work is intentionally frozen while the empirical constituent-path analysis is incomplete.

This file is an analysis workflow gate. It does not modify the fixed theory, introduce a new biological mechanism, or add a manuscript claim.

## Fixed theory being tested only at the pathway level

The current theory remains unchanged. The empirical program does **not** attempt to estimate the full local mixed partial from heterogeneous literature studies. Instead, it asks whether one or more biological pathways required by the existing conditional interpretation can be supported quantitatively.

The first target remains the existing `B_to_pollination` pathway: a flower-specific defensive/access-restriction trait can reduce legitimate pollinator use. A main-effect meta-analysis of this pathway can support the biological plausibility and direction of pollinator interference, but it does not estimate the cross-partial magnitude `iota` and does not validate the complete attraction-defence sign criterion.

A second module now tests a different empirical requirement: whether broad floral-volatile receiver responses are adequately represented by one universal pollinator-versus-florivore sign, or whether sign/state heterogeneity and source dependence have to be retained. This module is not allowed to substitute for the strict B-role pathway gate.

## Existing quantitative gates retained

The repository's existing meta-analysis rules are retained:

- fewer than 3 independent study clusters in a compatible stratum: no pooled estimate;
- at least 3 independent study clusters: exploratory random-effects synthesis is allowed;
- at least 5 independent study clusters: stability analyses become eligible.

These thresholds are already used in `empirical/broad_reality_evidence/broad_meta_analysis_strata.csv`; they are not new theory parameters.

## Manuscript-resumption gate

Do not return to manuscript framing, figure polishing, or journal submission preparation until all of the following are true:

1. **Primary constituent pathway is quantitatively identified.** At least one theory-relevant pathway has a source-audited, effect-size-compatible synthesis with at least five independent study clusters, or an equivalently defensible update/reanalysis of a published meta-analysis with study-level effects and dependence handled explicitly.
2. **Outcome mixing is controlled.** Preference/choice, visitation rate, residence time/consumption, pollen transfer, and reproduction are not silently pooled as if they measured the same outcome.
3. **Trait-role gate is enforced.** A floral chemical or physical trait enters `B` only when the source independently establishes a flower-specific antagonist-reduction, deterrence, resistance, or access-restriction role. A secondary-metabolite label alone is insufficient.
4. **Dose/context dependence is preserved.** Natural/field-relevant and supra-natural treatments are distinguished when the source provides that information; opposite effects at different doses are retained rather than averaged away.
5. **Study independence is audited.** Multiple effects, doses, taxa, years, or papers from the same biological panel are not counted as independent replication.
6. **Remaining pathways have an explicit evidence state.** They are either quantitatively synthesized, directionally supported but quantitatively sparse, or identified as unresolved evidence gaps. Sparse pathways are not promoted to quantitative validation.
7. **Theory/empiricism boundary is explicit.** Empirical main effects are described as evidence for constituent routes only. They are not presented as direct estimates of `rho`, `iota`, `kappa`, or `W_AD` unless a study design actually identifies the relevant cross-trait curvature.

## Gate C — Sasidharan et al. 2023 FVOC module

The Sasidharan et al. 2023 source workbook (DOI `10.1093/aob/mcad064`) has now been recovered and its five worksheets exported without interpretation. Table S1 contains 517 populated FVOC/insect rows, with repeated compound/insect tests within publication sources.

A publication-reference-cluster bootstrap therefore replaces row-level independence for the broad florivore-versus-pollinator comparison. The source-row contrasts are:

```text
detection:  florivore 0.819, pollinator 0.706, F-P +0.113,
            publication-cluster 95% interval [-0.082, +0.311]
attraction: florivore 0.233, pollinator 0.356, F-P -0.123,
            publication-cluster 95% interval [-0.397, +0.078]
repulsion:  florivore 0.055, pollinator 0.059, F-P -0.004,
            publication-cluster 95% interval [-0.106, +0.079]
```

All three dependence-preserving intervals cross zero. The published row-level guild contrast is therefore not promoted to a publication-level universal-effect claim. Conversely, the workbook provides source-linked evidence that response states vary across compounds, receivers, plant systems and publications.

Gate C is fixed as:

```text
source workbook recovered: YES
publication dependence reconstructed: YES
universal guild-effect module: FAIL_CLOSED
context/sign heterogeneity module: PASS
GATE_C = PASS_AS_HETEROGENEITY_MODULE_NOT_AS_UNIVERSAL_GUILD_EFFECT
```

This is a positive completion of the heterogeneity module, not completion of the primary `B_to_pollination` meta-analysis. It therefore does **not** reopen manuscript work by itself.

Canonical Gate-C files:

- `SASIDHARAN2023_SOURCE_RECEIPT_V1.json`
- `SASIDHARAN2023_PUBLICATION_CLUSTER_SUMMARY_V1.csv`
- `SASIDHARAN2023_PUBLICATION_CLUSTER_READOUT_V1.md`
- `scripts/analyze_sasidharan2023_publication_clusters.py`

## Current state

The empirical layer now contains source-complete quantitative work showing that constituent pollinator responses can be dose-, species-, outcome- and source-dependent, plus the Sasidharan publication-cluster heterogeneity module above. However, the manuscript-resumption condition in item 1 remains open: a strict theory-relevant constituent pathway still needs an effect-size-compatible synthesis with adequate independent-study support, or an equivalently defensible reanalysis of a published study-level meta-analysis after the B-role and outcome-lane gates are enforced.

The next analysis target is therefore **not** further mining of Sasidharan rows. It is closure of the strict constituent-path quantitative gate using independent source-audited studies in a compatible outcome lane.
