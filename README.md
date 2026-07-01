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

Notebook imports should start with the [Notebook Import Staging Guide](docs/notebook_import_staging.md), then follow the [notebook cleanup workflow](docs/notebook_cleanup_workflow.md), [reusable notebook header template](docs/notebook_header_template.md), [secret-safe import checklist](docs/notebook_import_checklist.md), [notebook standards](docs/notebook_standards.md), and `.gitignore` guardrails before any notebook is committed. Imported and pending notebooks are tracked in the [notebook index](docs/notebook_index.md). Current imported notebooks are Notebook 00 through Notebook 14, with review trails recorded in the corresponding import audit docs, including [Notebook 11 import audit](docs/notebook_11_import_audit.md), [Notebook 12 import audit](docs/notebook_12_import_audit.md), [Notebook 13 import audit](docs/notebook_13_import_audit.md), and [Notebook 14 importation guide](docs/notebook_14_importation_guide.md). Manual Colab smoke testing remains pending, failed-needs-rerun, passed-with-notes, passed, source-only/not-runtime-claimed, or not claimed unless explicitly recorded in the notebook index or audit trail.

Notebook 09 is imported at [notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb](notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb) as a source-safe StratLake strategy comparison and research review notebook, with audit coverage in [Notebook 09 import audit](docs/notebook_09_import_audit.md) and command-surface classification in [Notebook 09 command surface classification](docs/notebook_09_command_surface_classification.md). It remains output-free, metadata-clean, and guarded by `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`. Issue #99 records Colab smoke as `notebook_09_colab_smoke_passed_with_notes`: restore, native strategy comparison, plots, artifact discovery, research summary, checkpoint refresh, and final handoff ran in an executed artifact outside Git. The smoke observed 14 strategies attempted, 11 completed, and 3 strategy-level failures captured as review rows. The executed artifact is not committed and does not prove all-strategy correctness, authoritative performance, artifact completeness, checkpoint generality, or Notebook 10 behavior.

Notebook 10 is imported at [notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb](notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb) as a source-safe StratLake walk-forward robustness and promotion-review notebook, with audit coverage in [Notebook 10 import audit](docs/notebook_10_import_audit.md), [Notebook 10 staging classification](docs/notebook_10_staging_classification.md), and [Notebook 10 command surface classification](docs/notebook_10_command_surface_classification.md). It remains output-free, execution-count-null, metadata-clean, cell-ID-clean, and guarded by `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`, `RUN_STRATLAKE_ARCHIVE_RESTORE = False`, and `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False`. Issue #107 records explicit Colab smoke as `colab_smoke_passed_with_notes`: archive restore completed, restored features/artifacts were discovered, 11 runnable strategies executed successfully in one smoke window, metrics were extracted from `artifact_json`, conservative promotion review produced no promoted/watchlist strategies, and final handoff was produced. The executed artifact remains outside Git. Caveats include a non-blocking package resolver warning, optional DuckDB snapshot restore warning, and a runtime-only archive checkpoint execution with validation/inspection warnings. Smoke mode remains workflow-validation only, not promotion-grade financial evidence; benchmark-avoidance outperformance from flat/inactive strategies is not alpha, and expanded-mode validation is required before any promotion-grade interpretation.

Notebook 11 is imported at [notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb](notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb) as a source-safe StratLake expanded promotion evidence sufficiency review notebook, with audit coverage in [Notebook 11 import audit](docs/notebook_11_import_audit.md), [Notebook 11 staging classification](docs/notebook_11_staging_classification.md), [Notebook 11 command surface classification](docs/notebook_11_command_surface_classification.md), and [Milestone 14 merge readiness](docs/milestone_14_merge_readiness.md). It extends Notebook 10's smoke-mode confidence review into the theme "from confidence review to promotion evidence," defaults to source-safe `expanded_preview`, documents guarded/manual `expanded_run`, and preserves conservative caveats around incomplete platform split metrics and promotion-gate artifacts. Issue #114 records three audited runtime artifacts: guarded `expanded_preview` passed with expected blockers, the first `expanded_run` restored Notebook 10 context but kept expanded execution disabled, and the second `expanded_run` completed four guarded strategy runs with metrics loaded while split metrics, promotion gates, and complete review artifacts remained absent. The final M14 handoff stance is `notebook_11_import_pr_ready`; the final runtime-smoke stance remains `notebook_11_expanded_run_smoke_passed_with_metrics_review_artifacts_incomplete`. Executed artifacts and generated runtime outputs remain outside Git, and committed source does not claim alpha, production readiness, strategy approval, statistical significance, complete platform artifact coverage, CI/runtime equivalence, checkpoint generality, or promotion-grade evidence.

Notebook 12 is imported at [notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb](notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb) as a source-safe StratLake campaign evidence gap review and human-review handoff notebook, with audit coverage in [Notebook 12 import audit](docs/notebook_12_import_audit.md), [Notebook 12 smoke audit summary](docs/notebook_12_smoke_audit_summary.md), [Notebook 12 staging classification](docs/notebook_12_staging_classification.md), [Notebook 12 command surface classification](docs/notebook_12_command_surface_classification.md), and [Milestone 15 merge readiness](docs/milestone_15_merge_readiness.md). It defaults to `cold_smoke_5_command_shape_readiness`, keeps `cold_smoke_1_preview` as the baseline preview profile, and preserves guarded manual profiles for preview, dry-run, validated provisional dry-run, and explicit non-dry-run smoke. Issues #117-#122 staged, classified, statically tested, guardrail-tested, documented, and finalized Notebook 12 for PR readiness. Issue #123 / M15.7 records `notebook_12_cold_smoke_guardrail_matrix_passed_with_no_native_campaign_execution`: preview and command-shape readiness passed with expected caveats, strict missing-filter guardrail passed, campaign smoke preview passed with expected caveats, dry-run and provisional dry-run remained blocked because no verified native dry-run surface was advertised, and `campaign_smoke_execute_allow_provisional_no_dry_run` was intentionally skipped. Notebook 12 separates native campaign artifacts from Notebook 11/12 review artifacts, keeps generated smoke configs classified as `notebook12_generated_smoke_config`, and treats missing campaign context, native artifacts, split metrics, promotion gates, or promotion evidence as caveats or next actions. No native campaign execution, manual non-dry-run smoke, strategy approval, alpha validation, production readiness, statistical significance, CI/native runtime equivalence, or promotion-grade readiness is claimed.

Notebook 13 is imported at [notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb](notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb) as a source-safe StratLake native campaign execution and artifact generation notebook, with audit coverage in [Notebook 13 import audit](docs/notebook_13_import_audit.md), [Notebook 13 smoke audit summary](docs/notebook_13_smoke_audit_summary.md), [Notebook 13 command surface classification](docs/notebook_13_command_surface_classification.md), and [Milestone 16 merge readiness](docs/milestone_16_merge_readiness.md). It defaults to `campaign_execution_preview`, preserves guarded manual `campaign_execution_preflight`, `campaign_execution_run`, and `campaign_execution_run_with_archive_checkpoint` profiles, and keeps archive restore and native execution disabled unless explicit runtime gates are enabled. Issues #126-#130 staged, classified, statically tested, guardrail-tightened, documented, and source-validated Notebook 13; Issue #132 / M16.7 records `notebook_13_runtime_smoke_verified_without_committed_outputs`; Issue #131 / M16.6 records final PR readiness as `notebook_13_import_pr_ready_source_safe_native_smoke_audited`. The audited runtime artifacts stayed outside Git: preview verified no restore/native execution, preflight verified restore and input readiness without native execution, and the full run verified `stratlake-run-research-campaign` return code 0 with artifacts detected. This evidence is not committed notebook output, not CI evidence, and not production, promotion, governance, alpha, statistical-significance, strategy-approval, split-metric-completeness, artifact-completeness, or source/runtime-equivalence proof. Generated configs remain notebook-generated execution candidates with `native_template: false`; requested alpha targets require a real alpha catalog; unknown requested strategies and catalog blockers prevent native execution.

Notebook 14 is imported at [notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb](notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb) as a source-safe campaign-evidence review pack and governance-observation companion, with documentation in the [Notebook 14 importation guide](docs/notebook_14_importation_guide.md) and [Notebook 14 command surface classification](docs/notebook_14_command_surface_classification.md). It defaults to `evidence_governance_preview`, keeps restore, campaign generation, evidence-review build/validation, governance reporting, catalog/lineage export, checkpointing, and runtime summary writes disabled unless explicit temporary-runtime gates are enabled, and preserves `campaign_feature_restore_and_generation_run` plus `existing_campaign_evidence_governance_review` as gated runtime-only profiles. Notebook 14 observes native evidence-review and governance surfaces without replacing native validation or governance, repairing derived packs, creating canonical promotion evidence, or claiming approval, promotion, readiness, deployment, production, alpha validity, statistical significance, live-trading suitability, or source/runtime equivalence.

Local notebook development and execution-readiness checks are documented in the [Notebook Development Environment](docs/notebook_development_environment.md) guide. Final branch scope and merge readiness are summarized in the [Milestone 2 merge-readiness closeout](docs/milestone_2_merge_readiness.md), [Milestone 3 merge-readiness closeout](docs/milestone_3_merge_readiness.md), [Milestone 4 merge-readiness closeout](docs/milestone_4_merge_readiness.md), [Milestone 5 merge-readiness closeout](docs/milestone_5_merge_readiness.md), [Milestone 6 merge-readiness closeout](docs/milestone_6_merge_readiness.md), [Milestone 7 merge-readiness closeout](docs/milestone_7_merge_readiness.md), the [Milestone 8 merge-readiness closeout](docs/milestone_8_merge_readiness.md), the [Milestone 9 merge-readiness closeout](docs/milestone_9_merge_readiness.md), the [Milestone 10 merge-readiness closeout](docs/milestone_10_merge_readiness.md), the [Milestone 11 merge-readiness closeout](docs/milestone_11_merge_readiness.md), the [Milestone 12 merge-readiness closeout](docs/milestone_12_merge_readiness.md), the [Milestone 14 merge-readiness closeout](docs/milestone_14_merge_readiness.md), the [Milestone 15 merge-readiness closeout](docs/milestone_15_merge_readiness.md), and the [Milestone 16 merge-readiness closeout](docs/milestone_16_merge_readiness.md).

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
python scripts/validate_notebook_execution_readiness.py notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb
python -m pytest tests/test_notebook_08_static_cli_restore_artifact_review.py -q
python -m pytest tests/test_notebook_08_source_readiness.py -q
python -m pytest tests/test_notebook_09_static_cli_restore_strategy_comparison_coverage.py -q
python -m pytest tests/test_notebook_09_source_readiness.py -q
python -m pytest tests/test_notebook_10_static_source_contracts.py -q
python -m pytest tests/test_notebook_10_source_readiness.py -q
python -m pytest tests/test_notebook_11_static_source_contracts.py -q
python -m pytest tests/test_notebook_12_source_contracts.py -q
python -m pytest tests/test_notebook_12_artifact_filter_guardrails.py -q
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
```

Validation layers are additive and should be run together:

- CLI contract validation checks broad command-surface examples and bounded safe `--help` contract behavior.
- CLI registry validation is argument-aware and checks known command/subcommand/flag/value syntax against the verified registry, including unsupported flags, boolean/value misuse, constrained `allowed_values`, `argparse_required`, `notebook_contract_required`, `required_when`, and excluded command candidates such as `fintech-restore-session`.
- Execution-readiness validation checks static JSON, output/count, path-fragment, classification, and safe Python syntax.

The Notebook 02, Notebook 03, Notebook 04, Notebook 05, and Notebook 06 targeted registry commands are optional focused confidence checks for restore, archive backup-pack, StratLake initialization, Q1 ingestion, feature-generation, dry-run export, and validation/handoff command surfaces where CLI assumption drift has highest risk. Notebook 08 focused tests inspect source-only restore, strategy, artifact-review, and sanitized readiness surfaces; they do not execute cells or require Colab, Drive, Alpaca credentials, archive packs, native strategy artifacts, or StratLake runtime outputs. Notebook 09 focused tests inspect source-only restore, native strategy comparison, parser/review-row, dataframe, plot, artifact-discovery, research-summary, checkpoint, handoff, and sanitized readiness surfaces; they do not execute cells or require Colab, Drive, Alpaca credentials, archive packs, native strategy artifacts, plots, generated reports, or Notebook 10 runtime behavior. Notebook 10 focused tests inspect source-only restore/archive guards, native command references, feature preflight, walk-forward robustness, promotion review, artifact references, warning taxonomy, benchmark-avoidance interpretation, and handoff fields; they do not execute cells or require Colab, Drive, Alpaca credentials, restored archives, native strategy artifacts, generated review outputs, plots, or promotion-grade evidence. Notebook 11 focused tests inspect source-only hygiene, source-safe defaults, corrected install fallback pattern, Notebook 10 context/artifact references, expanded-run command shape, manual-review candidates, governance/evidence-review guardrails, artifact path boundaries, classification docs, readiness config inclusion, generated-artifact absence, and non-claim/evidence caveat language; they do not execute cells or require Colab, Drive, Alpaca credentials, restored Notebook 10 artifacts, expanded strategy artifacts, governance outputs, generated review packages, or promotion-grade evidence. Notebook 12 focused tests inspect source-only hygiene, profile defaults, smoke guards, generated config source fields, native campaign artifact filtering, Notebook 11/12 review artifact separation, strict campaign/run filters, handoff fields, classification docs, and non-claim boundaries; they do not execute cells or require Colab, Drive, restored campaign archives, native campaign artifacts, generated review artifacts, governance outputs, or promotion-grade evidence. All repository validation layers are non-executing for upstream workflows: they do not run live ingestion/restore/archive/export commands, mount Drive, prompt for credentials, install notebook packages, create backup packs, initialize Fintech or StratLake sessions, generate feature data, call Alpaca, run native strategy backtests, comparisons, walk-forward execution, expanded strategy execution, or campaign execution, generate plots, write review artifacts, or mutate source notebooks. Missing local upstream Fintech and StratLake command warnings remain bounded to the existing CLI contract validator behavior.

For registry schema, policy, and maintenance details, see [CLI Command Registry Guide](docs/cli_command_registry.md).

## GitHub Issue Templates

This repository includes lightweight GitHub issue templates for notebook audits, milestone tasks, and upstream app triage. Use the upstream triage template when a notebook captures a failure that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, including Notebook 09-style cases where one strategy succeeds and other configured strategies fail.

## Planned Notebook Sequence

Notebook 00 through Notebook 14 are imported and tracked in the notebook index. Notebook 15 and later remain planned until they go through the same staged, cleaned, validated, and audited import workflow.

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
- Notebook 10 - walk-forward robustness and promotion review (imported; source-only validated; explicit Colab smoke passed with notes)
- Notebook 11 - expanded promotion evidence review (imported; source-only validated; runtime smoke recorded with incomplete platform artifacts; PR ready as `notebook_11_import_pr_ready`)
- Notebook 12 - campaign evidence gap and promotion readiness review (imported; source-only validated; cold-smoke guardrail matrix passed with no native campaign execution)
- Notebook 13 - native campaign execution and artifact generation (imported; source-only validated; runtime smoke verified outside Git with no readiness claims)
- Notebook 14 - campaign evidence review pack and governance observation (imported; source-only validated; preview-default with no readiness claims)

Current imported notebook chain:

- Notebook 00 establishes setup, session, and storage conventions.
- Notebook 01 runs the Fintech daily bars extraction/backfill workflow through native upstream commands.
- Notebook 02 restores or bootstraps a saved Fintech archive/session backup from Google Drive into `/content`, then validates restored workspace, session metadata, and curated/backfilled data readiness.
- Notebook 03 demonstrates the Fintech archive backup-pack workflow: `SESSION_ID`-derived Drive backup paths, pack dry-run, manual pack creation, backup-pack validation and inspection, local restore, and restored-file verification.
- Notebook 04 introduces the dual-session Fintech/StratLake setup flow: `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` are kept as separate identifiers for the upstream curated-data workspace and the downstream feature/research workspace. The key handoff is the explicit `--marketlake-root` argument that connects StratLake to the Fintech curated-data directory. Notebook 04 does not generate StratLake features; that belongs to Notebook 05.
- Notebook 05 continues the dual-session flow into Q1 daily-bars ingestion and Q1 StratLake feature generation. It keeps `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` distinct, uses `MARKETLAKE_ROOT` as the explicit curated-data handoff, runs active workspace paths under `/content`, and keeps Google Drive as persistence/archive/session storage only.
- Notebook 08 continues from the Notebook 07 archive/session checkpoint shape as a native StratLake strategy/backtest artifact review notebook. It reviews native strategy output, artifact inventory, plottable artifacts, benchmark rows, and handoff context without reimplementing strategy or backtest logic. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source, archive checkpoint refresh remains manual/off-by-default, and committed source does not claim authoritative restore, backtest, artifact-review, benchmark, plot, checkpoint, or handoff success. M11.6 records manual Colab smoke as passed with notes from an uploaded executed artifact that remains outside Git.
- Notebook 09 continues from Notebook 08 as a native StratLake strategy comparison and research review notebook. It preserves restore preview/manual gating, native strategy registry inspection, native multi-strategy comparison via `stratlake-run-strategy`, parsed stdout review rows, comparison dataframe/plot surfaces, artifact discovery by run id, research summary, optional archive checkpoint preview, and Notebook 10 handoff context. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source. Issue #99 records manual Colab smoke as passed with notes: restore, strategy comparison, plots, artifact discovery, research summary, archive checkpoint refresh, and final handoff rendered in an executed artifact outside Git; 14 strategies were attempted, 11 completed, and 3 strategy-level failures were captured as review rows. Committed source does not claim all-strategy correctness, authoritative performance results, benchmark alpha, plot correctness, artifact completeness, checkpoint generality, or Notebook 10 validation.
- Notebook 10 continues from Notebook 08/09 as a native StratLake walk-forward robustness and promotion-review notebook. It preserves restore preview/manual gating, feature-column discovery, native strategy preflight, walk-forward strategy execution via `stratlake-run-strategy`, robustness diagnostics, conservative promotion gates, warning taxonomy review, artifact inventory, optional archive checkpoint preview, and final handoff context. `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains guarded in committed source, restore/checkpoint refresh remain manual/off-by-default, and `NOTEBOOK10_MODE = "smoke"` is workflow-validation only. Issue #107 records explicit Colab smoke as passed with notes: 14 candidate strategies, 11 runnable, 3 feature-contract skips, 11 walk-forward rows, 11 promotion-review rows, no promoted/watchlist strategies, and all evaluated strategies as `needs_review`. Caveats include optional DuckDB snapshot restore warnings and runtime-only archive checkpoint execution with validation/inspection warnings. Committed source does not claim promotion-grade evidence, alpha, expanded-mode validation, artifact completeness, checkpoint success, or runtime correctness.
- Notebook 11 continues from Notebook 10 as an expanded evidence sufficiency review notebook. It asks what additional artifact-backed evidence would be required before a strategy could responsibly move from `needs_review` toward watchlist review or promotion candidacy. It preserves Notebook 10-style Fintech/StratLake initialization, guarded Notebook 10 archive restore, source-safe `expanded_preview` defaults, guarded `expanded_run` strategy execution via `stratlake-run-strategy`, manual-review candidate gating, caveat/blocker review, promotion-readiness interpretation, optional governance schema surfaces, and optional archive checkpoint preview. Issue #114 records `expanded_runs_attempted = 4`, `expanded_runs_completed = 4`, `expanded_metric_rows = 4`, `expanded_split_metric_rows = 0`, `expanded_complete_review_artifact_count = 0`, `eligible_for_human_watchlist_review_count = 0`, and `promotion_grade_claim_made = false` for the successful guarded expanded-run smoke. Issue #113 finalizes the M14 import handoff as `notebook_11_import_pr_ready`. Generated runtime outputs belong under `artifacts/notebook_11_expanded_promotion_evidence_review/` and stay out of Git. Committed source does not claim alpha, production readiness, strategy approval, statistical significance, complete platform artifact coverage, CI/runtime equivalence, checkpoint generality, or promotion-grade evidence.
- Notebook 12 continues from Notebook 11 as a campaign evidence gap and human-review handoff notebook. It preserves source-safe `cold_smoke_5_command_shape_readiness` defaults, `cold_smoke_1_preview` baseline preview, guarded campaign smoke profiles, optional archive restore, Notebook 11 context discovery, native campaign artifact discovery, Notebook 12 review artifact separation, caveat registration, optional archive checkpoint preview, and final handoff. Issue #122 finalizes the M15 import handoff as `notebook_12_import_pr_ready`; Issue #123 / M15.7 records the cold-smoke guardrail matrix stance `notebook_12_cold_smoke_guardrail_matrix_passed_with_no_native_campaign_execution`. Generated runtime outputs belong under `artifacts/notebook_12_campaign_evidence_gap_promotion_readiness/` and stay out of Git. Source-only tests cover profile/claim/handoff fields and artifact/context guardrails. Committed source does not claim native campaign execution, manual non-dry-run smoke, complete campaign artifacts, alpha, production readiness, strategy approval, statistical significance, CI/native runtime equivalence, or promotion-grade readiness.
- Notebook 13 continues from Notebook 12 as a guarded native campaign execution and artifact generation notebook. It preserves source-safe `campaign_execution_preview` defaults, manual restore/preflight/run profiles, `stratlake-init-notebook --root /content/stratlake`, guarded `stratlake-session-archive-restore-bootstrap`, generated native `research_campaign` execution-candidate configs, catalog/strategy/alpha guardrails, `stratlake-run-research-campaign --config <config>`, artifact inventory, caveat registration, optional governance/reporting/checkpoint surfaces, and final handoff. Issue #130 records `notebook_13_import_docs_and_smoke_audit_ready`; Issue #132 records `notebook_13_runtime_smoke_verified_without_committed_outputs` across preview, preflight, and full run profiles. Preview verified no restore or native execution, preflight verified restore and input readiness without native execution, and full run verified native execution return code 0 with artifacts detected in an executed artifact outside Git. Generated runtime outputs belong under `artifacts/notebook_13_native_campaign_execution_and_artifact_generation/` and stay out of Git. Source-only tests cover profiles, gates, config provenance, catalog/strategy/alpha blockers, artifact/handoff fields, and non-claim boundaries. Committed source does not claim production readiness, strategy approval, alpha validation, statistical significance, governance readiness, promotion readiness, split-metric completeness, artifact completeness, generated configs as upstream templates, committed smoke evidence, or source/runtime equivalence.

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
