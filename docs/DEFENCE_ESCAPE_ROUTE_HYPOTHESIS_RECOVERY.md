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
escape decision:     rho_delta > iota_delta + kappa_delta  <=>  Delta_AD W > 0
mechanism allocation: which of rho_delta, iota_delta and kappa_delta generated that sign?
```

Therefore **full channel point identification is not required to decide the strict escape inequality**. A same-scale total `A x D` reproductive interaction whose uncertainty lies entirely above zero would identify escape on that declared outcome scale. Channel decomposition is required for mechanism attribution, not for the sign decision itself.

The machine-readable hypothesis audit is `empirical/identification_design/DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv`. Its targeted primary-source verification is `docs/BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md`.

## What the ecological evidence has positively answered

### 1. The proposed mechanisms exist

The route ledger recovers all four constituent route families. In particular, 18 independent clusters contain a `D`-to-antagonism route and 10 contain a `D`-to-pollination route. These records establish that both relief opportunity and pollinator interference are biologically recurrent ingredients.

### 2. Defence is not uniformly costly to pollination

Matched chemical and physical systems contain guarded states in which antagonist access or damage declines without an equivalent pollinator loss. Other systems show interference or bypass. Current evidence therefore answers an important mechanistic question: whether defence helps or harms the attraction strategy depends on consumer susceptibility, exposure threshold, access geometry, timing, and function.

### 3. A switching architecture is recoverable in nature

The strongest current pattern-level result is the route-separation rule. A priori separated routes tend to permit antagonist filtering while preserving legitimate function; overlapped routes tend to create pollinator interference; bypassable routes tend to make the focal defence ineffective. The rule is recurrent and has survived a retrospective noncircularity stress test.

### 4. Existing studies already constrain different parts of the explanation

Trait factorials, consumer factorials, selective defence manipulations, observational trait interactions, and public-data reconstructions all exist, but mostly in different systems. This design fragmentation is a positive empirical result: it identifies the exact information already available and the smallest missing augmentation for each study.

### 5. The escape decision is formally easier than mechanism attribution

The strict escape condition is a sign question about total `Delta_AD W`. If a valid total interaction interval is entirely positive, the inequality is decided even while the compatible `(rho, iota, kappa)` allocations remain a plane or bounded set. The `classify_escape_criterion` helper in `trait_architecture/partial_identification.py` encodes exactly this distinction and does not infer a total interaction from channel-specific data.

### 6. The broadest deposited Impatiens fruit endpoint has now been checked

The public Soper Gorden & Adler *Impatiens capensis* panel was rerun against the fixed Dryad v4805 archive using the same hierarchical HC3 retrofit. In addition to the previously inspected CH-fruit and seed-per-CH-fruit components, the deposited `Total_Fruits_Per_Day` endpoint combines CH and CL fruit production.

For that broader fruit-production endpoint:

```text
A:D estimate = -0.1737
HC3 95% CI   = [-0.3791, +0.0316]
n             = 170
sign status   = CROSSES_ZERO
```

The randomized context modifiers `A:D:Robbing`, `A:D:Florivory`, and `A:D:Pollination` also all cross zero. This is a stronger endpoint-coverage result than the earlier component-only audit, but it remains observational in A and D and `Total_Fruits_Per_Day` is not total lifetime seed fitness. The full receipt is `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V2.md`.

### 7. A reconstructed CH+CL mature-seed-output sensitivity does not rescue the sign

The deposited table also contains mature CH/CL fruit rates and average seeds per CH/CL fruit. As a deliberately secondary sensitivity analysis, these quantities were combined at the individual-plant level as:

```text
estimated mature seed output per day
  = Mature_CH_Fruits_Per_Day * Average_Seeds_Per_CH_Fruit
  + Mature_CL_Fruits_Per_Day * Average_Seeds_Per_CL_Fruit
```

The same hierarchical HC3 model gives:

```text
A:D estimate = +0.1528
HC3 95% CI   = [-0.5487, +0.8544]
n             = 70
sign status   = CROSSES_ZERO
```

The point estimate reverses sign relative to the deposited total-fruit endpoint, but the interval is much wider and still crosses zero. This quantity is a **derived proxy**, not a deposited response and not lifetime fitness. It therefore cannot be promoted above the deposited endpoint; its value is diagnostic. The sign instability across plausible reproductive summaries strengthens the decision to stop mining nearby observational endpoints in this system rather than treating one favorable point estimate as escape evidence.

The machine-readable sensitivity receipt is `empirical/identification_design/IMPATIENS_RECONSTRUCTED_SEED_OUTPUT_SIGN_RECEIPT_V1.json`.

## Where the evidence stops

The present evidence does **not yet identify a positive escape event in one complete observed system**, but the reason is now more precise.

- The closest public observational trait-pair system has now been extended to the deposited CH+CL total-fruit endpoint. Its A×D estimate is negative in point value and its 95% interval crosses zero, so it does not supply a positive escape-sign anchor.
- A further derived CH+CL mature-seed-output sensitivity has a positive point estimate but a very wide interval spanning zero. It therefore does not rescue the sign, and because it is derived rather than deposited it has a lower claim ceiling.
- The `Impatiens` A and D traits are observational. Even an interval wholly above zero would have been an observational reproductive association rather than a causal `do(A) x do(D)` escape estimate.
- Kessler trait factorials are valuable channel-specific reproductive-service anchors, but they cannot be promoted to total `Delta_AD W` because antagonist loss and remaining cost are not on the same outcome surface.
- Consequently, no currently screened system supplies a defensible causal or randomized total `Delta_AD W` interval wholly above zero on the declared common reproductive scale. The escape sign remains `UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE` (legacy readout token: `UNRESOLVED_CURRENT_TOTAL_EVIDENCE`).
- Separately, no screened system point-identifies both `rho_delta` and `iota_delta` with the full selective crossed design, and no strict independent assay identifies `kappa_delta`. Mechanism allocation remains unresolved even if a future total interaction were positive.
- Zero recovered cost assays does not imply zero cost.

Thus the statement “escape is currently unresolved” remains correct, but **it must not be justified by saying that all three channels must first be point-identified**. A positive valid total interaction would decide the inequality; the full crossed consumer and cost design would then explain why it is positive.

## Hypothesis-by-hypothesis result

| Layer | Current result |
|---|---|
| One-trait conflict | Biological motivation and constituent A routes recovered; tested separately in SCH |
| Marginal antagonist reduction by D | Recurrent strong evidence |
| Pollinator-preserving selective defence | Recurrent, quantitative but still provisional across screened systems |
| Route-separation switching rule | Recurrent strong retrospective candidate |
| Observational broad fruit-production A×D | *Impatiens* `Total_Fruits_Per_Day`: -0.1737, HC3 CI [-0.3791, +0.0316], crosses zero |
| Derived mature-seed-output A×D | *Impatiens* CH+CL proxy: +0.1528, HC3 CI [-0.5487, +0.8544], n=70, crosses zero |
| Causal/valid total `Delta_AD W` | Sparse partial anchors; no positive interval on a manipulated common total outcome |
| Escape outcome `Delta_AD W > 0` | `UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE`; decidable from total sign without full allocation in principle |
| `rho_delta` and `iota_delta` allocation | Not point-identified in 0/16 screened systems |
| Independent `kappa_delta` | 0 strict estimates; documented evidence gap |
| Mechanism-resolved escape explanation | Not evaluable in current complete-system evidence |
| Experimental decision procedure | Achieved method result |

## Revised minimum augmentation

The empirical program is now naturally two-stage.

1. **Decide whether escape occurs.** Run or recover a defensible randomized/causal `A x D` factorial on one common reproductive outcome and propagate uncertainty for `Delta_AD W`. An interval wholly above zero identifies the strict escape inequality.
2. **Explain why it occurs.** Add selective antagonist and pollinator interventions, characterize `M0_delta`, test separability, and independently assay the remaining joint cost. These measurements allocate the positive or negative total interaction among `rho_delta`, `iota_delta` and `kappa_delta`.

The *Impatiens* upgrade now supplies a practical stopping rule: **do not spend the next development cycle constructing additional nearby observational reproductive summaries from the same panel**. The broad deposited endpoint crosses zero, the seed-output sensitivity also crosses zero and changes point sign, and A/D remain observational. The highest-value next empirical target is a genuinely manipulated A×D total reproductive surface.

This ordering prevents an unnecessarily strong mechanism gate from blocking a valid outcome-level result while preserving the stricter standard for causal explanation.

## Positive paper-level claim

> Nature repeatedly implements antagonist-reducing traits and selective route architectures that can preserve pollination. BITA separates two empirical questions that previous framing conflated: whether the attraction-by-defence fitness interaction is positive, which can be decided from a valid total fitness surface, and which relief, interference and cost channels generate that sign, which requires additional selective interventions and an independent cost assay. Reanalysis of the strongest public observational trait-pair system now includes its broader deposited CH+CL fruit-production endpoint plus a derived mature-seed-output sensitivity; both intervals cross zero and their point estimates differ in sign. Existing evidence therefore strongly recovers the constituent mechanisms and switching rule but does not yet provide a robust positive total interaction in a causally interpretable complete system.

This statement is stronger than “the mechanism was not identified” and narrower than claiming that defence has already been shown to release the one-trait conflict in a complete empirical system.
