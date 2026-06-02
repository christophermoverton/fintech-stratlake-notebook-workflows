# Notebook Index and Import Status Tracker

## Purpose

This tracker records which notebooks are imported, which notebooks are pending import, what each notebook's workflow role is, and what validation or audit status is known.

The tracker is a review surface, not an automated source of generated truth. It should help future notebook imports remain controlled, staged, cleaned, validated, audited, and artifact-free.

## Relationship to Controlled Import

Notebook imports should move through staging, cleanup, validation, audit, and review before entering `notebooks/`.

Use this tracker with:

- [Notebook Import Staging Guide](notebook_import_staging.md)
- [Notebook Cleanup Workflow](notebook_cleanup_workflow.md)
- [Reusable Notebook Header Template](notebook_header_template.md)
- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)
- [Notebook Development Environment](notebook_development_environment.md)
- [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md)
- [Notebook 00 Import Audit](notebook_00_import_audit.md)
- [Notebook 01 Import Audit](notebook_01_import_audit.md)

Do not use this tracker to justify direct imports from Google Drive. Future notebooks should remain outside the repository until they are staged, cleaned, validated, reviewed, and explicitly moved into `notebooks/`.

## Current Imported Notebooks

| Number | Title | Repository path | Workflow role | Upstream app coverage | Import status | Validation status | Audit record | Manual Colab smoke | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 00 | Setup and Storage Overview | [notebooks/00_setup_and_storage_overview.ipynb](../notebooks/00_setup_and_storage_overview.ipynb) | setup/storage/session/persistence overview | `fintech-market-ingestion`; references StratLake boundaries where relevant | `imported` | `cleaned`, `static_validated`, `readiness_validated`, `pytest_validated`, `cli_contract_validated`, `audit_recorded` | [Notebook 00 import audit](notebook_00_import_audit.md) | `pending` | First pilot import; final Colab runtime confirmation remains pending. |
| 01 | Fintech Daily Bars Extraction/Backfill | [notebooks/01_fintech_daily_bars_extraction_backfill.ipynb](../notebooks/01_fintech_daily_bars_extraction_backfill.ipynb) | extraction/backfill | `fintech-market-ingestion` | `pilot_imported`, `imported` | `cleaned`, `static_validated`, `readiness_validated`, `pytest_validated`, `cli_contract_validated`, `audit_recorded` | [Notebook 01 import audit](notebook_01_import_audit.md) | `passed-with-notes` | Core Colab smoke passed; Issue #27 fixes Drive placeholder syntax before dry-run preview cells are rerun for full pass. |

Notebook 00 and Notebook 01 are the imported notebooks currently tracked by this repository.

## Import Status Table

| Status | Meaning |
|---|---|
| `imported` | Notebook exists under `notebooks/`, is cleaned, output-free, tracked, and has passed repository validation. |
| `pilot_imported` | Notebook exists under `notebooks/` as a controlled pilot import and has passed the repository-side checks recorded for its milestone issue. |
| `imported_pending_audit` | Notebook exists under `notebooks/` and has passed repository-side validation, but its import audit record is not complete yet. |
| `pending_staging` | Candidate notebook exists outside the repo or is planned, but has not yet gone through staging and cleanup. |
| `needs_cleanup` | Candidate notebook has useful content but contains outputs, runtime state, paths, logs, blobs, or other cleanup needs. |
| `needs_rewrite` | Candidate notebook contains useful workflow intent but should be rewritten before import. |
| `upstream_triage_needed` | Notebook exposes behavior likely requiring changes or investigation in `fintech-market-ingestion` or `stratlake-trade-engine`. |
| `blocked` | Import is waiting on another issue, upstream command, validation workflow, or design decision. |
| `do_not_import` | Notebook or content should not be imported into this repo. |

## Validation Stage Table

| Stage | Meaning |
|---|---|
| `not_started` | No staging, cleanup, or validation has been recorded. |
| `staged` | Notebook has been copied to a staging location outside the repository. |
| `cleaned` | Outputs, execution counts, runtime metadata, private paths, and unsafe captured state have been reviewed and removed where needed. |
| `static_validated` | Repository static checks passed, including secret scan, notebook output check, and repository cleanliness validation. |
| `readiness_validated` | TOML-backed notebook execution-readiness validation passed. |
| `pytest_validated` | Sanitized pytest notebook execution passed without mutating source notebooks. |
| `cli_contract_validated` | Notebook CLI examples passed CLI contract validation. Missing local upstream commands may be warnings when configured. |
| `audit_recorded` | A notebook import audit record exists. |
| `colab_smoke_pending` | Manual Colab runtime smoke validation remains pending. |
| `colab_smoke_passed_with_notes` | Manual Colab runtime smoke validation found the core workflow working but recorded follow-up notes before full pass. |
| `colab_smoke_passed` | Manual Colab runtime smoke validation has been completed and recorded. |

Validation status may include multiple markers for the same notebook. Do not claim `colab_smoke_passed` unless a fresh Colab smoke test was actually completed.

## Pending Notebook Candidates

These are planned workflow categories only. They are not imported, cleaned, validated, audited, or confirmed runnable.

| Candidate | Workflow role | Expected upstream coverage | Import status | Validation status | Notes |
|---|---|---|---|---|---|
| Session persistence workflow | session persistence | `fintech-market-ingestion` | `pending_staging` | `not_started` | May align with planned Notebook 02. |
| Archive backup pack workflow | archive | `fintech-market-ingestion` | `pending_staging` | `not_started` | Must avoid committing archive packs or generated data. |
| Archive restore workflow | restore | `fintech-market-ingestion` | `pending_staging` | `not_started` | Restore execution should remain runtime-only. |
| StratLake initialization workflow | StratLake initialization | `stratlake-trade-engine` | `pending_staging` | `not_started` | Should use native StratLake setup commands where available. |
| Feature generation workflow | feature generation | `stratlake-trade-engine`; Fintech curated data inputs | `pending_staging` | `not_started` | Must not reimplement feature generation logic. |
| Validation / QA workflow | validation | both upstream apps as needed | `pending_staging` | `not_started` | Should validate and review runtime outputs without committing them. |
| Strategy smoke-test workflow | strategy smoke test | `stratlake-trade-engine` | `pending_staging` | `not_started` | Must use native strategy/CLI behavior where available. |
| Backtest review workflow | backtest review | `stratlake-trade-engine` | `pending_staging` | `not_started` | Must not reimplement backtesting or artifact generation. |
| Research comparison workflow | research comparison | `stratlake-trade-engine` | `pending_staging` | `not_started` | Should review native comparison outputs only. |
| Audit/review workflow | audit/review | repository workflow layer | `pending_staging` | `not_started` | Future audits should follow the Notebook 00 audit pattern. |

## Non-Importable and Do-Not-Import Categories

Do not import notebooks or content that:

- Contains real secrets, tokens, `.env` values, credential JSON, or private keys.
- Contains notebook outputs, execution state, tracebacks, logs, screenshots, or embedded output blobs that cannot be safely cleaned.
- Contains generated data, archive packs, restore packs, local app workspaces, runtime folders, or copied Google Drive exports.
- Depends on private local files, private Drive paths, usernames, or account-specific details.
- Reimplements native Fintech ingestion, StratLake feature generation, archive/restore, strategy, backtest, or artifact logic.
- Is obsolete, redundant, scratch-only, unsafe, or too stale to preserve.

Use `do_not_import`, `needs_rewrite`, or `upstream_triage_needed` instead of forcing unsafe content into `notebooks/`.

## Future Update Rules

Update this tracker when:

- A notebook is staged for review.
- A notebook moves between readiness categories.
- A notebook is imported into `notebooks/`.
- A notebook passes static validation, readiness validation, pytest validation, CLI contract validation, audit recording, or manual Colab smoke testing.
- A notebook is blocked, rejected, or moved to `do_not_import`.

Before marking a notebook `imported`, confirm:

- It exists under `notebooks/`.
- Outputs are cleared.
- Execution counts are `null`.
- Raw `.ipynb` JSON has been reviewed.
- Secrets and private paths are absent.
- Generated data and runtime artifacts are absent.
- Native-command-first boundaries are respected.
- Validation commands pass.
- An audit record exists or is planned in the same import sequence.

## Validation Commands Before Status Changes

Run these commands before marking a notebook as imported or advancing validation status:

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
pytest
```

Use explicit notebook target forms when reviewing a specific notebook:

```bash
python scripts/validate_notebook_execution_readiness.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_test.toml
python scripts/validate_notebook_cli_contracts.py notebooks/00_setup_and_storage_overview.ipynb --config config/notebook_cli_contracts.toml
```

Manual Colab smoke validation should follow [Colab Smoke-Test Workflow](colab_smoke_test_workflow.md). Keep Colab outputs, logs, screenshots, tracebacks, and generated artifacts out of Git.
