# Access-routing Letter: estimand and novelty self-audit (2026-10-13)

**Status:** interpretive self-audit on draft PR #360; no new effect estimate, no promotion of exploratory analyses, and no journal submission.

## 1. What is independently supported

| Evidence layer | Target and data grain | Supported conclusion | Claim limit |
| --- | --- | --- | --- |
| Ecuador conditional routing (P1) | 259 plant species; 2,265 bird–plant–site units underneath | Tube–bill mismatch positively predicts observed robbery share (Spearman rho 0.503; species permutation p 0.0001) | Conditional route composition among recorded feeding interactions, not an absolute robbery frequency or causal trait effect |
| Within-bird-species diagnostic | 1,285 bird × plant dyads; 28 bird species | Within-species centered-rank rho 0.340 (permutation p 0.0001) | Individual birds were **not** followed across tactics |
| Ecuador opportunity-based rates (P2) | Bird × clean-camera waypoint opportunity edges; binary physiological-reach barrier | **Post-open 1.8× reach sensitivity:** separately fitted legitimate RR 0.154 (0.087–0.271); robbery RR 0.816 (0.358–1.860) | Strong estimated legitimate-rate reduction on its fitted support; robbery direction unresolved; not a prospective or causal decomposition of P1 |
| Independent Afrotropical insect network | 57 plant species | Tube length positively associated with robbing–thieving balance (rho 0.347; permutation p 0.0086) | Different behavioural denominator from Ecuador; multitrait tube-length partial test p 0.211 |
| Equal-network directional statistic | One rank association per network | rho_J 0.428; permutation p 0.0001 | **k = 2**; not evidence for the same route-loss mechanism or a population mean over ecological networks |

## 2. The shared-denominator identity is not the fitted comparison

For a *single* opportunity population \(\mathcal U\), if both \(\lambda_R^{\mathcal U}(x)\) and \(\lambda_L^{\mathcal U}(x)\) are route-specific expected counts or rates over the **same** opportunities, weights and exposure contrast, then

\[
p_R^{\mathcal U}(x) = \frac{\lambda_R^{\mathcal U}(x)}{\lambda_R^{\mathcal U}(x)+\lambda_L^{\mathcal U}(x)},
\qquad
\mathrm{logit}\,p_R^{\mathcal U}(x) = \log\lambda_R^{\mathcal U}(x)-\log\lambda_L^{\mathcal U}(x).
\]

This identity does **not** turn two separately fitted fixed-effect estimates on different retained supports into a decomposition of the observed plant-level P1 association. In addition, plant-averaged P1 route fractions and P2 bird × waypoint FE contrasts differ in their analysis grain, weighting, functional form and access definition.

The post-open support audit shows:

| Original hummingbird 1.8× M1 opportunity matrix and fitted supports | Opportunity edges |
| --- | ---: |
| Constructed locally available bird × waypoint opportunities | 19,903 |
| Robbery-positive-margin FE support | 3,371 |
| Legitimate-positive-margin FE support | 15,377 |
| Intersection of these two fitted supports | **2,900** |

Therefore the reported **5.31 (1.92–14.67)** is a *descriptive ratio of separately fitted RRs*. It is **not** a measured or model-identified within-bird replacement rate, nor a common-risk-set allocation of higher robbery prevalence. A robbery RR interval extending to 1.860 must **not** be presented as demonstrating unchanged or equivalent robbery rates.

The original frozen culmen-only participation analysis gave pooled RR 1.772 and legitimate RR 1.883, whereas the post-open reach-based sensitivity gave legitimate RR 0.154 at 1.8×. The sign reversal under barrier definition is indispensable context; it cannot be discarded in favor of the preferred physiological interpretation.

Primary supporting records:
- `empirical/route_retention_composition/ROUTE_RATE_ESTIMAND_COMMON_SUPPORT_AUDIT_V1.md` (analysis branch `analysis/route-retention-composition-v1`)
- `empirical/floral_defence_selectivity/PARTICIPATION_ROUTE_DECOMPOSITION_PREREG_V1.md`
- `empirical/floral_defence_selectivity/AUBERT_ROUTE_SPECIFIC_PARTICIPATION_POSTOPEN_CONTRACT_V1.md`
- `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`

## 3. Apply the paper's own literature-identification standard

The frozen formal evidence frame contains **33** eligible programs. A later **post-hoc** audit found only **7/33** with a verified, zero-inclusive common-denominator *study design* permitting the two route rates to be assessed. That finite-frame number is neither an estimate of literature prevalence nor a replication count.

For BITA's **own** Ecuador rate analysis:
- A locally restricted zero-inclusive *opportunity construction* exists: **yes**.
- Both route outcomes are counted from that constructed matrix: **yes**.
- Both fitted route-specific coefficients represent a shared **positive-margin FE support**: **no**.
- A single model identifies a causal or population-common substitution effect: **no**.

Do not conflate a common *input design* with a common *fitted estimand*, or imply that the empirical extension closes the strict cross-route identification problem under the same numerical standard that motivated the 7/33 design audit.

## 4. Defensible novelty and limits

**Defensible novelty:** a network-scale, source-audited comparison of a known conditional mismatch–robbery prevalence pattern with *opportunity-augmented route-specific rate sensitivities*, coupled to a separate within-bird-species association and directional recurrence in an independent insect network. It demonstrates why prevalence cannot be read as a stand-in for absolute route frequency, and provides an empirical case consistent with much stronger filtering of legitimate feeding than any detectable robbery-rate increase under a particular post-open reach definition.

**Not demonstrated:** a unique numerical cause of the P1 association, a directly estimated same-risk-set rate replacement, evidence that absolute robbery did not increase, tracking of individual tactic switching, an experimentally isolated flower-geometry effect, adaptation of floral barriers as defences, a universal effect beyond k=2, or the same route-loss mechanism in the insect network.

This is the substantive novelty ceiling of the present Letter. To exceed it would require **new evidence**—for example a prospectively defined common-population joint route-rate estimand that survives zero margins and sensitivity checks, or independent experimental manipulation of legitimate and bypass access—not stronger prose.

## 5. Manuscript and cover-letter guard

Write **“the post-open legitimate-rate model estimated a strong reduction while robbery-rate change was unresolved”** rather than **“the higher robbery prevalence was caused by legitimate-visit loss.”** Treat P1 versus P2 as **complementary but different estimands**, and the 5.31 as descriptive, throughout the title-facing argument, abstract, figure, Discussion and cover.

Do not merge the current draft PR solely because this document and wording pass regression tests: author-controlled disclosures, DOI provenance, archival publication and submission remain separately blocked.
