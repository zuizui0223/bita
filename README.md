# Biotic Interaction Trait Architecture (BITA)

BITA's **primary submission paper** is now the Ecology Letters Letter:

> **Higher nectar robbery prevalence under access mismatch need not reflect higher robbery rates**

The broader floral-defence selectivity Synthesis remains preserved as the extended BITA evidence package and fallback manuscript architecture.

The mechanism-identification result `trait interaction != ecological mechanism` remains a BITA support principle: observational routing patterns are not promoted beyond the mechanisms and causal contrasts the data actually identify.

## Current submission thesis

> **Higher nectar-robbery prevalence under access mismatch can arise through selective loss of legitimate feeding without a detectable increase in robbery itself.**

The primary quantitative test is the all-Ecuador bird–flower network. Source metadata indicates unspecified piercing values are most probably legitimate interactions, so the primary analysis recodes missing piercing as non-robbing and treats plant species as the inferential unit:

```text
259 plant species aggregated from 2,265 pair-site units
plant-level mismatch rho = 0.503
species permutation p    = 0.0001
paired barrier species   = 130
mean paired difference   = +0.0915
label-swap p             = 0.0001

descriptive pair-site means:
barrier robbery     = 0.147
accessible robbery  = 0.020
18 / 18 comparable sites in the same direction
complete-case yes/no sensitivity = same plant-level direction

within-bird behavioral checks:
36 bird species paired barrier difference = +0.0933, p = 0.0001
28 bird species / 1,285 bird×plant dyads
within-bird centered-rank rho = 0.340, p = 0.0001
between-bird mean rho = 0.086, p = 0.551 (different estimand)
```

A smaller independent Afrotropical insect network provides corroboration:

```text
57 plant species
tube length vs robbing–thieving balance
rho = 0.347
permutation p = 0.0086
multitrait tube-length block p = 0.211
```

The two networks contribute one rank association each with equal network weight:

```text
rho_J = 0.428
joint permutation p = 0.0001
independent network contributions k = 2
```

Because `k=2`, the joint test does not estimate between-network heterogeneity, a network-population mean, or generality beyond the two analysed systems.

The zero-inclusive rate analysis is **highly sensitive to how anatomical reach is defined**. The preregistered exposed-culmen-only barrier gave pooled RR 1.772 and legitimate RR **1.883 (1.111–3.190)**, in the opposite direction to all tongue-reach scenarios. Since hummingbirds extend their tongues beyond the bill tip, culmen alone is an incomplete proxy for nectar reach; the original result remains preserved rather than silently dropped.

Across three **post-open** hummingbird-only reach multipliers (4/3, 1.8, 2.0× culmen), separately fitted legitimate feeding RRs were **0.354 (0.197–0.635)**, **0.154 (0.087–0.271)**, and **0.100 (0.065–0.155)**: all three 95% CIs exclude 1 below. Robbery RRs were **0.851 (0.328–2.212)**, **0.816 (0.358–1.860)**, and **1.393 (0.729–2.663)**: all CIs include 1, so their rate direction remains unresolved. Descriptive robbery-to-legitimate RR ratios vary from **2.406 to 13.876** across these scenarios, with the 4/3 ratio CI **0.862–6.720** including 1. The former 1.8-only display value **5.311 (1.923–14.672)** is a conditional, not multiplier-integrated, interval.

Route-specific fixed-effect fits retain different positive-margin supports: at 1.8×, robbery 3,371 and legitimate 15,377, with only 2,900 in common among 19,903 constructed hummingbird opportunities. Thus the ratios are descriptive, **not** directly identified common-risk-set substitution factors or algebraic decompositions of the plant-level P1 association. A uniform reach multiplier has not been independently validated for all 49 hummingbird species; species-specific tongue allometry and efficient extraction remain uncertain. The robust conclusion is therefore limited to the three tested post-open scenarios, **not** all possible physiological definitions. See [the own-estimand self-audit](docs/LETTER_ESTIMAND_SELF_AUDIT_2026_10_13.md).

Case et al. (2026) add **published directional corroboration** from a third independent multispecies Hawaiian bird–lobelioid dataset. Their published analysis reports that nectar robbing declines as bill length approaches flower length, equivalent under the BITA orientation to greater flower-minus-bill mismatch being associated with greater robbery. Dryad metadata describe 11 plant and 7 bird species. Because the direction was already public and the fauna is Aves, this dataset is not added to the standardized equal-network statistic: `k=2` remains primary, and a harmonized Case rank effect stays unopened until exact source bytes are verified.

Within the Ecuadorian bird network, the behavioral contrast is also recovered within bird species: 36 species show a positive paired barrier effect overall, and a continuous within-bird analysis across 1,285 bird × plant dyads gives rho = 0.340 (permutation p = 0.0001). The null correlation among 50 bird-species means (rho = 0.086, p = 0.551) is therefore a between-species result, not evidence that route switching disappears at the consumer grain.

## Mechanistic interpretation

The routing result is interpreted through the broader effective-access / exposure framework:

```text
legitimate route becomes harder to use
        |
        +--> exploitation declines, if no bypass exists
        |
        +--> exploitation reroutes, if bypass remains available
```

Source-audited floral-defence cases provide mechanistic context only. The matched effective-domain classifications are author-coded and have not yet undergone outcome-blind independent recoding, so the Letter does not use the matched-domain layer as independent validation and does not make an 11/11 success-rate argument.

## Manuscript graph

Primary submission:

- `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
- `manuscript/FIGURE_PLAN_ACCESS_ROUTING_LETTER_V0.md`
- `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
- `empirical/floral_defence_selectivity/results/joint_access_routing_species_robust.json`
- `empirical/floral_defence_selectivity/results/aubert2026_missingness_dependence_sensitivity.json`

Extended Synthesis reserve:

- `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`
- `manuscript/CLAIM_FREEZE_MACRO_V0.md`
- `manuscript/MACRO_MANUSCRIPT_SOURCE_AUDIT_V0.md`
- `submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md`
- `submission/FUNCTIONAL_ECOLOGY_ADAPTATION_V0.md`

Preserved mechanism-identification foundation:

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- `manuscript/CLAIM_FREEZE.md`

## Claim boundaries

Do not infer:

- causality from either network;
- a unique tube-length effect from Sakhalkar;
- generality across ecological networks from `k=2`;
- a common raw effect size across networks;
- independent validation from the author-coded matched-domain corpus;
- natural prevalence of selective defence;
- a universal mechanistic coefficient.

## Programme boundary

```text
SCH
functional conflict identification

SLK
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
architecture value and evolutionary realization

BITA
access / exposure asymmetry
        ->
interaction routing
        ->
selective defence / interference / bypass
```

## Submission route

```text
1. Ecology Letters — Letter
2. extended BITA Synthesis retained in reserve
3. Functional Ecology — Research Article fallback
4. Oikos — Research fallback
```

External submission remains author-controlled.

## Testing

```bash
python -m pip install -e '.[dev]'
pytest -m "not prose_contract"
pytest -m prose_contract
```
