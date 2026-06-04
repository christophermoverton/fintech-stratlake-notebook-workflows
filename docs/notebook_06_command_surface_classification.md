# Notebook 06 Command Surface Classification

## Scope

This document records the M9.2 command-surface and runtime-surface classification for
`notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb` before adding
Notebook 06 CLI registry, CLI contract, or sanitized execution coverage.

Notebook 06 remains a conservative validation, archive-preview, restore-readiness, and
handoff checkpoint after Notebook 05. Repository validation for Notebook 06 must stay
source-only. It must not execute live Colab cells, install packages, mount Drive, read
credentials, initialize sessions, ingest data, build features, create archives, restore
archives, or inspect generated runtime data.

Issue #69 imported Notebook 06 as cleaned source. Issue #70 classifies the surfaces that
must remain manual/runtime-only versus the surfaces that may become eligible for static
M9.3 registry/contract checks.

## Notebook Path

`notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb`

## Classification Categories

| Category | Meaning |
|---|---|
| `live_manual_runtime` | Command or runtime behavior intentionally executed only by a human in a live Colab/runtime session. |
| `live_manual_runtime_conditional` | Live runtime command gated by notebook-side conditions such as missing generated data. Unsafe for repository validation. |
| `live_manual_runtime_dry_run` | Live runtime command that executes in dry-run mode only. Still not source-only validation. |
| `preview_manual_guidance` | Printed or constructed command guidance that is not executed unless the user explicitly changes a guard. |
| `optional_commented_manual_restore` | Optional restore guidance that is not executed by default and remains manual. |
| `availability_check_only` | Command appears in a `shutil.which(...)` availability checklist only. Checklist presence does not validate command contracts. |
| `notebook_python_runtime` | Notebook-side Python surface with runtime dependency, mutation, inspection, display, or filesystem effects. |
| `contract_mismatch_or_unverified` | Command form is stale, mismatched against the current registry, or not yet verified against upstream implementation. |

## Command-Surface Table

| Surface | Notebook section | Example command or behavior | Classification | Repository validation treatment | Notes / follow-up |
|---|---|---|---|---|---|
| `pip install` | Install required packages | Installs notebook dependencies and upstream Fintech/StratLake packages | `live_manual_runtime` | Exclude from source-only validation and sanitized execution | Network/package install surface; not a CLI contract target. |
| `fintech-init-project` | Verify required CLI commands | `shutil.which("fintech-init-project")` | `availability_check_only` | Availability only; do not infer registry confirmation from checklist | Also appears as a live command below. |
| `fintech-backfill-daily` | Verify required CLI commands | `shutil.which("fintech-backfill-daily")` | `availability_check_only` | Availability only | Also appears as a conditional live command below. |
| `fintech-save-session` | Verify required CLI commands | `shutil.which("fintech-save-session")` | `availability_check_only` | Availability only; no live Notebook 06 command surface | Keep out of live Notebook 06 coverage unless a source-visible command is added later. |
| `fintech-restore-session` | Verify required CLI commands | `shutil.which("fintech-restore-session")` | `availability_check_only` | Availability only; no live Notebook 06 command surface | Do not confuse with `fintech-backup-data restore` backup-pack guidance. |
| `fintech-backup-data` | Verify required CLI commands | `shutil.which("fintech-backup-data")` | `availability_check_only` | Availability only | Pack/restore preview forms are classified separately and are not registry-current in this notebook. |
| `stratlake-init-session` | Verify required CLI commands | `shutil.which("stratlake-init-session")` | `availability_check_only` | Availability only | Also appears as a live command below. |
| `stratlake-build-features` | Verify required CLI commands | `shutil.which("stratlake-build-features")` | `availability_check_only` | Availability only | Also appears as a conditional live command below. |
| `stratlake-session-export` | Verify required CLI commands | `shutil.which("stratlake-session-export")` | `availability_check_only` | Availability only | Also appears as dry-run runtime command below. |
| `stratlake-session-import` | Verify required CLI commands | `shutil.which("stratlake-session-import")` | `availability_check_only` | Availability only; no live Notebook 06 command surface | Future/manual restore orientation only. |
| `stratlake-session-archive-bootstrap` | Verify optional/unverified preview commands | `shutil.which("stratlake-session-archive-bootstrap")` | `availability_check_only`; `contract_mismatch_or_unverified` | Optional availability print only; must not hard-fail source validation | M9.2 split this out of the hard-failing required workflow command list. Upstream contract remains unverified. |
| `stratlake-session-archive-restore-bootstrap` | Verify optional/unverified preview commands | `shutil.which("stratlake-session-archive-restore-bootstrap")` | `availability_check_only`; `contract_mismatch_or_unverified` | Optional availability print only; must not hard-fail source validation | M9.2 split this out of the hard-failing required workflow command list. Upstream contract remains unverified. |
| `fintech-init-project` | Initialize or reconnect the Fintech project session | `!fintech-init-project --root ... --notebooks --with-session --session-name ...` | `live_manual_runtime` | Eligible for static command-form coverage only; never execute in repo validation | Creates `/content` Fintech workspace/session manifest. |
| `stratlake-init-session` | Initialize or reconnect the StratLake project session | `!stratlake-init-session --root ... --project-name ... --marketlake-root ... --drive-root ... --enable-drive-persistence --notebook-configs` | `live_manual_runtime` | Eligible for static command-form coverage only; never execute in repo validation | Preserves explicit `MARKETLAKE_ROOT` Fintech-to-StratLake handoff. |
| `fintech-backup-data restore` | Optional restore Fintech curated data from Drive before API ingestion | M9.3-updated restore preview with `--backup-pack-dir`, `--restore-root`, and `--overwrite-policy fail` | `preview_manual_guidance`; `optional_commented_manual_restore` | Covered by static CLI contract/registry validation after M9.3 correction | M9.3 removed the stale `--root`/`--archive-id`/`--drive-root`/`--target-root`/`--copy-policy` preview form. |
| `fintech-backfill-daily` | Ensure Q1 daily bars are available locally | Conditional `!fintech-backfill-daily --symbols ... --start 2025-01-01 --end 2025-04-01 --out ... --feed iex --source session_{FINTECH_SESSION_ID} --window month` | `live_manual_runtime_conditional` | Eligible for static command-form coverage only; unsafe for repository execution | Conditional daily-bars backfill is live manual runtime and unsafe for repository validation. |
| `fintech-backup-data pack` | Optional archive the Fintech curated Q1 input | `FINTECH_PACK_COMMAND_TEXT` guarded by `CREATE_FINTECH_ARCHIVE = False`; M9.3-updated preview uses `--workspace-root`, `--source-dataset-root`, `--backup-root`, `--backup-id`, and `--shard-size-mb` | `preview_manual_guidance`; `notebook_python_runtime` | Covered by static CLI contract/registry validation after M9.3 correction | `subprocess.run(...)` remains guarded and manual-only; repository validation parses but does not execute the command. |
| `stratlake-build-features` | Ensure StratLake feature outputs are available | Conditional `!stratlake-build-features --timeframe 1D --start 2025-01-01 --end 2025-04-01 --tickers ... --marketlake-root ...` | `live_manual_runtime_conditional` | Eligible for static command-form coverage only; unsafe for repository execution | Conditional StratLake feature build is live manual runtime and unsafe for repository validation. |
| `stratlake-session-export` | Preview StratLake session export | `!stratlake-session-export --root ... --drive-root ... --include-features --include-artifacts --include-configs --dry-run` | `live_manual_runtime_dry_run` | Eligible for static dry-run command-form coverage; never execute in source-only validation | Dry-run is still live manual runtime because it depends on runtime workspace and Drive paths. |
| `stratlake-session-archive-bootstrap` | Optional archive the StratLake feature session | `subprocess.run(stratlake_archive_cmd, check=True)` guarded by `CREATE_STRATLAKE_ARCHIVE = False` | `preview_manual_guidance`; `contract_mismatch_or_unverified`; `notebook_python_runtime` | Defer from confirmed registry coverage until upstream verified | Preview remains manual guidance. Do not promote without verifying command existence, flags, and allowed values upstream. |
| `stratlake-session-archive-restore-bootstrap` | Restore-readiness command preview | Printed command list only | `preview_manual_guidance`; `contract_mismatch_or_unverified` | Defer from confirmed registry coverage until upstream verified | Restore preview remains manual guidance and is not executed by Notebook 06. |

## Notebook-Side Runtime Table

| Runtime surface | Notebook section | Classification | Safe for source-only validation? | Notes / follow-up |
|---|---|---|---|---|
| Google Drive mount | Authorize Google Drive access | `live_manual_runtime`; `notebook_python_runtime` | No | `drive.mount("/content/drive")` is live Colab authorization. |
| Drive folder creation | Create session-scoped Google Drive folders and archive IDs | `live_manual_runtime`; `notebook_python_runtime` | No | `.mkdir(...)` creates session/archive folders under Drive. Google Drive is persistence/archive storage only, not active app workspace. |
| Drive mutation guard | Define shared paths; create Drive folders | `notebook_python_runtime` | Source can be inspected only | Placeholder guard prevents accidental Drive folder creation before `DRIVE_FOLDER_NAME` is set. |
| Credential prompts | Configure Alpaca API credentials | `live_manual_runtime`; `notebook_python_runtime` | No | `getpass.getpass(...)` is interactive and must be skipped/no-op in sanitized execution. |
| Colab userdata / secrets access | Configure Alpaca API credentials | `live_manual_runtime`; `notebook_python_runtime` | No | `google.colab.userdata.get(...)` reads live runtime secrets. |
| Environment variable assignment | Configure Alpaca API credentials | `notebook_python_runtime` | No execution; source inspection only | Assigns Alpaca credential env vars at runtime. Do not run in repo validation. |
| `.mkdir(...)` | Config/ticker setup, daily-bars root, Drive paths | `notebook_python_runtime` | No | Runtime mutation surface under `/content` or Drive. |
| `.write_text(...)` | Prepare ticker files and Q1 validation window | `notebook_python_runtime` | No | Writes runtime ticker/config files; generated files must not be committed. |
| `os.chdir(...)` | Ensure StratLake feature outputs are available | `notebook_python_runtime` | No | Mutates current working directory before feature build. |
| Parquet reads | Validate Fintech daily-bars handoff; validate StratLake feature outputs | `notebook_python_runtime` | No | Runtime data inspection, not source validation. |
| `display(...)` | Daily-bars and feature-output validation | `notebook_python_runtime` | No | Runtime display surface; not CI-safe source validation. |
| Portability checks | Validate session portability assumptions | `notebook_python_runtime` | No execution; source inspection only | Checks generated sessions, configs, Drive roots, daily bars, and feature files. |
| Final JSON summary | Final handoff summary | `notebook_python_runtime` | No if upstream live cells are skipped | Depends on runtime session IDs, file counts, Drive roots, archive IDs, and generated data checks. |
| `subprocess.run(...)` archive guards | Fintech archive pack; StratLake archive bootstrap | `notebook_python_runtime`; `preview_manual_guidance` | No | Guarded by `CREATE_* = False`, but sanitized execution should skip/no-op anyway. |
| Filesystem `glob` / `rglob` checks | Session manifest discovery, generated data checks, feature/artifact checks | `notebook_python_runtime` | No execution in source validation | Reads runtime filesystem and generated artifacts. |
| Config file reads/previews | Verify StratLake notebook config files | `notebook_python_runtime` | No execution in source validation | Reads generated `universe.yml` and `paths.yml`. |
| Session manifest reads | Fintech and StratLake session initialization sections | `notebook_python_runtime` | No execution in source validation | Reads generated session metadata from `/content`. |
| Generated-data availability checks | Daily-bars and feature-output sections | `notebook_python_runtime` | No | Runtime data inspection cells should not be executed during source-only validation. |
| Archive pack existence checks | Restore preview and archive sections | `notebook_python_runtime` | No | Checks Drive archive/backup pack paths; does not validate archive correctness. |

## Required Classification Decisions

1. Conditional daily-bars backfill is `live_manual_runtime_conditional` and unsafe for repository validation.
2. Conditional StratLake feature build is `live_manual_runtime_conditional` and unsafe for repository validation.
3. Fintech daily-bars validation cells are runtime data inspection, not source validation.
4. StratLake feature-output validation cells are runtime data inspection, not source validation.
5. Parquet reads and `display(...)` calls are notebook runtime inspection surfaces, not CI-safe source validation.
6. Google Drive mount and Drive folder creation are live/manual runtime surfaces.
7. Credential prompts and Colab userdata reads are live/manual runtime surfaces.
8. `.mkdir(...)`, `.write_text(...)`, `os.chdir(...)`, and `subprocess.run(...)` are runtime mutation/execution surfaces and should not be executed during source-only repository validation.
9. `stratlake-session-export --dry-run` is `live_manual_runtime_dry_run`.
10. Notebook 06 `fintech-backup-data` preview forms need registry-current correction or explicit deferral.
11. StratLake archive/bootstrap previews remain unverified unless upstream checked.
12. Availability checks do not automatically promote commands into live execution or registry-confirmed command contracts.
13. Runtime data inspection cells should not be executed during source-only validation.

## Contract Mismatch / Unverified Surfaces

### Fintech backup command drift

Issue #70 found that Notebook 06 retained older-looking `fintech-backup-data pack` and
`restore` preview forms:

```text
fintech-backup-data pack
  --root ...
  --dataset-root ...
  --archive-id ...
  --drive-root ...
  --copy-policy overwrite_allowed
  --validate-after-copy
  --inspect-after-copy
```

```text
fintech-backup-data restore
  --root ...
  --archive-id ...
  --drive-root ...
  --target-root ...
  --copy-policy overwrite_allowed
  --validate-after-copy
  --inspect-after-copy
```

M8.3 corrected Notebook 05 to the registry-confirmed backup-pack forms:

```text
fintech-backup-data pack
  --workspace-root ...
  --source-dataset-root ...
  --backup-root ...
  --backup-id ...
  --shard-size-mb ...
```

```text
fintech-backup-data restore
  --backup-pack-dir ...
  --restore-root ...
  --overwrite-policy ...
```

M9.2 decision: do not silently validate the stale Notebook 06 forms. They were classified
as `contract_mismatch_or_unverified` unless corrected.

M9.3 resolution: Notebook 06 was updated to the registry-current backup-pack forms before
adding static coverage:

- `fintech-backup-data pack` now uses `--workspace-root`, `--source-dataset-root`,
  `--backup-root`, `--backup-id`, and `--shard-size-mb`.
- `fintech-backup-data restore` now uses `--backup-pack-dir`, `--restore-root`, and
  `--overwrite-policy fail`.

The corrected pack and restore previews are covered by static CLI contract/registry
validation. They remain preview/manual guidance only and are not executed during
repository validation.

### StratLake archive/bootstrap caution

The following commands remain unverified after M8:

- `stratlake-session-archive-bootstrap`
- `stratlake-session-archive-restore-bootstrap`

Notebook 06 uses them only as optional/unverified availability checks and preview/manual
guidance. M9.2 split them out of the hard-failing `required_workflow_commands` checklist
into `optional_unverified_preview_commands`, so a missing unverified archive/bootstrap
command does not block the notebook's core validation workflow.

M9.2 decision: classify these commands as `availability_check_only`,
`preview_manual_guidance`, and `contract_mismatch_or_unverified`. Do not promote them to
confirmed CLI registry coverage unless upstream verification is completed and documented.

## M9.3 Eligibility Summary

Likely eligible for static CLI contract/registry coverage, assuming existing registry
support and source-only validation:

- `fintech-init-project`
- `stratlake-init-session`
- `fintech-backfill-daily`
- `stratlake-build-features`
- `stratlake-session-export --dry-run`
- `fintech-backup-data pack` after M9.3 update to registry-current syntax
- `fintech-backup-data restore` after M9.3 update to registry-current syntax

Not eligible for confirmed M9.3 coverage unless corrected or upstream verified:

- `stratlake-session-archive-bootstrap`
- `stratlake-session-archive-restore-bootstrap`

Manual/runtime-only and not live-command coverage for Notebook 06:

- package installs
- Google Drive mount
- credential prompts and Colab userdata reads
- environment variable credential setup
- Drive folder creation
- ticker/config writes
- parquet reads and displays
- generated data/feature/archive existence inspections
- final runtime summary when dependent on skipped live cells

## M9.4 Sanitized Execution Guidance

Sanitized execution should skip or no-op:

- package installs
- Drive mount
- credential prompts
- Colab userdata reads
- environment variable credential setup
- Fintech session initialization
- StratLake session initialization
- Drive folder creation
- ticker/config writes
- conditional daily-bars backfill
- conditional feature build
- archive/restore/export commands
- `subprocess.run(...)`
- `.mkdir(...)`
- `.write_text(...)`
- `os.chdir(...)`
- parquet reads
- `display(...)`
- generated feature/daily-bars inspections
- archive pack existence checks
- config file previews that depend on generated runtime files
- session manifest reads that depend on live initialization
- final runtime summary if dependent on skipped live cells

If M9.4 introduces sanitized execution coverage, it should validate only safe source
structure and pure Python fragments that do not require Colab, credentials, generated
runtime files, upstream CLIs, Drive, or archive packs.

## Non-Claims

This classification does not:

- execute Notebook 06 live cells,
- run a Colab smoke test,
- install upstream packages,
- verify upstream CLI implementations,
- validate stale Fintech backup syntax,
- validate StratLake archive/bootstrap command contracts,
- create or restore archives,
- generate daily bars,
- generate StratLake features,
- inspect real generated data,
- claim `stratlake-session-archive-bootstrap` or
  `stratlake-session-archive-restore-bootstrap` are registry-current commands.

This document is a source classification and M9.3/M9.4 handoff record only.
