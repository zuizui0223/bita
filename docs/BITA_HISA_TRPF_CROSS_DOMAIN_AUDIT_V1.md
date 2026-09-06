# BITA HisA/TrpF cross-domain differentiation audit v1

## Question

Can real-time enzyme evolution provide a non-floral experimental anchor for BITA's general claim that functions initially carried by one multifunctional unit can become distributed across differentiated copies?

## Primary experiment

Näsvall et al. 2012, Science, DOI:

```text
10.1126/science.1226521
```

used a `Salmonella enterica` strain lacking `trpF` and a HisA-derived allele with both ancestral HisA and weak TrpF activity. Under continuous selection for both functions:

```text
shared bifunctional allele
-> amplification
-> mutations in different copies
-> HisA specialists / TrpF specialists / generalists
-> improved growth.
```

The experiment was completed in fewer than 3000 generations and directly observed functionally distinct copies emerge in real time.

A structural follow-up on the evolved `(beta-alpha)8`-barrel enzymes linked specialization to changes in protein structure/conformational behavior and catalytic function.

## BITA interpretation

This is a strong **cross-domain experimental functional-differentiation anchor**:

```text
ancestral/shared multifunctionality is observed;
additional copies create extra functional degrees of freedom;
different copies can specialize on different functions;
growth improves under the selected environment.
```

It is therefore much closer to BITA's architecture logic than a static comparative example.

## Boundary evidence from 2026

Näsvall & Abdalaal 2026, G3, DOI:

```text
10.1093/g3journal/jkag167
```

showed that `Delta trpF` rescue can also evolve through bifunctional mutations in `hisA` or `trpA` without duplication/divergence. Duplication of the target gene appeared in only one population and showed no functional divergence.

This is valuable BITA boundary evidence: extra dimensions / duplicated copies are not the only adaptive solution and should not be assumed to win whenever multifunctional demand exists.

## Duplication cost context

Adler et al. 2014, Molecular Biology and Evolution, DOI:

```text
10.1093/molbev/msu111
```

measured substantial fitness costs and instability of defined amplifications. This supports the biological plausibility of a nonzero architecture-cost term, but it is **not** a measurement of BITA `K` for the 2012 HisA/TrpF lineages.

## What is identified

Current cross-domain evidence strongly supports:

```text
functional differentiation across added gene copies can evolve experimentally;
specialist and generalist outcomes can coexist among trajectories;
functional divergence can be linked to structural/catalytic changes;
extra-copy costs are biologically real in related bacterial systems.
```

## What is not identified

The published HisA/TrpF system does not directly supply BITA's registered empirical quantities:

```text
SCH-derived z_reference
R_state = |x0*-z_ref|-|x1*-z_ref|
s on the BITA trait-coordinate definition
K for the same HisA/TrpF architecture on the same fitness scale
Delta_arch = R-K from an independently decomposed design.
```

The gene copies/sequence variants also represent a high-dimensional genotype space rather than the exact two-coordinate `x x y` manipulation used in the focal floral design.

Therefore the correct role is:

```text
G2_CROSS_DOMAIN_EXPERIMENTAL_DIFFERENTIATION_ANCHOR
NOT_A_PARAMETERIZED_BITA_THRESHOLD_TEST
```

## Stronger future route

A BITA-style microbial experiment could preregister a shared multifunctional starting genotype, construct a matched duplicated/separated architecture, quantify function-specific loading of the copies, measure the release of the original multifunctional constraint, and independently manipulate/measure duplication cost.

## Claim ceiling

Appropriate:

> HisA/TrpF real-time evolution demonstrates that additional genetic copies can permit experimentally observed functional specialization from a multifunctional ancestor, while other experiments show that bifunctional solutions can also persist.

Not appropriate:

> The published HisA/TrpF experiments estimate BITA `s`, `K`, `R_state`, or the BITA critical surface.
