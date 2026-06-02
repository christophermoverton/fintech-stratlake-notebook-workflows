# Notebook Development Environment

## Purpose

Use this guide to set up a local development environment for reviewing imported notebooks before commit. The environment supports repository static checks and a notebook execution-readiness harness that catches syntax problems in safe Python-only cells without executing notebook workflows end to end.

The harness complements Colab and manual review. It does not replace controlled staging, cleanup, raw JSON inspection, or notebook execution in an appropriate runtime.

## Local Virtual Environment

Create a virtual environment before running local validation.

Windows PowerShell:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

Unix or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

The notebook readiness harness uses the Python standard library and expects Python 3.11 or newer for `tomllib` TOML parsing.

## Static Repository Checks

Run the existing repository guardrails before committing notebook changes:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

These checks scan for likely secrets, notebook outputs, execution counts, generated folders, and other repository cleanliness problems.

## Execution-Readiness Check

Run the TOML-backed notebook readiness harness:

```bash
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
```

To validate a specific notebook:

```bash
python scripts/validate_notebook_execution_readiness.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_test.toml
```

The default config currently targets:

```text
notebooks/00_setup_and_storage_overview.ipynb
```

## What The Harness Checks

The harness:

- Loads the TOML config.
- Loads notebook JSON.
- Confirms code-cell outputs are empty when configured.
- Confirms code-cell execution counts are `null` when configured.
- Checks for forbidden committed path fragments.
- Classifies code cells by safety category.
- Compiles Python-only cells that are not skipped.
- Prints a concise readiness report.
- Exits nonzero on malformed JSON, output/count failures, forbidden paths, or Python syntax failures in checked cells.

This catches problems like malformed Python string construction in safe preview cells without running notebook side effects.

## Unsafe Cells Skipped By Default

The harness does not execute notebooks. It also skips cells that should not be locally executed or compiled as ordinary Python by default, including:

- Shell or magic cells.
- Colab-only cells.
- Google Drive mount cells.
- Credential and prompt cells.
- Package-install and network cells.
- Artifact-producing or upstream command cells.

Skipped cells still remain subject to output-free, execution-count, secret, and repository cleanliness checks. They are skipped for syntax compilation because they may rely on notebook magics, Colab runtime APIs, credentials, Drive mounts, or native upstream CLIs.

## What It Does Not Test

The harness does not:

- Execute the full notebook.
- Save notebook outputs.
- Mount Google Drive.
- Prompt for credentials.
- Install packages.
- Run market-data ingestion.
- Run archive or restore commands.
- Run StratLake feature generation, strategy execution, backtests, or artifact generation.
- Mutate notebook files.

Full Colab execution remains a manual or future explicitly guarded workflow.

## Relationship To Notebook Import

Use this development check after the staged notebook has been cleaned and before it is committed. It should be used with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Notebook Cleanup Workflow](notebook_cleanup_workflow.md)
- [Reusable Notebook Header Template](notebook_header_template.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)

The goal is a notebook that is clean, secret-safe, output-free, reviewable, and development-testable without weakening the repository's native-command-first boundaries.
