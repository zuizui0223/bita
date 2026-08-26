# Partial-identification frontier v1

## Status

This is an exploratory recovery layer for the canonical identification-design paper. It does **not** change the current Main claim set yet.

The current manuscript makes a sharp distinction between a total `A×D` interaction and full channel identification. The recoverable middle layer is **partial identification**: incomplete studies can restrict the feasible channel allocation even when they cannot point-identify every channel.

## 1. Identified set from the total interaction

The discrete bookkeeping relation is

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

If only `Delta_AD W = delta` is observed, the channel allocation belongs to

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}.
```

This is a two-dimensional plane in three-dimensional channel space. An arbitrarily large sample of the same total four-cell `A×D` surface cannot collapse that plane to a point. The obstacle is therefore structural information, not sampling precision.

The implementation in `trait_architecture/partial_identification.py` intersects this plane with caller-declared channel bounds and returns exact coordinate projections of the feasible set.

## 2. The historical one-sided result is a biotic-balance bound

A sharper recovery does **not** require assuming that rho and iota themselves are nonnegative. From

```text
rho_delta - iota_delta = delta + kappa_delta,
```

any bound on the joint-cost channel maps one-to-one to a bound on the biotic balance `rho_delta - iota_delta`.

In particular, if

```text
kappa_delta >= 0,
```

then

```text
rho_delta - iota_delta >= delta.
```

For a positive observed total interaction,

```text
delta > 0,
```

this forces

```text
rho_delta - iota_delta >= delta > 0.
```

Thus antagonist relief must exceed pollinator interference by at least the observed total interaction on the declared scale, even though rho and iota can remain individually unbounded. This is the clean partial-identification interpretation of the historical one-sided inequality. It is a **sharp bound on a channel contrast under an explicit kappa restriction**, not a standalone prediction theorem about nature.

Additional sign restrictions can sharpen individual coordinates. For example, if rho, iota and kappa are all constrained nonnegative and `delta > 0`, then `rho_delta >= delta`; that stronger coordinate claim requires the extra rho/iota sign assumptions and should not be conflated with the historical kappa-only result.

## 3. Every additional measurement shrinks the identified set

The information sequence is:

1. **Total interaction only**
   - identified set: an unbounded plane;
   - individual channels and the biotic balance are generally unbounded.

2. **Total interaction + a kappa sign/bound**
   - directly bounds `rho_delta - iota_delta`;
   - `kappa_delta >= 0` and positive `delta` force a positive biotic balance;
   - rho and iota can still be individually unbounded.

3. **Total interaction + bounded independent cost assay**
   - narrows the biotic-balance interval exactly by the same amount;
   - does not require pretending the cost is known without uncertainty.

4. **Total interaction + a selective estimate/bound for one consumer channel**
   - shrinks the other consumer channel and/or kappa projection;
   - can sign-identify a missing contrast before full point identification.

5. **Crossed A×D×G×P + M0 handling + separability**
   - point-identifies rho and iota under the declared causal gates;
   - leaves the joint residual unallocated.

6. **Independent A×D joint-cost assay on a commensurate scale**
   - closes the allocation if the assay is validated as the same remaining channel.

The scientific object is therefore an **identification frontier**, not a binary identified/unidentified label.

## 4. What this adds to the 16-system audit

The current high-information matrix already contains orthogonal fragments of this frontier:

- Kessler et al. 2008 reaches a direct discrete trait interaction but lacks crossed selective consumer toggles and has a systemic-D caveat.
- Soper Gorden & Adler 2018 reaches observational total interaction plus randomized context modification, but not selective channel isolation.
- Egan et al. 2021 reaches a strong consumer-factorial design while the focal A/D traits are not independently crossed and D is leaf-derived.
- Sun & Huang 2015 supplies a selective physical-defence system anchor but no A manipulation.
- across the 16-system screened set, `M0_delta` is not identified and an independent joint-cost assay is absent.

The stronger synthesis is not only

```text
full identification = 0.
```

It is:

```text
existing studies occupy different, complementary faces of the identification problem,
but none closes all dimensions of the allocation problem.
```

That turns the coverage matrix into a **design-fragmentation pattern** rather than a list of near misses.

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

These should remain design-component statements rather than an arbitrary scalar score.

## 6. Relation to broader causal-inference work

This extension should be positioned carefully rather than claimed as the invention of causal or partial identification.

Relevant adjacent work includes:

- Vansteelandt & Daniel 2017, *Epidemiology*, doi:10.1097/EDE.0000000000000596 — interventional effects for multiple mediators;
- Egami & Imai 2019, *JASA*, doi:10.1080/01621459.2018.1476246 — causal interaction estimands in factorial experiments;
- Correia, Dee & Ferraro 2025, *Biological Reviews*, doi:10.1111/brv.70011 — design and identification requirements for causal mediation in ecology.

The defensible paper-specific contribution is narrower:

> an interaction-specific ecological identification architecture that links a measurable trait interaction, partial bounds on mechanistic contrasts, multiple biotic channels, crossed consumer interventions, an internal four-way model-structure diagnostic, a non-zero pollinator-absent baseline, an independent joint-cost assay, and a cross-system design-coverage frontier.

## 7. Recommended manuscript recovery

Highest-value Main-text addition, if packaging remains clean:

1. define `I(delta)` in one short paragraph after structural non-identifiability;
2. recover the historical result as `kappa_delta >= 0 => rho_delta - iota_delta >= Delta_AD W`;
3. describe existing studies as occupying complementary faces of an identification frontier;
4. end with minimum augmentation: which next measurement shrinks the identified set most;
5. keep numerical study-specific channel bounds out of Main unless they are source-derived or biologically justified;
6. place projection algebra and worked sensitivity examples in Appendix S1.

This deepens the conclusion without resuming broad literature accumulation or inventing channel values that the current evidence cannot support.
