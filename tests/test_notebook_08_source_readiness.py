"""
Source-only readiness and sanitized validation tests for Notebook 08.

Scope (M11.4):
- Notebook structure and ordered workflow-section checks.
- Sanitized metadata checks: no Colab runtime metadata, widget state, display state,
  cell ids, execution info, output ids, or committed outputs.
- Credential and Drive placeholder safety checks.
- Runtime artifact exclusion and non-authoritative review stance checks.
- Manual/off-by-default restore/checkpoint boundary checks.

Testing rules:
- Parse the .ipynb JSON directly.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages are required.
- No network, Google Drive, Alpaca credentials, archives, native artifacts, or plots
  are required.
- No live Colab runtime is required.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB08_PATH = REPO_ROOT / "notebooks" / "08_stratlake_strategy_backtest_artifact_review.ipynb"
CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_08_command_surface_classification.md"
NOTEBOOK_TEST_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


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
def markdown_cells(notebook: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        cell
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown"
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
# Notebook identity and ordered workflow sections
# ---------------------------------------------------------------------------


def test_notebook_08_path_exists() -> None:
    assert NB08_PATH.exists(), f"Notebook 08 not found at {NB08_PATH}."


def test_notebook_08_title_present(notebook_source: str) -> None:
    assert "Notebook 08 — StratLake Strategy Backtest Artifact Review" in notebook_source


def test_notebook_08_workflow_sections_in_order(markdown_source: str) -> None:
    expected_sections = [
        "Install package dependencies",
        "Mount Google Drive and set credentials",
        "Configure workspace, Drive roots, and research windows",
        "Initialize or attach the Fintech notebook session",
        "Initialize or attach the StratLake notebook session",
        "Verify attached session paths and notebook configs",
        "Verify the Notebook 07 StratLake archive checkpoint",
        "Restore the Notebook 07 StratLake archive checkpoint",
        "Verify restored StratLake configs, features, and artifacts",
        "Verify native StratLake workspace inputs",
        "Inspect native strategy registry",
        "Run native StratLake strategy backtest",
        "Parse native strategy output into review rows",
        "Discover native artifacts for the run",
        "Load plottable native time series when available",
        "Plot native strategy review output",
        "Benchmark comparison review",
        "Optional archive checkpoint refresh",
        "Final Notebook 08 handoff summary",
    ]
    last_index = -1
    for section in expected_sections:
        index = markdown_source.find(section)
        assert index > last_index, (
            f"Expected section {section!r} to appear after the prior Notebook 08 section."
        )
        last_index = index


# ---------------------------------------------------------------------------
# Output and metadata readiness
# ---------------------------------------------------------------------------


def test_all_code_cells_output_free_and_unexecuted(code_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )


def test_markdown_cells_have_no_outputs(markdown_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(markdown_cells):
        assert "outputs" not in cell, f"Markdown cell {i} unexpectedly has outputs."


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
            f"Runtime output metadata key {key!r} must not appear in Notebook 08 source."
        )


# ---------------------------------------------------------------------------
# Credential and secret surface readiness
# ---------------------------------------------------------------------------


def test_alpaca_credentials_are_runtime_references_only(code_source: str) -> None:
    assert "ALPACA_API_KEY_ID" in code_source
    assert "ALPACA_API_SECRET_KEY" in code_source
    assert "userdata.get(" in code_source or "getpass.getpass(" in code_source
    assert "ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY are set but not printed" in code_source


def test_no_raw_credential_prints(code_source: str) -> None:
    forbidden_prints = [
        "print(alpaca_api_key_id)",
        "print(alpaca_api_secret_key)",
        'print(os.environ["ALPACA_API_KEY_ID"])',
        'print(os.environ["ALPACA_API_SECRET_KEY"])',
    ]
    for snippet in forbidden_prints:
        assert snippet not in code_source
    assert "print(\"ALPACA_DATA_BASE_URL:\", os.environ.get(\"ALPACA_DATA_BASE_URL\"))" in code_source
    assert "print(\"ALPACA_FEED:\", os.environ.get(\"ALPACA_FEED\"))" in code_source


def test_no_concrete_alpaca_key_like_values(notebook_source: str) -> None:
    token_patterns = [
        r"\bPK[A-Z0-9]{16,}\b",
        r"\bSK[A-Z0-9]{16,}\b",
        "-----BEGIN [A-Z ]*" + "PRIVATE" + " KEY-----",
        r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+/\-]{8,}",
        r"password\s*=\s*['\"][^'\"]{8,}['\"]",
        r"token\s*=\s*['\"][^'\"]{8,}['\"]",
    ]
    for pattern in token_patterns:
        assert re.search(pattern, notebook_source, flags=re.IGNORECASE) is None, (
            f"Notebook 08 source appears to contain a concrete secret-like value: {pattern}"
        )


# ---------------------------------------------------------------------------
# Drive/path readiness and source path boundaries
# ---------------------------------------------------------------------------


def test_drive_placeholder_and_guard_present(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert "raise ValueError" in code_source


def test_no_user_specific_or_legacy_drive_paths(notebook_source: str) -> None:
    forbidden_fragments = [
        "fintech-stratlake-tutorial",
        "C:\\Users\\",
        "C:/Users/",
        "/Users/",
        "/home/",
        "/content/drive/MyDrive/fintech-market-ingestion",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in notebook_source, (
            f"Notebook 08 source contains forbidden user/path fragment: {fragment}"
        )


def test_no_specific_private_drive_folder_name(notebook_source: str) -> None:
    drive_folder_assignment = re.search(
        r'DRIVE_FOLDER_NAME\s*=\s*"([^"]+)"',
        notebook_source,
    )
    assert drive_folder_assignment is not None
    assert drive_folder_assignment.group(1) == "REPLACE_WITH_DRIVE_FOLDER_NAME"


def test_drive_directories_guarded_before_creation(code_source: str) -> None:
    first_guard = code_source.find('DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"')
    first_drive_mkdir = code_source.find("FINTECH_DRIVE_SESSION_ROOT")
    assert first_guard != -1
    assert first_drive_mkdir != -1
    assert first_guard < first_drive_mkdir, (
        "Placeholder guard must appear before Drive session/archive folder construction."
    )


# ---------------------------------------------------------------------------
# Runtime artifact exclusions and review-only source boundaries
# ---------------------------------------------------------------------------


def test_no_committed_notebook_08_runtime_artifact_paths(notebook_source: str) -> None:
    forbidden_runtime_fragments = [
        ".png",
        ".jpg",
        ".jpeg",
        ".log",
        "archive_packs/",
        "restore_packs/",
        "stratlake-session-stratlake_q1_feature_consumption/",
        "momentum_v1_single_",
    ]
    for fragment in forbidden_runtime_fragments:
        assert fragment not in notebook_source, (
            f"Notebook 08 source contains a likely generated runtime artifact fragment: {fragment}"
        )


def test_artifact_file_extensions_are_review_filters_only(code_source: str) -> None:
    assert 'p.suffix.lower() in {".json", ".csv", ".parquet", ".md", ".html"}' in code_source
    assert "pd.read_parquet" in code_source
    assert "pd.read_csv" in code_source
    assert "write_text(" not in code_source
    assert "to_parquet(" not in code_source
    assert "to_csv(" not in code_source


# ---------------------------------------------------------------------------
# Non-authoritative review stance and manual gate readiness
# ---------------------------------------------------------------------------


def test_non_authoritative_stance_documented(classification_doc_text: str) -> None:
    expected_phrases = [
        "Source classification is not live runtime validation",
        "does not mean archive restore, strategy backtest",
        "Manual/off-by-default source-safe action",
        "Intended runtime gate, not source-import evidence",
        "Review-only DataFrame; not authoritative benchmark or performance reporting",
        "Plots are not committed and are not proof of backtest success",
    ]
    for phrase in expected_phrases:
        assert phrase in classification_doc_text


def test_manual_restore_and_checkpoint_defaults_source_safe(code_source: str) -> None:
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = True" not in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = True" not in code_source
    assert "Restore command preview" in code_source
    assert "Dry run only. Set RUN_STRATLAKE_ARCHIVE_CHECKPOINT=True" in code_source


def test_restore_and_checkpoint_commands_are_guarded(code_source: str) -> None:
    assert "if RUN_STRATLAKE_ARCHIVE_RESTORE:" in code_source
    assert "if RUN_STRATLAKE_ARCHIVE_CHECKPOINT:" in code_source
    restore_command_index = code_source.find("!stratlake-session-archive-restore-bootstrap")
    restore_guard_index = code_source.find("if RUN_STRATLAKE_ARCHIVE_RESTORE:")
    assert restore_guard_index != -1 and restore_command_index > restore_guard_index
    checkpoint_run_index = code_source.find("subprocess.run(\n        archive_cmd")
    checkpoint_guard_index = code_source.find("if RUN_STRATLAKE_ARCHIVE_CHECKPOINT:")
    assert checkpoint_guard_index != -1 and checkpoint_run_index > checkpoint_guard_index


@pytest.mark.parametrize("gate", [
    "RUN_FINTECH_INIT_PROJECT = True",
    "RUN_STRATLAKE_INIT_SESSION = True",
    "RUN_NATIVE_STRATEGY_BACKTEST = True",
])
def test_intended_live_runtime_gates_preserved(code_source: str, gate: str) -> None:
    assert gate in code_source, (
        f"{gate} is accepted as an intended live workflow gate, but this source-only "
        "readiness test does not execute it or claim runtime success."
    )


# ---------------------------------------------------------------------------
# Classification document and readiness config coverage
# ---------------------------------------------------------------------------


def test_notebook_08_classification_document_readiness(classification_doc_text: str) -> None:
    expected_phrases = [
        "Source classification is not live runtime validation",
        "Drive/session-root configuration surface",
        "archive restore CLI surface",
        "native strategy execution CLI surface",
        "artifact review surface",
        "visual_review_surface",
        "benchmark comparison surface",
        "archive checkpoint refresh CLI surface",
        "Risk And Guardrails",
        "M11.4 / Issue #88",
        "M11.6 / Issue #90",
    ]
    for phrase in expected_phrases:
        assert phrase in classification_doc_text


def test_notebook_08_in_readiness_config() -> None:
    config_text = NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")
    assert "08_stratlake_strategy_backtest_artifact_review.ipynb" in config_text, (
        "Notebook 08 must be listed in config/notebook_test.toml default_targets "
        "so the shared source-readiness harness includes it."
    )
