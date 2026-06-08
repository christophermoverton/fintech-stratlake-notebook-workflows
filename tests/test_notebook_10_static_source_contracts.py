"""
Static command, restore, walk-forward, robustness, promotion, and artifact tests
for Notebook 10.

Scope (M13.3):
- Parse committed notebook/docs source only.
- Verify command references, guard defaults, section order, strategy preflight,
  warning taxonomy, artifact filenames, promotion review, and handoff surfaces.
- Do not execute notebook cells, CLI commands, package installs, Drive mounts,
  archive restores, strategy runs, plots, artifact writes, or checkpoint refreshes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB10_PATH = (
    REPO_ROOT
    / "notebooks"
    / "10_stratlake_walk_forward_robustness_and_promotion_review.ipynb"
)
COMMAND_CLASSIFICATION_DOC = (
    REPO_ROOT / "docs" / "notebook_10_command_surface_classification.md"
)
STAGING_CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_10_staging_classification.md"


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB10_PATH.read_text(encoding="utf-8"))


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
def docs_text() -> str:
    return "\n".join(
        [
            COMMAND_CLASSIFICATION_DOC.read_text(encoding="utf-8"),
            STAGING_CLASSIFICATION_DOC.read_text(encoding="utf-8"),
        ]
    )


def _json_key_present(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_json_key_present(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_json_key_present(item, key) for item in value)
    return False


def test_notebook_10_path_exists() -> None:
    assert NB10_PATH.exists(), (
        f"Notebook 10 not found at {NB10_PATH}. "
        "M13.1 must stage the notebook before M13.3 static checks can run."
    )


def test_notebook_10_source_shape_and_title(
    notebook: dict[str, Any],
    notebook_source: str,
) -> None:
    cells = notebook.get("cells", [])
    markdown_count = sum(1 for cell in cells if cell.get("cell_type") == "markdown")
    code_count = sum(1 for cell in cells if cell.get("cell_type") == "code")

    assert notebook.get("nbformat") == 4
    assert len(cells) == 41
    assert markdown_count == 21
    assert code_count == 20
    assert "Notebook 10 — StratLake Walk-Forward Robustness and Promotion Review" in notebook_source
    assert "Draft v4" not in notebook_source
    assert "notebook_10_draft_version" not in notebook.get("metadata", {})


def test_notebook_10_workflow_sections_in_order(markdown_source: str) -> None:
    expected_sections = [
        "Install notebook dependencies and app packages",
        "Imports, Colab detection, and Google Drive auth",
        "Load Alpaca environment variables",
        "Configure workspace, sessions, archive paths, and notebook mode",
        "Verify installed native CLI commands and import surfaces",
        "Initialize or attach Fintech project/session",
        "Initialize or attach StratLake session",
        "Restore StratLake archive from Notebook 08/09",
        "Verify restored inputs and prior artifacts",
        "Discover feature columns for strategy preflight",
        "Discover and preflight candidate native strategies",
        "Run walk-forward strategy smoke/expanded evaluation",
        "Add diagnostic flags for financial interpretation",
        "Build robustness summary from split-level results",
        "Plot walk-forward robustness diagnostics",
        "Apply improved notebook-level promotion gates",
        "Smoke audit interpretation and import-readiness notes",
        "Write Notebook 10 review outputs and artifact inventory",
        "Optional archive checkpoint after Notebook 10 review",
        "Final handoff",
    ]
    last_index = -1
    for section in expected_sections:
        index = markdown_source.find(section)
        assert index > last_index, (
            f"Expected section {section!r} to appear after the prior Notebook 10 section."
        )
        last_index = index


def test_notebook_10_output_free_unexecuted_and_metadata_clean(
    notebook: dict[str, Any],
    code_cells: list[dict[str, Any]],
) -> None:
    assert set(notebook.get("metadata", {})) == {"kernelspec", "language_info"}
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )
    for key in ("colab", "widgets", "executionInfo", "outputId", "image/png"):
        assert not _json_key_present(notebook, key), (
            f"Runtime metadata or output payload key {key!r} must not appear."
        )


def test_conservative_controls_and_drive_guard_present(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert "raise ValueError" in code_source
    assert 'NOTEBOOK10_MODE = "smoke"' in code_source
    assert "RUN_ONLY_PREFLIGHT_RUNNABLE_STRATEGIES = True" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = True" not in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = True" not in code_source


@pytest.mark.parametrize("command", [
    "fintech-init-project",
    "fintech-backfill-daily",
    "fintech-backup-data",
    "stratlake-init-session",
    "stratlake-run-strategy",
    "stratlake-session-archive-bootstrap",
    "stratlake-session-archive-restore-bootstrap",
])
def test_expected_command_reference_present(notebook_source: str, command: str) -> None:
    assert command in notebook_source, (
        f"Expected Notebook 10 command reference {command!r} not found. "
        "This test validates source references only and does not execute commands."
    )


@pytest.mark.parametrize("module_name", [
    "src.research.walk_forward",
    "src.research.splits",
    "src.research.compare",
    "src.research.promotion",
    "src.research.robustness.runner",
    "src.research.robustness.walk_forward_efficiency",
])
def test_expected_native_surface_reference_present(
    notebook_source: str,
    module_name: str,
) -> None:
    assert module_name in notebook_source


@pytest.mark.parametrize("token", [
    "restore_cmd = [",
    "--archive-root",
    "--target-root",
    "--validate-before-restore",
    "--inspect-before-restore",
    "--overwrite-policy",
    "Restore command preview",
    "if RUN_STRATLAKE_ARCHIVE_RESTORE:",
    "Manual restore is off by default in committed source",
])
def test_archive_restore_surface_is_guarded_and_source_reviewable(
    code_source: str,
    token: str,
) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "archive_cmd = [",
    "--archive-id",
    "--archive-collision-policy",
    "--drive-root",
    "--copy-policy",
    "--include-features",
    "--include-artifacts",
    "--include-configs",
    "--validate-after-copy",
    "--inspect-after-copy",
    "if RUN_STRATLAKE_ARCHIVE_CHECKPOINT:",
])
def test_archive_checkpoint_surface_is_guarded_and_source_reviewable(
    code_source: str,
    token: str,
) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "strategies_config_path",
    "strategy_entries",
    "strategy_names",
    "KNOWN_REQUIRED_COLUMN_HINTS",
    '"breakout": ["high", "low"]',
    '"residual_momentum": ["market_return"]',
    '"weighted_cross_section_ensemble": ["market_return"]',
    "missing_columns",
    "preflight_runnable",
    "preflight_skipped",
    "RUN_ONLY_PREFLIGHT_RUNNABLE_STRATEGIES",
])
def test_strategy_discovery_and_feature_preflight_source_surface_present(
    code_source: str,
    token: str,
) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "for strategy_name in candidate_strategy_names:",
    "for window in WALK_FORWARD_WINDOWS:",
    "stratlake-run-strategy",
    "--strategies-config",
    "configs/strategies.yml",
    "--strategy",
    "--start",
    "--end",
    "RUN_NATIVE_WALK_FORWARD_EVALUATION",
    "parse_strategy_stdout",
    "walk_forward_results",
    "metric_source",
    "artifact_metric_path",
])
def test_walk_forward_strategy_execution_source_surface_present(
    code_source: str,
    token: str,
) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "benchmark_avoidance_outperformance",
    "Do not treat these as alpha evidence",
    "robustness_summary",
    "positive_excess_rate",
    "positive_cumulative_rate",
    "qa_clean_windows",
    "warning_windows",
    "error_windows",
])
def test_robustness_and_financial_interpretation_surfaces_present(
    code_source: str,
    token: str,
) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "PROMOTION_GATES",
    "allow_benchmark_avoidance_outperformance",
    "allow_signal_pct_sum_warning",
    "classify_strategy",
    '"promoted"',
    '"watchlist"',
    '"needs_review"',
    "promotion_decision",
    "promotion_reasons",
])
def test_promotion_review_surface_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("token", [
    "benchmark_degenerate_warning",
    "strategy_degenerate_warning",
    "flat_series_correlation_warning",
    "signal_pct_consistency",
    "qa_warn",
    "numeric_runtime_warning",
    "missing_required_columns",
    "runtime_failed",
    "exception_or_error_text",
    "stderr_other",
    "buyandholdstrategy",
    "no trades were generated",
])
def test_warning_taxonomy_terms_present(notebook_source: str, token: str) -> None:
    assert token in notebook_source


@pytest.mark.parametrize("filename", [
    "walk_forward_results.csv",
    "walk_forward_results.json",
    "robustness_summary.csv",
    "robustness_summary.json",
    "promotion_review.csv",
    "promotion_review.json",
    "preflight_summary.csv",
    "preflight_summary.json",
    "artifact_inventory.csv",
    "artifact_inventory.json",
    "summary.json",
    "smoke_audit_summary.json",
])
def test_expected_artifact_filename_reference_present(
    notebook_source: str,
    filename: str,
) -> None:
    assert filename in notebook_source


def test_normalized_artifact_directory_reference_present(
    notebook_source: str,
    docs_text: str,
) -> None:
    assert '"artifacts" / "notebook_10_walk_forward_promotion_review"' in notebook_source
    assert "artifacts/notebook_10_walk_forward_promotion_review/" in docs_text
    assert "notebook_10_walk_forward_promotion_review_v4" not in notebook_source


@pytest.mark.parametrize("token", [
    "final_handoff",
    "source_notebooks",
    "source_stratlake_archive_id",
    "notebook10_archive_id",
    "notebook10_mode",
    "preflight_rows",
    "preflight_runnable_count",
    "preflight_skipped_count",
    "walk_forward_rows",
    "promotion_review_rows",
    "promoted_strategies",
    "watchlist_strategies",
    "artifact_rows",
    "smoke_audit_status",
    "metric_source_counts",
    "warning_category_counts",
    "diagnostic_counts",
])
def test_final_handoff_fields_present(code_source: str, token: str) -> None:
    assert token in code_source


@pytest.mark.parametrize("phrase", [
    "Smoke mode is workflow-validation mode",
    "not promotion-grade financial evidence",
    "benchmark-avoidance",
    "not alpha",
    "promoted_strategies: []",
    "watchlist_strategies: []",
    "{'needs_review': 11}",
    "Feature-contract finding, not runtime failure",
])
def test_docs_preserve_non_claim_and_feature_contract_interpretation(
    docs_text: str,
    phrase: str,
) -> None:
    assert phrase in docs_text


def test_classification_docs_exist_and_reference_staged_notebook() -> None:
    assert COMMAND_CLASSIFICATION_DOC.exists()
    assert STAGING_CLASSIFICATION_DOC.exists()
    for path in (COMMAND_CLASSIFICATION_DOC, STAGING_CLASSIFICATION_DOC):
        text = path.read_text(encoding="utf-8")
        assert "notebooks/10_stratlake_walk_forward_robustness_and_promotion_review.ipynb" in text
        assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in text
        assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in text
        assert 'NOTEBOOK10_MODE = "smoke"' in text
