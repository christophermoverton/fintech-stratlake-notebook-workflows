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
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/04_stratlake_feature_series_index_setup.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
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
notebooks/01_fintech_daily_bars_extraction_backfill.ipynb
notebooks/02_fintech_session_persistence_save_restore.ipynb
notebooks/03_fintech_archive_backup_pack_and_restore.ipynb
notebooks/04_stratlake_feature_series_index_setup.ipynb
notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb
notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb
```

## Pytest Notebook Execution Harness

Run the pytest notebook execution harness:

```bash
pytest
```

This is a deeper layer than the Issue #14 readiness check. The readiness check loads notebook JSON, checks output/count state, classifies cells, and compiles safe Python-only cells. The pytest harness uses `nbformat` and `nbclient` to execute a temporary sanitized notebook copy in a notebook-capable environment.

The pytest harness does not execute the source notebook directly. It:

- Loads the configured imported notebooks with `nbformat`.
- Builds a sanitized temporary copy under pytest's temporary directory.
- Keeps markdown cells.
- Keeps safe Python cells where possible.
- Replaces shell, Colab, Drive mount, credential, package-install, upstream command, archive/restore, generated-data, and artifact-producing cells with safe no-op cells or harmless setup fragments.
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

## CLI Registry Validation

Run the argument-aware CLI registry validator:

```bash
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
```

Optional focused Notebook 02 check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
```

Optional focused Notebook 03 check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/03_fintech_archive_backup_pack_and_restore.ipynb --config config/notebook_cli_registry.toml
```

Optional focused Notebook 04 check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/04_stratlake_feature_series_index_setup.ipynb --config config/notebook_cli_registry.toml
```

Optional focused Notebook 05 check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb --config config/notebook_cli_registry.toml
```

Optional focused Notebook 06 check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb --config config/notebook_cli_registry.toml
```

The registry validator checks command and subcommand identity plus argument semantics against `config/cli_command_registry.toml` and `config/notebook_cli_registry.toml`. It validates supported versus unsupported flags, boolean flags receiving values, value flags missing values, constrained `allowed_values`, `argparse_required`, `notebook_contract_required`, and conditional `required_when` behavior. It also rejects excluded command candidates, including `fintech-restore-session`, when they appear as valid current notebook syntax.

Like the other repository-side validators, it is non-executing and does not run upstream CLI workflows.

## Validation Layer Roles

- CLI contract validation: broad command-surface and safe `--help` contract checks; expected missing local upstream command warnings can appear here.
- CLI registry validation: argument-aware command/subcommand/flag/value semantics and exclusion checks.
- Execution-readiness validation: notebook JSON/state and safe Python syntax readiness checks.

Keep all three layers enabled. The registry validator is additive and does not replace the existing CLI contract or execution-readiness checks.

For registry schema, traceability policy, and maintenance workflow, see [CLI Command Registry Guide](cli_command_registry.md).

## Notebook 04 Runtime Boundary

Notebook 04 (`notebooks/04_stratlake_feature_series_index_setup.ipynb`) is the first StratLake-facing notebook in the tutorial series. It introduces the dual-session pattern:

```text
FINTECH_SESSION_ID   -> upstream ingestion / curated-data workspace
STRATLAKE_SESSION_ID -> downstream feature/research workspace
```

Repository validation for Notebook 04 uses source-only readiness, CLI contract/registry validation, and sanitized execution. It does **not**:

- Install packages from TestPyPI (`fintech-market-ingestion`, `stratlake-trade-engine`, `pandas-market-calendars`).
- Mount Google Drive.
- Run `fintech-init-project` to create a Fintech session workspace.
- Run `stratlake-init-session` to create a StratLake session workspace.
- Create Drive session folders or archive directories.
- Enumerate available Drive sessions.
- Inspect or mutate `MARKETLAKE_ROOT`.
- Restore Fintech curated data from a Drive archive pack.
- Generate StratLake features.
- Mutate the Notebook 04 source file.

These operations remain manual Colab-only. The `FINTECH_SESSION_ID`, `STRATLAKE_SESSION_ID`, `MARKETLAKE_ROOT`, `fintech-init-project`, and `stratlake-init-session` identifiers are preserved in source as live Colab workflow guidance; they are skipped or no-oped by the sanitized execution harness.

The `fintech-backup-data pack` and `fintech-backup-data restore` preview strings in Notebook 04 use registry-confirmed flag shapes (updated in M7.3). They are printed as human-readable guidance only; they are never executed by repository validation.

## Notebook 05 Runtime Boundary

Notebook 05 (`notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb`) is a manual Colab workflow for live Q1 Fintech daily-bars ingestion and downstream StratLake feature generation. It keeps the Notebook 04 dual-session pattern:

```text
FINTECH_SESSION_ID   -> upstream ingestion / curated-data workspace
STRATLAKE_SESSION_ID -> downstream feature/research workspace
MARKETLAKE_ROOT      -> explicit Fintech-to-StratLake curated-data handoff
```

Repository validation for Notebook 05 uses source-only readiness, CLI contract/registry validation, and sanitized execution. It does **not**:

- Install packages from TestPyPI or PyPI.
- Mount Google Drive.
- Prompt for or read Alpaca credentials.
- Call Alpaca.
- Run `fintech-init-project` or `stratlake-init-session`.
- Run `fintech-backfill-daily`.
- Run `stratlake-build-features`.
- Run `stratlake-session-export`.
- Create Drive session folders or archive directories.
- Write runtime ticker/config files.
- Create daily bars directories.
- Inspect generated daily bars or generated feature outputs.
- Create, export, restore, or inspect archives.
- Mutate the Notebook 05 source file.

These operations remain manual Colab-only. Alpaca credentials should be handled only
through Colab Secrets or a hidden prompt in manual runtime, never committed or printed.
Google Drive remains persistence/archive/session storage only; active app work stays
under `/content`.

Notebook 05 preserves `FINTECH_SESSION_ID`, `STRATLAKE_SESSION_ID`, `MARKETLAKE_ROOT`,
the Q1 window `2025-01-01` to `2025-04-01`, `fintech-backfill-daily`,
`stratlake-build-features`, and `stratlake-session-export --dry-run` as source-visible
workflow guidance. Issue #66 records manual Colab smoke as
`colab_smoke_passed_with_notes` from an uploaded executed artifact. That executed
artifact must not be committed as repository source; developers must still clear
outputs, reset execution counts, strip runtime metadata, and avoid committing runtime
files.

## Notebook 06 Runtime Boundary

Notebook 06 (`notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb`) is
a conservative validation, archive-preview, restore-readiness, and handoff checkpoint
after Notebook 05. It is not a strategy notebook, backtest notebook, or
feature-generation framework. It validates the Fintech-to-StratLake Q1 feature handoff
and prepares Notebook 07 strategy/backtest work. It keeps the same dual-session pattern:

```text
FINTECH_SESSION_ID   -> upstream ingestion / curated-data workspace
STRATLAKE_SESSION_ID -> downstream feature/research workspace
MARKETLAKE_ROOT      -> explicit Fintech-to-StratLake curated-data handoff
```

Repository validation for Notebook 06 uses source-only readiness, CLI contract/registry
validation, and sanitized execution. It does **not**:

- Install packages from TestPyPI or PyPI.
- Mount Google Drive.
- Prompt for or read Alpaca credentials.
- Call Alpaca.
- Run `fintech-init-project` or `stratlake-init-session`.
- Create or mutate Drive session/archive folders.
- Write runtime ticker/config files.
- Run `fintech-backfill-daily`.
- Run `stratlake-build-features`.
- Run `stratlake-session-export --dry-run`.
- Execute `subprocess.run(...)` for archive creation or restore.
- Read generated daily bars or generated feature outputs.
- Call `display(...)`.
- Check CLI availability via `required_workflow_commands` (those checks raise
  `RuntimeError` when CLIs are absent in CI).
- Inspect StratLake session portability assuming runtime workspace exists.
- Construct the final JSON handoff summary from runtime-derived session values.
- Mutate the Notebook 06 source file.

These operations remain manual Colab-only. The Fintech backup pack/restore preview
commands were corrected to registry-current syntax in M9.3 (using `--backup-pack-dir`,
`--restore-root`, `--overwrite-policy`, `--workspace-root`, `--source-dataset-root`,
`--backup-root`, `--backup-id`, `--shard-size-mb`). They are printed as human-readable
guidance only; they are never executed by repository validation.

The `stratlake-session-archive-bootstrap` and `stratlake-session-archive-restore-bootstrap`
commands remain unverified preview/manual guidance. They are source-visible in
`optional_unverified_preview_commands` but are excluded from confirmed registry coverage
until upstream contract verification occurs.

Sanitized execution is conservative and validates source structure, source invariants,
and skip behavior. It does not prove live Colab runtime behavior. Manual Colab smoke
for Notebook 06 is `colab_smoke_passed_with_notes` (recorded in Issue #74).

## Validation Layer Distinction

Repository validation for source notebooks operates at four distinct layers:

1. **Source-only readiness** (`config/notebook_test.toml`): confirms notebook JSON is
   clean, output-free, execution-count-null, free of forbidden paths, and that safe
   Python cells compile. Does not execute the notebook.

2. **Static CLI contract/registry validation** (`config/notebook_cli_contracts.toml`,
   `config/notebook_cli_registry.toml`): parses command examples and preview strings
   against known CLI shapes, flags, and allowed values. Does not execute any commands.

3. **Sanitized execution** (`config/notebook_execution_test.toml`): builds a temporary
   copy replacing runtime-heavy cells with no-ops and executes the sanitized copy with
   `nbclient`. Confirms source notebook is unchanged after execution. Does not execute
   live runtime, Drive, credential, CLI, archive, restore, export, ingestion, or
   feature-generation cells.

4. **Manual Colab smoke** (documented in [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md)):
   a human runs the notebook end-to-end in a live Colab environment with real
   credentials, Drive mount, and upstream CLI access. Outcome is recorded as
   `colab_smoke_passed`, `colab_smoke_passed_with_notes`, or
   `colab_smoke_failed_needs_rerun`. Executed artifacts must not be committed.

**Sanitized execution is not a substitute for manual Colab smoke.** Each layer validates
a distinct concern. All four layers should be recorded before a notebook is treated as
fully validated.

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
- Notebook 03 archive backup-pack cells that create demo files, create backup packs, validate or inspect runtime backup packs, restore data, or inspect restored files.
- Notebook 04 cells that install packages, mount Google Drive, run `fintech-init-project`, run `stratlake-init-session`, create Drive session folders, enumerate Drive sessions, inspect `MARKETLAKE_ROOT`, or construct archive/restore command previews from runtime-derived session variables.
- Notebook 05 cells that install packages, mount Google Drive, read Alpaca credentials, run `fintech-init-project`, run `stratlake-init-session`, run `fintech-backfill-daily`, run `stratlake-build-features`, run `stratlake-session-export`, create Drive folders, write ticker/config files, create daily-bars directories, inspect generated data, mutate `os.chdir(...)`, or construct archive/export/restore previews from runtime-derived variables.
- Notebook 06 cells that install packages, mount Google Drive, read Alpaca credentials, run `fintech-init-project`, run `stratlake-init-session`, run `fintech-backfill-daily`, run `stratlake-build-features`, run `stratlake-session-export --dry-run`, call `subprocess.run(...)` for archive/restore, create Drive session/archive folders, write ticker/config files, inspect generated daily bars or feature outputs (`pd.read_parquet(...)`, `rglob("*.parquet")`), call `display(...)`, construct archive/restore previews from runtime-derived session paths, check CLI availability via `required_workflow_commands` (which raises `RuntimeError` when CLIs are absent), or construct the final JSON handoff summary from runtime-derived values.

Skipped cells still remain subject to output-free, execution-count, secret, and repository cleanliness checks. They are skipped for syntax compilation because they may rely on notebook magics, Colab runtime APIs, credentials, Drive mounts, or native upstream CLIs.

## What It Does Not Test

The harness does not:

- Execute the full notebook.
- Save notebook outputs.
- Mount Google Drive.
- Prompt for credentials.
- Install packages.
- Run market-data ingestion.
- Call Alpaca.
- Generate daily bars.
- Run archive or restore commands.
- Export sessions.
- Create demo `.parquet` placeholder files.
- Validate or inspect runtime backup packs.
- Run StratLake feature generation, strategy execution, backtests, or artifact generation.
- Initialize Fintech or StratLake project sessions (`fintech-init-project`, `stratlake-init-session`).
- Create or restore Fintech curated-data archive packs for StratLake's `marketlake_root`.
- Create Drive session folders, archive directories, or StratLake session workspaces.
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
