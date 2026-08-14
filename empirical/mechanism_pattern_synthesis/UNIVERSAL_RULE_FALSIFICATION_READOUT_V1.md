# Universal-rule falsification readout v1

## Status

This is a **retrospective falsification pass**, not the final universality claim. It compares the leading effective-domain separation rule against three simpler alternatives on a deliberately mixed set of supporting, switching, and failure cases already admitted or audited in the project.

## Competing rules

- `R0`: one universal attraction-defence sign.
- `R1`: D strength alone determines the state.
- `R2`: implementation class (chemical vs physical) determines selectivity.
- `R3`: effective-domain separation determines whether antagonist relief is obtained without pollinator interference; overlap causes interference, bypass/tolerance causes D-channel failure.

## Case comparison

| System | Implementation | Exposure architecture coded from source mechanism | Observed state | R0 | R1 | R2 | R3 |
|---|---|---|---|---|---|---|---|
| Catalpa | chemical iridoid | thieves strongly exposed/sensitive; tested legitimate bees weakly affected | antagonist use down, legitimate consumption ~null | fail as universal sign | insufficient | chemical class alone cannot predict | **match: consumer separation** |
| Polemonium | chemical volatile | antagonist and pollinator thresholds converge as dose rises | moderate guarded state -> high-dose pollinator cost | fail | partly explains dose transition but not why thresholds differ | same chemical class contains both states | **match: window closes with exposure** |
| Aconitum | chemical alkaloid | robber response threshold lower than legitimate-pollinator threshold | selective low/intermediate window; pollinator cost at high concentration | fail | partly | same class contains state switch | **match: threshold separation** |
| Pedicularis | physical water barrier | seed-predator attack route crosses barrier; robber/pollinator can bypass/avoid that route | seed predation down; tested robber/pollinator visitation ~null | fail | no | physical class alone not sufficient | **match: attack-route separation** |
| Thunia | physical bract | same Bombus can enter different functional modes depending on access geometry | robbery down while legitimate pollen transfer/fruit set maintained or increased | fail | no | physical class alone not sufficient | **match: functional-mode separation/routing** |
| Codonopsis | physical wax | ant approach surfaces slippery; pollinator foothold is a non-slippery basal zone | ant access reduced while legitimate hornet foothold retained | fail | no | physical class alone not sufficient | **match: spatial separation** |
| Chrysothemis | physical water calyx | ovipositing moth attacks pre-anthesis bud through liquid barrier; pollination occurs after anthesis | specialist oviposition/herbivory reduced; other visitors can bypass | fail | no | physical class alone not sufficient | **match: developmental-time + attack-route separation** |
| Bejaria | physical sticky surface | insect visitors in both antagonist and mutualist roles contact broad sticky surface | strong florivore defence but broad insect exclusion / no clean guarded state | fail | no | **contradicts 'physical=selective'** | **match: overlapping domain** |
| Salvia boundary audit | physical calyx/access | robber can bite exposed corolla and bypass candidate barrier | candidate anti-robber D channel not demonstrated | n/a | no | physical class does not guarantee efficacy | **match: bypass -> channel failure** |
| Rivest Lupinus boundary audit | chemical pollen alkaloid | candidate consumers show tolerance or antagonist role is not cleanly established | defence-like chemistry does not yield clean focal D->antagonist effect | n/a | no | chemical class does not guarantee efficacy | **match: tolerance / failed D gate** |
| Kessler 2015, M. sexta | floral scent A x nectar-restriction D | same species is pollinator and ovipositing antagonist; nectar and scent strongly affect its pollination and oviposition decisions | source-mean crossed A x D sign negative | universal sign contradicted by Hyles | strength alone cannot explain consumer reversal | not a chemical-vs-physical contrast | **match: strong consumer-domain overlap** |
| Kessler 2015, H. lineata | same A and D manipulations | pollinator tolerates loss of either scent or nectar singly; antagonist-reduction role of nectar restriction is established through M. sexta | source-mean crossed A x D sign positive | universal sign contradicted by M. sexta | same D level, different sign | same implementation, different sign | **match: pollinator-side D sensitivity reduced / domains more separable** |

## What is actually falsified

### R0 — one universal sign

Rejected as a useful general rule. The same Kessler 2015 crossed floral architecture changes the descriptive discrete A-by-D sign between M. sexta and H. lineata. Marginal systems also contain guarded, interfering, and failed-D states.

### R1 — defence strength alone

Insufficient. Dose/exposure explains some within-system switches (Polemonium, Aconitum), but the same nominal trait manipulation can yield different states across consumers, attack routes, spatial zones, or visitor functions. Kessler 2015 is particularly damaging to a strength-only explanation because the trait manipulation is fixed while pollinator identity changes the crossed sign.

### R2 — chemical versus physical implementation

Rejected as the main rule. Both chemical and physical classes contain selective and non-selective/failure states. Codonopsis and Bejaria are both physical but differ in domain breadth; chemical systems likewise move between guarded and interfering states with dose or consumer identity.

### R3 — effective-domain separation

Survives this retrospective challenge set better than R0-R2. It explains:

- guarded states via consumer, attack-route, spatial, temporal, or functional separation;
- interference states via overlap;
- failed D states via bypass/tolerance;
- a direct crossed-factorial sign reversal when consumer-specific dependence changes under fixed A/D manipulations.

## Important limitation

This pass is not independent prediction because R3 was developed while inspecting many of these systems. Good retrospective compression is necessary but not sufficient evidence of a universal law.

Therefore the conclusion is **not yet final**.

## Next decisive test: out-of-set challenge

Register an independent challenge batch of systems not used to formulate R3. For each candidate source:

1. code antagonist and pollinator effective domains from methods/mechanism descriptions before recording focal outcome signs;
2. predict one of `guarded`, `overlap/interference`, `bypass/failure`, or `unresolved`;
3. reveal/record outcomes only after prediction coding;
4. score prediction agreement and contradictions;
5. require representation from both chemical and physical implementations and at least two consumer guilds.

Do not promote R3 to the final paper conclusion until this out-of-set challenge is completed or until a transparent reason shows that an independent challenge set cannot be assembled from existing literature.
