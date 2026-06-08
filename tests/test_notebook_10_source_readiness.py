"""
Source-only readiness and sanitized validation tests for Notebook 10.

Scope (M13.3):
- Notebook JSON parseability, source shape, output-free state, metadata hygiene,
  credential safety, Drive placeholder safety, runtime artifact exclusions, and
  documentation readiness.
- No notebook cells or CLI commands are executed.
"""

from __future__ import annotations

import json
import re
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
NOTEBOOK_TEST_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


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


def test_notebook_10_json_parseability_and_cell_shape(notebook: dict[str, Any]) -> None:
    cells = notebook.get("cells", [])
    assert notebook.get("nbformat") == 4
    assert notebook.get("nbformat_minor") == 5
    assert len(cells) == 41
    assert sum(1 for cell in cells if cell.get("cell_type") == "markdown") == 21
    assert sum(1 for cell in cells if cell.get("cell_type") == "code") == 20


def test_code_cells_output_free_and_execution_counts_null(
    code_cells: list[dict[str, Any]],
) -> None:
    for i, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {i} has non-null execution_count."
        )


def test_markdown_cells_have_no_outputs(markdown_cells: list[dict[str, Any]]) -> None:
    for i, cell in enumerate(markdown_cells):
        assert "outputs" not in cell, f"Markdown cell {i} unexpectedly has outputs."


def test_top_level_metadata_limited_to_repo_convention(notebook: dict[str, Any]) -> None:
    assert set(notebook.get("metadata", {})) == {"kernelspec", "language_info"}
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"
    assert notebook["metadata"]["language_info"]["name"] == "python"


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
    for key in (
        "executionInfo",
        "outputId",
        "application/vnd.google.colaboratory",
        "image/png",
        "image/jpeg",
        "text/html",
    ):
        assert not _json_key_present(notebook, key), (
            f"Runtime output metadata key {key!r} must not appear in Notebook 10 source."
        )


def test_title_and_draft_identity_clean(notebook: dict[str, Any], notebook_source: str) -> None:
    assert "Notebook 10 — StratLake Walk-Forward Robustness and Promotion Review" in notebook_source
    assert "Draft v4" not in notebook_source
    assert "Draft v3" not in notebook_source
    assert "notebook_10_draft_version" not in notebook_source
    assert "notebook_10_draft_version" not in notebook.get("metadata", {})


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
            f"Notebook 10 source appears to contain a concrete secret-like value: {pattern}"
        )


def test_drive_placeholder_and_private_path_boundaries(
    code_source: str,
    notebook_source: str,
) -> None:
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assert 'DRIVE_FOLDER_NAME == "REPLACE_WITH_DRIVE_FOLDER_NAME"' in code_source
    assignment = re.search(r'DRIVE_FOLDER_NAME\s*=\s*"([^"]+)"', notebook_source)
    assert assignment is not None
    assert assignment.group(1) == "REPLACE_WITH_DRIVE_FOLDER_NAME"

    forbidden_fragments = [
        "TEST1",
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
            f"Notebook 10 source contains forbidden user/path fragment: {fragment}"
        )


def test_runtime_artifact_payloads_are_not_committed(notebook_source: str) -> None:
    forbidden_runtime_fragments = [
        "data:image/",
        ";base64,",
        "Traceback (most recent call last)",
        "archive_packs/",
        "restore_packs/",
        "notebook_10_walk_forward_promotion_review_v4",
    ]
    for fragment in forbidden_runtime_fragments:
        assert fragment not in notebook_source, (
            f"Notebook 10 source contains likely generated runtime payload: {fragment}"
        )


def test_artifact_writes_are_source_references_not_committed_outputs(
    code_source: str,
) -> None:
    assert 'NOTEBOOK10_REVIEW_DIR = STRATLAKE_ROOT / "artifacts"' in code_source
    assert '"notebook_10_walk_forward_promotion_review"' in code_source
    assert ".to_csv(" in code_source
    assert ".to_json(" in code_source
    assert ".write_text(" in code_source
    assert "artifact_inventory" in code_source


def test_smoke_mode_non_claim_language_present(
    notebook_source: str,
    docs_text: str,
) -> None:
    assert "smoke mode validates workflow wiring" in notebook_source
    assert "not promotion-grade financial evidence" in notebook_source
    assert "benchmark avoidance" in notebook_source
    assert "benchmark-avoidance" in docs_text
    assert "not alpha" in docs_text


def test_manual_restore_checkpoint_and_strategy_execution_boundaries(
    code_source: str,
    docs_text: str,
) -> None:
    assert "RUN_STRATLAKE_ARCHIVE_RESTORE = False" in code_source
    assert "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False" in code_source
    assert "RUN_NATIVE_WALK_FORWARD_EVALUATION = True" in code_source
    assert "Native strategy execution and walk-forward smoke/expanded evaluation are live/manual" in docs_text
    assert "Repository validation must not execute notebook cells" in docs_text


def test_notebook_10_docs_readiness_and_source_only_stance(docs_text: str) -> None:
    expected_phrases = [
        "Notebook 10 Command Surface Classification",
        "Notebook 10 Staging Classification",
        "source-safe",
        "live/manual",
        "guarded",
        "out of CI scope",
        "Feature-contract finding, not runtime failure",
        "M13.2 does not claim promotion-grade evidence",
        "notebook_10_command_runtime_surfaces_classified",
    ]
    for phrase in expected_phrases:
        assert phrase in docs_text


def test_notebook_10_in_shared_readiness_config() -> None:
    config_text = NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")
    assert "10_stratlake_walk_forward_robustness_and_promotion_review.ipynb" in config_text, (
        "Notebook 10 must be listed in config/notebook_test.toml default_targets "
        "so the shared source-readiness harness includes it."
    )
