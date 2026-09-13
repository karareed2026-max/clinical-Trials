# Proposed AACT Trial-Termination Analysis Dataset

This is a study-level candidate dataset derived from the preserved AACT ZIP. The raw archive was read only and was not extracted, modified, deleted, or reorganized. No studies were excluded for missing values, status, phase, or study type. No final complexity score, machine-learning model, or causal analysis was created.

- Source archive: `data/raw/2026-09-12/20260912_export_ctgov.zip`
- Candidate output: `data/processed/aact_trial_termination_candidate_2026-09-12.tsv.gz`
- Studies available: **602,514**
- Unique NCT IDs: **602,514**
- Duplicate NCT IDs: **0**

## Construction rules

- The `studies` table is the study spine; one output row is emitted per AACT `studies` row.
- Conditions, interventions, sponsors, facilities, designs, and outcomes are aggregated by `nct_id`; original source values are retained as delimited text where multiple values exist.
- `primary_condition` is the first condition by source ID order; `conditions_all` preserves all condition names. No therapeutic-area classification was assigned.
- `placebo_used` is `yes` when an intervention name or description contains `placebo`, `no` when interventions exist but no placebo text is found, and missing when no intervention is reported.
- `randomized_binary` reflects exact AACT allocation `RANDOMIZED`; blank allocation is kept as missing. `terminated_binary` is 1 for `overall_status=TERMINATED` and 0 otherwise. Comparison-group eligibility remains undecided; all original status categories are reported below.
- `study_duration_days` is calculated only from full valid `YYYY-MM-DD` start and completion dates with completion on or after start. Partial, invalid, reversed, or missing dates produce missing duration.

## Proposed variables

| Variable | Source or derivation | Purpose |
| --- | --- | --- |
| `nct_id` | `studies.nct_id` | Study identifier and join key |
| `overall_status`, `terminated_binary`, `why_stopped`, `last_known_status` | `studies` | Outcome and status detail |
| `study_type`, `phase` | `studies` | Trial type and phase categories, including all reported categories |
| `enrollment`, `enrollment_type` | `studies` | Recruitment scale and estimated/actual status |
| `lead_sponsor_type`, `lead_sponsor_organization`, `sponsor_types`, `sponsor_organizations`, `sponsor_count` | `sponsors` | Sponsorship characteristics |
| `primary_condition`, `conditions_all` | `conditions` | Therapeutic condition information; no arbitrary classification |
| `intervention_count`, `intervention_names`, `intervention_types`, `placebo_used` | `interventions` | Intervention complexity and placebo indicator |
| `primary_outcome_type`, `primary_outcome_types_all`, `primary_outcome_count` | `outcomes` | Primary outcome structure |
| `number_of_arms`, `number_of_groups` | `studies` | Complexity variables preserved from AACT |
| `number_of_sites` | count of distinct `facilities.id` | Operational footprint |
| `allocation`, `randomized_binary`, `randomized_vs_nonrandomized` | `designs` | Randomization classification |
| `intervention_model`, `masking`, `primary_purpose`, `observational_model`, `time_perspective` | `designs` | Design and complexity descriptors |
| `study_start_date`, `study_completion_date`, `start_year`, `completion_year` | `studies` | Timing variables |
| `study_duration_days` | valid completion minus start date | Observed study duration |

## Required distributions

### Overall status

| Category | Count |
| --- | ---: |
| COMPLETED | 329,096 |
| UNKNOWN | 97,091 |
| RECRUITING | 64,647 |
| TERMINATED | 34,295 |
| NOT_YET_RECRUITING | 29,592 |
| ACTIVE_NOT_RECRUITING | 21,993 |
| WITHDRAWN | 16,749 |
| ENROLLING_BY_INVITATION | 5,235 |
| SUSPENDED | 1,765 |
| WITHHELD | 984 |
| NO_LONGER_AVAILABLE | 533 |
| AVAILABLE | 257 |
| APPROVED_FOR_MARKETING | 240 |
| TEMPORARILY_NOT_AVAILABLE | 37 |

### Phase

| Category | Count |
| --- | ---: |
| NA | 236,439 |
| [missing] | 142,799 |
| PHASE2 | 65,493 |
| PHASE1 | 48,633 |
| PHASE3 | 42,245 |
| PHASE4 | 35,782 |
| PHASE1/PHASE2 | 17,060 |
| PHASE2/PHASE3 | 7,590 |
| EARLY_PHASE1 | 6,473 |

### Study type

| Category | Count |
| --- | ---: |
| INTERVENTIONAL | 459,840 |
| OBSERVATIONAL | 140,623 |
| EXPANDED_ACCESS | 1,067 |
| [missing] | 984 |

### Randomized classification

| Category | Count |
| --- | ---: |
| randomized | 302,582 |
| non-randomized | 151,567 |
| not reported | 148,365 |

### Placebo use

| Category | Count |
| --- | ---: |
| no | 476,106 |
| yes | 65,367 |
| [missing] | 61,041 |

### Sponsor type

| Category | Count |
| --- | ---: |
| OTHER | 431,008 |
| INDUSTRY | 132,306 |
| OTHER_GOV | 16,023 |
| NIH | 11,574 |
| NETWORK | 5,026 |
| FED | 4,935 |
| [missing] | 984 |
| INDIV | 560 |
| UNKNOWN | 95 |
| AMBIG | 3 |

### Primary outcome type

| Category | Count |
| --- | ---: |
| [missing] | 522,435 |
| PRIMARY | 80,079 |

### Reasons for stopping

| Category | Count |
| --- | ---: |
| [missing] | 555,527 |
| Sponsor decision | 337 |
| Lack of funding | 311 |
| Slow accrual | 273 |
| Lack of enrollment | 181 |
| Sponsor Decision | 181 |
| Low accrual | 172 |
| slow accrual | 143 |
| Business decision | 143 |
| low accrual | 138 |
| See termination reason in detailed description. | 132 |
| Low enrollment | 129 |
| Slow enrollment | 120 |
| No participants enrolled | 119 |
| lack of funding | 115 |
| Poor accrual | 111 |
| Slow recruitment | 109 |
| COVID-19 | 105 |
| Funding | 101 |
| Lack of recruitment | 94 |

### Primary condition (top 20)

| Category | Count |
| --- | ---: |
| Healthy | 9,892 |
| Breast Cancer | 7,555 |
| Obesity | 4,738 |
| Stroke | 4,135 |
| Prostate Cancer | 3,709 |
| Asthma | 3,141 |
| Hypertension | 2,965 |
| HIV Infections | 2,933 |
| Cancer | 2,890 |
| Coronary Artery Disease | 2,850 |
| Heart Failure | 2,765 |
| Pain | 2,626 |
| Schizophrenia | 2,550 |
| Colorectal Cancer | 2,517 |
| Healthy Volunteers | 2,473 |
| COVID-19 | 2,399 |
| Depression | 2,278 |
| Multiple Sclerosis | 2,267 |
| Diabetes Mellitus, Type 2 | 2,245 |
| Lung Cancer | 2,208 |

### Interventions per study

Non-missing: **602,514**; missing: **0** (0.00%)

| Minimum | P25 | Median | P75 | Maximum |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 2 | 97 |

### Sites per study

Non-missing: **602,514**; missing: **0** (0.00%)

| Minimum | P25 | Median | P75 | Maximum |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 1 | 3,510 |

### Enrollment

Non-missing: **595,379**; missing: **7,135** (1.18%)

| Minimum | P25 | Median | P75 | Maximum |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 30 | 69 | 190 | 188,814,085 |

### Study duration (days)

Non-missing: **584,782**; missing: **17,732** (2.94%)

| Minimum | P25 | Median | P75 | Maximum |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 358 | 731 | 1,381 | 40,177 |

## Missingness for every proposed variable

| Variable | Missing | Missing % |
| --- | ---: | ---: |
| `nct_id` | 0 | 0.00% |
| `overall_status` | 0 | 0.00% |
| `terminated_binary` | 0 | 0.00% |
| `why_stopped` | 555,527 | 92.20% |
| `last_known_status` | 505,423 | 83.89% |
| `study_type` | 984 | 0.16% |
| `phase` | 142,799 | 23.70% |
| `enrollment` | 7,135 | 1.18% |
| `enrollment_type` | 17,133 | 2.84% |
| `lead_sponsor_type` | 984 | 0.16% |
| `lead_sponsor_organization` | 0 | 0.00% |
| `sponsor_types` | 984 | 0.16% |
| `sponsor_organizations` | 0 | 0.00% |
| `sponsor_count` | 0 | 0.00% |
| `primary_condition` | 1,022 | 0.17% |
| `conditions_all` | 1,022 | 0.17% |
| `intervention_count` | 0 | 0.00% |
| `intervention_names` | 61,215 | 10.16% |
| `intervention_types` | 61,041 | 10.13% |
| `placebo_used` | 61,041 | 10.13% |
| `primary_outcome_type` | 522,435 | 86.71% |
| `primary_outcome_types_all` | 522,435 | 86.71% |
| `primary_outcome_count` | 0 | 0.00% |
| `number_of_arms` | 166,626 | 27.66% |
| `number_of_groups` | 509,553 | 84.57% |
| `number_of_sites` | 0 | 0.00% |
| `allocation` | 148,365 | 24.62% |
| `randomized_binary` | 148,365 | 24.62% |
| `randomized_vs_nonrandomized` | 0 | 0.00% |
| `intervention_model` | 149,268 | 24.77% |
| `masking` | 148,076 | 24.58% |
| `primary_purpose` | 149,490 | 24.81% |
| `observational_model` | 467,676 | 77.62% |
| `time_perspective` | 464,805 | 77.14% |
| `study_start_date` | 5,362 | 0.89% |
| `study_completion_date` | 16,689 | 2.77% |
| `start_year` | 5,362 | 0.89% |
| `completion_year` | 16,689 | 2.77% |
| `study_duration_days` | 17,732 | 2.94% |

## Interpretation boundary

This dataset is intentionally a complete candidate set. The reported `terminated_binary` coding identifies terminated records but does not decide which non-terminated statuses should form a comparison group. Phase, status, sponsor, condition, and design categories are reported as supplied by AACT; future therapeutic-area grouping and complexity measurement require an explicit, documented decision.
