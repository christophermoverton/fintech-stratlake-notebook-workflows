# Notebook 06 Staging and Classification

## Summary

This document records the Milestone 9 staging and classification decisions for
Notebook 06 before and during cleanup, command classification, validation, and audit
work.

Notebook 06 is a conservative validation, archive-preview, restore-readiness, and
handoff checkpoint after Notebook 05. It is not a strategy notebook, a backtest
notebook, a feature-generation framework, an archive implementation, or a restore
implementation. It validates the Fintech-to-StratLake Q1 feature handoff and prepares
Notebook 07 strategy/backtest work.

Repository validation remains source-only and sanitized. Live runtime state belongs in
Colab and Google Drive, not in Git.

## Candidate Notebook Identity

| Field | Value |
|---|---|
| Repository path | `notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb` |
| Source notebook | Cleaned Colab workflow source supplied outside the repository |
| Notebook title | Notebook 06 — StratLake Feature Validation, Archive, and Handoff |
| Workflow classification | Validation, archive-preview, restore-readiness, and handoff checkpoint |
| Primary upstream app | `fintech-market-ingestion` |
| Secondary upstream app | `stratlake-trade-engine` |
| Relationship to Notebook 05 | Validates the Q1 feature handoff produced by Notebook 05; does not regenerate features |
| Relationship to Notebook 07 | Prepares the validated feature session for Notebook 07 strategy/backtest work |
| Staging category | `source_safe_after_cleanup` after Issue #69 |
| Import status | `imported` |
| Manual Colab smoke status | `colab_smoke_passed_with_notes` |

## Notebook Role

Notebook 06 should guide a Colab user through:

- Installing notebook dependencies (`pandas-market-calendars`, `fintech-market-ingestion`,
  `stratlake-trade-engine`).
- Verifying required CLI availability with `shutil.which(...)`.
- Mounting Google Drive manually.
- Defining Fintech, StratLake, MarketLake, and Drive roots.
- Initializing or reconnecting Fintech and StratLake sessions under `/content`.
- Verifying StratLake notebook config files (`universe.yml`, `paths.yml`).
- Creating session-scoped Drive archive folders.
- Configuring Alpaca API credentials from Colab Secrets or a hidden prompt.
- Preparing runtime ticker/config files and the Q1 validation window.
- Optionally restoring Fintech curated data from a Drive archive before API ingestion.
- Validating Fintech daily-bars handoff into `MARKETLAKE_ROOT`.
- Optionally archiving the Fintech curated Q1 input.
- Optionally running `stratlake-build-features` if feature outputs are missing.
- Validating StratLake feature outputs.
- Validating session portability assumptions.
- Running `stratlake-session-export --dry-run`.
- Optionally archiving the StratLake feature session.
- Printing StratLake restore-readiness command preview.
- Printing a final handoff summary for Notebook 07.

Notebook 06 should not reimplement Fintech ingestion or StratLake feature generation
logic in notebook-side Python beyond what is needed to orchestrate and validate existing
upstream CLI outputs.

## Source Review Facts

Milestone 9 review confirmed:

- Outputs were cleared.
- Code-cell execution counts were reset to `null`.
- Top-level Colab/runtime metadata was stripped.
- Cell runtime metadata was stripped or minimized.
- No generated data, archive packs, restored files, session manifests, Drive artifacts,
  logs, screenshots, credentials, private paths, or feature outputs were committed.
- `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains the Drive root placeholder.
- The Q1 window remains `2025-01-01` through `2025-04-01`.
- The compact ticker universe remains `["AAPL", "MSFT", "NVDA"]`.
- `FINTECH_SESSION_ID`, `STRATLAKE_SESSION_ID`, and `MARKETLAKE_ROOT` remain
  source-visible.
- Registry-current Fintech backup pack/restore preview syntax is in place (corrected
  by M9.3).
- StratLake archive/bootstrap preview commands remain source-visible as
  `optional_unverified_preview_commands`.

## Staging Status

| Stage | Status |
|---|---|
| Staged | Complete — Issue #69 |
| Cleaned | Complete — Issue #69 |
| Source hygiene verified | Complete — Issues #69, #71 |
| Command surfaces classified | Complete — Issue #70 |
| CLI contract validated | Complete — Issue #71 |
| CLI registry validated | Complete — Issue #71 |
| Source-only readiness validated | Complete — Issue #72 |
| Sanitized execution validated | Complete — Issue #72 |
| Audit recorded | Complete — Issue #73 |
| Manual Colab smoke | Complete with notes — Issue #74 |
| Milestone merge readiness | Pending — M9.7 |

## Repository Source Status

The committed Notebook 06 source is:

- Output-free.
- Null execution count.
- Free of top-level Colab/runtime metadata.
- Free of committed generated data.
- Free of committed session artifacts.
- Free of committed archive packs or restored contents.
- Free of credentials or private paths.
- Source-only repository validated.
- Static CLI contract validated.
- Static CLI registry validated.
- Source-only readiness validated.
- Sanitized execution validated.

## Runtime and Manual Status

All live Colab runtime surfaces remain manual. The following are manual Colab-only and
must never be executed by repository validation or committed to Git:

- Package install.
- Google Drive mount.
- Colab Secrets / `getpass` credential access.
- Alpaca API key setup.
- Fintech session initialization (`fintech-init-project`).
- StratLake session initialization (`stratlake-init-session`).
- Runtime ticker/config file writes.
- Google Drive session/archive folder creation.
- `fintech-backup-data restore` (preview only; not executed from source).
- Fintech daily-bars backfill (`fintech-backfill-daily`).
- StratLake feature build (`stratlake-build-features`).
- Generated data inspection (`pd.read_parquet(...)`, `.rglob("*.parquet")`).
- `display(...)` calls.
- `subprocess.run(...)` archive/restore execution.
- `stratlake-session-export --dry-run` (live dry-run; depends on runtime workspace).
- `stratlake-session-archive-bootstrap` (guarded preview; not executed).
- `stratlake-session-archive-restore-bootstrap` (printed preview; not executed).
- `fintech-backup-data pack` (guarded preview; not executed).
- Final JSON handoff summary (depends on runtime-derived values).

## Validation Coverage Matrix

| Validation layer | Status | Config/file |
|---|---|---|
| Secret scan | Pass | `scripts/scan_for_secret_patterns.py` |
| No-output check | Pass | `scripts/check_notebooks_no_outputs.py` |
| Repo cleanliness | Pass | `scripts/validate_repo_cleanliness.py` |
| Source-only readiness | Pass | `config/notebook_test.toml` |
| Sanitized execution | Pass | `config/notebook_execution_test.toml` |
| CLI contract | Pass | `config/notebook_cli_contracts.toml` |
| CLI registry | Pass | `config/notebook_cli_registry.toml` |
| pytest (notebook execution) | Pass — 47/47 | `tests/test_notebook_execution.py` |
| pytest (CLI contracts) | Pass | `tests/test_notebook_cli_contracts.py` |
| pytest (CLI registry) | Pass | `tests/test_notebook_cli_registry.py` |
| Manual Colab smoke | Pass with notes — Issue #74 | Issue #74 |

## Command Coverage Matrix

| Command | Coverage type | Classification |
|---|---|---|
| `fintech-init-project` | CLI contract, CLI registry, sanitized skip | `live_manual_runtime` |
| `stratlake-init-session` | CLI contract, CLI registry, sanitized skip | `live_manual_runtime` |
| `fintech-backfill-daily` | CLI contract, CLI registry, sanitized skip | `live_manual_runtime_conditional` |
| `fintech-backup-data restore` | CLI contract, CLI registry, sanitized skip | `preview_manual_guidance` |
| `fintech-backup-data pack` | CLI contract, CLI registry, sanitized skip | `preview_manual_guidance` |
| `stratlake-build-features` | CLI contract, CLI registry, sanitized skip | `live_manual_runtime_conditional` |
| `stratlake-session-export --dry-run` | CLI contract, CLI registry, sanitized skip | `live_manual_runtime_dry_run` |
| `stratlake-session-archive-bootstrap` | Source-visible; deferred from confirmed registry coverage | `contract_mismatch_or_unverified` |
| `stratlake-session-archive-restore-bootstrap` | Source-visible; deferred from confirmed registry coverage | `contract_mismatch_or_unverified` |

## Sanitized Execution Treatment

Sanitized execution builds a temporary notebook copy in which runtime-heavy cells are
replaced with `# Skipped by pytest sanitized notebook execution harness.` no-ops. The
source notebook is never modified.

Cells skipped during sanitized execution include all cells containing:

- `!pip install` / `%pip` (package install)
- `drive.mount(` / `google.colab` (Colab/Drive)
- `userdata.get(` / `getpass.getpass(` (credentials)
- `FINTECH_ROOT` / `STRATLAKE_ROOT` / `MARKETLAKE_ROOT` (runtime path namespaces)
- `FINTECH_DRIVE` / `STRATLAKE_DRIVE` (Drive path construction)
- `DAILY_BARS_ROOT` (generated daily-bars path)
- `!fintech-init-project` / `!stratlake-init-session` (session initialization)
- `!fintech-backfill-daily` / `!stratlake-build-features` / `!stratlake-session-export` (live runtime commands)
- `!fintech-backup-data` / `subprocess.run(` (archive/restore execution)
- `.mkdir(` / `.write_text(` / `os.chdir(` (filesystem mutation)
- `rglob("*.parquet")` / `pd.read_parquet(` (generated data inspection)
- `display(` (Colab display calls)
- `FINTECH_SESSION_MANIFEST` / `STRATLAKE_SESSION_FILE` (session manifest reads)
- `FINTECH_ARCHIVE_ID` / `STRATLAKE_ARCHIVE_ID` (archive ID construction)
- `RESTORE_FINTECH` / `RESTORE_STRATLAKE` (restore path construction)
- `required_workflow_commands` / `missing_required_commands` (CLI availability check that raises RuntimeError when CLIs are absent)
- `feature_candidates` (generated feature output enumeration)

Sanitized execution is conservative and validates source structure, source invariants,
and skip behavior. **It does not prove live Colab runtime behavior.** It is not a
substitute for manual Colab smoke testing.

## Colab Smoke Status

`colab_smoke_passed_with_notes` — Issue #74.

An executed Colab Notebook 06 artifact was reviewed outside the repository. All 21
code cells executed without errors or tracebacks.

**Confirmed in smoke run:**

- Package install and CLI availability (all required commands found; both optional
  archive/bootstrap commands also found but not executed).
- Google Drive mounted; session/archive folders created.
- Alpaca credentials configured without printing secret values.
- `fintech-init-project` ran; `FINTECH_SESSION_ID` extracted.
- `stratlake-init-session` ran; `STRATLAKE_SESSION_ID` extracted; notebook configs generated.
- `universe.yml` and `paths.yml` previewed.
- Q1 daily-bars backfill ran; 180 rows across 3 symbols.
- Fintech daily-bars handoff validated.
- StratLake feature build ran; 3 feature parquet files found; sample shape (60, 15).
- All portability/session checks passed.
- `stratlake-session-export --dry-run` completed.
- Final JSON handoff summary printed.

**Notes (why `passed_with_notes`):**

- Non-blocking pip resolver warning (`toolz 1.1.0` vs `ibis-framework` expectation).
- `CREATE_FINTECH_ARCHIVE = False` — Fintech archive creation not executed.
- `CREATE_STRATLAKE_ARCHIVE = False` — StratLake archive creation not executed.
- Restore previews showed archive packs did not exist (expected; archive creation was preview-only).
- `stratlake-session-archive-bootstrap` and `stratlake-session-archive-restore-bootstrap`
  were available but not executed; upstream contracts remain unverified beyond availability.
- Executed artifact must not be committed.

## Non-Claims

This document does not claim that Notebook 06:

- Generated new repository artifacts.
- Committed generated feature outputs.
- Committed daily bars.
- Executed live backfills in CI.
- Executed live StratLake feature builds in CI.
- Executed archives or restores in CI.
- Executed Google Drive mutation in CI.
- Used credentials in CI.
- Passed Colab smoke test (smoke is pending).
- Verified `stratlake-session-archive-bootstrap` or `stratlake-session-archive-restore-bootstrap` upstream contracts.
- Used Google Drive as the active app workspace.
- Is a strategy or backtest notebook.

## Merge Readiness Handoff Notes

M9.6 manual Colab smoke is complete with notes. All core runtime checks passed; archive
creation and restore remained preview-only; StratLake archive/bootstrap commands remain
unverified beyond availability.

Notebook 06 is not yet final milestone merge-ready until:

- M9.7: Milestone 9 merge readiness is confirmed using M9.6 smoke status.

Do not close M9 merge readiness in M9.6. M9.7 should use `colab_smoke_passed_with_notes`
as the recorded smoke outcome when making merge-readiness decisions.

## Committed Source

The following may be committed as part of M9:

- Cleaned Notebook 06 source.
- Documentation: import audit, staging classification, command-surface classification,
  index updates, and development-environment notes.
- Validation configs for source-only readiness, sanitized execution, CLI contracts, and
  CLI registry coverage.
- pytest tests for source hygiene, source invariants, sanitized execution skip behavior,
  and config membership.
