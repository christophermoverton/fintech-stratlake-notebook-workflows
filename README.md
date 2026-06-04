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

Notebook imports should start with the [Notebook Import Staging Guide](docs/notebook_import_staging.md), then follow the [notebook cleanup workflow](docs/notebook_cleanup_workflow.md), [reusable notebook header template](docs/notebook_header_template.md), [secret-safe import checklist](docs/notebook_import_checklist.md), [notebook standards](docs/notebook_standards.md), and `.gitignore` guardrails before any notebook is committed. Imported and pending notebooks are tracked in the [notebook index](docs/notebook_index.md). Current imported notebooks are [Notebook 00 - setup and storage overview](notebooks/00_setup_and_storage_overview.ipynb), [Notebook 01 - Fintech daily bars extraction/backfill](notebooks/01_fintech_daily_bars_extraction_backfill.ipynb), [Notebook 02 - Fintech archive restore and session readiness](notebooks/02_fintech_session_persistence_save_restore.ipynb), [Notebook 03 - Fintech archive backup pack and restore](notebooks/03_fintech_archive_backup_pack_and_restore.ipynb), [Notebook 04 - StratLake feature-series index and dual-session setup](notebooks/04_stratlake_feature_series_index_setup.ipynb), [Notebook 05 - StratLake Q1 feature data generation with Fintech daily bars](notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb), and [Notebook 06 - StratLake feature validation, archive, and handoff](notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb), and [Notebook 07 - StratLake feature consumption, baseline research smoke test, and archive checkpoint](notebooks/07_stratlake_feature_consumption_baseline_research.ipynb), with review trails recorded in the [Notebook 00 import audit](docs/notebook_00_import_audit.md), [Notebook 01 import audit](docs/notebook_01_import_audit.md), [Notebook 02 import audit](docs/notebook_02_import_audit.md), [Notebook 03 import audit](docs/notebook_03_import_audit.md), [Notebook 04 import audit](docs/notebook_04_import_audit.md), [Notebook 05 import audit](docs/notebook_05_import_audit.md), [Notebook 06 import audit](docs/notebook_06_import_audit.md), and [Notebook 07 import audit](docs/notebook_07_import_audit.md). Notebook 07 consumes the Notebook 06 Fintech → StratLake Q1 feature handoff, discovers feature outputs, prefers native StratLake strategy smoke where available, preserves a fallback diagnostic as secondary/non-authoritative, previews archive checkpoint and restore surfaces, and prepares handoff to Notebook 08 for formal strategy/backtest artifacts. Notebook 07 is cleaned, output-free, and source-safe; manual Colab smoke is passed with notes (native strategy smoke return code 0, QA PASS, archive creation remained preview-only/off, executed artifact is not committed). Manual Colab smoke testing remains pending, failed-needs-rerun, passed-with-notes, passed, or not claimed unless explicitly recorded in the notebook index or audit trail.

Local notebook development and execution-readiness checks are documented in the [Notebook Development Environment](docs/notebook_development_environment.md) guide. Final branch scope and merge readiness are summarized in the [Milestone 2 merge-readiness closeout](docs/milestone_2_merge_readiness.md), [Milestone 3 merge-readiness closeout](docs/milestone_3_merge_readiness.md), [Milestone 4 merge-readiness closeout](docs/milestone_4_merge_readiness.md), [Milestone 5 merge-readiness closeout](docs/milestone_5_merge_readiness.md), [Milestone 6 merge-readiness closeout](docs/milestone_6_merge_readiness.md), [Milestone 7 merge-readiness closeout](docs/milestone_7_merge_readiness.md), and the [Milestone 8 merge-readiness closeout](docs/milestone_8_merge_readiness.md).

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
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/04_stratlake_feature_series_index_setup.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
```

Validation layers are additive and should be run together:

- CLI contract validation checks broad command-surface examples and bounded safe `--help` contract behavior.
- CLI registry validation is argument-aware and checks known command/subcommand/flag/value syntax against the verified registry, including unsupported flags, boolean/value misuse, constrained `allowed_values`, `argparse_required`, `notebook_contract_required`, `required_when`, and excluded command candidates such as `fintech-restore-session`.
- Execution-readiness validation checks static JSON, output/count, path-fragment, classification, and safe Python syntax.

The Notebook 02, Notebook 03, Notebook 04, Notebook 05, and Notebook 06 targeted registry commands are optional focused confidence checks for restore, archive backup-pack, StratLake initialization, Q1 ingestion, feature-generation, dry-run export, and validation/handoff command surfaces where CLI assumption drift has highest risk. All repository validation layers are non-executing for upstream workflows: they do not run live ingestion/restore/archive/export commands, mount Drive, prompt for credentials, install notebook packages, create backup packs, initialize Fintech or StratLake sessions, generate feature data, call Alpaca, or mutate source notebooks. Missing local upstream Fintech and StratLake command warnings remain bounded to the existing CLI contract validator behavior.

For registry schema, policy, and maintenance details, see [CLI Command Registry Guide](docs/cli_command_registry.md).

## GitHub Issue Templates

This repository includes lightweight GitHub issue templates for notebook audits, milestone tasks, and upstream app triage. Use the upstream triage template when a notebook captures a failure that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, including Notebook 09-style cases where one strategy succeeds and other configured strategies fail.

## Planned Notebook Sequence

Notebook 00, Notebook 01, Notebook 02, Notebook 03, Notebook 04, Notebook 05, and Notebook 06 are imported and tracked in the notebook index. Notebook 07 and later remain planned until they go through the same staged, cleaned, validated, and audited import workflow.

- Notebook 00 - setup and storage overview
- Notebook 01 - Fintech daily bars extraction/backfill
- Notebook 02 - Fintech archive restore and session readiness
- Notebook 03 - Fintech archive backup pack and restore
- Notebook 04 - StratLake feature-series index and dual-session setup (imported; bridge/setup notebook, not feature generation)
- Notebook 05 - StratLake Q1 feature data generation with Fintech daily bars (imported; manual Colab live ingestion and feature generation; source-only validated)
- Notebook 06 - StratLake feature validation, archive, and handoff (imported; validation/archive-preview/handoff checkpoint; source-only and sanitized validated; manual Colab smoke passed with notes)
- Notebook 07 - feature consumption and native strategy smoke test
- Notebook 08 - single-strategy backtest and artifact review
- Notebook 09 - multi-strategy comparison and research review

Current imported notebook chain:

- Notebook 00 establishes setup, session, and storage conventions.
- Notebook 01 runs the Fintech daily bars extraction/backfill workflow through native upstream commands.
- Notebook 02 restores or bootstraps a saved Fintech archive/session backup from Google Drive into `/content`, then validates restored workspace, session metadata, and curated/backfilled data readiness.
- Notebook 03 demonstrates the Fintech archive backup-pack workflow: `SESSION_ID`-derived Drive backup paths, pack dry-run, manual pack creation, backup-pack validation and inspection, local restore, and restored-file verification.
- Notebook 04 introduces the dual-session Fintech/StratLake setup flow: `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` are kept as separate identifiers for the upstream curated-data workspace and the downstream feature/research workspace. The key handoff is the explicit `--marketlake-root` argument that connects StratLake to the Fintech curated-data directory. Notebook 04 does not generate StratLake features; that belongs to Notebook 05.
- Notebook 05 continues the dual-session flow into Q1 daily-bars ingestion and Q1 StratLake feature generation. It keeps `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` distinct, uses `MARKETLAKE_ROOT` as the explicit curated-data handoff, runs active workspace paths under `/content`, and keeps Google Drive as persistence/archive/session storage only.

Notebook 02 keeps live initialization, restore, Drive mount, credential setup, and restored workspace handling manual Colab-only. The Issue #37 uploaded smoke attempt exposed that separate Colab runtimes cannot rely on prior `/content` state, so Notebook 02 now starts from a Drive session backup-pack source (`fintech-market-ingestion/sessions/<SESSION_ID>/backups/<BACKUP_ID>`) and initializes the local `/content` restore workspace before restore instead of assuming Notebook 00/01 local state still exists. Manual Colab smoke is recorded as `passed-with-notes`: live Colab testing confirmed `fintech-init-project --notebooks` uses `--notebooks` as a standalone flag, `fintech-backup-data restore` is the archive/backfilled data restore command, and the safe valid default overwrite policy is `fail`. Notebook 03 repository validation remains source-only and sanitized, while Issue #51 records manual Colab smoke as `colab_smoke_passed_with_notes`; its package install, Drive mount, live archive pack, validation, inspection, restore, and generated demo-file cells remain manual Colab/runtime-only and generated smoke artifacts must stay out of Git. Notebook 04 repository validation is source-only and sanitized (Issues #53-#56): it does not run package install, Drive mount, `fintech-init-project`, `stratlake-init-session`, Drive folder creation, archive/restore, or StratLake feature generation; those remain manual Colab/runtime-only. Issue #59 records manual Colab smoke as `colab_smoke_passed_with_notes`: package install, CLI availability, Drive mount, Fintech/StratLake session initialization, session ID extraction, Drive path creation, and readiness check were confirmed; notes include non-linear cell execution and an empty `MARKETLAKE_ROOT` (acceptable for setup-only scope). Notebook 04 does not automatically target prior user-selected Drive archive folders; freshly instanced session IDs derive new Drive paths.

Notebook 05 repository validation is source-only and sanitized (Issues #61-#65): it confirms the Q1 date window, live command shapes, CLI registry/contract coverage, and sanitized skip boundaries, but it does not install packages, mount Drive, read Alpaca credentials, call Alpaca, run `fintech-backfill-daily`, run `stratlake-build-features`, run `stratlake-session-export`, create archives, restore archives, generate daily bars, or generate features. Issue #66 records Notebook 05 manual Colab smoke as `colab_smoke_passed_with_notes`: an uploaded executed Colab artifact confirmed the core live Q1 ingestion and feature-generation flow, but optional archive/bootstrap preview cells were not executed, StratLake archive/bootstrap previews remain manual guidance, and the executed artifact must not be committed. Advanced feature validation, strategy smoke tests, and backtest review remain deferred to Notebook 06+.

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
