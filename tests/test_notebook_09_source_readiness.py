"""
Source-only readiness and sanitized validation tests for Notebook 09.

Scope (M12.4):
- Notebook structure and ordered workflow-section checks.
- Sanitized metadata checks: no Colab runtime metadata, cell ids, execution info,
  output ids, widgets/display state, committed outputs, or image MIME payloads.
- Credential and Drive placeholder safety checks.
- Runtime artifact exclusion and non-authoritative review stance checks.
- Manual/off-by-default restore/checkpoint boundary checks.

Testing rules:
- Parse the .ipynb JSON directly.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages are required.
- No network, Google Drive, Alpaca credentials, archives, native artifacts, plots,
  logs, manifests, restored files, or generated data are required.
- No live Colab runtime is required.
"""

from __future__ import annotations

import json
import re
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
NOTEBOOK_TEST_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


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


def test_notebook_09_path_exists() -> None:
    assert NB09_PATH.exists(), f"Notebook 09 not found at {NB09_PATH}."


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


@pytest.mark.parametrize(
    "metadata_key",
    ["id", "executionInfo", "outputId", "colab", "execution", "widgets", "scrolled"],
)
def test_cell_runtime_metadata_absent(notebook: dict[str, Any], metadata_key: str) -> None:
    for i, cell in enumerate(notebook.get("cells", [])):
        assert metadata_key not in cell, (
            f"Notebook cell {i} has forbidden top-level cell key {metadata_key!r}."
        )
        assert metadata_key not in cell.get("metadata", {}), (
            f"Notebook cell {i} has forbidden metadata key {metadata_key!r}."
        )


def test_no_runtime_output_metadata_or_mime_payloads(notebook: dict[str, Any]) -> None:
    forbidden_keys = (
        "executionInfo",
        "outputId",
        "application/vnd.google.colaboratory",
        "image/png",
        "image/jpeg",
        "text/html",
    )
    for key in forbidden_keys:
        assert not _json_key_present(notebook, key), (
            f"Runtime output metadata key {key!r} must not appear in Notebook 09 source."
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


def test_no_concrete_credential_like_values(notebook_source: str) -> None:
    token_patterns = [
        r"\bPK[A-Z0-9]{16,}\b",
        r"\bSK[A-Z0-9]{16,}\b",
        "-----BEGIN [A-Z ]*" + "PRIVATE" + " KEY-----",
        r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+/\-]{8,}",
        r"password\s*=\s*['\"][^'\"]{8,}['\"]",
        r"token\s*=\s*['\"][^'\"]{8,}['\"]",
        r"api[_-]?secret\s*=\s*['\"][^'\"]{8,}['\"]",
    ]
    for pattern in token_patterns:
        assert re.search(pattern, notebook_source, flags=re.IGNORECASE) is None, (
            f"Notebook 09 source appears to contain a concrete secret-like value: {pattern}"
        )


# ---------------------------------------------------------------------------
# Drive/path readiness and source path boundaries
# ---------------------------------------------------------------------------


def test_drive_placeholder_and_guard_present(code_source: str) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'Path("/content/drive/MyDrive") / DRIVE_FOLDER_NAME' in code_source
    assert 'WORKSPACE_ROOT / "drive" / DRIVE_FOLDER_NAME' in code_source
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
        "/content/drive/MyDrive/fintech-stratlake-tutorial",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in notebook_source, (
            f"Notebook 09 source contains forbidden user/path fragment: {fragment}"
        )


def test_no_specific_private_drive_folder_name(notebook_source: str) -> None:
    drive_folder_assignment = re.search(
        r'DRIVE_FOLDER_NAME\s*=\s*"([^"]+)"',
        notebook_source,
    )
    assert drive_folder_assignment is not None
    assert drive_folder_assignment.group(1) == "REPLACE_WITH_DRIVE_FOLDER_NAME"


def test_drive_directories_guarded_before_drive_session_archive_use(code_source: str) -> None:
    first_guard = code_source.find('DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"')
    first_drive_namespace = code_source.find("FINTECH_DRIVE_ROOT")
    first_drive_mkdir = code_source.find("FINTECH_DRIVE_SESSION_ROOT")
    assert first_guard != -1
    assert first_drive_namespace != -1
    assert first_drive_mkdir != -1
    assert first_guard < first_drive_namespace < first_drive_mkdir, (
        "Placeholder guard must appear before Drive session/archive folder use."
    )


# ---------------------------------------------------------------------------
# Runtime artifact exclusions and review-only boundaries
# ---------------------------------------------------------------------------


def test_no_committed_notebook_09_runtime_artifact_fragments(notebook_source: str) -> None:
    forbidden_runtime_fragments = [
        "data:image/",
        ";base64,",
        "archive_packs/",
        "restore_packs/",
        "stratlake-session-stratlake_q1_feature_consumption/",
        "strategy_comparison.csv",
        "strategy_comparison.json",
        "session_manifest\":{\"",
        "Traceback (most recent call last)",
    ]
    for fragment in forbidden_runtime_fragments:
        assert fragment not in notebook_source, (
            f"Notebook 09 source contains a likely generated runtime artifact fragment: {fragment}"
        )


def test_artifact_extensions_are_discovery_filters_not_committed_payloads(code_source: str) -> None:
    assert 'p.suffix.lower() in [".json", ".csv", ".parquet", ".md", ".html"]' in code_source
    assert "artifact_inventory" in code_source
    assert "write_text(" not in code_source
    assert "to_parquet(" not in code_source
    assert "to_csv(" not in code_source
    assert "to_json(" not in code_source


# ---------------------------------------------------------------------------
# Manual gate readiness and non-authoritative stance
# ---------------------------------------------------------------------------


def test_manual_restore_and_checkpoint_defaults_source_safe(code_source: str) -> None:
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = True" not in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = True" not in code_source
    assert "Manual restore is off by default in committed source" in code_source
    assert "Dry run only. Set RUN_STRATLAKE_ARCHIVE_CHECKPOINT=True" in code_source


def test_native_strategy_comparison_gate_is_runtime_intent_not_source_proof(
    code_source: str,
    classification_doc_text: str,
) -> None:
    assert "RUN_NATIVE_STRATEGY_COMPARISON = True" in code_source
    expected_phrases = [
        "Native strategy comparison is intended live runtime behavior",
        "Source import does not claim strategy execution success",
        "Source import does not prove",
        "performance validity",
    ]
    for phrase in expected_phrases:
        assert phrase in classification_doc_text


def test_non_authoritative_review_stance_documented(classification_doc_text: str) -> None:
    expected_phrases = [
        "Parsed rows are review evidence",
        "The dataframe is a review surface",
        "Plots are runtime/review surfaces",
        "Artifact inventories are review surfaces",
        "research decision summary is a review/handoff surface",
        "Do not claim archive restore success",
        "Do not claim strategy comparison success",
        "Do not claim all-strategy correctness",
        "Do not claim authoritative performance results",
        "Do not claim benchmark rows prove alpha",
        "Do not claim plot correctness",
        "Do not claim artifact discovery correctness",
        "Do not claim archive checkpoint refresh success",
        "Do not claim Notebook 10 behavior is validated",
        "Do not claim source import proves runtime correctness",
    ]
    for phrase in expected_phrases:
        assert phrase in classification_doc_text


def test_notebook_source_preserves_native_first_boundary(notebook_source: str) -> None:
    expected_phrases = [
        "Native Fintech and StratLake commands are preferred",
        "Notebook code is used for orchestration, parsing, display, and artifact review",
        "does not implement custom strategy logic",
        "StratLake-native normalization, backtesting, feature generation, or archive behavior",
    ]
    for phrase in expected_phrases:
        assert phrase in notebook_source


# ---------------------------------------------------------------------------
# Classification document and shared readiness harness coverage
# ---------------------------------------------------------------------------


def test_notebook_09_classification_document_readiness(classification_doc_text: str) -> None:
    expected_phrases = [
        "Notebook 09",
        "Source-Only Validation Guidance",
        "runtime-only",
        "Non-Authoritative",
        "Expected CLI commands are present",
        "Drive folder configuration must use the placeholder pattern",
        "Restore is manual/off-by-default",
        "Checkpoint refresh is optional/manual/off-by-default",
        "The final handoff points toward Notebook 10",
        "Source import does not validate Notebook 10 behavior",
    ]
    for phrase in expected_phrases:
        assert phrase in classification_doc_text


def test_notebook_09_in_readiness_config() -> None:
    config_text = NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")
    assert "09_stratlake_strategy_comparison_and_research_review.ipynb" in config_text, (
        "Notebook 09 must be listed in config/notebook_test.toml default_targets "
        "so the shared source-readiness harness includes it."
    )
