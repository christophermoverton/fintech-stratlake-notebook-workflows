# Fintech + StratLake Notebook Workflows

## Purpose

This repository provides a notebook-first Colab workflow layer for integrating `fintech-market-ingestion` and `stratlake-trade-engine`. It is intended for development, tutorials, reviewable integration workflows, and repeatable handoffs between market-data ingestion and StratLake research.

The core principle is that notebook workflows should be easy to import, run, and review without exposing credentials, committing generated data, or reimplementing native app logic.

## Repository Scope

This repository supports notebook-first workflows for:

- Fintech market data ingestion.
- Google Drive session persistence.
- Archive pack creation and restore.
- StratLake notebook session initialization.
- Feature generation from Fintech curated data.
- Native StratLake strategy smoke tests.
- Backtest artifact review.
- Strategy comparison and research review.

Notebook code in this repository should orchestrate commands, validate expected inputs and outputs, parse results, display summaries, and support human review. Native app behavior should remain in the upstream application repositories.

## What This Repository Is Not

This repository is intentionally narrow in scope:

- This repo does not replace `fintech-market-ingestion`.
- This repo does not replace `stratlake-trade-engine`.
- This repo does not own native ingestion logic.
- This repo does not own native feature normalization logic.
- This repo does not own native strategy/backtest logic.
- This repo does not commit generated datasets, artifacts, archives, or secrets.

## Workflow Overview

The workflows are designed for Colab sessions where active work happens under `/content`. Google Drive may be mounted for persistence, archive packs, backups, and restore workflows, but Drive should not become the active application workspace.

The notebooks will guide users through setup, Fintech extraction and backfill, session persistence, archive and restore flows, StratLake initialization, feature generation, validation, strategy smoke tests, backtest review, and research comparison.

Notebook imports should start with the [Notebook Import Staging Guide](docs/notebook_import_staging.md), then follow the [notebook cleanup workflow](docs/notebook_cleanup_workflow.md), [reusable notebook header template](docs/notebook_header_template.md), [secret-safe import checklist](docs/notebook_import_checklist.md), [notebook standards](docs/notebook_standards.md), and `.gitignore` guardrails before any notebook is committed. Imported and pending notebooks are tracked in the [notebook index](docs/notebook_index.md). Current imported notebooks are [Notebook 00 - setup and storage overview](notebooks/00_setup_and_storage_overview.ipynb), [Notebook 01 - Fintech daily bars extraction/backfill](notebooks/01_fintech_daily_bars_extraction_backfill.ipynb), and [Notebook 02 - Fintech archive restore and session readiness](notebooks/02_fintech_session_persistence_save_restore.ipynb), with review trails recorded in the [Notebook 00 import audit](docs/notebook_00_import_audit.md), [Notebook 01 import audit](docs/notebook_01_import_audit.md), and [Notebook 02 import audit](docs/notebook_02_import_audit.md). Manual Colab smoke testing remains pending, failed-needs-rerun, refactored-needs-rerun, or not claimed unless explicitly recorded in the notebook index or audit trail.

Local notebook development and execution-readiness checks are documented in the [Notebook Development Environment](docs/notebook_development_environment.md) guide. Final branch scope and merge readiness are summarized in the [Milestone 2 merge-readiness closeout](docs/milestone_2_merge_readiness.md) and [Milestone 3 merge-readiness closeout](docs/milestone_3_merge_readiness.md).

## Upstream App Repositories

This repository integrates with two upstream app repositories:

- `fintech-market-ingestion`
- `stratlake-trade-engine`

Those repositories remain the source of truth for their native application logic, command-line interfaces, data contracts, and artifacts.

## Colab + Google Drive Principles

- Active Colab work should stay under `/content`.
- Google Drive should be used only for persistence, archive packs, backups, and restore workflows.
- Drive mount and live persistence or restore actions are manual Colab-only.
- Secrets should be provided through safe runtime mechanisms and must not be committed.
- Local app workspaces, generated data, session payloads, notebook outputs, archive packs, restore packs, restore outputs, runtime folders, and artifacts should remain outside version control.
- Imported notebooks should be reviewed for credentials, outputs, generated paths, and accidental data embeds before commit.
- Notebook filenames, headers, path variables, and commit readiness should follow the [notebook standards](docs/notebook_standards.md).

## Native Command First

Use native `fintech-market-ingestion` and `stratlake-trade-engine` CLI commands whenever available.

Notebook code should orchestrate, validate, parse, display, and review outputs. Notebook code should not reimplement native ingestion, archive/restore, feature generation, backtesting, strategy logic, or artifact generation.

## Generated Files Are Not Committed

Do not commit generated data, parquet files, session payloads, archive packs, restore packs, restore outputs, artifacts, secrets, tokens, `.env` values, private paths, personal Drive folder names, local app workspaces, runtime folders, notebook outputs, execution counts, or Google Drive exports. Generated files should be reproducible from native commands or preserved outside Git through the documented persistence and archive workflows.

## Validation Commands

Run the repository guardrails before committing notebook changes:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
pytest
```

The notebook execution-readiness command performs static JSON, output/count, path-fragment, classification, and safe Python syntax checks. The CLI contract validator checks notebook command examples against configured safe `--help` contracts. The pytest harness executes only sanitized temporary notebook copies. These layers do not mutate source notebooks, mount Drive, prompt for credentials, install packages, run ingestion, run archive/restore commands, or save outputs to committed notebooks.

## GitHub Issue Templates

This repository includes lightweight GitHub issue templates for notebook audits, milestone tasks, and upstream app triage. Use the upstream triage template when a notebook captures a failure that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, including Notebook 09-style cases where one strategy succeeds and other configured strategies fail.

## Planned Notebook Sequence

Notebook 00, Notebook 01, and Notebook 02 are imported and tracked in the notebook index. Notebook 03 and later remain planned until they go through the same staged, cleaned, validated, and audited import workflow.

- Notebook 00 - setup and storage overview
- Notebook 01 - Fintech daily bars extraction/backfill
- Notebook 02 - Fintech archive restore and session readiness
- Notebook 03 - archive backup pack and restore
- Notebook 04 - StratLake feature-series/index setup
- Notebook 05 - StratLake Q1 feature data generation with daily-bars ingestion
- Notebook 06 - StratLake feature validation, archive, and handoff
- Notebook 07 - feature consumption and native strategy smoke test
- Notebook 08 - single-strategy backtest and artifact review
- Notebook 09 - multi-strategy comparison and research review

Current imported notebook chain:

- Notebook 00 establishes setup, session, and storage conventions.
- Notebook 01 runs the Fintech daily bars extraction/backfill workflow through native upstream commands.
- Notebook 02 restores or bootstraps a saved Fintech archive/session backup from Google Drive into `/content`, then validates restored workspace, session metadata, and curated/backfilled data readiness.

Notebook 02 keeps live restore, Drive mount, credential setup, and restored workspace handling manual Colab-only. The Issue #37 uploaded smoke attempt exposed that separate Colab runtimes cannot rely on prior `/content` state, so Notebook 02 now starts from a Drive archive/session source instead of assuming Notebook 00/01 local state still exists. Dedicated restore command behavior remains candidate/upstream-confirmation-dependent where applicable. Archive creation, advanced archive inspection/transfer, StratLake initialization, feature generation, strategy smoke tests, and backtest review remain deferred to Notebook 03+.

## Repository Layout

```text
config/
notebooks/
docs/
scripts/
examples/
.github/ISSUE_TEMPLATE/
```

- `config/` contains notebook development and validation configuration.
- `notebooks/` contains reviewed, secret-safe Colab notebooks after the import checklist and ignore guardrails are ready.
- `docs/` contains supporting documentation, checklists, and workflow notes.
- `scripts/` contains small repository helper scripts for notebook workflow support. It should not duplicate native app logic.
- `examples/` contains lightweight examples that are safe to commit and do not include generated datasets, artifacts, archives, or secrets.
- `.github/ISSUE_TEMPLATE/` contains GitHub issue templates for milestone and workflow tracking.

## Development Milestones

- Milestone 1 - Repository Foundation and Secret-Safe Notebook Import.
- Milestone 2 - Notebook Workflow Scaffolding and First Import Pilot.
- Later milestones will import additional reviewed notebooks, expand native-command-first StratLake review workflows, and continue controlled Colab smoke validation.
