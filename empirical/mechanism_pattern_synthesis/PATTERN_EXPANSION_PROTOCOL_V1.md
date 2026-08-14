# Part II Pattern expansion protocol v1

## Purpose

Expand the empirical half of the Mechanism → Pattern paper without turning heterogeneous literature into an artificial universal effect size.

The expansion question is:

> Which mechanism-derived empirical patterns recur across independent systems, which contexts change their state, and where does direct identification remain sparse?

The target is **pattern generality**, not a target number of papers.

## Frozen theory boundary

Part I is unchanged:

```text
W_AD = M_AD - G_AD - C_AD
orientation gate
W_AD = rho - iota - kappa
```

No new theory parameter, focal trait, or biological mechanism may be introduced merely to accommodate new literature.

## Expansion layers

### Layer 1 — source-adjudicated mechanism recurrence

Re-open the fixed 258-work retrieval corpus pinned at branch commit:

```text
evidence/audit-all-258-study-architecture
7cf3122b46578e065ec619be0ed42a6c26a72a12
```

The fixed corpus contains 258 candidate works, 235 with archived abstracts and 238 with an OpenAlex OA route. These are discovery metadata only, not eligible biological effects.

Prioritize candidates that can add genuinely new cells to the current Pattern matrix:

1. `A -> antagonism`;
2. `D -> pollination`;
3. same-system multi-route evidence;
4. sign/state switching across trait intensity, resources, exposure, consumer identity, response definition, or compound identity;
5. shared-unit designs approaching direct `A x D` identification.

Do not spend screening effort first on already-saturated cells unless a study provides stronger shared-unit or quantitative evidence.

### Layer 2 — independent quantitative syntheses

Admit an external quantitative synthesis only if it answers a distinct theory-derived Pattern question.

Required fields:

```text
module_question
biological_axis
study_or_component_count
effect_scale
dependence_structure
heterogeneity_or_influence_state
context_moderators
admitted_inference
forbidden_inference
source_version
```

Current expansion candidates:

1. Haas-Desmarais et al. 2026 — antagonist-pressure / tissue × damage-type context module.
2. Caruso et al. 2019 — selection-level agent/trait/pollinator context module.
3. Additional cross-synthesis replication only if it contributes a distinct mechanism/context axis.

### Layer 3 — cross-module recurrence

After module-specific analysis, compare only **pattern classes**, not raw effect sizes across incompatible scales.

Candidate recurrent classes:

```text
negative antagonist cost
pollinator-response suppression
shared mutualist/antagonist tracking
consumer-role dependence
trait-intensity threshold
resource/exposure dependence
tissue/damage-type dependence
response-stage dependence
selection-agent dependence
pollinator-guild dependence
```

A class is strengthened when it recurs in independent study universes or independent quantitative syntheses.

## Expansion stopping rule

Do not stop at an arbitrary N.

Stop screening when both conditions are met:

1. two consecutive prioritized screening batches add no new mechanism × context × outcome class and do not materially change an existing class; and
2. no newly identified quantitative synthesis adds a distinct theory-derived Pattern axis.

A new paper that merely repeats an already well-supported cell may improve confidence but does not reset the stopping rule unless it changes the independence or quantitative strength of that cell.

## Current Pattern hypothesis under test

The existing manuscript conclusion is treated as a hypothesis to test, not as a fact to preserve:

> recurrent constituent mechanisms + context-dependent balance

Expansion may strengthen, narrow, or overturn this statement.

## Hard prohibitions

- Retrieval metadata flags are not biological evidence.
- Candidate-work counts are not field-wide prevalence.
- Herbivory treatment is not a defence phenotype `D`.
- Leaf or whole-plant defence is not silently relabelled as flower-specific `D`.
- A negative effect of herbivory on pollination is not `M_AD`.
- A negative effect of herbivory on reproduction is not `W_AD`.
- Cross-study module effects are not `rho`, `iota`, `kappa`, or `W_AD`.
- Same-system evidence is not direct `A x D` evidence.
- Incompatible outcomes are not pooled solely to increase sample size.

## Deliverables

1. prioritized 258-corpus rescreen ledger;
2. Haas-Desmarais 2026 source/design/readout audit;
3. Caruso 2019 source/design/readout audit;
4. expanded Pattern-module registry;
5. updated cross-module Pattern matrix;
6. manuscript/Figure 3 changes only after a new module passes its inference gate.
