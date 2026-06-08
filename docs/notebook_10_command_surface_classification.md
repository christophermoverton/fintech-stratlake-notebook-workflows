# Notebook 10 Command Surface Classification

## Purpose

Notebook 10 (`notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb`) is a source-safe StratLake walk-forward robustness and promotion-review notebook. It follows Notebook 08 strategy backtest artifact review and Notebook 09 strategy comparison/research review. Its workflow theme is "from strategy comparison to confidence."

This document classifies Notebook 10 command, restore, strategy, robustness, promotion, artifact-review, archive, and handoff surfaces. The classifications describe intended source and runtime behavior. They do not prove live restore success, Google Drive availability, credential availability, native strategy success, robustness evidence, promotion readiness, artifact correctness, archive checkpoint success, or financial significance.

Notebook 10 remains an importation and composition milestone. It composes existing StratLake functionality and review artifacts; it does not introduce a new core StratLake engine command.

## Notebook Source And Target Path

| Property | Value |
|---|---|
| Issue | #103 - M13.2 - Classify Notebook 10 Restore, Strategy, Robustness, and Promotion Surfaces |
| Depends on | #102 - M13.1 - Stage and Clean Notebook 10 Walk-Forward Robustness Promotion Review |
| Target notebook | `notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb` |
| Staged source shape | 41 cells: 21 markdown, 20 code |
| Source posture | Cleaned, output-free, execution counts reset, Colab/runtime metadata stripped or minimized |
| Runtime posture | Live/manual Colab or local notebook execution only; not CI execution |

## Classification Legend

| Category | Meaning |
|---|---|
| `source_only` | Source text, notebook JSON, metadata, references, and guards can be inspected without runtime execution. |
| `live_manual` | Requires deliberate live notebook execution in Colab or another prepared runtime. |
| `guarded_runtime` | Runtime action is protected by a boolean gate, placeholder guard, mode switch, or manual enablement. |
| `preview_only` | Command shape is printed or source-reviewable without being executed by default. |
| `runtime_validation` | Validates runtime/session state such as restored paths, config files, feature columns, or CLI availability. |
| `runtime_review` | Reviews runtime outputs such as result rows, diagnostics, robustness summaries, plots, or audit summaries. |
| `artifact_review` | Writes, discovers, or inventories generated runtime artifacts. |
| `promotion_review` | Applies conservative notebook-level promotion gates and decision labels. |
| `handoff` | Produces final runtime context for downstream notebook or milestone work. |
| `out_of_ci_scope` | Must not be required by repository validation or CI because it depends on live runtime state, credentials, Drive, restored archives, native execution, or generated artifacts. |

## Section-By-Section Classification Table

| Section | Notebook step | Primary surface | Classification | Runtime dependency | Repository validation stance | Notes |
|---:|---|---|---|---|---|---|
| 1 | Install notebook dependencies and app packages | Package installation | `live_manual`, `out_of_ci_scope` | Network/package index and live Python runtime | Source checks may verify references only; do not execute installs. | Colab/runtime setup surface. |
| 2 | Imports, Colab detection, and Google Drive auth | Import and Drive auth | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Colab environment and user Drive auth | Inspect source guards only; do not mount Drive. | Committed source must not include authenticated state. |
| 3 | Load Alpaca environment variables | Credential configuration | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Colab Secrets or hidden prompt values | Verify secret-safe source only. | No credentials are committed or printed. |
| 4 | Configure workspace, sessions, archive paths, and notebook mode | Workspace/session/mode config | `source_only`, `guarded_runtime` | User-configured Drive folder for live execution | Verify placeholder guard and conservative defaults. | `NOTEBOOK10_MODE = "smoke"` is workflow validation only. |
| 5 | Verify installed native CLI commands and import surfaces | CLI/import availability check | `live_manual`, `runtime_validation`, `out_of_ci_scope` | Installed packages and runtime PATH/import surface | Verify expected command and import references only. | Does not prove commands are installed. |
| 6 | Initialize or attach Fintech project/session | Fintech session initialization | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Runtime package, workspace, and session manifest state | Verify `fintech-init-project` command construction only. | Generated project/session files stay out of Git. |
| 7 | Initialize or attach StratLake session | StratLake session initialization | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Runtime package, MarketLake root, Drive root, configs | Verify `stratlake-init-session` command construction only. | Composes native session init surface. |
| 8 | Restore StratLake archive from Notebook 08/09 | Archive restore | `live_manual`, `guarded_runtime`, `preview_only`, `out_of_ci_scope` | Existing Drive archive pack and live target root | Assert `RUN_STRATLAKE_ARCHIVE_RESTORE = False` and command shape. | Restore is manual/off-by-default in committed source. |
| 9 | Verify restored inputs and prior artifacts | Restored input validation | `runtime_validation`, `artifact_review`, `out_of_ci_scope` | Restored configs, artifacts, MarketLake/StratLake paths | Verify required-path references only. | Does not prove archive restore succeeded. |
| 10 | Discover feature columns for strategy preflight | Feature-column inspection | `runtime_validation`, `out_of_ci_scope` | Restored feature files/dataframes | Verify source structure only. | Supports strategy feature-contract checks. |
| 11 | Discover and preflight candidate native strategies | Strategy preflight | `runtime_validation`, `source_only` | Restored `configs/strategies.yml` and feature columns | Verify preflight logic and known contract finding references. | Skipped strategies are contract findings, not runtime failures. |
| 12 | Run walk-forward strategy smoke/expanded evaluation | Native strategy execution | `live_manual`, `guarded_runtime`, `runtime_review`, `out_of_ci_scope` | Native CLI, restored inputs, selected strategies, runtime mode | Verify `stratlake-run-strategy` shape and guards; do not execute. | Smoke mode validates workflow wiring only. |
| 13 | Add diagnostic flags for financial interpretation | Diagnostic review | `runtime_review` | Walk-forward result rows | Verify diagnostic flag source only. | Flags benchmark-avoidance outperformance and flat/inactive behavior. |
| 14 | Build robustness summary from split-level results | Robustness summary | `runtime_review` | Walk-forward split-level result rows | Verify summary fields and source shape only. | Depends on runtime strategy outputs. |
| 15 | Plot walk-forward robustness diagnostics | Visualization | `runtime_review`, `out_of_ci_scope` | Runtime dataframe rows and plotting backend | Verify plotting source exists; no plots committed. | Visual diagnostics are not source validation. |
| 16 | Apply improved notebook-level promotion gates | Promotion gate review | `promotion_review`, `runtime_review` | Robustness summary and diagnostics | Verify strict gates and smoke-mode posture. | No promotion-grade claim from smoke mode. |
| 17 | Smoke audit interpretation and import-readiness notes | Smoke/audit interpretation | `runtime_review`, `source_only` | Runtime result/audit rows when executed | Verify non-authoritative smoke language and taxonomy definitions. | Workflow-validation evidence only. |
| 18 | Write Notebook 10 review outputs and artifact inventory | Artifact writing and inventory | `artifact_review`, `guarded_runtime`, `out_of_ci_scope` | Runtime result frames and StratLake artifact roots | Verify output directory and expected filenames only. | Generated artifacts are not committed in M13.2. |
| 19 | Optional archive checkpoint after Notebook 10 review | Archive checkpoint refresh | `live_manual`, `guarded_runtime`, `preview_only`, `out_of_ci_scope` | Runtime artifacts/features/configs and Drive archive root | Assert `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False` and command shape. | Manual/off-by-default archive refresh. |
| 20 | Final handoff | Handoff summary | `handoff`, `runtime_review`, `source_only` | Runtime IDs, result rows, artifact inventory | Verify structure only. | Runtime values are generated only during live execution. |

## Composed StratLake Surfaces

Notebook 10 composes existing StratLake surfaces rather than adding engine functionality. Relevant source and documentation surfaces include:

- `src/research/walk_forward.py`
- `src/portfolio/walk_forward.py`
- `src/research/splits.py`
- `src/cli/run_strategy.py`
- `src/cli/compare_strategies.py`
- `src/execution/strategy.py`
- `src/execution/comparison.py`
- `src/research/compare.py`
- `src/config/robustness.py`
- `src/research/extended_robustness.py`
- `src/research/robustness/runner.py`
- `src/research/robustness/walk_forward_efficiency.py`
- `src/research/promotion.py`
- `configs/robustness.yml`
- `configs/alpha_promotion_gates.yml`
- `docs/walk_forward_strategy_runner.md`
- `docs/strategy_comparison_cli.md`
- `docs/examples/milestone_13_review_promotion_workflow.md`

Repository documentation should treat these as upstream/native surfaces that Notebook 10 reviews or composes. M13.2 does not add a new `stratlake-*` core command.

## Command And Runtime Surfaces

| Surface | Notebook use | Classification | Source-only validation boundary |
|---|---|---|---|
| Package installation | Installs notebook dependencies and app packages for live runtime. | `live_manual`, `out_of_ci_scope` | Verify package references only; no install in CI. |
| Colab/Drive auth | Detects Colab and mounts Drive when applicable. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Do not mount Drive during repository checks. |
| Alpaca secrets | Reads Colab Secrets or prompts for credentials. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Confirm values are not committed or printed. |
| `fintech-init-project` | Initializes or attaches Fintech project/session. | `live_manual`, `guarded_runtime` | Verify command construction only. |
| `stratlake-init-session` | Initializes or attaches StratLake session and notebook configs. | `live_manual`, `guarded_runtime` | Verify command construction only. |
| `stratlake-session-archive-restore-bootstrap` | Restores Notebook 08/09 archive into active StratLake root. | `live_manual`, `guarded_runtime`, `preview_only` | Confirm false default and command preview; do not restore. |
| Native CLI checks | Checks command availability and import surfaces. | `runtime_validation` | Verify expected references; do not require PATH availability in CI. |
| Strategy discovery | Reads/restores config and candidate strategy names. | `runtime_validation` | Verify discovery/preflight source only. |
| Feature preflight | Classifies missing feature requirements before native execution. | `runtime_validation` | Verify logic and known contract findings only. |
| `stratlake-run-strategy` | Runs selected strategies across smoke or expanded windows. | `live_manual`, `guarded_runtime`, `runtime_review` | Verify command shape and guards; do not execute. |
| Robustness review | Builds split-level and strategy-level summaries. | `runtime_review` | Verify source fields only. |
| Plotting | Plots walk-forward diagnostics. | `runtime_review`, `out_of_ci_scope` | No plots or outputs committed. |
| Promotion gates | Applies conservative notebook-level gates. | `promotion_review` | Verify strict gate surface and smoke-mode non-claim. |
| Artifact writing | Writes review CSV/JSON files and inventory. | `artifact_review`, `out_of_ci_scope` | Verify filenames/path only; generated files stay out of Git. |
| Archive checkpoint | Optionally refreshes Notebook 10 archive checkpoint. | `live_manual`, `guarded_runtime`, `preview_only` | Confirm false default; do not archive. |
| Final handoff | Displays session, archive, result, artifact, and next-step context. | `handoff`, `runtime_review` | Verify structure only; no runtime values claimed. |

## Restore And Archive Posture

Archive restore is a live/manual, guarded runtime surface. The staged notebook should keep:

```python
RUN_STRATLAKE_ARCHIVE_RESTORE = False
```

The restore command surface is source-reviewable, but execution is out of CI scope. Restore requires a configured Drive folder, a real Notebook 08/09 archive pack, and a live target workspace. M13.2 does not prove archive existence, checksum integrity, restore compatibility, overwrite safety, or restored data availability.

Archive checkpoint refresh is also live/manual and guarded:

```python
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False
```

Checkpoint refresh may copy features, artifacts, and configs into Drive when manually enabled. It must remain off by default in committed source. M13.2 does not create or validate archive packs.

## Strategy And Walk-Forward Execution Posture

Native strategy execution and walk-forward smoke/expanded evaluation are live/manual runtime surfaces. Source validation should verify command construction and guards, not run commands.

The conservative staged defaults are:

```python
NOTEBOOK10_MODE = "smoke"
RUN_ONLY_PREFLIGHT_RUNNABLE_STRATEGIES = True
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False
```

Smoke mode is workflow-validation mode. It validates workflow wiring, archive restore composition, strategy preflight, native execution plumbing, artifact parsing, diagnostics, and promotion-gate behavior. Smoke mode is not promotion-grade financial evidence. Expanded mode validation is deferred and out of scope for M13.2.

## Feature-Contract Preflight Posture

Feature-column discovery and strategy preflight are runtime validation surfaces. They depend on restored Notebook 08/09 feature data and native strategy configuration.

Known v4 preflight findings should be documented as expected restored-data feature-contract findings, not runtime failures:

| Strategy | Missing feature requirements | Interpretation |
|---|---|---|
| `breakout` | `high`, `low` | Restored feature data did not satisfy the strategy contract. |
| `residual_momentum` | `market_return` | Restored feature data did not satisfy the strategy contract. |
| `weighted_cross_section_ensemble` | `market_return` | Restored feature data did not satisfy the strategy contract. |

The v4 smoke context discovered 14 candidate strategies and selected 11 runnable strategies. That selection is live smoke evidence from the external artifact, not a source-only repository claim.

## Warning Taxonomy

Notebook 10 warning categories are diagnostic review surfaces:

- `benchmark_degenerate_warning`
- `strategy_degenerate_warning`
- `flat_series_correlation_warning`
- `signal_pct_consistency`
- `qa_warn`
- `numeric_runtime_warning`
- `missing_required_columns`
- `runtime_failed`
- `exception_or_error_text`
- `stderr_other`

Interpretation rules:

- Benchmark-degenerate and strategy-degenerate warnings are diagnostic warnings, not necessarily runtime failures.
- Missing feature requirements are feature-contract findings and should be separated from execution failures.
- Generic `numeric_runtime_warning` should be used only when a more specific warning category is not available.
- Flat/inactive strategies that show positive excess return only because the benchmark declined should be treated as benchmark-avoidance, not alpha.

The staged notebook includes the M13.1 warning-classifier refinement for:

- `buyandholdstrategy`
- `no trades were generated`

## Promotion Review Posture

Promotion review is a conservative runtime review surface. The gates should preserve strict smoke-mode behavior and should not promote strategies from one smoke window.

Known v4 smoke interpretation:

- Window: 2026-01-02 through 2026-01-31.
- Feature shape: 100 feature rows and 5 symbols, plausible for roughly 20 trading sessions times 5 symbols.
- Promotion result: `promoted_strategies: []`.
- Watchlist result: `watchlist_strategies: []`.
- Decision counts: `{'needs_review': 11}`.

This result is expected because only one smoke window was run, all evaluated strategies had QA WARN, `qa_clean_windows = 0`, `warning_windows = 1`, `positive_cumulative_rate = 0.0`, several strategies were flat/inactive, and several positive excess returns came from benchmark avoidance.

M13.2 does not claim promotion-grade evidence, alpha evidence, statistical significance, or production readiness.

## Artifact And Handoff Posture

Notebook 10 writes review artifacts only during live runtime execution. The normalized review directory is:

```text
artifacts/notebook_10_walk_forward_promotion_review/
```

Expected source-visible artifact filenames are:

- `walk_forward_results.csv`
- `walk_forward_results.json`
- `robustness_summary.csv`
- `robustness_summary.json`
- `promotion_review.csv`
- `promotion_review.json`
- `preflight_summary.csv`
- `preflight_summary.json`
- `artifact_inventory.csv`
- `artifact_inventory.json`
- `summary.json`
- `smoke_audit_summary.json`

These filenames are source-reviewable references. M13.2 must not commit generated CSV/JSON files, plots, restored archives, restored parquet files, logs, screenshots, or runtime output.

The final handoff is a runtime summary surface. Source validation may verify structure and labels only; runtime values are generated during live execution.

## Source-Only Validation Boundary

Repository validation for M13.2 may inspect:

- Notebook JSON parseability.
- Output-free and execution-count-free source state inherited from #102.
- Staged notebook path references.
- 20-section workflow representation.
- Guarded defaults: `RUN_STRATLAKE_ARCHIVE_RESTORE = False`, `RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False`, and `NOTEBOOK10_MODE = "smoke"`.
- Drive placeholder guard: `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"`.
- Expected native command references and review artifact filenames.
- Warning taxonomy terms, including `buyandholdstrategy` and `no trades were generated`.
- Documentation source safety via `git diff --check`.

Repository validation must not execute notebook cells, run CLI commands, install packages, mount Drive, prompt for credentials, restore archives, run strategies, generate plots, write runtime artifacts, refresh checkpoints, or perform expanded-mode validation.

## Non-Claims

M13.2 does not claim:

- Notebook 10 was executed from committed source.
- Google Drive mounted successfully.
- Alpaca credentials were present or valid.
- Notebook 08/09 archive restore succeeded.
- Native StratLake CLI commands were installed or executed.
- Walk-forward results are financially significant.
- Smoke-mode results are promotion-grade evidence.
- Any strategy demonstrated alpha.
- Any strategy should be promoted or watchlisted.
- Runtime artifacts, plots, archive packs, restored data, or logs were generated or committed.
- A new core StratLake engine command was introduced.

Completion stance for this classification issue: `notebook_10_command_runtime_surfaces_classified`.
