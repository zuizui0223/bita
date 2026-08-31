# BITA defence-as-escape-route primary-source audit v1

## Audit question

Can a second, antagonist-reducing floral trait `D` provide an ecological escape route from the one-trait attraction trade-off? In the BITA decomposition,

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

the strong version of that claim requires evidence that `D` reduces the **A-dependent antagonist cost** (`rho_delta`), preserves the **A-dependent pollinator benefit** (low `iota_delta`), and does not impose an offsetting direct or joint cost (`kappa_delta`). A positive total interaction is equivalent, within the declared decomposition and outcome scale, to

```text
rho_delta > iota_delta + kappa_delta.
```

This audit asks how far selected primary studies actually reach. It is a targeted audit of high-information systems already present in BITA, not a systematic estimate of how common escape routes are in nature.

## Fail-closed definitions used here

- `rho_delta` is not a marginal `D -> antagonist` effect. It is the `A x D` interaction in antagonist loss recovered through a selective antagonist intervention.
- `iota_delta` is not a marginal `D -> pollinator` effect. It is the baseline-corrected `A x D` interaction in the pollinator contribution.
- `m0_delta` is the `A x D` interaction in pollinator-absent reproduction. It must be measured or biologically justified, not silently set to zero.
- `kappa_delta` is not whatever remains after subtraction. It requires an independent `A x D` construction/allocation-cost assay on a commensurate scale.
- separability requires the `A x D x antagonist x pollinator` four-way diagnostic in a crossed selective-intervention design. Total-fitness interaction evidence cannot be promoted to pathway identification.

Evidence labels are:

```text
DIRECT       the design contains the intervention contrast defining the target estimand
INDIRECT     the design supports a constituent route or a candidate selective mechanism
BOUNDARY     the biology is relevant but does not contain distinct A and D trait axes
ABSENT       the target quantity is not measured or justified
```

## Primary-source evidence matrix

| Study | Primary design and outcome | `rho_delta` | `iota_delta` and `m0_delta` | `kappa_delta` | Separability / escape criterion | Fail-closed claim ceiling |
|---|---|---|---|---|---|---|
| Kessler, Gase & Baldwin 2008, *Nicotiana attenuata* ([Science, DOI 10.1126/science.1160072](https://doi.org/10.1126/science.1160072)) | Field experiment independently silenced the floral attractant benzylacetone and nicotine production in all four combinations. The source reports pollinator visitation, florivory, nectar robbing, male and female outcrossing. Nicotine reduced florivory and robbing; both nicotine and benzylacetone were required for maximal visitation and outcrossing. | **INDIRECT route support only.** Nicotine has an antagonist-reducing role, but antagonist presence was observed, not independently toggled across the four trait states. Therefore the study does not isolate the `A x D` antagonist-loss contrast. | **INDIRECT route support only; `m0_delta` ABSENT.** The result that both compounds support outcrossing is compatible with little or even beneficial pollinator-side interference in this system, but it does not identify `iota_delta`. Emasculation and a no-pollinator weather day do not replace a crossed pollinator intervention. | **ABSENT.** No independent joint construction/allocation-cost assay. Systemic nicotine silencing also allows non-floral consequences into plant-level fitness. | The BITA aggregate reconstruction gives a descriptively positive, sign-robust discrete `Delta_AD W` range from published rounded capsule proportions, but the source does not report formal interaction uncertainty and has no `A x D x G x P` test. Thus the study is the closest **trait-factorial, total-interaction anchor**, not channel identification. A positive escape inequality is descriptively compatible, not formally established. | A crossed A/D-like phenotype can yield positive reproductive non-additivity. Do not claim identified `rho`, `iota`, `kappa`, separability, or a flower-exclusive defence mechanism. |
| Egan et al. 2021, *Fragaria vesca* ([Evolution Letters, DOI 10.1002/evl3.262](https://doi.org/10.1002/evl3.262); [open article](https://academic.oup.com/evlett/article/5/6/636/6697546)) | Full-factorial common garden crossed herbivore addition/removal with open/supplemental hand pollination and measured total seed output. It estimated agent-mediated selection on nine measured attraction- and defence-related traits. Inflorescence density experienced opposing herbivore- and pollinator-mediated selection; agent-mediated selection was context dependent. | **INDIRECT design-side support.** The study manipulates ecological agents, but it does not independently manipulate one floral A and one floral D or fit their trait-by-trait interaction. Several defence metabolites are leaf-derived. | **INDIRECT design-side support; `m0_delta` ABSENT.** Open versus supplemental hand pollination is not pollinator present versus selectively excluded, and it does not identify pollinator-absent reproduction. | **ABSENT.** No independent floral `A x D` cost assay. | No manipulated `A x D`, hence no `A x D x G x P` separability diagnostic and no total `Delta_AD W` for the focal trait pair. | Pollinator and herbivore contexts jointly alter selection on attraction/defence-related traits. This is the complementary **consumer-factorial anchor**, not evidence that a particular D releases a particular A from trade-off. |
| Soper Gorden & Adler 2018, *Impatiens capensis* ([American Journal of Botany, DOI 10.1002/ajb2.1182](https://doi.org/10.1002/ajb2.1182); [data DOI 10.5061/dryad.0j96d17](https://doi.org/10.5061/dryad.0j96d17)) | Field experiment randomly simulated increased florivory, nectar robbing and pollination. The source reports non-additive treatment effects on later visitors and reproduction. The deposited individual-plant panel contains pre-treatment flower redness, floral condensed tannins, and reproductive components. BITA's predeclared retrofit estimates observational `redness x tannins` terms and their randomized treatment modifiers. | **INDIRECT / unresolved.** A and D are observed, not manipulated; agent treatments are intensity additions rather than selective exclusions. The randomized `A x D x florivory/robbing` modifiers therefore cannot be renamed `rho_delta`. | **INDIRECT / unresolved; `m0_delta` ABSENT.** The `A x D x pollination` modifier is not a pollinator-presence increment and all relevant retrofit intervals cross zero. Pollinator-absent reproduction was not recovered. | **ABSENT.** No independent joint-cost assay. | No four-way selective-intervention diagnostic. BITA's two observational `A x D` reproductive-component estimates have opposite point signs and both confidence intervals include zero; all eight total/modifier intervals in the broader retrofit cross zero. | This is a high-information **observational trait-pair plus randomized context-modification anchor**. It demonstrates exactly where reanalysis stops; it does not establish an escape route or a stable interaction sign. |
| Sun & Huang 2015, *Pedicularis rex* ([AoB PLANTS, DOI 10.1093/aobpla/plv019](https://doi.org/10.1093/aobpla/plv019); [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4392828/)) | Experimentally drained water-holding cupulate bracts and measured legitimate pollinator visits, nectar-robber visits, seed predation and seed set. Draining strongly increased seed predation; legitimate pollinators and robbers did not discriminate detectably between intact and drained treatments. Robbers bypassed the barrier by piercing above the water. | **INDIRECT but biologically strong.** The same D manipulation causally reduces one antagonist route, but no independent A contrast is present, so the A-dependent relief contrast is not estimated. | **INDIRECT guarded-state evidence; `m0_delta` ABSENT.** The same manipulation did not detectably reduce pollinator visitation, but a marginal null-compatible D effect is not `iota_delta = 0`. | **ABSENT.** No A axis and no joint-cost assay. | No A/D trait factorial and no consumer four-way diagnostic. The escape inequality is not evaluable. | A flower-associated physical defence can be attack-mode selective and protect reproduction without a detected pollinator-visitation penalty. This is the strongest **system-selection anchor** for a future escape-route experiment, not parameter identification. |
| Kessler et al. 2019, *Nicotiana attenuata* ([Functional Ecology, DOI 10.1111/1365-2435.13332](https://doi.org/10.1111/1365-2435.13332); [primary repository DOI 10.17617/3.24](https://doi.org/10.17617/3.24)) | Floral benzylacetone emission was silenced and florivore colonization/damage were measured over field seasons and timed feeding assays. The article reports more *Diabrotica undecimpunctata* colonization and floral damage when benzylacetone is absent, and demonstrates temporal and concentration-dependent sensory effects. | **BOUNDARY, not `rho_delta`.** Benzylacetone is one dual-function floral trait with both pollinator-attracting and defensive roles. Ecological functions do not create two independent trait axes. | **BOUNDARY.** This study does not independently cross a defence trait with the attractive benzylacetone axis or estimate pollinator-side A/D interaction. | **ABSENT.** | No distinct A/D factorial or crossed consumer design. The public field-data reconstruction also retains a one-observation 2014 source/deposit discrepancy rather than silently repairing it. | An attractive signal can itself deter a florivore, showing multifunctionality and temporal gating. This is a boundary case for the one-trait/shared-cue problem, not evidence that a second D enables escape in BITA. |
| Knauer, Bakhtiari & Schiestl 2018, *Biscutella laevigata* ([Nature Communications, DOI 10.1038/s41467-018-03792-x](https://doi.org/10.1038/s41467-018-03792-x)) | Field and behavioural experiments show that beta-ocimene attracts both bees and crab spiders; spiders reduce bee visitation, but remove florivores and reduce their negative fitness effect. A crossed spider-by-florivore experiment produced a positive interaction on seed set, and florivory induced the spider-attracting volatile. | **BOUNDARY / INDIRECT mechanism support.** Spider presence can relieve florivore cost, but the spider is an ecological agent rather than an independently manipulated plant D trait crossed with A. | **BOUNDARY / INDIRECT interference support.** Spiders reduced bee visits and changed the association between beta-ocimene and bee visitation, demonstrating a real mutualist cost of antagonist control, but not `iota_delta` for an A/D plant-trait pair. `m0_delta` is absent. | **ABSENT.** | The spider-by-florivore fitness interaction is not the BITA `A x D x G x P` diagnostic. No floral A/D trait factorial or independent cost assay exists. | Antagonist control can switch from costly to beneficial when florivores are present, and the same signal can recruit mutualists and an antagonist-removing predator. This validates context-dependent mechanism logic, not BITA channel allocation. |

## What is positively recovered

The primary literature does recover three biologically important parts of the proposed mechanism.

1. **Selective defence without an obvious pollinator-visitation penalty exists.** The strongest example in this set is the experimentally drained water barrier of *Pedicularis rex*: seed predation rises when the barrier is removed, while legitimate visitors show no detected treatment response. This makes a low-interference defence biologically credible.
2. **A crossed attraction/defence-like phenotype can show positive reproductive non-additivity.** Kessler et al. (2008) is unusually close to the required A/D trait factorial. BITA's reconstruction preserves a positive discrete interaction across the rounded published capsule proportions, so an escape-compatible total pattern is not merely theoretical.
3. **The balance is genuinely context dependent.** Egan et al. show that pollinator- and herbivore-mediated selection depends on the other agent; Knauer et al. show experimentally that a pollinator-deterring spider becomes beneficial by removing florivores; *Impatiens* supplies a public-data example in which plausible trait interactions remain weak and component dependent.

These are positive ecological results: the theory-defined routes recur, a selective-D candidate exists, and at least one close trait factorial is compatible with positive total complementarity.

## What is not recovered

None of the six focal studies identifies the full defence escape route as a mechanism allocation.

```text
direct rho_delta:                    0 studies
baseline-corrected iota_delta:      0 studies
measured/justified m0_delta:        0 studies under the full crossed design
independent kappa_delta assay:      0 studies
A x D x G x P separability test:    0 studies
full point identification:          0 studies
```

The zeroes are design-coverage statements for this targeted high-information set, not prevalence estimates. They do not mean the mechanisms are absent. They mean that present studies occupy complementary faces of the identification problem.

## Study-by-study minimum augmentation

| Starting system | Smallest high-value augmentation | What it would add | What would still remain |
|---|---|---|---|
| Kessler 2008 | Local or flower-restricted nicotine manipulation plus selective antagonist and pollinator interventions crossed with the four trait states | Converts the strongest trait factorial toward direct `rho_delta` and `iota_increment_delta` estimation | `m0_delta`, separability validation and an independent cost assay still require explicit treatment |
| Egan 2021 | Manipulate one biologically valid floral A and one flower-specific D on the existing consumer-factorial backbone | Adds the missing trait-factorial side | Supplemental hand pollination must become an interpretable pollinator-state contrast; leaf-derived D is insufficient |
| Impatiens 2018 | Randomize or experimentally manipulate redness and floral tannins, then replace interaction additions with selective consumer toggles | Moves observational A/D context modification toward causal channel contrasts | Pollinator-absent baseline and joint cost remain separate gates |
| Pedicularis 2015 | Add an independent floral-attraction manipulation to the water-bract system | Tests whether the selective barrier changes A-dependent seed-predator cost and pollinator benefit | True antagonist/pollinator toggles, `m0_delta`, cost and separability remain necessary |
| Kessler 2019 | Introduce a distinct, independently manipulable D rather than relabelling benzylacetone's defensive function | Creates a genuine two-trait question | All channel interventions and cost information would still be required |
| Knauer 2018 | Manipulate a plant defence trait separately from the attractive beta-ocimene axis while retaining the crossed ecological-agent experiment | Connects conditional antagonist control to a plant A/D architecture | Selective pollinator state, `m0_delta`, joint cost and four-way interpretation require redesign |

## Bottom-line adjudication

The empirical literature supports the **plausibility** of defence as an escape route more strongly than it supports its **identification**.

The most defensible manuscript claim is:

> Existing experiments recover each major biological ingredient of the proposed escape route in complementary systems: attraction/defence-like reproductive non-additivity, selective antagonist reduction with no detected pollinator-visitation penalty, and context-dependent costs of antagonist control. The screened studies do not yet identify `rho_delta`, baseline-corrected `iota_delta`, `kappa_delta`, or separability in one linked experiment. BITA therefore explains both how far current data reach and exactly which additional interventions would convert route plausibility into mechanism identification.

The manuscript should not claim:

> Existing studies show that defence generally releases floral attraction from its antagonist trade-off.

## Provenance note

All biological design and outcome claims above were checked against the linked primary articles or their first-party data repositories. Numerical BITA interaction summaries for Kessler 2008 and the *Impatiens* trait-pair retrofit are project reconstructions, not source-reported coefficients; their inference limits remain documented in `empirical/identification_design/KESSLER_2008_IDENTIFICATION_REAUDIT_V2.md` and `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.md`.
