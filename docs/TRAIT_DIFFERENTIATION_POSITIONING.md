# Trait differentiation literature positioning

## Why this audit matters

The SCH/BITA Chapter 2 reframe moves BITA into a mature theoretical literature on functional specialization, division of labor, modularity and the evolution of reduced pleiotropy. The paper must therefore avoid claiming that the general idea of resolving a multifunctional trade-off by specialization is new.

## Closest prior theory

### Rueffler, Hermisson & Wagner 2012

**Evolution of functional specialization and division of labor.** PNAS 109:E326–E335. DOI: 10.1073/pnas.1110521109.

This is the closest conceptual predecessor. It starts from undifferentiated modules that contribute to two tasks under a trade-off and asks when functionally specialized modules are favoured. It identifies general conditions involving positional effects, accelerating performance functions and synergistic interactions.

Implication for BITA:

```text
NOT NOVEL:
trade-offs can favour division of labor / functional specialization

POSSIBLE BITA CONTRIBUTION:
connect a measured one-trait ecological compromise to an explicit
shared-vs-differentiated architecture comparison, then show what
experimental information is required to identify the ecological
channels once differentiated trait axes exist
```

### Guillaume & Otto 2012

**Gene Functional Trade-Offs and the Evolution of Pleiotropy.** Genetics 192:1389–1409. DOI: 10.1534/genetics.112.143214.

This work models how genes contributing to two functions evolve toward pleiotropy or specialization depending on the shape of functional trade-offs and the mapping from trait functionality to fitness. It also treats duplication/subfunctionalization.

Implication for BITA:

Do not claim novelty for the statement that strong functional trade-offs can favour specialization or reduced pleiotropy.

### Sack & Buckley 2020

**Trait Multi-Functionality in Plant Stress Response.** Integrative and Comparative Biology 60. DOI: 10.1093/icb/icz152.

This framework emphasizes that single traits commonly serve multiple functions and may therefore be optimized for multiple functions rather than for any one function alone.

Implication for SCH/BITA:

This is a useful conceptual bridge for Chapter 1: a multifunctional trait can sit away from any single-function optimum because its realized state reflects several functions simultaneously.

## Defensible programme-level novelty

The strongest non-overlapping position is not a new general theory of specialization. It is a **three-layer bridge**:

```text
1. BALANCE / SCH
   identify and characterize a real ecological trade-off on one trait axis

2. ARCHITECTURE / BITA theory
   ask whether the measured compromise can be improved by allocating
   the conflicting functions across differentiated trait axes

3. IDENTIFICATION / BITA empirical design
   once two axes exist, distinguish total cross-trait interaction from
   the ecological channels that generated the apparent release
```

The mature BITA identification work is important here. General specialization theory predicts when differentiation may be favoured, but it does not by itself tell an empiricist how to determine which ecological channel generated a measured interaction between the resulting traits.

## Role of the quadratic baseline

The new `trait_architecture/differentiation.py` model should be presented as an **operational baseline tailored to the SCH/BITA programme**, not as the first mathematical demonstration that specialization can beat a multifunctional compromise.

Its value is that it gives the chapter a directly interpretable measurable boundary:

```text
recoverable fitness loss from the shared compromise
>
additional architecture + residual coupling cost
```

and interfaces cleanly with the existing BITA two-trait mechanism-identification module.

## Reviewer-risk language

Avoid:

- “We provide the first general theory of trait differentiation.”
- “We show for the first time that trade-offs drive specialization.”
- “Division of labor emerges when specialization benefits exceed costs” as a standalone novelty claim.

Prefer:

- “Building on general theory of multifunctionality and functional specialization, we formulate the balance-to-differentiation transition on the same trait coordinates used by an empirical ecological conflict.”
- “Our contribution is to connect architecture choice to mechanism identification: a differentiated two-trait phenotype can relieve a shared-trait compromise without revealing which ecological channel produced that relief.”
- “The framework converts a general specialization idea into an explicit empirical sequence from shared-axis balance, through architecture gain, to channel-resolved tests.”

## Immediate manuscript consequence

The Introduction should cite the specialization/modularity literature before presenting `Delta_arch`. The first novelty paragraph should then pivot to the empirical inference gap rather than implying that the shared-versus-specialized architecture comparison is itself unprecedented.
