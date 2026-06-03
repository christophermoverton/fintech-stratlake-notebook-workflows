# Milestone 5 Merge Readiness

## Milestone Summary

Milestone 5 - CLI Command Registry and Argument-Aware Notebook Validation added a verified, traceable CLI registry layer for notebook command examples and integrated it into the repository validation stack.

Milestone 5 delivered:

- a source-traceable CLI command registry
- a non-executing argument-aware registry validator
- focused regression tests for registry and validator behavior
- validation-stack integration in repository documentation
- a dedicated registry maintenance guide

Milestone 5 is additive and does not replace:

- CLI contract validation
- execution-readiness validation
- sanitized pytest notebook execution
- manual Colab smoke testing

## Principle Preserved

Notebook command validation should verify command syntax and argument semantics against confirmed upstream command surfaces without executing live runtime workflows or weakening source-only notebook boundaries.

## Completed Issues

| Issue | Title | Outcome |
|---|---|---|
| #39 / M5.1 | Define CLI Command Registry Contract | Added `config/cli_command_registry.toml` with traceable command/subcommand/flag schema, required-flag semantics, unsupported patterns, and excluded candidates. |
| #40 / M5.2 | Add Argument-Aware CLI Registry Validator | Added `scripts/validate_notebook_cli_registry.py` and `config/notebook_cli_registry.toml` for non-executing notebook command validation. |
| #41 / M5.3 | Add CLI Registry Tests | Added `tests/test_notebook_cli_registry.py` with focused registry/validator regression coverage (39 tests). |
| #42 / M5.4 | Integrate Registry Validation into Notebook Validation Stack | Updated README and notebook docs so registry validation runs between CLI contract and execution-readiness checks. |
| #43 / M5.5 | Add CLI Registry Documentation and Maintenance Guide | Added `docs/cli_command_registry.md` with schema, policy, maintenance workflow, and layer relationship guidance. |
| #44 / M5.6 | Milestone 5 Validation and Merge Readiness | Added this closeout and reran the full repository validation stack with current results. |

## Files Added Or Updated

Core registry/config:

- `config/cli_command_registry.toml`
- `config/notebook_cli_registry.toml`

Validator:

- `scripts/validate_notebook_cli_registry.py`

Tests:

- `tests/test_notebook_cli_registry.py`

Docs:

- `docs/cli_command_registry.md`
- `docs/milestone_5_merge_readiness.md`
- `README.md`
- `docs/notebook_development_environment.md`
- `docs/notebook_index.md`
- `docs/milestone_4_merge_readiness.md`

## Registry Schema Summary

The registry includes:

- schema metadata and accuracy policy
- ownership metadata (`owner`)
- expected-missing-local behavior (`expected_missing_local`)
- command classifications
- source traceability via `confirmed_from`
- command entries
- subcommand entries
- flag entries
- excluded candidates
- unsupported flags
- unsupported patterns

Required-flag semantics are explicit:

- ambiguous `required = true/false` is intentionally not used
- `argparse_required` means upstream parser requirement
- `notebook_contract_required` means current notebook/contract expectation
- `required_when` means conditional runtime requirement

## Commands And Subcommands Covered

Valid current notebook command surfaces:

- `fintech-init-project`
- `fintech-backfill-daily`
- `fintech-save-session`
- `fintech-backup-data`
- `fintech-backup-data pack`
- `fintech-backup-data validate`
- `fintech-backup-data inspect`
- `fintech-backup-data restore`

Excluded or out-of-scope candidates:

- `fintech-restore-session` is upstream-confirmed as a separate command but excluded from valid current notebook backup-pack restore syntax.
- StratLake commands are excluded from valid current notebook syntax because current imported notebooks do not reference a concrete StratLake CLI command.

## Validator Behavior Summary

`scripts/validate_notebook_cli_registry.py`:

- loads `config/notebook_cli_registry.toml`
- loads `config/cli_command_registry.toml`
- validates notebook shell examples and conservative command-preview variables
- checks known commands and subcommands
- checks supported flags and rejects unsupported/unknown flags
- catches boolean flags receiving values
- catches value flags missing values
- enforces `allowed_values`
- enforces `argparse_required`
- enforces `notebook_contract_required`
- enforces `required_when = "not_dry_run"`
- rejects excluded candidates
- classifies examples as `safe_help`, `safe_preview`, `dry_run`, `manual_only_live`, or `unsafe_live`
- produces deterministic report output and exit codes
- does not execute upstream commands

## Test Coverage Summary

`tests/test_notebook_cli_registry.py` adds 39 tests covering:

- registry TOML parsing
- registry model construction
- expected commands/subcommands
- excluded candidates
- no ambiguous plain `required`
- required-flag semantics
- valid command examples
- invalid command examples
- help handling
- unknown command policy behavior
- ignored setup command handling
- current notebook validation
- Notebook 02-specific validation
- source-notebook non-mutation
- subprocess smoke checks

## Documentation Updates

Milestone 5 documentation updates include:

- README validation stack updates with registry validator placement and layer distinctions
- `docs/notebook_development_environment.md` updates with a CLI Registry Validation section and validation-layer roles
- `docs/notebook_index.md` updates with `cli_registry_validated` status and expanded validation commands
- `docs/milestone_4_merge_readiness.md` additive M5 validation-stack note
- `docs/cli_command_registry.md` as the dedicated schema/policy/maintenance guide

## M4/M5 Regression Lessons Preserved

- `fintech-init-project --notebooks` is a standalone boolean flag.
- `fintech-init-project --with-session` is a standalone boolean flag.
- Boolean flags must not receive explicit values like `""`.
- `fintech-backup-data restore` is the Notebook 02 backup-pack restore path.
- `fintech-backup-data restore --backup-pack-dir` is upstream-required.
- `fintech-backup-data restore --restore-root` is upstream-required.
- `fintech-backup-data restore --overwrite-policy` accepts only `fail`, `replace`, `merge`.
- `refuse` is invalid.
- `--source` is not valid for `fintech-backup-data restore`.
- `fintech-restore-session` is not the current Notebook 02 backup-pack restore command.
- StratLake commands are not valid current notebook syntax until concrete Notebook 03+ workflows confirm and register them.

## Invalid Command Patterns Now Caught

Examples now caught by registry validation and test coverage include:

- `fintech-init-project --notebooks ""`
- `fintech-init-project --with-session ""`
- `fintech-backup-data restore --overwrite-policy refuse`
- `fintech-backup-data restore --source ...`
- `fintech-backup-data restore` missing `--backup-pack-dir`
- `fintech-backup-data restore` missing `--restore-root`
- `fintech-backup-data restore --unknown-flag ...`
- `fintech-backup-data restore --backup-pack-dir --restore-root ...`
- `fintech-restore-session --overwrite-policy ...`
- concrete StratLake command examples before confirmation and registration

## Validation Commands And Results

Validation stack run for this closeout:

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

| Command | Result |
|---|---|
| `python scripts/scan_for_secret_patterns.py .` | Passed; secret pattern scan clean. |
| `python scripts/check_notebooks_no_outputs.py notebooks` | Passed; checked 3 notebooks. |
| `python scripts/validate_repo_cleanliness.py .` | Passed. |
| `python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml` | Passed; 3 notebook targets, 24 command examples, 0 failures. |
| `python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml` | Passed; 3 notebook targets, 22 command examples, 0 failures. |
| `python scripts/validate_notebook_cli_registry.py notebooks/02_fintech_session_persistence_save_restore.ipynb --config config/notebook_cli_registry.toml` | Passed; 1 notebook target, 7 command examples, 0 failures. |
| `python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml` | Passed; 3 notebooks checked, 45 code cells checked, 24 compiled, 21 skipped, 0 failures. |
| `python -m pytest tests/test_notebook_cli_contracts.py` | Passed; 13 tests passed. |
| `python -m pytest tests/test_notebook_cli_registry.py` | Passed; 39 tests passed. |
| `python -m pytest tests/test_notebook_execution.py` | Passed; 14 tests passed. |
| `python -m pytest` | Passed; 66 tests passed. |

## Known Expected Warnings

Expected warning categories observed:

- Missing local upstream Fintech CLI command warnings from CLI contract validation:
  - `fintech-init-project`
  - `fintech-backfill-daily`
  - `fintech-save-session`
  - `fintech-backup-data`
- Existing Notebook 00 `nbformat` `MissingIDFieldWarning`.
- Existing Windows ZMQ/tornado runtime warning during sanitized notebook execution.

These warnings are non-blocking and do not indicate unsafe execution, notebook mutation, or committed runtime artifacts.

## Source Hygiene And Boundary Confirmation

Closeout confirms:

- source notebooks were not mutated
- notebooks remain output-free
- execution counts remain null
- no generated data was committed
- no restored data was committed
- no backup/archive packs were committed
- no manifests were committed
- no Drive artifacts were committed
- no credentials were committed
- no private paths were committed
- no runtime state was committed
- no live upstream Fintech or StratLake CLI commands were executed
- no live `--help` commands were executed by the registry validator
- no Drive mount occurred
- no data restore occurred
- no archive/backup-pack creation occurred
- no runtime workspace initialization occurred

## Non-Goals / Deferred Work

- Notebook 03+ workflows remain deferred.
- StratLake CLI command registration remains deferred until concrete notebook usage is introduced and upstream commands are confirmed.
- Broad Python expression/list extraction in the registry validator remains intentionally conservative.
- Registry does not attempt exhaustive upstream CLI option coverage.
- Manual Colab smoke testing remains required for runtime-only workflows.
- Registry does not replace upstream CLI parser tests or implementation tests.

## Final Merge Readiness Recommendation

Final status: ready_for_review_or_merge

Conditions satisfied:

- full validation stack passed
- additive validation layers remain intact
- source-only notebook boundaries remain intact
- no runtime artifacts or sensitive data were committed