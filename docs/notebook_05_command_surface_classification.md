# Notebook 05 Command Surface Classification

## Purpose

This document records the M8.2 command-surface classification for
`notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb`
before Notebook 05 CLI contract and registry coverage is added in M8.3.

Notebook 05 is the first imported notebook in the series that performs live Fintech
daily-bars ingestion and live StratLake feature generation in a manual Colab runtime.
This classification separates live runtime commands from dry-run commands, preview
guidance, optional commented restore/archive examples, availability checks, and
notebook-side Python runtime side effects.

## Scope

Notebook 05 preserves the conservative Q1 feature-generation tutorial imported in M8.1:

- Fintech remains the upstream curated daily-bars provider.
- StratLake remains the downstream feature/research workspace.
- `MARKETLAKE_ROOT` remains the explicit Fintech-to-StratLake handoff.
- `FINTECH_SESSION_ID` and `STRATLAKE_SESSION_ID` remain distinct.
- The Q1 window remains `2025-01-01` through `2025-04-01`.

Repository validation for Notebook 05 remains source-only and sanitized. It must not
execute live Colab, Google Drive, package install, credential, ingestion, feature-build,
export, archive, restore, or runtime data-inspection workflows.

## Classification Legend

| Classification | Meaning |
|---|---|
| `live_manual_runtime` | Command intentionally executed by Notebook 05 during manual Colab runtime. |
| `live_manual_runtime_dry_run` | Command intentionally executed by Notebook 05 during manual runtime, but only in dry-run mode. |
| `preview_manual_guidance` | Command printed or shown as a preview for the user to inspect before manually uncommenting or running. |
| `optional_commented_manual_restore` | Restore/archive command present only as a commented example or optional manual guidance. |
| `availability_check_only` | Command appears only in `shutil.which(...)` or the command checklist and is not live Notebook 05 execution. |
| `notebook_python_runtime` | Notebook-side Python runtime surface with side effects or runtime dependency, such as `.mkdir(...)`, `.write_text(...)`, `os.chdir(...)`, file discovery, Drive checks, or credential prompts. |
| `contract_mismatch_or_unverified` | Command form appears stale, older-looking, or not yet confirmed against the current upstream CLI contract. |

## Notebook Runtime Boundary

Repository validation must not:

- install packages,
- mount Google Drive,
- prompt for credentials,
- create Drive folders,
- write runtime ticker/config files,
- run `fintech-init-project`,
- run `stratlake-init-session`,
- run `fintech-backfill-daily`,
- run `stratlake-build-features`,
- run `stratlake-session-export`,
- create archives,
- restore archives,
- inspect live runtime data,
- generate features.

These operations remain manual Colab-runtime surfaces. Local repository checks should
only inspect source, notebook hygiene, and static command forms.

## Command Classification Table

| Command / surface | Source location / section | Observed form | Classification | Live in Notebook 05? | Side effects | Registry / contract action for M8.3 | Notes / blockers |
|---|---|---|---|---|---|---|---|
| `pip install pandas-market-calendars` | Cell `729b15e6`; Install required presentation packages | `!pip install "pandas-market-calendars>=5.0"` | `live_manual_runtime` | Yes, manual Colab only | Installs package into runtime | Keep ignored by registry validators; repository validation skips package install | Network/package install; not a repo validation command. |
| `pip install fintech-market-ingestion` | Cell `729b15e6`; Install required presentation packages | `!pip install -i https://test.pypi.org/simple/ fintech-market-ingestion` | `live_manual_runtime` | Yes, manual Colab only | Installs upstream Fintech CLI package | Keep ignored by registry validators; repository validation skips package install | Network/package install; version surface is not validated here. |
| `pip install stratlake-trade-engine` | Cell `729b15e6`; Install required presentation packages | `!pip install -i https://test.pypi.org/simple/ stratlake-trade-engine` | `live_manual_runtime` | Yes, manual Colab only | Installs upstream StratLake CLI package | Keep ignored by registry validators; repository validation skips package install | Network/package install; version surface is not validated here. |
| `shutil.which(...)` command checklist | Cell `f36c9ea9`; Verify required CLI commands | Checks `fintech-init-project`, `fintech-backfill-daily`, `fintech-save-session`, `fintech-restore-session`, `fintech-backup-data`, `stratlake-init-session`, `stratlake-build-features`, `stratlake-session-export`, `stratlake-session-import`, `stratlake-session-archive-bootstrap`, `stratlake-session-archive-restore-bootstrap` | `availability_check_only` | No | Prints local command paths only | Do not treat checklist presence as live command scope | `fintech-restore-session`, `fintech-save-session`, `stratlake-session-import`, and archive commands are availability-only unless separately used below. |
| `drive.mount("/content/drive")` | Cell `99822946`; Authorize Google Drive access | `from google.colab import drive`; `drive.mount("/content/drive")` | `notebook_python_runtime` | Yes, manual Colab only | Mounts Google Drive into Colab runtime | Exclude from CLI registry; keep skipped in source validation | Runtime authorization surface; never repository validation. |
| Drive root placeholder guard | Cell `876835f0`; Define shared Fintech and StratLake paths | `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` guard before `DRIVE_ROOT` use | `notebook_python_runtime` | Yes, manual Colab path setup | Raises until user sets Drive folder name | No CLI registry action | Source-safety guard added in M8.1; keeps Drive from becoming active app workspace. |
| `fintech-init-project` | Cell `bce5c87a`; Initialize the Fintech project session | `!fintech-init-project --root {FINTECH_ROOT.as_posix()} --notebooks --with-session --session-name {FINTECH_SESSION_NAME}` | `live_manual_runtime` | Yes | Creates Fintech `/content` workspace/session manifest | Add NB05 as source-visible live command; confirm existing flags and extend `confirmed_from`/targets | Same command shape as prior notebooks; live init remains manual Colab only. |
| `stratlake-init-session` | Cell `3dd31cc7`; Initialize the StratLake project session | `!stratlake-init-session --root ... --project-name ... --marketlake-root ... --drive-root ... --enable-drive-persistence --notebook-configs` | `live_manual_runtime` | Yes | Creates StratLake `/content` session and notebook configs | Add NB05 as source-visible live command; preserve `--marketlake-root`; source-verify upstream flags if still pending | Same NB04 shape; `--marketlake-root` is the critical Fintech-to-StratLake handoff. |
| StratLake config existence checks | Cell `Bd0ZSBoPx8gs`; Verify notebook config files | `.exists()` checks for `configs/universe.yml` and `configs/paths.yml` | `notebook_python_runtime` | Yes, after session init | Reads runtime filesystem; may raise if configs missing | No CLI registry action | Runtime verification only; not CLI execution. |
| `STRATLAKE_SESSION_ID` extraction | Cell `0d21ddaa`; Extract `STRATLAKE_SESSION_ID` | Reads `.stratlake/session.json`; `.exists()` then `json.loads(...)` | `notebook_python_runtime` | Yes, after session init | Reads generated session metadata | No CLI registry action | Preserves separate downstream session identity. |
| Drive session/archive `.mkdir(...)` | Cell `0b8e19df`; Create SESSION_ID-based Google Drive folders and archive IDs | Guards placeholder and Drive mount, then `path.mkdir(parents=True, exist_ok=True)` under Drive roots | `notebook_python_runtime` | Yes, manual Colab only | Creates Drive session/archive folders | No CLI registry action; keep skipped in sanitized execution | Drive is persistence/archive storage only, not active app workspace. |
| Drive session/path inspection | Cell `8d3dc4dc`; Optional: choose previous Drive sessions for restore | `.glob("*")`, `.is_dir()`, `.exists()` over Drive session/archive roots | `notebook_python_runtime` | Yes, optional runtime inspection | Reads mounted Drive folder structure | No CLI registry action | Does not restore or mutate data; depends on mounted Drive. |
| `STRATLAKE_TICKERS_FILE.write_text(...)` | Cell `ec58bcb9`; Prepare a StratLake ticker file | `STRATLAKE_CONFIGS_ROOT.mkdir(...)`; `STRATLAKE_TICKERS_FILE.write_text("AAPL\nMSFT\nNVDA\n", ...)` | `notebook_python_runtime` | Yes | Creates runtime config/ticker file under `/content` StratLake workspace | No CLI registry action | Generated runtime file must not be committed. |
| Colab secrets / Alpaca credential prompt | Cell `c1206418`; Configure Alpaca API credentials from Colab Secrets | `google.colab.userdata`; `getpass.getpass(...)`; sets `os.environ[...]` | `notebook_python_runtime` | Yes, manual Colab only | Reads credentials, sets runtime env vars | No CLI registry action; keep skipped in source validation | Does not print key/secret; repository validation must not prompt or read credentials. |
| `FINTECH_TICKERS_FILE.write_text(...)` | Cell `b7dea0a0`; Prepare the Fintech ticker file and daily bars output path | `FINTECH_CONFIGS_ROOT.mkdir(...)`; `FINTECH_TICKERS_FILE.write_text(...)` | `notebook_python_runtime` | Yes | Creates runtime ticker file under `/content` Fintech workspace | No CLI registry action | Generated runtime file must not be committed. |
| `DAILY_BARS_ROOT.mkdir(...)` | Cell `b7dea0a0`; Prepare the Fintech ticker file and daily bars output path | `DAILY_BARS_ROOT = MARKETLAKE_ROOT / "bars_daily"`; `.mkdir(...)` | `notebook_python_runtime` | Yes | Creates local curated-data output directory under `/content` | No CLI registry action | Keeps active data under local `/content` workspace. |
| Optional `fintech-backup-data restore` commented example | Cell `U74qVc08x8gu`; Optional: restore Fintech curated data before ingestion | Commented `# !fintech-backup-data restore --backup-pack-dir ... --restore-root ... --overwrite-policy fail` | `optional_commented_manual_restore` | No | None unless user manually uncomments in Colab | M8.3 updated this guidance to the registry-confirmed backup-pack restore shape | Do not reintroduce `fintech-restore-session` as the backup-pack restore path. |
| `fintech-backfill-daily` | Cell `a4dbb67a`; Extract Q1 daily bars into the local Fintech curated-data workspace | `!fintech-backfill-daily --symbols ... --start 2025-01-01 --end 2025-04-01 --out ... --feed iex --source session_{FINTECH_SESSION_ID} --window month` | `live_manual_runtime` | Yes | Calls Alpaca/data provider and writes curated daily bars under `/content` | Add NB05 live command coverage; validate flags and Q1 dates/source shape | This is live ingestion and must never run in repo validation. |
| Daily bars parquet inspection | Cell `ca096520`; Inspect extracted Q1 daily bars | `DAILY_BARS_ROOT.rglob("*.parquet")`; `.exists()` | `notebook_python_runtime` | Yes, after ingestion | Reads runtime generated data paths | No CLI registry action | Runtime data inspection only; repository validation must not inspect generated data. |
| `MARKETLAKE_ROOT.rglob("*.parquet")` | Cell `4879f15f`; Precheck the upstream curated-data root | `MARKETLAKE_ROOT.rglob("*.parquet")`; `.exists()` | `notebook_python_runtime` | Yes, before feature build | Reads Fintech curated-data workspace | No CLI registry action | Confirms input availability; does not generate data itself. |
| `fintech-backup-data pack` preview string | Cell `vqhdHkjVx8gu`; Optional: archive the Fintech Q1 curated-data input | Printed f-string: `fintech-backup-data pack --workspace-root ... --source-dataset-root ... --backup-root ... --backup-id ... --shard-size-mb 512` | `preview_manual_guidance` | No | Prints preview only | M8.3 updated this preview to the registry-confirmed pack shape and added static coverage | Archive pack creation remains manual guidance and must not run in repository validation. |
| Optional commented `fintech-backup-data pack` | Cell `vqhdHkjVx8gu`; Optional: archive the Fintech Q1 curated-data input | Commented `# !fintech-backup-data pack ...` with same registry-confirmed flags | `preview_manual_guidance` | No | None unless user manually uncomments in Colab | M8.3 updated this guidance to the registry-confirmed pack shape | Archive pack creation is manual guidance and must not run in repository validation. |
| `os.chdir(STRATLAKE_ROOT)` | Cell `ad8ee301`; Build Q1 daily features with StratLake | `os.chdir(STRATLAKE_ROOT)` before CLI invocation | `notebook_python_runtime` | Yes | Mutates runtime current working directory | No CLI registry action | Ensures relative StratLake outputs land under the intended `/content` workspace. |
| `stratlake-build-features` | Cell `ad8ee301`; Build Q1 daily features with StratLake | `!stratlake-build-features --timeframe 1D --start 2025-01-01 --end 2025-04-01 --tickers ... --marketlake-root ...` | `live_manual_runtime` | Yes | Generates StratLake feature outputs under `/content` StratLake workspace | Add NB05 live command coverage; verify upstream flags and `1D` timeframe value | First live feature-generation command in imported series; never repository validation. |
| Generated feature parquet inspection | Cell `a566d607`; Inspect generated StratLake feature files | `(STRATLAKE_ROOT / "data").rglob("*.parquet")` | `notebook_python_runtime` | Yes, after feature build | Reads generated feature outputs | No CLI registry action | Runtime output inspection only; generated files must stay out of Git. |
| `stratlake-session-export --dry-run` | Cell `773f1d97`; Optional: export the feature session snapshot to Drive | `!stratlake-session-export --root ... --drive-root ... --include-features --include-artifacts --include-configs --dry-run` | `live_manual_runtime_dry_run` | Yes, dry-run only | Should preview export plan without writing export payload | Add NB05 dry-run command coverage; verify flags and boolean/value semantics | Notebook 05 does not run a live export; only dry-run is source-visible. |
| `stratlake-session-archive-bootstrap` preview string | Cell `un9-BO0hx8gw`; Optional: archive the StratLake feature session | Printed f-string with `--root`, `--archive-id`, `--archive-collision-policy overwrite_allowed`, `--drive-root`, `--copy-policy overwrite_allowed`, include/validate/inspect flags | `preview_manual_guidance`; `contract_mismatch_or_unverified` | No | Prints archive preview only | M8.3 must verify command existence, flags, and allowed values before registry coverage | StratLake archive command remains unverified in current registry. |
| `stratlake-session-archive-restore-bootstrap` preview string | Cell `un9-BO0hx8gw`; Optional: archive the StratLake feature session | Printed f-string with `--root`, `--archive-id`, `--drive-root`, `--copy-policy overwrite_allowed`, include/validate/inspect flags | `preview_manual_guidance`; `contract_mismatch_or_unverified` | No | Prints restore preview only | M8.3 must verify command existence, flags, and allowed values before registry coverage | Restore preview only; not live Notebook 05 execution. |
| Optional commented `stratlake-session-archive-bootstrap` | Cell `un9-BO0hx8gw`; Optional: archive the StratLake feature session | Commented `# !stratlake-session-archive-bootstrap ...` | `preview_manual_guidance`; `contract_mismatch_or_unverified` | No | None unless user manually uncomments in Colab | Keep manual guidance unless intentionally promoted in a future issue | Would create archive artifacts if uncommented; not repository validation. |

## Availability-Check-Only Commands

The following commands appear in the `required_commands` checklist in cell `f36c9ea9`.
Checklist presence means only that the notebook expects them to be installed in the
manual Colab runtime. It does not make them live Notebook 05 execution.

| Command | Notebook 05 status | M8.3 action |
|---|---|---|
| `fintech-save-session` | `availability_check_only` | Keep out of live NB05 scope unless a separate source-visible command is added. |
| `fintech-restore-session` | `availability_check_only` | Keep excluded from backup-pack restore path; do not reintroduce as valid restore syntax for NB05. |
| `stratlake-session-import` | `availability_check_only` | Keep out of live NB05 scope. |

Other checklist commands have separate Notebook 05 surfaces:

- `fintech-init-project`: live runtime command.
- `fintech-backfill-daily`: live runtime command.
- `fintech-backup-data`: preview/commented pack/restore guidance only.
- `stratlake-init-session`: live runtime command.
- `stratlake-build-features`: live runtime command.
- `stratlake-session-export`: dry-run runtime command only.
- `stratlake-session-archive-bootstrap`: preview/commented archive guidance only.
- `stratlake-session-archive-restore-bootstrap`: preview restore guidance only.

## Contract Mismatch Or Unverified Surfaces

### `fintech-backup-data pack`

Notebook 05 still shows an older-looking pack preview/commented form:

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

The current registry-confirmed pack form from earlier milestones is:

```text
fintech-backup-data pack
  --workspace-root ...
  --source-dataset-root ...
  --backup-root ...
  --backup-id ...
  --shard-size-mb ...
```

M8.3 resolution: Notebook 05 was updated to the registry-confirmed pack form already used
by Notebook 04. Static validators now cover the printed pack preview source. This remains
manual guidance only and is not executed by repository validation.

### `fintech-backup-data restore`

Notebook 05 shows only a commented optional restore form:

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

The current registry-confirmed backup-pack restore form is:

```text
fintech-backup-data restore
  --backup-pack-dir ...
  --restore-root ...
  --overwrite-policy ...
```

M8.3 resolution: the optional commented restore guidance was updated to the
registry-confirmed backup-pack restore form. It remains commented manual guidance only.
`fintech-restore-session` must not be promoted as the backup-pack restore path.

### StratLake archive/export family

Notebook 05 uses `stratlake-session-export` only with `--dry-run`; M8.3 added static
coverage for that dry-run source shape. Notebook 05 still shows
`stratlake-session-archive-bootstrap` plus `stratlake-session-archive-restore-bootstrap`
only as printed/commented guidance. These archive/bootstrap surfaces remain deferred
pending current upstream StratLake CLI verification.

## M8.3 Resolution

Issue #63 completed the following:

- Added Notebook 05 to `config/notebook_cli_contracts.toml`.
- Added Notebook 05 to `config/notebook_cli_registry.toml`.
- Added static registry coverage for `stratlake-build-features`.
- Added static registry coverage for `stratlake-session-export --dry-run`.
- Extended existing source coverage for `fintech-init-project`, `fintech-backfill-daily`,
  `stratlake-init-session`, and `fintech-backup-data pack`.
- Corrected Notebook 05 Fintech backup pack and optional restore guidance to the
  registry-confirmed flag forms.
- Kept availability-check-only commands out of live Notebook 05 scope.
- Deferred StratLake archive/bootstrap preview validation until upstream command flags are
  verified.

## M8.3 Handoff

Issue #63 should:

- Add CLI contract/registry coverage for source-visible live Notebook 05 commands.
- Add Notebook 05 to CLI contract and registry default targets only after command shapes are resolved.
- Validate source shape for `fintech-init-project` in Notebook 05 and extend `confirmed_from` if unchanged.
- Validate source shape for `stratlake-init-session` in Notebook 05, preserving `--marketlake-root`.
- Validate source shape for `fintech-backfill-daily`, including `--symbols`, `--start 2025-01-01`, `--end 2025-04-01`, `--out`, `--feed iex`, `--source session_{FINTECH_SESSION_ID}`, and `--window month`.
- Validate source shape for `stratlake-build-features`, including `--timeframe 1D`, the Q1 date window, `--tickers`, and `--marketlake-root`.
- Validate source shape for `stratlake-session-export --dry-run` and keep it classified as dry-run only.
- Maintain `fintech-backup-data pack` and commented restore guidance on the registry-confirmed flag forms.
- Confirm `stratlake-session-archive-bootstrap` flags, including archive collision/copy policy values and include/validate/inspect flags.
- Confirm `stratlake-session-archive-restore-bootstrap` flags and policy values.
- Keep availability-check-only commands out of live Notebook 05 command scope.
- Keep commented restore/archive examples classified as manual guidance unless intentionally promoted.
- Keep repository validation non-executing for package install, Drive, credentials, ingestion, feature generation, export, archive, restore, and runtime data inspection.

## Non-Claims

M8.2 did not:

- run any Notebook 05 CLI command,
- install packages,
- mount Google Drive,
- read Alpaca credentials,
- call Alpaca,
- generate daily bars,
- generate features,
- create archives,
- restore archives,
- validate live Colab runtime behavior,
- update Notebook 05 CLI registry or contract configs,
- claim manual Colab smoke success.

This document is a source classification and M8.3 handoff only.
