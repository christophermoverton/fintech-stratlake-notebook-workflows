"""
Static source-contract tests for Notebook 13.

Scope (M16.3):
- Parse committed Notebook 13 and its M16.2 classification document as source
  text only.
- Verify source-safe notebook shape, profile defaults, runtime guards, command
  surfaces, and conservative claim boundaries.
- Do not execute notebook cells, install packages, mount Drive, restore
  archives, initialize sessions, call native CLIs, generate configs, or write
  runtime artifacts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB13_PATH = (
    REPO_ROOT
    / "notebooks"
    / "13_stratlake_native_campaign_execution_and_artifact_generation.ipynb"
)
CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_13_command_surface_classification.md"


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB13_PATH.read_text(encoding="utf-8"))


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


@pytest.fixture(scope="module")
def docs_text() -> str:
    return CLASSIFICATION_DOC.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _profile_block(code_source: str, profile_name: str) -> str:
    pattern = rf'"{re.escape(profile_name)}":\s*\{{(?P<body>.*?)\n\s*\}}'
    match = re.search(pattern, code_source, flags=re.DOTALL)
    assert match is not None, f"Expected profile {profile_name!r} in Notebook 13."
    return match.group("body")


def test_notebook_13_path_exists_and_json_shape(
    notebook: dict[str, Any],
    notebook_source: str,
) -> None:
    assert NB13_PATH.exists()
    assert notebook.get("nbformat") == 4
    cells = notebook.get("cells", [])
    assert cells
    assert any(cell.get("cell_type") == "markdown" for cell in cells)
    assert any(cell.get("cell_type") == "code" for cell in cells)
    assert "Notebook 13" in notebook_source
    assert "notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb" in notebook_source


def test_notebook_13_is_output_free_and_unexecuted(
    notebook: dict[str, Any],
    code_cells: list[dict[str, Any]],
) -> None:
    assert code_cells
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )
    assert "widgets" not in notebook.get("metadata", {})


def test_default_profile_is_source_safe_preview(code_source: str, docs_text: str) -> None:
    assert (
        'NOTEBOOK13_TEST_PROFILE = os.environ.get(\n'
        '    "NOTEBOOK13_TEST_PROFILE",\n'
        '    "campaign_execution_preview",\n'
        ').strip() or "campaign_execution_preview"'
    ) in code_source
    assert "Committed default profile | `campaign_execution_preview`" in docs_text
    assert "campaign_execution_preview" in docs_text


def test_preview_profile_disables_restore_execution_governance_and_checkpoint(
    code_source: str,
) -> None:
    preview = _profile_block(code_source, "campaign_execution_preview")
    for disabled_flag in [
        "RUN_FINTECH_SESSION_INIT",
        "RUN_STRATLAKE_SESSION_INIT",
        "RUN_ARCHIVE_RESTORE",
        "RUN_NATIVE_CAMPAIGN_EXECUTION",
        "RUN_OPTIONAL_REPORT_COMMANDS",
        "RUN_OPTIONAL_GOVERNANCE_COMMANDS",
        "RUN_ARCHIVE_CHECKPOINT",
    ]:
        assert re.search(rf'"{disabled_flag}"\s*:\s*False\b', preview)
    assert re.search(r'"RUN_CAMPAIGN_PREFLIGHT"\s*:\s*True\b', preview)


@pytest.mark.parametrize(
    "profile",
    [
        "campaign_execution_preflight",
        "campaign_execution_run",
        "campaign_execution_run_with_archive_checkpoint",
    ],
)
def test_run_profiles_exist_but_are_not_default(code_source: str, profile: str) -> None:
    assert f'"{profile}":' in code_source
    default_block = re.search(
        r'NOTEBOOK13_TEST_PROFILE\s*=\s*os\.environ\.get\(\s*"NOTEBOOK13_TEST_PROFILE",\s*"(?P<default>[^"]+)"',
        code_source,
        flags=re.DOTALL,
    )
    assert default_block is not None
    assert default_block.group("default") == "campaign_execution_preview"
    assert default_block.group("default") != profile


@pytest.mark.parametrize(
    "gate",
    [
        "NOTEBOOK13_ALLOW_NATIVE_EXECUTION",
        "NOTEBOOK13_ALLOW_ARCHIVE_RESTORE",
        "NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT",
        "NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION",
        "NOTEBOOK13_MARK_INPUTS_USER_REVIEWED",
    ],
)
def test_explicit_runtime_gates_default_false(code_source: str, docs_text: str, gate: str) -> None:
    assert gate in code_source
    assert re.search(
        rf'{gate}\s*=\s*os\.environ\.get\(\s*"{gate}",\s*"false",',
        code_source,
        flags=re.DOTALL,
    )
    assert gate in docs_text
    assert f"{gate} = False" in docs_text


@pytest.mark.parametrize(
    "surface",
    [
        "RUN_STRATLAKE_SESSION_INIT",
        "RUN_ARCHIVE_RESTORE",
        "NOTEBOOK13_CREATE_EXECUTION_CONFIGS",
        "RUN_NATIVE_CAMPAIGN_EXECUTION",
        "RUN_OPTIONAL_REPORT_COMMANDS",
        "RUN_OPTIONAL_GOVERNANCE_COMMANDS",
        "RUN_ARCHIVE_CHECKPOINT",
    ],
)
def test_profile_request_gates_are_source_visible(notebook_source: str, surface: str) -> None:
    assert surface in notebook_source


def test_classification_doc_preserves_source_only_test_discipline(docs_text: str) -> None:
    normalized = _normalized(docs_text)
    for token in [
        "Repository validation must not execute notebook cells",
        "install packages",
        "mount Google Drive",
        "initialize Fintech or StratLake sessions",
        "restore archives",
        "run native campaigns",
        "run governance/reporting commands",
        "checkpoint archives",
        "write runtime artifacts",
        "treat external smoke evidence as committed notebook output",
    ]:
        assert token in normalized
