# Notebook 04 Staging and Classification

## Summary

This document records the Milestone 7 staging and classification decisions for Notebook 04
before and during cleanup, validation, and audit work.

Notebook 04 is the StratLake feature-series index and dual-session setup tutorial. It is
the first StratLake-facing notebook in the repository sequence. It bridges the Fintech
curated-data workspace (`FINTECH_SESSION_ID`) with the downstream StratLake
feature/research workspace (`STRATLAKE_SESSION_ID`). Its live workflow depends on a Colab
runtime, mounted Google Drive, installed packages, generated session metadata, curated
market data, and StratLake session state. Repository validation must therefore remain
source-only and sanitized.

## Candidate Notebook Identity

| Field | Value |
|---|---|
| Repository path | `notebooks/04_stratlake_feature_series_index_setup.ipynb` |
| Source notebook | Smoke-tested Colab notebook supplied outside repository |
| Notebook title | Notebook 04 — StratLake Feature Data Series Index and Dual-Session Setup |
| Workflow classification | StratLake feature-series setup and dual-session Fintech/StratLake bridge |
| Primary upstream app | `stratlake-trade-engine` |
| Secondary upstream app | `fintech-market-ingestion` (upstream curated-data provider) |
| Relationship to Notebook 00 | Preserves `/content` workspace and storage conventions |
| Relationship to Notebook 03 | Uses Fintech `SESSION_ID`-scoped archive paths; does not recreate them |
| Relationship to Notebook 05 | Forward orientation only; Notebook 05 is not yet imported |
| Staging category | `needs_cleanup` before import; `source_safe_after_cleanup` after Issue #53 |
| Import status | `imported` after Issue #53 |
| Manual Colab smoke status | `colab_smoke_pending` |

## Source Review Facts

Initial M7.1 review of the uploaded notebook found:

- 29 total cells: 16 markdown cells, 13 code cells.
- All code cells reviewed for outputs, execution counts, and Colab/runtime metadata.
- Outputs cleared; execution counts reset to `null`; Colab metadata stripped.
- No generated data, archive packs, restored files, session manifests, feature files,
  or Drive artifacts committed.
- No credentials, private paths, or account-specific identifiers committed.

## Expected Notebook Role

Notebook 04 should guide a Colab user through:

- Installing `fintech-market-ingestion`, `stratlake-trade-engine`, and
  `pandas-market-calendars` from TestPyPI manually in Colab.
- Verifying CLI command availability for all nine required commands.
- Mounting Google Drive manually in Colab.
- Defining shared Fintech and StratLake local and Drive paths from session variables.
- Initializing a Fintech project session to obtain `FINTECH_SESSION_ID`.
- Extracting `FINTECH_SESSION_ID` from the generated Fintech session manifest.
- Initializing a StratLake session with an explicit `--marketlake-root` pointing at
  the Fintech curated-data directory.
- Extracting `STRATLAKE_SESSION_ID` from the generated StratLake session metadata.
- Creating `SESSION_ID`-scoped Drive folders for Fintech and StratLake persistence.
- Optionally reviewing available Drive sessions for restore.
- Printing `fintech-backup-data pack` and `restore` command previews as guidance.
- Optionally verifying or restoring Fintech curated data before StratLake feature generation.
- Confirming shared readiness across both session identifiers, Drive paths, and `MARKETLAKE_ROOT`.
- Orienting toward Notebook 05 (StratLake Q1 feature data generation).

Notebook 04 is a **setup/bridge notebook**, not a feature-generation notebook. It does not
generate StratLake features. Feature generation belongs to Notebook 05.

## Cell-Level Staging Classification

### `729b15e6` — Package install cell

**Category: live manual runtime; package install; sanitized execution skipped.**

```python
!pip install "pandas-market-calendars>=5.0"
!pip install -i https://test.pypi.org/simple/ fintech-market-ingestion
!pip install -i https://test.pypi.org/simple/ stratlake-trade-engine
```

- Must be run manually in a fresh Colab runtime before any other cells.
- Repository validation does not install packages from TestPyPI or PyPI.
- Skipped by sanitized execution harness (shell prefix `!`).
- Skipped by readiness validator (shell/magic + network/package-install classification).

---

### `f36c9ea9` — CLI availability check

**Category: source-inspected; readiness/orientation check; compile-safe.**

```python
import shutil
required_commands = [...]
for command in required_commands:
    path = shutil.which(command)
    print(f"{command}: {path if path else 'NOT FOUND'}")
```

- Uses `shutil.which()` only; does not execute any CLI command.
- In a repository environment, all commands report `NOT FOUND` since the upstream
  packages are not installed; this is expected and harmless.
- Kept by sanitized execution harness (no unsafe patterns).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns).
- Do not treat `shutil.which()` presence as evidence of live CLI execution.

---

### `99822946` — Google Drive mount cell

**Category: live manual runtime; Drive mount; sanitized execution skipped.**

```python
from google.colab import drive
drive.mount("/content/drive")
```

- Must be run manually in Colab.
- Repository validation does not mount Google Drive.
- Skipped by sanitized execution harness (`google.colab` pattern).
- Skipped by readiness validator (`colab_only` + `drive_mount` classification).

---

### `876835f0` — Shared path setup

**Category: source-inspected; Drive placeholder documented; sanitized execution skipped.**

Defines `FINTECH_ROOT`, `STRATLAKE_ROOT`, `DRIVE_FOLDER_NAME`, `DRIVE_ROOT`,
`FINTECH_DRIVE_ROOT`, `STRATLAKE_DRIVE_ROOT`, `MARKETLAKE_ROOT`,
`FINTECH_SESSION_NAME`, `STRATLAKE_SESSION_NAME`, and `DRIVE_FOLDER_NAME_IS_PLACEHOLDER`.

- Contains valid Python variable assignments and print statements.
- Skipped by sanitized execution harness (`FINTECH_ROOT` in skip patterns — variables
  derived from skipped-cell state cannot be safely isolated).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns;
  `FINTECH_ROOT` does not trigger readiness validator skip, only execution skip).
- `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` placeholder is preserved with
  a printed warning when still active.

---

### `bce5c87a` — Initialize Fintech project session

**Category: live manual runtime; live CLI command; sanitized execution skipped.**

```shell
!fintech-init-project \
  --root {FINTECH_ROOT.as_posix()} \
  --notebooks \
  --with-session \
  --session-name {FINTECH_SESSION_NAME}
```

- Creates the upstream Fintech project/session workspace under `/content`.
- Must be run manually in Colab after package install and path setup.
- Repository validation does not execute `fintech-init-project`.
- Skipped by sanitized execution harness (shell prefix `!`).
- Skipped by readiness validator (`shell_or_magic` + `artifact_or_upstream_command` classification).
- Flags match registry-confirmed `fintech-init-project` shape exactly.

---

### `483eb3d3` — Extract `FINTECH_SESSION_ID`

**Category: runtime-dependent; source-inspected or skipped; sanitized execution skipped.**

Reads the latest Fintech session manifest and extracts `FINTECH_SESSION_ID`.

- Depends on `fintech-init-project` having run first; skipped in repository validation.
- Skipped by sanitized execution harness (`FINTECH_ROOT` in skip patterns).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns).
- `FINTECH_SESSION_ID` is preserved in source as the canonical Fintech session identifier.

---

### `3dd31cc7` — Initialize StratLake session

**Category: live manual runtime; live CLI command; sanitized execution skipped.**

```shell
!stratlake-init-session \
  --root {STRATLAKE_ROOT.as_posix()} \
  --project-name {STRATLAKE_SESSION_NAME} \
  --marketlake-root {MARKETLAKE_ROOT.as_posix()} \
  --drive-root {DRIVE_ROOT.as_posix()} \
  --enable-drive-persistence \
  --notebook-configs
```

- Creates the downstream StratLake session workspace with the explicit
  `--marketlake-root` handoff from Fintech curated data.
- Must be run manually in Colab after Fintech session initialization.
- Repository validation does not execute `stratlake-init-session`.
- Skipped by sanitized execution harness (shell prefix `!`; `!stratlake-init-session`
  also in explicit skip patterns).
- Skipped by readiness validator (`shell_or_magic` + `artifact_or_upstream_command` classification).
- Flags are smoke-test-confirmed; upstream source verification remains pending.

---

### `0d21ddaa` — Extract `STRATLAKE_SESSION_ID`

**Category: runtime-dependent; sanitized execution skipped.**

Reads `.stratlake/session.json` and extracts `STRATLAKE_SESSION_ID`.

- Depends on `stratlake-init-session` having run first; skipped in repository validation.
- Skipped by sanitized execution harness (`STRATLAKE_ROOT` in skip patterns).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns).
- `STRATLAKE_SESSION_ID` is preserved in source as the canonical StratLake identifier.

---

### `0b8e19df` — Create Drive session folders

**Category: live manual runtime; Drive filesystem mutation; sanitized execution skipped.**

Creates `SESSION_ID`-scoped Drive directories for Fintech and StratLake under
`/content/drive/MyDrive/{DRIVE_FOLDER_NAME}/`.

- Includes `DRIVE_FOLDER_NAME_IS_PLACEHOLDER` and Drive mount guards before execution.
- Calls `.mkdir(parents=True, exist_ok=True)` on multiple Drive paths.
- Repository validation does not create Drive directories.
- Skipped by sanitized execution harness (`.mkdir(` in skip patterns).
- Skipped by readiness validator (no direct skip from `classify_cell`; compiled as
  valid Python syntax — Drive paths only fail at runtime, not at compile time).

---

### `8d3dc4dc` — Previous Drive session/path inspection

**Category: runtime-dependent; Drive path enumeration; sanitized execution skipped.**

Enumerates available Fintech and StratLake Drive sessions using `.glob()` on Drive paths.
Defines `RESTORE_FINTECH_SESSION_ID`, `RESTORE_STRATLAKE_SESSION_ID`, and related
archive path variables.

- Depends on prior Drive folder creation; skipped in repository validation.
- Skipped by sanitized execution harness (`available_fintech_sessions` in skip patterns).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns).

---

### `nb04_pack_preview` — Fintech archive pack preview

**Category: preview/manual guidance; CLI-validated as preview; sanitized execution skipped.**

Constructs and prints a `fintech-backup-data pack` command template using session-derived
variables.

- Not executed; prints human-readable guidance only.
- Flags use registry-confirmed shape (`--workspace-root`, `--source-dataset-root`,
  `--backup-root`, `--backup-id`, `--shard-size-mb`) updated in M7.3.
- Skipped by sanitized execution harness (`FINTECH_ROOT` pattern matches `FINTECH_ROOT_STR`
  in skip patterns).
- Validated as `printed_preview` classification by CLI registry and contract validators.

---

### `BWLYWDVttgH8` — Fintech archive restore preview

**Category: preview/manual guidance; CLI-validated as preview; sanitized execution skipped.**

Constructs and prints a `fintech-backup-data restore` command template using
restore-session-derived variables.

- Not executed; prints human-readable guidance only.
- Flags use registry-confirmed shape (`--backup-pack-dir`, `--restore-root`,
  `--overwrite-policy fail`) updated in M7.3.
- Skipped by sanitized execution harness (`fintech-backup-data restore` in skip patterns).
- Validated as `printed_preview` classification by CLI registry and contract validators.

---

### `tr2kxVdNtgH9` — Optional: verify or restore curated data

**Category: source-inspected / optional manual guidance; sanitized execution skipped.**

Checks `MARKETLAKE_ROOT.exists()` and lists sample curated-data paths if present. Contains
an intentionally commented `!fintech-backup-data restore` example.

- The commented restore command is optional manual guidance; it is never executed.
- Depends on `MARKETLAKE_ROOT` being defined (from a skipped cell); skipped in
  repository validation.
- Skipped by sanitized execution harness (`MARKETLAKE_ROOT` in skip patterns).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns;
  the commented `!fintech-backup-data restore` does not trigger shell classification
  because it is inside a Python comment, not a live shell prefix line).

---

### `1a86c0cb` — Shared readiness check

**Category: runtime-dependent; source-inspected or skipped; sanitized execution skipped.**

Prints status of all session identifiers, archive identifiers, local workspace paths,
Drive session paths, archive pack paths, and the `MARKETLAKE_ROOT` handoff status.

- Depends on all prior session/path variables being defined; skipped in repository validation.
- Skipped by sanitized execution harness (`FINTECH_ROOT` in skip patterns matches
  `FINTECH_ROOT.exists()` in cell source).
- Compiled by readiness validator (valid Python syntax, no shell/colab/drive patterns).

---

### `4efe9531` — Notebook 05 forward reference (markdown)

**Category: future notebook orientation only; no code; no action required.**

Documents the `FINTECH_SESSION_ID`, `STRATLAKE_SESSION_ID`, `MARKETLAKE_ROOT`,
`STRATLAKE_ROOT`, and `STRATLAKE_DRIVE_SESSION_ROOT` variables that Notebook 05 should
reuse.

- Markdown cell only; no code execution.
- Notebook 05 is future tutorial continuity only and is not yet imported or implemented.

---

## Sanitized Execution Boundary Summary

| Cell | Category | Sanitized execution result |
|---|---|---|
| `729b15e6` | Package install | Skipped (shell `!`) |
| `f36c9ea9` | CLI availability check | Kept; `shutil.which` runs harmlessly |
| `99822946` | Google Drive mount | Skipped (`google.colab` pattern) |
| `876835f0` | Shared path setup | Skipped (`FINTECH_ROOT` pattern) |
| `bce5c87a` | Fintech session init | Skipped (shell `!`) |
| `483eb3d3` | FINTECH_SESSION_ID extraction | Skipped (`FINTECH_ROOT` pattern) |
| `3dd31cc7` | StratLake session init | Skipped (shell `!`) |
| `0d21ddaa` | STRATLAKE_SESSION_ID extraction | Skipped (`STRATLAKE_ROOT` pattern) |
| `0b8e19df` | Drive folder creation | Skipped (`.mkdir(` pattern) |
| `8d3dc4dc` | Drive session enumeration | Skipped (`available_fintech_sessions` pattern) |
| `nb04_pack_preview` | Pack preview | Skipped (`FINTECH_ROOT` substring match) |
| `BWLYWDVttgH8` | Restore preview | Skipped (`fintech-backup-data restore` pattern) |
| `tr2kxVdNtgH9` | Optional curated data check | Skipped (`MARKETLAKE_ROOT` pattern) |
| `1a86c0cb` | Shared readiness check | Skipped (`FINTECH_ROOT` pattern) |

All markdown cells are kept as-is.

## Repository Validation Does Not Perform

- Live Colab execution.
- Google Drive mount.
- Package installation from TestPyPI or PyPI.
- `fintech-init-project` execution.
- `stratlake-init-session` execution.
- Drive session folder creation.
- Drive archive directory creation.
- Drive session enumeration.
- `MARKETLAKE_ROOT` content inspection or validation.
- Fintech curated-data archive pack creation.
- Fintech curated-data archive restore.
- StratLake feature generation.
- Session manifest creation.
- Source notebook mutation.

## Known Follow-up Items for M7.6

- Manual Colab smoke for Notebook 04 remains `pending`.
- `stratlake-init-session` upstream source verification remains pending.
- Notebook 05 remains future tutorial continuity only; it is not implemented.
