# Notebook 09 Command Surface Classification

## 1. Purpose

Notebook 09 (`notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb`) is a source-safe StratLake strategy comparison and research review notebook. It follows Notebook 08 by restoring or attaching to the prior StratLake archive/session shape, reviewing native strategy registry and comparison output, discovering native artifacts by run id, summarizing research decision evidence, and handing off toward Notebook 10.

This document classifies Notebook 09 source and runtime surfaces. It does not prove runtime restore success, strategy comparison success, plot correctness, artifact correctness, benchmark validity, performance significance, archive checkpoint refresh success, or Notebook 10 behavior.

Notebook 09 should remain native-first: it compares StratLake strategies through package/CLI surfaces where available, parses native stdout into review rows, and avoids notebook-side strategy framework, backtest, normalization, feature-generation, archive, or authoritative selection logic.

## 2. Classification Summary Table

| Notebook section | Surface type | Runtime behavior | Source-only validation stance | Non-claims |
|---|---|---|---|---|
| 1. Install notebook dependencies and app packages | Dependency/install surface | Installs notebook dependencies and app packages in a live runtime. | Verify setup cell exists; do not execute package installation. | Does not prove package availability in Colab or local runtime. |
| 2. Imports, Colab detection, and Google Drive auth | Import, environment, Drive auth surface | Imports libraries, detects Colab, and mounts Drive when in Colab. | Inspect imports and guards; do not mount Drive. | Does not prove authenticated state or Drive availability. |
| 3. Load Alpaca environment variables | Runtime credential configuration surface | Reads Colab Secrets or prompts for Alpaca variables at runtime. | Check secret-safe handling only. | Does not prove API access or credential availability. |
| 4. Configure workspace, sessions, archive paths, and analysis window | Workspace/session/archive path surface | Builds workspace roots, Drive roots, session ids, archive paths, and Q1 analysis windows. | Verify placeholder guard and expected variable names. | Does not prove runtime path existence. |
| 5. Verify installed native CLI commands | CLI availability surface | Checks command availability with `shutil.which`. | Verify expected command names are present. | Does not prove commands are installed in the user's environment. |
| 6. Initialize or attach Fintech project/session | Fintech project/session init surface | Runs `fintech-init-project` when enabled and discovers session manifests. | Verify command construction exists. | Does not claim initialization success or generated session files. |
| 7. Initialize or attach StratLake session | StratLake project/session init surface | Runs `stratlake-init-session` and prepares native StratLake session paths. | Verify command construction exists. | Does not claim StratLake session initialization success. |
| 8. Restore StratLake archive from Notebook 07/08 | Manual archive restore surface | Previews or runs `stratlake-session-archive-restore-bootstrap` if manually enabled. | Assert `RUN_STRATLAKE_ARCHIVE_RESTORE = False` and preview shape. | Does not prove archive existence or restore success. |
| 9. Verify restored native StratLake inputs | Restored input validation surface | Checks expected restored configs, features, and artifacts. | Verify checks exist. | Does not prove market data, daily bars, configs, or strategy inputs exist. |
| 10. Inspect available native strategies | Native strategy registry inspection surface | Reads `configs/strategies.yml` and derives strategy names. | Verify registry inspection source exists. | Does not prove all expected strategies are available. |
| 11. Run native strategy comparison | Native strategy comparison execution, parser, and dataframe surface | Runs `stratlake-run-strategy` for available strategy names and builds `strategy_comparison`. | Verify gate, command shape, parser fields, and dataframe construction. | Does not prove strategy execution success, correctness, alpha, or performance significance. |
| 12. Plot native strategy comparison | Comparison plot surface | Plots selected comparison metrics and diagnostics when runtime rows exist. | Verify plotting surface exists; committed notebook remains output-free. | Does not prove plot correctness or generated images. |
| 13. Discover native artifacts by run ID | Native artifact discovery surface | Searches artifacts, data, and reports roots for run-id and file-type candidates. | Verify discovery logic exists. | Does not prove artifacts exist or are correct. |
| 14. Research decision summary | Research review and decision-summary surface | Summarizes parsed runtime evidence, rankings, warnings, and caveats when available. | Verify summary source exists. | Does not provide authoritative strategy selection or performance reporting. |
| 15. Optional archive checkpoint after comparison | Manual archive checkpoint refresh surface | Previews or runs `stratlake-session-archive-bootstrap` if manually enabled. | Assert `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False` and command shape. | Does not claim checkpoint refresh success or create archive packs. |
| 16. Final handoff | Handoff summary surface | Displays session, archive, strategy, artifact, and next-notebook context. | Verify final handoff summary exists. | Does not validate Notebook 10 behavior. |

## 3. Dependency / Install Surface

Section 1 is a runtime preparation surface. It installs notebook dependencies and project packages, including `pandas-market-calendars`, `fintech-market-ingestion`, and `stratlake-trade-engine`.

Source validation can verify that the install/setup cell exists and references the expected packages. Source validation should not execute package installation, access package indexes, or mutate the runtime. Source import does not prove package availability in Colab, local Python, or any future notebook runtime.

## 4. Imports, Colab Detection, and Drive Auth Surface

Section 2 imports runtime libraries, detects whether the notebook is running in Colab, and mounts Google Drive when `IN_COLAB` is true.

Colab detection and Drive auth are runtime/environment behavior. Committed source should not include authenticated Drive state, mounted file listings, tokens, credentials, or runtime output. Source validation can inspect import and guard source text, but it should not mount Drive or prompt for user authentication.

## 5. Runtime Environment / Alpaca Configuration Surface

Section 3 configures Alpaca/runtime environment variables through Colab Secrets or hidden prompt fallback. The relevant names are runtime-only values such as `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY`, `ALPACA_DATA_BASE_URL`, and `ALPACA_FEED`.

No keys, credentials, or private values should be committed. Source validation checks only that credential handling is secret-safe and output-free. Source import does not prove API access, account permission, data feed availability, or credential presence.

## 6. Workspace, Session, Archive Path, and Analysis Window Surface

Section 4 defines the notebook workspace, Drive, session, archive, and analysis-window configuration. Notebook 09 source includes or later derives these path/config variables:

| Variable | Classification |
|---|---|
| `DRIVE_FOLDER_NAME` | Source-safe Drive folder placeholder. |
| `DRIVE_ROOT` | Placeholder-derived Drive root for Colab and local fallback. |
| `FINTECH_ROOT` | Active Fintech workspace root under `WORKSPACE_ROOT`. |
| `STRATLAKE_ROOT` | Active StratLake workspace root under `WORKSPACE_ROOT`. |
| `FINTECH_DRIVE_ROOT` | Drive persistence namespace for Fintech runtime files. |
| `STRATLAKE_DRIVE_ROOT` | Drive persistence namespace for StratLake runtime files. |
| `MARKETLAKE_ROOT` | Fintech curated data handoff root, derived after Fintech session attach. |
| `DAILY_BARS_ROOT` | Daily bars root under `MARKETLAKE_ROOT`. |
| `FINTECH_SESSION_NAME` | Fintech session name. |
| `STRATLAKE_SESSION_NAME` | StratLake session name. |
| `STRATLAKE_SESSION_ID_OVERRIDE` | Optional reattach override for prior StratLake session/archive. |
| `STRATLAKE_ARCHIVE_ID` | StratLake archive id derived from active session id. |
| `STRATLAKE_DRIVE_SESSION_ROOT` | Drive session root for StratLake persistence. |
| `STRATLAKE_DRIVE_ARCHIVE_ROOT` | Drive archive root for StratLake archive packs. |
| `STRATLAKE_ARCHIVE_PACK_DIR` | Expected Notebook 07/08 archive pack directory. |
| `ANALYSIS_START` | Q1 analysis start date. |
| `ANALYSIS_END` | Q1 analysis end date. |
| `BACKFILL_START` | Padded daily-bar backfill start date. |
| `BACKFILL_END` | Padded daily-bar backfill end date. |
| `BACKFILL_SYMBOLS` | Symbol list used by the broader workflow. |
| `strategies_config_path` | Native strategy config path, `STRATLAKE_ROOT / "configs" / "strategies.yml"`. |

Drive folder configuration must use the placeholder pattern:

```python
DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"
DRIVE_ROOT = Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME if IN_COLAB else WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME
```

The placeholder guard prevents accidental live Drive/session/archive path use from committed source. Real Drive folder names and private local paths must not be committed. Source import does not prove that any configured runtime path exists.

## 7. CLI Availability Check Surface

Section 5 checks availability for these native command names:

- `fintech-init-project`
- `fintech-backfill-daily`
- `fintech-backup-data`
- `stratlake-init-session`
- `stratlake-run-strategy`
- `stratlake-session-archive-bootstrap`
- `stratlake-session-archive-restore-bootstrap`

This is a runtime availability surface. Source tests can verify that command names are present in the notebook source. Runtime checks verify actual command availability in the user's environment. Source import does not prove command availability, CLI flag compatibility, package installation, or end-to-end command behavior.

## 8. Fintech Project/Session Init Surface

Section 6 constructs and optionally runs `fintech-init-project`.

The command is intended to initialize or attach a Fintech project/session at runtime using `FINTECH_ROOT`, `FINTECH_SESSION_NAME`, `--with-session`, and `--colab-profile`. Source validation can verify command construction exists and that downstream session discovery references the expected manifest shape. Source import does not claim initialization success. Generated project directories, session manifests, backups, curated data, or logs must not be committed.

## 9. StratLake Project/Session Init Surface

Section 7 constructs and optionally runs `stratlake-init-session`.

The command is intended to initialize or attach a StratLake session at runtime using `STRATLAKE_ROOT`, `STRATLAKE_SESSION_NAME`, `MARKETLAKE_ROOT`, `DRIVE_ROOT`, `--enable-drive-persistence`, and `--notebook-configs`. Source validation can verify command construction exists. Source import does not claim session initialization success, config generation success, Drive persistence success, or runtime package compatibility. Generated session files must not be committed.

## 10. Archive Restore Surface

Section 8 constructs the `stratlake-session-archive-restore-bootstrap` command and guards restore execution with `RUN_STRATLAKE_ARCHIVE_RESTORE`.

Expected committed-source state:

```python
RUN_STRATLAKE_ARCHIVE_RESTORE = False
```

Restore is manual/off-by-default in committed source. Command construction or preview may remain so a live user can inspect the restore shape before enabling it. Restore depends on runtime archive availability at `STRATLAKE_ARCHIVE_PACK_DIR` and on the active `STRATLAKE_ROOT`. Source import does not prove archive existence, archive integrity, restore compatibility, overwrite safety, or restore success. Restored files must not be committed.

## 11. Restored Native Input Validation Surface

Section 9 checks restored native StratLake inputs, including:

- `STRATLAKE_ROOT / "configs" / "universe.yml"`
- `STRATLAKE_ROOT / "configs" / "paths.yml"`
- `STRATLAKE_ROOT / "configs" / "strategies.yml"`
- `STRATLAKE_ROOT / "data" / "curated" / "features_daily"`
- `STRATLAKE_ROOT / "artifacts"`

These checks are runtime/session dependent. Source validation can verify that checks exist and are output-free in committed source. Source import does not prove market data, daily bars, feature files, configs, strategy input files, or artifacts exist. Input validation results are runtime evidence only when smoke-tested and documented.

## 12. Native Strategy Registry Inspection Surface

Section 10 inspects available native StratLake strategies by reading `configs/strategies.yml` through `strategies_config_path`.

Strategy availability depends on installed package behavior, generated/restored configs, and runtime session state. Source import does not prove all expected strategies are available. Notebook 09 should not implement its own strategy registry; it should inspect the native config surface and pass resulting names into native CLI/package surfaces.

## 13. Native Strategy Comparison Execution Surface

Section 11 constructs and optionally runs `stratlake-run-strategy` for each discovered native strategy name.

Expected committed-source gate:

```python
RUN_NATIVE_STRATEGY_COMPARISON = True
```

Native strategy comparison is intended live runtime behavior. Source validation can verify the command shape, including `stratlake-run-strategy`, `--strategies-config`, `configs/strategies.yml`, `--strategy`, `--start`, and `--end`, plus the gate presence. Source import does not claim strategy execution success, strategy correctness, benchmark correctness, alpha, performance significance, or all-strategy coverage. Strategy comparison should remain native CLI/package driven, not notebook-side strategy logic.

## 14. Native Stdout Parser and Review Row Surface

Section 11 parses native CLI stdout into review rows. The parser fields include:

- `cumulative_return`
- `sharpe_ratio`
- `long_pct`
- `short_pct`
- `flat_pct`
- `trades`
- `turnover`
- `avg_holding_bars`
- `qa_status`
- `qa_rows`
- `qa_symbols`
- `benchmark_return`
- `excess_return`
- `correlation`

Parsed rows are review evidence. Parser presence does not prove metric correctness, upstream output stability, benchmark validity, or strategy correctness. Parsed rows should not be treated as authoritative strategy-selection evidence from source import alone. Static tests may verify expected parser fields are present.

## 15. Strategy Comparison Dataframe Surface

Section 11 builds `strategy_comparison = pd.DataFrame(strategy_rows)`, sorts by available review metrics such as `completed`, `excess_return`, and `sharpe_ratio`, and displays the dataframe in live runtime.

The dataframe is a review surface. The committed notebook should not contain executed dataframe outputs. Source tests can verify dataframe construction exists. Dataframe contents are runtime evidence only when smoke-tested and documented; they are not a committed performance report.

## 16. Comparison Plot Surface

Section 12 plots native strategy comparison metrics when `strategy_comparison` has runtime rows. It also displays diagnostic columns such as strategy, run id, QA status, rows, symbols, trades, turnover, holding bars, and position percentages.

Plots are runtime/review surfaces. Generated plots/images must not be committed. Source import does not prove plot correctness, visual suitability, or rendered output. A later smoke issue may document whether plots rendered from live runtime evidence.

## 17. Native Artifact Discovery by Run ID Surface

Section 13 discovers native artifacts by scanning `STRATLAKE_ROOT / "artifacts"`, `STRATLAKE_ROOT / "data"`, and `STRATLAKE_ROOT / "reports"` for files matching runtime run ids or review file suffixes such as `.json`, `.csv`, `.parquet`, `.md`, and `.html`.

Artifact discovery is runtime/session dependent. Source validation can verify discovery logic exists. Source import does not prove artifacts exist, match run ids, are complete, or are correct. Artifact inventories are review surfaces, not committed performance reports. Discovered artifacts should not be committed unless explicitly intended and source-safe, which is not part of M12.2.

## 18. Research Decision Summary Surface

Section 14 summarizes runtime comparison evidence when available. It may report strategies attempted, completed strategies, best rows by return or Sharpe, benchmark/excess-return context, stderr warnings, and caveats.

The research decision summary is a review/handoff surface. It may summarize parsed runtime evidence if available, but it must not be treated as authoritative strategy selection from source import alone. Source import does not prove benchmark rows, alpha, plot correctness, artifact correctness, or performance validity.

## 19. Optional Archive Checkpoint Refresh Surface

Section 15 constructs the `stratlake-session-archive-bootstrap` command and guards checkpoint refresh execution with `RUN_STRATLAKE_ARCHIVE_CHECKPOINT`.

Expected committed-source state:

```python
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False
```

Checkpoint refresh is optional/manual/off-by-default. Source import does not claim checkpoint success, copy success, validation success, inspection success, or archive integrity. Archive packs must not be committed. A later smoke issue can document whether checkpoint refresh was skipped or explicitly run.

## 20. Final Handoff Surface

Section 16 builds `final_handoff` with notebook name, Fintech and StratLake session ids, archive id, analysis window, strategies attempted/completed, artifact rows, archive pack path, and the next notebook label.

The final handoff points toward Notebook 10. Handoff is review/documentation context only. Source import does not validate Notebook 10 behavior, Notebook 10 inputs, or any downstream workflow. Notebook 10 behavior should not be claimed in M12.2.

## 21. Source-Only Validation Guidance

Later source-only tests should verify, without executing Notebook 09:

- Notebook exists at `notebooks/09_stratlake_strategy_comparison_and_research_review.ipynb`.
- Code-cell outputs are cleared.
- Code-cell execution counts are null.
- Colab/runtime metadata is absent.
- Hardcoded tutorial Drive path is absent.
- `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` placeholder guard is present.
- `RUN_STRATLAKE_ARCHIVE_RESTORE = False` is present.
- `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False` is present.
- `RUN_NATIVE_STRATEGY_COMPARISON = True` is present.
- Expected CLI commands are present.
- Restore command preview/guard is present.
- Strategy comparison command shape is present.
- Parser metrics are present.
- Dataframe review surface is present.
- Plotting surface is present.
- Artifact discovery by run id is present.
- Research decision summary is present.
- Optional archive checkpoint preview is present.
- Final handoff summary is present.

These tests should not run Colab smoke, mount Drive, prompt for credentials, restore archives, run strategy comparison, refresh checkpoints, generate plots, create logs, create manifests, restore files, create archive packs, or create Drive folders.

## 22. Required Non-Authoritative Review Stance

M12.2 is documentation/classification only. The required stance is:

- Do not claim archive restore success.
- Do not claim strategy comparison success.
- Do not claim all-strategy correctness.
- Do not claim authoritative performance results.
- Do not claim benchmark rows prove alpha.
- Do not claim plot correctness.
- Do not claim artifact discovery correctness.
- Do not claim archive checkpoint refresh success.
- Do not claim Notebook 10 behavior is validated.
- Do not claim source import proves runtime correctness.

Notebook 09 remains a native StratLake comparison and research review notebook. It is not a notebook-side strategy framework, notebook-side backtest engine, authoritative strategy-selection notebook, committed performance report, or proof of all-strategy correctness.
