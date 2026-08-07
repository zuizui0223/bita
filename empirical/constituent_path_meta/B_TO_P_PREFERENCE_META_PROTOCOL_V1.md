# B-to-pollinator preference meta-analysis protocol v1

## Empirical target

This analysis addresses one constituent pathway of the fixed attraction-defence theory:

> Does increasing a source-verified flower-specific defence/access-restriction trait alter legitimate pollinator use?

The primary quantitative lane is deliberately narrower:

> direct pollinator preference/choice responses to experimentally varied flower defensive chemistry.

This analysis can support the biological reality and direction/context dependence of the `B_to_pollination` pathway. It does **not** estimate the cross-partial `iota=-M_AD`, because most studies manipulate `B` without jointly manipulating the same focal attraction trait `A`.

## Trait-role inclusion gate

A study enters the primary B-to-pollinator pool only if the source supports all of the following:

1. the manipulated trait occurs in the flower, floral nectar, pollen, or a flower-specific access structure;
2. the source independently identifies an antagonist-reduction, resistance, deterrence, defence, filtering, or access-restriction role for that trait;
3. the pollinator/visitor is a legitimate mutualist for the focal biological system or an explicitly justified pollinator assay taxon;
4. the manipulation or comparison isolates the focal trait sufficiently to recover a directional pollinator response;
5. a numerical effect and its sampling uncertainty are recoverable from reported statistics or public source data.

A compound is not coded as `B` merely because it is a secondary metabolite or toxic in another context.

## Primary outcome lane

The primary lane is preference/choice. It includes experiments where pollinators choose between otherwise matched flowers/feeders differing in the focal B trait or concentration and where the response can be represented as a study-level preference for the higher-B option.

Do not pool the following into this primary lane:

- visitation rate without a simultaneous or source-comparable choice construct;
- time per flower or residence time;
- nectar volume consumed;
- pollen transfer;
- fruit or seed production;
- learning or memory scores;
- survival, mobility, or physiological performance.

These are retained as secondary lanes because prior source screening shows they can move in different directions within the same experiment.

## Effect orientation

All effects are oriented so that:

- negative = higher B reduces pollinator preference/use;
- zero = no directional preference/use difference;
- positive = higher B increases pollinator preference/use.

When the source reports a binary choice proportion against a neutral 0.5 benchmark and provides a study-level mean plus SD/SEM and sample size, a standardized one-sample effect may be reconstructed using the reported statistics. Repeated choices within an individual are not treated as independent observations; the experimental unit reported by the source is retained.

If a source provides raw individual-level choice data, the preferred route is to estimate the treatment contrast directly from those data with the experimental unit and repeated-measure structure preserved.

## Dose/context treatment

Dose is not averaged away before analysis when the source shows dose dependence.

Each effect is labelled using the source's own biological context where possible:

- natural/field-relevant range;
- high end of natural range;
- supra-natural/elevated experimental range;
- not classifiable from source.

No universal concentration threshold is imposed across compounds.

Multiple dose effects from one paper remain in the same `independence_cluster`. They are not counted as independent studies.

## Independence

The independent-study count is based on biological study/panel identity, not the number of effect rows. Multiple compounds, doses, pollinator species, outcomes, sites, years, or papers sharing the same experimental panel are audited for dependence before pooling.

## Quantitative synthesis gate

The existing repository thresholds are retained:

- k < 3 independent clusters: report extraction/status only; no pooled estimate;
- k >= 3: exploratory random-effects synthesis may be reported;
- k >= 5: stability analyses become eligible.

The manuscript remains frozen until the analysis completion gate in `ANALYSIS_COMPLETION_GATE.md` is met.

## Planned synthesis

Once the minimum gate is met:

1. estimate the overall oriented B-to-pollinator preference effect with study dependence handled explicitly;
2. preserve dose class as a moderator/sensitivity distinction when sufficient independent studies exist;
3. run leave-one-study-out sensitivity only when k is large enough to be interpretable;
4. report the result as evidence for the constituent B-to-pollinator pathway, not as an estimate of `iota` or the full attraction-defence interaction.

## External benchmark

Parachnowitsch, Manson & Sletvold (2019; doi:10.1093/aob/mcy132) previously meta-analysed pollinator responses to nectar secondary metabolites and reported that these compounds generally reduced pollinator preferences while also emphasizing concentration-dependent, neutral, and positive low-dose responses. Their individual effect-size data are listed as supplementary material. This prior synthesis is treated as an external benchmark and source-recovery target, not copied into the present effect table without study-level audit.

Post-2019 studies are screened as an update layer, including the milkweed/cardenolide work of Villalona et al. (2020) and Jones, Warburton & Martin (2023), which explicitly report dose-dependent pollinator responses.
