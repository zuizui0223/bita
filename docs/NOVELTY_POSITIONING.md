# Novelty and positioning boundary

## Prior art that must be acknowledged explicitly

The manuscript must not present the biological coupling of pollination, herbivory, floral attraction, and defence as a new idea. It also must not present cross-trait fitness curvature itself as a new mathematical object.

At minimum, the positioning must acknowledge four established lines of work:

1. **Cross-trait fitness curvature and correlational selection are established multivariate-selection concepts.** Lande and Arnold (1983) provided the classical framework for measuring selection on correlated characters, and later fitness-surface work developed the interpretation and visualization of quadratic and cross-trait selection. Therefore using a local cross derivative or interaction term to describe how fitness depends on a trait combination is not itself a novelty claim.
2. **Defence can carry an ecological cost through pollination.** Strauss et al. (1999) explicitly examined ecological costs of herbivore resistance in the currency of pollination and showed that more resistant *Brassica rapa* lines differed in floral traits and pollinator foraging use. This directly predates any claim that defence-associated traits can impose collateral pollination costs.
3. **Mutualists and antagonists can have nonadditive fitness effects relevant to correlated evolution.** Herrera et al. (2002) experimentally manipulated pollinator and herbivore effects in a factorial field design and found geographically consistent nonadditivity in fitness consequences, proposing a pathway for correlated evolution of mutualism- and antagonism-related traits. This directly predates any claim that combined mutualist and antagonist effects can create nonadditive selection or favour trait combinations.
4. **Ecological parameters can shift the balance between mutualism and antagonism in explicit models.** Revilla and Encinas-Viso (2014) developed a stage-structured pollination–herbivory model with qualitative transitions between mutualism- and antagonism-dominated dynamics. Context dependence and ecological regime transitions are therefore not novel in themselves.

References:

- Lande, R., & Arnold, S. J. (1983). The measurement of selection on correlated characters. *Evolution* 37:1210–1226.
- Strauss, S. Y., Siemens, D. H., Decher, M. B., & Mitchell-Olds, T. (1999). Ecological costs of plant resistance to herbivores in the currency of pollination. *Evolution* 53:1105–1113. doi:10.1111/j.1558-5646.1999.tb04525.x.
- Herrera, C. M., Medrano, M., Rey, P. J., Sánchez-Lafuente, A. M., García, M. B., Guitián, J., & Manzaneda, A. J. (2002). Interaction of pollinators and herbivores on plant fitness suggests a pathway for correlated evolution of mutualism- and antagonism-related traits. *PNAS* 99:16823–16828. doi:10.1073/pnas.252362799.
- Revilla, T. A., & Encinas-Viso, F. (2014). Dynamical transitions in a pollination–herbivory interaction. arXiv:1404.4804.

## What is not claimed as novel

The manuscript does not claim novelty for any of the following:

- multivariate fitness surfaces, quadratic selection, or cross-trait fitness curvature;
- pollinators and antagonists jointly shaping plant fitness or floral evolution;
- attractive floral traits exposing plants to antagonists;
- defence or resistance carrying collateral costs through pollinator responses;
- nonadditive fitness effects of mutualists and antagonists;
- correlated evolution being favoured by such nonadditivity;
- ecological context changing the balance between mutualism and antagonism;
- an algebraic decomposition of a mixed partial by itself.

In particular, the identity

```text
W_AD = M_AD - G_AD - C_AD
```

is algebra, not a novelty claim, and `W_AD` is one local cross-curvature quantity within the broader family of multivariate fitness-surface descriptions.

## The narrower contribution being claimed

The defensible contribution is a **mechanistically oriented focal-trait diagnostic** that applies a local cross-curvature quantity to a declared pair of floral traits and separates three distinct sources of that curvature:

```text
local A x D marginal-fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

For one declared attraction trait `A` and one declared flower-specific barrier/defence trait `D`, the framework:

1. imposes an explicit **orientation gate** before converting signed mixed curvatures into non-negative mechanism magnitudes;
2. keeps the ecological pollination cost of defence separate from direct allocation or construction cost;
3. expresses the local sign boundary as a balance among antagonist relief, mutualist interference, and direct joint cost;
4. distinguishes the diagnostic sign condition from the additional assumptions needed for environmental comparative statics;
5. writes those additional conditions as explicit local derivative inequalities rather than treating “more antagonists” or “more pollinators” as universally directional;
6. allows nonlinear regime dependence, under which a one-dimensional regime contrast may have no crossing, one crossing, or multiple sign switches;
7. keeps the local curvature result separate from claims about covariance, genetic correlation, optima, or evolutionary trajectories.

The strongest defensible statement is therefore **not** that cross-trait selection, nonadditivity, trade-offs, correlated evolution, or ecological context are newly discovered. It is that the manuscript provides a compact floral mutualist–antagonist diagnostic that separates three mechanistic contributions, states when the non-negative orientation is valid, and makes the extra derivative conditions for regime predictions explicit.

## Novelty status: deliberately provisional

This is a formulation and inference-architecture claim, not a claim of discovering a new biological phenomenon or a new class of fitness curvature.

The current citation review establishes important nearby prior art and materially narrows the novelty claim. It does **not** yet prove that no earlier paper has written an algebraically equivalent focal-trait criterion with the same three-way mechanism separation, orientation gate, and regime-derivative conditions. Until a targeted search of theoretical, correlational-selection, and plant mutualist–antagonist literature is complete, the manuscript should use wording such as:

> We develop a mechanistically oriented local diagnostic framework...

rather than:

> We provide the first general theory...

or:

> We derive a novel universal criterion...

## What is deliberately narrower than a full evolutionary model

`W_AD` is a local mixed partial of a declared fitness or fitness-score surface. It describes how the marginal fitness effect of one focal trait changes with the other.

If `W` is defined as relative fitness on standardized trait coordinates, an empirically estimated cross-trait quadratic term can be discussed in the language of correlational selection. The present supplement does not automatically assume that scaling. It therefore uses the more general phrase **local marginal-fitness interaction** unless a concrete empirical application supplies the required fitness and trait definitions.

`W_AD` does not by itself predict:

- population-level trait covariance;
- genetic correlation;
- an evolved environmental cline;
- an evolutionary trajectory;
- a stable equilibrium or global optimum.

Those would require additional assumptions about fitness scaling, constraints, genetic architecture, and dynamics. Herrera et al. (2002) is especially important here: its discussion of correlated evolution should not be used as permission to infer trait covariance directly from the present mixed partial.

## Trait-definition and orientation boundary

The theory is not a model of an omnibus `attraction` index crossed with an omnibus `defence` index. Every application must choose one focal `A`–`D` pair and declare its measurement scale.

`D` is defined by a flower-specific antagonist-reduction role. A pollinator cost is a possible effect of that same focal trait. A trait that merely obstructs pollinators is not sufficient to instantiate the complete defence mechanism.

The biological labels also do not determine the mixed-curvature signs. A negative `D -> pollinator use` response does not by itself identify `M_AD < 0`, and a protective `D -> antagonist damage` response does not by itself identify `G_AD < 0`. The focal interaction with the marginal effect of `A` must be established.

This distinction is important for empirical synthesis: records from different traits or taxa can establish that a pathway occurs, but they do not jointly estimate one system-specific mixed partial.

## Parameterisation boundary

Mixed partials are coordinate-dependent quantities. Positive affine rescaling preserves the sign, but arbitrary nonlinear trait transformations can alter a cross-partial away from special cases. The manuscript therefore treats the sign as a property of a declared biological parameterisation, not as a transformation-free universal label.

## Empirical role of the literature layer

The current literature layer is a preliminary mechanism-plausibility check. All active direction records are coded from Crossref-deposited abstracts rather than promoted full-text effect extractions.

One predeclared three-cluster manipulation stratum for chemical barriers and pollinator preference/foraging is uniformly negative at the abstract-coding level. A separate visitation-rate stratum contains one mixed record. This is restricted abstract-level directional consistency with a collateral pollinator-cost route, not a full-text meta-analysis and not evidence for the focal `M_AD` curvature by itself.

The evidence does not estimate the full mutualist-interference curvature, antagonist-relief curvature, direct joint cost, complete mixed partial, or environmental derivative of the mixed partial. The current quantitative extraction table is not sufficient for pooled calibration.

Strauss et al. (1999) also means that the existence of a defence-associated pollination cost should be treated as biological precedent, not as the manuscript's novelty. The literature layer supports plausibility and scope; it is not the central conceptual contribution.

## Reviewer-facing positioning

A defensible abstract-level claim is:

> Building on multivariate selection theory and evidence that pollination and antagonism can interact nonadditively and that defence can carry pollination costs, we develop a mechanistically oriented focal-trait diagnostic that separates antagonist relief, mutualist interference, and direct joint cost, states the sign conditions required for that orientation, and identifies the additional regime-scaling conditions required for ecological change to shift the local marginal-fitness interaction toward complementarity or substitutability.

Avoid stronger formulations such as:

- “We introduce a new kind of cross-trait fitness interaction.”
- “We are the first to show that pollinators and herbivores jointly shape plant fitness.”
- “We discover that defence can trade off with pollination.”
- “We show for the first time that mutualist and antagonist effects are nonadditive.”
- “We derive a completely general theorem for all attraction–defence systems.”
- “More antagonists always favour attraction–defence complementarity.”
- “The mixed partial predicts positive or negative trait correlations.”
- “The literature data empirically validate the full regime map.”
- “All floral defence and access-limitation traits are measurements of one common `D` axis.”
