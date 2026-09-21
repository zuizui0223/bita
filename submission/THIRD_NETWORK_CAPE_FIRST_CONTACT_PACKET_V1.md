# Cape third-network first-contact packet v1

## Status

~~~text
SCIENTIFIC_PROTOCOL = FROZEN
CONTACTS_VERIFIED = 2026-09-21
EMAIL_BODY = SEND_READY
FEASIBILITY_FORM = READY
OUTCOME_EXPOSURE_QUARANTINE = READY
EXTERNAL_SEND = AUTHOR_APPROVAL_REQUIRED
~~~

## First message

**To**

- steenhuisens@ufs.ac.za
- jeremy.midgley@uct.ac.za

**CC**

- none on the first message

**Subject**

~~~text
Prospective small-mammal × Protea study of floral access routing
~~~

**Body**

Use exactly:

- `submission/THIRD_NETWORK_CAPE_COLLABORATION_EMAIL_V1.md`

The signature is:

~~~text
Ruiqi Zhang
Graduate School of Agriculture, Kyoto University
zhang.ruiqi.77h@st.kyoto-u.ac.jp
~~~

## Attach / include

Preferred first-contact support material:

- `submission/THIRD_NETWORK_CAPE_FEASIBILITY_FORM_V1.md`

Do not attach historical route-specific results, site-specific B/L tables,
candidate-species rankings, or any M–Y visualization.

## Outcome-blind boundaries

The first message may ask about:

- candidate regions / site pools;
- >=5 flowering Protea species;
- >=5 non-flying mammal species from route-blind evidence;
- flowering windows;
- camera logistics;
- plant-depth measurement;
- independent mammal morphometrics;
- land / permit / ethics pathways;
- collaboration interest.

It must not ask which site, plant, or mammal has shown more destructive,
lateral, robbing, bypass, or legitimate access.

## Reply handling

Do not convert the raw reply directly into the site-selection table.

1. retain the raw reply as correspondence provenance;
2. extract only route-blind feasibility into
   `THIRD_NETWORK_COLLABORATION_RESPONSE_SCHEMA_V1.csv`;
3. classify unsolicited exposure with
   `scripts/evaluate_third_network_collaboration_response.py`;
4. exclude SITE_EXPOSED / PLANT_EXPOSED / MAMMAL_EXPOSED entities;
5. block the current Cape lane if SYSTEM_EXPOSED;
6. pass only the clean pool to the later route-blind presurvey.

## Follow-up contacts

Use only if the primary first-contact route does not resolve field feasibility or
if Steenhuisen / Midgley recommend them:

- c.peter@ru.ac.za
- johnsonsd@ukzn.ac.za

Do not expand recipients simply to increase the chance of a favorable site.

## External-action boundary

No message has been sent by creation of this packet.

The next external action is a single author-approved first-contact message to
Steenhuisen and Midgley.
