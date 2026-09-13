# openFDA Dataset Assessment for Trial Termination Research

## Scope

The research question is: **What factors are associated with early termination of clinical trials?**

This assessment uses the official [openFDA API catalog](https://open.fda.gov/apis/),
endpoint documentation, and API metadata responses. No openFDA bulk dataset was
downloaded. The AACT raw archive remains separate and untouched.

Record counts below are approximate API record counts observed on 2026-09-13;
they change as FDA updates the APIs. A record count is not a count of unique
drugs, products, patients, adverse events, or trials.

## Candidate datasets

### Drug and safety datasets

| Dataset | Approximate size and currentness | Contents | Possible connection to AACT |
| --- | ---: | --- | --- |
| [Drug adverse events](https://open.fda.gov/apis/drug/event/) (`drug/event`) | 20,692,690 records; API metadata last updated 2026-07-30 | FAERS reports from 2004 onward, including report dates, seriousness indicators, patient characteristics, suspected or concomitant products, indications, routes, and reported reactions. | Match AACT intervention names to `patient.drug.medicinalproduct`, then derive pre-specified drug-level safety-signal features or post-market adverse-event burden. No NCT ID is provided, so this is an intervention-level linkage rather than a trial-level join. |
| [Drugs@FDA](https://open.fda.gov/apis/drug/drugsfda/) (`drug/drugsfda`) | 29,325 records; API metadata last updated 2026-09-11 | FDA drug applications and approval history, including application number, sponsor name, products, submission types/statuses, submission dates, review priority, and class descriptions. | Match drug interventions and sponsor names to identify whether an intervention has an FDA application or approval history, regulatory maturity, submission activity, or sponsor-level regulatory context. |
| [Drug labeling](https://open.fda.gov/apis/drug/label/) (`drug/label`) | 262,842 records; API metadata last updated 2026-09-11 | Structured product labels, including active ingredients, brand/generic names, manufacturer, route, indications, warnings, contraindications, dosage, and safety information. | Match intervention names, ingredients, UNII, or product NDC to add labeled indication, route, warning, and contraindication features. Labels generally describe marketed products and do not identify the originating clinical trial. |
| [Orange Book](https://open.fda.gov/apis/drug/orangebook/) (`drug/orangebook`) | 48,664 records; API metadata last updated 2026-09-11 | Approved drug products, active ingredients, application/product numbers, marketing status, dosage form, route, therapeutic-equivalence codes, patent, and exclusivity information where available. | Match drug interventions to characterize approval status, generic/reference-product status, route, and market or exclusivity context. Useful as a regulatory maturity covariate, but not a direct trial-termination source. |
| [Drug NDC](https://open.fda.gov/apis/drug/ndc/) (`drug/ndc`) | 137,841 records; API metadata last updated 2026-09-11 | National Drug Code product/package records, including labeler, product and package identifiers, active ingredients, dosage form, route, marketing category, and product status. | Normalize intervention names to ingredients and marketed products, then link to labels, Orange Book, or FAERS. The NDC is a product identifier and is not a clinical-trial identifier. |
| [Drug enforcement reports](https://open.fda.gov/apis/drug/enforcement/) (`drug/enforcement`) | 17,938 records; API metadata last updated 2026-09-02 | Drug recalls and enforcement actions, including recalling firm, product description, recall reason, classification, dates, distribution, and termination date. | Match products or firms to identify recalls or quality/safety actions that could contextualize a trial intervention. Usually post-market and vulnerable to name-matching ambiguity. |
| [Drug shortages](https://open.fda.gov/apis/drug/drugshortages/) | Official openFDA catalog entry; no working public JSON endpoint was returned during this review, so size was not estimated. | Drug shortage status and related supply information where available through FDA resources. | Could provide an operational or supply-related explanation for interruption or termination, but it needs endpoint verification before use and is not a direct trial dataset. |

### Device datasets

These are potentially relevant because AACT includes device and drug-device
interventions, but they are less useful for an all-therapeutic-area first pass
unless device trials are analyzed separately.

| Dataset | Approximate size and currentness | Contents | Possible connection to AACT |
| --- | ---: | --- | --- |
| [Device adverse events](https://open.fda.gov/apis/device/event/) (`device/event`) | 26,136,889 records; API metadata last updated 2026-09-08 | Medical-device adverse-event reports, including device identifiers, event types, patient/event details, manufacturers, and report dates. | Match device intervention names or identifiers to add post-market device-event burden. Direct trial linkage is generally unavailable. |
| [Device recalls](https://open.fda.gov/apis/device/recall/) (`device/recall`) | 59,131 records; API metadata last updated 2026-09-10 | Device recall records, products, firms, recall reasons, classifications, and dates. | Add device recall or quality-action context for trials involving devices. |
| [510(k)](https://open.fda.gov/apis/device/510k/) (`device/510k`) | 176,000 records; API metadata last updated 2026-08-31 | Premarket notification records, applicants, product codes, decision dates, trade names, and decision codes. | Characterize device regulatory clearance and applicant history for device interventions. |
| [PMA](https://open.fda.gov/apis/device/pma/) (`device/pma`) | 57,066 records; API metadata last updated 2026-08-31 | Premarket approval records, applicants, device names, PMA numbers, decision dates, and supplement information. | Characterize higher-risk device approval history and regulatory status. |
| [Device classification](https://open.fda.gov/apis/device/classification/) (`device/classification`) | 7,091 records; API metadata last updated 2026-08-31 | Device product codes, classification, regulation numbers, review panels, and risk class. | Map device interventions to device class and regulatory category. |
| [Device registration/listing](https://open.fda.gov/apis/device/registrationlisting/) (`device/registrationlisting`) | 334,839 records; API metadata last updated 2026-08-31 | Establishment registration and device listing information. | Add manufacturer or marketed-device context, but weak direct connection to trial termination. |
| [Unique Device Identification](https://open.fda.gov/apis/device/udi/) (`device/udi`) | 5,182,695 records; API metadata last updated 2026-09-02 | UDI device records, brand, company, model/version, identifiers, product codes, and distribution/status attributes. | Improve device-name and identifier normalization before linking to device events, recalls, or approvals. |

## What is not present

The openFDA API catalog does not provide a general clinical-trial registry that
duplicates ClinicalTrials.gov or AACT. ClinicalTrials.gov remains the source for
trial status, enrollment, phase, design, dates, arms, allocation, masking, and
reported stopping reason. openFDA can add product, safety, labeling, approval,
recall, or device context, but it generally does not provide an NCT-level join.

## Recommendation

### Recommended dataset: Drug adverse events (`drug/event`)

For a first complementary dataset, use the openFDA **Drug Adverse Events API**.
It is the best match to a plausible mechanism of early termination: safety or
tolerability concerns related to an intervention. It is also broad enough to
cover drug interventions across the therapeutic areas represented in AACT and
large enough to support intervention-level safety features rather than relying
on a small hand-picked product list.

This recommendation is for a future, carefully defined linkage study. It does
not imply that an adverse-event report caused a particular trial to terminate.
The openFDA documentation warns that reports may list several drugs and several
reactions, that causality is not established, that reporting is affected by
exposure and publicity, and that the data should not be used alone for clinical
or causal conclusions. FAERS is also largely post-market, so features must be
restricted by date relative to trial start or termination to avoid temporal
leakage.

## Variables to consider later

Potential derived variables from `drug/event` include:

- `patient.drug.medicinalproduct`: normalized intervention/product name for
  linkage to AACT `interventions.name`.
- `patient.drug.drugindication`: reported indication, useful for comparing the
  event context with AACT `conditions.name`.
- `patient.drug.drugadministrationroute`: administration route, potentially
  comparable with intervention details and product labels.
- `patient.reaction.reactionmeddrapt`: reported reaction terms, summarized into
  pre-specified safety categories rather than used as unrestricted post hoc
  features.
- `serious`, `seriousnessdeath`, and related seriousness flags: counts or rates
  of serious reports, with careful denominators and sensitivity analyses.
- `receivedate`, `receiptdate`, and `transmissiondate`: time windows for
  restricting events to information available before a trial's termination.
- `primarysource.reportercountry` and `primarysource.qualification`: reporting
  context and source type.
- `drugauthorizationnumb` and other available product identifiers: possible
  support for matching to Drugs@FDA, NDC, or labels, subject to coverage.

The initial AACT linkage would likely be at the intervention/product level, with
manual or dictionary-assisted name normalization and an explicit unresolved
match category. No openFDA data has been downloaded, transformed, or joined yet.