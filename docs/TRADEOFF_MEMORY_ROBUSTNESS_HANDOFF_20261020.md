# Functional trade-off integration: memory robustness and irreducible concurrent conflict

Date: 2026-10-20. Companion to TRADEOFF_TO_EVOLVED_ARCHITECTURE_CAUSAL_SYNTHESIS_V1.md in BITA PR #362. The PAYOFF theory source is PR #338, theory/TWO_CUE_MEMORY_AND_IRREDUCIBLE_CONFLICT.md.

## Scientific claim recovered from the model, not nature

**Genuine simultaneous conflict creates a structural benefit that better temporal prediction cannot eliminate. Fast environmental change alone does not imply that a fixed structure wins against memory-assisted plasticity.**

These are conditional theoretical findings, not evidence that an historical trade-off generated floral or sexual architecture. Functional conflict, module payoff, accessibility, source-specific mechanism and evolutionary origin are separate inferential objects.

## Three comparators and the right ecological questions

A one-coordinate structure must satisfy both simultaneously active functions. Three strategies must be compared on the **same reproductive-fitness timescale**, after defining the actual ecological functionality of each:

1. SHARED: the original same-coordinate compromise, without a special cue-contingent phenotype controller.
2. PLASTIC: a reversibly cue-controlled **single** phenotypic coordinate, possibly informed by past observations; do not call this a new genetic module simply because its expressed sexual morphology changes.
3. FIXED MODULES: a genuinely viable two-coordinate design that can coexpress the two relevant functions at separate optima and pays an architecture-specific cost; separation of male and female functions **among distinct individuals** is not automatically the same model.

The extended PAYOFF model adds a memory-controlled policy based on present and previous **noisy** cues, without observing the hidden environment. The two-cue stationary policy is analytically optimized by solving two convex quadratic regions and their diagonal. Independent enumeration of all 64 consecutive environment/cue paths verifies its expected loss. No arbitrary internal-state controller or unlimited memory policy is optimized in the numeric witness.

## Result A: evolutionary-value ranking can be re-entrant

The original memoryless example (a=3, b=1, Delta=2, q=0.9, plastic running cost B=0.05, phenotype switch cost c=1, fixed module K=3.8) still favors plasticity at rho=0.1 and fixed modules at rho=0.9.

A separately labeled **post-open synthetic robustness** cost K=3.87, all other inputs unchanged, yields:

| True environmental switching probability rho | Two-cue plastic loss | Fixed-module loss K | Intrinsic model winner |
| --- | ---: | ---: | --- |
| 0.90 | 3.869056206 | 3.87 | Memory plasticity |
| 0.95 | 3.872457906 | 3.87 | Fixed modules |
| 0.99 | 3.867283201 | 3.87 | Memory plasticity |

Near rho=1 a two-state environment nearly alternates deterministically; frequent change can be predictable. Two numerical phase crossings occur near rho=0.9066209383 and 0.9765403818. A memory maintenance fee can erase the second advantage: at rho=.99, fee must be **less than 0.002716799** to retain two-cue preference over fixed modules.

The ecological macro predictor cannot be just "frequency of environmental shifts." Measure temporal autocorrelation, predictability conditional on accessible cues and the costs of operating/reconfiguring a shared phenotype, separately.

## Result B: the simultaneous conflict floor survives all memory

For each environmental state E and every scalar shared phenotype x,

    F_E(x)=C+(a+b)(x-x*_E)^2 >= C,
    C=ab*Delta^2/(a+b).

This is a pathwise statement independent of data history. If signal, memory and switching costs are nonnegative, every strategy that **still forces both simultaneously active functions through one phenotypic coordinate** has loss >=C, including a hypothetical fully informed controller. A genuinely viable ideal coexpressed two-coordinate module with matched K<C therefore beats every such one-coordinate policy in the model.

This does not cover switching **when** the functions are performed, avoiding simultaneous enemy exposure, modifying the feasible coordinate dimension, or having functions on different individuals (dioecy). Those are different biological strategy sets rather than exceptions to the math.

## Source-derived Wurmbea context remains limited

In Wurmbea, marked plants can shift expression within their lifetime. Controlled high/low resource regimes produced different observed perfect-flower expression rates (66% vs 42%) in one subdioecious setting, and another study's relative female seed advantage changes from 3.7 to 1.4 under manipulated outcrossing. A published Case et al. (2008) plastid voucher study and follow-up source audit identify close maternal-marker backgrounds across some sexually different populations; the MR2/MR3 psbBTNH provenance conflict remains on HOLD, not silently corrected.

These source data provide candidate physiological, developmental and reproductive routes. **They do not estimate** the noise accuracy q, environmental transition rho, the simultaneous pure-function conflict floor C, plastic response cost c, memory cost M or structural cost K. Seed advantage is not matched male-plus-female lifetime fitness, and cpDNA distances do not reconstruct nuclear inherited architecture. The PAYOFF module witness must not be fitted by substituting 66%/42% for q or 3.7/1.4 for K.

## Updated cross-repository handoff

- SCH: identify genuine *simultaneous* opposing selection on the same coordinate, not merely different contextual optima.
- BALANCE: test whether shared, reversible and differentiated alternatives can be matched and optimized on the same fitness scale. Source-selected natural histories are not representative prevalence.
- SLK: owns general architecture value and the sequence value -> accessibility -> invasion -> fixation -> occupancy.
- PAYOFF: adds model-specific cue memory, switching-cost, environmental-predictability and coordination counterexamples.
- BITA: identifies ecological channels creating observed trait interactions, with selective consumer manipulation where feasible; fitted residuals are neither measured module cost nor proof of historical origin.

**Next empirical sampling variables:** functional demand simultaneity within a reproductive window; temporal environment predictability independent of variance/frequency; individual reversible phenotypic response and actual switching burden; viable structural alternatives and direct common-fitness comparison; dated heritable origin.

**Promotion ceiling:** mathematical mechanism verified, historical trade-off-caused new architecture **not verified**. No new original biology or macro-analysis effect is claimed by this memory-only extension.
