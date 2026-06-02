# Notebook 01 Staging and Classification

## Summary

This document records the M3.1 staging and classification foundation for Notebook 01 before cleanup, validation, audit, and import work begins.

Notebook 01 is classified as a Fintech daily bars extraction/backfill workflow.

The reviewed source candidate is the attached Notebook 01 local download in the user's Downloads folder.

This source notebook remains outside the repository. It must not be copied into `notebooks/` until the M3.2 cleanup, validation, and audit work is complete.

## Staging Decision

| Field | Decision |
|---|---|
| Planned repository filename | `01_fintech_daily_bars_extraction_backfill.ipynb` |
| Workflow classification | Fintech daily bars extraction/backfill workflow |
| Primary upstream app | `fintech-market-ingestion` |
| Secondary upstream app | None expected for Notebook 01 |
| Staging category | `cleaned` |
| Import status | `pilot_imported`, `imported_pending_audit`; manual Colab smoke pending |
| Local validation status | Cleanup validation passed; CLI contract validation added; execution-readiness and sanitized pytest coverage added |
| Manual Colab smoke status | Pending after cleanup/import validation |

The source candidate is useful and aligned with the planned Notebook 01 workflow, but the original runtime capture was not import-ready because it contained committed outputs. The source review found 42 cells, 19 code cells, 14 code cells with outputs, and no non-null execution counts. Issue #20 prepared a cleaned candidate at `notebooks/01_fintech_daily_bars_extraction_backfill.ipynb`; Issue #23 confirmed it as the controlled Notebook 01 pilot import. The original runtime capture remains outside the repository.

## Expected Notebook Role

Notebook 01 should orient a Colab user through the Fintech daily bars extraction/backfill workflow while preserving the repository boundary:

- Provide session/setup orientation for the extraction workflow.
- Install or locate the upstream Fintech app in the Colab runtime.
- Preview required command availability with safe help/version checks.
- Define a local `/content` Fintech workspace for active work.
- Use Google Drive only for persistence, backup, archive, and restore storage.
- Configure Alpaca credentials through Colab Secrets or safe hidden prompts.
- Run or preview native Fintech daily bars extraction/backfill commands.
- Validate generated daily bars outputs as runtime artifacts.
- Hand off generated data, session persistence, backup, or restore notes without committing generated artifacts.
- Support manual Colab smoke testing after local repository validation.

Notebook 01 must remain an orchestration, validation, parsing, display, and review layer. It must not reimplement native Fintech ingestion logic.

## Expected Notebook Sections

The cleaned Notebook 01 should contain these sections, with source-specific text updated during M3.2:

| Section | Expected content | M3.2 cleanup notes |
|---|---|---|
| Reusable header and purpose | Standard Notebook 01 title, purpose, workflow role, upstream app declaration, generated artifact boundaries, and validation commands. | Replace standalone header with the repository header pattern. |
| Prerequisites | Colab runtime, upstream Fintech package/install expectation, Alpaca credential requirement, and generated data boundary. | Keep package install cells safe and reviewable. |
| Upstream app setup | Install or locate `fintech-market-ingestion` and verify native CLIs. | Prefer safe package/version/help checks where possible. |
| Local workspace setup | Define `WORKSPACE_ROOT` under `/content/fintech-market-ingestion-demo`. | Keep active app work under `/content`. |
| Environment/secrets guidance | Use Colab Secrets first, hidden prompt fallback second, and placeholder secret names only. | Remove any printed secret truthiness if it is unnecessary or could encourage logging. |
| Extraction/backfill examples | Use native `fintech-backfill-daily` command examples. | Live/API execution should be excluded from local validation. |
| Validation/QA examples | Inspect expected daily bars runtime outputs and summarize file counts or paths after execution. | Outputs must be cleared before import. |
| Generated data boundary notes | Generated Parquet/data files remain runtime-only and out of Git. | Make this explicit near command cells. |
| Persistence/archive handoff notes | Session save and backup commands may be previewed, with live writes kept optional and runtime-only. | Keep save/archive/restore writes commented or dry-run-first. |
| Cleanup-before-commit checklist | Output clearing, null execution counts, secret scan, path review, generated artifact review, and validation commands. | Add an explicit import gate at the end. |

## CLI Command Inventory

| Command or command family | Expected notebook use | Category | Local validation expectation |
|---|---|---|---|
| `python -m pip install --upgrade pip` | Prepare Colab package tooling. | Manual Colab-only live/runtime setup command | Excluded from local validation. |
| `python -m pip install "pandas-market-calendars>=5.0"` | Install runtime dependency. | Manual Colab-only live/runtime setup command | Excluded from local validation. |
| `python -m pip install -i https://test.pypi.org/simple/ fintech-market-ingestion` | Install upstream app in Colab runtime. | Manual Colab-only live/runtime setup command | Excluded from local validation. |
| `shutil.which(...)` checks for Fintech commands | Report whether required CLIs are available. | Safe local command | Safe as static/source logic; no upstream execution required. |
| `fintech-init-project --help` | Verify command availability and usage. | Help/version command | Safe for CLI contract validation when installed; expected missing upstream command warning otherwise. |
| `fintech-backfill-daily --help` | Verify daily bars backfill usage. | Help/version command | Safe for CLI contract validation when installed; expected missing upstream command warning otherwise. |
| `fintech-save-session --help` | Verify session save usage. | Help/version command | Safe for CLI contract validation when installed; expected missing upstream command warning otherwise. |
| `fintech-backup-data --help` | Verify backup/archive usage. | Help/version command | Safe for CLI contract validation when installed; expected missing upstream command warning otherwise. |
| `drive.mount("/content/drive")` | Mount Google Drive for persistence storage. | Manual Colab-only live/API command | Excluded from local validation. |
| `fintech-init-project --root ... --notebooks --with-session --session-name ...` | Initialize local Fintech demo/session workspace. | Manual Colab-only runtime mutation command | Excluded from local validation. |
| Session manifest parsing with `json` and `pathlib` | Read local runtime session metadata. | Safe local command family when run against test fixtures | Not added to local execution coverage until cleaned and sanitized. |
| Drive session directory creation with `mkdir(...)` | Prepare Drive persistence folders. | Manual Colab-only runtime mutation command | Excluded from local validation. |
| Colab Secrets / `getpass` credential setup | Load Alpaca credentials. | Manual Colab-only credential command family | Excluded from local validation. |
| `fintech-backfill-daily --symbols ... --start ... --end ... --out ... --feed ... --source ... --window ...` | Run daily bars extraction/backfill against Alpaca. | Manual Colab-only live/API command | Excluded from local validation. |
| Daily bars Parquet inspection with `Path.rglob("*.parquet")` | Summarize generated runtime files. | Safe local command family when run against test fixtures | Not added to local execution coverage until cleaned and sanitized. |
| `fintech-save-session ... --include-curated-data --dry-run` | Preview session save to Drive. | Dry-run/preview command | May be documented, but excluded from local validation unless upstream CLI contract is configured safely. |
| Commented `fintech-save-session ... --include-curated-data` | Optional live session save. | Manual Colab-only live/runtime command | Excluded from local validation. |
| `fintech-backup-data pack ... --dry-run` | Preview archive backup pack creation. | Dry-run/preview command | May be documented, but excluded from local validation unless upstream CLI contract is configured safely. |
| Commented `fintech-backup-data pack ...` | Optional live archive pack creation. | Manual Colab-only live/runtime command | Excluded from local validation. |
| Commented `fintech-backup-data validate ...` | Validate an archive pack after runtime creation. | Manual Colab-only runtime command | Excluded from local validation. |
| Printed `fintech-backup-data restore ...` template | Show restore command without execution. | Dry-run/preview command | Safe as a command preview only. |

If the upstream app is not installed locally, help/contract checks for `fintech-init-project`, `fintech-backfill-daily`, `fintech-save-session`, and `fintech-backup-data` may emit expected missing-command warnings. Those warnings are acceptable only when the validator is configured to treat missing upstream commands as warnings.

## Risk Inventory

| Risk | Notebook 01 relevance | Required mitigation before import |
|---|---|---|
| Committed notebook outputs | Source candidate currently has outputs in 14 code cells. | Clear all outputs before import. |
| Non-null execution counts | Source candidate currently has null execution counts. | Confirm all code cells remain `null` after cleanup. |
| Generated Parquet/data files | Daily bars backfill writes Parquet output under runtime data roots. | Do not commit generated data; document runtime-only boundary. |
| Local app workspaces | Fintech workspace is created under `/content/fintech-market-ingestion-demo`. | Do not copy workspaces into Git. |
| Archives or restore packs | Optional backup pack and restore command examples are present. | Keep live archive/restore actions runtime-only; do not commit packs. |
| Private Google Drive paths | Source used a concrete mounted Drive project path and outputs included session-specific Drive paths. | Replace or document as portable placeholders; clear outputs containing Drive session paths. |
| Private usernames or machine paths | Source file lives in a local Downloads path. | Keep source path only in staging doc; do not import source from Downloads directly. |
| `.env` values | Upstream help/output references `.env.example`; live `.env` values must not appear. | Search raw JSON for `.env` values; keep credential values out of source. |
| API keys | Alpaca key names are used. | Use placeholder secret names only; never commit literal key values. |
| Credential JSON | Not expected for Notebook 01. | Block import if any credential JSON appears in source, metadata, or outputs. |
| Tokens/secrets | Credential setup prompts for Alpaca secrets. | Use Colab Secrets or hidden prompts; do not print or display secret values. |
| Live API execution in local tests | Backfill command can call Alpaca APIs. | Exclude live/API cells from local validation and pytest execution. |
| Drive mount in local tests | `drive.mount` is Colab-only. | Exclude Drive mount cells from local validation and pytest execution. |
| Accidental reimplementation of upstream Fintech ingestion logic | Notebook includes native CLI command usage; no reimplementation should be added. | Preserve native-command-first boundary during cleanup. |

## Go/No-Go Checklist for M3.2 Cleanup

| Gate | Status |
|---|---|
| Notebook 01 source/staging location identified. | Go |
| Workflow role confirmed as Fintech daily bars extraction/backfill. | Go |
| Unsafe commands identified. | Go |
| CLI command inventory drafted. | Go |
| Generated data risks identified. | Go |
| Secret/path risks identified. | Go |
| Local validation constraints documented. | Go |
| Import deferred until cleanup, validation, audit, and review work is complete. | Go |

Go result: Notebook 01 may proceed through M3.2 cleanup validation. The cleaned candidate may remain under `notebooks/` only if outputs are cleared, raw JSON is reviewed, source is made portable, and cleanup validation passes. Full validation expansion, import audit, and manual Colab smoke testing remain later follow-up work.

## Future Staging Pattern

Future notebook files should be staged for addition with the same controlled flow:

1. Keep the candidate notebook outside the repository, such as a local or Drive `notebook_import_staging/needs_cleanup/` folder.
2. Record the source location and classification in a per-notebook staging document.
3. Inventory command families before cleanup and mark live/API, Drive mount, archive, restore, and credential flows as excluded from local validation.
4. Identify output, execution count, generated data, private path, and secret risks before moving the file.
5. Clean a copy of the notebook, not the original runtime capture.
6. Move only the cleaned, output-free, reviewed notebook into `notebooks/`.
7. Run repository validation and record an import audit before treating the notebook as imported.

This keeps each future notebook addition reviewable and prevents direct Google Drive or runtime captures from entering Git.

## Non-Goals for M3.1

- Do not import Notebook 01 into `notebooks/`.
- Do not clean Notebook 01 yet, except to document cleanup needs.
- Do not add Notebook 01 to pytest execution coverage.
- Do not update CLI contract config for Notebook 01 yet.
- Do not run live ingestion.
- Do not mount Google Drive in local tests.
- Do not add generated Parquet/data, archives, restore packs, or runtime folders.
- Do not broaden scope to Notebook 02 or later notebooks.
