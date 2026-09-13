# AACT Flat-File Inventory: 2026-09-12

Source archive: `20260912_export_ctgov.zip`  
Archive SHA-256: `838406738300d3f2766e33ce5457f287ecd172fec227d4229755bed35297a05c`  
Source: [AACT official downloads](https://aact.ctti-clinicaltrials.org/downloads)

This report inventories every table in the preserved ZIP. Row counts are data rows excluding the header. Headers and row data were streamed directly from the archive; no raw files were cleaned, deleted, modified, extracted, or reorganized.

## Research focus

Potential relevance is an initial screening judgment for the question: **What factors are associated with early termination of clinical trials?** Core columns include trial status and stopping reason, phase, enrollment, sponsor, condition, intervention, design, arms, sites, dates, randomization or allocation, and masking. This is an inventory only, not a final analysis dataset or variable-selection decision.

## Summary

| Tables | Inventory columns |
| ---: | ---: |
| 49 | 453 |

## Tables

### `baseline_counts`

Participant baseline counts reported for result groups.

**Rows:** 240449  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `units`, `scope`, `count`  
**Potentially relevant to early termination:** `result_group_id`, `ctgov_group_code`

### `baseline_measurements`

Participant baseline measurements reported for result groups.

**Rows:** 2963066  
**Columns:** 22  
**Column names:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `classification`, `category`, `title`, `description`, `units`, `param_type`, `param_value`, `param_value_num`, `dispersion_type`, `dispersion_value`, `dispersion_value_num`, `dispersion_lower_limit`, `dispersion_upper_limit`, `explanation_of_na`, `number_analyzed`, `number_analyzed_units`, `population_description`, `calculate_percentage`  
**Potentially relevant to early termination:** `result_group_id`, `ctgov_group_code`, `param_type`, `dispersion_type`, `calculate_percentage`

### `brief_summaries`

Brief structured summaries of study records.

**Rows:** 601530  
**Columns:** 3  
**Column names:** `id`, `nct_id`, `description`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `browse_conditions`

Normalized condition terms used for browsing and indexing studies.

**Rows:** 4368819  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `mesh_term`, `downcase_mesh_term`, `mesh_type`  
**Potentially relevant to early termination:** `id`, `nct_id`, `mesh_term`, `downcase_mesh_term`, `mesh_type`

### `browse_interventions`

Normalized intervention terms used for browsing and indexing studies.

**Rows:** 2553067  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `mesh_term`, `downcase_mesh_term`, `mesh_type`  
**Potentially relevant to early termination:** `id`, `nct_id`, `mesh_term`, `downcase_mesh_term`, `mesh_type`

### `calculated_values`

AACT-calculated study and result values.

**Rows:** 602514  
**Columns:** 19  
**Column names:** `id`, `nct_id`, `number_of_facilities`, `number_of_nsae_subjects`, `number_of_sae_subjects`, `registered_in_calendar_year`, `nlm_download_date`, `actual_duration`, `were_results_reported`, `months_to_report_results`, `has_us_facility`, `has_single_facility`, `minimum_age_num`, `maximum_age_num`, `minimum_age_unit`, `maximum_age_unit`, `number_of_primary_outcomes_to_measure`, `number_of_secondary_outcomes_to_measure`, `number_of_other_outcomes_to_measure`  
**Potentially relevant to early termination:** `registered_in_calendar_year`, `nlm_download_date`, `months_to_report_results`, `has_us_facility`, `has_single_facility`, `minimum_age_num`, `maximum_age_num`, `minimum_age_unit`, `maximum_age_unit`, `number_of_primary_outcomes_to_measure`, `number_of_secondary_outcomes_to_measure`, `number_of_other_outcomes_to_measure`

### `central_contacts`

Central study contact information.

**Rows:** 226221  
**Columns:** 8  
**Column names:** `id`, `nct_id`, `contact_type`, `name`, `phone`, `email`, `phone_extension`, `role`  
**Potentially relevant to early termination:** `id`, `nct_id`, `contact_type`, `name`, `phone`, `email`, `phone_extension`, `role`

### `conditions`

Conditions and diseases investigated by each study.

**Rows:** 1083025  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `name`, `downcase_name`  
**Potentially relevant to early termination:** `id`, `nct_id`, `name`, `downcase_name`

### `countries`

Countries in which study sites are located.

**Rows:** 816098  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `name`, `removed`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `design_group_interventions`

Interventions assigned to design groups or arms.

**Rows:** 1344197  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `design_group_id`, `intervention_id`  
**Potentially relevant to early termination:** `id`, `nct_id`, `design_group_id`, `intervention_id`

### `design_groups`

Study design groups, cohorts, or arms.

**Rows:** 1108587  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `group_type`, `title`, `description`  
**Potentially relevant to early termination:** `id`, `nct_id`, `group_type`, `title`, `description`

### `design_outcomes`

AACT source table; see the column list for available fields.

**Rows:** 3761914  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `outcome_type`, `measure`, `time_frame`, `population`, `description`  
**Potentially relevant to early termination:** `outcome_type`

### `designs`

Core study design characteristics, including allocation, masking, and intervention model.

**Rows:** 597720  
**Columns:** 14  
**Column names:** `id`, `nct_id`, `allocation`, `intervention_model`, `observational_model`, `primary_purpose`, `time_perspective`, `masking`, `masking_description`, `intervention_model_description`, `subject_masked`, `caregiver_masked`, `investigator_masked`, `outcomes_assessor_masked`  
**Potentially relevant to early termination:** `id`, `nct_id`, `allocation`, `intervention_model`, `observational_model`, `primary_purpose`, `time_perspective`, `masking`, `masking_description`, `intervention_model_description`, `subject_masked`, `caregiver_masked`, `investigator_masked`, `outcomes_assessor_masked`

### `detailed_descriptions`

Detailed study descriptions and protocol information.

**Rows:** 601530  
**Columns:** 3  
**Column names:** `id`, `nct_id`, `description`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `documents`

Documents associated with study records.

**Rows:** 10838  
**Columns:** 6  
**Column names:** `id`, `nct_id`, `document_id`, `document_type`, `url`, `comment`  
**Potentially relevant to early termination:** `document_type`

### `drop_withdrawals`

Participant drop and withdrawal counts or reasons.

**Rows:** 602414  
**Columns:** 10  
**Column names:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `period`, `reason`, `count`, `drop_withdraw_comment`, `reason_comment`, `count_units`  
**Potentially relevant to early termination:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `period`, `reason`, `count`, `drop_withdraw_comment`, `reason_comment`, `count_units`

### `eligibilities`

Eligibility criteria and participant population characteristics.

**Rows:** 601530  
**Columns:** 14  
**Column names:** `id`, `nct_id`, `sampling_method`, `gender`, `minimum_age`, `maximum_age`, `healthy_volunteers`, `population`, `criteria`, `gender_description`, `gender_based`, `adult`, `child`, `older_adult`  
**Potentially relevant to early termination:** `id`, `nct_id`, `sampling_method`, `gender`, `minimum_age`, `maximum_age`, `healthy_volunteers`, `population`, `criteria`, `gender_description`, `gender_based`, `adult`, `child`, `older_adult`

### `facilities`

Study facilities and site locations.

**Rows:** 3523526  
**Columns:** 10  
**Column names:** `id`, `nct_id`, `status`, `name`, `city`, `state`, `zip`, `country`, `latitude`, `longitude`  
**Potentially relevant to early termination:** `status`, `country`

### `facility_contacts`

Contacts associated with study facilities.

**Rows:** 421325  
**Columns:** 8  
**Column names:** `id`, `nct_id`, `facility_id`, `contact_type`, `name`, `email`, `phone`, `phone_extension`  
**Potentially relevant to early termination:** `id`, `nct_id`, `facility_id`, `contact_type`, `name`, `email`, `phone`, `phone_extension`

### `facility_investigators`

Investigators associated with study facilities.

**Rows:** 226624  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `facility_id`, `role`, `name`  
**Potentially relevant to early termination:** `id`, `nct_id`, `facility_id`, `role`, `name`

### `id_information`

Secondary study identifiers and identification information.

**Rows:** 796767  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `id_source`, `id_value`, `id_type`, `id_type_description`, `id_link`  
**Potentially relevant to early termination:** `id_type`, `id_type_description`

### `intervention_other_names`

Other names associated with study interventions.

**Rows:** 486506  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `intervention_id`, `name`  
**Potentially relevant to early termination:** `id`, `nct_id`, `intervention_id`, `name`

### `interventions`

Interventions, treatments, devices, drugs, or procedures studied.

**Rows:** 1019126  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `intervention_type`, `name`, `description`  
**Potentially relevant to early termination:** `id`, `nct_id`, `intervention_type`, `name`, `description`

### `ipd_information_types`

Types of individual participant data information reported.

**Rows:** 96041  
**Columns:** 3  
**Column names:** `id`, `nct_id`, `name`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `keywords`

Keywords associated with study records.

**Rows:** 1621095  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `name`, `downcase_name`  
**Potentially relevant to early termination:** `id`, `nct_id`, `name`, `downcase_name`

### `links`

External links associated with study records.

**Rows:** 75845  
**Columns:** 4  
**Column names:** `id`, `nct_id`, `url`, `description`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `milestones`

Study milestones and milestone dates or statuses.

**Rows:** 898711  
**Columns:** 10  
**Column names:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `title`, `period`, `description`, `count`, `milestone_description`, `count_units`  
**Potentially relevant to early termination:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `title`, `period`, `description`, `count`, `milestone_description`, `count_units`

### `outcome_analyses`

Statistical analyses associated with reported outcomes.

**Rows:** 326455  
**Columns:** 25  
**Column names:** `id`, `nct_id`, `outcome_id`, `non_inferiority_type`, `non_inferiority_description`, `param_type`, `param_value`, `dispersion_type`, `dispersion_value`, `p_value_modifier`, `p_value`, `ci_n_sides`, `ci_percent`, `ci_lower_limit`, `ci_upper_limit`, `ci_upper_limit_na_comment`, `p_value_description`, `method`, `method_description`, `estimate_description`, `groups_description`, `other_analysis_description`, `ci_upper_limit_raw`, `ci_lower_limit_raw`, `p_value_raw`  
**Potentially relevant to early termination:** `outcome_id`, `non_inferiority_type`, `param_type`, `dispersion_type`, `groups_description`

### `outcome_analysis_groups`

Groups used in reported outcome analyses.

**Rows:** 631153  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `outcome_analysis_id`, `result_group_id`, `ctgov_group_code`  
**Potentially relevant to early termination:** `outcome_analysis_id`, `result_group_id`, `ctgov_group_code`

### `outcome_counts`

Counts associated with reported outcome measurements.

**Rows:** 1608624  
**Columns:** 8  
**Column names:** `id`, `nct_id`, `outcome_id`, `result_group_id`, `ctgov_group_code`, `scope`, `units`, `count`  
**Potentially relevant to early termination:** `outcome_id`, `result_group_id`, `ctgov_group_code`

### `outcome_measurements`

Reported outcome measurement values.

**Rows:** 4995195  
**Columns:** 21  
**Column names:** `id`, `nct_id`, `outcome_id`, `result_group_id`, `ctgov_group_code`, `classification`, `category`, `title`, `description`, `units`, `param_type`, `param_value`, `param_value_num`, `dispersion_type`, `dispersion_value`, `dispersion_value_num`, `dispersion_lower_limit`, `dispersion_upper_limit`, `explanation_of_na`, `dispersion_upper_limit_raw`, `dispersion_lower_limit_raw`  
**Potentially relevant to early termination:** `outcome_id`, `result_group_id`, `ctgov_group_code`, `param_type`, `dispersion_type`

### `outcomes`

Primary and secondary outcome definitions.

**Rows:** 666333  
**Columns:** 13  
**Column names:** `id`, `nct_id`, `outcome_type`, `title`, `description`, `time_frame`, `population`, `anticipated_posting_date`, `anticipated_posting_month_year`, `units`, `units_analyzed`, `dispersion_type`, `param_type`  
**Potentially relevant to early termination:** `outcome_type`, `anticipated_posting_date`, `anticipated_posting_month_year`, `dispersion_type`, `param_type`

### `overall_officials`

Study officials and their roles.

**Rows:** 534026  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `role`, `name`, `affiliation`  
**Potentially relevant to early termination:** `id`, `nct_id`, `role`, `name`, `affiliation`

### `participant_flows`

Participant flow information through study periods and groups.

**Rows:** 80079  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `recruitment_details`, `pre_assignment_details`, `units_analyzed`  
**Potentially relevant to early termination:** `id`, `nct_id`, `recruitment_details`, `pre_assignment_details`, `units_analyzed`

### `pending_results`

Pending or incomplete results information.

**Rows:** 33512  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `event`, `event_date_description`, `event_date`  
**Potentially relevant to early termination:** `event`, `event_date_description`, `event_date`

### `provided_documents`

Documents provided with study records.

**Rows:** 85636  
**Columns:** 8  
**Column names:** `id`, `nct_id`, `document_type`, `has_protocol`, `has_icf`, `has_sap`, `document_date`, `url`  
**Potentially relevant to early termination:** `document_type`, `document_date`

### `reported_events`

Reported adverse events and other events.

**Rows:** 12034973  
**Columns:** 17  
**Column names:** `id`, `nct_id`, `result_group_id`, `ctgov_group_code`, `time_frame`, `event_type`, `default_vocab`, `default_assessment`, `subjects_affected`, `subjects_at_risk`, `description`, `event_count`, `organ_system`, `adverse_event_term`, `frequency_threshold`, `vocab`, `assessment`  
**Potentially relevant to early termination:** `result_group_id`, `ctgov_group_code`, `event_type`, `event_count`, `adverse_event_term`

### `reported_event_totals`

Aggregate reported event totals.

**Rows:** 604152  
**Columns:** 9  
**Column names:** `id`, `nct_id`, `ctgov_group_code`, `event_type`, `classification`, `subjects_affected`, `subjects_at_risk`, `created_at`, `updated_at`  
**Potentially relevant to early termination:** `ctgov_group_code`, `event_type`, `updated_at`

### `responsible_parties`

Responsible party information for study records.

**Rows:** 584077  
**Columns:** 8  
**Column names:** `id`, `nct_id`, `responsible_party_type`, `name`, `title`, `organization`, `affiliation`, `old_name_title`  
**Potentially relevant to early termination:** `id`, `nct_id`, `responsible_party_type`, `name`, `title`, `organization`, `affiliation`, `old_name_title`

### `result_agreements`

Agreements associated with study results.

**Rows:** 80079  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `pi_employee`, `agreement`, `restriction_type`, `other_details`, `restrictive_agreement`  
**Potentially relevant to early termination:** `restriction_type`

### `result_contacts`

Contacts associated with study results.

**Rows:** 80079  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `organization`, `name`, `phone`, `email`, `extension`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `result_groups`

Groups used in study results.

**Rows:** 2217791  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `ctgov_group_code`, `result_type`, `title`, `description`, `outcome_id`  
**Potentially relevant to early termination:** `ctgov_group_code`, `result_type`, `outcome_id`

### `retractions`

Retraction or data-quality records associated with studies.

**Rows:** 335  
**Columns:** 5  
**Column names:** `id`, `reference_id`, `pmid`, `source`, `nct_id`  
**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.

### `search_results`

Search result metadata.

**Rows:** 0  
**Columns:** 7  
**Column names:** `id`, `nct_id`, `name`, `created_at`, `updated_at`, `grouping`, `study_search_id`  
**Potentially relevant to early termination:** `updated_at`, `grouping`

### `search_term_results`

Study matches for search terms.

**Rows:** 513966  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `search_term_id`, `created_at`, `updated_at`  
**Potentially relevant to early termination:** `updated_at`

### `search_terms`

Search terms used in the source data.

**Rows:** 186  
**Columns:** 5  
**Column names:** `id`, `term`, `group`, `created_at`, `updated_at`  
**Potentially relevant to early termination:** `group`, `updated_at`

### `sponsors`

Sponsors and collaborators associated with studies.

**Rows:** 960581  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `agency_class`, `lead_or_collaborator`, `name`  
**Potentially relevant to early termination:** `id`, `nct_id`, `agency_class`, `lead_or_collaborator`, `name`

### `studies`

One record per study with status, dates, phase, enrollment, design summary, and high-level protocol fields.

**Rows:** 602514  
**Columns:** 71  
**Column names:** `nct_id`, `nlm_download_date_description`, `study_first_submitted_date`, `results_first_submitted_date`, `disposition_first_submitted_date`, `last_update_submitted_date`, `study_first_submitted_qc_date`, `study_first_posted_date`, `study_first_posted_date_type`, `results_first_submitted_qc_date`, `results_first_posted_date`, `results_first_posted_date_type`, `disposition_first_submitted_qc_date`, `disposition_first_posted_date`, `disposition_first_posted_date_type`, `last_update_submitted_qc_date`, `last_update_posted_date`, `last_update_posted_date_type`, `start_month_year`, `start_date_type`, `start_date`, `verification_month_year`, `verification_date`, `completion_month_year`, `completion_date_type`, `completion_date`, `primary_completion_month_year`, `primary_completion_date_type`, `primary_completion_date`, `target_duration`, `study_type`, `acronym`, `baseline_population`, `brief_title`, `official_title`, `overall_status`, `last_known_status`, `phase`, `enrollment`, `enrollment_type`, `source`, `limitations_and_caveats`, `number_of_arms`, `number_of_groups`, `why_stopped`, `has_expanded_access`, `expanded_access_type_individual`, `expanded_access_type_intermediate`, `expanded_access_type_treatment`, `has_dmc`, `is_fda_regulated_drug`, `is_fda_regulated_device`, `is_unapproved_device`, `is_ppsd`, `is_us_export`, `biospec_retention`, `biospec_description`, `ipd_time_frame`, `ipd_access_criteria`, `ipd_url`, `plan_to_share_ipd`, `plan_to_share_ipd_description`, `created_at`, `updated_at`, `source_class`, `delayed_posting`, `expanded_access_nctid`, `expanded_access_status_for_nctid`, `fdaaa801_violation`, `baseline_type_units_analyzed`, `patient_registry`  
**Potentially relevant to early termination:** `nct_id`, `nlm_download_date_description`, `study_first_submitted_date`, `results_first_submitted_date`, `disposition_first_submitted_date`, `last_update_submitted_date`, `study_first_submitted_qc_date`, `study_first_posted_date`, `study_first_posted_date_type`, `results_first_submitted_qc_date`, `results_first_posted_date`, `results_first_posted_date_type`, `disposition_first_submitted_qc_date`, `disposition_first_posted_date`, `disposition_first_posted_date_type`, `last_update_submitted_qc_date`, `last_update_posted_date`, `last_update_posted_date_type`, `start_month_year`, `start_date_type`, `start_date`, `verification_month_year`, `verification_date`, `completion_month_year`, `completion_date_type`, `completion_date`, `primary_completion_month_year`, `primary_completion_date_type`, `primary_completion_date`, `target_duration`, `study_type`, `acronym`, `baseline_population`, `brief_title`, `official_title`, `overall_status`, `last_known_status`, `phase`, `enrollment`, `enrollment_type`, `source`, `limitations_and_caveats`, `number_of_arms`, `number_of_groups`, `why_stopped`, `has_expanded_access`, `expanded_access_type_individual`, `expanded_access_type_intermediate`, `expanded_access_type_treatment`, `has_dmc`, `is_fda_regulated_drug`, `is_fda_regulated_device`, `is_unapproved_device`, `is_ppsd`, `is_us_export`, `biospec_retention`, `biospec_description`, `ipd_time_frame`, `ipd_access_criteria`, `ipd_url`, `plan_to_share_ipd`, `plan_to_share_ipd_description`, `created_at`, `updated_at`, `source_class`, `delayed_posting`, `expanded_access_nctid`, `expanded_access_status_for_nctid`, `fdaaa801_violation`, `baseline_type_units_analyzed`, `patient_registry`

### `study_references`

References cited by study records.

**Rows:** 1140120  
**Columns:** 5  
**Column names:** `id`, `nct_id`, `pmid`, `reference_type`, `citation`  
**Potentially relevant to early termination:** `reference_type`

