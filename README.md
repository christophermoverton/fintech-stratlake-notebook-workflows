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
- Walk-forward robustness and promotion review.

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

The notebooks will guide users through setup, Fintech extraction and backfill, session persistence, archive and restore flows, StratLake initialization, feature generation, validation, strategy smoke tests, backtest review, research comparison, and walk-forward robustness/promotion review.

Notebook imports should start with the [Notebook Import Staging Guide](docs/notebook_import_staging.md), then follow the [notebook cleanup workflow](docs/notebook_cleanup_workflow.md), [reusable notebook header template](docs/notebook_header_template.md), [secret-safe import checklist](docs/notebook_import_checklist.md), [notebook standards](docs/notebook_standards.md), and `.gitignore` guardrails before any notebook is committed. Imported and pending notebooks are tracked in the [notebook index](docs/notebook_index.md). Current imported notebooks are [Notebook 00 - setup and storage overview](notebooks/00_setup_and_storage_overview.ipynb), [Notebook 01 - Fintech daily bars extraction/backfill](notebooks/01_fintech_daily_bars_extraction_backfill.ipynb), [Notebook 02 - Fintech archive restore and session readiness](notebooks/02_fintech_session_persistence_save_restore.ipynb), [Notebook 03 - Fintech archive backup pack and restore](notebooks/03_fintech_archive_backup_pack_and_restore.ipynb), [Notebook 04 - StratLake feature-series index and dual-session setup](notebooks/04_stratlake_feature_series_index_setup.ipynb), [Notebook 05 - StratLake Q1 feature data generation with Fintech daily bars](notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb), [Notebook 06 - StratLake feature validation, archive, and handoff](notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb), [Notebook 07 - StratLake feature consumption, baseline research smoke test, and archive checkpoint](notebooks/07_stratlake_feature_consumption_baseline_research.ipynb), [Notebook 08 - StratLake strategy backtest artifact review](notebooks/08_stratlake_strategy_backtest_artifact_review.ipynb), [Notebook 09 - StratLake strategy comparison and research review](notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb), and [Notebook 10 - StratLake walk-forward robustness and promotion review](notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb), with review trails recorded in the [Notebook 00 import audit](docs/notebook_00_import_audit.md), [Notebook 01 import audit](docs/notebook_01_import_audit.md), [Notebook 02 import audit](docs/notebook_02_import_audit.md), [Notebook 03 import audit](docs/notebook_03_import_audit.md), [Notebook 04 import audit](docs/notebook_04_import_audit.md), [Notebook 05 import audit](docs/notebook_05_import_audit.md), [Notebook 06 import audit](docs/notebook_06_import_audit.md), [Notebook 07 import audit](docs/notebook_07_import_audit.md), [Notebook 08 import audit](docs/notebook_08_import_audit.md), [Notebook 09 import audit](docs/notebook_09_import_audit.md), and [Notebook 10 import audit](docs/notebook_10_import_audit.md). Notebook 08 imports cleaned source that reviews native StratLake strategy/backtest artifacts and can reattach to the Notebook 07 archive/session state when `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` is replaced by the user. Manual Colab smoke is recorded as `passed-with-notes`: restore and native `momentum_v1` execution were observed in an uploaded executed artifact, archive checkpoint refresh remained off, source remains clean/non-authoritative, and the executed artifact is not committed. Manual Colab smoke testing remains pending, failed-needs-rerun, passed-with-notes, passed, or not claimed unless explicitly recorded in the notebook index or audit trail.

Notebook 09 is imported at [notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb](notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb) as a source-safe StratLake strategy comparison and research review notebook, with audit coverage in [Notebook 09 import audit](docs/notebook_09_import_audit.md) and command-surface classification in [Notebook 09 command surface classification](docs/notebook_09_command_surface_classification.md). It remains output-free, metadata-clean, and guarded by `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`. Issue #99 records Colab smoke as `notebook_09_colab_smoke_passed_with_notes`: restore, native strategy comparison, plots, artifact discovery, research summary, checkpoint refresh, and final handoff ran in an executed artifact outside Git. The smoke observed 14 strategies attempted, 11 completed, and 3 strategy-level failures captured as review rows. The executed artifact is not committed and does not prove all-strategy correctness, authoritative performance, artifact completeness, checkpoint generality, or Notebook 10 behavior.

Notebook 10 is imported at [notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb](notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb) as a source-safe StratLake walk-forward robustness and promotion-review notebook, with audit coverage in [Notebook 10 import audit](docs/notebook_10_import_audit.md), [Notebook 10 staging classification](docs/notebook_10_staging_classification.md), and [Notebook 10 command surface classification](docs/notebook_10_command_surface_classification.md). It remains output-free, execution-count-null, metadata-clean, cell-ID-clean, and guarded by `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`, `RUN_STRATLAKE_ARCHIVE_RESTORE = False`, and `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False`. M13 records external Draft v4 smoke evidence separately from committed source validation: one smoke window ran, 14 strategies were preflighted, 11 were runnable, 3 were skipped as feature-contract findings, no strategies were promoted or watchlisted, and all evaluated strategies were `needs_review`. Smoke mode validates workflow wiring only; benchmark-avoidance outperformance from flat/inactive strategies is not alpha, and expanded-mode validation is required before any promotion-grade interpretation.

Local notebook development and execution-readiness checks are documented in the [Notebook Development Environment](docs/notebook_development_environment.md) guide. Final branch scope and merge readiness are summarized in the [Milestone 2 merge-readiness closeout](docs/milestone_2_merge_readiness.md), [Milestone 3 merge-readiness closeout](docs/milestone_3_merge_readiness.md), [Milestone 4 merge-readiness closeout](docs/milestone_4_merge_readiness.md), [Milestone 5 merge-readiness closeout](docs/milestone_5_merge_readiness.md), [Milestone 6 merge-readiness closeout](docs/milestone_6_merge_readiness.md), [Milestone 7 merge-readiness closeout](docs/milestone_7_merge_readiness.md), the [Milestone 8 merge-readiness closeout](docs/milestone_8_merge_readiness.md), the [Milestone 9 merge-readiness closeout](docs/milestone_9_merge_readiness.md), the [Milestone 10 merge-readiness closeout](docs/milestone_10_merge_readiness.md), the [Milestone 11 merge-readiness closeout](docs/milestone_11_merge_readiness.md), and the [Milestone 12 merge-readiness closeout](docs/milestone_12_merge_readiness.md).

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
python scripts/validate_notebook_execution_readiness.py notebooks/08_stratlake_strategy_backtest_artifact_review.ipynb
python scripts/validate_notebook_execution_readiness.py notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb
python scripts/validate_notebook_execution_readiness.py notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb
python -m pytest tests/test_notebook_08_static_cli_restore_artifact_review.py -q
python -m pytest tests/test_notebook_08_source_readiness.py -q
python -m pytest tests/test_notebook_09_static_cli_restore_strategy_comparison_coverage.py -q
python -m pytest tests/test_notebook_09_source_readiness.py -q
python -m pytest tests/test_notebook_10_static_source_contracts.py -q
python -m pytest tests/test_notebook_10_source_readiness.py -q
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
```

Validation layers are additive and should be run together:

- CLI contract validation checks broad command-surface examples and bounded safe `--help` contract behavior.
- CLI registry validation is argument-aware and checks known command/subcommand/flag/value syntax against the verified registry, including unsupported flags, boolean/value misuse, constrained `allowed_values`, `argparse_required`, `notebook_contract_required`, `required_when`, and excluded command candidates such as `fintech-restore-session`.
- Execution-readiness validation checks static JSON, output/count, path-fragment, classification, and safe Python syntax.

The Notebook 02, Notebook 03, Notebook 04, Notebook 05, and Notebook 06 targeted registry commands are optional focused confidence checks for restore, archive backup-pack, StratLake initialization, Q1 ingestion, feature-generation, dry-run export, and validation/handoff command surfaces where CLI assumption drift has highest risk. Notebook 08 focused tests inspect source-only restore, strategy, artifact-review, and sanitized readiness surfaces; they do not execute cells or require Colab, Drive, Alpaca credentials, archive packs, native strategy artifacts, or StratLake runtime outputs. Notebook 09 focused tests inspect source-only restore, native strategy comparison, parser/review-row, dataframe, plot, artifact-discovery, research-summary, checkpoint, handoff, and sanitized readiness surfaces; they do not execute cells or require Colab, Drive, Alpaca credentials, archive packs, native strategy artifacts, plots, generated reports, or Notebook 10 runtime behavior. Notebook 10 focused tests inspect source-only restore/archive guards, native command references, feature preflight, walk-forward robustness, promotion review, artifact references, warning taxonomy, benchmark-avoidance interpretation, and handoff fields; they do not execute cells or require Colab, Drive, Alpaca credentials, restored archives, native strategy artifacts, generated review outputs, plots, or promotion-grade evidence. All repository validation layers are non-executing for upstream workflows: they do not run live ingestion/restore/archive/export commands, mount Drive, prompt for credentials, install notebook packages, create backup packs, initialize Fintech or StratLake sessions, generate feature data, call Alpaca, run native strategy backtests, comparisons, or walk-forward execution, generate plots, write review artifacts, or mutate source notebooks. Missing local upstream Fintech and StratLake command warnings remain bounded to the existing CLI contract validator behavior.

For registry schema, policy, and maintenance details, see [CLI Command Registry Guide](docs/cli_command_registry.md).

## GitHub Issue Templates

This repository includes lightweight GitHub issue templates for notebook audits, milestone tasks, and upstream app triage. Use the upstream triage template when a notebook captures a failure that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, including Notebook 09-style cases where one strategy succeeds and other configured strategies fail.

## Planned Notebook Sequence

Notebook 00 through Notebook 10 are imported and tracked in the notebook index. Notebook 11 and later remain planned until they go through the same staged, cleaned, validated, and audited import workflow.

- Notebook 00 - setup and storage overview
- Notebook 01 - Fintech daily bars extraction/backfill
- Notebook 02 - Fintech archive restore and session readiness
- Notebook 03 - Fintech archive backup pack and restore
- Notebook 04 - StratLake feature-series index and dual-session setup (imported; bridge/setup notebook, not feature generation)
- Notebook 05 - StratLake Q1 feature data generation with Fintech daily bars (imported; manual Colab live ingestion and feature generation; source-only validated)
- Notebook 06 - StratLake feature validation, archive, and handoff (imported; validation/archive-preview/handoff checkpoint; source-only and sanitized validated; manual Colab smoke passed with notes)
- Notebook 07 - feature consumption and native strategy smoke test (imported; manual Colab smoke passed with notes)
- Notebook 08 - single-strategy backtest and artifact review (imported; source-only validated; manual Colab smoke passed with notes)
- Notebook 09 - multi-strategy comparison and research review (imported; source-only validated; manual Colab smoke passed with notes)
- Notebook 10 - walk-forward robustness and promotion review (imported; source-only validated; external v4 smoke interpreted with notes)

Current imported notebook chain:

- Notebook 00 establishes setup, session, and storage conventions.
- Notebook 01 runs the Fintech daily bars extraction/backfill workflow through native upstream commands.
- Notebook 02 restores or bootstraps a saved Fintech archive/session backup from Google Drive into `/content`, then validates restored workspace, session metadata, and curated/backfilled data readiness.
- Notebook 03 demonstrates the Fintech archive backup-pack workflow: `SESSION_ID`-derived Drive backup paths, pack dry-run, manual pack creation, backup-pack validation and inspection, local restore, and restored-file verification.
- Notebook 04 introduces the dual-session Fintech/StratLake setup flow: `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` are kept as separate identifiers for the upstream curated-data workspace and the downstream feature/research workspace. The key handoff is the explicit `--marketlake-root` argument that connects StratLake to the Fintech curated-data directory. Notebook 04 does not generate StratLake features; that belongs to Notebook 05.
- Notebook 05 continues the dual-session flow into Q1 daily-bars ingestion and Q1 StratLake feature generation. It keeps `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` distinct, uses `MARKETLAKE_ROOT` as the explicit curated-data handoff, runs active workspace paths under `/content`, and keeps Google Drive as persistence/archive/session storage only.
- Notebook 08 continues from the Notebook 07 archive/session checkpoint shape as a native StratLake strategy/backtest artifact review notebook. It reviews native strategy output, artifact inventory, plottable artifacts, benchmark rows, and handoff context without reimplementing strategy or backtest logic. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source, archive checkpoint refresh remains manual/off-by-default, and committed source does not claim authoritative restore, backtest, artifact-review, benchmark, plot, checkpoint, or handoff success. M11.6 records manual Colab smoke as passed with notes from an uploaded executed artifact that remains outside Git.
- Notebook 09 continues from Notebook 08 as a native StratLake strategy comparison and research review notebook. It preserves restore preview/manual gating, native strategy registry inspection, native multi-strategy comparison via `stratlake-run-strategy`, parsed stdout review rows, comparison dataframe/plot surfaces, artifact discovery by run id, research summary, optional archive checkpoint preview, and Notebook 10 handoff context. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source. Issue #99 records manual Colab smoke as passed with notes: restore, strategy comparison, plots, artifact discovery, research summary, archive checkpoint refresh, and final handoff rendered in an executed artifact outside Git; 14 strategies were attempted, 11 completed, and 3 strategy-level failures were captured as review rows. Committed source does not claim all-strategy correctness, authoritative performance results, benchmark alpha, plot correctness, artifact completeness, checkpoint generality, or Notebook 10 validation.
- Notebook 10 continues from Notebook 08/09 as a native StratLake walk-forward robustness and promotion-review notebook. It preserves restore preview/manual gating, feature-column discovery, native strategy preflight, walk-forward strategy execution via `stratlake-run-strategy`, robustness diagnostics, conservative promotion gates, warning taxonomy review, artifact inventory, optional archive checkpoint preview, and final handoff context. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source, restore/checkpoint refresh remain manual/off-by-default, and `NOTEBOOK10_MODE = "smoke"` is workflow-validation only. M13 records external Draft v4 smoke evidence: 14 candidate strategies, 11 runnable, 3 feature-contract skips, 11 walk-forward rows, 11 promotion-review rows, no promoted/watchlist strategies, and all evaluated strategies as `needs_review`. Committed source does not claim promotion-grade evidence, alpha, expanded-mode validation, artifact completeness, checkpoint success, or runtime correctness.

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
