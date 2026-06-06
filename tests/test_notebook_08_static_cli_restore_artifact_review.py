"""
Static CLI, restore, strategy, and artifact-review tests for Notebook 08.

These tests parse the committed notebook source and verify expected command
references, guard defaults, Drive placeholder behavior, native strategy review
surfaces, artifact-review structure, and classification documentation.

Scope (M11.3):
- Source text substring and structural checks only.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages on PATH are required.
- No network, Google Drive, Alpaca credentials, or generated data are required.
- No live Colab runtime is required.

Classification note:
Runtime gates such as RUN_FINTECH_INIT_PROJECT, RUN_STRATLAKE_INIT_SESSION,
and RUN_NATIVE_STRATEGY_BACKTEST are verified as intended live notebook
workflow gates. Their presence is not source-import evidence that runtime
initialization, archive restore, strategy backtest, artifact review, benchmark
review, plot generation, or handoff succeeded.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB08_PATH = REPO_ROOT / "notebooks" / "08_stratlake_strategy_backtest_artifact_review.ipynb"
CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_08_command_surface_classification.md"


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB08_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def notebook_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )


@pytest.fixture(scope="module")
def code_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    )


@pytest.fixture(scope="module")
def code_cells(notebook: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        cell
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    ]


def _json_key_present(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_json_key_present(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_json_key_present(item, key) for item in value)
    return False


# ---------------------------------------------------------------------------
# Notebook source hygiene
# ---------------------------------------------------------------------------


def test_notebook_08_path_exists() -> None:
    assert NB08_PATH.exists(), (
        f"Notebook 08 not found at {NB08_PATH}. "
        "M11.1 must stage the notebook before M11.3 static checks can run."
    )


def test_no_committed_outputs(code_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], (
            f"Code cell {i} has committed outputs. Notebook 08 source must remain output-free."
        )


def test_no_non_null_execution_counts(code_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(code_cells):
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has a non-null execution_count."
        )


@pytest.mark.parametrize("metadata_key", ["colab", "executionInfo", "outputId"])
def test_colab_runtime_metadata_absent(notebook: dict[str, Any], metadata_key: str) -> None:
    assert not _json_key_present(notebook, metadata_key), (
        f"Notebook 08 source must not contain Colab/runtime metadata key {metadata_key!r}."
    )


def test_no_hardcoded_tutorial_drive_root(notebook_source: str) -> None:
    assert "fintech-stratlake-tutorial" not in notebook_source, (
        "Notebook 08 must use DRIVE_FOLDER_NAME placeholder instead of a hardcoded "
        "fintech-stratlake-tutorial Drive root."
    )


def test_drive_folder_name_placeholder_and_guard(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert "raise ValueError" in code_source, (
        "Notebook 08 must stop before creating Drive session/archive folders when "
        "DRIVE_FOLDER_NAME remains the placeholder."
    )


# ---------------------------------------------------------------------------
# Manual/off-by-default gates and intended runtime gates
# ---------------------------------------------------------------------------


def test_archive_restore_and_checkpoint_defaults_false(code_source: str) -> None:
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = True" not in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = True" not in code_source


def test_restore_cell_preserves_manual_command_preview(code_source: str) -> None:
    assert "Manual restore is off by default in committed source" in code_source
    assert "Restore command preview" in code_source
    assert "if RUN_STRATLAKE_ARCHIVE_RESTORE:" in code_source
    assert "else:" in code_source


def test_checkpoint_cell_preserves_dry_run_preview_behavior(code_source: str) -> None:
    assert "StratLake archive checkpoint command:" in code_source
    assert "Dry run only. Set RUN_STRATLAKE_ARCHIVE_CHECKPOINT=True" in code_source
    assert "if RUN_STRATLAKE_ARCHIVE_CHECKPOINT:" in code_source


@pytest.mark.parametrize("gate", [
    "RUN_FINTECH_INIT_PROJECT = True",
    "RUN_STRATLAKE_INIT_SESSION = True",
    "RUN_NATIVE_STRATEGY_BACKTEST = True",
])
def test_intended_live_runtime_gate_present(code_source: str, gate: str) -> None:
    assert gate in code_source, (
        f"{gate} must remain present as an intended live runtime workflow gate. "
        "This source-only test does not execute the gate or claim runtime success."
    )


# ---------------------------------------------------------------------------
# CLI command surfaces and key flags
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", [
    "fintech-init-project",
    "stratlake-init-session",
    "stratlake-session-archive-restore-bootstrap",
    "stratlake-run-strategy",
    "stratlake-session-archive-bootstrap",
])
def test_expected_cli_command_reference_present(notebook_source: str, command: str) -> None:
    assert command in notebook_source, (
        f"Expected Notebook 08 CLI surface {command!r} not found. "
        "This is a source reference check only."
    )


@pytest.mark.parametrize("flag", ["--root", "--session-name", "--with-session", "--colab-profile"])
def test_fintech_init_project_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source


@pytest.mark.parametrize("flag", [
    "--root",
    "--project-name",
    "--marketlake-root",
    "--drive-root",
    "--enable-drive-persistence",
    "--notebook-configs",
])
def test_stratlake_init_session_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source


@pytest.mark.parametrize("flag", [
    "--archive-root",
    "--target-root",
    "--validate-before-restore",
    "--inspect-before-restore",
    "--overwrite-policy",
    "overwrite_allowed",
])
def test_archive_restore_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source


@pytest.mark.parametrize("token", [
    "--strategies-config",
    "configs/strategies.yml",
    "--strategy",
    "NATIVE_STRATEGY_NAME",
    "--start",
    "ANALYSIS_START",
    "--end",
    "ANALYSIS_END",
])
def test_stratlake_run_strategy_command_shape_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("flag", [
    "--root",
    "--archive-id",
    "--archive-collision-policy",
    "overwrite_allowed",
    "--drive-root",
    "--copy-policy",
    "--include-features",
    "--include-artifacts",
    "--include-configs",
    "--validate-after-copy",
    "--inspect-after-copy",
])
def test_archive_checkpoint_flag_present(code_source: str, flag: str) -> None:
    assert flag in code_source


# ---------------------------------------------------------------------------
# Path, restore, and session identity surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path_symbol", [
    "DRIVE_ROOT",
    "FINTECH_ROOT",
    "STRATLAKE_ROOT",
    "MARKETLAKE_ROOT",
    "DAILY_BARS_ROOT",
    "FINTECH_DRIVE_ROOT",
    "STRATLAKE_DRIVE_ROOT",
    "STRATLAKE_DRIVE_SESSION_ROOT",
    "STRATLAKE_DRIVE_ARCHIVE_ROOT",
    "STRATLAKE_ARCHIVE_PACK_DIR",
    "FEATURES_DAILY_ROOT",
    "STRATEGIES_CONFIG",
])
def test_expected_path_surface_reference_present(code_source: str, path_symbol: str) -> None:
    assert path_symbol in code_source


def test_stratlake_session_and_archive_identity_present(code_source: str) -> None:
    assert 'STRATLAKE_SESSION_NAME = "stratlake_q1_feature_consumption"' in code_source
    assert 'STRATLAKE_ARCHIVE_ID = f"stratlake-session-{STRATLAKE_SESSION_ID}"' in code_source


# ---------------------------------------------------------------------------
# Native strategy/backtest review surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", [
    'NATIVE_STRATEGY_NAME = "momentum_v1"',
    "native_strategy_stdout",
    "native_strategy_stderr",
    "native_strategy_returncode",
    "native_strategy_completed",
    "parse_native_strategy_stdout",
    "strategy_result",
    "strategy_result_row",
    "run_id",
])
def test_native_strategy_review_reference_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("metric", [
    "cumulative_return",
    "sharpe_ratio",
    "long_pct",
    "short_pct",
    "flat_pct",
    "trades",
    "turnover",
    "avg_holding_bars",
    "qa_status",
    "qa_rows",
    "qa_symbols",
    "benchmark_return",
    "excess_return",
    "correlation",
])
def test_native_strategy_parser_metric_reference_present(code_source: str, metric: str) -> None:
    assert metric in code_source


# ---------------------------------------------------------------------------
# Artifact-review, plot, benchmark, and handoff surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", [
    "artifact_search_roots",
    "artifact_inventory",
    "matches_run_id",
    "native_time_series",
    "time_series_source",
    ".parquet",
    ".csv",
    "pd.read_parquet",
    "pd.read_csv",
    "matplotlib.pyplot",
    "benchmark_review",
    "summary",
])
def test_artifact_plot_benchmark_handoff_reference_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("root_reference", [
    'STRATLAKE_ROOT / "artifacts"',
    'STRATLAKE_ROOT / "reports"',
    'STRATLAKE_ROOT / "data"',
])
def test_artifact_search_root_reference_present(code_source: str, root_reference: str) -> None:
    assert root_reference in code_source


# ---------------------------------------------------------------------------
# Classification documentation coverage
# ---------------------------------------------------------------------------


def test_notebook_08_classification_document_exists() -> None:
    assert CLASSIFICATION_DOC.exists(), (
        f"Notebook 08 classification document not found at {CLASSIFICATION_DOC}."
    )


@pytest.mark.parametrize("phrase", [
    "Source classification is not live runtime validation",
    "RUN_STRATLAKE_ARCHIVE_RESTORE",
    "RUN_STRATLAKE_ARCHIVE_CHECKPOINT",
    "RUN_NATIVE_STRATEGY_BACKTEST",
    "stratlake-session-archive-restore-bootstrap",
    "stratlake-run-strategy",
    "artifact-review",
    "M11.3",
    "M11.6",
])
def test_notebook_08_classification_document_phrase_present(phrase: str) -> None:
    doc_text = CLASSIFICATION_DOC.read_text(encoding="utf-8")
    assert phrase in doc_text, (
        f"Expected phrase {phrase!r} not found in Notebook 08 classification document."
    )
