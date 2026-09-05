# Cross-world criticality identification v1

## Core result

The question

> do SCH and BITA cross the same ecological critical point, or do the shared and differentiated worlds have different effective critical points?

has an identification condition before it has a biological answer.

If the two architecture worlds are observed only in disconnected experiments, their relative fitness offset is not automatically identified. Within-world contrasts can remain exactly unchanged while the cross-world critical point moves.

## Additive-offset argument

Suppose the architecture margin along an ecological control axis `e` is

```text
Phi(e) = W_D(e) - W_S(e).
```

If the differentiated world is known only up to an additive constant `c`, then

```text
W_D'(e) = W_D(e) + c
Phi'(e) = Phi(e) + c.
```

Every within-differentiated-world contrast is unchanged:

```text
W_D'(e2)-W_D'(e1)
= W_D(e2)-W_D(e1).
```

But the zero crossing generally moves:

```text
Phi(e_c)=0
```

need not imply

```text
Phi'(e_c)=0.
```

The regression test uses a simple margin from -1 to +1 over `e=0..2`: the critical point is `e=1`. Adding a constant +0.5 leaves all within-world differences unchanged but moves the crossing to `e=0.5`.

Therefore:

```text
within-world response shapes alone
!= identified cross-world critical point.
```

## What fixes the cross-world gauge

At least one valid bridge is required.

### Direct bridge

Randomize or otherwise causally compare shared-like and differentiated states within the same population/season/block using the same absolute reproductive-fitness endpoint.

Then

```text
W_D - W_S
```

is directly identified on the common scale.

### Independent offset bridge

If direct architecture randomization is impossible, independently estimate the between-world offset using a validated common-fitness comparator and an assay for the additional architecture/deployment burden.

This is where `K` becomes an identification parameter rather than merely a theoretical penalty.

## Why kappa does not fix the offset

The local BITA joint channel `kappa_delta` describes interaction-specific cost/benefit once the two axes already exist. It does not establish the absolute fitness offset between a shared architecture and a differentiated architecture.

Thus:

```text
kappa_delta
!= cross-world offset
!= K_arch.
```

## Same-world versus parallel-world interpretation

After the offset is fixed and a common ecological axis `e` is declared, estimate:

```text
e_c,S  from the SCH-side projected architecture margin
e_c,D  from the direct/bridged differentiated-world margin
Delta_e_c = e_c,D - e_c,S.
```

Then:

```text
Delta_e_c compatible with 0
-> one shared critical-context description is adequate

Delta_e_c persistently nonzero
-> effective parallel-world criticality.
```

A genuine nonzero `Delta_e_c` can arise because the architecture change itself modifies quantities that the simple nested model treats as fixed, for example:

- function-specific objectives move when the second axis appears;
- developmental or regulatory costs depend on ecological context;
- residual cross-loading changes functional weights;
- the differentiated state creates a new ecological interaction;
- the shared state is not actually nested inside the differentiated state.

These are biological departures worth explaining, not nuisance discrepancies to force to zero.

## Current status

```text
common theory critical surface:              IDENTIFIED
same-vs-parallel zero-crossing comparator:   IMPLEMENTED
SCH fitness-scale conflict-budget analyzer:  IMPLEMENTED
BITA K/scale projection:                     IMPLEMENTED
cross-world offset in biological data:       NOT YET IDENTIFIED
natural numeric Delta_e_c:                   NOT YET IDENTIFIED.
```

The next decisive empirical design must therefore contain a cross-world bridge, not merely two separately well-estimated within-world response surfaces.

## Implementation

- `trait_architecture/cross_world_identification.py`
- `tests/test_cross_world_identification.py`
- `scripts/compare_sch_bita_critical_contexts.py`
