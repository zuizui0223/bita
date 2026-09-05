# Critical-definition concordance v1

## Question

When different operational definitions are used to locate a transition, do they recover the same critical region or definition-specific parallel regions?

This is distinct from the stronger SCH/BITA cross-world question. Here the contexts are the same biological populations and the definitions are different measurements of transition on that common context ordering.

## Registered categories

For each definition, first convert its natural threshold to a signed margin with zero meaning "at the definition-specific boundary". Examples are:

```text
selection gradient beta             threshold 0
selection differential S            threshold 0
female-gain exponent b              threshold 1, so margin = b-1
architecture margin Phi             threshold 0
state-specific release R_state      threshold 0.
```

For an ordered set of contexts, recover a unique exact-zero context or adjacent sign-change bracket. Multiple crossings fail closed.

The cross-definition classification is:

```text
SAME_COARSE_CRITICAL_BRACKET
  all definitions cross in the same exact context / adjacent pair

OVERLAPPING_CRITICAL_BRACKETS
  non-identical brackets share at least one ordered context

PARALLEL_DEFINITION_BRACKETS
  identified brackets are separated on the context ordering

SAME_NUMERIC_CRITICAL_CONTEXT_WITHIN_TOLERANCE
  explicit common scalar context values yield interpolated zero crossings
  whose spread is inside a prospectively declared tolerance

PARALLEL_NUMERIC_CRITICAL_CONTEXTS
  explicit numeric crossings are separated beyond that tolerance.
```

Ordered labels alone never justify a numeric critical point.

Implementation:

```text
trait_architecture/critical_definition_concordance.py
```

## Peucedanum worked reality check

Kudo & Shibata (2025) provide five plots along a phenology / seed-predation mosaic:

```text
HA -> HL -> HC -> KD -> HD.
```

Three published definitions independently change regime between HL and HC.

### Definition 1 — direct selection gradient on perfect-flower production

For final fruit-set rate, published beta values are:

```text
HA -0.035
HL -0.029
HC +0.034
KD +0.008
HD +0.026.
```

### Definition 2 — selection differential

Published S values are:

```text
HA -0.027
HL -0.051
HC +0.036
KD +0.021
HD +0.024.
```

### Definition 3 — female-gain shape

The exponential female-gain exponents are:

```text
HA 0.63
HL 0.45
HC 1.15
KD 1.26
HD 1.55.
```

Using `b-1` as the signed margin, this definition also crosses zero between HL and HC.

The registered readout is therefore:

```text
SAME_COARSE_CRITICAL_BRACKET
common bracket = HL--HC.
```

This is stronger than saying that one selected statistic changes sign: a direct multivariate gradient, a univariate selection differential and the shape of the female gain curve all place their coarse boundary in the same region.

It is still not proof that they have one identical numeric critical point.

## Conditional predator-egg proxy sensitivity

The same paper reports mean predator eggs per umbel:

```text
HL = 3.09
HC = 1.64.
```

Treating this **only as an observational antagonist-pressure proxy** and imposing a local linear interpolation between the two plots gives definition-specific point crossings:

```text
final-fruit beta       ~2.423 eggs/umbel
final-fruit S          ~2.240 eggs/umbel
female-gain b-1        ~1.951 eggs/umbel.
```

Thus the definitions do not yield numerically identical point estimates under this extra interpolation model.

The registered sensitivity analysis then samples the published coefficient uncertainties under independent normal approximations, retains draws in which the HL and HC signs actually bracket zero, and compares the conditional 95% intervals. This does **not** propagate uncertainty in the egg-load axis itself.

Implementation:

```text
scripts/analyze_peucedanum_antagonist_proxy_criticality.py
empirical/identification_design/PEUCEDANUM_ANTAGONIST_PROXY_CRITICALITY_INPUT_V1.json
```

The correct interpretation is conditional:

```text
same coarse critical region
+
definition-specific proxy point estimates
+
ask whether their uncertainty intervals retain a common intersection.
```

If they do, a single latent numeric critical context remains compatible with the available data. If they do not, the definitions support separated proxy-critical contexts, but that still does not by itself establish separate SCH/BITA architecture worlds.

## Relation to same-world versus parallel-world criticality

There are now three increasingly strong questions:

```text
Q1  Coarse definition concordance
    Do different definitions cross in the same ordered context bracket?

Q2  Numeric definition concordance
    On one explicit scalar context axis, are their numeric crossings compatible?

Q3  Cross-world architecture concordance
    After fixing the SCH/BITA fitness offset and common scale, do the independently
    estimated shared-world and differentiated-world margins cross at the same e?
```

Peucedanum currently reaches Q1 positively and supplies a conditional sensitivity analysis for Q2. It does not reach Q3.

Pedicularis remains the registered same-species route for Q3 because the repository separates the SCH antagonist intervention from the BITA water-defence axis and requires a common-fitness bridge.

## Claim ceiling

Do not infer from the Peucedanum concordance that:

- predator eggs per umbel are the theoretical BITA functional weight `b`;
- the local-linear interpolation is a mechanistic law;
- coefficient-only uncertainty is the full uncertainty on the critical context;
- the common SCH/BITA architecture boundary `Phi=0` has been observed;
- historical modularization occurred at the HL--HC transition.

The strongest current statement is that **multiple independent operational definitions locate one concordant observational transition region, while the exact causal architecture critical point remains unidentified**.
