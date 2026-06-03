# Notebook 02 Staging and Classification

## Summary

This document records the M4.1 staging and classification foundation for Notebook 02 before cleanup, validation, audit, and import work begins.

Notebook 02 is planned as the Fintech session persistence save/restore workflow.

The reviewed source candidate is the attached Notebook 02 local download in the user's Downloads folder. The original runtime-captured source notebook remains outside the repository. This issue does not import a cleaned Notebook 02 source file into `notebooks/`.

Milestone 4 starts the next one-notebook controlled import after Notebook 01. It should preserve the same staged import, cleanup before commit, CLI contract validation, execution-readiness validation, sanitized pytest coverage, import audit, notebook index update, artifact-free repository boundary, and native-command-first discipline established by Milestone 3.

## Candidate Notebook Identity

| Field | Decision |
|---|---|
| Planned repository path | `notebooks/02_fintech_session_persistence_save_restore.ipynb` |
| Workflow classification | Fintech session persistence save/restore workflow |
| Primary upstream app | `fintech-market-ingestion` |
| Secondary upstream app | None expected unless later review finds otherwise |
| Relationship to Notebook 00 | Builds on setup, session initialization, and storage overview conventions |
| Relationship to Notebook 01 | Persists and restores a session after extraction/backfill workflow state exists |
| Staging category | `needs_cleanup` |
| Import status | `pending_staging`; no notebook source import performed |
| Local validation status | Not started for Notebook 02 source; M4.1 is documentation/classification only |
| Manual Colab smoke status | Not started |

The source candidate is useful and aligned with the planned Notebook 02 workflow, but the original runtime capture is not import-ready. Source review found 49 cells, 21 code cells, 18 code cells with outputs, and 18 code cells with non-null execution counts. A cleaned copy must be prepared in M4.2 before any Notebook 02 source enters `notebooks/`.

## Expected Notebook Role

Notebook 02 should orient a Colab user through lightweight Fintech session persistence and recovery while preserving the repository boundary:

- Preserve or check the active `SESSION_ID`.
- Review local Colab workspace and session paths under `/content`.
- Use native Fintech session save command examples.
- Use native Fintech session restore command examples when available.
- Use Google Drive as persistence and restore storage only.
- Verify session metadata or restored state through lightweight review cells.
- Document generated-session boundaries and runtime-only outputs.
- Hand off archive pack and larger restore workflows to Notebook 03.

Notebook 02 must remain an orchestration, validation, parsing, display, and review layer. It must not reimplement native Fintech session persistence, archive, restore, ingestion, or generated artifact logic.

## Scope Classification

Notebook 02 should focus on session persistence and restore readiness, not full archive backup/restore.

In scope:

- Checking or extracting `SESSION_ID` from the active local Fintech session.
- Reviewing local `/content` workspace paths and session metadata.
- Preparing Google Drive session-persistence folders with shell-safe placeholders.
- Previewing native Fintech session save command help and command templates.
- Previewing native Fintech session restore command help and command templates if the upstream CLI exposes them.
- Running actual save/restore only as manual Colab runtime cells, never in local repository validation.
- Reviewing saved or restored session metadata with lightweight checks after runtime execution.
- Stating which generated session payloads, restore outputs, runtime folders, logs, and notebook outputs must stay out of Git.

Out of scope:

- Full archive backup pack creation.
- Full archive restore execution.
- Archive shard or package inspection.
- Archive transfer workflows.
- Restore-pack execution workflows.
- Reimplementing upstream Fintech persistence behavior in notebook cells.

## Explicit Deferrals

Notebook 02 should not become the full archive pack/restore notebook.

Defer to likely Notebook 03:

- Full archive backup pack workflow.
- Full archive restore workflow.
- Archive shard/package inspection.
- Archive transfer workflow.
- Restore-pack execution workflow.

Notebook 02 may include safe dry-run, help, or preview references that bridge to Notebook 03 only when they clarify boundaries. Those references should not expand Milestone 4 beyond session persistence save/restore.

## Expected Notebook Sections

The cleaned Notebook 02 should likely contain these sections, with source-specific text updated during M4.2:

| Section | Expected content | M4.2 cleanup notes |
|---|---|---|
| Reusable header and scope | Standard Notebook 02 title, purpose, workflow role, upstream app declaration, generated artifact boundaries, and validation commands. | Use the repository header pattern and planned filename. |
| Prerequisite relationship | Explain dependency on Notebook 00 setup/storage conventions and Notebook 01 extraction/backfill session state. | Do not imply Notebook 02 can create extraction outputs by itself. |
| Runtime environment checks | Confirm Colab runtime expectations, upstream command availability, and local `/content` workspace assumptions. | Keep checks static or help/preview-oriented where possible. |
| `SESSION_ID` check or extraction | Preserve the active session identity from local runtime metadata or a shell-safe placeholder. | Avoid committing captured session values from a prior runtime. |
| Local `/content` workspace checks | Review Fintech root, session manifest paths, and expected local state. | Do not commit local workspace contents or file listings with generated payloads. |
| Google Drive mount/manual persistence setup | Mount Drive only in manual Colab runtime cells. | Exclude from local validation and sanitized pytest execution. |
| Drive folder placeholder setup | Use shell-safe placeholders such as `REPLACE_WITH_DRIVE_FOLDER_NAME`. | Do not use angle-bracket placeholders inside shell-interpolated paths. |
| Command help/preview cells | Show native session save/restore command help and safe command previews. | Mark uncertain command names for upstream confirmation. |
| Session save workflow | Use native session save command examples to persist selected state to Drive. | Actual writes are manual Colab-only runtime commands. |
| Session restore workflow | Use native restore command examples if available to restore selected session state from Drive. | Actual restore is manual Colab-only and must not run locally. |
| Restored session verification/review | Review session metadata, restored path existence, or small summaries after runtime restore. | Avoid broad generated data inspection or archive payload display. |
| Cleanup/artifact boundary notes | State outputs, counts, payloads, restore outputs, archives, and runtime folders must not be committed. | Enforce before import. |
| Next-step handoff | Direct full archive backup/restore work to Notebook 03. | Keep Notebook 02 scope narrow. |

## Expected Native Command Inventory

The following command inventory should be validated during M4.2 and wired into M4.3 CLI contract validation only where safe. Do not treat uncertain command names or flags as guaranteed upstream behavior until they are confirmed against the current `fintech-market-ingestion` CLI.

| Command or command family | Expected notebook use | Category | Local validation expectation |
|---|---|---|---|
| `fintech-save-session --help` | Verify session save command availability and usage. | Safe help/version command | Safe for CLI contract validation when installed; expected missing upstream command warning otherwise. |
| `fintech-save-session ... --dry-run` | Preview session save destination and selected runtime state. | Dry-run/preview command | Candidate for source/contract validation only if upstream dry-run behavior is confirmed safe. |
| Commented `fintech-save-session ...` | Actual session save to Drive. | Manual Colab-only runtime command | Excluded from local validation and sanitized pytest execution. |
| Restore/session restore command help | Verify session restore command availability if upstream exposes a dedicated restore CLI. | Safe help/version command, command name uncertain | Requires confirmation against current upstream CLI before contract validation. |
| Restore/session restore dry-run or preview command | Preview restore from Drive back to local `/content` workspace if upstream supports it. | Dry-run/preview command, command name uncertain | Candidate for source/contract validation only after upstream confirmation. |
| Commented restore/session restore execution | Actual restore from Drive to local runtime workspace. | Manual Colab-only runtime command | Excluded from local validation and sanitized pytest execution. |
| Session inspection or metadata command help | Verify metadata or session inspection command availability if upstream exposes one. | Safe help/version command, command name uncertain | Requires confirmation against current upstream CLI before contract validation. |
| Lightweight metadata/path review with `json` and `pathlib` | Review local session metadata or restored state after runtime actions. | Safe local code when fixture-backed or static | May be sanitized in pytest later; should not require real generated runtime state locally. |
| `drive.mount("/content/drive")` | Mount Drive for persistence and restore storage. | Manual Colab-only live/API command | Excluded from local validation and sanitized pytest execution. |

Known command names from earlier notebooks include `fintech-save-session` and `fintech-backup-data`. Notebook 02 should not assume a dedicated restore or metadata CLI name until M4.2/M4.3 confirms current upstream help output. If no dedicated restore command exists, the notebook should document that finding and avoid inventing behavior.

If the upstream app is not installed locally, help/contract checks for Fintech commands may emit expected missing-command warnings. Those warnings are acceptable only when the validator is configured to treat missing upstream commands as warnings.

## Runtime-Only Command Classification

These commands and command families must remain manual Colab-only unless a later issue proves a safe local fixture path:

- Google Drive mount.
- Credential setup.
- Actual session save to Drive.
- Actual restore from Drive.
- Commands requiring existing generated local runtime state.
- Commands that create session payloads.
- Commands that create restore outputs.
- Commands that create archive packs.
- Commands that create generated data.
- Commands that inspect broad generated data trees or archive contents.

Local repository validation must not mount Drive, prompt for credentials, require network access, call live APIs, create generated runtime state, write session payloads, restore outputs, archive packs, or mutate upstream repositories.

## CLI Contract Candidates

The M4.3 CLI contract work should classify Notebook 02 examples before adding them to config:

| Candidate | Classification | M4.3 handling |
|---|---|---|
| `fintech-save-session --help` | Safe help/version | Add as a safe help contract when Notebook 02 source is imported or staged for contract validation. |
| `fintech-save-session ... --dry-run` | Dry-run/preview | Validate only as source/contract preview if upstream dry-run behavior is confirmed safe. |
| Dedicated restore help command, if available | Safe help/version, command name uncertain | Confirm current upstream name and flags before adding. |
| Dedicated restore dry-run/preview, if available | Dry-run/preview, command name uncertain | Validate only after confirming it does not require Drive, credentials, or generated runtime state. |
| Session inspection/metadata help command, if available | Safe help/version, command name uncertain | Confirm current upstream name before adding. |
| Missing restore/session command examples | Expected missing upstream command warning | Record as a warning or follow-up only if the notebook source clearly labels uncertainty. |
| Drive mount, credential prompts, live save, live restore | Manual Colab-only runtime command | Exclude from local CLI contract execution. |

## Cleanup Risk Inventory

M4.2 must remove or normalize these risks before import:

| Risk | Notebook 02 relevance | Required mitigation before import |
|---|---|---|
| Notebook outputs | Source candidate has outputs in 18 code cells. | Clear all outputs before import. |
| Execution counts | Source candidate has 18 code cells with non-null execution counts. | Reset execution counts to `null`. |
| Tracebacks | Runtime-captured persistence or restore failures may include paths or environment details. | Remove outputs and summarize any real failure in safe markdown only. |
| Logs | Save/restore commands and package/runtime checks can emit verbose logs. | Clear logs and avoid committing generated manifests. |
| Screenshots or rich displays | Colab runs may include rendered output blobs. | Remove all output blobs before import. |
| Private paths | Downloads, local machine, `/content`, and mounted Drive paths may appear in source or outputs. | Replace with portable placeholders or safe runtime variables. |
| Drive account paths | Mounted Drive paths may reveal personal folders. | Use shell-safe placeholders such as `REPLACE_WITH_DRIVE_FOLDER_NAME`. |
| Credentials | Credential setup cells may reference runtime secrets. | Keep placeholder secret names only; never commit literal values. |
| Tokens | Live API or Drive output may expose tokens. | Search raw JSON and block import if any token appears. |
| `.env` values | Upstream apps may use environment files. | Do not commit `.env` content or values. |
| Generated session payloads | Session save may create payload folders or manifests. | Keep payloads outside Git and out of notebook outputs. |
| Restore outputs | Restore may create files under `/content` or Drive. | Keep restore output files and listings out of Git. |
| Archive packs | Archive references may appear as bridge material. | Do not create or commit archive packs in Notebook 02. |
| Generated Parquet/data | Notebook 01 state may include generated daily bars data. | Do not commit data or broad generated file listings. |
| Local app workspaces | Fintech workspace under `/content` is generated runtime state. | Do not copy workspace files into the repo. |
| Runtime folders | `/content`, temporary session folders, caches, or staging folders may appear. | Keep runtime folders outside Git and remove copied listings. |
| Upstream logic duplication | Notebook cells could try to implement save/restore behavior manually. | Replace with native CLI orchestration or classify as upstream triage. |

## Path and Placeholder Rules

Notebook 02 must preserve these path rules:

- Active app work remains under `/content`.
- Google Drive is persistence, backup, and restore storage only.
- Google Drive must not become the active app workspace.
- Runtime session payloads and restore outputs stay outside Git.
- Do not use angle-bracket placeholders inside shell-interpolated paths.
- Prefer shell-safe placeholders such as `REPLACE_WITH_DRIVE_FOLDER_NAME`.
- Use portable runtime variables for Drive roots, session roots, and restore targets.
- Avoid committing local Windows paths, personal Drive folder names, account names, usernames, or machine-specific paths.

Safe placeholder pattern:

```python
DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"
DRIVE_ROOT = Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME
```

Unsafe shell-interpolated pattern:

```python
DRIVE_ROOT = Path("/content/drive/MyDrive/<DRIVE_FOLDER_PLACEHOLDER>")
```

The unsafe pattern can be interpreted as shell redirection when interpolated into `!` command cells and should be removed during cleanup.

## Repository Boundary Rules

This issue must not:

- Import Notebook 02 into `notebooks/`.
- Commit generated data.
- Commit session payloads.
- Commit restore outputs.
- Commit archives.
- Commit notebook outputs.
- Commit execution counts.
- Commit credentials or private paths.
- Run live save/restore in repository validation.
- Mount Google Drive in local validation.
- Require credentials, network access, live APIs, or generated runtime state.
- Modify upstream repositories.
- Reimplement upstream `fintech-market-ingestion` session persistence logic.
- Modify upstream `fintech-market-ingestion`.
- Modify upstream `stratlake-trade-engine`.

This issue adds the staging/classification record only. M4.2 should clean and normalize a copy of Notebook 02 before any source import is considered.

## Go/No-Go Checklist for M4.2 Cleanup

| Gate | Status |
|---|---|
| Candidate Notebook 02 source located outside committed repo. | Go |
| Workflow role confirmed as Fintech session persistence save/restore. | Go |
| Planned repository path identified. | Go |
| Relationship to Notebook 00 documented. | Go |
| Relationship to Notebook 01 documented. | Go |
| Full archive pack/restore workflow deferred to Notebook 03. | Go |
| Command inventory complete enough for M4.3 planning. | Go |
| Uncertain restore/session command names marked for upstream confirmation. | Go |
| Runtime-only cells and command families identified. | Go |
| Cleanup risks inventoried. | Go |
| Path and placeholder rules documented. | Go |
| Artifact boundaries clear. | Go |
| No generated files added. | Go |
| No notebook source import performed yet. | Go |

Go result: Notebook 02 can proceed to M4.2 cleanup/import preparation only as a cleaned copy. The source candidate remains outside the repository and must not be moved into `notebooks/` until outputs, execution counts, private paths, credentials, generated payloads, restore outputs, archive references, and runtime state are cleaned and validated.

## Recommended Next Issue

The next step is M4.2 - Clean and Normalize Notebook 02 Session Persistence Workflow.

M4.2 should clean a staged copy of Notebook 02, preserve the session persistence scope, keep full archive workflows deferred to Notebook 03, and prepare the notebook for later CLI contract validation, execution-readiness validation, sanitized pytest coverage, import audit, and notebook index updates.

## Non-Goals for M4.1

- Do not add `notebooks/02_fintech_session_persistence_save_restore.ipynb`.
- Do not edit Notebook 00 or Notebook 01 unless a broken reference is discovered and clearly justified.
- Do not wire validation configs yet.
- Do not add tests yet.
- Do not run live Colab workflows.
- Do not mount Google Drive.
- Do not execute session save/restore.
- Do not add generated files.
- Do not add archive packs.
- Do not modify upstream `fintech-market-ingestion`.
- Do not modify upstream `stratlake-trade-engine`.
- Do not reimplement upstream session persistence logic.
