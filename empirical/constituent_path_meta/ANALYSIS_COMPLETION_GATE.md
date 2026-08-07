# Analysis completion gate before manuscript work resumes

## Status

Manuscript work is intentionally frozen while the empirical constituent-path analysis is incomplete.

This file is an analysis workflow gate. It does not modify the fixed theory, introduce a new biological mechanism, or add a manuscript claim.

## Fixed theory being tested only at the pathway level

The current theory remains unchanged. The empirical program does **not** attempt to estimate the full local mixed partial from heterogeneous literature studies. Instead, it asks whether one or more biological pathways required by the existing conditional interpretation can be supported quantitatively.

The first target is the existing `B_to_pollination` pathway: a flower-specific defensive/access-restriction trait can reduce legitimate pollinator use. A main-effect meta-analysis of this pathway can support the biological plausibility and direction of pollinator interference, but it does not estimate the cross-partial magnitude `iota` and does not validate the complete attraction-defence sign criterion.

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

## Current state at branch creation

On `main`, `empirical/broad_reality_evidence/broad_effect_extractions.csv` contains no quantitative effect rows. Directional evidence exists for `B_to_pollination`, and historical analysis branches contain candidate full-text targets and one verified observational `Impatiens capensis` B-to-pollination coefficient. These materials are inputs for source re-audit, not completed synthesis.

The first completion target is therefore a source-audited quantitative `B_to_pollination` synthesis, with a preference/choice lane analyzed separately from visitation-rate and consumption/residence-time lanes.
