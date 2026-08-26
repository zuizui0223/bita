# Partial-identification frontier v1

## Status

This is an exploratory recovery layer for the canonical identification-design paper. It does **not** change the current Main claim set yet.

The current manuscript makes a sharp binary distinction between a total `A×D` interaction and full channel identification. The next recoverable result is to insert a mathematically explicit middle layer: **partial identification**.

## 1. Identified set from the total interaction

The discrete bookkeeping relation is

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

If only `Delta_AD W = delta` is observed, the channel allocation belongs to the set

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}.
```

This is a two-dimensional plane in three-dimensional channel space. An arbitrarily large sample of the same total four-cell `A×D` surface cannot collapse that plane to a point. This makes the manuscript's structural non-identifiability geometrically explicit.

The implementation in `trait_architecture/partial_identification.py` intersects this plane with caller-declared channel bounds and returns the exact coordinate projections of the feasible set.

## 2. The old one-sided inequality becomes a partial-identification bound

Suppose the oriented channels are constrained to be nonnegative:

```text
rho_delta >= 0
iota_delta >= 0
kappa_delta >= 0.
```

For a positive observed total interaction `delta > 0`, the identified set implies

```text
rho_delta >= delta.
```

But `rho_delta`, `iota_delta`, and `kappa_delta` are still not point identified and rho has no finite upper bound without additional information.

This is a stronger interpretation of the historical one-sided result: it is not a prediction theorem about nature; it is a **sharp bound on the channel allocation under explicit sign restrictions**.

## 3. Every additional measurement shrinks the identified set

Examples:

1. **Total interaction only**
   - identified set: unbounded plane;
   - no channel sign is generally identified.

2. **Total interaction + sign restrictions**
   - converts some claims into one-sided bounds;
   - still does not allocate the interaction.

3. **Total interaction + bounded independent cost assay**
   - restricts the feasible rho/iota balance;
   - does not require pretending the cost is known exactly.

4. **Total interaction + selective estimate/bound for one consumer channel**
   - shrinks the other channel's feasible interval;
   - can sign-identify a missing channel before full point identification.

5. **Crossed A×D×G×P + M0 handling + separability**
   - point-identifies rho and iota under the declared causal gates;
   - leaves the joint residual unallocated.

6. **Independent A×D joint-cost assay on a commensurate scale**
   - closes the allocation if the assay is validated as the same remaining channel.

Thus the relevant scientific object is an **identification frontier**, not a binary identified/unidentified label.

## 4. What this adds to the 16-system audit

The current high-information matrix already contains orthogonal fragments of this frontier:

- Kessler et al. 2008 reaches a direct discrete trait interaction but lacks crossed selective consumer toggles and has a systemic-D caveat.
- Soper Gorden & Adler 2018 reaches observational total interaction plus randomized context modification, but not selective channel isolation.
- Egan et al. 2021 reaches a strong consumer-factorial design while the focal A/D traits are not independently crossed and D is leaf-derived.
- Sun & Huang 2015 supplies a selective physical-defence system anchor but no A manipulation.
- across the 16-system screened set, `M0_delta` is not identified and an independent joint-cost assay is absent.

The stronger synthesis is therefore not only

```text
full identification = 0.
```

It is:

```text
existing studies occupy different, complementary faces of the identification set,
but none closes all dimensions of the allocation problem.
```

That statement turns the coverage matrix into a **design-fragmentation pattern** rather than a list of near misses.

## 5. Minimum-augmentation question

For every existing study, the next useful question becomes:

```text
What is the smallest additional intervention or measurement that most shrinks the identified set?
```

Examples:

- Kessler 2008: resolve D scope, then add selective consumer interventions; M0 and independent cost remain separate gates.
- Impatiens 2018: trait randomization and selective consumer exclusions are more informative than another observational interaction term.
- Egan 2021: experimentally cross biologically valid floral A and D on the existing consumer-factorial backbone.
- Pedicularis: add an independent attraction manipulation to the selective-D system, then construct true consumer toggles if biologically feasible.

A future audit can encode these as design components rather than assign an arbitrary single scalar score.

## 6. Relation to broader causal-inference work

This extension should be positioned carefully rather than claimed as the invention of causal identification.

Relevant adjacent work includes:

- Vansteelandt & Daniel 2017, *Epidemiology*, doi:10.1097/EDE.0000000000000596 — interventional effects for multiple mediators and weaker identification assumptions than natural effects;
- Egami & Imai 2019, *JASA*, doi:10.1080/01621459.2018.1476246 — causal interaction estimands in factorial experiments;
- Correia, Dee & Ferraro 2025, *Biological Reviews*, doi:10.1111/brv.70011 — explicit design and identification requirements for causal mediation in ecology.

The defensible paper-specific novelty would be narrower:

> an interaction-specific ecological identification architecture that links a measurable trait interaction, multiple biotic channels, crossed consumer interventions, an internal four-way model-structure diagnostic, a non-zero pollinator-absent baseline, an independent joint-cost assay, and a cross-system design-coverage frontier.

## 7. Recommended manuscript recovery

Highest-value addition, if validation remains clean:

1. add a short Main subsection defining `I(delta)` and the identification frontier;
2. reinterpret the historical sign result as a partial-identification bound;
3. turn the 16-system coverage result from `full identification = 0` into a design-fragmentation / minimum-augmentation result;
4. keep numerical study-specific bounds out of Main unless source-derived uncertainty or biologically justified bounds are available;
5. place detailed identified-set algebra and sensitivity examples in Appendix S1.

This would deepen the conclusion without resuming broad literature accumulation or claiming channel values that the current evidence cannot support.
