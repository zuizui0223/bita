# BITA Peucedanum field execution and permission gate v1

## Current programme status

The strongest Japan-accessible BITA execution candidate is the andromonoecious alpine herb `Peucedanum multivittatum` (ハクサンボウフウ).

The current status must be split into two independent statements:

```text
BIOLOGICALLY_READY_FOR_TECHNICAL_PILOT
!=
ADMINISTRATIVELY_READY_FOR_FIELD_MANIPULATION.
```

The biological design, common-support gate, technical-pilot receipt, causal Stage-A experiment, randomized Stage-B q x G experiment and attrition-aware analysis are implemented.

Field manipulation must not begin until the administrative gate is independently closed.

## Field-site priority

### Priority 1 — HA, Taisetsu Mountains

HA is the strongest first technical-pilot site because the published programme has already demonstrated there:

- severe recurrent predispersal seed predation,
- a dense 7 m x 7 m focal patch,
- 106 tagged flowering plants in the 2021 focal experiment,
- predator-egg census after flowering,
- removal of all recorded eggs with forceps before hatching,
- initial and final fruit accounting,
- leaf sampling and genetic paternity analysis,
- short pollen dispersal compatible with a spatially compact paternity design.

Thus HA has direct precedent for the most operationally difficult existing component of the experiment: egg census/removal and reproductive follow-up.

### Priority 2 — HL

HL is the first biological replication/backup because the 2025 study also classified it among the early-flowering populations with severe predation and a saturating female gain curve.

### Priority 3 — other early Taisetsu populations

PK and KE remain candidate backups for the high-predation regime, but the same depth of egg-removal/paternity precedent has not been recovered for them.

### Late populations

Late populations are useful low-antagonism natural controls / geographic validation systems. They are not preferred sites for the first randomized antagonist experiment because the central causal treatment requires a strong natural predator-pressure contrast.

## Phenological field window

The biological sequence recovered from the primary literature is:

```text
snowmelt
-> vegetative/flowering census
-> terminal-umbel male phase
   perfect and male flowers overlap for roughly 4-5 days
-> stamens shed from perfect flowers
-> pistils elongate / female transition
-> predator oviposition commonly occurs during the female stage
-> initial fruit production
-> larval predation
-> fruit maturation roughly two weeks after flowering.
```

The 2021 Taisetsu study reports flowering from mid-July to late August depending on snowmelt and a major moth oviposition period from mid- to late July at the study site.

For Stage B, the narrow critical workflow is therefore:

```text
male phase complete
-> identify perfect vs male flowers at female transition
-> count available perfect/male flowers
-> determine runtime common-support eligibility
-> randomize q only among common-support eligible units
-> perform q manipulation
-> immediately record eggs_before_manipulation
-> manipulation is technically qualified only if the preregistered egg/timing gate passes.
```

A presurvey estimates whether a q design is feasible, but individual eligibility must be rechecked at runtime because reliable sex classification is tied to the female transition.

## Runtime ledger

Use:

```text
empirical/identification_design/PEUCEDANUM_FIELD_RUNTIME_ELIGIBILITY_LEDGER_V1.csv
```

for the transition from field observation to randomized treatment.

It records:

```text
site / plot / unit
observation date and time
male-phase completion
available perfect/male counts
runtime common-support status
q assignment lock
manipulation start/end time
pre-manipulation eggs
mechanical damage
operator
authorization IDs.
```

No q assignment should be recorded before the common-support field is resolved for that unit.

## Current regulatory facts — checked 2026-09-05

### 1. The host plant is a Daisetsuzan designated plant

The Ministry of the Environment's Daisetsuzan National Park designated-plant list, revised 2025-07-22, contains:

```text
No. 565
ハクサンボウフウ
Peucedanum multivittatum
```

and notes inclusion of キレハノハクサンボウフウ.

Therefore, if the HA field site is in a National Park **special area**, q manipulation by floral removal and leaf sampling fall within the regulatory issue of collecting/damaging a designated plant. In a special protection district, plant collection/damage is regulated even more broadly.

Do not infer field authorization from the fact that previous research was performed at HA; a new project requires its own current authorization status.

### 2. Plant manipulation and leaf sampling are separate declared actions

The field plan must separately resolve:

```text
A. flower removal / damage used to create q treatments
B. leaf collection or damage for genotyping / paternity.
```

They may be covered by one authorization in practice, but the administrative readiness receipt keeps them separate so that leaf sampling can be removed from the design if it is not authorized.

### 3. The predator moth is not on the current National Park designated-animal list

The current Ministry of the Environment designated-animal page lists the National Parks/animals for which designated-animal rules operate in ordinary special areas. Daisetsuzan is not listed, and `Phaulernis fulviguttella` is not a designated animal on that list.

This does **not** mean egg removal is automatically authorized.

Current Natural Parks Act guidance states:

```text
special protection district:
  capture/killing of all animals and collection/damage of animal eggs are regulated

special area:
  designated-animal capture etc. is regulated under the designated-animal provision.
```

Other laws, local rules, land-management conditions or an exact-site special-protection designation may still apply.

Therefore the egg-removal field remains:

```text
ZONE_AND_AUTHORITY_DEPENDENT
```

until the responsible office explicitly confirms `PERMITTED` or `NOT_REQUIRED_CONFIRMED_BY_AUTHORITY`.

### 4. Scientific research can be eligible for permission, but permission is not automatic

National Park permit-handling criteria provide a route for plant/animal collection or damage where the action is necessary for academic research or another public-interest purpose and the site-specific conservation criteria are satisfied.

Daisetsuzan management guidance additionally emphasizes:

- use the minimum quantity needed for research,
- avoid unnecessary concentration of collection/damage,
- protect threatened taxa,
- carry the authorization during the activity,
- avoid high-use periods/areas where possible.

This is a possible permission basis, not a prediction that the current project will be approved.

## Exact zoning remains unresolved

The published Taisetsu study gives the broad study region as approximately:

```text
43°32–33'N
142°51–53'E
```

and identifies focal populations by codes such as HA/HL rather than publishing the exact field coordinates needed for a legal zone overlay.

The Ministry of the Environment explicitly advises that detailed zone confirmation should be performed with the responsible ranger/management office.

Therefore current status is:

```text
HA biological identity: HIGH_CONFIDENCE
HA exact coordinates for permit routing: NOT YET RECOVERED
HA exact park zone: NOT YET VERIFIED.
```

Do not assign `SPECIAL_PROTECTION`, `CLASS_1`, `CLASS_2`, `CLASS_3` or `ORDINARY` from the broad paper coordinates alone.

## Administrative routing

The Ministry of the Environment currently routes Daisetsuzan applications by municipality.

```text
Daisetsuzan National Park Management Office
  handles areas other than the municipality groups below
  TEL 01658-2-2574
  RO-KAMIKAWA@env.go.jp

Higashikawa Ranger Office
  handles Furano City, Higashikawa Town, Biei Town, Sorachi District
  TEL 0166-82-2527
  RO-HIGASHIKAWA@env.go.jp

Kamishihoro Ranger Office
  handles Kato District and Shintoku Town
  TEL 01564-2-3337
  RO-KAMISHIHORO@env.go.jp
```

The responsible office must be selected only after the exact HA municipality/site is confirmed.

## Separate administrative gates

Before field manipulation, resolve each action independently:

| Action | Biological role | Current administrative status |
| --- | --- | --- |
| Observe/census without collection | presurvey/phenology | site-access rules still need confirmation |
| Remove perfect/male flowers | randomized q manipulation | BLOCKED pending exact zone + plant authorization |
| Collect/damage leaves | paternity/genotyping | BLOCKED pending exact zone + plant authorization |
| Count moth eggs without removal | mechanism census | access/site rules to confirm |
| Remove/damage moth eggs | randomized G | BLOCKED pending exact zone + authority confirmation/authorization |
| Install markers or temporary equipment | repeated-unit tracking | land/park conditions to confirm |

## Machine administrative gate

Use:

```text
empirical/identification_design/PEUCEDANUM_FIELD_ADMIN_READINESS_TEMPLATE_V1.json
scripts/evaluate_peucedanum_field_admin_readiness.py
```

The evaluator deliberately does not contain a legal inference engine.

For every planned action, it accepts only:

```text
PERMITTED
or
NOT_REQUIRED_CONFIRMED_BY_AUTHORITY.
```

It also requires:

```text
exact coordinates verified
municipality resolved
park zone resolved
responsible office resolved
authorization window covers planned field dates
land manager/site owner identified
site access/research status resolved
other required authorizations checked.
```

Only then can it return:

```text
PEUCEDANUM_FIELD_ADMINISTRATIVELY_READY.
```

An expired authorization, unresolved zone, uncertain 'probably not required' status or missing land-manager permission blocks the receipt.

## Biological vs administrative readiness

The full execution gate is:

```text
BIOLOGY
primary site selected (HA)
+ phenological timing window supported
+ presurvey/common-support plan
+ technical q-manipulation pilot
+ Stage-A / Stage-B analysis registered

ADMINISTRATION
exact HA coordinates
+ municipality / park zone
+ plant manipulation authorization
+ leaf-sampling authorization if retained
+ egg-removal authorization or written not-required confirmation
+ land-manager/site access approval
+ any other required legal/ethical approvals

BIOLOGY + ADMINISTRATION
-> FIELD EXECUTION READY.
```

## Recommended next administrative action

The highest-value next step is not a larger confirmatory sample. It is to recover the exact HA site from the original field team / existing project records and send the responsible Ministry of the Environment office a single action-specific inquiry describing:

1. exact coordinates and mapped treatment footprint,
2. `Peucedanum multivittatum` designated-plant status,
3. number of plants screened versus actually manipulated,
4. maximum flowers removed per individual and total,
5. whether leaves will be sampled and maximum leaf tissue per plant,
6. moth egg census and proposed remove/retain manipulation,
7. temporary tags/markers,
8. field dates,
9. rationale for why the experiment must use a naturally high-predation Taisetsu population,
10. minimization and restoration/cleanup measures.

The response should be stored as the authorization evidence used to populate the administrative-readiness template.

## Claim boundary

This document is a research-operation gate, not legal advice. Regulations and site zoning can change, and the responsible authority determines whether a specific action requires or receives permission.
