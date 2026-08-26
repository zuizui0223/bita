# Identification design v1 — discrete attraction × defence channel estimands

## Status

This document redirects the theory toward an **identification design**. It does not change any previously reproduced empirical result. The central object is now a measurable two-level `A × D` interaction, not a claim that a local mixed partial is directly recoverable from existing studies.

The algebraic inequality is retained only as a diagnostic consequence of the decomposition. Its value depends on whether the channel terms can be identified by intervention.

## 1. Primary experimental estimand is discrete

For any outcome surface `X(A,D)` evaluated at two declared attraction levels and two declared defence levels, define

```text
Delta_AD X = X11 - X10 - X01 + X00.
```

This is a **secant interaction across the chosen two levels**. It is not a local mixed partial. A derivative interpretation is a small-contrast limit, not the default experimental claim.

For the full ecological context with antagonists and pollinators present,

```text
Delta_AD W_full
```

is the directly observable total attraction × defence interaction.

## 2. Proposition 1 remains: total W alone does not identify channels

Knowing the total `W(A,D)` surface does not uniquely identify its mutualist, antagonist, and joint-cost components. The new design does not remove that result. It **circumvents it with channel-specific interventions**.

The relevant distinction is:

```text
not identifiable from total W alone
!=
not identifiable after selective interventions.
```

## 3. Required crossed experiment: A × D × antagonist × pollinator

Use four binary factors:

```text
A = low / high attraction
D = low / high flower-specific antagonist-reducing defence
G = antagonist excluded / present
P = pollinator excluded / present
```

This gives 16 cells.

The 16 cells are **not sufficient by construction**. The design is interpretable only if:

1. the antagonist intervention is selective enough not to change the pollinator channel or the A/D manipulation;
2. the pollinator intervention is selective enough not to change the antagonist channel or the A/D manipulation;
3. the same biological A and D contrasts are maintained across all consumer-state cells;
4. cross-state channel contrasts satisfy the declared separability diagnostic;
5. pollinator-independent reproduction is either negligible for the focal interaction or separately quantified.

A bag that removes pollinators and antagonists simultaneously fails condition 2 even though all arithmetic contrasts can still be calculated.

## 4. Antagonist-relief estimand

At fixed pollinator state `p`, define the antagonist-exclusion contrast

```text
R_p(A,D) = W(A,D,G=0,P=p) - W(A,D,G=1,P=p).
```

Under a selective antagonist intervention this is the antagonist loss associated with the focal state. Define

```text
rho_delta^(p) = - Delta_AD R_p.
```

If the A × D antagonist channel is separable from pollinator state, then

```text
rho_delta^(0) = rho_delta^(1).
```

Only then is their common value promoted to `rho_delta`.

This estimand is stronger than a simple `D -> antagonism` effect. It asks whether D specifically changes the **A-dependent** antagonist cost.

## 5. Pollinator-interference estimand and the M0 correction

At fixed antagonist state `g`, define the pollinator-presence increment

```text
Q_g(A,D) = W(A,D,G=g,P=1) - W(A,D,G=g,P=0).
```

The crossed experiment directly identifies

```text
iota_increment_delta^(g) = - Delta_AD Q_g
                          = - Delta_AD (M1 - M0),
```

where `M1` is the mutualist/reproductive contribution with pollinators present and `M0` is the pollinator-absent contribution.

Thus a pollinator contrast does **not** automatically identify the manuscript's total

```text
iota_delta = - Delta_AD M1.
```

Let

```text
m0_delta = Delta_AD M0.
```

Then

```text
iota_delta = iota_increment_delta - m0_delta.
```

Therefore one must either:

- work in a system where `m0_delta = 0` is biologically justified (for example a suitable self-incompatible system), or
- estimate `m0_delta` separately.

A nonzero autonomous/selfing baseline is allowed. It must not be silently set to zero.

## 6. Separability is tested inside the crossed design

Compute antagonist relief at both pollinator states and pollinator increment interference at both antagonist states:

```text
rho_delta^(0), rho_delta^(1)
iota_increment_delta^(0), iota_increment_delta^(1).
```

The relevant invariance condition is

```text
rho_delta^(1) - rho_delta^(0) = 0
```

and equivalently

```text
iota_increment_delta^(1) - iota_increment_delta^(0) = 0.
```

In a saturated binary factorial these are the same `A × D × G × P` four-way interaction up to sign, so they are **not two independent tests**. They are two readings of one A×D-specific cross-consumer coupling diagnostic.

If this four-way contrast is nonzero beyond the declared equivalence margin, the simple channel-separation interpretation fails. The discrepancy must not be absorbed into `kappa`.

In empirical data this should be tested with uncertainty-aware contrasts/equivalence intervals, not a hard point-estimate threshold.

## 7. Selective intervention is a biological design criterion

Crossed arithmetic cannot rescue a biologically nonselective intervention. Candidate systems should be chosen because the two consumer channels can plausibly be separated by one or more of:

- body-size exclusion;
- access-route exclusion;
- diel activity separation;
- phenological separation;
- behavioural or taxonomic selectivity;
- targeted manipulation that changes one access mechanism without altering the other.

The current repository contains a useful **system-selection anchor** in *Pedicularis rex* (Sun & Huang 2015): draining the water-holding cupulate bract strongly changes seed-predator damage while the same manipulation shows no detected change in legitimate pollinator or nectar-robber visitation. The study lacks an independent A manipulation and therefore does not identify `rho_delta`, but it demonstrates the kind of consumer-selective physical mechanism that a future crossed design needs.

## 8. Joint cost: residual and independent assay must remain distinct

After `rho_delta`, baseline-corrected `iota_delta`, and `Delta_AD W_full` are available, define the **unallocated residual**

```text
U_delta = rho_delta - iota_delta - Delta_AD W_full.
```

Do not automatically call `U_delta` kappa. Imperfect exclusion, an incomplete channel decomposition, baseline misspecification, and unmodelled higher-order mechanisms can all enter this residual.

Run a separate `A × D` allocation/construction-cost assay with pollinator and antagonist channels suppressed or standardized. On a declared cost endpoint `C`, estimate

```text
kappa_assay_delta = Delta_AD C.
```

The sign can be compared even when the cost endpoint is not on the same scale as W. Magnitude comparison requires a commensurate outcome scale.

The design therefore has two distinct outputs:

```text
crossed ecological experiment -> U_delta
independent cost assay         -> kappa_assay_delta
```

Agreement supports the intended decomposition. Disagreement diagnoses missing channels, intervention leakage, baseline error, or a mismatched cost assay.

## 9. The inequality becomes a sign-inference diagnostic

The old one-sided statement is no longer sold as a prediction theorem. In discrete form,

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

If complementarity is observed but the identified biotic balance is nonpositive,

```text
Delta_AD W > 0
and
rho_delta <= iota_delta,
```

then the unallocated joint channel must be negative:

```text
U_delta < 0.
```

If the independent cost assay and the residual are shown to represent the same joint channel, this implies

```text
kappa_delta < 0.
```

This is the useful role of the algebra: **constrain the sign of an otherwise difficult-to-observe joint channel by combining directly measured total interaction and channel-specific contrasts**.

## 10. Existing studies become an identification-coverage audit

The literature synthesis should no longer be framed as empirical validation of the inequality. Instead each study is asked:

1. Is A separately defined and manipulated/measured?
2. Is D separately defined as a flower-specific antagonist-reducing axis?
3. Is an A×D total interaction estimable on a linked outcome?
4. Is there a selective antagonist toggle?
5. Is there a selective pollinator toggle?
6. Is `Delta_AD M0` known or justifiably zero?
7. Is an independent A×D joint-cost assay present?
8. Which estimands are therefore recoverable?

The first anchor audit is stored in `empirical/identification_design/EXISTING_STUDY_IDENTIFICATION_AUDIT_V1.csv`.

## 11. Current interpretation of the closest systems

### Soper Gorden & Adler 2018 — *Impatiens capensis*

The deposited linked plant panel contains floral redness and floral condensed tannins and supports an explicit total A×D term. That makes it useful for `Delta_AD W` / total interaction demonstration. It lacks the crossed antagonist and pollinator interventions needed to split that interaction into `rho_delta` and `iota_delta`.

### Kessler et al. 2015 — *Nicotiana attenuata*

The four floral phenotypes form a genuine 2×2 design, but the second axis is nectar reward restriction, not an independently justified antagonist-reducing D. It therefore demonstrates why a factorial phenotype alone is insufficient for identification. The current repository audit also did not recover a raw uncertainty-bearing outcome table for reconstructing the desired channel contrasts.

### Sun & Huang 2015 — *Pedicularis rex*

This is not an A×D study, but the water-bract manipulation is unusually useful for system selection because its experimentally demonstrated seed-predator protection occurs without a detected legitimate-pollinator or nectar-robber response. It is a candidate template for constructing a selective D toggle, not an estimate of rho.

## 12. Consequence for the paper architecture

The proposed main line is now:

```text
observed total interaction
-> observational non-identifiability
-> measurable discrete estimands
-> crossed 16-cell intervention design
-> internal separability diagnostic
-> explicit M0 correction
-> independent joint-cost assay
-> sign inference for the unobserved joint channel
-> existing-study identification coverage / near misses
-> experimental roadmap
```

The 2,592-point finite grid becomes implementation/model-family sensitivity material, not a headline empirical or theoretical result.
