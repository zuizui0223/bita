# Channel leverage readout v1: which measurement would change conclusions

Reproduce with:

```bash
python scripts/run_channel_leverage.py \
  configs/part_i_robustness_grid.json empirical/channel_leverage 0.25
```

## 1. The question, and why it is asked now

The declared empirical target measures one parameter, `c_D`, of one channel. That pathway was
chosen because its literature is the most tractable: the studies are manipulations, the outcome is
a direct channel measurement rather than total fitness, and the route already has independent
clusters in one compatibility cell.

Feasibility is a legitimate reason to start somewhere. It is not the same as being the most
informative place to start, and the project should not let the two blur together. This analysis
asks the comparable question for every parameter of the three-channel balance:

> if this parameter could be pinned to a given relative precision, what fraction of the declared
> grid's sign classifications would that settle?

Boundaries are found by root-finding on the deployed mixed partial in
`trait_architecture/robustness.py`, so the result holds across all four declared
endpoint-normalized response-shape variants, not only the baseline exponential form. Under the
shape variants the mixed partial depends on the attraction coordinate `A` through the
attraction-gain and joint-cost terms, so `A` is retained as a grid axis here. It cancels only in
the baseline form, which is why the earlier `c_D`-only analysis could drop it.

Two independent derivations of the `c_D` boundary — the closed form in
`trait_architecture/empirical_leverage.py` and the scan-and-bisect search here — are checked
against each other at 27 grid points in `tests/test_channel_leverage.py`.

## 2. Result: the declared target ranks fourth of five

Pooled over four parameter scenarios and four response-shape variants, at a relative precision of
±25% of the scenario's own parameter value:

| rank | parameter | channel | prior-sensitive fraction | settled fraction | value of information |
|---|---|---|---|---|---|
| 1 | `attraction_tracking` (`d_A`) | antagonist relief `rho` | 0.862 | 0.855 | **0.717** |
| 2 | `attraction_defence_shared_cost` (`c_AD`) | direct joint cost `kappa` | 0.612 | 0.932 | 0.544 |
| 3 | `floral_defence_efficacy` (`e_F`) | antagonist relief `rho` | 0.671 | 0.857 | 0.528 |
| 4 | `defence_pollinator_cost` (`c_D`) | mutualist interference `iota` | 0.553 | 0.926 | **0.480** |
| 5 | `attraction_gain` (`b_A`) | mutualist interference `iota` | 0.509 | 0.909 | 0.418 |

*Value of information* is the settled fraction minus the fraction the declared prior range already
settles, so a parameter scores highly only when measuring it resolves points that were genuinely
open beforehand.

`attraction_tracking` — how strongly floral antagonists track the focal attraction trait — leads
on both components: it is the parameter that matters at the most grid points (0.862 prior
sensitive) and the one whose measurement resolves the most.

## 3. The ordering does not depend on the response shape

Rank 1 within each declared endpoint-normalized variant, at ±25%:

| response-shape variant | leading parameter | value of information | rank of `c_D` |
|---|---|---|---|
| `baseline` | `attraction_tracking` | 0.75 | 4 |
| `saturating_attraction` | `attraction_tracking` | 0.76 | 4 |
| `saturating_defence` | `attraction_tracking` | 0.68 | 2 |
| `saturating_both_curved_cost` | `attraction_tracking` | 0.68 | 3 (tied) |

`attraction_tracking` leads all four. `c_D` never leads any. The one variant where the
interference channel rises to second is `saturating_defence`, which is exactly the variant that
makes the defence response most curved — an internally coherent result rather than noise.

## 4. Value of information against precision

| parameter | ±10% | ±25% | ±50% | ±100% |
|---|---|---|---|---|
| `attraction_tracking` | 0.800 | 0.717 | 0.554 | 0.130 |
| `floral_defence_efficacy` | 0.609 | 0.528 | 0.375 | 0.000 |
| `attraction_defence_shared_cost` | 0.590 | 0.544 | 0.493 | 0.381 |
| `defence_pollinator_cost` | 0.520 | 0.480 | 0.403 | 0.163 |
| `attraction_gain` | 0.470 | 0.418 | 0.325 | 0.079 |

The ranking is stable from ±10% to ±50%. At ±100% it degrades for the bounded parameters —
`floral_defence_efficacy` reaches exactly zero because a ±100% window around a value near 0.5
covers its entire declared prior range `[0, 1]`, so the "measurement" adds nothing. That is a
property of the declared range, not a finding, and it is why the ranking is reported at ±25%.

## 5. What this changes

It does **not** retract the declared empirical target. `c_D` remains the right first target:
it is the only channel with a manipulative literature that measures the channel directly, the
bridge from the measured route to the channel sign is explicit, and the pre-registration and
analysis for it are complete and executable. A fourth-ranked measurement that can actually be
made beats a first-ranked one that cannot.

It does change what the project should say about the target, and what it should queue next.

- **Say plainly that the tractable channel is not the decisive one.** Reporting a `c_D` synthesis
  without this ranking would leave the impression that the measured channel is where the sign is
  decided. It is not, in this corollary, on this grid.
- **The highest-leverage next target is `d_A`, in the `A_to_antagonism` route.** How strongly
  floral antagonists track the focal attraction trait. That route already has two declared strata
  in the registry (`AH_visual_damage_logor_observational`, `AH_scent_damage_logor_observational`)
  and is measurable observationally, so it is not obviously out of reach — but it is an
  observational route, and the identification problems that come with that are different from and
  probably harder than the manipulative `c_D` literature.
- **The joint-cost parameter `c_AD` ranks second and has essentially no direct literature.** It is
  the term the manuscript already flags as needing matched trait-allocation data. This analysis
  puts a number on how much that gap costs.

## 6. Boundary

Value of information is a property of the declared corollary, the declared finite grid, and the
declared prior ranges — which are stated in `channel_leverage_diagnostics.json` and are declared,
not fitted. Substituting different prior ranges will move the numbers; the ranking should be
re-run rather than assumed to carry over.

This analysis ranks which measurement would change sign classifications. It estimates no
parameter, contains no evidence about nature, and makes no statement about how common either sign
is. Grid fractions are unweighted occupancies of the declared finite design, consistent with the
Part I convention.
