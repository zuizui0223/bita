# Tables for integrated Theoretical Ecology submission

## Table 1. Definitions, required declarations, and inference boundaries

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

## Table 2. Declared endpoint-normalized finite sensitivity design and canonical results

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

## Table 3. Source-adjudicated mechanism-pattern evidence architecture

| Evidence layer | Current independent study clusters / state | Main empirical information | Inference boundary |
|---|---:|---|---|
| \(A\rightarrow\)pollination | 4 clusters; 2 quantitative | Attraction can increase pollinator use or pollinator-mediated reproduction, with consumer-specific responses in some systems | Does not identify \(M_{AD}\) without the same focal \(D\) |
| \(A\rightarrow\)antagonism | 5 clusters; 3 quantitative | Floral signals can also be tracked by antagonists; shared and antagonist-biased tracking both occur | Does not estimate antagonist-relief curvature by itself |
| \(D\rightarrow\)antagonism | 10 clusters; 3 quantitative | Flower-specific chemical and physical mechanisms can reduce antagonist entry, use, oviposition, or damage | Marginal defence efficacy is not \(G_{AD}\) unless linked to the marginal value of the same \(A\) |
| \(D\rightarrow\)pollination | 7 clusters; 3 quantitative | Pollinator cost can be absent, negative, reward-compensated, consumer-specific, duration-dependent, or response-construct dependent | A negative marginal pollinator effect is not automatically \(M_{AD}<0\) |
| Same-system multi-route | 10 clusters | Guarded, guarded-window, interference, context-switching, shared-tracking, antagonist-biased, response-construct, and unresolved regimes recur | Same-system marginal routes are stronger linkage evidence but are not direct \(A\times D\) estimates |
| Context/sign switching | 11 clusters | Five theory-facing classes: trait intensity/expression; resource/exposure; consumer identity/role; response stage/scale; compound identity/mechanism partition | Counts are recurrence within the screened architecture, not prevalence |
| Direct \(A\times D\) | 1 strict cluster | *Impatiens capensis*: two reproductive-component interactions are estimable but both CIs cross zero and point signs differ | No general direct sign is identified |
| Direct joint cost \(\kappa\) | 0 strict estimates after saturated registered search | Marginal costs, covariance, and ecological interference exist, but no strict simultaneous A+D intrinsic-cost estimate was found | \(\kappa\) is unidentified, not zero |

**Note.** The mechanism-coverage audit contains 38 source-adjudicated effect/directional records across 14 independent biological study clusters. Route-specific cluster counts overlap because the same study may contribute to several linked routes. They must not be summed as independent studies.

## Table 4. Quantitative synthesis modules and admitted inference

| Module | Data structure and scale | Canonical quantitative result | Robustness / limitation | Admitted role in the integrated paper |
|---|---|---|---|---|
| Leal et al. 2025 floral larceny | Secondary reanalysis of deposited study-level group data; one aggregate effect per independent cluster and outcome stratum; log response ratio | Female reproductive success: \(-0.210\), 48 clusters; nectar standing crop: \(-0.483\), 28; legitimate visitation: \(-0.291\), 22 | Direction stable to declared within-cluster correlation, quarantined-row sensitivity, and leave-one-cluster-out; very high heterogeneity; Egger-type asymmetry interpreted cautiously for LRR | Shows that realised floral-antagonist pressure can impose substantial reward, visitation, and female-fitness costs and that \(H\) and pollinator use need not be empirically separable |
| Sasidharan et al. 2023 FVOCs | Deposited categorical synthesis reconstructed into 32 conservative study components | Current-deposit physiological detection: florivore 84/103 vs pollinator 151/220; assembled risk difference \(+0.129\); positive in 32/32 leave-one-study-component-out refits | Only three study components contain physiological data for both roles and all paired differences are zero; six repeated behavioral units switch between attraction and no response; printed/current-deposit discrepancies retained | Shows shared pollinator/florivore tracking and cross-study context dependence of floral volatile responses without claiming a causal within-study role contrast |

**Boundary for both modules.** Neither module estimates \(\rho\), \(\iota\), \(\kappa\), or \(W_{AD}\). The Leal module is pinned to immutable repository commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`; the Sasidharan module uses the 32-component citation topology as the canonical dependence structure.
