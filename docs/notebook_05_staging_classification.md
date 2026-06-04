# Notebook 05 Staging and Classification

## Summary

This document records the Milestone 8 staging and classification decisions for
Notebook 05 before and during cleanup, command classification, validation, and audit
work.

Notebook 05 is the Q1 StratLake feature-generation tutorial with live Fintech
daily-bars ingestion. It preserves the dual-session pattern introduced by Notebook 04:
`FINTECH_SESSION_ID` identifies the upstream Fintech curated-data workspace, and
`STRATLAKE_SESSION_ID` identifies the downstream StratLake feature/research workspace.
The explicit handoff remains `MARKETLAKE_ROOT`.

Repository validation remains source-only and sanitized. Live runtime state belongs in
Colab and Google Drive, not in Git.

## Candidate Notebook Identity

| Field | Value |
|---|---|
| Repository path | `notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb` |
| Source notebook | Uploaded Notebook 05 latest session archive file supplied outside the repository |
| Notebook title | Notebook 05 - StratLake Q1 Feature Data Generation with Fintech Daily Bars |
| Workflow classification | Live manual Q1 Fintech ingestion plus downstream StratLake feature generation |
| Primary upstream app | `fintech-market-ingestion` |
| Secondary upstream app | `stratlake-trade-engine` |
| Relationship to Notebook 04 | Continues the dual-session Fintech/StratLake handoff into feature generation |
| Staging category | `source_safe_after_cleanup` after Issue #61 |
| Import status | `imported` |
| Manual Colab smoke status | `colab_smoke_pending` |

## Source Review Facts

Milestone 8 review confirmed:

- Outputs were cleared.
- Code-cell execution counts were reset to `null`.
- Top-level Colab/runtime metadata was stripped.
- Cell runtime metadata was stripped or minimized.
- No generated data, archive packs, restored files, session manifests, Drive artifacts,
  logs, screenshots, credentials, private paths, or feature outputs were committed.
- `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` remains the Drive root placeholder.
- The Q1 window remains `2025-01-01` through `2025-04-01`.

## Expected Notebook Role

Notebook 05 should guide a Colab user through:

- Installing `pandas-market-calendars`, `fintech-market-ingestion`, and
  `stratlake-trade-engine`.
- Verifying CLI availability with `shutil.which(...)`.
- Mounting Google Drive manually.
- Defining Fintech, StratLake, MarketLake, and Drive roots.
- Initializing a Fintech project/session under `/content`.
- Extracting `FINTECH_SESSION_ID`.
- Initializing a StratLake session under `/content` with explicit `--marketlake-root`.
- Extracting `STRATLAKE_SESSION_ID`.
- Creating Drive session/archive folders after placeholder and Drive mount guards pass.
- Preparing runtime ticker/config files.
- Reading Alpaca credentials only from Colab Secrets or a hidden prompt.
- Running `fintech-backfill-daily` for Q1 daily bars.
- Inspecting generated curated daily bars.
- Running `stratlake-build-features` for Q1 daily features.
- Inspecting generated feature outputs.
- Running `stratlake-session-export --dry-run`.
- Printing archive/bootstrap and restore guidance.

Notebook 05 should not reimplement Fintech ingestion logic or StratLake feature
generation logic in notebook-side Python.

## Committed Source

The following may be committed:

- Cleaned Notebook 05 source.
- Documentation, including import audit, staging classification, command-surface
  classification, index updates, and development-environment notes.
- Validation configs for source-only readiness, sanitized execution, CLI contracts, and
  CLI registry coverage.
- Tests that inspect source, command shapes, notebook hygiene, and sanitized execution
  boundaries.

## Manual Colab Runtime-Only State

The following belongs only in manual Colab runtime or user-controlled Google Drive:

- Installed packages.
- Mounted Google Drive.
- `/content/fintech-market-ingestion-demo`.
- `/content/stratlake-trade-engine-demo`.
- Fintech session manifests.
- StratLake `.stratlake` session metadata.
- Runtime ticker/config files.
- Alpaca credential environment variables.
- Generated daily bars.
- Generated StratLake features.
- Drive session/archive folders.
- Backup/archive packs.
- Restored archive contents.
- Runtime logs, screenshots, and notebook outputs.

## Never Committed

Never commit:

- Credentials, tokens, `.env` values, or Colab secret values.
- Generated parquet files.
- Raw, curated, or generated market data.
- StratLake feature outputs.
- Restored archive contents.
- Drive runtime folders.
- Session manifests.
- Archive packs or backup packs.
- Runtime logs or screenshots.
- Executed notebook outputs.
- Non-null execution counts.
- Colab runtime metadata.
- Private paths or account-specific Drive folder names.

## Derived Manual Guidance Only

These surfaces are guidance for manual Colab review and should not be treated as
repository-executed commands:

- Fintech archive pack preview.
- Fintech backup-pack restore preview.
- StratLake archive bootstrap preview.
- StratLake archive restore preview.

M8.3 corrected the Fintech backup pack and restore guidance to registry-confirmed flag
forms. StratLake archive/bootstrap previews remain pending upstream CLI verification.

## Cell-Level Staging Classification

| Cell / surface | Category | Repository validation behavior |
|---|---|---|
| `729b15e6` package installs | live manual runtime | Skipped/no-oped; no package installation |
| `f36c9ea9` CLI availability checklist | availability-check-only | Source-inspected; `shutil.which(...)` is not live execution |
| `99822946` Google Drive mount | live manual runtime | Skipped/no-oped; no Drive mount |
| `876835f0` shared path setup and Drive placeholder | runtime path setup | Source-checked; Drive mutation guarded |
| `bce5c87a` `fintech-init-project` | live manual runtime CLI | Static command shape validated; never executed |
| `483eb3d3` `FINTECH_SESSION_ID` extraction | runtime-dependent Python | Skipped/no-oped where needed |
| `3dd31cc7` `stratlake-init-session` | live manual runtime CLI | Static command shape validated; never executed |
| `Bd0ZSBoPx8gs` config existence checks | runtime filesystem inspection | Skipped/no-oped where needed |
| `0d21ddaa` `STRATLAKE_SESSION_ID` extraction | runtime-dependent Python | Skipped/no-oped where needed |
| `0b8e19df` Drive folder creation | Drive mutation | Skipped/no-oped; no Drive folders created |
| `8d3dc4dc` Drive session/path inspection | runtime Drive inspection | Skipped/no-oped |
| `ec58bcb9` StratLake ticker/config writes | runtime file creation | Skipped/no-oped; no config files written |
| `c1206418` Alpaca credentials | credential prompt/secrets | Skipped/no-oped; no credentials read |
| `b7dea0a0` Fintech ticker/output path setup | runtime file/directory creation | Skipped/no-oped |
| `U74qVc08x8gu` optional Fintech restore guidance | commented manual restore guidance | Not executed |
| `a4dbb67a` `fintech-backfill-daily` | live manual runtime CLI | Static command shape validated; never executed |
| `ca096520` daily bars inspection | generated-data inspection | Skipped/no-oped |
| `4879f15f` `MARKETLAKE_ROOT.rglob("*.parquet")` | runtime input inspection | Skipped/no-oped |
| `vqhdHkjVx8gu` Fintech pack preview | preview/manual guidance | Static preview shape validated; not executed |
| `ad8ee301` `os.chdir(...)` and `stratlake-build-features` | runtime cwd mutation plus live CLI | Static command shape validated; never executed |
| `a566d607` feature output inspection | generated-data inspection | Skipped/no-oped |
| `773f1d97` `stratlake-session-export --dry-run` | live manual runtime dry-run CLI | Static dry-run shape validated; never executed |
| `un9-BO0hx8gw` StratLake archive/bootstrap previews | preview/manual guidance; unverified | Not executed; verification deferred |

## Sanitized Execution Boundary Summary

Sanitized execution must skip or no-op:

- `!pip install` and `%pip` cells.
- `from google.colab import drive` and `drive.mount("/content/drive")`.
- `google.colab.userdata`, `getpass.getpass(...)`, and Alpaca credential variables.
- `!fintech-init-project`, `!fintech-backfill-daily`, and `!fintech-backup-data`.
- `!stratlake-init-session`, `!stratlake-build-features`, `!stratlake-session-export`,
  `!stratlake-session-archive-bootstrap`, and
  `!stratlake-session-archive-restore-bootstrap`.
- `.mkdir(...)`, `.write_text(...)`, and `os.chdir(...)`.
- `rglob("*.parquet")` and `.exists()` checks that depend on skipped live cells.
- Reads of generated session manifests or `.stratlake/session.json`.

## Repository Validation Does Not Perform

Repository validation does not:

- install packages,
- mount Google Drive,
- prompt for credentials,
- read Alpaca credentials,
- call Alpaca,
- initialize Fintech or StratLake sessions,
- create Drive folders,
- write runtime ticker/config files,
- create daily bars directories,
- run Fintech CLI commands,
- run StratLake CLI commands,
- generate daily bars,
- generate StratLake features,
- export sessions,
- create archives,
- restore archives,
- inspect generated runtime data.

## Manual Colab Smoke Status

Manual Colab smoke remains `colab_smoke_pending`. No M8 repository validation result
should be read as live Colab runtime evidence.

## Known Follow-Up Items

- Issue #66 should record manual Colab smoke only after a real Colab run is performed.
- Issue #67 should review final merge readiness and preserve all non-claims.
- StratLake archive/bootstrap preview flags should stay manual guidance until upstream
  command contracts are verified.
