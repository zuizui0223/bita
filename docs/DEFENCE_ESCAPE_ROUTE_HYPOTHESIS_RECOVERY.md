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

The strict escape condition is a sign question about total `Delta_AD W`. If a valid total interaction interval is entirely positive, the inequality is decided even while the compatible `(rho, iota, kappa)` allocations remain a plane or bounded set. The new `classify_escape_criterion` helper in `trait_architecture/partial_identification.py` encodes exactly this distinction and does not infer a total interaction from channel-specific data.

## Where the evidence stops

The present evidence does **not yet identify a positive escape event in one complete observed system**, but the reason is now more precise.

- Total `A x D` reproductive-outcome anchors are sparse. The `Impatiens` reconstruction remains the cleaner total candidate, but its interaction confidence intervals cross zero and component point signs differ.
- Kessler trait factorials are valuable channel-specific reproductive-service anchors, but they cannot be promoted to total `Delta_AD W` because antagonist loss and remaining cost are not on the same outcome surface.
- Consequently, no currently screened system supplies a defensible total `Delta_AD W` interval wholly above zero on the declared common reproductive scale. The escape sign is therefore `UNRESOLVED_CURRENT_TOTAL_EVIDENCE`.
- Separately, no screened system point-identifies both `rho_delta` and `iota_delta` with the full selective crossed design, and no strict independent assay identifies `kappa_delta`. Mechanism allocation remains unresolved even if a future total interaction were positive.
- Zero recovered cost assays does not imply zero cost.

Thus the statement “escape is currently unresolved” remains correct, but **it must not be justified by saying that all three channels must first be point-identified**. A positive total interaction would decide the inequality; the full crossed consumer and cost design would then explain why it is positive.

## Hypothesis-by-hypothesis result

| Layer | Current result |
|---|---|
| One-trait conflict | Biological motivation and constituent A routes recovered; tested separately in SCH |
| Marginal antagonist reduction by D | Recurrent strong evidence |
| Pollinator-preserving selective defence | Recurrent, quantitative but still provisional across screened systems |
| Route-separation switching rule | Recurrent strong retrospective candidate |
| Total `Delta_AD W` | Sparse partial anchors; sign unresolved on a valid common total outcome |
| Escape outcome `Delta_AD W > 0` | `UNRESOLVED_CURRENT_TOTAL_EVIDENCE`; decidable from total sign without full allocation in principle |
| `rho_delta` and `iota_delta` allocation | Not point-identified in 0/16 screened systems |
| Independent `kappa_delta` | 0 strict estimates; documented evidence gap |
| Mechanism-resolved escape explanation | Not evaluable in current complete-system evidence |
| Experimental decision procedure | Achieved method result |

## Revised minimum augmentation

The empirical program is now naturally two-stage.

1. **Decide whether escape occurs.** Run or recover a defensible randomized/causal `A x D` factorial on one common reproductive outcome and propagate uncertainty for `Delta_AD W`. An interval wholly above zero identifies the strict escape inequality.
2. **Explain why it occurs.** Add selective antagonist and pollinator interventions, characterize `M0_delta`, test separability, and independently assay the remaining joint cost. These measurements allocate the positive or negative total interaction among `rho_delta`, `iota_delta` and `kappa_delta`.

This ordering prevents an unnecessarily strong mechanism gate from blocking a valid outcome-level result while preserving the stricter standard for causal explanation.

## Positive paper-level claim

> Nature repeatedly implements antagonist-reducing traits and selective route architectures that can preserve pollination. BITA separates two empirical questions that previous framing conflated: whether the attraction-by-defence fitness interaction is positive, which can be decided from a valid total fitness surface, and which relief, interference and cost channels generate that sign, which requires additional selective interventions and an independent cost assay. Existing evidence strongly recovers the constituent mechanisms and switching rule but does not yet provide a robust positive total interaction in a complete system.

This statement is stronger than “the mechanism was not identified” and narrower than claiming that defence has already been shown to release the one-trait conflict in a complete empirical system.