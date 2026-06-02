# Reusable Notebook Header Template

## Purpose

Use this guide when preparing the standard opening section for future imported notebooks. A consistent header makes each notebook easier to review, safer to run in Colab, and clearer about the boundary between this notebook workflow repository and the upstream app repositories.

This guide prepares reusable header guidance only. It does not import Notebook 00 or any other notebook, and it does not add executable workflow logic.

## Relationship to Import Review

The notebook header should be completed while the notebook is still in controlled staging, before it is moved into `notebooks/`.

Use this guide with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Notebook Cleanup Workflow](notebook_cleanup_workflow.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)

The header is a review aid, not a substitute for cleanup, validation, or diff review. A notebook is not ready to import until outputs are cleared, execution counts are reset or removed where practical, raw JSON is inspected, and repository validation commands pass.

## Standard Header Structure

Each notebook should open with a Markdown header that covers the sections below. Keep the content specific to the notebook being imported; do not copy stale values from another notebook.

### Notebook Title

Use the planned notebook number and a clear title:

```markdown
# Notebook XX - <Notebook Title>
```

The filename should still follow the numbered snake_case convention described in the notebook standards.

### Notebook Purpose

Explain what the notebook does and what workflow question it answers. The purpose should make the notebook's place in the tutorial or integration sequence clear.

Good purpose statements describe the notebook's orchestration and review role. They should not imply that this repository owns native Fintech ingestion, StratLake feature generation, archive/restore, strategy, backtest, or artifact logic.

### Upstream Apps Used

Declare whether the notebook uses:

- `fintech-market-ingestion`
- `stratlake-trade-engine`
- both upstream apps

For each app, state the notebook-level role, such as installing the app, running a native CLI command, validating expected files, or reviewing generated artifacts.

### Workflow Role

Select one or more workflow roles:

- setup
- extraction/backfill
- session persistence
- archive
- restore
- StratLake initialization
- feature generation
- validation
- strategy smoke test
- backtest review
- research comparison
- audit/review

If a notebook has multiple roles, list only the roles it actually performs. Avoid broad labels that make review harder.

### Runtime Environment Assumptions

State that the notebook is Colab-first and that active runtime work happens under `/content`.

The header should make these assumptions explicit:

- Runtime: Google Colab.
- Active workspace: `/content`.
- Google Drive: persistence, backup, archive, and restore workflows only.
- Version control: generated data, archives, restore packs, local workspaces, runtime folders, notebook outputs, and secrets are not committed.

### Required User Inputs and Configuration

List the user-provided inputs needed to run the notebook. Use placeholders, not real values.

Examples:

- `<FINTECH_SESSION_NAME>`
- `<STRATLAKE_SESSION_ID>`
- `<DRIVE_ROOT>`
- `<START_DATE>`
- `<END_DATE>`
- `<SYMBOL_LIST>`

Placeholders should document what the user must supply without embedding private Drive paths, local machine paths, account details, or credential values.

### Secret Handling

The header must state that credentials are supplied through Colab Secrets or safe runtime prompts.

Do not hard-code:

- API keys.
- Tokens.
- Credential values.
- `.env` values.
- Credential JSON.
- Private keys.

Placeholder secret names such as `ALPACA_API_KEY_ID` and `ALPACA_API_SECRET_KEY` are acceptable. Literal secret values are not.

### Path Conventions

Use portable runtime variables instead of machine-specific paths.

Recommended variables include:

- `FINTECH_ROOT`
- `FINTECH_SESSION_NAME`
- `STRATLAKE_ROOT`
- `STRATLAKE_SESSION_ID`
- `STRATLAKE_ARCHIVE_ID`
- `DRIVE_ROOT`
- `MARKETLAKE_ROOT`

The header should confirm:

- Active app work stays under `/content`.
- Google Drive is used for persistence, backup, archive, and restore workflows.
- Local Windows, macOS, Linux home-directory, mounted Drive, and personal machine paths are not committed.
- Generated app workspaces are not committed.

### Native-Command-First Boundary

The header must describe the notebook as an orchestration, validation, parsing, display, and review layer.

Notebook cells may:

- Configure runtime variables.
- Run upstream app CLIs.
- Validate expected files.
- Parse small summaries for review.
- Display runtime-generated outputs.
- Guide a human review workflow.

Notebook cells should not reimplement:

- Fintech ingestion logic.
- Fintech archive or restore behavior.
- StratLake feature generation or normalization.
- StratLake archive or restore behavior.
- Strategy logic.
- Backtesting logic.
- Artifact generation logic.

Use native upstream app CLI commands whenever available.

### Generated Artifact Boundaries

The header should state which outputs the notebook may generate at runtime and confirm they stay outside Git.

Generated runtime content includes:

- Market data outputs.
- Parquet, CSV, JSONL, DuckDB, SQLite, or feature-store files.
- StratLake features.
- Backtest artifacts.
- Archive packs.
- Restore packs.
- Local app workspaces.
- Runtime folders.
- Notebook outputs.

Generated files should be recreated by native commands or preserved outside Git through Google Drive persistence, backup, archive, and restore workflows.

### Validation Before Commit

Every header should include the expected validation commands:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

These commands are guardrails. Manual review of the notebook source, raw `.ipynb` JSON, `git status`, and `git diff` is still required.

## Header Review Checklist

Before importing a notebook, confirm:

- The title matches the planned notebook number and purpose.
- The purpose is specific and reviewable.
- Upstream app usage is declared.
- Workflow roles are selected accurately.
- Colab-first runtime assumptions are stated.
- `/content` is the active workspace.
- Google Drive is limited to persistence, backup, archive, and restore workflows.
- Required inputs use placeholders, not private values.
- Secret handling uses Colab Secrets or safe runtime prompts.
- Path variables are portable.
- No local machine path or personal Drive path is hard-coded.
- Native-command-first boundaries are stated.
- Generated artifact boundaries are stated.
- Validation commands are listed.
- The header does not include generated data, archive payloads, restore payloads, runtime output, or secrets.

## Copyable Markdown Header

Copy this block into future notebooks and replace every placeholder with notebook-specific content before import.

````markdown
# Notebook XX - <Notebook Title>

## Purpose

Describe what this notebook does, where it fits in the workflow sequence, and what workflow question it answers.

## Upstream apps used

- `fintech-market-ingestion`: <yes/no and notebook-level role>
- `stratlake-trade-engine`: <yes/no and notebook-level role>

## Workflow role

Select one or more:

- setup
- extraction/backfill
- session persistence
- archive
- restore
- StratLake initialization
- feature generation
- validation
- strategy smoke test
- backtest review
- research comparison
- audit/review

## Runtime assumptions

- Designed for Google Colab.
- Active runtime work happens under `/content`.
- Google Drive is used only for persistence, backup, archive, and restore workflows.
- Generated data, archives, restore packs, local workspaces, runtime folders, notebook outputs, and secrets are not committed.

## Required user inputs

- `<PLACEHOLDER_INPUT_1>`: <description>
- `<PLACEHOLDER_INPUT_2>`: <description>

## Secrets

This notebook must use Colab Secrets or safe runtime prompts for credentials.

Do not hard-code API keys, tokens, secrets, `.env` values, credential JSON, or private keys.

## Path conventions

Use portable runtime variables. Do not hard-code local machine paths, personal Google Drive paths, or committed local workspace paths.

Recommended variables:

- `FINTECH_ROOT`
- `FINTECH_SESSION_NAME`
- `STRATLAKE_ROOT`
- `STRATLAKE_SESSION_ID`
- `STRATLAKE_ARCHIVE_ID`
- `DRIVE_ROOT`
- `MARKETLAKE_ROOT`

## Native-command-first boundary

This notebook should orchestrate upstream app commands, validate expected files, parse small summaries, display runtime outputs, and support human review.

It must not reimplement native ingestion, archive/restore, feature generation, strategy, backtest, or artifact logic.

## Generated artifact boundaries

List expected runtime-generated outputs here and confirm they must stay outside Git.

- `<GENERATED_OUTPUT_1>`: <runtime location or description>
- `<GENERATED_OUTPUT_2>`: <runtime location or description>

Do not commit generated data, archives, restore packs, local app workspaces, runtime folders, notebook outputs, or secrets.

## Validation before commit

Run:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```
````

## Optional Setup Code Cell Skeleton

If a notebook needs an initial setup code cell, keep it placeholder-based and safe. This skeleton defines paths and secret-name placeholders without embedding credential values or implementing upstream app logic.

```python
from pathlib import Path
import os

CONTENT_ROOT = Path("/content")
FINTECH_ROOT = CONTENT_ROOT / "fintech-market-ingestion-demo"
STRATLAKE_ROOT = CONTENT_ROOT / "stratlake-trade-engine-demo"
DRIVE_ROOT = Path("/content/drive/MyDrive/<DRIVE_FOLDER_PLACEHOLDER>")

FINTECH_SESSION_NAME = "<FINTECH_SESSION_NAME>"
STRATLAKE_SESSION_ID = "<STRATLAKE_SESSION_ID>"
STRATLAKE_ARCHIVE_ID = "<STRATLAKE_ARCHIVE_ID>"
MARKETLAKE_ROOT = DRIVE_ROOT / "marketlake"

ALPACA_API_KEY_ID_SECRET_NAME = "ALPACA_API_KEY_ID"
ALPACA_API_SECRET_KEY_SECRET_NAME = "ALPACA_API_SECRET_KEY"

for runtime_path in (FINTECH_ROOT, STRATLAKE_ROOT):
    if not str(runtime_path).startswith("/content/"):
        raise ValueError(f"Runtime path must stay under /content: {runtime_path}")

print("Runtime placeholders configured. Credentials must be loaded through Colab Secrets or a safe prompt.")
```

Do not expand this skeleton into ingestion, archive/restore, feature-generation, strategy, backtest, or artifact-generation behavior. Use native upstream app commands in later cells where available.

## Final Import Gate

For this M2.3 header-template issue, the final diff must remain documentation/template-only except for an optional README link. No Notebook 00 pilot import should be performed.
