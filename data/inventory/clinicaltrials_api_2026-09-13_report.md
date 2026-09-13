# ClinicalTrials.gov API Representative Download

## Download summary

The official ClinicalTrials.gov API v2 endpoint was used:

`https://clinicaltrials.gov/api/v2/studies`

The raw responses are stored separately from the AACT snapshot in:

`data/raw/clinicaltrials_api/2026-09-13/`

Five status-stratified requests were downloaded, with 20 studies per response:

| Response | API filter | Records |
| --- | --- | ---: |
| `studies_terminated.json` | `TERMINATED` | 20 |
| `studies_withdrawn.json` | `WITHDRAWN` | 20 |
| `studies_suspended.json` | `SUSPENDED` | 20 |
| `studies_completed.json` | `COMPLETED` | 20 |
| `studies_recruiting.json` | `RECRUITING` | 20 |
| **Total** | **Five bounded status samples** | **100** |

The API response files are complete raw JSON responses, not reduced extracts.
They have not been cleaned, reformatted, filtered after download, or merged.
The API reported version `2.0.5` and data timestamp `2026-09-11T09:00:04` at
download time. SHA-256 checksums are recorded below for provenance:

| File | SHA-256 |
| --- | --- |
| `studies_completed.json` | `61862aec0ff7c7df9e8ae19ff4694630d9ebf0d41f1f6997d4da78a4e340a0d3` |
| `studies_recruiting.json` | `7028ae3454b4816dc86b35172b4e218d32cbba4c263531a0309aee6598497188` |
| `studies_suspended.json` | `1b519fe1081cc397b20c2e022defa19ce83cf699f33b2ecc5ce0e2c0a351b382` |
| `studies_terminated.json` | `4cca456e5fd62d375f95f8d6a68e9c91200c1fb03f482f8e33a840eb93b940c8` |
| `studies_withdrawn.json` | `323974ad1221911d18fa61bbac48d160f75092d56a3b7b3045725ee4f1580612` |

Definitions are based on the [ClinicalTrials.gov API documentation](https://clinicaltrials.gov/data-api/about-api)
and the [ClinicalTrials.gov data structure](https://clinicaltrials.gov/data-api/api).

## Requested fields and meanings

Each study is contained in the API response under `studies[].protocolSection`.
The API uses nested modules rather than a single flat row.

| Project field | ClinicalTrials.gov API path | Meaning in ClinicalTrials.gov | AACT correspondence |
| --- | --- | --- | --- |
| NCT ID | `identificationModule.nctId` | The unique ClinicalTrials.gov identifier assigned to the study. | `studies.nct_id` |
| Overall study status | `statusModule.overallStatus` | The current overall recruitment/status category, such as `RECRUITING`, `COMPLETED`, `TERMINATED`, `WITHDRAWN`, or `SUSPENDED`. | `studies.overall_status` |
| Study type | `designModule.studyType` | Whether the study is interventional or observational, with other registry study-type categories where applicable. | `studies.study_type` |
| Phase | `designModule.phases[]` | The development phase or phases of an interventional study, such as `PHASE1`, `PHASE2`, or `PHASE3`; observational studies generally have no phase. | `studies.phase` |
| Enrollment | `designModule.enrollmentInfo.count` and `.type` | Planned or actual number of participants and whether the count is estimated or actual. | `studies.enrollment`, `studies.enrollment_type` |
| Sponsor information | `sponsorCollaboratorsModule.leadSponsor`, `.collaborators`, and `.responsibleParty` | The lead organization, collaborating organizations, and party responsible for submitting or overseeing the study. | `sponsors` table; also `studies.source`, `overall_officials`, and `responsible_parties` |
| Conditions | `conditionsModule.conditions[]` | Diseases, disorders, or health conditions studied. | `conditions.name` linked by `nct_id` |
| Interventions | `armsInterventionsModule.interventions[]` and `.armGroups[]` | Treatments, drugs, devices, procedures, behavioral interventions, or other interventions, plus their assigned groups or arms. | `interventions`, `design_group_interventions`, and `design_groups` |
| Study start date | `statusModule.startDateStruct.date` and `.type` | The study start date and whether it is actual or estimated. | `studies.start_date`, `studies.start_date_type`, and month-year fields |
| Study completion date | `statusModule.completionDateStruct.date` and `.type` | The date by which the study is expected or recorded to be completed and whether it is actual or estimated. | `studies.completion_date`, `studies.completion_date_type`, and month-year fields |
| Study design | `designModule` and `designModule.designInfo` | The study's design characteristics, including study type, allocation, intervention model, masking, time perspective, observational model, and primary purpose. | `designs` table plus `studies.study_type` |
| Number of arms | `designModule.numberOfArms` when present; otherwise `armsInterventionsModule.armGroups[]` | The number of intervention or comparison arms. In this representative sample, an explicit `numberOfArms` value was not populated; arm groups are available for studies that report them. | `studies.number_of_arms`, `studies.number_of_groups`, `design_groups` |
| Allocation | `designModule.designInfo.allocation` | How participants are assigned to study groups, including randomized or non-randomized allocation. | `designs.allocation` |
| Intervention model | `designModule.designInfo.interventionModel` | The structure by which an intervention is administered or compared, such as parallel, crossover, or single-group. | `designs.intervention_model` |
| Masking | `designModule.designInfo.maskingInfo.masking` and `.whoMasked[]` | Whether participants, care providers, investigators, or outcome assessors know the intervention assignment. | `designs.masking`, `designs.subject_masked`, `designs.caregiver_masked`, `designs.investigator_masked`, `designs.outcomes_assessor_masked` |
| Primary purpose | `designModule.designInfo.primaryPurpose` | The main purpose of an interventional study, such as treatment, prevention, diagnostic, supportive care, or other purpose. | `designs.primary_purpose` |

## Correspondence and limitations

The API and AACT describe the same registry records but expose them differently:

- ClinicalTrials.gov API v2 preserves a nested JSON protocol model. AACT flattens
  related modules into relational tables and includes additional derived or
  historical fields.
- API arrays such as `phases`, `conditions`, `interventions`, `collaborators`,
  and `armGroups` correspond to one-to-many AACT tables or repeated study-linked
  rows, not always one scalar AACT field.
- API date objects include both `date` and `type`; AACT stores separate date,
  date-type, and month-year columns.
- `numberOfArms` may be absent in the API. Counting `armGroups[]` is not always
  identical to the AACT value and should be handled as a documented mapping
  decision later.
- AACT's `studies.overall_status` is the primary termination outcome candidate;
  `studies.why_stopped` provides a reported stopping reason when available.
  The API records downloaded here are for structure and definition validation,
  not for cleaning, modeling, or producing the final analysis dataset.

No data cleaning, deletion, variable selection, or analysis has been performed.