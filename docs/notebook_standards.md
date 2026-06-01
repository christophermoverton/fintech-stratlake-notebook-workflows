# Notebook Naming, Metadata, and Commit Standards

## Purpose

This document defines notebook naming, top-of-notebook metadata, path/session conventions, archive/restore metadata, and commit-readiness standards for the initial Colab notebook sequence. It must be used before importing reviewed notebooks from Google Drive into this repository.

The goal is to keep notebook workflows easy to import, run, and review without exposing credentials, committing generated data, or reimplementing native `fintech-market-ingestion` or `stratlake-trade-engine` logic.

## Notebook Naming Convention

Notebook filenames must be stable, numbered, and snake_case. The leading number preserves tutorial order. Do not reuse an existing number for an unrelated workflow. If a future workflow is added, use the next available number or a clearly scoped subdirectory in a later milestone.

Use this filename pattern:

```text
NN_short_snake_case_description.ipynb
```

Reviewed notebooks may be committed later, but only after outputs are cleared, execution counts are reset or removed where practical, and validation checks pass.

## Planned Notebook Sequence

```text
00_setup_and_storage_overview.ipynb
01_fintech_daily_bars_backfill.ipynb
02_session_save_and_restore.ipynb
03_archive_backup_pack_and_restore.ipynb
04_stratlake_feature_series_index_setup.ipynb
05_stratlake_q1_feature_generation.ipynb
06_feature_validation_archive_handoff.ipynb
07_feature_consumption_strategy_smoke_test.ipynb
08_single_strategy_backtest_artifact_review.ipynb
09_multi_strategy_comparison_review.ipynb
```

Notebook 00 through Notebook 09 should remain the initial tutorial and integration path. Later notebooks should preserve this ordering instead of renaming or repurposing these files.

## Required Notebook Header Metadata

Each notebook should include a Markdown metadata header near the top:

```markdown
# Notebook XX - Title

## Purpose
Briefly explain what this notebook does and how it fits the workflow sequence.

## Repository Role
This notebook belongs to the notebook workflow repository and should orchestrate native app behavior rather than reimplementing upstream logic.

## Expected Runtime
- Runtime: Google Colab
- Active workspace: `/content`
- Persistence/archive storage: Google Drive
- Credentials: Colab Secrets or hidden prompt fallback

## Upstream Apps
- fintech-market-ingestion
- stratlake-trade-engine

## Session and Path Variables
- FINTECH_ROOT:
- FINTECH_SESSION_NAME:
- STRATLAKE_ROOT:
- STRATLAKE_SESSION_ID:
- STRATLAKE_ARCHIVE_ID:
- DRIVE_ROOT:
- MARKETLAKE_ROOT:

## Native Commands Used
List the Fintech and StratLake CLI commands used by this notebook.

## Generated Outputs
List expected generated outputs and confirm they must not be committed.

## Commit Safety
Outputs must be cleared and repository validation checks must pass before commit.
```

The header should be updated for each notebook instead of copied forward as stale boilerplate.

## Path and Session Conventions

- Active Colab work belongs under `/content`.
- Google Drive is for persistence, backups, archive packs, and restore packs.
- Google Drive should not become the active app workspace unless a notebook documents a safe reason.
- `FINTECH_ROOT` should point to the Fintech demo or project root in the active Colab workspace.
- `STRATLAKE_ROOT` should point to the StratLake demo or project root in the active Colab workspace.
- `DRIVE_ROOT` should point to the Google Drive persistence root used by the tutorial.
- `MARKETLAKE_ROOT` should point to Fintech curated data consumed by StratLake.
- Stable session IDs should be used when a notebook depends on outputs from earlier notebooks.
- Repository-relative paths should be used where possible in committed notebook source.
- Local Windows paths should not be committed unless clearly marked as non-reproducible local notes.

## Archive and Restore Metadata

When a notebook creates or consumes a StratLake archive/session, document the session and archive identifiers in the notebook header or setup section.

Known example conventions:

```text
STRATLAKE_SESSION_ID = stratlake_q1_feature_consumption
STRATLAKE_ARCHIVE_ID = stratlake-session-stratlake_q1_feature_consumption
```

Known archive pack runtime path pattern:

```text
/content/drive/MyDrive/fintech-stratlake-tutorial/stratlake-trade-engine/sessions/stratlake_q1_feature_consumption/archives/stratlake-session-stratlake_q1_feature_consumption
```

This path is a runtime or Google Drive persistence path. It documents where generated archive content may exist during a Colab workflow, but the generated content must not be committed.

Restore commands using `--target-root .` should be run from inside the target StratLake workspace, for example:

```text
/content/stratlake-trade-engine-demo
```

## Native Command First Standard

Notebooks may:

- Install packages.
- Configure runtime variables.
- Call native CLIs.
- Validate expected files.
- Parse command outputs.
- Display summaries.
- Review artifacts.

Notebooks should not reimplement:

- Fintech ingestion logic.
- StratLake feature normalization.
- Archive creation or restore logic.
- Strategy logic.
- Backtesting logic.
- Artifact generation logic.

Use native `fintech-market-ingestion` and `stratlake-trade-engine` CLI commands whenever available. Notebook cells should remain orchestration and review layers.

## Commit Readiness Checklist

Before committing a notebook:

- Notebook outputs are cleared.
- Execution counts are reset or removed where practical.
- No hardcoded secrets are present.
- No printed environment dumps are present.
- No generated data or archive files are staged.
- No local app workspaces are staged.
- No Google Drive runtime folders are staged.
- Native-command-first boundaries are respected.
- Validation scripts pass.

## Review Checklist Before Import

- The notebook filename matches the planned numbered snake_case convention.
- The required metadata header is present and specific to the notebook.
- `/content` is used as the active Colab workspace.
- Google Drive usage is limited to persistence, archive, backup, and restore workflows.
- Session IDs and archive IDs are documented when later notebooks depend on them.
- Generated outputs are listed and clearly marked as not committed.
- Native CLI commands are listed.
- Notebook code orchestrates, validates, parses, displays, and reviews outputs instead of reimplementing upstream app logic.
- The secret-safe import checklist has been followed.

## Validation Commands

Run these commands before committing reviewed notebooks:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

These scripts are guardrails, not a replacement for manual review.

## Non-Goals

- Do not import Notebook 00 through Notebook 09 as part of this standards issue.
- Do not add generated data.
- Do not add archive packs.
- Do not add restore packs.
- Do not add local app workspaces.
- Do not add real notebook outputs.
- Do not create issue templates.
- Do not add GitHub Actions workflows.
- Do not implement upstream app fixes.
