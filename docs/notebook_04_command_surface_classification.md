# Notebook 04 Command Surface Classification

## Summary

This document records the M7.2 command-surface review and classification for
`notebooks/04_stratlake_feature_series_index_setup.ipynb`.

Notebook 04 is the first StratLake-facing notebook in the tutorial series. It introduces
the dual-session pattern and the explicit `marketlake_root` handoff from Fintech to
StratLake. Its command surfaces span two upstream packages and four distinct usage
patterns (live runtime, availability check, printed preview, and optional manual guidance).

Commit reviewed: `e4c0c8ff44ee2635e767fbb318b35f95eb8e2319` (M7.1 import and cleanup).

## Audit Scope

| Field | Value |
|---|---|
| Notebook path | `notebooks/04_stratlake_feature_series_index_setup.ipynb` |
| Upstream packages | `fintech-market-ingestion`, `stratlake-trade-engine` |
| Total cells | 29 (16 markdown, 13 code) |
| Fintech commands observed | `fintech-init-project`, `fintech-save-session`, `fintech-backup-data` |
| StratLake commands observed | `stratlake-init-session`, `stratlake-build-features`, `stratlake-session-export`, `stratlake-session-import`, `stratlake-session-archive-bootstrap`, `stratlake-session-archive-restore-bootstrap` |

## Cell-Level Evidence

| Cell ID | Cell heading | Relevant command forms found |
|---|---|---|
| `f36c9ea9` | Verify required CLI commands | `shutil.which()` check for all 9 commands |
| `bce5c87a` | Initialize the Fintech project session | `!fintech-init-project` live shell |
| `3dd31cc7` | Initialize the StratLake project session | `!stratlake-init-session` live shell |
| `BWLYWDVttgH8` | Fintech curated-data archive command previews | `fintech-backup-data pack` and `restore` as printed f-strings |
| `tr2kxVdNtgH9` | Optional: verify or restore Fintech curated data | `fintech-backup-data restore` as commented shell (optional manual guidance) |

## Command Surface Classification Table

| Command | Source cell | Observed form | Classification | Live in NB04? | Registry action for M7.3 | Notes |
|---|---|---|---|---|---|---|
| `fintech-init-project` | `bce5c87a` | `!fintech-init-project --root ... --notebooks --with-session --session-name ...` | `live_runtime_command` | yes | Add NB04 to `confirmed_from`; extend contract/registry targets | Flags match registry exactly. Creates upstream Fintech session manifest. |
| `stratlake-init-session` | `3dd31cc7` | `!stratlake-init-session --root ... --project-name ... --marketlake-root ... --drive-root ... --enable-drive-persistence --notebook-configs` | `live_runtime_command` | yes | Add new `[[commands]]` entry for `stratlake-init-session`; update excluded_candidates scope note | Entirely new to registry. Previously all StratLake commands were classified as excluded future scope. NB04 promotes this one command to live. Flags are smoke-test-confirmed; M7.3 must verify against upstream CLI implementation. |
| `fintech-save-session` | `f36c9ea9` | `shutil.which("fintech-save-session")` | `availability_readiness_check` | no | Do not register as live for NB04; keep existing registry entry unchanged | Not executed in NB04. Appears only in the CLI availability check. Fintech session save is a Notebook 00/01 behavior. |
| `fintech-backup-data` (base) | `f36c9ea9` | `shutil.which("fintech-backup-data")` | `availability_readiness_check` | no | Extend existing `confirmed_from` to include NB04 | Not called as a live subcommand in NB04. |
| `fintech-backup-data pack` | `BWLYWDVttgH8` | Printed f-string preview (not executed) | `printed_preview` | no | Register as `printed_preview` for NB04; **flag mismatch is a M7.3 blocker** | Preview flags: `--root`, `--dataset-root`, `--archive-id`, `--drive-root`, `--copy-policy overwrite_allowed`, `--validate-after-copy`, `--inspect-after-copy`. Registry-confirmed pack flags: `--workspace-root`, `--source-dataset-root`, `--backup-root`, `--backup-id`, `--shard-size-mb`. These are different flag surfaces. See flag concern section below. |
| `fintech-backup-data restore` | `BWLYWDVttgH8` (printed) + `tr2kxVdNtgH9` (commented) | Printed f-string + commented `!` shell | `printed_preview` / `optional_manual_guidance` | no | Register as `printed_preview` / `optional_manual_guidance` for NB04; **flag mismatch is a M7.3 blocker** | Preview/commented flags: `--root`, `--archive-id`, `--drive-root`, `--target-root`, `--copy-policy overwrite_allowed`, `--validate-after-copy`, `--inspect-after-copy`. Registry-confirmed restore flags: `--backup-pack-dir`, `--restore-root`, `--overwrite-policy`. Different flag surfaces. See flag concern section below. `fintech-restore-session` is NOT used and must not be introduced. |
| `stratlake-build-features` | `f36c9ea9` | `shutil.which("stratlake-build-features")` | `availability_readiness_check` / `future_series_orientation` | no | Do not register as live for NB04 | Not executed in NB04. Referenced in Notebook 05 forward orientation. Feature generation is Notebook 05 scope. |
| `stratlake-session-export` | `f36c9ea9` | `shutil.which("stratlake-session-export")` | `availability_readiness_check` | no | Do not register as live for NB04 | Not executed in NB04. Future session-save notebook scope. |
| `stratlake-session-import` | `f36c9ea9` | `shutil.which("stratlake-session-import")` | `availability_readiness_check` | no | Do not register as live for NB04 | Not executed in NB04. Future session-restore notebook scope. |
| `stratlake-session-archive-bootstrap` | `f36c9ea9` | `shutil.which("stratlake-session-archive-bootstrap")` | `availability_readiness_check` | no | Do not register as live for NB04 | Not executed in NB04. Future archive notebook scope. |
| `stratlake-session-archive-restore-bootstrap` | `f36c9ea9` | `shutil.which("stratlake-session-archive-restore-bootstrap")` | `availability_readiness_check` | no | Do not register as live for NB04 | Not executed in NB04. Future archive-restore notebook scope. |

## Live Command Detail: `fintech-init-project`

Source cell `bce5c87a` — "Initialize the Fintech project session":

```shell
!fintech-init-project \
  --root {FINTECH_ROOT.as_posix()} \
  --notebooks \
  --with-session \
  --session-name {FINTECH_SESSION_NAME}
```

Flags observed: `--root`, `--notebooks`, `--with-session`, `--session-name`

Registry status: confirmed. All four flags match the existing `cli_command_registry.toml`
entry for `fintech-init-project`. The flag shapes match Notebooks 01–03 precedent exactly.

Classification: `live_runtime_command`. Creates the upstream Fintech project workspace and
session manifest. `FINTECH_SESSION_ID` is extracted from the generated manifest in the
following cell. This is the same live initialization pattern used in prior notebooks.

M7.3 action: Add `fintech-stratlake-notebook-workflows:notebooks/04_stratlake_feature_series_index_setup.ipynb`
to `confirmed_from` for `fintech-init-project` in `cli_command_registry.toml`. Add NB04
to `notebook_cli_contracts.toml` and `notebook_cli_registry.toml` default_targets.

## Live Command Detail: `stratlake-init-session`

Source cell `3dd31cc7` — "Initialize the StratLake project session":

```shell
!stratlake-init-session \
  --root {STRATLAKE_ROOT.as_posix()} \
  --project-name {STRATLAKE_SESSION_NAME} \
  --marketlake-root {MARKETLAKE_ROOT.as_posix()} \
  --drive-root {DRIVE_ROOT.as_posix()} \
  --enable-drive-persistence \
  --notebook-configs
```

Flags observed: `--root`, `--project-name`, `--marketlake-root`, `--drive-root`,
`--enable-drive-persistence`, `--notebook-configs`

Registry status: **not registered**. The existing `cli_command_registry.toml` has a
`[[excluded_candidates]]` entry grouping all `stratlake-trade-engine commands` as
`excluded_future_notebook_scope`. Notebook 04 promotes `stratlake-init-session` out of
that excluded scope into a live runtime command. The excluded_candidates scope note
requires a documentation update; the actual `[[commands]]` entry belongs to M7.3.

Smoke test status: confirmed green by the smoke-tested uploaded source (M7.1 evidence).
Flags were produced by the live Colab runtime during the smoke test. Do not change flags
without upstream CLI implementation evidence.

Classification: `live_runtime_command`. Creates the downstream StratLake session workspace
with an explicit `--marketlake-root` pointing at the Fintech curated-data directory. This
is the key Fintech→StratLake handoff. `STRATLAKE_SESSION_ID` is extracted from the
generated `.stratlake/session.json` in the following cell.

M7.3 action:
- Add a new `[[commands]]` entry for `stratlake-init-session` to `cli_command_registry.toml`.
- Add a new `[[commands]]` entry to `notebook_cli_contracts.toml`.
- Update the `[[excluded_candidates]]` scope note for `stratlake-trade-engine commands` to
  clarify that `stratlake-init-session` is now promoted to live NB04 scope.
- Verify all six flags against the `stratlake-trade-engine` upstream CLI implementation.

## Preview Surface Detail: `fintech-backup-data pack` and `restore`

### Observed flag shapes in Notebook 04

Source cell `BWLYWDVttgH8` — "Fintech curated-data archive command previews":

```python
fintech_pack_preview = f'''
fintech-backup-data pack \
  --root {FINTECH_ROOT_STR} \
  --dataset-root {MARKETLAKE_ROOT_STR} \
  --archive-id {FINTECH_ARCHIVE_ID} \
  --drive-root {FINTECH_DRIVE_BACKUP_ROOT_STR} \
  --copy-policy overwrite_allowed \
  --validate-after-copy \
  --inspect-after-copy
'''.strip()

fintech_restore_preview = f'''
fintech-backup-data restore \
  --root {FINTECH_ROOT_STR} \
  --archive-id {RESTORE_FINTECH_ARCHIVE_ID} \
  --drive-root {RESTORE_FINTECH_DRIVE_BACKUP_ROOT_STR} \
  --target-root {MARKETLAKE_ROOT_STR} \
  --copy-policy overwrite_allowed \
  --validate-after-copy \
  --inspect-after-copy
'''.strip()
```

Source cell `tr2kxVdNtgH9` — "Optional: verify or restore Fintech curated data":

```python
# Example restore command, intentionally commented:
#
# !fintech-backup-data restore \
#   --root {FINTECH_ROOT_STR} \
#   --archive-id {RESTORE_FINTECH_ARCHIVE_ID} \
#   --drive-root {RESTORE_FINTECH_DRIVE_BACKUP_ROOT_STR} \
#   --target-root {MARKETLAKE_ROOT_STR} \
#   --copy-policy overwrite_allowed \
#   --validate-after-copy \
#   --inspect-after-copy
```

### Flag comparison

**`fintech-backup-data pack` — NB04 preview vs. registry:**

| Flag | NB04 preview | Registry (confirmed for pack) | Status |
|---|---|---|---|
| `--root` | present | not in registry for pack | unconfirmed |
| `--dataset-root` | present | not in registry for pack | unconfirmed |
| `--archive-id` | present | not in registry for pack | unconfirmed |
| `--drive-root` | present | not in registry for pack | unconfirmed |
| `--copy-policy overwrite_allowed` | present | not in registry for pack | unconfirmed |
| `--validate-after-copy` | present | not in registry for pack | unconfirmed |
| `--inspect-after-copy` | present | not in registry for pack | unconfirmed |
| `--workspace-root` | absent | `argparse_required=true, notebook_contract_required=true` | missing |
| `--source-dataset-root` | absent | `argparse_required=true, notebook_contract_required=true` | missing |
| `--backup-root` | absent | `argparse_required=true, notebook_contract_required=true` | missing |
| `--backup-id` | absent | `notebook_contract_required=true` | missing |
| `--shard-size-mb` | absent | `notebook_contract_required=true` | missing |

**`fintech-backup-data restore` — NB04 preview vs. registry:**

| Flag | NB04 preview/commented | Registry (confirmed for restore) | Status |
|---|---|---|---|
| `--root` | present | not in registry for restore | unconfirmed |
| `--archive-id` | present | not in registry for restore | unconfirmed |
| `--drive-root` | present | not in registry for restore | unconfirmed |
| `--target-root` | present | not in registry for restore | unconfirmed |
| `--copy-policy overwrite_allowed` | present | not in registry (`--overwrite-policy` is confirmed with values `fail/replace/merge`) | different name and value |
| `--validate-after-copy` | present | not in registry for restore | unconfirmed |
| `--inspect-after-copy` | present | not in registry for restore | unconfirmed |
| `--backup-pack-dir` | absent | `argparse_required=true, notebook_contract_required=true` | missing |
| `--restore-root` | absent | `argparse_required=true, notebook_contract_required=true` | missing |
| `--overwrite-policy` | absent (uses `--copy-policy`) | `notebook_contract_required=true`, `allowed_values=["fail","replace","merge"]` | name mismatch |

### Analysis

The Notebook 04 preview strings use a flag interface that is entirely different from the
registry-confirmed `fintech-backup-data pack` and `restore` shapes. This is not a small
flag difference; the flags appear to represent a different or newer command interface than
what `cli_command_registry.toml` currently records.

Possible interpretations:

1. **Newer upstream API**: The smoke-tested Colab runtime installed a newer version of
   `fintech-market-ingestion` from TestPyPI in which `fintech-backup-data` gained a
   different flag interface (`--root`, `--archive-id`, `--drive-root`, etc.) as a
   higher-level operation that wraps the lower-level pack/restore into a session-aware
   workflow. In this case the registry is behind and M7.3 must verify and update it.

2. **Preview is illustrative only**: The preview strings represent conceptually what the
   user would do, assembled using session-derived variable names that happen to share
   names with hypothetical future CLI flags. The flags were never validated against the
   installed CLI in the notebook's smoke-test session (since the preview only prints, not
   runs). In this case the flags may be invalid but the preview is harmless because it
   is never executed.

3. **Registry is authoritative for current shape**: The existing registry was confirmed
   from upstream implementation files (`src/cli/backup_data.py`). Until M7.3 verifies
   the upstream CLI, the registry represents the known-good shape and the preview flags
   are treated as unconfirmed.

### Disposition for M7.2

Because these flags appear only in **printed preview strings and a commented optional
example** — never in live execution — they do not affect Notebook 04 runtime behavior.
The preview cells print human-readable templates; no command is actually executed.

Per M7.2 policy:
- Do not change the Notebook 04 source based on this flag concern alone.
- The preview strings were produced by the smoke-tested runtime and reflect the author's
  intended usage pattern.
- M7.3 must verify the current `fintech-backup-data pack` and `restore` flag interface
  against the upstream `stratlake-trade-engine` or `fintech-market-ingestion` TestPyPI
  release before deciding whether to update the preview strings or update the registry.

Classification:
- `fintech-backup-data pack` in NB04: **`printed_preview`** — not live, flags unconfirmed.
- `fintech-backup-data restore` in NB04: **`printed_preview`** (cell `BWLYWDVttgH8`) and
  **`optional_manual_guidance`** (cell `tr2kxVdNtgH9`, commented) — not live, flags unconfirmed.
- `fintech-restore-session` is not present and must not be reintroduced.

## `stratlake-trade-engine commands` Excluded Candidates Scope Note

The existing `[[excluded_candidates]]` entry in `cli_command_registry.toml` groups all
StratLake commands under `excluded_future_notebook_scope` with the note:
"No StratLake command, subcommand, flag, or argument is treated as valid notebook syntax
in this registry."

Notebook 04 now uses `stratlake-init-session` as a live runtime command, which means
that blanket statement is no longer accurate. The scope note should be narrowed to
reflect that `stratlake-init-session` is promoted to NB04 live scope, and the remaining
StratLake commands remain excluded until their respective notebooks are imported.

This scope-note update is a documentation adjustment and does not require adding a full
`[[commands]]` entry for any StratLake command in this issue; that belongs to M7.3.

## Availability Check Commands (All)

Cell `f36c9ea9` contains a single `shutil.which()` loop covering all nine commands:

```python
required_commands = [
    "fintech-init-project",
    "fintech-save-session",
    "fintech-backup-data",
    "stratlake-init-session",
    "stratlake-build-features",
    "stratlake-session-export",
    "stratlake-session-import",
    "stratlake-session-archive-bootstrap",
    "stratlake-session-archive-restore-bootstrap",
]
```

**Classification: `availability_readiness_check` for all nine.**

Appearing in a `shutil.which()` check does not imply live execution in Notebook 04.
The availability check is a readiness gate: it confirms the runtime has all expected CLI
tools installed before the user runs live cells. Most of these commands are only
needed by later notebooks (Notebooks 05–07); their presence in this check orients the
user to the full tutorial suite without adding execution scope to Notebook 04.

Do not treat `shutil.which()` presence as evidence of live execution.

## Future Series Orientation Commands

The following commands appear **only** in the availability check and/or in the Notebook 05
forward-reference markdown. They are not present as live shell commands or preview strings
anywhere in Notebook 04:

- `stratlake-build-features` — Notebook 05 feature generation
- `stratlake-session-export` — Notebook 06 session save
- `stratlake-session-import` — Notebook 06 session restore
- `stratlake-session-archive-bootstrap` — Notebook 07 session archive
- `stratlake-session-archive-restore-bootstrap` — Notebook 07 session archive restore

**Classification: `availability_readiness_check` / `future_series_orientation`.**

Do not register any of these as live Notebook 04 behavior. Do not add them to the NB04
contract targets in M7.3.

## Excluded / Stale Candidates

| Command | Status | Reason |
|---|---|---|
| `fintech-restore-session` | excluded — not present in NB04 | Must not be reintroduced as the backup-pack restore path. Registry already records this as `excluded_not_current_notebook_scope`. |
| `fintech-backup-data pack` (preview flags) | unconfirmed flags — pending M7.3 | Preview flags differ from registry-confirmed shape. Not live in NB04. M7.3 must verify. |
| `fintech-backup-data restore` (preview/commented flags) | unconfirmed flags — pending M7.3 | Preview/commented flags differ from registry-confirmed shape. Not live in NB04. M7.3 must verify. |

## Notebook 04 Source Edits Required by M7.2

**None required.**

The `fintech-backup-data` flag mismatch is a concern, but because those flags appear only
in printed previews and a commented optional example — never in live execution — they do
not create a correctness or source-safety issue in this issue. M7.3 must resolve the
mismatch before those preview cells can be registered as validated.

No other concrete incompatibilities, stale command surfaces, or source-safety issues were
found in Notebook 04.

## M7.3 Handoff: Registry and Contract Actions Required

M7.3 must:

1. **Add Notebook 04 to `notebook_cli_contracts.toml` `default_targets`** and add a new
   `[[commands]]` block for `stratlake-init-session` with the six observed flags.

2. **Add Notebook 04 to `notebook_cli_registry.toml` `default_targets`**.

3. **Add a new `[[commands]]` entry to `cli_command_registry.toml` for `stratlake-init-session`**:
   - `owner = "stratlake-trade-engine"`
   - `classifications = ["manual_only_live"]`
   - Flags: `--root`, `--project-name`, `--marketlake-root`, `--drive-root`,
     `--enable-drive-persistence` (boolean), `--notebook-configs` (boolean)
   - Verify all flags against upstream `stratlake-trade-engine` implementation.

4. **Update the `[[excluded_candidates]]` scope note** for `stratlake-trade-engine commands`
   to narrow it: `stratlake-init-session` is promoted to NB04 live scope; remaining
   StratLake commands remain excluded until their notebooks are imported.

5. **Verify `fintech-backup-data pack` and `restore` preview flags** against the current
   `fintech-market-ingestion` TestPyPI release:
   - Confirm whether `--root`, `--dataset-root`, `--archive-id`, `--drive-root`,
     `--copy-policy`, `--validate-after-copy`, `--inspect-after-copy` are valid flags
     for the installed version.
   - If the upstream CLI has been updated, update `cli_command_registry.toml` entries
     for `fintech-backup-data pack` and `restore` accordingly.
   - If the preview flags are invalid for the installed CLI, update the NB04 preview
     strings to use the registry-confirmed shapes while preserving the preview intent.

6. **Extend `confirmed_from` for `fintech-init-project`** in `cli_command_registry.toml`
   to include NB04.

7. **Do not** register `fintech-save-session`, `stratlake-build-features`,
   `stratlake-session-export`, `stratlake-session-import`,
   `stratlake-session-archive-bootstrap`, or `stratlake-session-archive-restore-bootstrap`
   as live NB04 commands. These remain availability-check-only for this notebook.

8. **Do not** register `fintech-restore-session` in any NB04 context.

## Validation Results

| Script | Result |
|---|---|
| `python scripts/check_notebooks_no_outputs.py notebooks` | ✅ Passed (5 notebooks) |
| `python scripts/scan_for_secret_patterns.py .` | ✅ Passed |
| `python scripts/validate_repo_cleanliness.py .` | ✅ Passed |
| `python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml` | ✅ Passed (no failures; NB04 not yet in targets — expected) |
| `python scripts/validate_notebook_cli_registry.py --config config/notebook_cli_registry.toml` | ✅ Passed (no failures; NB04 not yet in targets — expected) |

The CLI validators do not fail because Notebook 04 is not yet in `default_targets` for
either config file. That is expected; M7.3 owns adding NB04 to the target lists.

## Known Blockers for M7.3

1. **`fintech-backup-data pack/restore` flag mismatch** — the preview flags in NB04 differ
   from the registry-confirmed command shapes. M7.3 cannot register the preview surfaces
   without first resolving which shape is authoritative (the registry or the smoke-tested
   notebook). Verification against the current TestPyPI release is required.

2. **`stratlake-init-session` not yet in upstream source registry** — the command is
   smoke-test-confirmed but not yet traced to a confirmed upstream implementation file.
   M7.3 should confirm from `stratlake-trade-engine` source before adding a full
   `[[commands]]` entry.

## Go/No-Go for M7.3

| Gate | Status |
|---|---|
| All NB04 command surfaces identified from source | Go |
| Live commands (`fintech-init-project`, `stratlake-init-session`) confirmed from cell evidence | Go |
| Availability-check commands correctly classified (not live) | Go |
| Printed preview and optional manual commands correctly classified (not live) | Go |
| Future-orientation commands correctly classified (not live in NB04) | Go |
| `fintech-restore-session` not present and not reintroduced | Go |
| `fintech-backup-data` preview flag mismatch documented | Go |
| No smoke-tested commands removed without evidence | Go |
| No speculative flags added | Go |
| No flags inferred across unrelated subcommands | Go |
| M7.3 handoff list documented | Go |
| `fintech-backup-data pack/restore` flag verification pending | **Blocked — M7.3 must verify** |
| `stratlake-init-session` upstream source confirmation pending | **Blocked — M7.3 must verify** |
