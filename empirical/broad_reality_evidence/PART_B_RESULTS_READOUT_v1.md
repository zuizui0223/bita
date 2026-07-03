# Part B results readout v1 (current evidence base)

Reproducible run of the full Part B pipeline (`scripts/run_part_b_support.py`,
layers B1–B5) on the current committed inputs. This is the honest present state:
the machinery is complete and runs end to end; the evidence base is thin, so most
cells are reported as *insufficient* rather than forced.

```text
inputs:
  B1 route records  empirical/broad_reality_evidence/broad_route_records.csv
  B2/B3 effects     empirical/broad_reality_evidence/part_b_arrow_effects.csv   (5 verified anchors)
  B2/B3 strata      empirical/broad_reality_evidence/part_b_arrow_strata.csv
  B3 hypotheses     configs/part_b_moderator_hypotheses.json
  B4 scenarios      configs/part_b_break_even_scenarios.json
```

## B1 direction map — one channel already has directional support

Of the source-adjudicated direction strata, exactly one currently reaches the
>= 3 independent-cluster threshold:

| Channel | Trait / outcome | Design | Clusters | Compatible | Verdict |
|---|---|---|---:|---:|---|
| `c_D` (`B_to_pollination`) | chemical_barrier -> pollinator preference/foraging | manipulation | 3 | 100% | `mostly_compatible_with_channel_assumption` |

So the model's `c_D > 0` premise (a floral chemical barrier reduces pollinator
use) has real, if modest, directional support. Every other channel stratum is
`insufficient_directional_clusters`.

## B2 per-arrow effect envelopes — five real anchors, none poolable yet

The five verified registry anchors (Impatiens 2018 x4 + Gymnadenia 2016 x1),
re-expressed in the marginal-arrow schema, each land alone in their stratum:

| Stratum | Part I arrow | Clusters | Status |
|---|---|---:|---|
| `AP_visual_visitation_beta_observational` | `b_A` | 1 | insufficient_independent_clusters |
| `AH_visual_damage_beta_observational` | `d_A` | 1 | insufficient_independent_clusters |
| `AH_scent_damage_logor_observational` | `d_A` | 1 | insufficient_independent_clusters |
| `BH_chemical_damage_beta_observational` | `e_F` | 1 | insufficient_independent_clusters |
| `BP_chemical_visitation_beta_observational` | `c_D` | 1 | insufficient_independent_clusters |

No arrow yet has the >= 3 independent clusters needed for a pooled envelope. This
is the same conclusion as `FIXED_CORPUS_CAPACITY_V1.md`, now produced by the
marginal-arrow pipeline rather than the joint-panel route.

## B3 moderator/conditionality — engine ready, no coded data yet

All three pre-registered moderator hypotheses return `insufficient_levels`: no
effect in the current table is coded with a moderator level, so neither the low
nor the high subgroup has effects. The B3 engine is verified (see
`tests/test_part_b_moderator.py`); it awaits moderator-coded effects, which is the
next data task.

## B4 break-even regime map — mechanism conditionality is well-behaved

The B4 sensitivity map (declared channel scenarios, not calibrated) reproduces
exactly the conditionality Part A proves. At the mid shared-cost scenario
`c_AD = 0.1`, across the 162-case local grid:

| Channel scenario | Complementary | Substitutable |
|---|---:|---:|
| low_tracking | 0 | 162 |
| baseline | 96 | 66 |
| high_tracking | 144 | 18 |

Stronger antagonist tracking and barrier efficacy with weaker obstruction push
cases into the complementary regime; the reverse pushes them to substitutable.
The map is a declared sensitivity result and becomes empirical once B2 envelopes
replace the declared channel scenarios.

## B5 evidence synthesis + regime-leverage priority

B5 combines each arrow's evidence state with its B4 regime leverage (how much the
complementary fraction of the local grid moves when that arrow swings across its
declared range) to produce an objective collection priority.

Critically, B5 does **not** call opposite signs a biological conflict merely
because they share an arrow label. The B2 compatibility stratum is
`trait class × outcome class × effect metric × design class`. Opposite signs
within one such stratum are a genuine `within_stratum_conflict`; opposite signs
across different strata are `cross_stratum_heterogeneity` and require separate
within-stratum replication before any moderator model is attempted.

| Rank | Arrow | Role | Clusters | Signs | State | Leverage | Recommended next action |
|---:|---|---|---:|---|---|---:|---|
| 1 | `d_A` | complementarity driver | 2 | +1 / -1 | **cross_stratum_heterogeneity** | +0.67 | retain visual and scent strata; collect compatible within-stratum clusters before B3 |
| 2 | `e_F` | complementarity driver | 1 | +1 / -0 | single anchor | +0.37 | collect 2 more independent clusters |
| 3 | `b_A` | substitutability driver | 1 | +1 / -0 | single anchor | -0.31 | collect 2 more independent clusters |
| 4 | `c_D` | substitutability driver | 1 | +0 / -1 | single anchor | -0.22 | collect 2 more independent clusters |

Leverage is measured with declared per-arrow ranges (`leverage_ranges` in the B4
config), so all four arrows are comparable. Signs are informative: the two
complementarity drivers (`d_A`, `e_F`) raise the complementary fraction, the two
substitutability drivers (`b_A`, `c_D`) lower it, exactly as the mixed-partial
expression requires.

The present `d_A` anchors differ in both their trait class and effect metric:
Impatiens is a visual-signal standardized beta (-0.09), whereas Gymnadenia is a
scent log odds ratio (+0.57). They are therefore not a test of a single shared
parameter whose sign has reversed. `d_A` remains the highest-leverage evidence
gap, but the correct next action is **stratum-specific collection**, not coding
`pollination_generalization` as if it already explained a sign conflict.

## Bottom line

The Part B pipeline is complete and reproducible. The current evidence supports
one channel premise directionally (`c_D`), holds five verified single-cluster
anchors across the four arrows, and cannot yet pool or test conditionality. B5
identifies the priority objectively: **`d_A` is the highest-leverage, stratified
evidence gap**, so visual-display and scent/reward routes must each gain
compatible independent clusters before a moderator or pooled-envelope claim.

## Next-step scouting (d_A)

A first scouting pass for `d_A` candidates is recorded in
`d_A_candidate_scouting_v1.md` / `d_A_candidate_scouting_v1.csv` (8 unverified
leads). The strongest is Schiestl et al. 2015 (eLife `10.7554/eLife.07641`): a
candidate manipulative scent/nectar -> hawkmoth-oviposition route on a generalized
system. Caruso et al. 2019 (Evolution `10.1111/evo.13639`) is a meta-analytic seed
for mining independent primary-study clusters. These remain candidates for human
verification, not effects, and enter the coding queue only after a direct estimate,
denominator, uncertainty, and trait-stratum basis are confirmed.
