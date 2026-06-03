# Notebook 03 Staging and Classification

## Summary

This document records the Milestone 6 staging and classification decision for Notebook 03 before and during cleanup, validation, and audit work.

Notebook 03 is the Fintech archive backup-pack and restore tutorial. It is useful and source-aligned after cleanup, but its live workflow depends on a Colab runtime, mounted Google Drive, generated session metadata, local curated data, backup-pack material, and restore output paths. Repository validation must therefore remain source-only and sanitized.

## Candidate Notebook Identity

| Field | Decision |
|---|---|
| Source notebook | `Notebook_03_Archive_` + `backup_pack_and_restore_` + `STANDALONE_latest_` + `fintech_milestone (1).ipynb` |
| Repository path | `notebooks/03_fintech_archive_backup_pack_and_restore.ipynb` |
| Workflow classification | Fintech archive backup-pack creation, validation, inspection, and restore tutorial |
| Primary upstream app | `fintech-market-ingestion` |
| Secondary upstream app | None expected |
| Relationship to Notebook 00 | Preserves `/content` workspace and storage conventions |
| Relationship to Notebook 01 | Uses curated-data paths that may be populated by extraction/backfill workflows |
| Relationship to Notebook 02 | Continues the archive/session restore boundary using current backup-pack command shapes |
| Staging category | `needs_cleanup` before import; `source_safe_after_cleanup` after Issue #46 |
| Import status | `imported` after Issue #46 |
| Manual Colab smoke status | `not_claimed` |

## Source Review Facts

Initial review of the uploaded notebook found:

- 41 total cells.
- 19 code cells.
- 22 markdown cells.
- 16 code cells with outputs.
- 16 code cells with non-null execution counts.
- Colab/runtime metadata including execution information, output ids, base URIs, timestamps, elapsed values, and user-identifying metadata.

Those runtime characteristics made the original notebook unsuitable for direct commit. Issue #46 imported a cleaned repository copy only.

## Expected Notebook Role

Notebook 03 should guide a Colab user through:

- Installing runtime dependencies manually in Colab.
- Mounting Google Drive manually in Colab.
- Initializing a local Fintech project/session under `/content`.
- Extracting `SESSION_ID` from the generated session manifest.
- Building Drive archive roots under `sessions/{SESSION_ID}/backups/{ARCHIVE_ID}`.
- Dry-running archive backup-pack creation.
- Creating a backup pack manually in runtime.
- Validating a runtime backup pack.
- Inspecting a runtime backup pack.
- Restoring a backup pack to local `/content` runtime storage.
- Verifying restored files after runtime restore.
- Keeping previous-session restore examples commented and manual.

Notebook 03 should remain a tutorial and orchestration layer. It must not reimplement native Fintech archive, restore, ingestion, generated artifact writing, or StratLake behavior.

## Runtime-Only Cell Classification

These Notebook 03 cells and command families are manual Colab/runtime-only:

- `!python -m pip install ...`.
- `from google.colab import drive`.
- `drive.mount("/content/drive")`.
- `fintech-init-project`.
- Reading generated `session_manifest.json` files.
- Creating Drive session and backup directories.
- Creating demo `.parquet` placeholder files.
- `fintech-backup-data pack --dry-run`.
- Live `fintech-backup-data pack`.
- `fintech-backup-data validate`.
- `fintech-backup-data inspect`.
- `fintech-backup-data restore`.
- Restored-file verification.
- Previous-session backup-pack validation, inspection, and restore examples.

Repository validation may parse and classify those cells, but must not execute them.

## Sanitized Validation Behavior

Issue #48 added Notebook 03 to the execution-readiness and sanitized pytest harnesses.

The readiness validator:

- Loads Notebook 03 as JSON.
- Checks outputs and execution counts.
- Checks forbidden committed path fragments.
- Classifies shell, Colab, Drive mount, package install, upstream CLI, archive, and restore cells as skipped.
- Compiles only safe Python cells that are not classified as runtime-only.

The sanitized pytest harness:

- Builds a temporary copy.
- Replaces runtime-only cells with no-op cells or harmless setup fragments.
- Executes only the sanitized temporary copy.
- Confirms the source notebook hash is unchanged.

Notebook 03-specific skip/no-op coverage includes backup-pack path variables, previous-session backup-pack variables, demo-file creation, restore-root setup, backup-pack restore, and restored-file inspection.

## Command Surface Classification

Notebook 03 uses only these upstream command families:

- `fintech-init-project`.
- `fintech-backup-data`.

Notebook 03 backup-pack command shapes:

- `fintech-backup-data pack --workspace-root --source-dataset-root --backup-root --backup-id --shard-size-mb --dry-run`.
- `fintech-backup-data pack --workspace-root --source-dataset-root --backup-root --backup-id --shard-size-mb`.
- `fintech-backup-data validate --backup-pack-dir`.
- `fintech-backup-data inspect --backup-pack-dir`.
- `fintech-backup-data restore --backup-pack-dir --restore-root --overwrite-policy fail`.

Classification decisions:

- Pack dry-run is source-validated and classified as dry-run, but not executed locally.
- Live pack is source-validated and classified as manual-only live.
- Validate, inspect, and restore are source-validated and classified as manual-only live.
- `--dry-run` is optional for pack because Notebook 03 includes both dry-run and manual live examples.
- `fintech-save-session` is not required by Notebook 03.
- `fintech-restore-session` is not used as a backup-pack restore path.
- No StratLake commands are introduced by Notebook 03.

## Cleanup Risk Inventory

| Risk | Notebook 03 relevance | Cleanup or validation action |
|---|---|---|
| Notebook outputs | Original source had outputs. | Cleared before import. |
| Execution counts | Original source had non-null counts. | Reset to `null`. |
| Colab runtime metadata | Original source had execution metadata. | Stripped before audit. |
| User-identifying metadata | Original source had display/user id metadata. | Removed before audit. |
| Drive folder names | Source path could expose exact Drive project folder. | Replaced with `REPLACE_WITH_DRIVE_FOLDER_NAME`. |
| Generated demo files | Notebook can create placeholder `.parquet` files. | Manual runtime-only; sanitizer no-ops. |
| Backup packs | Notebook can create archive backup packs. | Manual runtime-only; never committed. |
| Backup-pack manifests | Runtime pack output can create manifests. | Manual runtime-only; never committed. |
| Restore outputs | Notebook can restore files under `/content`. | Manual runtime-only; never committed. |
| Previous-session restore examples | Useful but risky if treated as live defaults. | Kept commented and manual-only. |
| Unsupported restore command assumptions | `fintech-restore-session` is not the backup-pack restore path. | Removed from Notebook 03 and preserved as an excluded registry candidate. |

## Repository Boundary Rules

Notebook 03 import and validation must not:

- Execute the notebook end to end.
- Install packages.
- Mount Google Drive.
- Run live upstream Fintech or StratLake commands.
- Initialize runtime workspaces.
- Create demo `.parquet` files.
- Create backup packs.
- Validate or inspect real backup packs.
- Restore data.
- Commit generated data, backup packs, manifests, restored files, Drive artifacts, credentials, outputs, execution counts, or runtime state.
- Add Notebook 04 or later work.

## Go/No-Go Checklist

| Gate | Status |
|---|---|
| Candidate Notebook 03 source located outside committed repo. | Go |
| Workflow role confirmed as archive backup-pack and restore tutorial. | Go |
| Target repository path identified. | Go |
| Outputs cleared. | Go |
| Execution counts reset to `null`. | Go |
| Colab/runtime metadata stripped. | Go |
| Private/user metadata removed. | Go |
| Drive folder placeholder normalized. | Go |
| `SESSION_ID`-derived backup paths preserved. | Go |
| Native command-first workflow preserved. | Go |
| CLI contract validation configured. | Go |
| CLI registry validation configured. | Go |
| Execution-readiness validation configured. | Go |
| Sanitized pytest execution configured. | Go |
| Live Colab smoke not claimed. | Go |
| No generated artifacts committed. | Go |

Go result: Notebook 03 is suitable as a cleaned, source-safe repository notebook with runtime-only archive and restore cells protected by source-only and sanitized validation.
