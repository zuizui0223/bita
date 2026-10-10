# Route retention versus composition — final frozen-array rerun

Status: **GITHUB ACTIONS COMPLETED; LEGITIMATE M2 CONFIRMED; ROBBING M2 NUMERICALLY NONCONVERGED**
Readout date: 2026-10-10
Branch: `analysis/route-retention-composition-v1`
Protocol: `ROUTE_RETENTION_COMPOSITION_DIAGNOSTIC_FREEZE_V1.md`

## Verified execution

- GitHub workflow run [37785895036](https://github.com/zuizui0223/bita/actions/runs/37785895036)
- Head commit: `954378283f075d5240eaf602cdbb047475a536ca`
- Point audit job: **success**, including synthetic classification tests, source-file checksum validation, and exact point-estimate reproduction.
- Full plant-cluster sensitivity job: **success**, including producing its machine-readable JSON artifact.
- Workflow artifact: `route-retention-composition-full`, ID `11556305678`.
- Frozen data: original, anonymously relabelled `BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4` from artifact `11293379572`. No re-download of observations from Zenodo and no shift of thresholds.

Inputs verified in the output receipt:
```text
aubert_ephi_pair_site_analysis.csv
    SHA256 = 94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa
aubert_ephi_participation_opportunities.csv
    SHA256 = 685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f
```

Input integrity:
```text
hummingbird opportunity edges  19,903
bird species                         49
plant species                       288
camera waypoints                  4,933
access / moderate / severe     14,770 / 1,847 / 3,286
route count reconstruction mismatches   0
all frozen support checks             PASS
```

## Route-specific results

Two Poisson models were fit without changing their formulas or mismatches:

- M1: bird species FE + camera waypoint FE.
- M2: bird species × site FE + camera waypoint FE.

| Route | Contrast | M1 rate ratio | M2 rate ratio |
|---|---|---:|---:|
| legitimate | moderate / accessible | 0.314927 | 0.307043 |
| legitimate | severe / accessible | 0.053300 | 0.048977 |
| legitimate | severe / moderate | 0.169247 | 0.159511 |
| robbery | moderate / accessible | 0.746015 | NOT CONVERGED |
| robbery | severe / accessible | 1.217321 | NOT CONVERGED |
| robbery | severe / moderate | 1.631765 | NOT CONVERGED |

### Legitimate M2: fully reproduced 288-plant jackknife

| Contrast | RR | 95% plant-jackknife CI | Successful leave-one |
|---|---:|---:|---:|
| moderate / accessible | 0.3070430 | 0.196014–0.480963 | 288/288 |
| severe / accessible | **0.0489769** | **0.026546–0.090360** | **288/288** |
| severe / moderate | 0.1595114 | 0.091456–0.278209 | 288/288 |

Every plant deletion retained a negative logged rate contrast.

These machine-generated values **agree** with the previous independent vectorized
implementation archived in `LEGITIMATE_M2_JACKKNIFE_INDEPENDENT_CROSSCHECK_V1.md`.
Thus the GitHub original script and independent numerical cross-check both reproduce
the same estimates and intervals.

### Robbery M2: cannot be promoted as a measured rate ratio

The robbery M2 three-state IPF terminated after the frozen 10,000 iterations
without meeting the convergence criterion:
```text
FIT_ERROR: three-state IPF failed to converge:
max margin relative error = 0.00008445273606494386
jackknife: NOT_RUN_M2_NOT_FIT
```

The top-level runner's machine decision is
`M2_NOT_IDENTIFIABLE`. **This is a pipeline classification triggered by
nonconvergence**, not proof of structural statistical nonidentifiability.
Slow numerical convergence, weak within-stratum robbery information and
quasi-separation are possible explanations. The specific mathematical cause
has **not** been established.

Do not silently substitute a relaxed tolerance, a reduced fixed-effect model, or
the numerically near-constant unfinished iterates as a new preregistered result.

## Sorting-only descriptive null: survives leave-one checks, not causal

The simpler constant bird×site mean-count expectation yields:

| State | legitimate O/E | robbery O/E |
|---|---:|---:|
| accessible | 1.22134 | 0.69631 |
| moderate | 0.89490 | 1.06921 |
| severe | 0.26268 | 1.58707 |

This discrepancy survives leave-one-plant, bird and site descriptive checks
recorded in `SORTING_LEAVE_CLUSTER_AND_M2_CONVERGENCE_DIAGNOSTIC_V1.md`.
The simple O/E expectation does **not** fully control camera effort, flower
rewards, plant×bird preference, detectability or source annotation uncertainty.

## Scientific decision

**Observed and robust:** Severe access mismatch is associated with
substantially lower legitimate feeding even within the same bird species ×
survey site and after conditioning on camera waypoint.

**Observed but bounded:** The observed robbery distribution differs from the
simplest fixed bird×site rate expectation.

**Not established:** A fully adjusted bird×site robbery effect, tracked
individual tactic switching, causal adaptation or bypass rescue of lost fitness.

Accordingly the primary manuscript's existing source-based result is unchanged.
This exploratory branch documents a robust legitimate-route loss and an
unresolved robbery mechanism; it does not justify a stronger general
claim about robbery facilitation.

### Next decision — not a new preregistered hypothesis

The remaining problem is the robber M2 **numerical/existence diagnosis**,
not a reason to invent another ecological hypothesis. Before any new formal
claim, test fixed-effect separation / identifiable support under exactly the same
three-state model, using numerical diagnostics only, with no p-value promotion.
