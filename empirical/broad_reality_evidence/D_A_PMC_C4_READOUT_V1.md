# d_A PMC route screen and C4 target v1

## Scope

This records a source-feasibility screen for the two registered PMCID leads in
`d_A_candidate_scouting_v1.csv`. It does not add a verified effect or modify the
Part B effect table.

```text
workflow:     Resolve d_A candidate sources
workflow run: 28642363462
artifact:     d-a-source-receipts
screened:     PMC11442331 (Parnassia), PMC8795787 (Aerides)
method:       exact PMC XML with section-heading and figure/table locators
```

## Result

| Candidate | Track | Structural result | Handling |
|---|---|---|---|
| Parnassia wightiana (`10.1002/ece3.70380`) | visual/display | `Staminodes Removal Experiments` and `Florivory Dynamics` headings both occur. | Retain as the first visual/display `d_A` C4 target. |
| Aerides odorata (`10.3389/fpls.2021.767725`) | unresolved display/scent | Headings describe larceny/florivory effects on pollinator behavior and fruit set, with no trait-intervention heading. | Do not code as `d_A`; retain only as a possible H-to-P source. |

## Parnassia reading target

```text
candidate:              dA_cand_parnassia
empirical track:        visual_display
trait intervention:     Staminodes Removal Experiments; Staminode Removal Experiments
antagonist outcome:     Florivory Dynamics
referenced figures:     FIGURE 1; FIGURE 3
source access:          full-text XML recovered
C4 status:              needs_manual_model_and_effect_context
```

Before any effect row is created, read the intervention and florivory sections
together and record treatment/control definition, antagonist denominator,
experimental unit, replication, model coefficient or raw contrast, uncertainty,
and exact table/figure/section locator.

## Boundary

The XML screen does not establish an effect direction or effect size. It only fixes
the first source-specific reading target for the visual/display `d_A` track. The
scent/reward `d_A` track remains separate and still needs compatible evidence.
