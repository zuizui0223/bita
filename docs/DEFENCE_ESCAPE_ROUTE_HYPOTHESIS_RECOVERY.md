# Defence escape-route hypothesis recovery

## The Chapter 2 question

The one-trait companion question asks what happens when pollinators and antagonists track the same attraction/display coordinate. BITA begins at the next step:

> **Can a distinct flower-associated defence trait `D` release the conflict on `A`, and what observations distinguish antagonist relief from pollinator interference and joint cost?**

For the declared two-level coordinates,

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

Positive attraction-defence complementarity is an escape route only when antagonist relief exceeds the pollinator penalty and remaining joint cost:

```text
rho_delta > iota_delta + kappa_delta.
```

These equations imply an important identification split:

```text
escape decision:      rho_delta > iota_delta + kappa_delta  <=>  Delta_AD W > 0
mechanism allocation: which of rho_delta, iota_delta and kappa_delta generated that sign?
```

Therefore **full channel point identification is not required to decide the strict escape inequality**. A valid same-scale total `A x D` reproductive interaction whose uncertainty lies entirely above zero would identify escape on that declared outcome scale. Channel decomposition is required for mechanism attribution, not for the sign decision itself.

The machine-readable hypothesis audit is `empirical/identification_design/DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv`. Its targeted primary-source verification is `docs/BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md`.

## What the ecological evidence has positively answered

### 1. The proposed mechanisms exist

The route ledger recovers all four constituent route families. In particular, 18 independent clusters contain a `D`-to-antagonism route and 10 contain a `D`-to-pollination route. These records establish that both relief opportunity and pollinator interference are biologically recurrent ingredients.

### 2. Defence is not uniformly costly to pollination

Matched chemical and physical systems contain guarded states in which antagonist access or damage declines without an equivalent pollinator loss. Other systems show interference or bypass. Current evidence therefore answers an important mechanistic question: whether defence helps or harms the attraction strategy depends on consumer susceptibility, exposure threshold, access geometry, timing, and function.

### 3. A switching architecture is recoverable in nature

The strongest current pattern-level result is the route-separation rule. A priori separated routes tend to permit antagonist filtering while preserving legitimate function; overlapped routes tend to create pollinator interference; bypassable routes tend to make the focal defence ineffective. The rule is recurrent and has survived a retrospective noncircularity stress test.

### 4. Existing studies constrain different parts of the explanation

Trait factorials, consumer factorials, selective defence manipulations, observational trait interactions, and public-data reconstructions all exist, but mostly in different systems. This design fragmentation is a positive empirical result: it identifies the exact information already available and the smallest missing augmentation for each study.

### 5. The escape decision is formally easier than mechanism attribution

The strict escape condition is a sign question about total `Delta_AD W`. If a valid total interaction interval is entirely positive, the inequality is decided even while the compatible `(rho, iota, kappa)` allocations remain a plane or bounded set. The `classify_escape_criterion` helper in `trait_architecture/partial_identification.py` encodes exactly this distinction and does not infer a total interaction from channel-specific data.

### 6. Kessler 2008 already supplies a manipulated A×D-like reproductive surface

Kessler, Gase & Baldwin (2008; doi:10.1126/science.1160072) independently blocked floral benzylacetone production and nicotine production in all four combinations in a native-field experiment:

```text
EV    A+, D+
PMT   A+, D-
CHAL  A-, D+
CP    A-, D-
```

The mapping is unusually close to the focal architecture: benzylacetone is the validated floral attractant axis and nicotine/nectar nicotine is a defence/repellent candidate axis. The experiment measured common female and male reproductive outcomes. For pollinator-mediated female outcrossing, the published article reports 474 informative antherectomized flowers and 87 capsules after excluding a wind-only day, with the `A+,D+` state near 35% capsule production and the three states missing one or both components near 12–14%.

The published rounded range therefore gives a positive discrete interaction on both probability and logit point scales. This is not merely a channel-specific service anchor: **a manipulated two-trait common reproductive surface exists**.

The remaining problem is uncertainty. A registered Science supporting-material probe tested five current/legacy routes for Fig. S8A and received HTTP 403 on all five. Exact day-by-genotype values and the source-scale factorial uncertainty were therefore not recovered. See `empirical/identification_design/KESSLER_2008_SUPPLEMENT_ACCESS_RECEIPT_V1.md`.

A second registered analysis then enumerated integer allocations compatible with the published 474-flower / 87-capsule totals and deliberately widened rounded cell bands. Across maximum cell-denominator ratios from 1.25 to 3.0:

```text
minimum probability-scale Delta: +0.1731 -> +0.1710
minimum naive probability z:      2.461  -> 2.296
minimum logit beta:               +0.891 -> +0.876
minimum logit z:                   1.763  -> 1.593
minimum logit 95% CI lower bound: -0.100 -> -0.205
```

Thus millions of aggregate-compatible allocations preserve the **positive interaction sign**, but they do not identify the source/design-based interval. Treating flowers as independent is also fragile: at the broadest denominator profile a variance inflation of about 1.37 would reduce the worst naive probability-scale z to 1.96. The aggregate analysis is therefore labelled `SIGN_ROBUST_FORMAL_SOURCE_UNCERTAINTY_UNRESOLVED`, not a recovered source interaction test. See `empirical/identification_design/KESSLER_2008_AGGREGATE_BOUNDS_V1.md`.

A second caveat remains biological rather than statistical: `Napmt1/2` silencing reduces nicotine systemically, so the manipulated D coordinate is not perfectly flower-restricted even though floral/nectar nicotine is central to the visitor phenotype.

### 7. Impatiens supplies the complementary uncertainty-bearing observational case

The public Soper Gorden & Adler *Impatiens capensis* panel was rerun against the fixed Dryad v4805 archive using the same hierarchical HC3 retrofit. The deposited `Total_Fruits_Per_Day` endpoint combines CH and CL fruit production:

```text
A:D estimate = -0.1737
HC3 95% CI   = [-0.3791, +0.0316]
n             = 170
sign status   = CROSSES_ZERO
```

The deposited table also permits a deliberately secondary reconstructed CH+CL mature-seed-output proxy:

```text
A:D estimate = +0.1528
HC3 95% CI   = [-0.5487, +0.8544]
n             = 70
sign status   = CROSSES_ZERO
```

The point estimate reverses sign across the two summaries and both intervals cross zero. Moreover, the *Impatiens* A and D traits are observational. This system therefore supplies uncertainty-bearing reproductive associations but not a causal escape estimate. The sign instability supports a stopping rule against further nearby endpoint mining from the same panel.

## Where the evidence stops

The present evidence does **not yet identify a positive escape event with a defensible source/design-based interval wholly above zero**, but the reason is now much sharper.

- **Kessler 2008:** manipulated A and D-like axes, same 2×2 field plants, common reproductive outcomes, and a robustly positive aggregate interaction sign are all recovered. What is missing is the source/design-based interaction uncertainty; the D manipulation also has a systemic-nicotine scope caveat.
- **Impatiens 2018:** uncertainty-bearing total-fruit and derived seed-output associations are available, but A and D are observational and both intervals cross zero.
- Consequently, the empirical gap is **not** “nobody has manipulated A×D on a common reproductive surface.” That surface exists in Kessler. The remaining outcome-level gap is an uncertainty-identified positive manipulated interaction with an adequately bounded trait intervention.
- Separately, no screened system point-identifies both `rho_delta` and `iota_delta` with the full selective crossed design, and no strict independent assay identifies `kappa_delta`. Mechanism allocation remains unresolved even if a future total interaction is formally positive.
- Zero recovered cost assays does not imply zero cost.

The machine status remains `UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE` (legacy readout token: `UNRESOLVED_CURRENT_TOTAL_EVIDENCE`) because the strict decision rule is an uncertainty-bearing total interval, not a positive rounded point contrast. This token should be read as “formal escape sign not uncertainty-identified,” not as “all available point signs are unknown.”

Thus the statement “escape is currently unresolved” remains correct, but **it must not be justified by saying that all three channels must first be point-identified**. A valid positive total interaction would decide the inequality; the full crossed consumer and cost design would then explain why it is positive.

## Hypothesis-by-hypothesis result

| Layer | Current result |
|---|---|
| One-trait conflict | Biological motivation and constituent A routes recovered; tested separately in SCH |
| Marginal antagonist reduction by D | Recurrent strong evidence |
| Pollinator-preserving selective defence | Recurrent, quantitative but still provisional across screened systems |
| Route-separation switching rule | Recurrent strong retrospective candidate |
| Manipulated common reproductive A×D | Kessler 2008: direct 2×2 factorial; aggregate sign robustly positive; source/design CI not recovered |
| Observational broad fruit-production A×D | *Impatiens* `Total_Fruits_Per_Day`: -0.1737, HC3 CI [-0.3791, +0.0316], crosses zero |
| Derived mature-seed-output A×D | *Impatiens* CH+CL proxy: +0.1528, HC3 CI [-0.5487, +0.8544], n=70, crosses zero |
| Formal escape outcome `Delta_AD W > 0` | `UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE`; Kessler is the strongest positive sign anchor but lacks source/design uncertainty |
| `rho_delta` and `iota_delta` allocation | Not point-identified in 0/16 screened systems |
| Independent `kappa_delta` | 0 strict estimates; documented evidence gap |
| Mechanism-resolved escape explanation | Not evaluable in current complete-system evidence |
| Experimental decision procedure | Achieved method result |

## Revised minimum augmentation

The empirical program is now naturally two-stage, but stage 1 is narrower than before.

1. **Decide whether escape occurs.** First attempt to recover Kessler's source/design-based A×D uncertainty from lawful supporting-material or author-deposited data. If that remains inaccessible, prioritize a second genuinely manipulated A×D common reproductive surface with complete uncertainty. A valid interval wholly above zero identifies the strict escape inequality.
2. **Explain why it occurs.** Add selective antagonist and pollinator interventions, characterize `M0_delta`, test separability, and independently assay the remaining joint cost. These measurements allocate the positive or negative total interaction among `rho_delta`, `iota_delta` and `kappa_delta`.

The *Impatiens* upgrade supplies a practical stopping rule: **do not spend the next development cycle constructing additional nearby observational reproductive summaries from the same panel**. The Kessler result likewise supplies a different stopping rule: **do not describe the next empirical search as looking for the first manipulated A×D surface**. That surface is already recovered; the missing object is its defensible uncertainty or an independent complete replication.

This ordering prevents an unnecessarily strong mechanism gate from blocking a valid outcome-level result while preserving the stricter standard for causal explanation.

## Validation state

The Kessler supplement probe is regression-tested and its registered publisher access run completed successfully as a fail-closed probe. The aggregate-bound analysis is independently regression-tested and its registered Actions run completed successfully after enumerating all declared denominator profiles. The *Impatiens* fixed-Dryad reanalysis, candidate identification package, Ecology submission package, submission-scope guard, and complete Python 3.10/3.11/3.12 pytest matrix have also passed on PR #153 during this recovery branch.

## Positive paper-level claim

> Nature repeatedly implements antagonist-reducing traits and selective route architectures that can preserve pollination. BITA separates two empirical questions that previous framing conflated: whether the attraction-by-defence fitness interaction is positive, and which relief, interference and cost channels generate that sign. A direct field manipulation of floral attraction and nicotine already supplies a positive, aggregate-sign-robust two-trait reproductive interaction, while an independent public observational system supplies uncertainty-bearing estimates that cross zero. What remains missing at the outcome level is a source/design-based positive interaction interval with clean trait scope; what remains missing at the mechanism level is selective channel and independent cost identification.

This statement is stronger than “the mechanism was not identified,” stronger than “direct A×D experimentation is absent,” and narrower than claiming that defence has already been formally shown to release the one-trait conflict in a complete empirical system.
