# Physical floral-defence pollinator-follow-up gap audit v1

## Question

Can the current D-side macro corpus be expanded with additional **physical floral-defence studies that directly manipulate the focal defence and measure both antagonist and legitimate-pollinator responses in the same study**?

Frozen strict gate:

~~~text
same focal physical D
+ D manipulated or directly contrasted
+ antagonist response measured
+ legitimate pollinator / pollination response measured against the same D
+ independent primary study
~~~

Indirect evidence that the antagonist itself disrupts pollinators is biologically valuable but does not substitute for a direct D-to-pollinator contrast.

## Takeda, Kadokawa & Kawakita 2021 — slippery perianths

DOI: 10.1093/aob/mcaa168

Result supported by the primary study:

- slippery perianths reduce entry by nectar-thieving ants;
- experimental ant introduction into *Codonopsis lanceolata* flowers evicts hornet pollinators and shortens pollinator visit duration;
- fruit and seed set did not differ detectably between flowers with and without introduced ants.

Strict-gate adjudication:

~~~text
physical D -> antagonist: PASS
antagonist -> pollinator disruption: PASS
same physical D -> pollinator response: NOT DIRECTLY MANIPULATED
strict new matched-D increment: 0
~~~

The study itself identifies direct pollinator-choice tests of slipperiness as a needed future experiment.

## Sun & Huang 2015 — water-filled cupulate bracts in Pedicularis rex

DOI: 10.1093/aobpla/plv019

This is already admitted in BITA and therefore is not a new system.

The experiment drained the water-filled bracts and measured legitimate pollinators, nectar robbers, seed predation and reproduction. Legitimate pollinator visitation and nectar-robber visitation did not differ detectably between drained and intact flowers, whereas seed predation increased after drainage.

Adjudication:

~~~text
physical D -> seed antagonist: PASS
same physical D -> legitimate pollinator: NULL_COMPATIBLE
new strict increment: 0 (already in corpus)
~~~

This remains an important physical same-D null-compatible case.

## Carlson & Harms 2007 — water calyx in Chrysothemis friedrichsthaliana

DOI: 10.1098/rsbl.2007.0095

Draining the water calyx approximately doubled alucitid egg deposition / subsequent floral herbivory relative to intact water-filled calyces.

The paper discusses possible effects on other floral visitors but does not experimentally manipulate the water calyx and estimate legitimate pollinator response as the same-D outcome.

Adjudication:

~~~text
physical D -> floral herbivore: PASS
same physical D -> pollinator response: NOT MEASURED DIRECTLY
strict new matched-D increment: 0
~~~

## Tagawa 2018 — petal hairs in Menyanthes trifoliata

DOI: 10.1016/j.aspen.2018.09.006

Trimming petal hairs increased the success of nectar-thieving ants entering floral tubes; intact hairs also increased the time needed for ants to enter.

The study tests the ant barrier directly but does not provide a same-manipulation legitimate-pollinator outcome.

Adjudication:

~~~text
physical D -> nectar-thieving ant: PASS
same physical D -> pollinator response: NOT MEASURED DIRECTLY
strict new matched-D increment: 0
~~~

## Chautá et al. 2022 — floral stickiness in Bejaria resinosa

DOI: 10.1038/s41598-022-23261-2

Floral stickiness reduces florivore damage, and manipulating/removing stickiness affects fruit-set outcomes in a population-dependent way.

The source explicitly treats the possible cost to pollinators as unresolved and requiring a different experimental design. Trapped insects include potential pollinators, but this does not identify a direct D-to-pollination effect.

Adjudication:

~~~text
physical/sticky floral D -> florivory: PASS
fitness consequence: PRESENT
same D -> direct pollinator channel: UNRESOLVED
strict new matched-D increment: 0
~~~

## Targeted-search result

~~~text
new strict physical-D systems admitted: 0
existing physical null-compatible system confirmed: Pedicularis
high-value indirect bridge: Takeda 2021
physical D without direct pollinator follow-up: Chrysothemis, Menyanthes
pollinator trade-off unresolved: Bejaria
~~~

## Macro interpretation

The route-level corpus currently contains:

~~~text
physical D study programs: 7
physical programs with same-study D -> pollination follow-up: 2
chemical D study programs: 9
chemical programs with same-study D -> pollination follow-up: 7
~~~

Thus the current physical-versus-chemical difference in pollinator-follow-up coverage is best interpreted as a **measurement gap**, not as evidence that physical defences are biologically safer.

## Decisive future design

The most valuable missing experiment is a physical geometry/access manipulation in which the same focal D is crossed or graded while measuring:

1. antagonist entry/use;
2. legitimate pollinator entry, handling and/or pollen transfer;
3. bypass behaviour;
4. reproductive outcome;
5. more than one barrier intensity or geometry where feasible.

This experiment directly addresses the current empirical asymmetry without weakening the frozen same-D evidence gate.

## Source links

- Takeda et al. 2021: https://doi.org/10.1093/aob/mcaa168
- Sun & Huang 2015: https://doi.org/10.1093/aobpla/plv019
- Carlson & Harms 2007: https://doi.org/10.1098/rsbl.2007.0095
- Tagawa 2018: https://doi.org/10.1016/j.aspen.2018.09.006
- Chautá et al. 2022: https://doi.org/10.1038/s41598-022-23261-2
