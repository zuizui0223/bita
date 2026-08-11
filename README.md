# Biotic Interaction Trait Architecture

Reproducible theory and mechanism-pattern empirical synthesis for one focal floral attraction trait (`A`), one focal flower-specific barrier/defence trait (`D`), and one declared outcome scale (`W`).

The current integration line is PR #126 (`agent/mechanism-pattern-universality-v1`). Its scientific completion gate is closed: the fixed theoretical core is unchanged, while the empirical half now maps **what is recurrent, what is context dependent, and what remains unidentified**.

## Fixed theoretical core

For a declared `A`–`D` pair and declared `W` scale, the local mixed partial

```text
W_AD = d2W / dA dD
```

measures how one focal trait changes the other's local marginal effect on that declared outcome scale.

The signed bookkeeping identity

```text
W_AD = M_AD - G_AD - C_AD
```

is not itself a novelty claim and does not uniquely identify biological mechanisms from total `W` alone. Channel-specific curvatures require operational definitions, channel-specific measurements or manipulations, or additional structural assumptions.

After the relevant orientation conditions have been established for a focal model, the local balance is written as

```text
W_AD = rho - iota - kappa

rho   = antagonist-relief magnitude
iota  = mutualist/pollinator-interference magnitude
kappa = direct joint-cost curvature
```

Local complementarity requires `rho > iota + kappa`; local substitutability requires the reverse inequality. The result is local and does not by itself imply trait covariance, genetic correlation, an evolutionary trajectory, a stable optimum, or an evolved environmental cline.

## Environmental comparative statics

Within a neighbourhood where the orientation gate remains valid,

```text
W_AD(P,H) = rho(P,H) - iota(P,H) - kappa(P,H)
```

and therefore

```text
dW_AD/dH = d rho/dH - d iota/dH - d kappa/dH
dW_AD/dP = d rho/dP - d iota/dP - d kappa/dP
```

Greater antagonist pressure or pollinator service has no universal direction unless the corresponding derivative inequality is satisfied. The separable expressions in the implemented corollary are special cases, not universal environmental laws.

See `docs/GENERAL_SIGN_CRITERION.md`, `docs/NOVELTY_POSITIONING.md`, and `theory/README.md` for assumptions, derivations, prior-art positioning, and inference boundaries.

## Finite sensitivity analysis

The active numerical sweep evaluates the implemented corollary across declared local `A` and `D` coordinates, exogenous pollinator-service (`P`) and antagonist-pressure (`H`) regimes, biological parameter scenarios, and endpoint-normalized nonlinear response-shape variants.

Reproductive assurance `R` is retained only as an **auxiliary background moderator** of the pollination-mediated channel. It is not a third focal trait.

The canonical committed run is `endpoint_normalized_grid_v2`: 2,592 declared mixed-partial evaluations. Its percentages are unweighted occupancies of that declared finite design, not empirical probabilities or estimates of prevalence in nature.

## Mechanism-pattern empirical synthesis

The empirical layer no longer consists only of an abstract-level route registry. Source-adjudicated evidence is organized around four marginal mechanism families, same-system multi-route architecture, direct `A x D` evidence, context/sign switching, quantitative cross-study modules, and direct joint-cost evidence.

The scientific endpoint is deliberately not a pooled estimate of `W_AD`. Marginal studies cannot be algebraically combined into a mixed partial. Instead the synthesis asks whether the mechanisms required by the theory recur, under which contexts they change state, and which theoretically important quantities remain unidentified.

### Four theory-facing marginal families

The source-adjudicated ledger has explicit empirical states for:

```text
A_to_pollination
A_to_antagonism
D_to_antagonism
D_to_pollination
```

The mechanism-coverage audit currently contains 38 source-adjudicated effect/directional records across 14 independent biological study clusters. These counts measure evidence capacity in the screened architecture, not prevalence in nature.

### Same-system regime structure

Ten source-adjudicated biological systems contain at least two theory-relevant marginal routes with shared study dependence retained. The same-system readout documents guarded states, guarded windows followed by pollinator interference, context switching, response-construct dependence, shared attraction tracking, antagonist-biased tracking, and unresolved systems.

These linked systems are stronger mechanistic evidence than unrelated marginal studies, but they are still not relabelled as direct `A x D` estimates.

### Direct `A x D` evidence

The registered direct-interaction search reached its stopping rule after two consecutive expansion batches produced no new eligible direct-design class.

Only one strict current direct cluster is retained: Soper Gorden & Adler (2018), *Impatiens capensis*. Its two reproductive-component interaction estimates have confidence intervals spanning zero and opposite point signs. The direct sign is therefore unresolved.

The absence of a broad direct literature is treated as a bounded evidence-gap result, not proof that no additional eligible study exists outside the registered search universe.

### Conditionality map

`SIGN_SWITCH_LEDGER_V1.csv` contains 11 independent study clusters. Fine-grained within-study contrasts are collapsed into five theory-facing classes:

1. trait intensity / expression regime;
2. resource / exposure context;
3. consumer identity / functional role;
4. response definition / decision stage / reproductive scale;
5. compound identity / mechanism partition.

The project does not manufacture a cross-outcome moderator coefficient from incompatible endpoints. Conditionality is mapped at the level supported by the evidence.

## Two quantitative synthesis modules

### Module 1: floral-larceny antagonist-pressure gate

The completed Leal et al. (2025, *Ecology*, doi:10.1002/ecy.70036) deposited-synthesis reanalysis is pinned to immutable repository commit:

```text
ed33b25593c0d90ad6657753f6f5501d9efc7b82
```

Canonical admitted results include:

```text
female reproductive success: pooled LRR -0.210, 48 independent clusters
nectar standing crop:         pooled LRR -0.483, 28 clusters
legitimate visitation:        pooled LRR -0.291, 22 clusters
```

The directions are robust to the declared within-cluster correlation and quarantine sensitivities and to leave-one-cluster-out refits. Heterogeneity is very high and the declared moderators explain little of it. Funnel asymmetry is reported where detected with the known log-response-ratio limitation.

This module establishes that realised floral-antagonist pressure can carry substantial reward, visitation, and female-fitness costs. It does **not** estimate `rho`, `iota`, `kappa`, or `W_AD`.

### Module 2: floral volatile compounds across pollinators and florivores

The Sasidharan et al. (2023, *Annals of Botany*, doi:10.1093/aob/mcad064) deposited-synthesis reanalysis conservatively recovers 32 study components from the current deposited workbook.

In the current deposit, physiological detection occurs in `84/103` florivore tests and `151/220` pollinator tests, an assembled risk difference of about `+0.129`. The direction remains positive after deleting each recovered study component in turn (`32/32`). However, only three study components contain physiological data for both roles, and all three paired role differences are zero. The assembled contrast is therefore not treated as a causal within-study role effect.

Six repeated behavioral `FVOC x insect x role` units switch between attraction and no response across studies, directly retaining context dependence rather than deleting discordant records.

Canonical adjudication: `PASS_AS_DEPOSITED_REANALYSIS`.

## Direct joint-cost evidence state

A dedicated search for the additional intrinsic resource, construction, energetic, biosynthetic, opportunity, or fitness cost of simultaneously producing a distinct floral attraction axis and a distinct flower-specific defence/access axis reached its registered stopping rule with zero strict eligible estimates.

Therefore:

```text
kappa identified empirically: no
kappa estimated as zero:      no
```

Separate attraction costs, defence costs, trait covariance, or ecological pollinator interference are not used to manufacture `kappa`.

## Completion and inference boundary

The mechanism-pattern completion gate is A–H PASS. See `empirical/mechanism_pattern_synthesis/COMPLETION_STATUS_V2.md`.

The integrated submission must preserve these boundaries:

- marginal routes do not estimate `W_AD`;
- publication or study counts do not become model parameters;
- screened-set and deposited-data proportions are not prevalence in nature;
- the single direct interaction is not generalized beyond its study;
- incompatible outcomes are not averaged into a cross-outcome grand mean;
- the absence of direct joint-cost evidence does not imply `kappa = 0`;
- the finite sensitivity grid is not an empirically calibrated regime map.

## Supplement structure

```text
configs/                              declared sensitivity configuration
theory/                               mathematical definitions and interpretation
trait_architecture/                   active theory, sensitivity, and validation code
scripts/                              reproduction and bounded source-audit entry points
empirical/part_i_robustness/          canonical theory sensitivity outputs
empirical/mechanism_pattern_synthesis integrated source-adjudicated empirical architecture
empirical/broad_reality_evidence/     retained earlier route/context assets and pinned module source
docs/                                 scope, assumptions, methods, and claim boundaries
manuscript/                           canonical integrated manuscript source
tests/                                regression and integrity tests
.github/workflows/                    automated reproduction and source audits
```

See `SUPPLEMENT_MANIFEST.md` for the canonical claim-to-file map and immutable external-module pin.

## Reproduce the current branch

Python 3.11 is the reference environment for the core supplement.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m pytest

python scripts/run_part_i_robustness.py \
  configs/part_i_robustness_grid.json \
  artifacts/supplement/part_i
```

Source-specific audit workflows are documented beside their scripts and under `.github/workflows/`. The exact Leal larceny module is reproduced from the immutable commit listed above rather than silently reimplemented on the integration branch.

## Data policy

Only derived, aggregate, schema, bibliographic, or appropriately licensed material required for the fixed theory or the mechanism-pattern empirical synthesis belongs in the submission tree. Raw third-party observations are not committed merely for convenience. Source discrepancies, inaccessible archives, and negative searches are retained explicitly when they affect inference.
