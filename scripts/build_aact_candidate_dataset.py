#!/usr/bin/env python3
"""Build a transparent, study-level AACT candidate dataset.

The source ZIP is read only. One-to-many AACT tables are aggregated by nct_id;
no studies or variables are filtered out because of missing values.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import re
import sqlite3
import tempfile
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path


OUTPUT_COLUMNS = [
    "nct_id", "overall_status", "terminated_binary", "why_stopped",
    "last_known_status", "study_type", "phase", "enrollment",
    "enrollment_type", "lead_sponsor_type", "lead_sponsor_organization",
    "sponsor_types", "sponsor_organizations", "sponsor_count",
    "primary_condition", "conditions_all", "intervention_count",
    "intervention_names", "intervention_types", "placebo_used",
    "primary_outcome_type", "primary_outcome_types_all", "primary_outcome_count",
    "number_of_arms", "number_of_groups", "number_of_sites",
    "allocation", "randomized_binary", "randomized_vs_nonrandomized",
    "intervention_model", "masking", "primary_purpose", "observational_model",
    "time_perspective", "study_start_date", "study_completion_date",
    "start_year", "completion_year", "study_duration_days",
]

TABLE_COLUMNS = {
    "studies": [
        "nct_id", "overall_status", "why_stopped", "last_known_status",
        "study_type", "phase", "enrollment", "enrollment_type",
        "number_of_arms", "number_of_groups", "start_date", "completion_date",
    ],
}


def clean(value: str | None) -> str:
    return str(value).strip() if value is not None else ""


def unique_join(values: list[str]) -> str:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = clean(value)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return "|".join(result)


def parse_full_date(value: str) -> date | None:
    value = clean(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def add_table(conn: sqlite3.Connection, archive: zipfile.ZipFile, table: str) -> None:
    definitions = {
        "studies": """CREATE TABLE studies (
            nct_id TEXT, overall_status TEXT, why_stopped TEXT,
            last_known_status TEXT, study_type TEXT, phase TEXT,
            enrollment TEXT, enrollment_type TEXT, number_of_arms TEXT,
            number_of_groups TEXT, start_date TEXT, completion_date TEXT)""",
        "designs": """CREATE TABLE designs (
            nct_id TEXT, allocation TEXT, intervention_model TEXT,
            masking TEXT, primary_purpose TEXT, observational_model TEXT,
            time_perspective TEXT)""",
        "interventions": """CREATE TABLE interventions (
            id TEXT, nct_id TEXT, intervention_type TEXT, name TEXT, description TEXT)""",
        "conditions": "CREATE TABLE conditions (id TEXT, nct_id TEXT, name TEXT)",
        "facilities": "CREATE TABLE facilities (id TEXT, nct_id TEXT, name TEXT)",
        "sponsors": "CREATE TABLE sponsors (id TEXT, nct_id TEXT, agency_class TEXT, lead_or_collaborator TEXT, name TEXT)",
        "outcomes": "CREATE TABLE outcomes (id TEXT, nct_id TEXT, outcome_type TEXT)",
    }
    conn.execute(definitions[table])
    default_columns = {
        "designs": ["nct_id", "allocation", "intervention_model", "masking", "primary_purpose", "observational_model", "time_perspective"],
        "interventions": ["id", "nct_id", "intervention_type", "name", "description"],
        "conditions": ["id", "nct_id", "name"],
        "facilities": ["id", "nct_id", "name"],
        "sponsors": ["id", "nct_id", "agency_class", "lead_or_collaborator", "name"],
        "outcomes": ["id", "nct_id", "outcome_type"],
    }
    columns = TABLE_COLUMNS.get(table) or default_columns[table]
    placeholders = ",".join("?" for _ in columns)
    insert = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    with archive.open(f"{table}.txt") as binary:
        text = (line.decode("utf-8", errors="replace") for line in binary)
        reader = csv.DictReader(text, delimiter="|")
        batch: list[tuple[str, ...]] = []
        for row in reader:
            batch.append(tuple(clean(row.get(column)) for column in columns))
            if len(batch) >= 10000:
                conn.executemany(insert, batch)
                batch.clear()
    if batch:
        conn.executemany(insert, batch)
    conn.commit()


def build_candidate(archive_path: Path, output_path: Path, report_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as archive, tempfile.NamedTemporaryFile(suffix=".sqlite") as temp:
        conn = sqlite3.connect(temp.name)
        for table in ("studies", "designs", "interventions", "conditions", "facilities", "sponsors", "outcomes"):
            add_table(conn, archive, table)

        conn.executescript("""
        CREATE INDEX studies_nct ON studies(nct_id);
        CREATE INDEX designs_nct ON designs(nct_id);
        CREATE INDEX interventions_nct ON interventions(nct_id);
        CREATE INDEX conditions_nct ON conditions(nct_id);
        CREATE INDEX facilities_nct ON facilities(nct_id);
        CREATE INDEX sponsors_nct ON sponsors(nct_id);
        CREATE INDEX outcomes_nct ON outcomes(nct_id);
        """)
        conn.commit()

        query = """
        SELECT s.*,
          (SELECT group_concat(DISTINCT allocation) FROM designs d WHERE d.nct_id=s.nct_id AND allocation<>'') AS allocation,
          (SELECT group_concat(DISTINCT intervention_model) FROM designs d WHERE d.nct_id=s.nct_id AND intervention_model<>'') AS intervention_model,
          (SELECT group_concat(DISTINCT masking) FROM designs d WHERE d.nct_id=s.nct_id AND masking<>'') AS masking,
          (SELECT group_concat(DISTINCT primary_purpose) FROM designs d WHERE d.nct_id=s.nct_id AND primary_purpose<>'') AS primary_purpose,
          (SELECT group_concat(DISTINCT observational_model) FROM designs d WHERE d.nct_id=s.nct_id AND observational_model<>'') AS observational_model,
          (SELECT group_concat(DISTINCT time_perspective) FROM designs d WHERE d.nct_id=s.nct_id AND time_perspective<>'') AS time_perspective,
          (SELECT count(DISTINCT id) FROM interventions i WHERE i.nct_id=s.nct_id) AS intervention_count,
          (SELECT group_concat(DISTINCT name) FROM interventions i WHERE i.nct_id=s.nct_id AND name<>'') AS intervention_names,
          (SELECT group_concat(DISTINCT intervention_type) FROM interventions i WHERE i.nct_id=s.nct_id AND intervention_type<>'') AS intervention_types,
          (SELECT CASE WHEN EXISTS (SELECT 1 FROM interventions i WHERE i.nct_id=s.nct_id AND lower(i.name || ' ' || i.description) LIKE '%placebo%') THEN 'yes' WHEN EXISTS (SELECT 1 FROM interventions i WHERE i.nct_id=s.nct_id) THEN 'no' ELSE '' END) AS placebo_used,
          (SELECT group_concat(DISTINCT name) FROM conditions c WHERE c.nct_id=s.nct_id AND name<>'') AS conditions_all,
          (SELECT name FROM conditions c WHERE c.nct_id=s.nct_id AND name<>'' ORDER BY CAST(id AS INTEGER), id LIMIT 1) AS primary_condition,
          (SELECT count(DISTINCT id) FROM facilities f WHERE f.nct_id=s.nct_id) AS number_of_sites,
          (SELECT group_concat(DISTINCT agency_class) FROM sponsors sp WHERE sp.nct_id=s.nct_id AND agency_class<>'') AS sponsor_types,
          (SELECT group_concat(DISTINCT name) FROM sponsors sp WHERE sp.nct_id=s.nct_id AND name<>'') AS sponsor_organizations,
          (SELECT count(DISTINCT id) FROM sponsors sp WHERE sp.nct_id=s.nct_id) AS sponsor_count,
          (SELECT agency_class FROM sponsors sp WHERE sp.nct_id=s.nct_id AND lower(lead_or_collaborator)='lead' ORDER BY CAST(id AS INTEGER), id LIMIT 1) AS lead_sponsor_type,
          (SELECT name FROM sponsors sp WHERE sp.nct_id=s.nct_id AND lower(lead_or_collaborator)='lead' ORDER BY CAST(id AS INTEGER), id LIMIT 1) AS lead_sponsor_organization,
          (SELECT group_concat(DISTINCT outcome_type) FROM outcomes o WHERE o.nct_id=s.nct_id AND upper(outcome_type)='PRIMARY') AS primary_outcome_types_all,
          (SELECT count(*) FROM outcomes o WHERE o.nct_id=s.nct_id AND upper(outcome_type)='PRIMARY') AS primary_outcome_count
        FROM studies s ORDER BY s.nct_id
        """
        cursor = conn.execute(query)
        source_names = [column[0] for column in cursor.description]
        source_index = {name: index for index, name in enumerate(source_names)}
        report_rows: list[dict[str, str]] = []
        with gzip.open(output_path, "wt", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=OUTPUT_COLUMNS, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in cursor:
                values = {name: clean(row[index]) for name, index in source_index.items()}
                start = parse_full_date(values["start_date"])
                completion = parse_full_date(values["completion_date"])
                duration = (completion - start).days if start and completion and completion >= start else ""
                allocation = values.get("allocation", "")
                status = values.get("overall_status", "")
                randomized = "1" if allocation.upper() == "RANDOMIZED" else "0" if allocation else ""
                randomized_class = "randomized" if randomized == "1" else "non-randomized" if randomized == "0" else "not reported"
                primary_types = values.get("primary_outcome_types_all", "")
                values.update({
                    "terminated_binary": "1" if status.upper() == "TERMINATED" else "0",
                    "study_start_date": values.pop("start_date"),
                    "study_completion_date": values.pop("completion_date"),
                    "start_year": str(start.year) if start else "",
                    "completion_year": str(completion.year) if completion else "",
                    "study_duration_days": str(duration) if duration != "" else "",
                    "randomized_binary": randomized,
                    "randomized_vs_nonrandomized": randomized_class,
                    "primary_outcome_type": primary_types.split(",")[0] if primary_types else "",
                })
                values["number_of_arms"] = values.get("number_of_arms", "")
                values["number_of_groups"] = values.get("number_of_groups", "")
                writer.writerow({column: values.get(column, "") for column in OUTPUT_COLUMNS})
                report_rows.append({column: values.get(column, "") for column in OUTPUT_COLUMNS})
        write_report(report_path, archive_path, report_rows)
        conn.close()


def format_number(value: float) -> str:
    return f"{value:,.2f}" if value % 1 else f"{value:,.0f}"


def distribution(rows: list[dict[str, str]], column: str, limit: int = 20) -> list[tuple[str, int]]:
    counts = Counter(row.get(column, "") or "[missing]" for row in rows)
    return counts.most_common(limit)


def numeric_summary(rows: list[dict[str, str]], column: str) -> tuple[int, int, str, str, str, str, str]:
    missing = sum(not row.get(column, "") for row in rows)
    values = sorted(float(row[column]) for row in rows if row.get(column, "") != "")
    if not values:
        return len(rows), missing, "", "", "", "", ""
    def percentile(p: float) -> float:
        position = (len(values) - 1) * p
        low, high = int(position), min(int(position) + 1, len(values) - 1)
        return values[low] + (values[high] - values[low]) * (position - low)
    return len(rows), missing, *(format_number(value) for value in (min(values), percentile(.25), percentile(.5), percentile(.75), max(values)))


def write_report(path: Path, archive: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Proposed AACT Trial-Termination Analysis Dataset",
        "",
        "This is a study-level candidate dataset derived from the preserved AACT ZIP. The raw archive was read only and was not extracted, modified, deleted, or reorganized. No studies were excluded for missing values, status, phase, or study type. No final complexity score, machine-learning model, or causal analysis was created.",
        "",
        f"- Source archive: `{archive}`",
        f"- Candidate output: `data/processed/aact_trial_termination_candidate_2026-09-12.tsv.gz`",
        f"- Studies available: **{len(rows):,}**",
        f"- Unique NCT IDs: **{len({row['nct_id'] for row in rows if row['nct_id']}):,}**",
        f"- Duplicate NCT IDs: **{len(rows) - len({row['nct_id'] for row in rows if row['nct_id']}):,}**",
        "",
        "## Construction rules",
        "",
        "- The `studies` table is the study spine; one output row is emitted per AACT `studies` row.",
        "- Conditions, interventions, sponsors, facilities, designs, and outcomes are aggregated by `nct_id`; original source values are retained as delimited text where multiple values exist.",
        "- `primary_condition` is the first condition by source ID order; `conditions_all` preserves all condition names. No therapeutic-area classification was assigned.",
        "- `placebo_used` is `yes` when an intervention name or description contains `placebo`, `no` when interventions exist but no placebo text is found, and missing when no intervention is reported.",
        "- `randomized_binary` reflects exact AACT allocation `RANDOMIZED`; blank allocation is kept as missing. `terminated_binary` is 1 for `overall_status=TERMINATED` and 0 otherwise. Comparison-group eligibility remains undecided; all original status categories are reported below.",
        "- `study_duration_days` is calculated only from full valid `YYYY-MM-DD` start and completion dates with completion on or after start. Partial, invalid, reversed, or missing dates produce missing duration.",
        "",
        "## Proposed variables",
        "",
        """| Variable | Source or derivation | Purpose |
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
| `study_duration_days` | valid completion minus start date | Observed study duration |""",
        "",
        "## Required distributions",
        "",
    ]
    categorical = [
        ("Overall status", "overall_status"), ("Phase", "phase"), ("Study type", "study_type"),
        ("Randomized classification", "randomized_vs_nonrandomized"), ("Placebo use", "placebo_used"),
        ("Sponsor type", "lead_sponsor_type"), ("Primary outcome type", "primary_outcome_type"),
        ("Reasons for stopping", "why_stopped"), ("Primary condition (top 20)", "primary_condition"),
    ]
    for title, column in categorical:
        lines += [f"### {title}", "", "| Category | Count |", "| --- | ---: |"]
        lines += [f"| {value} | {count:,} |" for value, count in distribution(rows, column)]
        lines.append("")
    for title, column in [("Interventions per study", "intervention_count"), ("Sites per study", "number_of_sites"), ("Enrollment", "enrollment"), ("Study duration (days)", "study_duration_days")]:
        total, missing, minimum, p25, median, p75, maximum = numeric_summary(rows, column)
        lines += [f"### {title}", "", f"Non-missing: **{total - missing:,}**; missing: **{missing:,}** ({missing / total * 100:.2f}%)", "", "| Minimum | P25 | Median | P75 | Maximum |", "| ---: | ---: | ---: | ---: | ---: |", f"| {minimum or '[none]'} | {p25 or '[none]'} | {median or '[none]'} | {p75 or '[none]'} | {maximum or '[none]'} |", ""]
    lines += ["## Missingness for every proposed variable", "", "| Variable | Missing | Missing % |", "| --- | ---: | ---: |"]
    for column in OUTPUT_COLUMNS:
        missing = sum(not row.get(column, "") for row in rows)
        lines.append(f"| `{column}` | {missing:,} | {missing / len(rows) * 100:.2f}% |")
    lines += ["", "## Interpretation boundary", "", "This dataset is intentionally a complete candidate set. The reported `terminated_binary` coding identifies terminated records but does not decide which non-terminated statuses should form a comparison group. Phase, status, sponsor, condition, and design categories are reported as supplied by AACT; future therapeutic-area grouping and complexity measurement require an explicit, documented decision.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    build_candidate(args.archive, args.output, args.report)