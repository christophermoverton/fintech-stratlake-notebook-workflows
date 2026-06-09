"""
Static source-contract tests for Notebook 11.

Scope (M14.1):
- Parse committed notebook source only.
- Verify source-safe controls, guarded runtime surfaces, expanded-run command
  shape, artifact paths, Notebook 10 context references, and non-claim language.
- Do not execute notebook cells, CLI commands, package installs, Drive mounts,
  archive restores, strategy runs, governance jobs, artifact writes, or
  checkpoint refreshes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB11_PATH = (
    REPO_ROOT
    / "notebooks"
    / "11_stratlake_expanded_promotion_evidence_review.ipynb"
)


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB11_PATH.read_text(encoding="utf-8"))


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


def _has_env_bool_default(code_source: str, name: str, expected: str) -> bool:
    pattern = rf'{name}\s*=\s*env_bool\(\s*"{name}",\s*{expected}\s*,?\s*\)'
    return re.search(pattern, code_source, flags=re.MULTILINE) is not None


def test_notebook_11_path_exists() -> None:
    assert NB11_PATH.exists()


def test_notebook_11_source_shape_and_title(
    notebook: dict[str, Any],
    notebook_source: str,
) -> None:
    cells = notebook.get("cells", [])
    assert notebook.get("nbformat") == 4
    assert len(cells) == 51
    assert sum(1 for cell in cells if cell.get("cell_type") == "markdown") == 28
    assert sum(1 for cell in cells if cell.get("cell_type") == "code") == 23
    assert "Notebook 11 — StratLake Expanded Promotion Evidence Review" in notebook_source
    assert "From confidence review to promotion evidence" in notebook_source
    assert "raw standalone draft" not in notebook_source


def test_output_free_unexecuted_cell_id_clean_and_metadata_limited(
    notebook: dict[str, Any],
    code_cells: list[dict[str, Any]],
) -> None:
    assert set(notebook.get("metadata", {})) == {"kernelspec", "language_info"}
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )
    for i, cell in enumerate(notebook.get("cells", [])):
        assert "id" not in cell, f"Cell {i} has a committed cell id."
        assert "executionInfo" not in cell.get("metadata", {})
        assert "outputId" not in cell.get("metadata", {})


def test_source_safe_default_controls(code_source: str) -> None:
    assert 'NOTEBOOK11_MODE = os.environ.get("NOTEBOOK11_MODE", "expanded_preview")' in code_source
    assert _has_env_bool_default(code_source, "RUN_STRATLAKE_ARCHIVE_RESTORE", "False")
    assert _has_env_bool_default(code_source, "RUN_EXPANDED_STRATEGY_EVALUATION", "False")
    assert _has_env_bool_default(code_source, "ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS", "False")
    assert _has_env_bool_default(code_source, "ALLOW_REFERENCE_ONLY_EXPANDED_PLAN", "False")
    assert _has_env_bool_default(code_source, "RUN_PROMOTION_GOVERNANCE_REPORT", "False")
    assert _has_env_bool_default(code_source, "RUN_STRATLAKE_ARCHIVE_CHECKPOINT", "False")
    assert _has_env_bool_default(
        code_source,
        "DISCOVER_EXISTING_EXPANDED_PLATFORM_ARTIFACTS",
        "False",
    )
    assert _has_env_bool_default(code_source, "AUTO_RESTORE_NOTEBOOK10_CONTEXT_IF_MISSING", "False")
    assert _has_env_bool_default(code_source, "RUN_EVIDENCE_REVIEW_CLI_BUILD", "False")
    assert _has_env_bool_default(code_source, "RUN_PROMOTION_GOVERNANCE_REPORT_CLI", "False")
    assert _has_env_bool_default(
        code_source,
        "RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY",
        "True",
    )


def test_drive_paths_and_notebook10_initialization_patterns_are_guarded(
    code_source: str,
) -> None:
    assert 'DRIVE_FOLDER_NAME = os.environ.get("STRATLAKE_DRIVE_FOLDER_NAME", "REPLACE_WITH_DRIVE_FOLDER_NAME")' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert "raise ValueError" in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME' in code_source
    assert "fintech-init-project" in code_source
    assert "stratlake-init-session" in code_source
    assert "--notebook-configs" in code_source
    assert "stratlake-session-archive-restore-bootstrap" in code_source
    assert "stratlake-session-archive-bootstrap" in code_source


@pytest.mark.parametrize(
    "token",
    [
        "notebook_10_walk_forward_promotion_review",
        "stratlake_q1_feature_consumption",
        "Notebook 10 smoke-mode handoff context",
        "expanded_preview_reference_only_context_needs_notebook10_artifacts",
    ],
)
def test_notebook10_context_references_preserved(notebook_source: str, token: str) -> None:
    assert token in notebook_source


def test_expected_artifact_path_and_expanded_run_command_shape(code_source: str) -> None:
    assert '"notebook_11_expanded_promotion_evidence_review"' in code_source
    assert 'NOTEBOOK11_REVIEW_DIR = STRATLAKE_ROOT / "artifacts"' in code_source
    assert "stratlake-run-strategy" in code_source
    for arg in ("--strategies-config", "--strategy", "--start", "--end"):
        assert arg in code_source


@pytest.mark.parametrize(
    "strategy",
    [
        "buy_and_hold_v1",
        "cross_section_momentum",
        "seeded_random_v1",
        "sma_crossover_v1",
    ],
)
def test_manual_review_candidates_preserved(notebook_source: str, strategy: str) -> None:
    assert strategy in notebook_source


def test_expanded_run_documented_but_disabled_by_default(notebook_source: str) -> None:
    assert "NOTEBOOK11_MODE = \"expanded_run\"" in notebook_source
    assert "RUN_EXPANDED_STRATEGY_EVALUATION = True" in notebook_source
    assert "ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS = True" in notebook_source
    assert "expanded_strategy_execution_not_run_default_off" in notebook_source


def test_non_claim_and_review_framing_preserved(notebook_source: str) -> None:
    assert "does **not** introduce a new promotion engine" in notebook_source
    assert "does **not** claim alpha" in notebook_source
    assert "production readiness" in notebook_source
    assert "statistical significance" in notebook_source
    assert "promotion-grade evidence by default" in notebook_source
    assert "expanded evidence" in notebook_source
    assert "caveat" in notebook_source
    assert "promotion-readiness interpretation" in notebook_source
