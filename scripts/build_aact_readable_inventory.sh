#!/usr/bin/env bash
set -euo pipefail

archive=${1:?Usage: build_aact_readable_inventory.sh ARCHIVE COLUMN_INVENTORY OUTPUT_MD}
column_inventory=${2:?Usage: build_aact_readable_inventory.sh ARCHIVE COLUMN_INVENTORY OUTPUT_MD}
output=${3:?Usage: build_aact_readable_inventory.sh ARCHIVE COLUMN_INVENTORY OUTPUT_MD}

mkdir -p "$(dirname "$output")"

archive_name=$(basename "$archive")
snapshot_date=$(basename "$(dirname "$archive")")
checksum=$(sha256sum "$archive" | awk '{print $1}')

description_for() {
  case "$1" in
    baseline_counts) printf '%s' 'Participant baseline counts reported for result groups.' ;;
    baseline_measurements) printf '%s' 'Participant baseline measurements reported for result groups.' ;;
    brief_summaries) printf '%s' 'Brief structured summaries of study records.' ;;
    browse_conditions) printf '%s' 'Normalized condition terms used for browsing and indexing studies.' ;;
    browse_interventions) printf '%s' 'Normalized intervention terms used for browsing and indexing studies.' ;;
    calculated_values) printf '%s' 'AACT-calculated study and result values.' ;;
    central_contacts) printf '%s' 'Central study contact information.' ;;
    conditions) printf '%s' 'Conditions and diseases investigated by each study.' ;;
    countries) printf '%s' 'Countries in which study sites are located.' ;;
    design_group_interventions) printf '%s' 'Interventions assigned to design groups or arms.' ;;
    design_groups) printf '%s' 'Study design groups, cohorts, or arms.' ;;
    designs) printf '%s' 'Core study design characteristics, including allocation, masking, and intervention model.' ;;
    detailed_descriptions) printf '%s' 'Detailed study descriptions and protocol information.' ;;
    documents) printf '%s' 'Documents associated with study records.' ;;
    drop_withdrawals) printf '%s' 'Participant drop and withdrawal counts or reasons.' ;;
    eligibilities) printf '%s' 'Eligibility criteria and participant population characteristics.' ;;
    facilities) printf '%s' 'Study facilities and site locations.' ;;
    facility_contacts) printf '%s' 'Contacts associated with study facilities.' ;;
    facility_investigators) printf '%s' 'Investigators associated with study facilities.' ;;
    id_information) printf '%s' 'Secondary study identifiers and identification information.' ;;
    intervention_other_names) printf '%s' 'Other names associated with study interventions.' ;;
    interventions) printf '%s' 'Interventions, treatments, devices, drugs, or procedures studied.' ;;
    ipd_information_types) printf '%s' 'Types of individual participant data information reported.' ;;
    keywords) printf '%s' 'Keywords associated with study records.' ;;
    links) printf '%s' 'External links associated with study records.' ;;
    milestones) printf '%s' 'Study milestones and milestone dates or statuses.' ;;
    outcome_analyses) printf '%s' 'Statistical analyses associated with reported outcomes.' ;;
    outcome_analysis_groups) printf '%s' 'Groups used in reported outcome analyses.' ;;
    outcome_counts) printf '%s' 'Counts associated with reported outcome measurements.' ;;
    outcome_measurements) printf '%s' 'Reported outcome measurement values.' ;;
    outcomes) printf '%s' 'Primary and secondary outcome definitions.' ;;
    overall_officials) printf '%s' 'Study officials and their roles.' ;;
    participant_flows) printf '%s' 'Participant flow information through study periods and groups.' ;;
    pending_results) printf '%s' 'Pending or incomplete results information.' ;;
    provided_documents) printf '%s' 'Documents provided with study records.' ;;
    reported_event_totals) printf '%s' 'Aggregate reported event totals.' ;;
    reported_events) printf '%s' 'Reported adverse events and other events.' ;;
    responsible_parties) printf '%s' 'Responsible party information for study records.' ;;
    result_agreements) printf '%s' 'Agreements associated with study results.' ;;
    result_contacts) printf '%s' 'Contacts associated with study results.' ;;
    result_groups) printf '%s' 'Groups used in study results.' ;;
    retractions) printf '%s' 'Retraction or data-quality records associated with studies.' ;;
    search_results) printf '%s' 'Search result metadata.' ;;
    search_term_results) printf '%s' 'Study matches for search terms.' ;;
    search_terms) printf '%s' 'Search terms used in the source data.' ;;
    sponsors) printf '%s' 'Sponsors and collaborators associated with studies.' ;;
    studies) printf '%s' 'One record per study with status, dates, phase, enrollment, design summary, and high-level protocol fields.' ;;
    study_references) printf '%s' 'References cited by study records.' ;;
    *) printf '%s' 'AACT source table; see the column list for available fields.' ;;
  esac
}

markdown_columns() {
  printf '%s' "$1" | tr '|' '\n' | awk 'BEGIN { first=1 } { if (!first) printf ", "; printf "`%s`", $0; first=0 }'
}

relevant_columns() {
  local table=$1
  awk -F '\t' -v table="$table" 'BEGIN { first=1 } $1 == table && $3 == "Core" { if (!first) printf ", "; printf "`%s`", $2; first=0 }' "$column_inventory"
}

{
  printf '# AACT Flat-File Inventory: %s\n\n' "$snapshot_date"
  printf 'Source archive: `%s`  \n' "$archive_name"
  printf 'Archive SHA-256: `%s`  \n' "$checksum"
  printf 'Source: [AACT official downloads](https://aact.ctti-clinicaltrials.org/downloads)\n\n'
  printf 'This report inventories every table in the preserved ZIP. Row counts are data rows excluding the header. Headers and row data were streamed directly from the archive; no raw files were cleaned, deleted, modified, extracted, or reorganized.\n\n'
  printf '## Research focus\n\n'
  printf 'Potential relevance is an initial screening judgment for the question: **What factors are associated with early termination of clinical trials?** Core columns include trial status and stopping reason, phase, enrollment, sponsor, condition, intervention, design, arms, sites, dates, randomization or allocation, and masking. This is an inventory only, not a final analysis dataset or variable-selection decision.\n\n'
  printf '## Summary\n\n'
  printf '| Tables | Inventory columns |\n| ---: | ---: |\n'
  printf '| %s | %s |\n\n' "$(unzip -Z1 "$archive" '*.txt' | wc -l)" "$(tail -n +2 "$column_inventory" | wc -l)"
  printf '## Tables\n\n'

  while IFS= read -r table_file; do
    table=${table_file%.txt}
    header=$(unzip -p "$archive" "$table_file" | sed -n '1p' | tr -d '\r')
    column_count=$(printf '%s' "$header" | awk -F '|' '{print NF}')
    row_count=$(unzip -p "$archive" "$table_file" | awk 'NR > 1 { count++ } END { print count + 0 }')

    printf '### `%s`\n\n' "$table"
    printf '%s\n\n' "$(description_for "$table")"
    printf '**Rows:** %s  \n' "$row_count"
    printf '**Columns:** %s  \n' "$column_count"
    printf '**Column names:** %s  \n' "$(markdown_columns "$header")"
    core=$(relevant_columns "$table")
    if [[ -n "$core" ]]; then
      printf '**Potentially relevant to early termination:** %s\n\n' "$core"
    else
      printf '**Potentially relevant to early termination:** None identified in the initial screening; retain the table for linkage or exploratory review.\n\n'
    fi
  done < <(unzip -Z1 "$archive" '*.txt' | sort)
} > "$output"