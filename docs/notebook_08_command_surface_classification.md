# Notebook 08 Command Surface Classification

## Purpose

Notebook 08 (`notebooks/08_stratlake_strategy_backtest_artifact_review.ipynb`) is a
**StratLake strategy backtest artifact review** notebook. It continues from Notebook 07,
reattaches to the StratLake session/archive shape when a user-configured Drive root is
available, and reviews native StratLake strategy output, generated artifacts, plots, and
benchmark comparison rows.

This document classifies the command, restore, strategy, backtest, artifact, benchmark,
plot, runtime, and handoff surfaces in the staged source.

**Source classification is not live runtime validation.** The classifications here describe
what each surface is intended to do when the notebook is executed in a live Colab or local
runtime. Passing repository source checks does not mean archive restore, strategy backtest,
artifact discovery, benchmark review, plot generation, archive checkpoint refresh, or handoff
summary execution has succeeded. Live Colab smoke is deferred to M11.6.

---

## Classification Legend

| Category | Meaning |
|---|---|
| `dependency_install_surface` | Package installation required for a fresh notebook runtime. |
| `credential_configuration_surface` | Runtime-only credential or Colab Drive setup. |
| `drive_session_root_configuration_surface` | Placeholder-guarded workspace, Drive, and session path setup. |
| `live_runtime_command_surface` | CLI command intended to run during normal live notebook execution. |
| `manual_off_by_default_command_surface` | CLI command preserved for a deliberate manual action but disabled in committed source. |
| `runtime_inspection_surface` | Path, config, file, artifact, or DataFrame inspection performed in notebook runtime. |
| `native_strategy_review_surface` | Native StratLake strategy/backtest execution and review flow. |
| `stdout_parsing_review_surface` | Notebook parsing of native CLI stdout for review rows, not authoritative reporting. |
| `artifact_review_surface` | Discovery or loading of native artifacts for inspection. |
| `visual_review_surface` | Plotting of native artifacts or parsed summary metrics. |
| `handoff_summary_surface` | Runtime summary intended to orient the next notebook. |
| `source_hygiene_guard` | Guards that keep committed source placeholder-driven, output-free, and non-mutating by default where needed. |
| `repository_source_only` | Source-level notebook properties such as cleared outputs, null execution counts, and stripped metadata. |

---

## Notebook 08 Section Classification

| # | Section | Surface type | Runtime behavior | Source-safety stance | Later coverage target |
|---|---|---|---|---|---|
| 1 | Install package dependencies | dependency/install surface | Runs `!pip install` for `pandas-market-calendars`, `fintech-market-ingestion`, and `stratlake-trade-engine` in a live runtime. | Manual runtime only; skipped by static readiness checks as network/package install and shell magic. | M11.3 static command/source coverage; M11.6 Colab smoke notes. |
| 2 | Mount Google Drive and set credentials | credential/configuration surface | Mounts Google Drive in Colab and prompts/reads Alpaca credentials into environment variables. | Runtime-only; no credential values are committed or printed. | M11.4 sanitized source validation; M11.6 smoke notes for credential setup boundary. |
| 3 | Configure workspace, Drive roots, and research windows | Drive/session-root configuration surface | Defines `WORKSPACE_ROOT`, `DRIVE_FOLDER_NAME`, `DRIVE_ROOT`, Fintech/StratLake roots, session names, Q1 dates, and local runtime roots. | `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` raises before Drive folder creation; hardcoded tutorial Drive root is absent. | M11.3 static guard coverage; M11.4 readiness validation. |
| 4 | Initialize or attach the Fintech notebook session | Fintech project/session init surface | `RUN_FINTECH_INIT_PROJECT = True` runs `fintech-init-project` and discovers the active session manifest. | Intended live runtime workflow gate; not proof of source-import success. Creates runtime folders/manifests only when executed. | M11.3 CLI coverage for command shape; M11.6 runtime notes. |
| 5 | Initialize or attach the StratLake notebook session | StratLake project/session init surface | `RUN_STRATLAKE_INIT_SESSION = True` runs `stratlake-init-session`, writes notebook configs, and attaches to `MARKETLAKE_ROOT`. | Intended live runtime workflow gate; depends on Drive placeholder replacement before Drive paths are created. | M11.3 CLI coverage for command shape and flags; M11.6 runtime notes. |
| 6 | Verify attached session paths and notebook configs | source-readiness/path inspection surface | Builds a DataFrame of expected Fintech, StratLake, config, feature, and archive paths. | Inspection only; displays existence state without proving runtime correctness. | M11.4 source-readiness/sanitized validation. |
| 7 | Verify the Notebook 07 StratLake archive checkpoint | archive checkpoint discovery surface | Prints expected archive pack path and previews archive contents if present. | Review-only discovery; does not prove Notebook 07 archive creation or restore success. | M11.3 archive path/static coverage; M11.6 smoke notes if exercised. |
| 8 | Restore the Notebook 07 StratLake archive checkpoint | archive restore CLI surface | `RUN_STRATLAKE_ARCHIVE_RESTORE = False`; prints `stratlake-session-archive-restore-bootstrap` command preview unless user enables it. | Manual/off-by-default source-safe action; must not run during import or validation. | M11.3 static restore guard/flag coverage; M11.6 smoke notes if manually run. |
| 9 | Verify restored StratLake configs, features, and artifacts | restored input validation surface | Checks restored `configs/*.yml`, `features_daily`, and `artifacts` paths, then counts feature/artifact files. | Runtime inspection only; source import does not claim restored state exists. | M11.4 readiness validation; M11.6 smoke notes. |
| 10 | Verify native StratLake workspace inputs | native config/feature/artifact input surface | Checks native root, MarketLake root, config files, and feature directory. | Review-only path inspection; no files are generated by source validation. | M11.4 source-only readiness validation. |
| 11 | Inspect native strategy registry | native strategy registry inspection surface | Reads and parses `configs/strategies.yml`, then displays strategy metadata. | Native config review only; does not prove strategy execution. | M11.3 static config-reference coverage; M11.6 runtime notes. |
| 12 | Run native StratLake strategy backtest | native strategy execution CLI surface | `RUN_NATIVE_STRATEGY_BACKTEST = True` runs `stratlake-run-strategy` with `momentum_v1` over the Q1 window in live runtime. | Intended runtime gate, not source-import evidence. May create native artifacts and logs only when executed. | M11.3 static CLI coverage; M11.6 smoke notes if executed. |
| 13 | Parse native strategy output into review rows | CLI stdout parsing/review surface | Parses native CLI stdout into a single `strategy_result` DataFrame. | Review-only parsing; parsed metrics are not authoritative performance claims. | M11.3 parser-source coverage; M11.4 source-readiness checks. |
| 14 | Discover native artifacts for the run | native artifact discovery surface | Scans `artifacts`, `reports`, and `data` for JSON/CSV/parquet/Markdown/HTML candidates and run-id matches. | Artifact inventory is a review surface; source validation does not create or verify artifacts. | M11.3 artifact discovery source coverage; M11.6 runtime notes. |
| 15 | Load plottable native time series when available | plottable artifact loading surface | Loads candidate parquet/CSV artifacts with date-like and numeric columns for plotting. | Runtime artifact loading only; source import does not claim time-series availability. | M11.4 source readiness; M11.6 smoke notes. |
| 16 | Plot native strategy review output | plot/review surface | Plots native time series when present, otherwise parsed summary metrics. | Visual review only; committed notebook remains output-free and does not commit plots. | M11.6 smoke notes if visual output is generated. |
| 17 | Benchmark comparison review | benchmark comparison surface | Selects benchmark-related columns from `strategy_result` into `benchmark_review`. | Review-only DataFrame; not authoritative benchmark or performance reporting. | M11.3 source coverage; M11.6 runtime notes. |
| 18 | Optional archive checkpoint refresh | archive checkpoint refresh CLI surface | `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False`; prints/runs `stratlake-session-archive-bootstrap` only if manually enabled. | Manual/off-by-default source-safe action; must not run during import or validation. | M11.3 static checkpoint guard coverage; M11.6 smoke notes only if explicitly run. |
| 19 | Final Notebook 08 handoff summary | handoff summary surface | Displays runtime summary with session ids, archive path, restore flag, strategy status, run id, artifact count, and time-series row count. | Runtime handoff only; source import does not claim summary values or success. | M11.5 docs/index updates; M11.7 merge-readiness closeout. |

---

## Manual And Runtime Gates

| Gate | Default | Classification | Source-only validation stance |
|---|---:|---|---|
| `RUN_STRATLAKE_ARCHIVE_RESTORE` | `False` | Manual/off-by-default archive restore CLI surface. | Must not execute during import, static coverage, or source-readiness validation. |
| `RUN_STRATLAKE_ARCHIVE_CHECKPOINT` | `False` | Manual/off-by-default archive checkpoint refresh CLI surface. | Must not execute during import, static coverage, or source-readiness validation. |
| `RUN_FINTECH_INIT_PROJECT` | `True` | Intended live Fintech session initialization workflow gate. | May remain true in source; static validation must distinguish intent from runtime success. |
| `RUN_STRATLAKE_INIT_SESSION` | `True` | Intended live StratLake session initialization workflow gate. | May remain true in source; static validation must not treat it as evidence of initialized sessions. |
| `RUN_NATIVE_STRATEGY_BACKTEST` | `True` | Intended live native strategy/backtest execution workflow gate. | May remain true in source; static validation must not execute it or claim strategy success. |

---

## Command Surface Classification

| Command | Notebook use | Previewed, guarded, or executed during normal runtime | Source-only validation stance | Drive placeholder dependency | Runtime artifact risk | Later static coverage target |
|---|---|---|---|---|---|---|
| `fintech-init-project` | Creates/attaches Fintech project and session using `--root`, `--session-name`, `--with-session`, and `--colab-profile`. | Executed when `RUN_FINTECH_INIT_PROJECT = True`. | Do not execute; verify source references and flag shape only. | Indirect: session Drive backup paths are guarded by `DRIVE_FOLDER_NAME` before folder creation. | May create project/session folders and session manifests. | M11.3 static CLI/source coverage. |
| `stratlake-init-session` | Creates/attaches StratLake project/session using `--root`, `--project-name`, `--marketlake-root`, `--drive-root`, `--enable-drive-persistence`, and `--notebook-configs`. | Executed when `RUN_STRATLAKE_INIT_SESSION = True`. | Do not execute; verify source references and flag shape only. | Yes, `--drive-root` uses placeholder-derived `DRIVE_ROOT`. | May create configs, session files, and runtime directories. | M11.3 static CLI/source coverage. |
| `stratlake-session-archive-restore-bootstrap` | Restores Notebook 07 StratLake archive into `STRATLAKE_ROOT`. | Guarded by `RUN_STRATLAKE_ARCHIVE_RESTORE = False`; command preview is printed by default. | Do not execute; assert false default and preview/flag shape. | Yes, archive pack path is under placeholder-derived Drive archive root. | May restore configs, features, artifacts, and overwrite target files when manually enabled. | M11.3 static restore guard and command coverage. |
| `stratlake-run-strategy` | Runs native `momentum_v1` strategy for `ANALYSIS_START` to `ANALYSIS_END` using `configs/strategies.yml`. | Executed when `RUN_NATIVE_STRATEGY_BACKTEST = True` in live runtime. | Do not execute; verify source command shape and parser/handoff references. | Indirect: restored/session inputs may come from Drive-backed archive paths. | May create native artifacts, reports, logs, or data outputs. | M11.3 static CLI and artifact-review coverage. |
| `stratlake-session-archive-bootstrap` | Optionally refreshes StratLake archive checkpoint with features, artifacts, and configs. | Guarded by `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False`; command preview is printed by default. | Do not execute; assert false default and preview/flag shape. | Yes, `--drive-root` uses `STRATLAKE_DRIVE_ARCHIVE_ROOT`. | May create or overwrite archive packs when manually enabled. | M11.3 static checkpoint guard and command coverage. |

---

## File And Path Surface Classification

| Path or variable | Classification | Source-safety stance |
|---|---|---|
| `DRIVE_FOLDER_NAME` | Source-safe placeholder. | Committed as `REPLACE_WITH_DRIVE_FOLDER_NAME`; must be replaced before live Drive execution. |
| `DRIVE_ROOT` | Placeholder-derived Drive persistence root. | Built from `Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME` in Colab and `WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME` locally. |
| `FINTECH_ROOT` | Local active Fintech workspace path. | Created under `WORKSPACE_ROOT`; runtime-generated contents must not be committed. |
| `STRATLAKE_ROOT` | Local active StratLake workspace path. | Created under `WORKSPACE_ROOT`; restored/generated StratLake contents must not be committed. |
| `MARKETLAKE_ROOT` | Fintech curated handoff path. | Runtime input/review path under `FINTECH_ROOT`; not a committed artifact path. |
| `DAILY_BARS_ROOT` | Daily bars input path. | Runtime data path under `MARKETLAKE_ROOT`; source validation does not require files. |
| `FINTECH_DRIVE_ROOT` | Drive persistence namespace for Fintech. | Derived from `DRIVE_ROOT`; guarded before directory creation. |
| `STRATLAKE_DRIVE_ROOT` | Drive persistence namespace for StratLake. | Derived from `DRIVE_ROOT`; guarded before directory creation. |
| `STRATLAKE_DRIVE_SESSION_ROOT` | Drive session path for StratLake. | Runtime Drive persistence path; requires placeholder replacement. |
| `STRATLAKE_DRIVE_ARCHIVE_ROOT` | Drive archive root for StratLake session. | Runtime archive persistence path; requires placeholder replacement. |
| `STRATLAKE_ARCHIVE_PACK_DIR` | Expected Notebook 07 archive pack path. | Review/restore path only; source import does not claim it exists. |
| `FEATURES_DAILY_ROOT` | Native feature input/review path. | Runtime restored/generated path under `STRATLAKE_ROOT`; source validation does not require parquet files. |
| `STRATEGIES_CONFIG` | Native strategy registry config path. | Runtime config path under `STRATLAKE_ROOT / "configs" / "strategies.yml"`; source validation may check reference only. |

---

## Artifact And Review Surface Classification

| Review surface | Notebook source object/path | Classification | Non-claim |
|---|---|---|---|
| Restored configs | `configs/universe.yml`, `configs/paths.yml`, `configs/strategies.yml` | Restored input validation surface. | Source import does not prove configs were restored. |
| Restored features | `data/curated/features_daily` | Restored feature input review surface. | Source import does not prove features exist or are valid. |
| Restored artifacts | `artifacts` | Restored artifact review surface. | Source import does not prove artifacts exist or match Notebook 07. |
| Native strategy registry | `configs/strategies.yml` | Native registry inspection surface. | Registry parsing is not proof of strategy execution. |
| Native strategy stdout | `native_strategy_stdout`, `native_strategy_stderr`, `native_strategy_returncode` | Native CLI review surface. | No stdout exists in committed source; runtime stdout is not authoritative performance proof. |
| Parsed strategy rows | `strategy_result`, `strategy_result_row`, `run_id` | Stdout parsing/review surface. | Parsed metrics are review rows, not authoritative performance reporting. |
| Artifact inventory | `artifact_inventory` | Native artifact discovery surface. | Inventory is candidate discovery, not artifact validation. |
| Native time-series artifacts | `native_time_series`, `time_series_source` | Plottable artifact loading surface. | Loading a plottable file does not prove complete artifact correctness. |
| Plot output | Matplotlib plot cell | Visual review surface. | Plots are not committed and are not proof of backtest success. |
| Benchmark review | `benchmark_review` | Benchmark comparison review surface. | Benchmark rows are non-authoritative unless later runtime smoke documents the source and outcome. |
| Final handoff summary | `summary` DataFrame | Handoff summary surface. | Summary values are live-runtime orientation only, not source-import evidence. |

---

## Risk And Guardrails

- Accidental Drive-specific path leakage: keep `DRIVE_FOLDER_NAME` as the only committed Drive folder placeholder and avoid real Drive folders in source/docs.
- Accidental restore execution during source validation: keep `RUN_STRATLAKE_ARCHIVE_RESTORE = False` and never execute Notebook 08 in M11.2.
- Accidental archive checkpoint refresh: keep `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False` and do not create archive packs.
- Accidental committed outputs: keep Notebook 08 output-free, execution counts null, and cell metadata minimized.
- Notebook-side drift from native StratLake logic: preserve `stratlake-run-strategy` as the native strategy surface and do not reimplement backtest logic in the notebook.
- Treating parsed stdout metrics as authoritative: classify stdout parsing as a review surface only.
- Treating source import as proof of archive restore or backtest success: defer runtime evidence to M11.6 smoke notes.

---

## Later-Issue Handoff

| Follow-up | Scope |
|---|---|
| M11.3 / Issue #87 | Add static CLI, restore, and artifact review coverage for Notebook 08. |
| M11.4 / Issue #88 | Add source-only readiness and sanitized validation coverage. |
| M11.5 / Issue #89 | Update import audit, notebook index, development docs, and README. |
| M11.6 / Issue #90 | Perform Colab smoke test from committed source and document runtime notes. |
| M11.7 / Issue #91 | Merge-readiness closeout. |

---

## M11.2 Non-Claims

Notebook 08 was not executed for this classification issue. M11.2 does not claim archive
restore success, archive export/checkpoint success, native strategy success, backtest
success, artifact-review success, benchmark correctness, plot correctness, or final
handoff summary correctness. It classifies the committed source so later issues can add
static coverage, source-readiness checks, documentation updates, smoke notes, and final
merge-readiness evidence.
