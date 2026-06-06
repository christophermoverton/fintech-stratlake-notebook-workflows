"""
Static CLI, restore, strategy-comparison, and artifact-review tests for Notebook 09.

These tests parse the committed notebook source and verify expected command
references, guard defaults, Drive placeholder behavior, native strategy comparison
surfaces, parser/review-row fields, artifact discovery, plotting, research summary,
handoff, and classification documentation.

Scope (M12.3):
- Source text substring and structural checks only.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages on PATH are required.
- No network, Google Drive, Alpaca credentials, archives, native artifacts, plots,
  logs, manifests, or generated data are required.
- No live Colab runtime is required.

Classification note:
Runtime gates such as RUN_NATIVE_STRATEGY_COMPARISON are verified as intended live
notebook workflow gates. Their presence is not source-import evidence that archive
restore, strategy comparison, parser correctness, dataframe output, plotting,
artifact discovery, research summary, archive checkpoint refresh, or Notebook 10
handoff behavior succeeded.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB09_PATH = (
    REPO_ROOT
    / "notebooks"
    / "09_stratlake_strategy_comparison_and_research_review.ipynb"
)
CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_09_command_surface_classification.md"


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB09_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def notebook_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )


@pytest.fixture(scope="module")
def markdown_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown"
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


@pytest.fixture(scope="module")
def classification_doc_text() -> str:
    return CLASSIFICATION_DOC.read_text(encoding="utf-8")


def _json_key_present(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_json_key_present(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_json_key_present(item, key) for item in value)
    return False


# ---------------------------------------------------------------------------
# Notebook identity, source hygiene, and workflow structure
# ---------------------------------------------------------------------------


def test_notebook_09_path_exists() -> None:
    assert NB09_PATH.exists(), (
        f"Notebook 09 not found at {NB09_PATH}. "
        "M12.1 must stage the notebook before M12.3 static checks can run."
    )


def test_notebook_09_title_present(notebook_source: str) -> None:
    assert "Notebook 09" in notebook_source
    assert "StratLake Strategy Comparison and Research Review" in notebook_source


def test_notebook_09_workflow_sections_in_order(markdown_source: str) -> None:
    expected_sections = [
        "Install notebook dependencies and app packages",
        "Imports, Colab detection, and Google Drive auth",
        "Load Alpaca environment variables",
        "Configure workspace, sessions, archive paths, and analysis window",
        "Verify installed native CLI commands",
        "Initialize or attach Fintech project/session",
        "Initialize or attach StratLake session",
        "Restore StratLake archive from Notebook 07/08",
        "Verify restored native StratLake inputs",
        "Inspect available native strategies",
        "Run native strategy comparison",
        "Plot native strategy comparison",
        "Discover native artifacts by run ID",
        "Research decision summary",
        "Optional archive checkpoint after comparison",
        "Final handoff",
    ]
    last_index = -1
    for section in expected_sections:
        index = markdown_source.find(section)
        assert index > last_index, (
            f"Expected section {section!r} to appear after the prior Notebook 09 section."
        )
        last_index = index


def test_all_code_cells_output_free_and_unexecuted(code_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )


@pytest.mark.parametrize("metadata_key", ["colab", "widgets", "accelerator", "display_state"])
def test_top_level_runtime_metadata_absent(notebook: dict[str, Any], metadata_key: str) -> None:
    assert metadata_key not in notebook.get("metadata", {}), (
        f"Top-level runtime metadata key {metadata_key!r} must be absent."
    )


@pytest.mark.parametrize("metadata_key", ["id", "executionInfo", "outputId", "colab", "execution"])
def test_cell_runtime_metadata_absent(notebook: dict[str, Any], metadata_key: str) -> None:
    for i, cell in enumerate(notebook.get("cells", [])):
        assert metadata_key not in cell, (
            f"Notebook cell {i} has forbidden top-level cell key {metadata_key!r}."
        )
        assert metadata_key not in cell.get("metadata", {}), (
            f"Notebook cell {i} has forbidden metadata key {metadata_key!r}."
        )


def test_no_runtime_output_metadata_anywhere(notebook: dict[str, Any]) -> None:
    for key in ("executionInfo", "outputId", "application/vnd.google.colaboratory", "image/png"):
        assert not _json_key_present(notebook, key), (
            f"Runtime output metadata key {key!r} must not appear in Notebook 09 source."
        )


def test_no_hardcoded_tutorial_drive_root(notebook_source: str) -> None:
    assert "fintech-stratlake-tutorial" not in notebook_source, (
        "Notebook 09 must use DRIVE_FOLDER_NAME placeholder instead of a hardcoded "
        "fintech-stratlake-tutorial Drive root."
    )


# ---------------------------------------------------------------------------
# Drive placeholder, runtime gates, and manual command guards
# ---------------------------------------------------------------------------


def test_drive_folder_name_placeholder_and_guard(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert "raise ValueError" in code_source, (
        "Notebook 09 must stop before creating Drive session/archive folders when "
        "DRIVE_FOLDER_NAME remains the placeholder."
    )


def test_runtime_gate_defaults_and_intended_strategy_comparison_gate(code_source: str) -> None:
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_NATIVE_STRATEGY_COMPARISON = True" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = True" not in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = True" not in code_source


def test_restore_surface_preserves_manual_preview_and_guard(code_source: str) -> None:
    assert "stratlake-session-archive-restore-bootstrap" in code_source
    assert "restore_cmd = [" in code_source
    assert "Restore command preview" in code_source
    assert "if RUN_STRATLAKE_ARCHIVE_RESTORE:" in code_source
    assert "Manual restore is off by default in committed source" in code_source


def test_checkpoint_surface_preserves_optional_preview_and_guard(code_source: str) -> None:
    assert "stratlake-session-archive-bootstrap" in code_source
    assert "archive_cmd = [" in code_source
    assert "StratLake archive checkpoint command:" in code_source
    assert "if RUN_STRATLAKE_ARCHIVE_CHECKPOINT:" in code_source
    assert "Dry run only. Set RUN_STRATLAKE_ARCHIVE_CHECKPOINT=True" in code_source


# ---------------------------------------------------------------------------
# CLI command surfaces and path/session config surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", [
    "fintech-init-project",
    "fintech-backfill-daily",
    "fintech-backup-data",
    "stratlake-init-session",
    "stratlake-run-strategy",
    "stratlake-session-archive-restore-bootstrap",
    "stratlake-session-archive-bootstrap",
])
def test_expected_cli_command_surface_present(notebook_source: str, command: str) -> None:
    assert command in notebook_source, (
        f"Expected Notebook 09 CLI surface {command!r} not found. "
        "This is a source reference check only."
    )


@pytest.mark.parametrize("path_symbol", [
    "DRIVE_FOLDER_NAME",
    "DRIVE_ROOT",
    "FINTECH_ROOT",
    "STRATLAKE_ROOT",
    "FINTECH_DRIVE_ROOT",
    "STRATLAKE_DRIVE_ROOT",
    "MARKETLAKE_ROOT",
    "DAILY_BARS_ROOT",
    "FINTECH_SESSION_NAME",
    "STRATLAKE_SESSION_NAME",
    "STRATLAKE_SESSION_ID_OVERRIDE",
    "STRATLAKE_ARCHIVE_ID",
    "STRATLAKE_DRIVE_SESSION_ROOT",
    "STRATLAKE_DRIVE_ARCHIVE_ROOT",
    "STRATLAKE_ARCHIVE_PACK_DIR",
    "ANALYSIS_START",
    "ANALYSIS_END",
    "BACKFILL_START",
    "BACKFILL_END",
    "BACKFILL_SYMBOLS",
    "strategies_config_path",
])
def test_expected_path_and_config_surface_present(code_source: str, path_symbol: str) -> None:
    assert path_symbol in code_source


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


@pytest.mark.parametrize("flag", [
    "--archive-id",
    "--archive-collision-policy",
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
# Native strategy comparison, parser, dataframe, and plotting surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", [
    "for strategy_name in strategy_names:",
    "stratlake-run-strategy",
    "--strategies-config",
    "configs/strategies.yml",
    "--strategy",
    "strategy_name",
    "--start",
    "ANALYSIS_START",
    "--end",
    "ANALYSIS_END",
    "subprocess.run(cmd",
    "capture_output=True",
    "strategy_logs",
])
def test_strategy_comparison_command_shape_present(code_source: str, token: str) -> None:
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
def test_parser_metric_reference_present(code_source: str, metric: str) -> None:
    assert metric in code_source


@pytest.mark.parametrize("token", [
    "parse_strategy_stdout",
    "strategy_rows",
    "strategy_comparison = pd.DataFrame(strategy_rows)",
    "sort_values",
    "display(strategy_comparison)",
    "No strategy comparison rows produced",
])
def test_strategy_comparison_dataframe_review_surface_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "matplotlib.pyplot",
    "plot_df",
    'kind="bar"',
    "figsize",
    "plt.tight_layout",
    "plt.show",
    "cumulative_return",
    "benchmark_return",
    "excess_return",
    "sharpe_ratio",
    "correlation",
    "No strategy_comparison dataframe available to plot",
])
def test_comparison_plot_surface_present(code_source: str, token: str) -> None:
    assert token in code_source


# ---------------------------------------------------------------------------
# Artifact discovery, research summary, and final handoff surfaces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", [
    "artifact_roots",
    'STRATLAKE_ROOT / "artifacts"',
    'STRATLAKE_ROOT / "data"',
    'STRATLAKE_ROOT / "reports"',
    "run_ids",
    "run_id",
    "rglob",
    "matched_run_ids",
    "artifact_inventory",
    ".parquet",
    ".json",
    ".csv",
    ".md",
    ".html",
])
def test_artifact_discovery_by_run_id_surface_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "Research decision summary",
    "Strategies attempted",
    "Strategies completed",
    "Best by excess return",
    "Best by Sharpe",
    "Rows with stderr warnings",
    "No strategy comparison results available",
])
def test_research_decision_summary_surface_present(notebook_source: str, token: str) -> None:
    assert token in notebook_source


@pytest.mark.parametrize("token", [
    "final_handoff",
    "Notebook 10",
    "next_notebook",
    "strategies_attempted",
    "strategies_completed",
    "artifact_rows",
    "archive_pack_dir",
])
def test_final_handoff_surface_present(code_source: str, token: str) -> None:
    assert token in code_source


# ---------------------------------------------------------------------------
# Classification documentation coverage
# ---------------------------------------------------------------------------


def test_notebook_09_classification_document_exists() -> None:
    assert CLASSIFICATION_DOC.exists(), (
        f"Notebook 09 classification document not found at {CLASSIFICATION_DOC}."
    )


@pytest.mark.parametrize("phrase", [
    "source-safe StratLake strategy comparison and research review notebook",
    "source and runtime surfaces",
    "runtime-only",
    "review surface",
    "does not prove runtime restore success",
    "strategy comparison success",
    "all-strategy correctness",
    "performance validity",
    "does not validate Notebook 10 behavior",
    "Do not claim archive restore success",
    "Do not claim strategy comparison success",
    "Do not claim source import proves runtime correctness",
])
def test_classification_document_source_only_non_authoritative_stance_present(
    classification_doc_text: str,
    phrase: str,
) -> None:
    assert phrase in classification_doc_text


@pytest.mark.parametrize("surface", [
    "Dependency / Install Surface",
    "Imports, Colab Detection, and Drive Auth Surface",
    "Runtime Environment / Alpaca Configuration Surface",
    "Workspace, Session, Archive Path, and Analysis Window Surface",
    "CLI Availability Check Surface",
    "Fintech Project/Session Init Surface",
    "StratLake Project/Session Init Surface",
    "Archive Restore Surface",
    "Restored Native Input Validation Surface",
    "Native Strategy Registry Inspection Surface",
    "Native Strategy Comparison Execution Surface",
    "Native Stdout Parser and Review Row Surface",
    "Strategy Comparison Dataframe Surface",
    "Comparison Plot Surface",
    "Native Artifact Discovery by Run ID Surface",
    "Research Decision Summary Surface",
    "Optional Archive Checkpoint Refresh Surface",
    "Final Handoff Surface",
])
def test_classification_document_expected_surface_sections_present(
    classification_doc_text: str,
    surface: str,
) -> None:
    assert surface in classification_doc_text
