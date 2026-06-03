# Notebook Index and Import Status Tracker

## Purpose

This tracker records which notebooks are imported, which notebooks are pending import, what each notebook's workflow role is, and what validation or audit status is known.

The tracker is a review surface, not an automated source of generated truth. It should help future notebook imports remain controlled, staged, cleaned, validated, audited, and artifact-free.

## Relationship to Controlled Import

Notebook imports should move through staging, cleanup, validation, audit, and review before entering `notebooks/`.

Use this tracker with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Notebook Cleanup Workflow](notebook_cleanup_workflow.md)
- [Reusable Notebook Header Template](notebook_header_template.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)
- [Notebook Development Environment](notebook_development_environment.md)
- [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md)
- [Notebook 00 Import Audit](notebook_00_import_audit.md)
- [Notebook 01 Import Audit](notebook_01_import_audit.md)
- [Notebook 02 Import Audit](notebook_02_import_audit.md)
- [Notebook 03 Import Audit](notebook_03_import_audit.md)

Do not use this tracker to justify direct imports from Google Drive. Future notebooks should remain outside the repository until they are staged, cleaned, validated, reviewed, and explicitly moved into `notebooks/`.

## Current Imported Notebooks

| Number | Title | Repository path | Workflow role | Upstream app coverage | Import status | Validation status | Audit record | Manual Colab smoke | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 00 | Setup and Storage Overview | [notebooks/00_setup_and_storage_overview.ipynb](../notebooks/00_setup_and_storage_overview.ipynb) | setup/storage/session/persistence overview | `fintech-market-ingestion`; references StratLake boundaries where relevant | `imported` | `cleaned`, `static_validated`, `readiness_validated`, `pytest_validated`, `cli_contract_validated`, `cli_registry_validated`, `audit_recorded` | [Notebook 00 import audit](notebook_00_import_audit.md) | `pending` | First pilot import; final Colab runtime confirmation remains pending. |
| 01 | Fintech Daily Bars Extraction/Backfill | [notebooks/01_fintech_daily_bars_extraction_backfill.ipynb](../notebooks/01_fintech_daily_bars_extraction_backfill.ipynb) | extraction/backfill | `fintech-market-ingestion` | `pilot_imported`, `imported` | `cleaned`, `static_validated`, `readiness_validated`, `pytest_validated`, `cli_contract_validated`, `cli_registry_validated`, `audit_recorded` | [Notebook 01 import audit](notebook_01_import_audit.md) | `passed-with-notes` | Core Colab smoke passed; Issue #27 fixes Drive placeholder syntax before dry-run preview cells are rerun for full pass. |
| 02 | Fintech Archive Restore and Session Readiness | [notebooks/02_fintech_session_persistence_save_restore.ipynb](../notebooks/02_fintech_session_persistence_save_restore.ipynb) | archive/session restore and readiness | `fintech-market-ingestion`; secondary upstream app none expected | `pilot_imported`, `imported` | `cleaned`, `static_validated`, `readiness_validated`, `pytest_validated`, `cli_contract_validated`, `cli_registry_validated`, `audit_recorded`, `colab_smoke_passed_with_notes` | [Notebook 02 import audit](notebook_02_import_audit.md); [staging/classification](notebook_02_staging_classification.md) | `passed-with-notes` | Issue #37 exposed the runtime-isolation problem: Notebook 02 cannot assume Notebook 00/01 `/content` state still exists. It now initializes the local `/content` Fintech project/session workspace with `fintech-init-project --notebooks --with-session`, then restores archived/backfilled curated data from an intentional Drive session backup-pack source (`sessions/<SESSION_ID>/backups/<BACKUP_ID>`) using `fintech-backup-data restore --backup-pack-dir --restore-root --overwrite-policy fail`. Manual Colab smoke passed with notes; live restore, Drive mount, credential setup, and restored workspace material remain manual Colab-only and must stay out of Git. Notebook 03 now covers archive backup-pack source examples; advanced archive transfer and downstream StratLake workflows remain deferred. |
| 03 | Fintech Archive Backup Pack and Restore | [notebooks/03_fintech_archive_backup_pack_and_restore.ipynb](../notebooks/03_fintech_archive_backup_pack_and_restore.ipynb) | archive backup-pack creation, validation, inspection, and restore tutorial | `fintech-market-ingestion`; secondary upstream app none expected | `imported` | `cleaned`, `static_validated`, `readiness_validated`, `sanitized_execution_validated`, `cli_contract_validated`, `cli_registry_validated`, `audit_recorded` | [Notebook 03 import audit](notebook_03_import_audit.md); [staging/classification](notebook_03_staging_classification.md) | `not_claimed` | Issue #46 imported and cleaned Notebook 03, including output/count removal, Colab runtime metadata stripping, private/user metadata removal, Drive-folder placeholder normalization, and removal of stale session restore/save availability checks. Issues #47 and #48 added CLI contract, argument-aware registry, readiness, and sanitized execution coverage. Repository validation is source-only and sanitized: it does not run package install, Drive mount, live `fintech-init-project`, backup pack creation, backup-pack validation/inspection, restore, demo `.parquet` creation, or restored-file verification. |

Notebook 00, Notebook 01, Notebook 02, and Notebook 03 are the imported notebooks currently tracked by this repository. Notebook 02 is repository-validated and audited, with Issue #37 manual Colab smoke recorded as `passed-with-notes`. Notebook 03 is repository-validated and audited as cleaned source with sanitized execution coverage; no live Notebook 03 Colab smoke status is claimed.

Notebook 02 and Notebook 03 preserve the restore/archive boundary: active Colab app work remains under `/content`; Google Drive is archive/session storage only; Drive should not become the active app workspace; generated archive/session payloads, restored workspace files, restore outputs, archive packs, generated data, notebook outputs, execution counts, credentials, private paths, and runtime folders stay out of Git.

## Import Status Table

| Status | Meaning |
|---|---|
| `imported` | Notebook exists under `notebooks/`, is cleaned, output-free, tracked, and has passed repository validation. |
| `pilot_imported` | Notebook exists under `notebooks/` as a controlled pilot import and has passed the repository-side checks recorded for its milestone issue. |
| `imported_pending_audit` | Notebook exists under `notebooks/` and has passed repository-side validation, but its import audit record is not complete yet. |
| `pending_staging` | Candidate notebook exists outside the repo or is planned, but has not yet gone through staging and cleanup. |
| `needs_cleanup` | Candidate notebook has useful content but contains outputs, runtime state, paths, logs, blobs, or other cleanup needs. |
| `needs_rewrite` | Candidate notebook contains useful workflow intent but should be rewritten before import. |
| `upstream_triage_needed` | Notebook exposes behavior likely requiring changes or investigation in `fintech-market-ingestion` or `stratlake-trade-engine`. |
| `blocked` | Import is waiting on another issue, upstream command, validation workflow, or design decision. |
| `do_not_import` | Notebook or content should not be imported into this repo. |

## Validation Stage Table

| Stage | Meaning |
|---|---|
| `not_started` | No staging, cleanup, or validation has been recorded. |
| `staged` | Notebook has been copied to a staging location outside the repository. |
| `cleaned` | Outputs, execution counts, runtime metadata, private paths, and unsafe captured state have been reviewed and removed where needed. |
| `static_validated` | Repository static checks passed, including secret scan, notebook output check, and repository cleanliness validation. |
| `readiness_validated` | TOML-backed notebook execution-readiness validation passed. |
| `pytest_validated` | Sanitized pytest notebook execution passed without mutating source notebooks. |
| `sanitized_execution_validated` | Sanitized pytest notebook execution passed without executing live runtime-only workflow cells or mutating source notebooks. |
| `cli_contract_validated` | Notebook CLI examples passed CLI contract validation. Missing local upstream commands may be warnings when configured. |
| `cli_registry_validated` | Notebook CLI examples passed argument-aware CLI registry validation, including command/subcommand/flag/value constraints and excluded-command checks. |
| `audit_recorded` | A notebook import audit record exists. |
| `colab_smoke_pending` | Manual Colab runtime smoke validation remains pending. |
| `colab_smoke_failed_needs_rerun` | A manual Colab smoke attempt was reviewed and failed or was invalid; rerun is required before pass can be claimed. |
| `colab_smoke_refactored_needs_rerun` | A failed smoke attempt caused a notebook workflow refactor; rerun the revised notebook before pass can be claimed. |
| `colab_smoke_passed_with_notes` | Manual Colab runtime smoke validation found the core workflow working but recorded follow-up notes before full pass. |
| `colab_smoke_passed` | Manual Colab runtime smoke validation has been completed and recorded. |

Validation status may include multiple markers for the same notebook. Do not claim `colab_smoke_passed` unless a fresh Colab smoke test was actually completed.

## Pending Notebook Candidates

These are planned workflow categories only. They are not imported, cleaned, validated, audited, or confirmed runnable.

| Candidate | Workflow role | Expected upstream coverage | Import status | Validation status | Notes |
|---|---|---|---|---|---|
| Advanced archive shard/package inspection and transfer workflow | archive inspection/transfer | `fintech-market-ingestion` | `pending_staging` | `not_started` | Notebook 03 covers backup-pack validate/inspect source examples; advanced archive transfer workflows remain future work and must not commit generated packages or listings. |
| StratLake initialization workflow | StratLake initialization | `stratlake-trade-engine` | `pending_staging` | `not_started` | Should use native StratLake setup commands where available. |
| Feature generation workflow | feature generation | `stratlake-trade-engine`; Fintech curated data inputs | `pending_staging` | `not_started` | Must not reimplement feature generation logic. |
| Validation / QA workflow | validation | both upstream apps as needed | `pending_staging` | `not_started` | Should validate and review runtime outputs without committing them. |
| Strategy smoke-test workflow | strategy smoke test | `stratlake-trade-engine` | `pending_staging` | `not_started` | Must use native strategy/CLI behavior where available. |
| Backtest review workflow | backtest review | `stratlake-trade-engine` | `pending_staging` | `not_started` | Must not reimplement backtesting or artifact generation. |
| Research comparison workflow | research comparison | `stratlake-trade-engine` | `pending_staging` | `not_started` | Should review native comparison outputs only. |
| Audit/review workflow | audit/review | repository workflow layer | `pending_staging` | `not_started` | Future audits should follow the Notebook 00 audit pattern. |

## Non-Importable and Do-Not-Import Categories

Do not import notebooks or content that:

- Contains real secrets, tokens, `.env` values, credential JSON, or private keys.
- Contains notebook outputs, execution state, tracebacks, logs, screenshots, or embedded output blobs that cannot be safely cleaned.
- Contains generated data, archive packs, restore packs, local app workspaces, runtime folders, or copied Google Drive exports.
- Depends on private local files, private Drive paths, usernames, or account-specific details.
- Reimplements native Fintech ingestion, StratLake feature generation, archive/restore, strategy, backtest, or artifact logic.
- Is obsolete, redundant, scratch-only, unsafe, or too stale to preserve.

Use `do_not_import`, `needs_rewrite`, or `upstream_triage_needed` instead of forcing unsafe content into `notebooks/`.

## Future Update Rules

Update this tracker when:

- A notebook is staged for review.
- A notebook moves between readiness categories.
- A notebook is imported into `notebooks/`.
- A notebook passes static validation, readiness validation, pytest validation, CLI contract validation, audit recording, or manual Colab smoke testing.
- A notebook is blocked, rejected, or moved to `do_not_import`.

Before marking a notebook `imported`, confirm:

- It exists under `notebooks/`.
- Outputs are cleared.
- Execution counts are `null`.
- Raw `.ipynb` JSON has been reviewed.
- Secrets and private paths are absent.
- Generated data and runtime artifacts are absent.
- Native-command-first boundaries are respected.
- Validation commands pass.
- An audit record exists or is planned in the same import sequence.

## Validation Commands Before Status Changes

Run these commands before marking a notebook as imported or advancing validation status:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
```

Validation layers remain additive:

- CLI contract validation covers broad command-surface and bounded safe `--help` checks; expected missing-local-upstream warnings remain in this layer.
- CLI registry validation adds argument-aware checks for command/subcommand/flag/value correctness and excluded command candidates.
- Execution-readiness validation remains the final static notebook-readiness check.

For registry schema and maintenance policy details, see [CLI Command Registry Guide](cli_command_registry.md).

Use explicit notebook target forms when reviewing a specific notebook:

```bash
python scripts/validate_notebook_execution_readiness.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_test.toml
python scripts/validate_notebook_cli_contracts.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_cli_contracts.toml
python scripts/validate_notebook_cli_registry.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_execution_readiness.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_test.toml
python scripts/validate_notebook_cli_registry.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_cli_registry.toml
```

Manual Colab smoke validation should follow [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md). Keep Colab outputs, logs, screenshots, tracebacks, and generated artifacts out of Git.
