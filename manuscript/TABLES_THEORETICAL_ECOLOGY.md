# Tables for Mechanism → Pattern Theoretical Ecology submission

## Part I — Mechanism

## Table 1. Mechanistic definitions, required declarations, and inference boundaries

| Symbol | Meaning | Required declaration | Does not imply |
|---|---|---|---|
| \(A\) | One focal floral attraction trait | Biological measurement, units or scaling, and orientation | Omnibus floral attractiveness |
| \(D\) | One focal flower-specific trait with an antagonist-reduction role | Target antagonist, reduction mechanism, measurement, and orientation | Any trait that merely obstructs pollinators |
| \(W\) | Fitness or biological-outcome surface | Units, transformation, ecological context, and focal point | Transformation-invariant fitness |
| \(W_{AD}\) | Local mixed partial of the declared outcome surface | Declared coordinates and evaluation point | Trait covariance, genetic correlation, optimum, or trajectory |
| \(\rho\) | Antagonist-relief magnitude | Orientation gate and channel definition | Total defence benefit |
| \(\iota\) | Mutualist-interference magnitude | Orientation gate and channel definition | Total pollination cost |
| \(\kappa\) | Direct joint-cost curvature | Direct cost-channel definition | Total energetic or construction cost |
| \(P\) | Exogenous pollinator-service context index | Operational scale and focal context | A universal multiplier of all mutualist effects |
| \(H\) | Exogenous antagonist-pressure context index | Operational scale and focal context | A universal multiplier of all antagonist effects |

**Note.** The oriented identity \(W_{AD}=\rho-\iota-\kappa\) is used only after the focal application establishes \(M_{AD}\le0\), \(G_{AD}\le0\), and \(C_{AD}\ge0\).

## Table 2. Mechanistic finite-sensitivity design and canonical sign regimes

| Quantity | Declared value |
|---|---|
| Attraction coordinates \(A\) | 0.2, 0.5, 0.8 |
| Defence coordinates \(D\) | 0.2, 0.5, 0.8 |
| Pollinator-service index \(P\) | 0.2, 0.5, 0.8 |
| Antagonist-pressure index \(H\) | 0.2, 0.5, 0.8 |
| Auxiliary reproductive-assurance moderator \(R\) | 0.0, 0.5 |
| Local cases | 162 |
| Biological parameter scenarios | 4 |
| Endpoint-normalized response-shape variants | 4 |
| Total mixed-partial evaluations | 2,592 |
| Complementary evaluations | 1,342 (51.8% unweighted finite-grid occupancy) |
| Substitutable evaluations | 1,250 (48.2% unweighted finite-grid occupancy) |
| Numerically neutral evaluations | 0 |
| Fixed case × scenario summaries | 648 |
| Unanimous across four response shapes | 480 |
| Mixed or sensitive across response shapes | 168 |
| Local cases unanimous across the deliberately heterogeneous full tested set | 0 of 162 |
| Absolute numerical zero tolerance | \(10^{-10}\) on the declared score scale |
| Minimum absolute mixed partial | \(1.7318900435991935\times10^{-6}\) |

**Note.** Percentages are unweighted occupancies of the declared finite design. They are not empirical probabilities, posterior probabilities, or estimates of prevalence in nature. \(R\) is an auxiliary background moderator in the implemented corollary, not a third focal trait.

## Part II — Pattern

## Table 3. Cross-study pattern scaffold: mechanism recurrence, conditionality, and identification gaps

| Evidence layer | Current independent study clusters / state | Main empirical Pattern | Inference boundary |
|---|---:|---|---|
| \(A\rightarrow\)pollination | 5 clusters | Attraction can increase pollinator use or pollinator-mediated reproduction; visitor identity and functional mode can change the realised return | Does not identify \(M_{AD}\) without the same focal \(D\) |
| \(A\rightarrow\)antagonism | 8 clusters | Floral signals are also tracked by antagonists across volatile, visual-bract, colour, and multidimensional colour/scent systems | Does not estimate antagonist-relief curvature by itself |
| \(D\rightarrow\)antagonism | 18 clusters | Flower-specific chemical and physically distinct barriers reduce antagonist entry, use, oviposition, or damage | Marginal defence efficacy is not \(G_{AD}\) unless linked to the marginal value of the same \(A\) |
| \(D\rightarrow\)pollination | 10 clusters | Pollinator effects include guarded nulls, interference, reward compensation, consumer specificity, and changes in legitimate-versus-robbing function | A marginal pollinator effect is not automatically \(M_{AD}\) |
| Same-system multi-route | 14 clusters | Guarded defence, shared tracking, attack-mode filtering, functional-mode routing, response dependence, and unresolved regimes recur | Same-system marginal routes are stronger linkage evidence but are not direct \(A\times D\) estimates |
| Context/sign switching | 17 clusters | Channels open, close, or change role across trait intensity, resource/exposure, consumer identity, response stage, population, attack geometry, and lifecycle | Counts are recurrence within the screened architecture, not prevalence |
| Context-only programs | 7 programs, excluded from route N | Environmental damage, pollination syndrome, reproductive-module defence, temporal ant exclusion, and lifecycle-linked selection add context without pretending to be clean marginal routes | Program count is not added to the 25 route-ledger clusters |
| Direct \(A\times D\) | 1 strict cluster | *Impatiens capensis*: two reproductive-component interactions are estimable but both CIs cross zero and point signs differ | No general direct sign is identified |
| Direct joint cost \(\kappa\) | 0 strict estimates after saturated registered search | Marginal costs, covariance, and ecological interference exist, but no strict simultaneous A+D intrinsic-cost estimate was found | \(\kappa\) is unidentified, not zero |

**Pattern-scaffold note.** The saturated architecture contains 56 source-adjudicated effect/directional records across 25 independent biological study clusters. Route-specific cluster counts overlap because the same study may contribute to several linked routes. Seven additional context programs and all study/case counts from secondary syntheses are excluded from route-ledger N. The expansion stopped after two consecutive targeted screening batches produced no new admissible Pattern class. This table maps recurrence onto Part I mechanism classes; it is not a grand meta-analysis and its counts are not prevalence estimates.

## Table 4. Quantitative meta-analytic patterns and admitted inference

| Module | Data structure and scale | Quantitative / published Pattern | Robustness / limitation | Admitted role in the Mechanism → Pattern paper |
|---|---|---|---|---|
| **Reproduced meta-analysis 1 — Leal et al. 2025 floral larceny** | Secondary reanalysis of deposited study-level group data; one aggregate effect per independent cluster and outcome stratum; log response ratio | Female reproductive success: \(-0.210\), 48 clusters; nectar standing crop: \(-0.483\), 28; legitimate visitation: \(-0.291\), 22 | Direction stable to declared within-cluster correlation, quarantined-row sensitivity, and leave-one-cluster-out; very high heterogeneity | Establishes recurrent realised antagonist costs across fitness, reward, and visitation |
| **Reproduced synthesis 2 — Sasidharan et al. 2023 FVOCs** | Deposited categorical synthesis reconstructed into 32 conservative study components | Physiological detection: florivore 84/103 vs pollinator 151/220; assembled risk difference \(+0.129\); positive in 32/32 leave-one-study-component-out refits | Only three components contain both physiological roles and all paired differences are zero; behavioral and source-version discrepancies retained | Establishes shared consumer responsiveness plus composition/context dependence without claiming a causal paired role effect |
| **Secondary context — Haas-Desmarais et al. 2026** | Published multilevel meta-analysis; 171 studies, 1,348 study cases | Overall herbivory-associated response is negative, with strong tissue, damage-type, response, and interaction dependence | Publisher supplement package independently retrieved and hashed; raw effect table not locally reconstructed; herbivory treatment is not focal \(D\) | Independent large-scale support for antagonist-pressure and tissue/context dependence |
| **Secondary context — Caruso et al. 2019** | Published selection synthesis; main analysis 755 directional gradients with SE from 36 articles | Selection depends on environmental agent, floral trait class, and pollinator guild | Dryad landing/API metadata and workbook identities verified; current file-byte access blocked; selection gradient is not \(W_{AD}\) | Independent selection-context support without relabelling other-biotic treatments as \(H\) |
| **Secondary cross-synthesis — Junker & Blüthgen 2010** | Published floral-scent synthesis; 18 publications, 425 observations | Visitor response differs with dependence on floral resources and remains different after study-level reduction | Visitor-dependence categories do not equal pollinator-versus-antagonist roles | Independent support for consumer-filtering and assay/context dependence |

**Boundary for all modules.** None estimates \(\rho\), \(\iota\), \(\kappa\), or \(W_{AD}\). Only the first two are reproduced quantitative modules in the current repository; the remaining three are explicitly secondary contextual/cross-synthesis modules. Together with Table 3, the Part II result is **recurrent mechanisms plus context-dependent balance**, not a universal sign of `W_AD`.
