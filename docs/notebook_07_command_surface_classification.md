# Notebook 07 Command Surface Classification

## Purpose

Notebook 07 (`notebooks/07_stratlake_feature_consumption_baseline_research.ipynb`) is a
**feature-consumption and baseline research-smoke** notebook. It consumes the Notebook 06
Fintech → StratLake feature handoff, prefers native StratLake CLI/package surfaces where
available for the strategy smoke test, and provides a lightweight notebook-local fallback
diagnostic as a secondary, non-authoritative path.

This document classifies every major command, runtime, native strategy-smoke, fallback
diagnostic, restore/export/archive, and visualization surface in the staged source.

**Source classification is not live runtime validation.** The classifications here describe
what each surface is intended to do when the notebook is executed in a live Colab or local
runtime. Passing repository source checks (no outputs, no secret patterns, clean metadata)
does not mean that live Colab runtime has succeeded. Live Colab smoke is deferred to M10.6.

---

## Classification legend

| Category | Meaning |
|---|---|
| `live_manual_runtime` | Commands/cells that require live Colab or local runtime execution and may change local workspace state. |
| `live_manual_runtime_conditional` | Runtime cells that execute only when a user-controlled flag or missing-data condition triggers them. |
| `live_manual_runtime_dry_run` | Runtime commands intended to inspect or preview behavior without writing final archive/export contents. |
| `preview_manual_guidance` | Command construction or printed guidance that should not be treated as executed or verified. |
| `optional_commented_manual_restore` | Restore/recovery surfaces intentionally guarded by booleans or comments; not executed by default. |
| `availability_check_only` | Checks that discover whether commands are installed or exposed, without confirming end-to-end contract behavior. |
| `notebook_python_runtime` | Python cells that inspect, parse, summarize, or prepare runtime data inside the notebook. |
| `runtime_inspection` | Data discovery, parquet scanning, sample loading, coverage diagnostics, and config/path inspection. |
| `runtime_visualization` | Plotting or display cells that render runtime results but are not source validation. |
| `native_strategy_smoke` | Native StratLake CLI/package strategy-smoke path, preferred over fallback diagnostics when available. |
| `fallback_diagnostic_only` | Notebook-local fallback diagnostics that are explicitly non-authoritative; not canonical strategy logic. |
| `contract_mismatch_or_unverified` | Surfaces that may exist only in some package versions, or are printed as candidates/previews without registry confirmation. |
| `source_hygiene_guard` | Guards added to keep committed repository source safe, such as Drive folder placeholders and archive off-by-default flags. |
| `repository_source_only` | Source-level notebook properties: output-free committed state, metadata cleanup, no generated artifacts. |

---

## Notebook 07 command/runtime surface table

| # | Notebook section | Cells | Surface | Classification | Default behavior | Repository stance | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Install notebook dependencies and project packages | 01–02 | `!pip install "pandas-market-calendars>=5.0"`, TestPyPI installs of `fintech-market-ingestion` and `stratlake-trade-engine` | `live_manual_runtime` | Runs on first cell execution in fresh runtime | Manual runtime; not source validation | Install cell is required before other cells can run |
| 2 | Verify expected CLIs | 03–04 | Required commands: `fintech-init-project`, `fintech-backfill-daily`, `fintech-save-session`, `fintech-restore-session`, `fintech-backup-data`, `stratlake-init-session`, `stratlake-build-features`, `stratlake-session-export`, `stratlake-session-import`, `stratlake-session-archive-bootstrap`, `stratlake-session-archive-restore-bootstrap`. Optional strategy commands: `stratlake-run-strategy`, `stratlake-backtest`, `stratlake-run-backtest`, `stratlake-compare-strategies` | `availability_check_only` | Raises `RuntimeError` if required commands are missing | Detects command presence; does not prove contract correctness or end-to-end behavior | Optional strategy commands are printed as availability guidance only |
| 3 | Imports and Google Drive mount | 05–06 | `drive.mount("/content/drive")` | `live_manual_runtime` | Runs only when `IN_COLAB` is `True` | Colab-only runtime side effect; no-op outside Colab | Drive mount does not affect committed source |
| 4 | Configure workspace and tutorial roots | 07–08 | `WORKSPACE_ROOT`, `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`, `DRIVE_ROOT` computed from placeholder, `FINTECH_ROOT` / `STRATLAKE_ROOT` under active workspace, `raise ValueError` guard | `source_hygiene_guard` + `notebook_python_runtime` | Repository default requires user to set `DRIVE_FOLDER_NAME` before Drive folder creation; raises `ValueError` if placeholder is unchanged | Repository-safe default; Drive paths are not created against a hardcoded private path | Analysis window, padded backfill/build window, and session name defaults are also configured here |
| 5 | Initialize or attach to the Fintech session | 09–10 | `FINTECH_SESSION_ID_OVERRIDE`, `fintech-init-project --root ... --session-name ... --with-session --colab-profile`, session manifest discovery, `.fintech/session.json` fallback | `live_manual_runtime` | Runs `fintech-init-project` when no override is set; falls back to session name if manifest is not found | Creates or attaches a runtime session; not source validation | Override pattern allows reconnecting to a prior Notebook 05/06 session |
| 6 | Initialize or attach to the StratLake session | 11–12 | `STRATLAKE_SESSION_ID_OVERRIDE`, `stratlake-init-session --root ... --project-name ... --marketlake-root ... --drive-root ... --enable-drive-persistence --notebook-configs`, `.stratlake/session.json` discovery | `live_manual_runtime` | Runs `stratlake-init-session` when no override is set | Creates or attaches a runtime session; `--notebook-configs` makes `configs/universe.yml` and `configs/paths.yml` available | `MARKETLAKE_ROOT` is defined here as the explicit Fintech → StratLake handoff |
| 7 | Build session-scoped Drive paths and archive identifiers | 13–14 | `FINTECH_DRIVE_SESSION_ROOT`, `STRATLAKE_DRIVE_SESSION_ROOT`, `FINTECH_BACKUP_PACK_DIR`, `STRATLAKE_ARCHIVE_PACK_DIR`, second `DRIVE_FOLDER_NAME` guard, Drive directory `mkdir` | `source_hygiene_guard` + `notebook_python_runtime` | Drive directories are created only after both `DRIVE_FOLDER_NAME` guards pass | Guarded path construction; Drive `mkdir` occurs only after user sets `DRIVE_FOLDER_NAME` | Second guard mirrors M9 Notebook 06 defensive pattern |
| 8 | Configure Alpaca credentials for standalone recovery/backfill | 15–16 | Colab `userdata` / `getpass`, `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY`, `ALPACA_DATA_BASE_URL`, `ALPACA_FEED` | `live_manual_runtime` | Prompts for credentials at runtime; raises `ValueError` if missing | Runtime-only; no credential values are committed | Credentials are set in environment variables only; not printed |
| 9 | Optional restore previews | 17–18 | `RESTORE_FINTECH_ARCHIVE = False`, `RESTORE_STRATLAKE_ARCHIVE = False`, `fintech-backup-data restore` preview, `stratlake-session-archive-restore-bootstrap` preview | `optional_commented_manual_restore` + `preview_manual_guidance` | Preview-only by default; restores execute only when booleans are set to `True` | Guarded/manual restore preview; not executed by committed source | Archive/bootstrap restore contracts remain unverified unless separately confirmed against upstream package registry |
| 10 | Verify notebook config files and session portability | 19–20 | `configs/universe.yml`, `configs/paths.yml` presence check, `raises FileNotFoundError` if missing | `runtime_inspection` | Raises `FileNotFoundError` if required config files are absent | Runtime path/config presence check; not a contract verification | Config files should be produced by `stratlake-init-session --notebook-configs` |
| 11 | Discover Fintech curated daily bars | 21–23 | `file_inventory(MARKETLAKE_ROOT)`, `extract_date_coverage_from_parquets`, Hive-style partition scanning | `runtime_inspection` | Scans local `MARKETLAKE_ROOT` for parquet files; displays inventory and date coverage | Local runtime data inspection only; no files are created or modified | Helper functions defined here are also used in subsequent discovery cells |
| 12 | Optional padded daily-bars backfill | 24–26 | `RUN_SMALL_DAILY_BARS_BACKFILL = True`, `FORCE_DAILY_BARS_BACKFILL = False`, `fintech-backfill-daily --symbols ... --start BACKFILL_START --end BACKFILL_END ...`, padded window coverage validation | `live_manual_runtime_conditional` | Backfill runs only when `RUN_SMALL_DAILY_BARS_BACKFILL` is `True` and daily bar files are missing (or `FORCE_DAILY_BARS_BACKFILL` is `True`) | Conditional runtime recovery/backfill; not repository validation | Padded window (`BACKFILL_START`/`BACKFILL_END`) covers Q1 warmup and forward-return buffer |
| 13 | Discover StratLake feature outputs | 27–28 | `file_inventory` across `FEATURES_DAILY_ROOT` and candidate roots, `resolve_existing_root` | `runtime_inspection` | Scans candidate roots under `STRATLAKE_ROOT` for feature parquet files; displays inventory | Runtime feature discovery only | Candidate root list covers several possible StratLake layout variants |
| 14 | Optional feature build if outputs are missing | 29–31 | `RUN_FEATURE_BUILD_IF_MISSING = True`, `FORCE_FEATURE_BUILD = False`, `stratlake-build-features --timeframe 1D --start FEATURE_BUILD_START --end FEATURE_BUILD_END ...` | `live_manual_runtime_conditional` | Build runs only when `RUN_FEATURE_BUILD_IF_MISSING` is `True` and no feature files are found (or `FORCE_FEATURE_BUILD` is `True`) | Conditional runtime feature build; not repository validation | Uses same padded window as backfill |
| 15 | Load representative daily-bars and feature samples | 32–33 | `load_parquet_sample(daily_bar_files, ...)`, `load_parquet_sample(feature_files, ...)`, Q1 filtering | `runtime_inspection` + `notebook_python_runtime` | Loads up to 80 files each into DataFrames; displays column inventory | Runtime data loading only; samples are not committed | Loaded samples feed coverage diagnostics and optional fallback diagnostic |
| 16 | Prepare loaded parquet samples for coverage diagnostics | 34–35 | `normalize_symbol_date_frame`, `bars_analysis`, `features_analysis`, Q1 window filtering, NaN coverage report | `runtime_inspection` + `notebook_python_runtime` | Normalizes symbol/date columns; computes Q1-filtered views and NaN coverage | Diagnostic-only normalization; native CLI commands remain the authoritative strategy/signal path | Comment in cell source explicitly labels this as diagnostic-only normalization |
| 17 | Native StratLake CLI strategy smoke test | 36–37 | `RUN_NATIVE_BASELINE_SMOKE = True`, `NATIVE_STRATEGY_NAME = "momentum_v1"`, `STRATEGY_START = ANALYSIS_START`, `STRATEGY_END = ANALYSIS_END`, `stratlake-run-strategy --strategies-config configs/strategies.yml --strategy momentum_v1 --start ... --end ...`, `parse_native_strategy_stdout`, `discover_native_strategy_timeseries` | `native_strategy_smoke` + `live_manual_runtime` | Runs `stratlake-run-strategy` when `RUN_NATIVE_BASELINE_SMOKE` is `True` and `configs/strategies.yml` exists; sets `native_smoke_completed = True` on return code 0 | Preferred smoke path; not proven by committed source | Skipped gracefully when `configs/strategies.yml` is absent; triggers fallback path via `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE` |
| 18 | Native strategy smoke-test outcome display | 38 | `native_strategy_status_df`, `native_smoke_completed`, `fallback_needed`, `run_id`, `qa_status`, `qa_rows`, `qa_symbols` | `runtime_inspection` | Displays a summary DataFrame of native smoke-test status | Displays runtime status only; not a source-level validation result | `fallback_needed` field reflects whether `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE` is `True` |
| 19 | Fallback-only notebook-local diagnostic | 39–40 | `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE = not native_smoke_completed`, feature/forward-return join, `source = notebook_local_fallback_diagnostic`, `strategy = feature_rank_fallback` | `fallback_diagnostic_only` | Runs only when `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE` is `True` (i.e., native smoke did not complete) | Secondary diagnostic only; explicitly non-canonical strategy logic | See "Native strategy vs fallback stance" section |
| 20 | Smoke-test plot cell | 41 | Native strategy time-series plot, native summary metrics bar chart, fallback cumulative long/short spread | `runtime_visualization` | Plots whichever output is available: native time series > native summary metrics > fallback spread | Visualization only; no committed plot output | Plot cell is useful in all three cases by design |
| 21 | Strategy/backtest command discovery | 42–43 | Candidates: `stratlake-run-strategy`, `stratlake-backtest`, `stratlake-run-backtest`, `python -m src.cli.run_strategy`, `python -m src.cli.backtest` | `availability_check_only` + `preview_manual_guidance` | Checks `shutil.which` availability for each candidate; prints guidance | Command discovery only; not registry confirmation | Do not treat every candidate as confirmed registry coverage in M10.2 |
| 22 | Export StratLake session to Drive, dry run | 44–45 | `stratlake-session-export --root ... --drive-root ... --include-features --include-artifacts --include-configs --dry-run` | `live_manual_runtime_dry_run` | Runs the dry-run export command; catches `FileNotFoundError` if command is absent | Dry-run only; not proof of export or archive success | `FileNotFoundError` catch handles package versions that do not expose this command |
| 23 | Optional StratLake archive checkpoint | 46–47 | `stratlake-session-archive-bootstrap --root ... --archive-id ... --drive-root ... --include-features --include-artifacts --include-configs ...`, `CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION = False` | `preview_manual_guidance` + `source_hygiene_guard` | Preview-only by default; archive runs only when `CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION` is set to `True` | Manual/off-by-default archive preview; not executed by committed source | Default changed to `False` in M10.1 source hygiene; archive/bootstrap contract remains unverified |
| 24 | Final Notebook 07 handoff summary | 48–49 | Runtime summary dictionary with session IDs, path counts, native smoke status, and `smoke_result`/`smoke_timeseries` row counts; Notebook 08 handoff message | `notebook_python_runtime` + `runtime_inspection` | Prints a JSON summary at runtime | Runtime summary only; generated JSON output is not committed | Points explicitly to Notebook 08 for formal strategy/backtest artifacts |

---

## Native strategy vs fallback stance

Notebook 07 maintains a clear hierarchy between native StratLake strategy execution and the
notebook-local fallback diagnostic:

**Native StratLake strategy smoke is the preferred path.** When `configs/strategies.yml`
exists and `stratlake-run-strategy` is available, Notebook 07 runs the native CLI command
against the Q1 analysis window (`ANALYSIS_START` / `ANALYSIS_END`). If the command succeeds
(`returncode == 0`), `native_smoke_completed` is set to `True` and `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE`
is set to `False`. The fallback diagnostic cell is skipped entirely.

**Notebook-local fallback diagnostic is explicitly secondary.** When the native CLI path is
unavailable or fails, `RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE` is set to `True`. The fallback
cell checks only whether loaded feature rows can be joined to daily bars, and computes a
feature-rank / forward-return long/short spread as a basic coverage diagnostic. The fallback
result is labeled `source = notebook_local_fallback_diagnostic` and
`strategy = feature_rank_fallback`.

**The fallback diagnostic is not canonical strategy logic.** It does not implement or
replicate the StratLake strategy/backtest framework. It should not be interpreted as formal
backtest performance. It is retained only as a handoff quality gate: if even the fallback
join fails, there is a fundamental data alignment problem to investigate before Notebook 08.

**Formal strategy/backtest artifacts are deferred to Notebook 08.** Notebook 07 is
intentionally scoped as a smoke/consumption notebook. Notebook 08 is where formal
StratLake strategy/backtest artifacts should be produced using package APIs and CLI.

---

## Archive/export/restore stance

**Restore commands are preview-only and guarded.** Both `RESTORE_FINTECH_ARCHIVE` and
`RESTORE_STRATLAKE_ARCHIVE` default to `False`. The restore cells print the command
previews but do not execute them. The `stratlake-session-archive-restore-bootstrap` contract
has not been verified against the upstream package registry and should not be treated as
confirmed.

**Dry-run export is runtime dry-run only.** The `stratlake-session-export --dry-run` call
runs in a live runtime to preview export scope. It does not write final archive contents.
It does not prove that export success has been achieved; a `FileNotFoundError` catch covers
package versions that do not expose this command.

**Archive checkpoint is manual and off-by-default.** `CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION`
was changed from `True` to `False` in M10.1. The archive bootstrap command preview is
printed but not executed. Setting the flag to `True` is a deliberate manual action.

**Archive/bootstrap command contracts remain unverified.** `stratlake-session-archive-bootstrap`
and `stratlake-session-archive-restore-bootstrap` are listed in the required CLI check cell
and the optional restore preview cell. Their actual flag contracts should not be promoted
to verified coverage unless checked against the upstream `stratlake-trade-engine` package
registry or confirmed in a live smoke session.

---

## Source validation vs runtime validation

| Milestone | Scope |
|---|---|
| M10.1 | Cleaned committed source: output-free, execution counts reset, metadata stripped, Drive root guarded, archive default off. |
| M10.2 | Command and runtime surface classification (this document). |
| M10.3 | Static CLI/source contract coverage checks (follow-up). |
| M10.4 | Source-only readiness checks and sanitized validation (follow-up). |
| M10.5 | Docs/index/README updates (follow-up). |
| M10.6 | Actual Colab smoke execution and result recording (follow-up). |
| M10.7 | Final merge readiness gate (follow-up). |

Passing source checks (no outputs, no secret patterns, clean metadata, readiness script) does
**not** mean that live Colab runtime has succeeded. Source checks validate the committed
notebook artifact. Runtime success requires live execution in a Colab or local environment
with installed packages, valid credentials, and available network access.
