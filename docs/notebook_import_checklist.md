# Secret-Safe Notebook Import Checklist

## Purpose

Follow this checklist before moving any Colab notebook from Google Drive into this repository. The goal is to make notebook workflows easy to import, run, and review without exposing credentials, committing generated data, or reimplementing native `fintech-market-ingestion` or `stratlake-trade-engine` logic.

## When to Use This Checklist

Use this checklist for every notebook imported from Google Drive, copied from a local Colab download, restored from an archive, or adapted from a prior runtime session. Do not import Notebook 00 through Notebook 09, or any other notebook, until this review is complete and later `.gitignore` guardrails are in place.

## Import Safety Principles

- Existing notebooks currently live in Google Drive and should stay there until safety guardrails are documented and reviewed.
- Active Colab work should stay under `/content`.
- Google Drive should be used only for persistence, archive packs, backups, and restore workflows.
- Do not commit generated data, parquet files, archive packs, restore packs, artifacts, secrets, local app workspaces, or notebook outputs.
- Do not print API keys or secrets.
- Use Colab Secrets with a hidden prompt fallback for Alpaca credentials.
- Use native Fintech and StratLake CLI commands whenever available.
- Notebook code should orchestrate, validate, parse, display, and review outputs.
- Notebook code should not reimplement native ingestion, archive/restore, feature generation, backtesting, strategy logic, or artifact generation.

The repository `.gitignore` is a safety boundary, not a substitute for review. Generated data, archives, artifacts, local workspaces, and secrets must not be committed even if an ignore rule is missing. Reviewed notebooks may be committed later, but only after outputs are cleared and safety checks pass. Active Colab work belongs under `/content`; Drive is for persistence, archive, and restore workflows, not Git source control.

The ignore rules intentionally block files with names containing `secret`, `secrets`, `credential`, or `credentials`. Avoid those words in commit-worthy filenames unless a later issue explicitly adds a narrow unignore rule for a safe documentation file.

## Approved Import Workflow

1. Copy the notebook from Google Drive into a temporary local staging folder.
2. Do not copy directly into `notebooks/` until review is complete.
3. Open the notebook and clear all outputs.
4. Remove or reset execution counts where practical.
5. Search the raw `.ipynb` JSON for secrets and accidental runtime output.
6. Replace hardcoded credentials with the approved Colab Secrets / hidden prompt fallback pattern.
7. Confirm generated files, archive packs, parquet data, and local workspaces are not embedded or committed.
8. Confirm paths follow the `/content` active-work and Google Drive persistence boundary.
9. Confirm notebook code uses native app CLIs rather than reimplementing upstream logic.
10. Move the cleaned notebook into `notebooks/`.
11. Run repository safety checks once they are available in later M1 issues.
12. Review `git status` before commit.

## Secret Safety Checks

Block the import if the notebook source, markdown, metadata, outputs, screenshots, or copied files include any of the following:

- Hardcoded Alpaca API keys.
- Hardcoded Alpaca secret keys.
- Printed environment variables containing secrets.
- `.env` files.
- Credential JSON files.
- Bearer tokens.
- Private keys.
- API responses that echo credentials.
- Screenshots or markdown cells containing secrets.

Search both rendered notebook cells and the raw `.ipynb` JSON. Literal secret values are not safe even when they appear in comments, markdown examples, tracebacks, or stale output cells.

## Notebook Output Cleanup

Before commit:

- Clear all cell outputs.
- Check for tracebacks that may include paths or environment values.
- Check for printed `os.environ`.
- Check for displayed credential variables.
- Check for accidental logs containing secrets.
- Check for large embedded output blobs.
- Remove execution output that includes generated tables, file listings, archive manifests, API responses, or runtime diagnostics that are not needed in source control.

## Generated Data and Artifact Checks

Block the import if Git would include generated or runtime files such as:

- Parquet files.
- CSV data exports.
- DuckDB or SQLite databases.
- Fintech local workspaces.
- StratLake local workspaces.
- Generated feature stores.
- Generated artifacts.
- Archive packs.
- Restore packs.
- Session folders.
- `/content` exports.
- Google Drive copied runtime folders.

Notebook imports should include reviewed notebook source only. Generated files should be recreated by native commands or preserved outside Git through documented persistence, backup, archive, and restore workflows.

## Colab and Google Drive Path Checks

- Active work should be under `/content`.
- Google Drive should be used for persistence, backups, archive packs, and restore packs.
- Drive should not become the active app workspace unless a notebook explicitly documents a safe reason.
- Repository paths should remain relative and portable where possible.
- Local Windows paths should not be committed in notebook source or markdown examples unless clearly marked as non-reproducible local notes.
- Avoid committing paths that point to a mounted personal Drive, local user home directory, runtime cache, or downloaded app workspace.

## Native Command First Review

Notebooks may:

- Orchestrate CLI commands.
- Validate inputs and outputs.
- Parse and display results.
- Summarize generated artifacts.
- Provide review cells.

Notebooks should not reimplement:

- Fintech ingestion logic.
- StratLake feature normalization.
- Archive creation or restore logic.
- Strategy logic.
- Backtesting logic.
- Artifact generation logic.

If native `fintech-market-ingestion` or `stratlake-trade-engine` CLI commands are available, the notebook should call them instead of duplicating their behavior in notebook cells.

## Approved Alpaca Credential Pattern

Use Colab Secrets first and a hidden prompt fallback second:

```python
import getpass
import os

try:
    from google.colab import userdata
except Exception:
    userdata = None

def get_secret_or_prompt(name: str) -> str:
    value = None
    if userdata is not None:
        try:
            value = userdata.get(name)
        except Exception:
            value = None
    if not value:
        value = getpass.getpass(f"Enter {name}: ")
    return value

alpaca_api_key_id = get_secret_or_prompt("ALPACA_API_KEY_ID")
alpaca_api_secret_key = get_secret_or_prompt("ALPACA_API_SECRET_KEY")

if not alpaca_api_key_id or not alpaca_api_secret_key:
    raise ValueError("Missing Alpaca API credentials.")

os.environ["ALPACA_API_KEY_ID"] = alpaca_api_key_id
os.environ["ALPACA_API_SECRET_KEY"] = alpaca_api_secret_key
os.environ["ALPACA_DATA_BASE_URL"] = "https://data.alpaca.markets"
os.environ["ALPACA_FEED"] = "iex"
```

Placeholder names such as `ALPACA_API_KEY_ID` and `ALPACA_API_SECRET_KEY` are safe as secret names. Literal credential values are not safe and must never be committed.

## Pre-Commit Validation Checklist

- The notebook was reviewed from a temporary staging folder before being moved into `notebooks/`.
- All outputs are cleared.
- Execution counts are removed or reset where practical.
- Raw `.ipynb` JSON was searched for secrets, tokens, private keys, credential JSON, and accidental runtime output.
- No generated data, archive packs, restore packs, artifacts, session folders, local app workspaces, or notebook outputs are staged.
- Paths follow the `/content` active-work and Google Drive persistence boundary.
- Alpaca credentials use the approved Colab Secrets / hidden prompt fallback pattern.
- Notebook cells use native app CLI commands whenever available.
- `git status` shows only the intended notebook and documentation changes.

## Import Blockers

Do not import or commit the notebook if any of these are true:

- A real secret, token, private key, or credential file is present.
- Notebook outputs are still present.
- Generated datasets, artifacts, archive packs, restore packs, session folders, or local app workspaces are staged.
- The notebook depends on Google Drive as the active app workspace without documenting a safe reason.
- The notebook reimplements native Fintech ingestion, StratLake feature normalization, archive/restore, strategy, backtesting, or artifact-generation logic.
- The notebook cannot be reviewed without private local files or non-portable paths.
- Safety checks from later M1 issues fail once those checks exist.

## Final Reviewer Checklist

- Purpose and scope match this repository's notebook-first integration role.
- No actual credentials or sensitive runtime values appear in source, markdown, metadata, or outputs.
- No notebook outputs, generated data, archives, restore packs, artifacts, or local workspaces are staged.
- Colab active work stays under `/content`.
- Google Drive usage is limited to persistence, backups, archive packs, and restore packs.
- Native-command-first boundaries are respected.
- The notebook is ready for review as source code, not as a captured runtime session.
