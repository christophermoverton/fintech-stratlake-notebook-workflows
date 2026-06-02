# Notebook Cleanup Workflow

## Purpose

Use this workflow to clean Colab notebooks before importing them into this repository. Cleanup turns a notebook from a captured runtime session into reviewable source: outputs are removed, execution state is reset, raw JSON is inspected, secrets and generated payloads are excluded, and notebook code is checked against the repository's native-command-first boundary.

Notebook cleanup must happen before a staged notebook is moved into `notebooks/`. This workflow prepares the process only; it does not import Notebook 00 or any other notebook.

## Relationship to Controlled Staging

Notebook imports should move through controlled staging, cleanup, validation, and review. Do not copy notebooks directly from Google Drive into `notebooks/`.

Use this workflow with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)

Recommended flow:

1. Copy the source notebook from Google Drive or a local download into an uncommitted staging folder outside the repository.
2. Classify the staged notebook using the staging guide.
3. Apply this cleanup workflow.
4. Apply the import checklist and notebook standards.
5. Run repository validation commands.
6. Review the Git diff.
7. Move only cleaned, reviewed notebooks into `notebooks/`.

Staging folders, rejected notebooks, runtime copies, exports, and downloaded Drive content must not be committed.

## Recommended Cleanup Order

1. Work from a staged copy outside the repository.
2. Clear all notebook cell outputs.
3. Reset or remove execution counts.
4. Save the cleaned notebook.
5. Inspect rendered cells for stale notes, local paths, and copied runtime details.
6. Inspect the raw `.ipynb` JSON for outputs, metadata, secrets, embedded blobs, and runtime state.
7. Confirm generated data, archive payloads, restore packs, and local app workspaces are not embedded or staged.
8. Confirm the notebook uses `/content` for active Colab work and Google Drive only for persistence, backup, archive, and restore workflows.
9. Confirm native upstream app CLI commands are used where available.
10. Confirm the notebook does not reimplement upstream app behavior.
11. Run validation commands.
12. Review `git status` and `git diff` before commit.

## Clear Cell Outputs

Clear every output before import. Outputs are runtime artifacts, not source. They may contain generated tables, file manifests, API responses, tracebacks, local paths, environment details, image blobs, or other content that should not enter version control.

In Colab, use the notebook menu option to clear all outputs before saving. After saving, reopen or reload the notebook if needed and confirm no cells still display output.

Block the import if any output remains, including:

- Printed command logs.
- Tracebacks.
- Warnings.
- Dataframe previews.
- Charts or images.
- HTML displays.
- File listings.
- Archive manifests.
- API responses.
- Environment dumps.
- Large embedded output blobs.

## Reset or Remove Execution Counts

Reset or remove execution counts where practical. Execution counts are runtime state and should not be used as evidence that a notebook is ready for commit.

When reviewing the raw `.ipynb` JSON, check code cells for stale values like:

```json
"execution_count": 12
```

Cleaned code cells should use `null` for execution count when outputs are cleared:

```json
"execution_count": null
```

If Colab leaves metadata behind after clearing outputs, inspect it manually and remove runtime-specific state when safe to do so.

## Review Raw `.ipynb` JSON

Do not rely only on the rendered notebook view. Open the staged `.ipynb` as text and inspect the JSON before import.

Search the raw JSON for:

- `"outputs": [` entries that contain values instead of empty lists.
- Non-null `"execution_count"` values.
- Base64 image or binary blobs.
- Long captured stdout or stderr streams.
- HTML or JavaScript output payloads.
- Tracebacks, warnings, and log dumps.
- Runtime filesystem listings.
- Generated tables or dataframe output.
- Secrets, tokens, keys, credential names with real values, or private file paths.
- Colab runtime metadata that records stale execution state.

The JSON review is required because secrets and output blobs can remain in notebook source even when they are not obvious in the rendered view.

## Check Runtime Dumps and Filesystem Listings

Remove cells or outputs that capture runtime dumps or accidental filesystem listings. These often include generated files, local workspaces, mounted Drive paths, temporary folders, and archive contents.

Block the import if the notebook source or outputs include committed copies of:

- `/content` directory listings.
- Mounted Google Drive directory listings.
- Fintech or StratLake local app workspaces.
- Runtime cache directories.
- Session folders.
- Archive pack contents.
- Restore pack contents.
- Generated artifact directories.
- Local user home directories.

It is acceptable for notebook source to define portable path variables and document expected runtime paths, but it must not commit runtime folder contents or copied filesystem dumps.

## Check Logs, Tracebacks, Warnings, and Environment Prints

Remove captured logs, tracebacks, warning dumps, and printed environment details from notebook outputs and markdown notes unless they are minimal, intentional source examples with no sensitive or generated content.

Pay special attention to:

- `os.environ` or shell environment prints.
- Package manager logs.
- CLI debug output.
- Stack traces with local paths.
- API errors that echo request headers or credentials.
- Warnings that include mounted Drive paths.
- Command output that includes generated file manifests.

If a notebook captures a real upstream failure, do not preserve the traceback as notebook output. Summarize the failure in source markdown or open an upstream triage issue when appropriate.

## Check Generated Tables, Charts, Images, and Embedded Blobs

Generated tables, dataframe previews, plots, screenshots, images, and HTML displays must be cleared before import. These are notebook outputs and can become large embedded JSON payloads.

Inspect for:

- Large dataframe previews.
- `display()` output.
- Matplotlib, Plotly, or Altair output.
- Images embedded as base64.
- HTML tables.
- Rich MIME bundles.
- Binary output blobs.

Notebook source may include code that regenerates summaries and review displays at runtime. The generated displays themselves must not be committed.

## Check Secrets, Tokens, Paths, and Personal Details

Search both rendered cells and raw JSON for secrets and personal details. Block the import if any real credential or sensitive value appears anywhere in source, markdown, metadata, or output.

Check for:

- Alpaca API keys or secret keys.
- Bearer tokens.
- Private keys.
- Credential JSON.
- `.env` content.
- Printed secret environment variables.
- API responses that echo credentials.
- Personal Google Drive paths.
- Local machine paths.
- Usernames, home directories, and machine-specific workspace paths.

Use Colab Secrets with a hidden prompt fallback for runtime credentials. Placeholder secret names such as `ALPACA_API_KEY_ID` and `ALPACA_API_SECRET_KEY` are acceptable; literal credential values are not.

## Check Colab Metadata and Runtime State

Colab-specific metadata should be minimal and safe. Remove stale runtime state when it is not needed for notebook behavior.

Review metadata for:

- Runtime hardware state.
- Widget state.
- Execution history.
- Collapsed cells hiding unsafe content.
- Cell IDs or metadata copied from unrelated notebooks.
- Output-related metadata left after clearing outputs.
- Drive mount state or local runtime paths.

Some harmless Colab metadata may remain, but metadata must not preserve generated outputs, secrets, local paths, or stale runtime assumptions.

## Confirm No Generated Data or Archive Payloads

Notebook cells must not contain generated data, archive payloads, restore payloads, or serialized artifacts. This includes pasted content in markdown, code string literals, JSON blocks, and output cells.

Block the import if cells contain:

- Parquet, CSV, JSONL, SQLite, DuckDB, or feature-store payloads.
- Archive pack manifests copied as committed data.
- Restore pack contents.
- Generated backtest artifacts.
- Generated feature tables.
- Runtime session payloads.
- Large copied API responses.

Generated files should be recreated by native commands or preserved outside Git through Google Drive persistence, backup, archive, and restore workflows.

## Confirm Native CLI Usage

Notebooks should use native `fintech-market-ingestion` and `stratlake-trade-engine` CLI commands whenever available. Notebook code may orchestrate commands, validate inputs and outputs, parse command results, display summaries, and support human review.

During cleanup, mark cells for rewrite if they duplicate behavior that belongs upstream. The notebook should call the app command rather than recoding app behavior in notebook cells.

Good notebook responsibilities include:

- Setting runtime variables.
- Installing or locating upstream apps.
- Running native CLI commands.
- Checking expected output files exist.
- Parsing small summaries for review.
- Displaying generated outputs after runtime execution.

## Confirm Upstream Logic Is Not Reimplemented

Do not import notebooks that reimplement native app responsibilities.

Notebook cells should not reimplement:

- Fintech ingestion logic.
- Fintech archive or restore behavior.
- StratLake feature generation or normalization.
- StratLake archive or restore behavior.
- Strategy logic.
- Backtesting logic.
- Artifact generation logic.

If the notebook contains useful logic that belongs in an upstream app, classify it as `upstream_triage_needed/` in staging and keep it out of `notebooks/` until the boundary is resolved.

## Final Validation Before Import

Run these commands before moving a cleaned notebook from staging into `notebooks/` and again before committing:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

These scripts are guardrails, not a replacement for manual review. After they pass, inspect `git status` and `git diff` to confirm:

- Only intended documentation and reviewed notebook source files are changed.
- No unreviewed staging folder is present.
- No Notebook 00 or other notebook was imported unless the current issue explicitly requires it.
- No `.ipynb` outputs are present.
- No generated data is staged.
- No archives or restore packs are staged.
- No local app workspaces or runtime folders are staged.
- No notebook outputs or embedded blobs are staged.
- No secrets or credential material are staged.
- No upstream app logic was reimplemented in this repository.

For this M2.2 cleanup workflow issue, the final diff must remain documentation-only except for an optional README link.
