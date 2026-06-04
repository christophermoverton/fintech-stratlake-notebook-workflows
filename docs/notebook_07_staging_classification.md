# Notebook 07 Staging Classification

## Purpose

Notebook 07 has been staged as cleaned repository source after M10.1. This document
classifies what is source-safe, manual runtime, conditional runtime, diagnostic,
preview-only, or deferred in the committed notebook.

The staged notebook is a **feature-consumption and baseline research-smoke** notebook. It
consumes the Notebook 06 Fintech → StratLake feature handoff outputs, runs a native
StratLake CLI strategy smoke test where available, and includes a notebook-local fallback
diagnostic as a non-authoritative secondary path. A final handoff summary points toward
Notebook 08 for formal strategy/backtest artifacts.

Staging classification describes the repository posture of each area. It is not a claim
that any live Colab runtime surface has been executed or validated.

---

## Staging status

| Property | Value |
|---|---|
| Target path | `notebooks/07_stratlake_feature_consumption_baseline_research.ipynb` |
| Source role | Feature consumption, baseline research smoke, archive checkpoint preview, Notebook 08 handoff |
| Total cells | 50 (23 markdown, 27 code) |
| Output-free | Yes — all code-cell outputs cleared |
| Execution counts reset | Yes — all execution counts set to `null` |
| Top-level Colab metadata stripped | Yes — `colab` key removed; only `kernelspec` and `language_info` retained |
| Cell-level metadata minimized | Yes — all cell `metadata` fields set to `{}` |
| Drive root guarded | Yes — `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` placeholder with `raise ValueError` guard in cells 08 and 14 |
| Archive checkpoint default | `CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION = False` (changed from `True` in M10.1) |
| Hardcoded private Drive path | Removed — replaced by `DRIVE_FOLDER_NAME` placeholder pattern |
| Generated artifacts committed | None |

---

## Staging classification table

| Area | Staging classification | Reason | Follow-up issue |
|---|---|---|---|
| Notebook 07 source import | `repository_source_only` | Notebook staged at target path; output-free, metadata clean, Drive root guarded, archive off-by-default | M10.1 complete |
| Command/runtime surface classification | `documentation` | Every major command, runtime, and diagnostic surface classified by category and default behavior | M10.2 (this issue) |
| CLI/source contract coverage | `source_only_static_coverage` | Static checks for command shape and flag syntax; no live registry or end-to-end verification | M10.3 |
| Source-only readiness checks | `source_hygiene_validation` | Notebook execution-readiness script; source hygiene scan; no live cell execution | M10.4 |
| Docs/index/README updates | `documentation` | Update repository-level index or README to reference Notebook 07 | M10.5 |
| Colab smoke | `live_manual_validation` | Live Colab runtime execution; result recording; smoke completion stance | M10.6 |
| Merge readiness | `final_milestone_gate` | Final review, PR checks, merge to main | M10.7 |

---

## Manual runtime surfaces

The following surfaces require live Colab or local runtime execution. None are validated by
committed source checks alone.

| Surface | Classification | Default |
|---|---|---|
| `!pip install` — package installs (cells 01–02) | `live_manual_runtime` | Runs on fresh runtime |
| `drive.mount("/content/drive")` — Google Drive mount (cell 06) | `live_manual_runtime` | Colab-only; no-op outside Colab |
| Alpaca credential prompts — `userdata` / `getpass` (cell 16) | `live_manual_runtime` | Prompts at runtime; no committed values |
| `fintech-init-project` — Fintech session initialization (cell 10) | `live_manual_runtime` | Runs unless `FINTECH_SESSION_ID_OVERRIDE` is set |
| `stratlake-init-session` — StratLake session initialization (cell 12) | `live_manual_runtime` | Runs unless `STRATLAKE_SESSION_ID_OVERRIDE` is set |
| `fintech-backup-data restore` — optional Fintech archive restore (cell 18) | `optional_commented_manual_restore` | `RESTORE_FINTECH_ARCHIVE = False`; preview-only by default |
| `stratlake-session-archive-restore-bootstrap` — optional StratLake restore (cell 18) | `optional_commented_manual_restore` | `RESTORE_STRATLAKE_ARCHIVE = False`; preview-only by default |
| `fintech-backfill-daily` — optional daily-bars backfill (cell 25) | `live_manual_runtime_conditional` | Runs when `RUN_SMALL_DAILY_BARS_BACKFILL = True` and bars are missing |
| `stratlake-build-features` — optional feature build (cell 31) | `live_manual_runtime_conditional` | Runs when `RUN_FEATURE_BUILD_IF_MISSING = True` and features are missing |
| `stratlake-run-strategy` — native strategy smoke test (cell 37) | `native_strategy_smoke` + `live_manual_runtime` | Runs when `RUN_NATIVE_BASELINE_SMOKE = True` and `configs/strategies.yml` exists |
| `stratlake-session-export --dry-run` — dry-run session export (cell 45) | `live_manual_runtime_dry_run` | Runs by default; catches `FileNotFoundError` gracefully |
| `stratlake-session-archive-bootstrap` — optional archive checkpoint (cell 47) | `preview_manual_guidance` + `source_hygiene_guard` | `CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION = False`; preview-only by default |

---

## Notebook-local and diagnostic surfaces

The following surfaces run inside the notebook Python environment and are classified
as inspection, diagnostic, or visualization only.

| Surface | Classification | Notes |
|---|---|---|
| CLI availability checks (cell 04) | `availability_check_only` | Detects command presence; does not prove contract behavior |
| `DRIVE_FOLDER_NAME` placeholder + `raise ValueError` guards (cells 08, 14) | `source_hygiene_guard` | Repository safety; user must set `DRIVE_FOLDER_NAME` before Drive folder creation |
| Session path / Drive path construction (cells 08, 14) | `notebook_python_runtime` | Path variables computed from session IDs and Drive root |
| Config file presence check (cell 20) | `runtime_inspection` | Raises `FileNotFoundError` if `universe.yml` or `paths.yml` is absent |
| Daily-bar parquet discovery and coverage (cells 22–23, 26) | `runtime_inspection` | Scans `MARKETLAKE_ROOT`; no files created |
| Feature parquet discovery (cells 28) | `runtime_inspection` | Scans candidate roots under `STRATLAKE_ROOT`; no files created |
| Sample loading and Q1 filtering (cells 33, 35) | `runtime_inspection` + `notebook_python_runtime` | Loads parquet samples for downstream diagnostics |
| NaN coverage diagnostic (cell 35) | `runtime_inspection` | Reports feature NaN fractions for Q1 analysis window |
| Native smoke stdout parsing and artifact discovery (cell 37) | `notebook_python_runtime` | Parses stable human-readable CLI output; does not re-implement strategy logic |
| Native smoke outcome display (cell 38) | `runtime_inspection` | Summary DataFrame of native smoke status; `fallback_needed` field |
| Fallback feature/forward-return merge diagnostic (cell 40) | `fallback_diagnostic_only` | Runs only when native smoke did not complete; explicitly non-canonical |
| Smoke-test plot (cell 41) | `runtime_visualization` | No committed plot output |
| Strategy/backtest command discovery (cell 43) | `availability_check_only` + `preview_manual_guidance` | Availability guidance only; not registry confirmation |
| Handoff summary dictionary (cell 49) | `notebook_python_runtime` + `runtime_inspection` | Runtime JSON summary; not committed |

---

## Repository source exclusions

The following items must not appear in committed Notebook 07 source.

- Executed cell outputs (stdout, stderr, display output)
- Non-null execution counts
- Colab top-level metadata (`colab` key)
- Cell-level runtime metadata (Colab IDs, widget state)
- Generated plots or inline figures
- Displayed DataFrame tables
- Feature parquet files
- Daily-bar parquet files
- Session manifests or session JSON files
- Archive packs or backup pack directories
- Restored data files
- API credentials or private key values
- Hardcoded private Drive folder paths
- Colab runtime state or profile data
- Execution logs or output logs
- Screenshots or screen captures
- Runtime JSON summaries
- Any generated artifacts from live cell execution

All of these exclusions were verified as absent in the M10.1 staged source. Validation
commands `scan_for_secret_patterns.py`, `check_notebooks_no_outputs.py`, and
`validate_repo_cleanliness.py` confirm this at the repository level.

---

## M10.2 completion stance

`notebook_07_command_runtime_surfaces_classified`

All major Notebook 07 command, runtime, native strategy-smoke, fallback diagnostic,
restore/export/archive, and visualization surfaces have been classified in
`docs/notebook_07_command_surface_classification.md`. Staging posture, manual runtime
boundaries, and repository source exclusions are documented in this file.

No notebook cells were modified in M10.2. No generated runtime artifacts were committed.
Colab smoke validation remains deferred to M10.6.
