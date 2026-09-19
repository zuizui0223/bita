# Functional Ecology fallback adaptation v0

Candidate source:

manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md

This adaptation is held in reserve while the Ecology Letters Synthesis proposal is the first editorial test.

## Numbered abstract draft

1. Flowers must remain accessible to mutualists while limiting antagonists that use the same structures and rewards. We develop an effective-exposure framework in which antagonists and pollinators differ in access, susceptibility, timing and response thresholds. The model predicts a selective window when antagonist suppression occurs before pollinator interference, collapse of selectivity under strong overlap, failure under bypass, and route switching when exploiters circumvent barriers.

2. We tested these predictions using four evidence layers: a deduplicated D-side route-level synthesis, a stricter matched-defence state analysis, a within-system conditionality synthesis, and an independent public-data reanalysis of an Afrotropical flower–visitor network.

3. The broad D-side route corpus contains 17 unique study programs spanning chemical (9), physical (7) and reward/access (1) implementations; 10 programs also contain same-study pollinator outcomes, which split among context-dependent (4), null-compatible (3), improved (1), interference (1) and unresolved (1) states. The stricter matched-defence corpus contains 17 systems. Eleven systems are directly scorable in a broader ecological-state analysis. All nine scorable historical systems and both systematic-expansion systems match the fixed prediction that separated domains show no observed pollinator interference, transitional domains show mixed responses, and overlap shows impairment. A coarse defence-modality classifier recovers 6/9 historical systems by leave-one-out prediction and 1/2 expansion systems. Null-compatible outcomes remain distinct from equivalence, and the narrower direction-supported Stage-2 subset remains only three systems.

4. Eight independent defence-side systems show state switching with dose, cumulative exposure, consumer identity, response stage or temporal expression. Two independent network reanalyses recover access routing in different faunas. In the Sakhalkar insect network, tube length is associated with robbing-versus-thieving balance among 57 plant species (Spearman rho = 0.347; permutation p = 0.0086). In the Aubert/EPHI Ecuador bird-network extension, mean robbery is 0.307 under flower-tube–bill barriers versus 0.081 when accessible across 1,378 pair-site units, with the same direction in 15/17 comparable sites (sign-test p = 0.00235; site-stratified permutation p = 0.0001).

5. Across case, within-system and community scales, floral defence selectivity is best treated as a state of trait × consumer × context. Access and exposure structure can organize whether antagonists are suppressed, mutualistic function is retained or impaired, and exploiters switch routes. We do not infer a universal causal coefficient or prevalence estimate.

Approximate length: <350 words.

## Replication statement draft

The primary comparative unit is one independent study cluster × one focal flower-associated defence/access axis × one declared ecological context. Repeated outcomes, doses, years, populations or consumers within a study do not create independent biological replication unless the source design establishes independence. The Sakhalkar network reanalysis uses plant species as the inferential unit; individual visit records are not treated as independent replicates. The Aubert/EPHI extension uses bird species × plant species × site as the inferential unit; individual camera interactions are first aggregated within those units. Site-stratified and minimum-interaction sensitivities are retained separately. All corpus counts, exact tests and public-data aggregate results are regenerated in continuous integration from committed source-adjudicated tables and public repositories.

## Data Sources section structure

Functional Ecology asks submissions using multiple published sources to cite those data sources in the manuscript or provide a separate Data Sources section.

### Data Sources — matched-defence synthesis

List all 17 admitted primary systems in alphabetical order, using the DOI-bearing primary source.

Do not merge linked-program contextual papers into the strict matched-D source list.

### Data Sources — conditionality synthesis

List the eight defence-side source studies underlying empirical/floral_defence_selectivity/d_side_conditionality_registry.csv.

Repeated switch records from one publication remain one Data Source entry.

### Data Sources — public network reanalyses

Sakhalkar et al. 2023 paper DOI: 10.1002/ecs2.4696

Public data/code DOI: 10.5281/zenodo.8398202

State explicitly that the deposited workbook currently yields 14,383 rows after the source-script filter, eight fewer than the paper summary count of 14,391.

Aubert et al. 2026 paper DOI: 10.1002/oik.11552

Public EPHI Ecuador mirror DOI: 10.5281/zenodo.14185547

State explicitly that the BITA analysis is an all-18-site extension using the public EPHI mirror and pair-site aggregation, not an exact reproduction of the published three-transect mixed model.

## Functional Ecology cover-letter spine

Lead in this order:

1. mechanism: effective access/exposure thresholds create a selective window;
2. macro result: the same access-routing direction recurs in two independent public networks—Afrotropical insect cheating modes and Ecuadorian bird–flower access barriers—while both remain observational;
3. cross-system evidence: 17 unique route-level D programs, 17 matched systems including 11 scorable ecological-state systems (9/9 historical + 2/2 expansion), plus 8 within-system conditionality systems;
4. methodological strength: outcome-blind architecture coding, independent cluster counting, exact Stage-2 claim gate;
5. restraint: no domain>modality or universal-prevalence claim.

Do not lead with the old “trait interaction is not mechanism” result.

## Formatting changes needed only after route activation

- switch the abstract to the numbered version above;
- add line and page numbers in the rendered submission file;
- keep standard Introduction / Materials and Methods / Results / Discussion structure;
- add the replication statement to Methods;
- add a separate Data Sources section;
- ensure title page is separated for double-anonymous review;
- keep the main text under the point where a >7,500-word length justification is required.

Current candidate source is already structurally close to this format.
