# Primary-source role sensitivity of the 2019 nectar meta-analysis

## Status

**The broad negative result is reproducible and persists after a declared defence-association screen. The strict same-system evidence remains too sparse and internally mixed for a canonical bita pathway estimate. The manuscript remains frozen.**

This analysis starts from the nine paper-level summaries reproduced from Parachnowitsch, Manson and Sletvold (2019; doi: `10.1093/aob/mcy132`). Each paper was returned to its primary source and assigned to fixed evidence tiers in `PARACHNOWITSCH2019_ROLE_AUDIT_V1.csv`. The tiers change only the evidential provenance of the focal trait. They do not add a biological mechanism, alter the theory, or estimate a new parameter.

## 1. Four transparent evidence tiers

### Published broad set

The first tier retains all nine papers and exactly reproduces the broad review question: responses to nectar secondary metabolites. It includes studies of visitation, consumption, cognition, infection context, multiple consumer groups, and traits whose flower-specific antagonist-reduction role is not established.

### Defence-associated primary sources

The second tier retains five papers whose primary source explicitly connects the focal nectar chemistry to defence, visitor filtering, or a chemically defended plant context:

- Adler and Irwin (2005);
- Johnson, Hargreaves and Brown (2006);
- Jones and Agrawal (2016);
- Köhler, Pirk and Nicolson (2012);
- Manson et al. (2013).

This remains broader than bita's strict route. In particular, the Köhler and Manson studies do not directly demonstrate antagonist reduction in the same experimental system.

### Defence-associated set plus the unresolved 2016 workbook identity

The supplement labels one positive paper-level summary as `Zhang et al 2016`. Its year, trait, bee taxa, assay design and response pattern are consistent with Tiedeken et al. (2016; doi: `10.1111/1365-2435.12588`), but the source authorship conflicts with the workbook label. The third tier includes this row only as a provisional identity sensitivity. The original workbook label is preserved, and the row is not treated as source-resolved.

### Same-system role-verified sources

The fourth tier retains only three primary studies where the focal source itself establishes a defence or visitor-filter role in the same biological system:

- Adler and Irwin (2005): nectar defence, pollinators and nectar robbers;
- Johnson et al. (2006): floral visitor filtering, effective pollinators and mismatched nectarivores;
- Jones and Agrawal (2016): cardenolide defence, mutualist bees and antagonist butterflies.

Even this tier is not a canonical B-to-legitimate-pollinator meta-analysis because the published paper summaries mix years, consumer roles, or theory pathways.

## 2. Results

| Evidence tier | Independent papers | Random-effects Hedges g | 95% CI | I² |
|---|---:|---:|---:|---:|
| Published broad set | 9 | -0.444 | -0.666 to -0.223 | 85.9% |
| Defence-associated, source verified | 5 | -0.631 | -0.978 to -0.283 | 87.7% |
| Defence-associated plus provisional 2016 identity | 6 | -0.453 | -0.840 to -0.067 | 90.3% |
| Same-system role verified | 3 | -0.462 | -1.065 to 0.142 | 89.1% |

The broad negative result is therefore not created solely by the health, memory, or weak-role papers. It remains negative when analysis is restricted to the five source-verified defence-associated studies. It also remains negative after adding the positive, provisionally identified 2016 paper.

However, the uncertainty expands sharply when only same-system role evidence is retained. The point estimate remains negative, but the interval includes zero. This is the expected consequence of a smaller evidence base and of unresolved mixing inside the published paper summaries, not evidence that the strict pathway is absent.

## 3. What is empirically supported

The current synthesis supports the following restricted statement:

> Across the published nectar-secondary-metabolite literature, higher expression or concentration of defence-associated floral chemistry is, on average, associated with lower measured pollinator use or consumption, but the effect is highly heterogeneous and is not a universal property of the trait label.

This conclusion is reinforced by the primary-source audits:

- Manson et al. show reductions only far above natural nectar concentrations.
- Villalona et al. show null, positive, and negative responses across dose and bee species, with the strongest deterrence at a supra-natural dose that also causes illness.
- Johnson et al. show that a floral filter can exclude mismatched visitors while leaving effective pollinators comparatively unaffected.
- Jones and Agrawal show that a natural-range cardenolide treatment can initially increase bee visits, whereas deterrence emerges over repeated colony foraging.

The empirical pattern is therefore conditional in exactly the ecological sense needed by the fixed theory: pollinator interference can occur, but its direction and magnitude depend on dose, consumer identity, assay duration, and response construct.

## 4. What is not yet supported

None of the four tier estimates is a direct estimate of `iota`, `rho`, `kappa`, or `W_AD`. The sensitivity analysis does not repair the following source-level problems:

- consumer-role mixing in Johnson et al.;
- pollinator and antagonist-path mixing in Jones and Agrawal;
- year and dose mixing in Adler and Irwin;
- visit-number and visit-length mixing in Manson et al.;
- multiple dependent concentration and sugar contrasts in Köhler et al.;
- unresolved source identity for the workbook's `Zhang et al 2016` label.

Consequently, the strict same-system tier is a diagnostic of evidence sufficiency, not a publishable strict-pathway meta-analysis.

## 5. Next quantitative target

The next work should replace broad paper summaries with role-correct, outcome-specific effects rather than add another statistical layer. Priority is:

1. separate the legitimate bee response from the monarch response in Jones and Agrawal (2016), retaining individual-bout and colony-duration assays separately;
2. retain Adler and Irwin's natural-range 2004 visitation effect as the single primary effect for that study cluster;
3. extract visit-number effects from Manson et al. by dose, without combining visit duration;
4. separate effective pollinator birds from mismatched visitors in Johnson et al.;
5. recover the repeated-choice dependence or a source-reported primary contrast for Köhler et al.

This route can determine whether an outcome-compatible, legitimate-pollinator-only synthesis reaches the existing exploratory threshold of three independent studies. Moderator analysis remains secondary.

## Manuscript decision

No manuscript text, figures, theorem statements, or journal framing are changed. Manuscript work remains frozen under `ANALYSIS_COMPLETION_GATE.md`.
