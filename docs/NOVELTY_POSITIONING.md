# Novelty and positioning boundary

## Prior art that must be acknowledged explicitly

The manuscript must not present the biological coupling of pollination, herbivory, floral attraction, and defence as a new idea.

At minimum, the positioning must acknowledge three established lines of work:

1. **Defence can carry an ecological cost through pollination.** Strauss et al. (1999) explicitly examined ecological costs of herbivore resistance in the currency of pollination and showed that more resistant *Brassica rapa* lines differed in floral traits and pollinator foraging use. This directly predates any claim that defence-associated traits can impose collateral pollination costs.
2. **Mutualists and antagonists can have nonadditive fitness effects relevant to correlated evolution.** Herrera et al. (2002) experimentally manipulated pollinator and herbivore effects in a factorial field design and found geographically consistent nonadditivity in fitness consequences, proposing a pathway for correlated evolution of mutualism- and antagonism-related traits. This directly predates any claim that combined mutualist and antagonist effects can create nonadditive selection or favour trait combinations.
3. **Ecological parameters can shift the balance between mutualism and antagonism in explicit models.** Revilla and Encinas-Viso (2014) developed a stage-structured pollination–herbivory model with qualitative transitions between mutualism- and antagonism-dominated dynamics. Context dependence and ecological regime transitions are therefore not novel in themselves.

References:

- Strauss, S. Y., Siemens, D. H., Decher, M. B., & Mitchell-Olds, T. (1999). Ecological costs of plant resistance to herbivores in the currency of pollination. *Evolution* 53:1105–1113. doi:10.1111/j.1558-5646.1999.tb04525.x.
- Herrera, C. M., Medrano, M., Rey, P. J., Sánchez-Lafuente, A. M., García, M. B., Guitián, J., & Manzaneda, A. J. (2002). Interaction of pollinators and herbivores on plant fitness suggests a pathway for correlated evolution of mutualism- and antagonism-related traits. *PNAS* 99:16823–16828. doi:10.1073/pnas.252362799.
- Revilla, T. A., & Encinas-Viso, F. (2014). Dynamical transitions in a pollination–herbivory interaction. arXiv:1404.4804.

## What is not claimed as novel

The manuscript does not claim novelty for any of the following:

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

is algebra, not a novelty claim.

## The narrower contribution being claimed

The defensible contribution is a **focal-trait local comparative-static diagnostic** that organizes a declared pair of continuous floral traits around three distinct local contributions:

```text
local A x D marginal-fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

For one declared attraction trait `A` and one declared flower-specific barrier/defence trait `D`, the framework:

1. keeps the ecological pollination cost of defence separate from direct allocation or construction cost;
2. expresses the local sign boundary as a balance among antagonist relief, mutualist interference, and direct joint cost;
3. distinguishes the diagnostic sign condition from the additional assumptions needed for environmental comparative statics;
4. writes those additional conditions as explicit local derivative inequalities rather than treating “more antagonists” or “more pollinators” as universally directional;
5. allows nonlinear regime dependence, under which a one-dimensional regime contrast may have no crossing, one crossing, or multiple sign switches;
6. keeps the local curvature result separate from claims about covariance, genetic correlation, optima, or evolutionary trajectories.

The strongest defensible statement is therefore **not** that nonadditivity, trade-offs, correlated evolution, or ecological context are newly discovered. It is that the manuscript provides a compact focal-pair diagnostic that separates three mechanisms often conflated in verbal arguments and makes the extra derivative conditions for regime predictions explicit.

## Novelty status: deliberately provisional

This is a formulation and inference-architecture claim, not a claim of discovering a new biological phenomenon.

The current citation review establishes important nearby prior art and materially narrows the novelty claim. It does **not** yet prove that no earlier paper has written an algebraically equivalent focal-trait criterion with the same three-way mechanism separation and regime-derivative conditions. Until a targeted search of theoretical and correlational-selection literature is complete, the manuscript should use wording such as:

> We develop a local diagnostic framework...

rather than:

> We provide the first general theory...

or:

> We derive a novel universal criterion...

## What is deliberately narrower than a full evolutionary model

`W_AD` is a local mixed partial of a declared fitness or fitness-score surface. It describes how the marginal fitness effect of one focal trait changes with the other.

It does not by itself predict:

- population-level trait covariance;
- genetic correlation;
- an evolved environmental cline;
- an evolutionary trajectory;
- a stable equilibrium or global optimum.

Those would require additional assumptions about fitness scaling, constraints, genetic architecture, and dynamics. Herrera et al. (2002) is especially important here: its discussion of correlated evolution should not be used as permission to infer trait covariance directly from the present mixed partial.

## Trait-definition boundary

The theory is not a model of an omnibus `attraction` index crossed with an omnibus `defence` index. Every application must choose one focal `A`–`D` pair and declare its measurement scale.

`D` is defined by a flower-specific antagonist-reduction role. A pollinator cost is a possible effect of that same focal trait. A trait that merely obstructs pollinators is not sufficient to instantiate the complete defence mechanism.

This distinction is important for empirical synthesis: records from different traits or taxa can establish that a pathway is biologically possible, but they do not jointly estimate one system-specific mixed partial.

## Parameterisation boundary

Mixed partials are coordinate-dependent quantities. Positive affine rescaling preserves the sign, but arbitrary nonlinear trait transformations can alter a cross-partial away from special cases. The manuscript therefore treats the sign as a property of a declared biological parameterisation, not as a transformation-free universal label.

## Empirical role of the literature layer

The current literature layer is a mechanism-plausibility check. Source-adjudicated route records show that flower-associated defence/barrier traits can reduce pollinator use in some systems.

That evidence does not estimate the full mutualist-interference curvature, antagonist-relief curvature, direct joint cost, complete mixed partial, or environmental derivative of the mixed partial. The current quantitative extraction table is not sufficient for pooled calibration.

Strauss et al. (1999) also means that the existence of a defence-associated pollination cost should be treated as biological precedent, not as the manuscript's novelty. The literature layer supports plausibility and scope; it is not the central conceptual contribution.

## Reviewer-facing positioning

A defensible abstract-level claim is:

> Building on evidence that pollination and antagonism can interact nonadditively and that defence can carry pollination costs, we develop a focal-trait local diagnostic that separates antagonist relief, mutualist interference, and direct joint cost, and we state the additional regime-scaling conditions required for ecological change to shift the local marginal-fitness interaction toward complementarity or substitutability.

Avoid stronger formulations such as:

- “We are the first to show that pollinators and herbivores jointly shape plant fitness.”
- “We discover that defence can trade off with pollination.”
- “We show for the first time that mutualist and antagonist effects are nonadditive.”
- “We derive a completely general theorem for all attraction–defence systems.”
- “More antagonists always favour attraction–defence complementarity.”
- “The mixed partial predicts positive or negative trait correlations.”
- “The literature data empirically validate the full regime map.”
- “All floral defence and access-limitation traits are measurements of one common `D` axis.”
