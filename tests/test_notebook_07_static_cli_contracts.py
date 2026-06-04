"""
Static CLI contract and source invariant tests for Notebook 07.

These tests parse the committed notebook source and verify expected command
references, source guards, native strategy-smoke workflow references, fallback
diagnostic labeling, archive/restore defaults, and structural invariants.

Scope (M10.3):
- Source text substring and structural checks only.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages on PATH are required.
- No network, Google Drive, Alpaca credentials, or generated data are required.
- No live Colab runtime is required.

Classification note:
Command-discovery candidates (stratlake-run-strategy, stratlake-backtest, etc.)
are verified as source text references only.  These tests do not confirm that
those commands are installed or that their contracts are correct.

Archive/bootstrap command references (stratlake-session-archive-bootstrap,
stratlake-session-archive-restore-bootstrap) are verified as source references
and guard-behavior checks only.  These tests do not confirm upstream command
contracts or live archive/restore success.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB07_PATH = REPO_ROOT / "notebooks" / "07_stratlake_feature_consumption_baseline_research.ipynb"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def notebook() -> dict:
    return json.loads(NB07_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def notebook_source(notebook: dict) -> str:
    """Full source text of all cells joined for substring search."""
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )


@pytest.fixture(scope="module")
def code_source(notebook: dict) -> str:
    """Full source text of code cells only."""
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    )


@pytest.fixture(scope="module")
def markdown_source(notebook: dict) -> str:
    """Full source text of markdown cells only."""
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown"
    )


# ---------------------------------------------------------------------------
# Notebook path invariant
# ---------------------------------------------------------------------------


def test_notebook_07_path_exists() -> None:
    assert NB07_PATH.exists(), (
        f"Notebook 07 not found at {NB07_PATH}. "
        "M10.1 must stage the notebook before M10.3 static checks can run."
    )


# ---------------------------------------------------------------------------
# Source-only safety invariants (structural)
# ---------------------------------------------------------------------------


def test_no_committed_outputs(notebook: dict) -> None:
    for i, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") == "code":
            assert cell.get("outputs", []) == [], (
                f"Cell {i} has committed outputs. "
                "M10.1 must clear all cell outputs before the notebook is committed."
            )


def test_no_non_null_execution_counts(notebook: dict) -> None:
    for i, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") == "code":
            assert cell.get("execution_count") is None, (
                f"Cell {i} has a non-null execution_count. "
                "M10.1 must reset all execution counts to null."
            )


def test_no_top_level_colab_metadata(notebook: dict) -> None:
    assert "colab" not in notebook.get("metadata", {}), (
        "Top-level 'colab' metadata must be stripped for repository source safety."
    )


def test_notebook_cell_count(notebook: dict) -> None:
    cells = notebook.get("cells", [])
    assert len(cells) == 50, (
        f"Expected 50 cells (23 markdown + 27 code), got {len(cells)}. "
        "Structural deviation from the M10.1 staged source must be documented."
    )


def test_code_cell_count(notebook: dict) -> None:
    code_cells = [c for c in notebook.get("cells", []) if c.get("cell_type") == "code"]
    assert len(code_cells) == 27, (
        f"Expected 27 code cells, got {len(code_cells)}."
    )


def test_markdown_cell_count(notebook: dict) -> None:
    md_cells = [c for c in notebook.get("cells", []) if c.get("cell_type") == "markdown"]
    assert len(md_cells) == 23, (
        f"Expected 23 markdown cells, got {len(md_cells)}."
    )


# ---------------------------------------------------------------------------
# Core Fintech CLI references
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", [
    "fintech-init-project",
    "fintech-backfill-daily",
    "fintech-save-session",
    "fintech-restore-session",
    "fintech-backup-data",
])
def test_fintech_cli_reference_present(notebook_source: str, command: str) -> None:
    assert command in notebook_source, (
        f"Expected Fintech CLI reference '{command}' not found in Notebook 07 source. "
        "This is a source contract check — the command must appear as a reference or "
        "availability check. It does not require the command to be installed."
    )


def test_fintech_backup_data_restore_verb_present(code_source: str) -> None:
    """fintech-backup-data restore must appear in the optional Fintech restore preview."""
    assert "fintech-backup-data" in code_source
    assert '"restore"' in code_source or "'restore'" in code_source, (
        "fintech-backup-data 'restore' subcommand reference must appear in the "
        "optional restore preview cell."
    )


# ---------------------------------------------------------------------------
# Core StratLake CLI references
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", [
    "stratlake-init-session",
    "stratlake-build-features",
    "stratlake-session-export",
    "stratlake-session-import",
    "stratlake-session-archive-bootstrap",
    "stratlake-session-archive-restore-bootstrap",
])
def test_stratlake_cli_reference_present(notebook_source: str, command: str) -> None:
    assert command in notebook_source, (
        f"Expected StratLake CLI reference '{command}' not found in Notebook 07 source. "
        "This is a source reference check only — not a claim that the command is "
        "installed or that its contract is confirmed."
    )


# ---------------------------------------------------------------------------
# Native strategy smoke references
# ---------------------------------------------------------------------------


def test_run_native_baseline_smoke_default_true(code_source: str) -> None:
    assert "RUN_NATIVE_BASELINE_SMOKE = True" in code_source, (
        "RUN_NATIVE_BASELINE_SMOKE must default to True in Notebook 07 source. "
        "The native strategy smoke test is the preferred validation path."
    )


def test_native_strategy_name_momentum_v1(code_source: str) -> None:
    assert 'NATIVE_STRATEGY_NAME = "momentum_v1"' in code_source, (
        "NATIVE_STRATEGY_NAME must be set to 'momentum_v1' in Notebook 07 source."
    )


def test_strategy_start_equals_analysis_start(code_source: str) -> None:
    assert "STRATEGY_START = ANALYSIS_START" in code_source, (
        "STRATEGY_START must equal ANALYSIS_START so the native smoke test uses "
        "the Q1 analysis window, not the padded backfill/build window."
    )


def test_strategy_end_equals_analysis_end(code_source: str) -> None:
    assert "STRATEGY_END = ANALYSIS_END" in code_source, (
        "STRATEGY_END must equal ANALYSIS_END so the native smoke test uses "
        "the Q1 analysis window."
    )


def test_stratlake_run_strategy_reference(notebook_source: str) -> None:
    assert "stratlake-run-strategy" in notebook_source, (
        "stratlake-run-strategy must appear in Notebook 07 as the native strategy smoke "
        "command. This is a source reference check — not a claim that the command is "
        "installed or that the smoke test has passed."
    )


def test_native_smoke_strategies_config_flag(code_source: str) -> None:
    assert "--strategies-config" in code_source, (
        "Native strategy smoke command must reference --strategies-config flag."
    )


def test_native_smoke_strategy_flag(code_source: str) -> None:
    assert '"--strategy"' in code_source, (
        "Native strategy smoke command must reference --strategy flag."
    )


def test_native_smoke_start_flag(code_source: str) -> None:
    assert '"--start"' in code_source, (
        "Native strategy smoke command must reference --start flag."
    )


def test_native_smoke_end_flag(code_source: str) -> None:
    assert '"--end"' in code_source, (
        "Native strategy smoke command must reference --end flag."
    )


def test_native_smoke_completed_variable_present(code_source: str) -> None:
    assert "native_smoke_completed" in code_source, (
        "native_smoke_completed must be tracked. It gates whether the fallback "
        "diagnostic is needed."
    )


def test_run_notebook_local_fallback_smoke_derived_from_native(code_source: str) -> None:
    assert "RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE = not native_smoke_completed" in code_source, (
        "RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE must be set to 'not native_smoke_completed'. "
        "This ensures the fallback diagnostic only runs when the native smoke did not complete."
    )


# ---------------------------------------------------------------------------
# Strategy/backtest command discovery candidates (source references only)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("candidate", [
    "stratlake-run-strategy",
    "stratlake-backtest",
    "stratlake-run-backtest",
    "python -m src.cli.run_strategy",
    "python -m src.cli.backtest",
])
def test_strategy_discovery_candidate_present_as_source_reference(
    notebook_source: str, candidate: str
) -> None:
    assert candidate in notebook_source, (
        f"Strategy/backtest discovery candidate '{candidate}' not found in Notebook 07 "
        "source. These candidates are availability guidance only — not confirmed installed "
        "commands and not treated as registry-verified CLI coverage in M10.3."
    )


# ---------------------------------------------------------------------------
# Drive guard invariants (source hygiene)
# ---------------------------------------------------------------------------


def test_drive_folder_name_placeholder_present(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source, (
        "DRIVE_FOLDER_NAME must use the placeholder pattern. "
        "Hardcoded Drive folder names are a source hygiene violation (M10.1)."
    )


def test_drive_root_uses_drive_folder_name_variable(code_source: str) -> None:
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source, (
        "DRIVE_ROOT must be constructed from DRIVE_FOLDER_NAME, not a hardcoded path."
    )


def test_drive_folder_name_raise_value_error_guard(code_source: str) -> None:
    assert (
        'raise ValueError("Set DRIVE_FOLDER_NAME before creating Google Drive session/archive folders.")'
        in code_source
    ), (
        "A ValueError guard for DRIVE_FOLDER_NAME == 'REPLACE_WITH_DRIVE_FOLDER_NAME' "
        "must appear before any Drive folder creation."
    )


def test_no_hardcoded_tutorial_drive_path(notebook_source: str) -> None:
    assert "/content/drive/MyDrive/fintech-stratlake-tutorial" not in notebook_source, (
        "Hardcoded private Drive path '/content/drive/MyDrive/fintech-stratlake-tutorial' "
        "must not appear in Notebook 07 source. "
        "Use DRIVE_FOLDER_NAME placeholder instead (M10.1 source hygiene)."
    )


def test_no_hardcoded_fintech_stratlake_tutorial_string_in_code(code_source: str) -> None:
    assert '"fintech-stratlake-tutorial"' not in code_source, (
        "Hardcoded Drive folder name 'fintech-stratlake-tutorial' must not appear "
        "as a string literal in Notebook 07 code cells."
    )


# ---------------------------------------------------------------------------
# Archive checkpoint safety invariants
# ---------------------------------------------------------------------------


def test_archive_checkpoint_default_false(code_source: str) -> None:
    assert "CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION = False" in code_source, (
        "CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION must default to False. "
        "M10.1 source hygiene changed this from True to protect against accidental "
        "archive creation from committed source."
    )


def test_archive_checkpoint_not_default_true(code_source: str) -> None:
    assert "CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION = True" not in code_source, (
        "CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION must NOT be True in committed source. "
        "Setting it to True is a deliberate manual action at runtime."
    )


def test_archive_bootstrap_reference(notebook_source: str) -> None:
    assert "stratlake-session-archive-bootstrap" in notebook_source, (
        "stratlake-session-archive-bootstrap must appear in Notebook 07 as the archive "
        "command reference. This is a source reference check — not registry confirmation."
    )


@pytest.mark.parametrize("flag", [
    "--archive-id",
    "--archive-collision-policy",
    "--drive-root",
    "--copy-policy",
    "--include-features",
    "--include-artifacts",
    "--include-configs",
    "--validate-after-copy",
    "--inspect-after-copy",
])
def test_archive_bootstrap_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source, (
        f"Archive bootstrap flag '{flag}' not found in Notebook 07 code source. "
        "The archive command preview must preserve expected flag shape."
    )


def test_archive_checkpoint_preview_text_present(notebook_source: str) -> None:
    assert "CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION=True" in notebook_source, (
        "Archive checkpoint preview text referencing "
        "'CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION=True' must be present "
        "so users know how to enable archive creation manually."
    )


# ---------------------------------------------------------------------------
# Dry-run export invariants
# ---------------------------------------------------------------------------


def test_session_export_reference(notebook_source: str) -> None:
    assert "stratlake-session-export" in notebook_source, (
        "stratlake-session-export must appear in Notebook 07."
    )


def test_session_export_dry_run_flag_present(code_source: str) -> None:
    assert '"--dry-run"' in code_source, (
        "stratlake-session-export must use '--dry-run' in Notebook 07. "
        "The export cell is classified as live_manual_runtime_dry_run."
    )


@pytest.mark.parametrize("flag", ["--include-features", "--include-artifacts", "--include-configs"])
def test_session_export_include_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source, (
        f"Dry-run export must include flag '{flag}'."
    )


def test_session_export_uses_drive_session_root_str(code_source: str) -> None:
    assert "STRATLAKE_DRIVE_SESSION_ROOT_STR" in code_source, (
        "Dry-run export must use STRATLAKE_DRIVE_SESSION_ROOT_STR for the Drive destination."
    )


def test_session_export_file_not_found_handling(code_source: str) -> None:
    assert "FileNotFoundError" in code_source, (
        "Export cell must handle FileNotFoundError for package versions that do not "
        "expose stratlake-session-export."
    )


# ---------------------------------------------------------------------------
# Restore preview invariants
# ---------------------------------------------------------------------------


def test_restore_fintech_archive_default_false(code_source: str) -> None:
    assert "RESTORE_FINTECH_ARCHIVE = False" in code_source, (
        "RESTORE_FINTECH_ARCHIVE must default to False. "
        "Fintech archive restore is preview/manual only."
    )


def test_restore_stratlake_archive_default_false(code_source: str) -> None:
    assert "RESTORE_STRATLAKE_ARCHIVE = False" in code_source, (
        "RESTORE_STRATLAKE_ARCHIVE must default to False. "
        "StratLake archive restore is preview/manual only."
    )


def test_stratlake_restore_bootstrap_reference(notebook_source: str) -> None:
    assert "stratlake-session-archive-restore-bootstrap" in notebook_source, (
        "stratlake-session-archive-restore-bootstrap must appear in Notebook 07 "
        "as the restore preview reference."
    )


def test_restore_validate_after_copy_flag(code_source: str) -> None:
    assert "--validate-after-copy" in code_source, (
        "--validate-after-copy must appear in the restore command preview."
    )


def test_restore_inspect_after_copy_flag(code_source: str) -> None:
    assert "--inspect-after-copy" in code_source, (
        "--inspect-after-copy must appear in the restore command preview."
    )


def test_restore_is_guarded_by_boolean(code_source: str) -> None:
    """Restore execution must be guarded by the false-default boolean flags."""
    assert "if RESTORE_FINTECH_ARCHIVE:" in code_source, (
        "Fintech restore must be gated by 'if RESTORE_FINTECH_ARCHIVE:'."
    )
    assert "if RESTORE_STRATLAKE_ARCHIVE:" in code_source, (
        "StratLake restore must be gated by 'if RESTORE_STRATLAKE_ARCHIVE:'."
    )


# ---------------------------------------------------------------------------
# Fallback diagnostic labeling invariants
# ---------------------------------------------------------------------------


def test_fallback_section_referenced_in_markdown(markdown_source: str) -> None:
    assert "fallback" in markdown_source.lower(), (
        "At least one markdown cell must describe the fallback diagnostic section. "
        "The fallback must be clearly labeled as secondary and non-authoritative."
    )


def test_fallback_source_label_present(code_source: str) -> None:
    assert "notebook_local_fallback_diagnostic" in code_source, (
        "Fallback diagnostic source must be labeled 'notebook_local_fallback_diagnostic'. "
        "This label distinguishes fallback output from native strategy smoke output."
    )


def test_fallback_strategy_label_present(code_source: str) -> None:
    assert "feature_rank_fallback" in code_source, (
        "Fallback diagnostic strategy must be labeled 'feature_rank_fallback'. "
        "This label distinguishes fallback logic from canonical strategy/backtest logic."
    )


def test_fallback_depends_on_run_notebook_local_fallback_smoke(code_source: str) -> None:
    assert "RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE" in code_source, (
        "Fallback diagnostic must depend on RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE."
    )


def test_fallback_not_unconditional(code_source: str) -> None:
    assert "if not RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE:" in code_source, (
        "Fallback diagnostic must be guarded by "
        "'if not RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE:' to skip when native smoke completes."
    )


# ---------------------------------------------------------------------------
# Notebook 08 handoff invariant
# ---------------------------------------------------------------------------


def test_notebook_08_handoff_reference(notebook_source: str) -> None:
    assert "Notebook 08" in notebook_source, (
        "Final handoff summary must reference Notebook 08. "
        "Notebook 07 is a smoke/consumption notebook; formal strategy/backtest "
        "artifacts are deferred to Notebook 08."
    )


def test_notebook_08_handoff_describes_formal_artifacts(notebook_source: str) -> None:
    assert "Formal StratLake strategy/backtest artifacts" in notebook_source, (
        "Final handoff must explicitly describe Notebook 08 as the destination for "
        "formal StratLake strategy/backtest artifacts using package APIs/CLI."
    )


# ---------------------------------------------------------------------------
# Analysis window and key configuration values
# ---------------------------------------------------------------------------


def test_analysis_start_value(code_source: str) -> None:
    assert 'ANALYSIS_START = "2026-01-02"' in code_source, (
        "ANALYSIS_START must be '2026-01-02' in Notebook 07."
    )


def test_analysis_end_value(code_source: str) -> None:
    assert 'ANALYSIS_END = "2026-03-31"' in code_source, (
        "ANALYSIS_END must be '2026-03-31' in Notebook 07."
    )


def test_backfill_start_value(code_source: str) -> None:
    assert 'BACKFILL_START = "2025-11-03"' in code_source, (
        "BACKFILL_START must be '2025-11-03' (Q1 warmup window)."
    )


def test_backfill_end_value(code_source: str) -> None:
    assert 'BACKFILL_END = "2026-04-15"' in code_source, (
        "BACKFILL_END must be '2026-04-15' (forward-return buffer)."
    )


def test_backfill_symbols_value(code_source: str) -> None:
    assert "AAPL,MSFT,NVDA,SPY,QQQ" in code_source, (
        "BACKFILL_SYMBOLS must include AAPL,MSFT,NVDA,SPY,QQQ."
    )


def test_feature_build_start_equals_backfill_start(code_source: str) -> None:
    assert "FEATURE_BUILD_START = BACKFILL_START" in code_source, (
        "FEATURE_BUILD_START must equal BACKFILL_START so the build window "
        "covers the full warmup period."
    )


def test_feature_build_end_equals_backfill_end(code_source: str) -> None:
    assert "FEATURE_BUILD_END = BACKFILL_END" in code_source, (
        "FEATURE_BUILD_END must equal BACKFILL_END so the build window "
        "covers the forward-return buffer."
    )


# ---------------------------------------------------------------------------
# Session name values
# ---------------------------------------------------------------------------


def test_fintech_session_name(code_source: str) -> None:
    assert 'FINTECH_SESSION_NAME = "fintech_stratlake_input"' in code_source, (
        "FINTECH_SESSION_NAME must be 'fintech_stratlake_input' in Notebook 07."
    )


def test_stratlake_session_name(code_source: str) -> None:
    assert 'STRATLAKE_SESSION_NAME = "stratlake_q1_feature_consumption"' in code_source, (
        "STRATLAKE_SESSION_NAME must be 'stratlake_q1_feature_consumption' in Notebook 07."
    )


def test_fintech_session_id_override_empty_string(code_source: str) -> None:
    assert 'FINTECH_SESSION_ID_OVERRIDE = ""' in code_source, (
        "FINTECH_SESSION_ID_OVERRIDE must default to empty string."
    )


def test_stratlake_session_id_override_empty_string(code_source: str) -> None:
    assert 'STRATLAKE_SESSION_ID_OVERRIDE = ""' in code_source, (
        "STRATLAKE_SESSION_ID_OVERRIDE must default to empty string."
    )


# ---------------------------------------------------------------------------
# Key path variables
# ---------------------------------------------------------------------------


def test_marketlake_root_reference(code_source: str) -> None:
    assert "MARKETLAKE_ROOT" in code_source, (
        "MARKETLAKE_ROOT must be defined in Notebook 07 as the Fintech → StratLake handoff."
    )


def test_daily_bars_root_reference(code_source: str) -> None:
    assert "DAILY_BARS_ROOT" in code_source, (
        "DAILY_BARS_ROOT must be defined in Notebook 07."
    )


def test_features_daily_root_reference(code_source: str) -> None:
    assert "FEATURES_DAILY_ROOT" in code_source, (
        "FEATURES_DAILY_ROOT must be defined in Notebook 07."
    )


# ---------------------------------------------------------------------------
# Conditional backfill and feature build flags
# ---------------------------------------------------------------------------


def test_run_small_daily_bars_backfill_default_true(code_source: str) -> None:
    assert "RUN_SMALL_DAILY_BARS_BACKFILL = True" in code_source, (
        "RUN_SMALL_DAILY_BARS_BACKFILL must default to True."
    )


def test_force_daily_bars_backfill_default_false(code_source: str) -> None:
    assert "FORCE_DAILY_BARS_BACKFILL = False" in code_source, (
        "FORCE_DAILY_BARS_BACKFILL must default to False."
    )


def test_run_feature_build_if_missing_default_true(code_source: str) -> None:
    assert "RUN_FEATURE_BUILD_IF_MISSING = True" in code_source, (
        "RUN_FEATURE_BUILD_IF_MISSING must default to True."
    )


def test_force_feature_build_default_false(code_source: str) -> None:
    assert "FORCE_FEATURE_BUILD = False" in code_source, (
        "FORCE_FEATURE_BUILD must default to False."
    )
