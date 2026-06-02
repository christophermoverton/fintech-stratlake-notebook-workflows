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
python -m pip install -r requirements-notebook-dev.txt
```

Unix or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-notebook-dev.txt
```

The notebook readiness harness uses the Python standard library and expects Python 3.11 or newer for `tomllib` TOML parsing. The pytest execution harness uses the notebook development dependencies in `requirements-notebook-dev.txt`, including JupyterLab, pytest, nbformat, nbclient, and ipykernel.

## Launch JupyterLab

After installing notebook development dependencies, launch JupyterLab from the repository root:

```bash
jupyter lab
```

Use JupyterLab for local notebook authoring and review. Source notebooks should still be cleaned before commit: clear outputs, reset execution counts, and run the repository validation commands.

## Static Repository Checks

Run the existing repository guardrails before committing notebook changes:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
pytest
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

## Pytest Notebook Execution Harness

Run the pytest notebook execution harness:

```bash
pytest
```

This is a deeper layer than the Issue #14 readiness check. The readiness check loads notebook JSON, checks output/count state, classifies cells, and compiles safe Python-only cells. The pytest harness uses `nbformat` and `nbclient` to execute a temporary sanitized notebook copy in a notebook-capable environment.

The pytest harness does not execute the source notebook directly. It:

- Loads Notebook 00 with `nbformat`.
- Builds a sanitized temporary copy under pytest's temporary directory.
- Keeps markdown cells.
- Keeps safe Python cells where possible.
- Replaces shell, Colab, Drive mount, credential, package-install, upstream command, and artifact-producing cells with safe no-op cells or harmless setup fragments.
- Executes the sanitized copy with `nbclient`.
- Confirms the source notebook hash is unchanged.
- Confirms the source notebook remains output-free and has `null` execution counts.

Temporary executed notebooks are test artifacts only and must not be committed.

## CLI Contract Validation

Run the CLI contract validator:

```bash
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
```

To validate a specific notebook:

```bash
python scripts/validate_notebook_cli_contracts.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_cli_contracts.toml
```

The CLI contract validator parses notebook shell command examples and conservative command-preview strings. It checks command names, configured subcommands, and expected flags against `config/notebook_cli_contracts.toml`. When upstream commands are installed locally, it may call safe `--help` forms only. Missing local commands are warnings by default.

The validator never executes notebook command cells, real ingestion, archive writes, restore writes, Drive mounts, credential prompts, live API calls, or artifact-producing workflows.

## Manual Colab Smoke Testing

Local validation cannot fully replace a fresh Colab runtime check. Use the [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md) after local guardrails pass and before treating a notebook as run-ready.

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

The pytest execution harness follows the same safety boundary for source notebooks. It may write sanitized and executed copies under pytest temporary folders, but it never writes outputs back into committed notebooks.

Full Colab execution remains a manual or future explicitly guarded workflow.

## Relationship To Notebook Import

Use this development check after the staged notebook has been cleaned and before it is committed. It should be used with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Notebook Cleanup Workflow](notebook_cleanup_workflow.md)
- [Reusable Notebook Header Template](notebook_header_template.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)

The goal is a notebook that is clean, secret-safe, output-free, reviewable, and development-testable without weakening the repository's native-command-first boundaries.
