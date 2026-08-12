# Pattern expansion completion gate v1

## Decision

**PASS — CURRENT MANUSCRIPT PATTERN EXPANSION SATURATED UNDER THE REGISTERED STOPPING RULE.**

This decision applies to the current Mechanism → Pattern paper. It does not claim exhaustive coverage of every floral mutualist–antagonist paper ever published.

## Registered stopping rule

`PATTERN_EXPANSION_PROTOCOL_V1.md` requires both:

1. two consecutive prioritized screening batches that add no new admissible mechanism × context × outcome Pattern class or materially change an existing class; and
2. no new quantitative synthesis that adds a distinct theory-facing Pattern axis.

Both conditions are now met.

## Condition 1 — two consecutive no-new-class batches

### Batch 8

`PRIORITY_RESCREEN_BATCH_8_V1.csv`

Distinct candidate set:

- *Jacaranda caroba* nectar robbery / pollinator response;
- *Caryopteris divaricata* corolla morphology / robber–pollinator partition;
- *Abronia fragrans* flower colour / site florivory context;
- *Cypripedium flavum* reinforcing pollinator / seed-predator selection.

Outcome:

```text
new admissible Pattern class: 0
new route-ledger system:       0
material change to a class:    0
```

Each candidate mapped onto an already represented class or failed the focal-trait contract.

### Batch 9

`PRIORITY_RESCREEN_BATCH_9_V1.csv`

Distinct candidate families:

- *Rhododendron ponticum* grayanotoxin / pollinator-guild filtering;
- *Toxicoscordion venenosum* toxic nectar / pollinator tolerance;
- non-*Acacia* ant-plant floral ant–pollinator conflict;
- additional nectar secondary-metabolite pollinator-filter literature.

Outcome:

```text
new admissible Pattern class: 0
new route-ledger system:       0
material change to a class:    0
```

The candidates map onto already represented consumer-role / pollinator-guild dependence, compound/dose context, guarded defence, or spatial/temporal filtering. No candidate justified broadening the definition of focal floral `D`.

Thus the consecutive-batch requirement is satisfied.

## Condition 2 — quantitative Pattern-axis saturation

`QUANTITATIVE_PATTERN_EXPANSION_SEARCH_V1.md` records five retained quantitative modules/axes:

1. Leal 2025 — realised floral-antagonist costs across reward, visitation, and female fitness;
2. Sasidharan 2023 — shared floral-signal tracking with consumer/compound dependence;
3. Haas-Desmarais 2026 — tissue/damage-mode and natural/simulated herbivory dependence across 171 studies / 1,348 cases;
4. Caruso 2019 — selection-agent, floral-trait-class and pollinator-guild dependence;
5. Junker & Blüthgen 2010 — consumer-dependency filtering of floral-scent responses.

Additional targeted searches did not expose a sixth quantitative synthesis that changed the theory-facing Pattern architecture.

Outcome:

```text
new distinct quantitative Pattern axis: 0
quantitative stop condition:          PASS
```

## Expansion yield

The expansion did not simply increase publication count. It added independent biological systems only when a source passed the focal trait / route / independence rules.

Current provisional route-ledger architecture on this branch:

```text
records:                         56   (canonical 38)
independent biological clusters: 25   (canonical 14)
A -> pollination clusters:         5   (canonical 4)
A -> antagonism clusters:          8   (canonical 5)
D -> antagonism clusters:         18   (canonical 10)
D -> pollination clusters:        10   (canonical 7)
same-system multi-route clusters: 14   (canonical 10)
context/sign-switch clusters:     17   (canonical 11)
```

Route counts overlap by study and are not additive independent-study totals.

Seven context-only programs are intentionally excluded from route-ledger N.

## Biological dimensions added by the expansion

### A-side generality

New independent signal systems extend `A -> antagonism` beyond the original scent-heavy architecture:

- visual showy bracts in *Dalechampia*;
- petal colour in *Raphanus*;
- recombinant flower colour + scent axes in *Silene*.

### Flower-specific physical D

Independent mechanisms now include:

- water-filled bract (*Pedicularis*);
- floral stickiness (*Bejaria*, *Erica*);
- slippery epicuticular wax (*Codonopsis/Fritillaria*);
- petal hairs (*Menyanthes*);
- spur-enclosing bract (*Thunia*);
- water calyx (*Chrysothemis*).

This increases mechanism diversity rather than repeating one chemical defence.

### Chemical guarded state

*Catalpa* nectar iridoids independently show strong thief deterrence with no detected reduction in tested legitimate-pollinator reward consumption.

### Consumer-role conditionality

The expansion adds distinct ways in which consumer function changes:

- antagonist attack-mode bypass (*Pedicularis*);
- field vs grasshopper vs snail response (*Bejaria*);
- thief vs legitimate pollinator response (*Catalpa*);
- same adult consumer acting as pollinator and florivore (*Anemone*);
- same *Bombus* routed between legitimate pollination and robbery by bract state (*Thunia*);
- adult pollinator vs larval seed predator in the same *Hadena* lifecycle (*Silene stellata*).

### Spatial / temporal / functional routing

New sources show that floral defence can alter where, when, or how interactions occur rather than simply lowering visitor abundance:

- Acacia/Vachellia ant-repellence during the reproductive window;
- body-size/access filtering by slippery perianths;
- petal-hair locomotion barriers;
- bract-mediated pollinator-vs-robber routing in *Thunia*.

## Central Pattern after expansion

The expansion strengthens, rather than changes, the central conclusion:

> **Constituent attraction and defence mechanisms recur across chemically and physically distinct floral systems, but their realized balance depends on consumer identity, attack mode, trait expression, resource/tissue context, spatial or temporal filtering, and response stage.**

The broader evidence therefore supports:

> **recurrent mechanism + context-dependent balance**

and still does **not** support a universal positive or negative sign of `W_AD`.

## Identification gaps remain intentionally open

The expansion does not change the strongest inference boundary:

```text
direct A x D strict evidence:   1 canonical cluster, sign unresolved
direct joint-cost estimates:    0 strict estimates
kappa:                          unidentified, not zero
```

No marginal, context, or meta-analytic result is used to manufacture either missing quantity.

## Merge/adoption rule

This expansion branch is ready for review against the canonical manuscript branch, but its provisional counts must not silently replace canonical manuscript numbers.

Next step:

1. validate expansion CI/readout;
2. open a draft PR from `analysis/pattern-expansion-v1` into `agent/mechanism-pattern-universality-v1`;
3. review the expanded Figure 3 / Table 3 / Part II narrative impact;
4. only then promote selected expansion files/counts into the canonical submission package.

### Final state

```text
source-level expansion stopping gate: PASS
quantitative Pattern-axis gate:       PASS
inference-boundary gate:              PASS
current expansion status:             COMPLETE_FOR_REVIEW
canonical manuscript updated:         NO
```
