# Critical appraisal: is the Part B pivot correct?

## Verdict

The pivot — from identifying the mixed partial in a joint panel (proof) to pooling
the four marginal arrows separately and composing them through the Part A
expression (support) — is **methodologically sound and clearly superior to the
collapsed proof route for making any empirical progress**. It is correctly scoped
and honestly labelled. It has four genuine limitations that must stay visible; none
invalidates it, and the docs already encode most of them.

## Why it is sound

1. **The theorem is premises -> conditional sign.** Part A derives that
   `sign(∂²W/∂A∂D)` is fixed by the four channel terms and `c_AD`. Supporting the
   premises (the arrows) and the functional form is a valid way to support a
   conditional claim; you need not measure a compound quantity whose components and
   composition rule are known.
2. **The four marginal literatures are mature and independent.** attraction->visitation,
   attraction->florivory, barrier->florivory, barrier->access each have their own
   substantial literature. Pooling within a scale/design class is standard
   meta-analysis; counting independence per arrow is the correct fix for the
   joint-panel collapse (17,933 -> 0).
3. **It does not overclaim.** It is declared support, not proof; `c_AD` is bounded
   (B4), never estimated; B4 is a declared sensitivity map; contrary signs are
   findings, never recoded.

## Genuine limitations (keep visible)

### L1 — Cross-system composition, not within-system prediction
The empirically informed regime map assembles marginal effects measured in
**different** systems. It is therefore a "typical/assembled" statement, exposed to
cross-system confounding (systems where `d_A` is measured may differ systematically
from those where `c_D` is measured). It is a plausibility synthesis, not a
prediction about any one plant. Mitigation: keep the within-system claim as the job
of the Part III/IV joint panels, and lean on B3 moderators to make the
context-dependence explicit rather than averaged away.

### L2 — The scale bridge is unresolved (calibration relocated, not dissolved)
Converting a log-odds-ratio or standardized slope into the dimensionless
`b_A, d_A, e_F, c_D` needs a declared, defensible calibration
(`parameter_envelopes` contracts are all `awaiting_synthesis`/null). Until that
exists, B4's "empirical" regime map is **sensitivity-grade**, using declared channel
values — the same calibration wall as before, now isolated to one clean step. The
pivot makes the problem smaller and explicit; it does not remove it.

### L3 — "Arrow-level" mixes sub-constructs
The two `d_A` anchors are visual-display (Impatiens, standardized beta) and scent
(Gymnadenia, log-odds-ratio): different trait classes **and** different scales. They
inform the arrow's sign but are not poolable together. So the B5 "sign conflict" may
be **trait-class moderation** (visual vs scent) as much as system or generalization.
Consequence: the B3 moderator set should not be limited to
`pollination_generalization`; a `trait_class` (visual/scent/reward) contrast is an
equally motivated conditionality axis and should be pre-registered too.

### L4 — Agent-of-selection seeds are not marginal d_A effects
Caruso et al. 2019 (`10.1111/evo.13639`) reports **selection gradients** for
herbivores vs pollinators on floral traits. A herbivore-mediated selection gradient
on flower size is *not* a `flower size -> florivory` effect; it is how herbivores
reshape the trait-fitness relationship. So such meta-analyses seed candidate
**systems**, not drop-in `d_A` rows — the trait->antagonism estimate must come from
the underlying primary study. Conflating the two would violate the arrow's estimand.

## Consequences for the plan

- Keep the two-part framing and the support-not-proof language exactly as is.
- Add a `trait_class` moderator hypothesis alongside `pollination_generalization`
  (L3), so the `d_A` conflict is tested against both explanations.
- Treat agent-of-selection meta-analyses (Caruso, Moreira) as **system seeds**, and
  extract the marginal `d_A` effect from the primary study, never from the gradient
  (L4).
- Prioritise the scale-bridge calibration (L2) as the gate that upgrades B4 from
  sensitivity to empirical — it is now the single most valuable unblocker after the
  `d_A` data.

## Bottom line

The pivot is correct: it is the honest, tractable way to give the theorem
real-world support, and it is already scoped so its limitations are stated rather
than hidden. The work to do is not to re-litigate the strategy but to (1) resolve
the `d_A` conflict with both a generalization and a trait-class moderator, (2)
declare the effect->parameter scale bridge, and (3) keep every composed result
labelled as cross-system support, not within-system proof.
