#!/usr/bin/env bash
set -euo pipefail

archive=${1:?Usage: build_aact_inventory.sh ARCHIVE OUTPUT_TSV}
output=${2:?Usage: build_aact_inventory.sh ARCHIVE OUTPUT_TSV}

mkdir -p "$(dirname "$output")"
printf 'table\tcolumn\trelevance\treason\n' > "$output"

while IFS= read -r table_file; do
  table=${table_file%.txt}
  header=$(unzip -p "$archive" "$table_file" | sed -n '1p' | tr -d '\r')

  IFS='|' read -r -a columns <<< "$header"
  for column in "${columns[@]}"; do
    relevance=Context
    reason='Available in the source table; retain for exploratory analysis or linkage.'

    if [[ "$table" == "studies" ]]; then
      relevance=Core
      reason='Study-level status, timing, design, enrollment, sponsor, or regulatory context.'
    elif [[ "$table" == "conditions" || "$table" == "browse_conditions" || "$table" == "keywords" ]]; then
      relevance=Core
      reason='Condition or topic associated with the study.'
    elif [[ "$table" == "interventions" || "$table" == "intervention_other_names" || "$table" == "browse_interventions" || "$table" == "design_group_interventions" ]]; then
      relevance=Core
      reason='Intervention, treatment group, or intervention classification associated with the study.'
    elif [[ "$table" == "designs" || "$table" == "design_groups" || "$table" == "eligibilities" || "$table" == "milestones" || "$table" == "drop_withdrawals" || "$table" == "participant_flows" ]]; then
      relevance=Core
      reason='Study design, eligibility, progress, withdrawal, or participant-flow information.'
    elif [[ "$table" == "sponsors" || "$table" == "overall_officials" || "$table" == "responsible_parties" || "$table" == "central_contacts" || "$table" == "facility_contacts" || "$table" == "facility_investigators" ]]; then
      relevance=Core
      reason='Sponsor, responsible party, investigator, contact, or site information.'
    elif [[ "$table" == "id_information" || "$table" == "links" || "$table" == "study_references" || "$table" == "documents" || "$table" == "provided_documents" ]]; then
      relevance=Supporting
      reason='Study identifiers, references, linked records, or documents useful for provenance and enrichment.'
    elif [[ "$table" == "countries" || "$table" == "facilities" ]]; then
      relevance=Supporting
      reason='Geographic or site-level context that may be associated with study continuation or termination.'
    elif [[ "$table" == "retractions" || "$table" == "search_terms" || "$table" == "search_term_results" || "$table" == "search_results" ]]; then
      relevance=Supporting
      reason='Data quality, search, or retraction metadata that may affect cohort construction.'
    elif [[ "$table" == "baseline_counts" || "$table" == "baseline_measurements" || "$table" == "outcomes" || "$table" == "outcome_analyses" || "$table" == "outcome_analysis_groups" || "$table" == "outcome_counts" || "$table" == "outcome_measurements" || "$table" == "reported_events" || "$table" == "reported_event_totals" || "$table" == "result_groups" || "$table" == "result_agreements" || "$table" == "result_contacts" || "$table" == "pending_results" ]]; then
      relevance=Supporting
      reason='Results, outcomes, or adverse-event context potentially associated with study status or termination.'
    fi

    if [[ "$column" =~ (status|stopp|withdraw|terminat|phase|enroll|sponsor|condition|intervention|design|date|month|year|start|complet|finish|recruit|arm|group|allocat|mask|observ|purpose|perspective|eligib|age|sex|gender|country|facility|location|official|responsib|why|reason|endpoint|outcome|event|adverse|milestone|contact|type) ]]; then
      relevance=Core
      reason='Column name indicates a plausible termination predictor, outcome, timing, design, sponsor, population, intervention, or study-status feature.'
    fi

    printf '%s\t%s\t%s\t%s\n' "$table" "$column" "$relevance" "$reason" >> "$output"
  done
done < <(unzip -Z1 "$archive" '*.txt' | sort)