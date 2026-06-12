"""
Static source-contract tests for Notebook 12.

Scope (M15.3):
- Parse committed notebook and classification docs source only.
- Verify source-safe notebook shape, profile controls, runtime guards, generated
  smoke config source fields, artifact/context handoff fields, claim flags,
  classification docs, and non-claim language.
- Do not execute notebook cells, CLI commands, package installs, Drive mounts,
  archive restores, native StratLake campaign commands, artifact writes, or
  checkpoint refreshes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB12_PATH = (
    REPO_ROOT
    / "notebooks"
    / "12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb"
)
COMMAND_CLASSIFICATION_DOC = (
    REPO_ROOT / "docs" / "notebook_12_command_surface_classification.md"
)
STAGING_CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_12_staging_classification.md"


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB12_PATH.read_text(encoding="utf-8"))


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
        path.read_text(encoding="utf-8")
        for path in [COMMAND_CLASSIFICATION_DOC, STAGING_CLASSIFICATION_DOC]
    )


def _json_key_present(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_json_key_present(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_json_key_present(item, key) for item in value)
    return False


def _dict_default_false_present(code_source: str, name: str) -> bool:
    return re.search(rf'"{name}"\s*:\s*False\b', code_source) is not None


def test_notebook_12_path_exists() -> None:
    assert NB12_PATH.exists()


def test_notebook_12_json_shape_and_source_role(
    notebook: dict[str, Any],
    notebook_source: str,
) -> None:
    cells = notebook.get("cells", [])
    assert notebook.get("nbformat") == 4
    assert len(cells) == 50
    assert sum(1 for cell in cells if cell.get("cell_type") == "markdown") == 29
    assert sum(1 for cell in cells if cell.get("cell_type") == "code") == 21
    assert "Notebook 12" in notebook_source
    assert "campaign evidence reviewer" in notebook_source
    assert "notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb" in notebook_source


def test_notebook_12_output_free_unexecuted_and_metadata_minimized(
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
    for key in ("colab", "widgets", "executionInfo", "outputId", "image/png"):
        assert not _json_key_present(notebook, key), (
            f"Runtime metadata or output payload key {key!r} must not appear."
        )


@pytest.mark.parametrize(
    "profile",
    [
        "NOTEBOOK12_TEST_PROFILE",
        "cold_smoke_1_preview",
        "cold_smoke_5_command_shape_readiness",
        "campaign_smoke_preview",
        "campaign_smoke_dry_run",
        "campaign_smoke_dry_run_allow_provisional",
        "campaign_smoke_execute_allow_provisional_no_dry_run",
    ],
)
def test_required_profile_strings_are_preserved(notebook_source: str, profile: str) -> None:
    assert profile in notebook_source


@pytest.mark.parametrize(
    "guard",
    [
        "ALLOW_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG_FOR_EXECUTION",
        "ALLOW_NON_DRY_RUN_NATIVE_CAMPAIGN_SMOKE_EXECUTION",
        "VALIDATE_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG",
        "REQUIRE_DRY_RUN_ARGUMENT_FOR_NATIVE_CAMPAIGN_SMOKE",
        "NATIVE_CAMPAIGN_SMOKE_DRY_RUN_ONLY",
    ],
)
def test_required_guard_strings_are_preserved(notebook_source: str, guard: str) -> None:
    assert guard in notebook_source


def test_default_profile_implementation_and_documentation_are_aligned(
    code_source: str,
    markdown_source: str,
    docs_text: str,
) -> None:
    assert (
        'NOTEBOOK12_TEST_PROFILE = os.environ.get("NOTEBOOK12_TEST_PROFILE", '
        '"cold_smoke_5_command_shape_readiness").strip() or '
        '"cold_smoke_5_command_shape_readiness"'
    ) in code_source
    assert "Committed import default is `cold_smoke_5_command_shape_readiness`" in markdown_source
    assert "`cold_smoke_1_preview` remains available as the baseline no-restore preview" in docs_text
    assert "committed import default is\n`cold_smoke_5_command_shape_readiness`" in docs_text


def test_native_campaign_smoke_execution_is_guarded_off_by_default(
    code_source: str,
) -> None:
    for guard_name in [
        "RUN_NATIVE_CAMPAIGN_SMOKE",
        "ALLOW_NATIVE_CAMPAIGN_SMOKE_EXECUTION",
        "ALLOW_NON_DRY_RUN_NATIVE_CAMPAIGN_SMOKE_EXECUTION",
        "ALLOW_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG_FOR_EXECUTION",
    ]:
        assert _dict_default_false_present(code_source, guard_name)
    assert '"NATIVE_CAMPAIGN_SMOKE_DRY_RUN_ONLY": True' in code_source
    assert '"REQUIRE_DRY_RUN_ARGUMENT_FOR_NATIVE_CAMPAIGN_SMOKE": True' in code_source
    assert "if RUN_NATIVE_CAMPAIGN_SMOKE:" in code_source
    assert "elif not ALLOW_NATIVE_CAMPAIGN_SMOKE_EXECUTION:" in code_source
    assert (
        "elif not NATIVE_CAMPAIGN_SMOKE_DRY_RUN_ONLY "
        "and not ALLOW_NON_DRY_RUN_NATIVE_CAMPAIGN_SMOKE_EXECUTION:"
    ) in code_source


@pytest.mark.parametrize(
    "token",
    [
        "native_campaign_smoke_config_source",
        "native_campaign_smoke_config_is_notebook_generated",
        "native_campaign_smoke_config_is_native_template",
        "notebook12_generated_smoke_config",
        "native_campaign_template",
        "selected_campaign_smoke_config_is_notebook_generated",
        "selected_campaign_smoke_config_is_native_template",
    ],
)
def test_generated_smoke_config_source_fields_are_preserved(
    notebook_source: str,
    token: str,
) -> None:
    assert token in notebook_source


@pytest.mark.parametrize(
    "token",
    [
        "notebook12_review_artifact_rows",
        "native_campaign_artifact_rows",
        "candidate_campaign_context_rows",
        "campaign_context_loaded",
        "CAMPAIGN_DISCOVERY_INCLUDE_NOTEBOOK12_REVIEW_DIR",
        "path_is_relative_to(path, NOTEBOOK12_REVIEW_DIR)",
        "notebook12_review_artifact",
    ],
)
def test_artifact_context_handoff_fields_are_preserved(
    notebook_source: str,
    token: str,
) -> None:
    assert token in notebook_source


@pytest.mark.parametrize(
    "token",
    [
        "promotion_grade_claim_made",
        "runtime_execution_claim_made",
        '"promotion_grade_claim_made": False',
        '"runtime_execution_claim_made": bool(native_campaign_smoke_result.get("executed", False))',
    ],
)
def test_claim_flags_are_preserved(notebook_source: str, token: str) -> None:
    assert token in notebook_source


def test_non_claim_language_remains_present(notebook_source: str) -> None:
    required_non_claim_phrases = [
        "do not mean approval, promotion, alpha confirmation, production readiness, or statistical significance",
        "does not make approval, alpha, production-readiness, statistical-significance, or promotion-grade claims",
        "does not claim campaign correctness",
        "It does **not** reimplement StratLake strategy logic, campaign orchestration, metrics, promotion gates, or governance logic",
        "it will not execute that provisional config unless explicitly allowed",
    ]
    for phrase in required_non_claim_phrases:
        assert phrase in notebook_source


@pytest.mark.parametrize(
    "forbidden_pattern",
    [
        r"\bapproved for promotion\b",
        r"\bstrategy approved\b",
        r"\balpha (?:validated|confirmed|ready)\b",
        r"\bproduction[- ]ready\b",
        r"\bproduction readiness certified\b",
        r"\bstatistically significant\b",
        r"\bpromotion-grade readiness achieved\b",
        r"\bCI/native runtime equivalence\b",
    ],
)
def test_positive_readiness_or_equivalence_claims_are_not_introduced(
    notebook_source: str,
    forbidden_pattern: str,
) -> None:
    assert re.search(forbidden_pattern, notebook_source, flags=re.IGNORECASE) is None


def test_classification_docs_exist_and_preserve_boundaries(docs_text: str) -> None:
    assert COMMAND_CLASSIFICATION_DOC.exists()
    assert STAGING_CLASSIFICATION_DOC.exists()
    normalized_docs_text = re.sub(r"\s+", " ", docs_text)
    for token in [
        "source-safe campaign evidence gap review and human-review handoff notebook",
        "does not replace native StratLake campaign execution",
        "It is not native StratLake campaign orchestration",
        "notebook12_generated_smoke_config",
        "`native_campaign_artifact_rows`, `notebook12_review_artifact_rows`, and",
        "Missing campaign context or missing promotion evidence should be documented as caveats",
        "`campaign_smoke_execute_allow_provisional_no_dry_run`",
        "committed import default is `cold_smoke_5_command_shape_readiness`",
    ]:
        assert token in normalized_docs_text
