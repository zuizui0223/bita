# Leal 2025 robber-study label provenance audit v1

## Decision

The 56 distinct values in the Leal et al. (2025) `study` column are frozen as
**56 historical source labels**, not as 56 verified independent study programs.

Do not use the phrase `56 unique studies` for the formal geometry-recurrence
frame until the two split-required labels below are source-resolved. However,
the direct-geometry **eligibility** of those two labels is now resolved as stably
ineligible under every verified/credible source component.

## Audit trigger

The public `complete_hedges.csv` file was grouped by `study` and inspected for
labels containing more than one plant species. Six labels met that condition.

Four are legitimate multi-species source programs:

- `Arizmendieetal1996`: *Salvia mexicana* + *Fuchsia microphylla*;
- `Bergamo&Sazima2018`: *Besleria longimucronata* + *Crotalaria vitellina*;
- `Burkleetal_2007`: *Linaria vulgaris* + *Delphinium nuttallianum*;
- `Irwinetal_2008`: *Ipomopsis aggregata* + *Polemonium viscosum*.

Two labels contain plant records that cannot all originate from the named source.

## Conflict 1 — Varma&Sinu2019

Leal rows under this one label contain:

~~~text
Embothrium coccineum
Sesamum radiatum
~~~

The verified Varma & Sinu paper is exclusively:

> Varma S, Sinu PA (2019) Nectar robbing in bellflower (*Sesamum radiatum*)
> benefited pollinators but unaffected maternal function of plant reproduction.
> *Scientific Reports* 9:8357. DOI 10.1038/s41598-019-44741-y.

Therefore the *Embothrium coccineum* rows cannot be assigned to Varma & Sinu 2019.

A biologically and temporally plausible source is:

> Valdivia CE, Orellana JI, Morales-Paredes C (2018)
> Ant-mediated nectar robbing from the Chilean firetree *Embothrium coccineum*
> (Proteaceae): no effect on seed production.
> *Annales Botanici Fennici* 55:217–226.
> DOI 10.5735/085.055.0403.

That candidate is **not yet accepted as the row-level source** merely from topic
matching. Exact numeric/provenance confirmation is still required before
reassignment. This source uncertainty no longer affects the geometry screen:
Varma & Sinu 2019 and the credible Embothrium source both test consequences of
robbery rather than access geometry as the predictor of robbery.

## Conflict 2 — Zhangetal2009a

Leal rows under this label contain:

~~~text
Corydalis ternatifolia
Corydalis tomentella
Corydalis incisa
Glechoma longituba
~~~

The verified Zhang et al. paper is:

> Zhang Y-W et al. (2009) Differential effects of nectar robbing by the same
> bumble-bee species on three sympatric *Corydalis* species with varied mating
> systems. *Annals of Botany* 104:33–39.
> DOI 10.1093/aob/mcp104.

It explicitly concerns the three *Corydalis* species. The *Glechoma longituba*
rows therefore require a separate source mapping.

Several Zhang-group *Glechoma* programs occur in the same time window, including:

- Zhang et al. 2007, DOI 10.1007/s11258-006-9244-y;
- Zhang et al. 2009, DOI 10.1111/j.1420-9101.2008.01669.x;
- Zhang et al. 2011, DOI 10.1111/j.1438-8677.2009.00279.x.

The two *Glechoma* rows are not reassigned until their exact source is resolved.
For the geometry screen, however, the verified Corydalis paper and every currently
plausible Glechoma source program are geometry-ineligible, so source resolution
cannot add an eligible direct-geometry program.

## Consequence for the formal recurrence frame

Current state:

~~~text
LEAL_STUDY_FIELD_LABELS = 56
MULTI_PLANT_LABELS = 6
LEGITIMATE_MULTI_SPECIES_LABELS = 4
PROVENANCE_CONFLICT_LABELS = 2
PROVENANCE_CONFLICT_GEOMETRY_ELIGIBILITY = STABLE_INELIGIBLE
HISTORICAL_DIRECT_GEOMETRY_ELIGIBLE_SET = RESOLVED_AT_4
SOURCE_RESOLVED_INDEPENDENT_PROGRAM_COUNT = NOT_YET_FINAL
FORMAL_RECURRENCE_RESULT = CLOSED
~~~

The historical geometry-eligibility screen is now complete: 52 labels are
geometry-ineligible (including the two provenance conflicts) and four are eligible.
The all-study source-resolved denominator is still unavailable, and the formal
recurrence statistic also remains blocked by the lack of a finite, exportable,
deduplicated geometry-specific bibliographic update frame.

This audit is about source identity only; it does not change the standardized
Letter network result (`k = 2`).
