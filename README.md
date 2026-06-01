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

Notebook imports should start with the [Notebook Import Staging Guide](docs/notebook_import_staging.md), then follow the [notebook cleanup workflow](docs/notebook_cleanup_workflow.md), [reusable notebook header template](docs/notebook_header_template.md), [secret-safe import checklist](docs/notebook_import_checklist.md), [notebook standards](docs/notebook_standards.md), and `.gitignore` guardrails before any notebook is committed. The first pilot import is [Notebook 00 - setup and storage overview](notebooks/00_setup_and_storage_overview.ipynb).

## Upstream App Repositories

This repository integrates with two upstream app repositories:

- `fintech-market-ingestion`
- `stratlake-trade-engine`

Those repositories remain the source of truth for their native application logic, command-line interfaces, data contracts, and artifacts.

## Colab + Google Drive Principles

- Active Colab work should stay under `/content`.
- Google Drive should be used only for persistence, archive packs, backups, and restore workflows.
- Secrets should be provided through safe runtime mechanisms and must not be committed.
- Local app workspaces, generated data, notebook outputs, archive packs, restore packs, and artifacts should remain outside version control.
- Imported notebooks should be reviewed for credentials, outputs, generated paths, and accidental data embeds before commit.
- Notebook filenames, headers, path variables, and commit readiness should follow the [notebook standards](docs/notebook_standards.md).

## Native Command First

Use native `fintech-market-ingestion` and `stratlake-trade-engine` CLI commands whenever available.

Notebook code should orchestrate, validate, parse, display, and review outputs. Notebook code should not reimplement native ingestion, archive/restore, feature generation, backtesting, strategy logic, or artifact generation.

## Generated Files Are Not Committed

Do not commit generated data, parquet files, archive packs, restore packs, artifacts, secrets, local app workspaces, notebook outputs, or Google Drive exports. Generated files should be reproducible from native commands or preserved outside Git through the documented persistence and archive workflows.

## GitHub Issue Templates

This repository includes lightweight GitHub issue templates for notebook audits, milestone tasks, and upstream app triage. Use the upstream triage template when a notebook captures a failure that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, including Notebook 09-style cases where one strategy succeeds and other configured strategies fail.

## Planned Notebook Sequence

- Notebook 00 - setup and storage overview
- Notebook 01 - Fintech daily bars extraction/backfill
- Notebook 02 - session save and restore
- Notebook 03 - archive backup pack and restore
- Notebook 04 - StratLake feature-series/index setup
- Notebook 05 - StratLake Q1 feature data generation with daily-bars ingestion
- Notebook 06 - StratLake feature validation, archive, and handoff
- Notebook 07 - feature consumption and native strategy smoke test
- Notebook 08 - single-strategy backtest and artifact review
- Notebook 09 - multi-strategy comparison and research review

## Repository Layout

```text
notebooks/
docs/
scripts/
examples/
.github/ISSUE_TEMPLATE/
```

- `notebooks/` contains reviewed, secret-safe Colab notebooks after the import checklist and ignore guardrails are ready.
- `docs/` contains supporting documentation, checklists, and workflow notes.
- `scripts/` contains small repository helper scripts for notebook workflow support. It should not duplicate native app logic.
- `examples/` contains lightweight examples that are safe to commit and do not include generated datasets, artifacts, archives, or secrets.
- `.github/ISSUE_TEMPLATE/` contains GitHub issue templates for milestone and workflow tracking.

## Development Milestones

- Milestone 1 - Repository Foundation and Secret-Safe Notebook Import.
- Later milestones will import reviewed notebooks, add validation helpers, document restore workflows, and expand native-command-first StratLake review workflows.
