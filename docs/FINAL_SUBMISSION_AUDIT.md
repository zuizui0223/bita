# Final submission audit

## Audit purpose

This audit checks whether the active repository now tells one coherent **theory + mechanism-pattern synthesis** story, whether the scientific completion gate has genuinely closed, and whether empirical evidence is being promoted beyond what its design identifies.

## Integrated submission spine

The manuscript-facing repository retains one fixed theoretical target:

```text
For one declared floral attraction trait A,
one declared flower-specific antagonist-reducing trait D,
and one declared outcome scale W,
the local A x D mixed partial can be interpreted mechanistically only after
channel definitions and orientation conditions have been established.
```

After the orientation gate, the local balance is

```text
W_AD = rho - iota - kappa
```

with antagonist relief (`rho`), mutualist/pollinator interference (`iota`), and direct joint-cost curvature (`kappa`) kept distinct.

The empirical synthesis does not attempt to estimate this mixed partial by pooling unrelated marginal studies. It asks which component mechanisms recur, which change state across ecological contexts, which co-occur in the same systems, and which quantities remain empirically unidentified.

## Scientific completion decision

The mechanism-pattern completion gate is closed.

```text
Gates A-H:                   PASS
scientific completion gate: PASS
manuscript reconstruction:  ALLOWED
```

The gate basis is recorded in `empirical/mechanism_pattern_synthesis/COMPLETION_STATUS_V2.md`.

### Gate A — direct interaction

The registered direct `A x D` search reached its stopping rule. One strict direct cluster is retained, Soper Gorden & Adler (2018), *Impatiens capensis*. Its two reproductive-component interaction estimates have confidence intervals overlapping zero and opposite point directions. The direct sign is therefore unresolved rather than positive or negative.

### Gate B — four marginal mechanism families

All four theory-facing route families have explicit source-adjudicated empirical states:

```text
A_to_pollination
A_to_antagonism
D_to_antagonism
D_to_pollination
```

The coverage audit currently contains 38 effect/directional records across 14 independent biological study clusters. These are evidence-capacity counts, not prevalence estimates.

### Gate C — two quantitative modules

Two biologically distinct source-audited quantitative modules are admitted.

**Leal et al. 2025 floral larceny** is pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. The canonical deposited-synthesis reanalysis includes 48 independent clusters for female reproductive success, 28 for nectar standing crop, and 22 for legitimate visitation. Direction survives the declared ingestion and leave-one-cluster-out sensitivities, while very high heterogeneity and asymmetry diagnostics remain explicit.

**Sasidharan et al. 2023 floral volatiles** is admitted as `PASS_AS_DEPOSITED_REANALYSIS`. The conservative source topology recovers 32 study components. The current-deposit physiological florivore-minus-pollinator contrast remains positive in 32/32 leave-one-component-out refits, but only three components contain both roles and all three paired differences are zero. The assembled contrast is therefore not treated as a causal within-study role effect.

### Gate D — conditionality

Eleven independent sign/context-switch study clusters are retained and mapped into five theory-facing classes: trait intensity/expression, resource/exposure context, consumer identity/functional role, response definition/stage/scale, and compound identity/mechanism partition. Incompatible outcomes are not forced into a cross-outcome meta-regression.

### Gate E — same-system architecture

Ten source-adjudicated systems contain at least two theory-relevant marginal routes with study-level dependence retained. Guarded, guarded-window, interference, shared-tracking, antagonist-biased, context-switching, response-construct, and unresolved states are all represented. Same-system recurrence is not relabelled as direct `A x D` evidence.

### Gate F — direct joint cost

The dedicated search for additional intrinsic cost associated with simultaneous investment in distinct floral attraction and flower-specific defence axes reached its registered stopping rule with zero strict eligible estimates.

Therefore `kappa` remains **unidentified**. It is not estimated as zero. Separate attraction costs, defence costs, trait covariance, and ecological pollinator interference are not combined to manufacture `kappa`.

### Gates G-H — robustness and inference boundary

Module-specific independence, influence, heterogeneity, sensitivity, source-version, and bias diagnostics have been completed at the level appropriate to each quantitative data structure. The theory–empiricism audit explicitly prohibits treating marginal routes as `W_AD`, study counts as parameters, deposit proportions as prevalence, or the single direct interaction as a general sign result.

## Decision on reproductive assurance R

`R` remains in the implemented corollary only as an auxiliary background moderator of the pollination-mediated channel.

It is **not**:

- a third focal trait in the manuscript claim;
- an omnibus reproductive strategy axis;
- a separate empirical target of the current paper.

A paired audit of the declared grid showed that changing `R` from `0.0` to `0.5` changes the local sign in **16 of 1,296** otherwise matched scenario × response-shape evaluations. The effect is small but not identically zero. Removing `R` silently would change a small subset of the canonical finite sensitivity results; retaining it transparently is the reproducible choice.

The manuscript must not lead with `R`, interpret its current parameterization as an empirical estimate, or claim that the paper develops a **three-trait theory**.

## Decision on empirical synthesis language

The earlier statement that the literature layer was "preliminary context only" is superseded for the current integration line. The active paper now contains a source-adjudicated mechanism-pattern empirical synthesis with two quantitative modules and explicit saturated evidence gaps.

This promotion does **not** mean the empirical layer validates or calibrates the mixed-partial model. The correct relationship is:

```text
fixed theory
+ independent evidence that constituent mechanisms recur and change state
+ quantitative synthesis of two theory-relevant mechanism modules
+ direct-evidence and joint-cost identification gaps
= integrated theory + empirical-synthesis paper
```

not:

```text
marginal empirical effects -> estimated W_AD
```

## Submission language to preserve

Use:

```text
fixed local sign criterion
mechanism-pattern empirical synthesis
source-adjudicated same-system architecture
mapped ecological conditionality
two quantitative synthesis modules
bounded direct-interaction evidence gap
kappa unidentified
finite-set sensitivity analysis
auxiliary background moderator R
```

Avoid:

```text
empirically calibrated regime map
prevalence of complementarity in nature
universal attraction-defence law
universal negative defence-to-pollinator effect
marginal meta-analysis estimates W_AD
zero joint-cost evidence means kappa = 0
three-trait theory
```

## Remaining implementation audit

The scientific completion gate no longer justifies additional evidence hunting by default. Remaining work is manuscript and submission integration:

1. update the canonical manuscript from the obsolete preliminary-literature framing to the completed mechanism-pattern synthesis;
2. keep the theory equations, Proposition 1, and endpoint-normalized finite sensitivity results fixed unless a separate scientific revision is explicitly justified;
3. add manuscript tables/figures that display mechanism coverage, conditionality, quantitative modules, and identification gaps without converting counts to prevalence;
4. maintain the immutable Leal module pin and the Sasidharan source-discrepancy boundary;
5. rerun repository CI after narrative and manuscript reconstruction.

The governing rule for further changes is now: strengthen the integrated inference while keeping the distinction between **theoretical mixed curvature** and **empirical constituent-path evidence** explicit.
