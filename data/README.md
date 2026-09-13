# AACT data

## Raw snapshot

The raw AACT flat-file snapshot is preserved at:

`data/raw/2026-09-12/20260912_export_ctgov.zip`

Source: [AACT official downloads](https://aact.ctti-clinicaltrials.org/downloads)

- Snapshot date: 2026-09-12
- Archive: `20260912_export_ctgov.zip`
- Format: pipe-delimited text files, one file per AACT table
- SHA-256: `838406738300d3f2766e33ce5457f287ecd172fec227d4229755bed35297a05c`
- Tables in archive: 49
- Compressed size: 2,528,358,195 bytes

The archive is the original downloaded object and must not be edited, filtered, or
repacked. The inventory is generated from table headers inside the ZIP, so the
large raw files do not need to be extracted or duplicated.

## Inventory

`inventory/aact_2026-09-12_columns.tsv` is a complete table-and-column inventory.
It includes a preliminary relevance classification for termination analysis:

`inventory/aact_2026-09-12_readable.md` is the reviewable inventory with row
counts, column counts, complete column-name lists, table descriptions, and
potentially relevant columns for early-termination research.

- `Core`: directly represents study status, termination reason, design, timing, enrollment, sponsor, condition, intervention, population, sites, or related predictors.
- `Supporting`: useful results, provenance, linkage, geographic, or data-quality context.
- `Context`: available source columns not yet assigned a specific termination-analysis role.

The classification is an initial screening aid, not a deletion list. No source
variables have been removed.

Regenerate the inventory with:

```sh
./scripts/build_aact_inventory.sh \
  data/raw/2026-09-12/20260912_export_ctgov.zip \
  data/inventory/aact_2026-09-12_columns.tsv
```

## Proposed analysis dataset

The study-level candidate dataset is stored separately from the raw archive:

- `processed/aact_trial_termination_candidate_2026-09-12.tsv.gz`
- `processed/aact_trial_termination_candidate_2026-09-12_report.md`

The candidate dataset contains 602,514 study rows and 39 proposed variables.
It preserves all study-status categories and does not remove records or
variables because of missingness. The report documents the aggregation rules,
distributions, missing percentages, and the unresolved decision about which
non-terminated statuses should form a comparison group.

Regenerate it with:

```sh
python3 scripts/build_aact_candidate_dataset.py \
  data/raw/2026-09-12/20260912_export_ctgov.zip \
  data/processed/aact_trial_termination_candidate_2026-09-12.tsv.gz \
  data/processed/aact_trial_termination_candidate_2026-09-12_report.md
```