# CLI Command Registry

## Purpose

The CLI command registry exists to validate notebook command examples against verified upstream command surfaces used by current imported notebooks.

It protects notebook examples from drifting into invalid command syntax, catches argument-level mistakes before manual Colab smoke testing, and preserves lessons from prior M4/M5 regressions.

The registry validator is:

- non-executing
- additive to the existing validation stack
- repository-side only
- not a replacement for upstream CLI parser tests, implementation tests, or runtime smoke testing

## What The Registry Validates

Registry validation checks:

- known command names
- known subcommands
- supported flags
- unsupported flags
- boolean flags receiving values
- value flags missing values
- constrained `allowed_values`
- `argparse_required`
- `notebook_contract_required`
- `required_when`
- excluded candidates such as `fintech-restore-session`
- conservative notebook command examples from shell cells and command-preview variables

## What The Registry Does Not Validate

Registry validation does not:

- execute upstream commands
- run live `--help`
- mount Google Drive
- restore data
- create backup/archive packs
- initialize runtime workspaces
- install packages from notebooks
- call external APIs
- verify every upstream command option exhaustively
- replace upstream CLI parser tests
- replace manual Colab smoke testing
- make unconfirmed commands valid

## Files

- `config/cli_command_registry.toml`: verified command/subcommand/flag registry with traceability metadata.
- `config/notebook_cli_registry.toml`: validator configuration, default targets, unknown-command policy, and ignore/watch behavior.
- `scripts/validate_notebook_cli_registry.py`: non-executing argument-aware validator.
- `tests/test_notebook_cli_registry.py`: regression tests for registry and validator behavior.

## Registry Accuracy Policy

Anti-hallucination rule:

Commands, subcommands, flags, constrained values, defaults, unsupported patterns, and classifications must not be invented or inferred because they seem plausible.

Every supported registry entry must be grounded in at least one of:

- upstream `fintech-market-ingestion` implementation
- upstream `fintech-market-ingestion` tests/docs
- upstream `stratlake-trade-engine` implementation/tests/docs, only when relevant to current notebook scope
- current notebook workflow usage
- existing repository validation config, clearly marked as notebook-side expectation rather than upstream proof

If a command or flag cannot be confirmed:

- do not add it as supported
- omit it, or mark it as excluded/unconfirmed only when useful
- document uncertainty in notes
- do not treat it as valid notebook syntax

## Schema Overview

Current registry concepts in `config/cli_command_registry.toml`:

Top-level metadata:

- `schema_version`
- `accuracy_policy`
- `default_unknown_command_policy` (registry metadata)
- notes including explicit guidance to avoid ambiguous plain `required`

Command entries:

- `[[commands]]`
- `name`
- `owner`
- `subcommands`
- `expected_missing_local`
- `classifications`
- `confirmed_from`
- `upstream_source_status`
- `notes`
- `[commands.flags]`

Subcommand entries:

- `[[command_subcommands]]`
- `command`
- `subcommand`
- `owner`
- `expected_missing_local`
- `classifications`
- `confirmed_from`
- `unsupported_flags`
- `unsupported_patterns`
- `[command_subcommands.flags]`

Excluded candidates:

- `[[excluded_candidates]]`
- `name`
- `owner`
- `status`
- `valid_notebook_syntax = false`
- `confirmed_from`
- `notes`
- `unsupported_patterns`

## Command Entries

`[[commands]]` describe top-level CLI command surfaces that are valid in current notebook scope.

Each command entry is traceable via `confirmed_from` and may include:

- `classifications` for reporting intent
- `subcommands` for command families
- command-level `unsupported_patterns` where known invalid assumptions must be blocked
- command-level flags under `[commands.flags]`

## Subcommand Entries

`[[command_subcommands]]` define the argument-aware surface for command families.

These entries are used for strict subcommand validation, including:

- supported flags
- unsupported flags
- unsupported patterns
- required-flag semantics
- constrained value checks

## Flag Entries

Flag entries support explicit semantics:

- `kind = "boolean"`: standalone flag that must not receive a value.
- `kind = "value"`: flag that requires a value in `--flag value` or `--flag=value` form.
- `argparse_required`: upstream parser requires this argument.
- `notebook_contract_required`: notebook examples require explicit inclusion for reproducibility/clarity.
- `required_when`: conditional runtime requirement (for example, when not dry run).
- `allowed_values`: enforced constrained value set.
- `example_values`: documentation-only examples, not enforced.
- `default_value` or `default_behavior`: metadata only; not auto-required by validator.
- `confirmed_from`: traceability evidence for the flag definition.

## Required-Flag Semantics

Ambiguous plain `required = true/false` is intentionally not used.

Use:

- `argparse_required` for upstream parser requirements.
- `notebook_contract_required` for notebook-side explicit expectations.
- `required_when` for conditional runtime requirements.

Examples currently preserved:

- `fintech-backup-data restore --backup-pack-dir`: `argparse_required = true`
- `fintech-backup-data restore --restore-root`: `argparse_required = true`
- `fintech-save-session --destination`: `required_when = "not_dry_run"`

## Unsupported Flags and Patterns

Use `unsupported_flags` and `unsupported_patterns` to block known-invalid assumptions.

M4/M5 examples preserved:

- `fintech-backup-data restore --source ...` is unsupported.
- `fintech-backup-data restore --overwrite-policy refuse` is unsupported.
- older workspace/target-dataset-root/backup-root/backup-id restore preview shape is not valid for current backup-pack restore syntax.

## Classifications

Classifications describe notebook command intent and validator reporting.

- `safe_help`: help-only command examples.
- `safe_preview`: printed/preview command text.
- `dry_run`: command syntax includes dry-run semantics.
- `manual_only_live`: valid syntax but live execution remains manual Colab/runtime-only.
- `unsafe_live`: should not be run by repository validation.

Classifications do not grant permission for repository validation to execute upstream workflows.

## Excluded Candidates

Excluded candidates record known commands/families that are not valid current notebook syntax.

Why this exists:

- prevent accidental reintroduction of outdated assumptions
- keep future/out-of-scope commands from being treated as valid too early
- preserve explicit boundaries between current notebook scope and future workflows

Current examples:

- `fintech-restore-session`: known command, but excluded from current Notebook 02 backup-pack restore syntax.
- `stratlake-trade-engine commands`: excluded until concrete Notebook 03+ workflows confirm and register specific commands.

## Validator Config

`config/notebook_cli_registry.toml` controls validation behavior.

Key fields:

- `registry_path`
- `default_targets`
- `unknown_command_policy`
- `fail_on_invalid_known_command`
- `fail_on_invalid_known_flag`
- `fail_on_invalid_flag_value`
- `fail_on_boolean_flag_value`
- `fail_on_missing_argparse_required`
- `fail_on_missing_notebook_contract_required`
- `safe_help_only`
- `watched_command_prefixes`
- `ignored_command_prefixes`
- `ignored_shell_prefixes`
- `preview_variable_suffixes`

Unknown command policy meanings:

- `warn`: report warning, do not fail.
- `fail`: emit failure.
- `ignore`: do not report unknown watched commands.

## How To Run Registry Validation

Full configured targets:

```bash
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
```

Notebook 02 focused check:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
```

Specific notebook check example:

```bash
python scripts/validate_notebook_cli_registry.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_cli_registry.toml
```

Expected report sections include:

- targets checked
- command examples found
- registry command examples validated
- classification counts
- warnings
- failures

## How To Add A New Command

1. Confirm command/subcommand/flag behavior from approved evidence sources.
2. Add `[[commands]]` and, if needed, `[[command_subcommands]]` entries.
3. Record `owner`, `confirmed_from`, and `upstream_source_status`.
4. Add flags with explicit `kind` and required semantics.
5. Add `unsupported_flags` or `unsupported_patterns` where needed.
6. Add/adjust tests in `tests/test_notebook_cli_registry.py`.
7. Run full registry and repository validation stack.

## How To Update An Existing Command

1. Identify exact upstream or notebook-side change.
2. Update only confirmed fields.
3. Preserve anti-hallucination policy and traceability metadata.
4. Re-check `argparse_required` vs `notebook_contract_required` semantics.
5. Add regression coverage for new valid/invalid examples.
6. Re-run full validation stack before commit.

## How To Handle Upstream CLI Changes

When upstream behavior changes:

1. Verify upstream source/test/docs evidence.
2. Update registry entries and notes with fresh `confirmed_from` references.
3. Add tests for changed behavior and legacy-regression protection.
4. If behavior is uncertain, do not mark as supported yet.
5. Keep excluded candidates/unsupported patterns updated so old assumptions stay blocked.

## How To Handle Unconfirmed Commands or Flags

If evidence is incomplete:

- do not add as supported
- optionally record as excluded candidate with explicit status and notes
- keep uncertainty documented
- wait for implementation/test/docs or notebook-scope confirmation

## Relationship To Other Validation Layers

Validation layers are additive:

- CLI contract validation: broad command-surface and safe-help contract checks; may warn about missing local upstream commands.
- CLI registry validation: argument-aware command/subcommand/flag/value semantics from verified registry; non-executing.
- execution-readiness validation: notebook JSON/state and safe Python syntax checks.
- pytest notebook execution: executes sanitized temporary notebook copies; source notebooks must remain unchanged.
- manual Colab smoke testing: required for runtime-only workflows such as Drive mount, credentials, live archive/restore, ingestion, and session workflows.

## M4/M5 Regression Lessons Preserved

The registry and validator preserve these specific lessons:

- `fintech-init-project --notebooks` is boolean.
- `fintech-init-project --with-session` is boolean.
- boolean flags must not receive explicit values like `""`.
- `fintech-backup-data restore` is the Notebook 02 backup-pack restore path.
- `fintech-backup-data restore --backup-pack-dir` is upstream-required.
- `fintech-backup-data restore --restore-root` is upstream-required.
- `fintech-backup-data restore --overwrite-policy` accepts only `fail`, `replace`, `merge`.
- `refuse` is invalid.
- `--source` is not valid for `fintech-backup-data restore`.
- `fintech-restore-session` is not the current Notebook 02 backup-pack restore command.
- StratLake commands are not valid current notebook syntax until concrete Notebook 03+ workflows confirm and register them.

## Maintenance Checklist

Before adding or changing a registry entry:

- [ ] Confirm the command/subcommand in upstream implementation, tests, docs, or current notebook usage.
- [ ] Record `owner`.
- [ ] Record `confirmed_from`.
- [ ] Distinguish `argparse_required` from `notebook_contract_required`.
- [ ] Use `required_when` for conditional runtime requirements.
- [ ] Use `allowed_values` only for confirmed constrained values.
- [ ] Use `example_values` for examples that should not be enforced.
- [ ] Add unsupported flags/patterns for known-invalid notebook assumptions.
- [ ] Add or update tests in `tests/test_notebook_cli_registry.py`.
- [ ] Run registry validation for all configured notebooks.
- [ ] Run focused validation for any notebook affected by the change.
- [ ] Run full repository validation before commit.

## Full Validation Stack

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml
python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python -m pytest tests/test_notebook_cli_contracts.py
python -m pytest tests/test_notebook_cli_registry.py
python -m pytest tests/test_notebook_execution.py
python -m pytest
```

## Boundaries

Do not use registry maintenance to:

- execute live upstream Fintech or StratLake commands
- run live `--help`
- mount Google Drive
- restore data
- create backup packs
- initialize runtime workspaces
- install packages from notebooks
- mutate source notebooks
- add speculative commands/flags
- expand scope to Notebook 03+ before planned workflow confirmation

The registry is a source-safe, repository-side validation aid, not a runtime execution system.
