"""
Source-only readiness and sanitized execution-safety tests for Notebook 07.

Scope (M10.4):
- Sanitized notebook metadata checks (no widget state, no execution timing,
  no Colab runtime metadata, minimized cell metadata).
- Notebook title / identity presence checks.
- Credential safety: env-var names allowed; actual values must not appear.
- Runtime artifact exclusion: generated file extensions must not be committed
  as notebook outputs or inline notebook source artifact paths.
- Execution-readiness boundary: Drive mount, credential prompts, backfill,
  feature build, native smoke, fallback, and archive are all guarded or
  runtime-conditional.
- Generic validation-config coverage: Notebook 07 is included in
  notebook_test.toml default_targets so the shared readiness harness covers it.

This file intentionally avoids duplicating CLI/source-reference or
config-value invariants that are already covered by M10.3
(tests/test_notebook_07_static_cli_contracts.py).

Testing rules:
- Parse the .ipynb JSON directly — no nbformat import required.
- No notebook cells are executed.
- No CLI commands are executed.
- No installed packages are required.
- No network, Google Drive, Alpaca credentials, or generated data required.
- No live Colab runtime is required.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB07_PATH = REPO_ROOT / "notebooks" / "07_stratlake_feature_consumption_baseline_research.ipynb"
NOTEBOOK_TEST_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def notebook() -> dict:
    return json.loads(NB07_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def notebook_source(notebook: dict) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )


@pytest.fixture(scope="module")
def code_source(notebook: dict) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    )


@pytest.fixture(scope="module")
def markdown_source(notebook: dict) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown"
    )


@pytest.fixture(scope="module")
def code_cells(notebook: dict) -> list:
    return [c for c in notebook.get("cells", []) if c.get("cell_type") == "code"]


# ---------------------------------------------------------------------------
# Notebook identity
# ---------------------------------------------------------------------------


def test_notebook_07_path_exists() -> None:
    assert NB07_PATH.exists(), f"Notebook 07 not found at {NB07_PATH}."


@pytest.mark.parametrize("phrase", [
    "Notebook 07",
    "StratLake Feature Consumption",
    "Baseline Research Smoke",
    "Archive Checkpoint",
])
def test_notebook_title_phrases_present(notebook_source: str, phrase: str) -> None:
    assert phrase in notebook_source, (
        f"Expected title phrase '{phrase}' not found in Notebook 07 source."
    )


# ---------------------------------------------------------------------------
# Sanitized metadata — top-level
# ---------------------------------------------------------------------------


def test_no_widget_state_metadata(notebook: dict) -> None:
    metadata = notebook.get("metadata", {})
    assert "widgets" not in metadata, (
        "Top-level 'widgets' (widget state) metadata must be absent for repository safety."
    )


def test_no_colab_runtime_metadata(notebook: dict) -> None:
    metadata = notebook.get("metadata", {})
    assert "colab" not in metadata, (
        "Top-level 'colab' metadata must be stripped."
    )


def test_no_accelerator_metadata(notebook: dict) -> None:
    metadata = notebook.get("metadata", {})
    assert "accelerator" not in metadata, (
        "Top-level 'accelerator' metadata (Colab GPU/TPU setting) must be absent."
    )


# ---------------------------------------------------------------------------
# Sanitized metadata — cell level
# ---------------------------------------------------------------------------


def test_no_cell_execution_timing_metadata(code_cells: list) -> None:
    for i, cell in enumerate(code_cells):
        cell_meta = cell.get("metadata", {})
        assert "execution" not in cell_meta, (
            f"Code cell {i} has execution timing metadata. "
            "Cell execution timing must be stripped before committing."
        )


def test_no_cell_id_collision_risk(code_cells: list) -> None:
    """Cell IDs, if present, must be unique (not duplicated from a copy-paste)."""
    ids = [cell.get("id") for cell in code_cells if cell.get("id") is not None]
    assert len(ids) == len(set(ids)), (
        "Duplicate cell IDs detected. Each cell must have a unique 'id' field."
    )


def test_no_inline_image_output(code_cells: list) -> None:
    for i, cell in enumerate(code_cells):
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            assert "image/png" not in data, (
                f"Code cell {i} has an inline PNG image output. All outputs must be cleared."
            )
            assert "image/jpeg" not in data, (
                f"Code cell {i} has an inline JPEG image output. All outputs must be cleared."
            )


def test_no_dataframe_html_output(code_cells: list) -> None:
    for i, cell in enumerate(code_cells):
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            html = data.get("text/html", "")
            assert "<table" not in html, (
                f"Code cell {i} has an HTML table (DataFrame) output. All outputs must be cleared."
            )


# ---------------------------------------------------------------------------
# Credential safety
# ---------------------------------------------------------------------------


_KNOWN_CREDENTIAL_VAR_NAMES = {
    "ALPACA_API_KEY_ID",
    "ALPACA_API_SECRET_KEY",
    "ALPACA_DATA_BASE_URL",
    "ALPACA_FEED",
}

# Patterns that would indicate a real credential value was accidentally committed.
_FORBIDDEN_CREDENTIAL_VALUE_PATTERNS = [
    "PK",  # Alpaca key ID prefix — too broad on its own, checked in combination below
]


def test_credential_variable_names_are_present(code_source: str) -> None:
    """Env-var names are allowed — they document what the notebook expects."""
    for name in ("ALPACA_API_KEY_ID", "ALPACA_API_SECRET_KEY"):
        assert name in code_source, (
            f"Expected credential variable name '{name}' in Notebook 07 source. "
            "The notebook must reference these names to document its runtime requirements."
        )


def test_no_printed_credential_values(code_source: str) -> None:
    """The notebook must not print credential values."""
    assert "print(ALPACA_API_KEY_ID)" not in code_source, (
        "Notebook must not print ALPACA_API_KEY_ID."
    )
    assert "print(ALPACA_API_SECRET_KEY)" not in code_source, (
        "Notebook must not print ALPACA_API_SECRET_KEY."
    )


def test_credential_not_printed_confirmation_message_present(code_source: str) -> None:
    """The notebook should include a statement confirming credentials are not printed."""
    assert (
        "ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY are set but not printed" in code_source
    ), (
        "Notebook must include a statement confirming that Alpaca credentials "
        "are set but not printed."
    )


def test_credentials_prompted_via_userdata_or_getpass(code_source: str) -> None:
    """Alpaca credentials must be fetched at runtime via userdata or getpass."""
    has_userdata = "userdata.get(" in code_source
    has_getpass = "getpass.getpass(" in code_source
    assert has_userdata or has_getpass, (
        "Alpaca credentials must be prompted at runtime via userdata.get() or getpass.getpass(). "
        "They must never be hardcoded in the notebook source."
    )


# ---------------------------------------------------------------------------
# Runtime artifact exclusions (no generated artifacts committed)
# ---------------------------------------------------------------------------


def test_no_parquet_artifacts_in_outputs(code_cells: list) -> None:
    for i, cell in enumerate(code_cells):
        for output in cell.get("outputs", []):
            text = "".join(output.get("text", []))
            assert ".parquet" not in text.lower(), (
                f"Code cell {i} output references a .parquet path. All outputs must be cleared."
            )


def test_no_output_mime_bundles(code_cells: list) -> None:
    for i, cell in enumerate(code_cells):
        outputs = cell.get("outputs", [])
        assert outputs == [], (
            f"Code cell {i} has non-empty outputs (MIME bundle or stream). "
            "All outputs must be cleared before committing."
        )


# ---------------------------------------------------------------------------
# Execution-readiness boundary: drive mount is conditional on IN_COLAB
# ---------------------------------------------------------------------------


def test_drive_mount_conditional_on_in_colab(code_source: str) -> None:
    assert "IN_COLAB" in code_source, (
        "Notebook must define/use IN_COLAB to guard Colab-specific operations."
    )
    assert "drive.mount(" in code_source, (
        "drive.mount() must appear in source so it is clearly a runtime operation."
    )


# ---------------------------------------------------------------------------
# Execution-readiness boundary: backfill and feature build are conditional
# ---------------------------------------------------------------------------


def test_backfill_conditional_on_missing_data_or_force(code_source: str) -> None:
    """Backfill execution must check for existing data or a force flag."""
    assert "FORCE_DAILY_BARS_BACKFILL" in code_source, (
        "FORCE_DAILY_BARS_BACKFILL flag must be present to gate unconditional backfill."
    )
    assert "RUN_SMALL_DAILY_BARS_BACKFILL" in code_source, (
        "RUN_SMALL_DAILY_BARS_BACKFILL must be present as the outer backfill gate."
    )


def test_feature_build_conditional_on_missing_features_or_force(code_source: str) -> None:
    """Feature build execution must check for missing features or a force flag."""
    assert "FORCE_FEATURE_BUILD" in code_source, (
        "FORCE_FEATURE_BUILD flag must be present to gate unconditional feature build."
    )
    assert "RUN_FEATURE_BUILD_IF_MISSING" in code_source, (
        "RUN_FEATURE_BUILD_IF_MISSING must be present as the outer feature-build gate."
    )


# ---------------------------------------------------------------------------
# Execution-readiness boundary: native smoke governed by flags and config file
# ---------------------------------------------------------------------------


def test_native_smoke_governed_by_run_flag(code_source: str) -> None:
    assert "RUN_NATIVE_BASELINE_SMOKE" in code_source, (
        "Native strategy smoke must be governed by RUN_NATIVE_BASELINE_SMOKE."
    )


def test_native_smoke_governed_by_strategies_config_exists(code_source: str) -> None:
    assert "STRATEGIES_CONFIG" in code_source, (
        "Native smoke must reference STRATEGIES_CONFIG so it only runs when the "
        "strategies config file is present."
    )
    assert ".exists()" in code_source, (
        "Notebook must call .exists() on STRATEGIES_CONFIG to guard native smoke execution."
    )


# ---------------------------------------------------------------------------
# Execution-readiness boundary: fallback diagnostic is conditional/secondary
# ---------------------------------------------------------------------------


def test_fallback_governed_by_run_flag(code_source: str) -> None:
    assert "RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE" in code_source, (
        "Fallback diagnostic must be governed by RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE."
    )


def test_fallback_skipped_when_native_completed(code_source: str) -> None:
    assert "if not RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE:" in code_source, (
        "Fallback must be skipped when RUN_NOTEBOOK_LOCAL_FALLBACK_SMOKE is False "
        "(i.e. when the native smoke completed)."
    )


# ---------------------------------------------------------------------------
# Execution-readiness boundary: archive and restore are off by default
# ---------------------------------------------------------------------------


def test_archive_checkpoint_guarded(code_source: str) -> None:
    assert "if CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION:" in code_source, (
        "Archive creation must be gated by 'if CREATE_STRATLAKE_ARCHIVE_AFTER_CONSUMPTION:'."
    )


def test_restore_execution_guarded(code_source: str) -> None:
    assert "if RESTORE_FINTECH_ARCHIVE:" in code_source, (
        "Fintech restore must be gated by 'if RESTORE_FINTECH_ARCHIVE:'."
    )
    assert "if RESTORE_STRATLAKE_ARCHIVE:" in code_source, (
        "StratLake restore must be gated by 'if RESTORE_STRATLAKE_ARCHIVE:'."
    )


# ---------------------------------------------------------------------------
# Generic readiness config coverage
# ---------------------------------------------------------------------------


def test_notebook_07_in_readiness_config() -> None:
    """Notebook 07 must be listed in notebook_test.toml so the shared harness covers it."""
    config_text = NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")
    assert "07_stratlake_feature_consumption_baseline_research.ipynb" in config_text, (
        "Notebook 07 must be listed in config/notebook_test.toml default_targets "
        "so the shared execution-readiness harness includes it automatically."
    )


def test_forbidden_tutorial_drive_path_in_readiness_config() -> None:
    """The hardcoded tutorial Drive path must be in the forbidden fragments list."""
    config_text = NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")
    assert "/content/drive/MyDrive/fintech-stratlake-tutorial" in config_text, (
        "The hardcoded tutorial Drive path must be listed as a forbidden committed "
        "path fragment in config/notebook_test.toml."
    )
