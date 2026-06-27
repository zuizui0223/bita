# Megachile leaf-material-use meta-analysis feasibility program

## Goal

Build a cross-study dataset for asking whether plant traits predict observed leaf-material use by leaf-cutting bees. The intended first endpoint is **guild-level plant-material use**, not species-specific host choice.

\[
\Pr(\text{leaf-material use of plant }i)
= f(\text{leaf traits},\text{plant availability},\text{region},\text{study design}).
\]

This repository will not call a plant trait a defence trait merely because it covaries with leaf use. Leaf traits must remain separated into mechanical-resistance proxies, processing/accessibility traits, leaf-economics traits, and chemical-defence proxies.

## Two possible evidence targets

### Target A: selection / preference meta-analysis

A study is eligible when it has plant-level use or damage observations **and** a defined available/background plant pool or sampling-effort denominator.

This supports a use-versus-availability response.

### Target B: use-side synthesis

A study is eligible when it has extractable plant-level leaf-use observations but lacks a background pool.

This can describe the trait distribution of plants used by leaf-cutting bees, but cannot by itself estimate preference or avoidance.

Target B can be used while Target A is still being assembled; the two endpoints must not be pooled as if they answer the same question.

## Meta-analysis readiness thresholds

These are feasibility gates, not universal statistical laws.

| Level | Minimum evidence | Permitted conclusion |
|---|---|---|
| Not ready | fewer than 5 independent study-landscapes or no extractable plant-level records | continue discovery; no pooled analysis |
| Descriptive synthesis | at least 5 study-landscapes, at least 150 plant-level use records, at least 75 accepted plant taxa | describe used-plant trait distributions only |
| Provisional comparative analysis | at least 8 study-landscapes across at least 3 regions, at least 300 plant-level use records, study identifier retained | fit study-random-effect descriptive models |
| Selection meta-analysis | at least 10 study-landscapes, at least 500 plant-level observations, and at least 7 studies with explicit background/availability data | analyse use relative to availability with study-level random effects |

A study-landscape is an independent combination of study, location or landscape, and sampling period. Multiple tables from one landscape do not count as independent studies.

## Adaptive source routes

The source routes are tested in this order:

1. **Published community-level leaf-cut surveys**: plant-level cut-mark, use, or event tables.
2. **Nest-material and trap-nest studies**: plant IDs from nesting material, microscopy, barcoding, or direct observation.
3. **Open supplements and data repositories**: Dryad, Zenodo, Figshare, institutional repositories, appendices.
4. **Curated interaction databases**: only if the original record, locality, and interaction type are preserved.
5. **Citizen-science / image records**: discovery or calibration only unless species IDs, plant IDs, direct action, and observation metadata are all retained.
6. **Standardised field campaign**: sentinel plants plus local availability survey and trap nests; this becomes the primary empirical route if public data remain insufficient.

## Adaptive decision rule

For each source route, screen an initial batch of 25 candidate publications or datasets and record every candidate in `study_registry.csv`.

- If a route yields at least 3 studies eligible for Target A or Target B, expand the route to 75 candidates.
- If it yields 1–2 eligible studies, retain it as a secondary route and move to the next route.
- If it yields 0 eligible studies after 25 candidates, stop using it as a primary route.
- Once the descriptive or selection readiness threshold is met, stop broad discovery, lock the registry version, and begin extraction.

The objective is not to keep searching forever. It is to make each pivot auditable.
