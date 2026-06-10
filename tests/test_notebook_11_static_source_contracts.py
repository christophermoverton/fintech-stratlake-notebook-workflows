"""
Static source-contract and source-readiness tests for Notebook 11.

Scope (M14.1-M14.6):
- Parse committed notebook source only.
- Verify source-safe controls, guarded runtime surfaces, expanded-run command
  shape, artifact paths, Notebook 10 context references, install fallback
  pattern, governance guardrails, classification docs, readiness config, and
  non-claim language.
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
COMMAND_CLASSIFICATION_DOC = (
    REPO_ROOT / "docs" / "notebook_11_command_surface_classification.md"
)
STAGING_CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_11_staging_classification.md"
IMPORT_AUDIT_DOC = REPO_ROOT / "docs" / "notebook_11_import_audit.md"
NOTEBOOK_TEST_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"
NOTEBOOK_INDEX_DOC = REPO_ROOT / "docs" / "notebook_index.md"
README_DOC = REPO_ROOT / "README.md"
NOTEBOOK11_ARTIFACT_DIR = (
    REPO_ROOT / "artifacts" / "notebook_11_expanded_promotion_evidence_review"
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


@pytest.fixture(scope="module")
def docs_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            COMMAND_CLASSIFICATION_DOC,
            STAGING_CLASSIFICATION_DOC,
            IMPORT_AUDIT_DOC,
        ]
    )


@pytest.fixture(scope="module")
def notebook_test_config_text() -> str:
    return NOTEBOOK_TEST_CONFIG.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def repo_docs_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in [NOTEBOOK_INDEX_DOC, README_DOC, IMPORT_AUDIT_DOC]
    )


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


def test_expanded_preview_defensive_shutdowns_preserved(code_source: str) -> None:
    assert 'elif NOTEBOOK11_MODE == "expanded_preview":' in code_source
    preview_block = code_source.split('elif NOTEBOOK11_MODE == "expanded_preview":', 1)[1]
    preview_block = preview_block.split("for path in [FINTECH_ROOT, STRATLAKE_ROOT]:", 1)[0]
    for assignment in [
        "RUN_EXPANDED_STRATEGY_EVALUATION = False",
        "RUN_PROMOTION_GOVERNANCE_REPORT = False",
        "RUN_EVIDENCE_REVIEW_CLI_BUILD = False",
        "RUN_PROMOTION_GOVERNANCE_REPORT_CLI = False",
        "RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False",
    ]:
        assert assignment in preview_block


def test_install_fallback_pattern_preserved(notebook_source: str) -> None:
    assert '!pip install -q "pandas-market-calendars>=5.0"' in notebook_source
    assert (
        "!pip install -q --index-url https://test.pypi.org/simple/ "
        "--extra-index-url https://pypi.org/simple/ fintech-market-ingestion"
    ) in notebook_source
    assert (
        "!pip install -q --index-url https://test.pypi.org/simple/ "
        "--extra-index-url https://pypi.org/simple/ stratlake-trade-engine"
    ) in notebook_source


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


def test_alpaca_credentials_are_guarded_and_secret_safe(
    code_source: str,
    notebook_source: str,
) -> None:
    assert "RUN_LOAD_ALPACA_ENV = False" in code_source
    assert "if RUN_LOAD_ALPACA_ENV:" in code_source
    assert "get_secret_or_prompt(\"ALPACA_API_KEY_ID\")" in code_source
    assert "get_secret_or_prompt(\"ALPACA_API_SECRET_KEY\")" in code_source
    assert "ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY are set but not printed" in code_source
    for forbidden in [
        "print(alpaca_api_key_id)",
        "print(alpaca_api_secret_key)",
        'print(os.environ["ALPACA_API_KEY_ID"])',
        'print(os.environ["ALPACA_API_SECRET_KEY"])',
    ]:
        assert forbidden not in code_source
    secret_like_patterns = [
        r"\bPK[A-Z0-9]{16,}\b",
        r"\bSK[A-Z0-9]{16,}\b",
        r"api[_-]?secret\s*=\s*['\"][^'\"]{8,}['\"]",
        r"password\s*=\s*['\"][^'\"]{8,}['\"]",
        r"token\s*=\s*['\"][^'\"]{8,}['\"]",
        r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+/\-]{8,}",
    ]
    for pattern in secret_like_patterns:
        assert re.search(pattern, notebook_source, flags=re.IGNORECASE) is None


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


@pytest.mark.parametrize(
    "artifact_name",
    [
        "walk_forward_results",
        "robustness_summary",
        "promotion_review",
        "preflight_summary",
        "artifact_inventory",
        "summary.json",
        "smoke_audit_summary.json",
    ],
)
def test_notebook10_expected_artifact_references_preserved(
    notebook_source: str,
    artifact_name: str,
) -> None:
    assert artifact_name in notebook_source


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


def test_expanded_run_documented_but_manual_candidate_execution_disabled_by_default(
    notebook_source: str,
    code_source: str,
) -> None:
    assert "NOTEBOOK11_MODE = \"expanded_run\"" in notebook_source
    assert "RUN_EXPANDED_STRATEGY_EVALUATION = True" in notebook_source
    assert "ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS = True" in notebook_source
    assert "expanded_strategy_execution_not_run_default_off" in notebook_source
    assert _has_env_bool_default(code_source, "ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS", "False")


def test_governance_schema_discovery_and_execution_boundaries_preserved(
    code_source: str,
    docs_text: str,
) -> None:
    assert _has_env_bool_default(code_source, "RUN_EVIDENCE_REVIEW_CLI_BUILD", "False")
    assert _has_env_bool_default(code_source, "RUN_PROMOTION_GOVERNANCE_REPORT_CLI", "False")
    assert "RUN_GOVERNANCE_CLI_SCHEMA_DISCOVERY = env_bool(" in code_source
    assert '"stratlake-build-evidence-review", "build", "--help"' in code_source
    assert '"stratlake-run-promotion-governance-report", "--help"' in code_source
    assert '"stratlake-build-evidence-review"' in code_source
    assert '"stratlake-run-promotion-governance-report"' in code_source
    assert "schema discovery" in docs_text
    assert "Governance/evidence-review CLI execution" in docs_text


def test_non_claim_and_review_framing_preserved(notebook_source: str) -> None:
    assert "does **not** introduce a new promotion engine" in notebook_source
    assert "does **not** claim alpha" in notebook_source
    assert "production readiness" in notebook_source
    assert "statistical significance" in notebook_source
    assert "promotion-grade evidence by default" in notebook_source
    assert "expanded evidence" in notebook_source
    assert "caveat" in notebook_source
    assert "promotion-readiness interpretation" in notebook_source


def test_non_claim_and_evidence_caveat_language_preserved_in_docs(
    docs_text: str,
) -> None:
    for phrase in [
        "does not approve strategies",
        "does not prove live package installation",
        "strategy approval",
        "statistical significance",
        "complete platform artifact coverage",
        "CI/runtime equivalence",
        "promotion-grade evidence",
        "Command success is not promotion-grade evidence by itself",
        "Metric loading is useful but incomplete without split metrics and promotion",
        "Notebook 11 interpretive packages are notebook-scoped review aids only",
        "Platform split metrics and promotion gates remain required",
        "Source import is not runtime proof",
        "CI validation is not Colab/manual runtime equivalence",
    ]:
        assert phrase in docs_text


def test_runtime_surface_classification_docs_exist_and_use_expected_taxonomy(
    docs_text: str,
) -> None:
    assert COMMAND_CLASSIFICATION_DOC.exists()
    assert STAGING_CLASSIFICATION_DOC.exists()
    assert IMPORT_AUDIT_DOC.exists()
    for term in [
        "source_only",
        "live_manual",
        "guarded_runtime",
        "runtime_validation",
        "artifact_review",
        "promotion_readiness_review",
        "out_of_ci_scope",
    ]:
        assert term in docs_text


@pytest.mark.parametrize(
    "token",
    [
        "pandas-market-calendars",
        "fintech-market-ingestion",
        "stratlake-trade-engine",
        "fintech-init-project",
        "stratlake-init-session",
        "stratlake-session-archive-restore-bootstrap",
        "stratlake-run-strategy",
        "stratlake-build-evidence-review",
        "stratlake-run-promotion-governance-report",
        "stratlake-session-archive-bootstrap",
    ],
)
def test_runtime_surface_classification_docs_reference_key_commands(
    docs_text: str,
    token: str,
) -> None:
    assert token in docs_text


def test_runtime_surface_classification_docs_preserve_boundaries(
    docs_text: str,
) -> None:
    assert "artifacts/notebook_11_expanded_promotion_evidence_review/" in docs_text
    assert "Notebook 11 interpretive packages are notebook-scoped review aids only" in docs_text
    assert "Command success is not promotion-grade evidence by itself" in docs_text
    assert "Metric loading is useful but incomplete without split metrics and promotion" in docs_text
    assert "Source import is not runtime proof" in docs_text
    assert "CI validation is not Colab/manual runtime equivalence" in docs_text
    assert "Notebook 11 does not approve strategies" in docs_text


def test_import_audit_records_m14_closeout_and_validation(repo_docs_text: str) -> None:
    assert "Issues #109 through #114" in repo_docs_text
    assert "Issue #112" in repo_docs_text
    assert "Issue #114" in repo_docs_text
    assert "notebook_11_staged_clean_source_safe" in repo_docs_text
    assert "notebook_11_static_source_readiness_covered" in repo_docs_text
    assert "notebook_11_import_audit_docs_index_updated" in repo_docs_text
    assert "45 passed" in repo_docs_text
    assert "TestPyPI + PyPI fallback pattern" in repo_docs_text


def test_issue_114_runtime_smoke_evidence_is_source_documented(
    repo_docs_text: str,
) -> None:
    for token in [
        "notebook_11_expanded_preview_runtime_smoke_passed_with_expected_blockers",
        "notebook_11_expanded_run_restored_context_preview_passed_with_execution_not_enabled",
        "notebook_11_expanded_run_smoke_passed_with_metrics_review_artifacts_incomplete",
        "expanded_run_completed_with_metrics_review_artifacts_incomplete",
        "expanded_runs_attempted = 4",
        "expanded_runs_completed = 4",
        "expanded_metric_rows = 4",
        "expanded_split_metric_rows = 0",
        "expanded_complete_review_artifact_count = 0",
        "eligible_for_human_watchlist_review_count = 0",
        "promotion_grade_claim_made = false",
        "Generated runtime artifacts must stay out of Git",
    ]:
        assert token in repo_docs_text


def test_notebook_index_and_readme_document_notebook_11_identity(
    repo_docs_text: str,
) -> None:
    for token in [
        "Notebook 11",
        "StratLake Expanded Promotion Evidence Review",
        "notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb",
        "From confidence review to promotion evidence",
        "expanded evidence sufficiency review",
        "expanded_preview",
        "expanded_run",
        "artifacts/notebook_11_expanded_promotion_evidence_review/",
        "does not approve strategies",
        "does not claim alpha",
        "does not claim alpha, production readiness, strategy approval, statistical significance",
    ]:
        assert token in repo_docs_text


def test_notebook_11_included_in_source_only_readiness_config(
    notebook_test_config_text: str,
) -> None:
    assert "notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb" in notebook_test_config_text
    assert "require_no_outputs = true" in notebook_test_config_text
    assert "require_null_execution_counts = true" in notebook_test_config_text
    assert "compile_python_cells = true" in notebook_test_config_text
    assert "skip_shell_cells = true" in notebook_test_config_text
    assert "skip_colab_cells = true" in notebook_test_config_text
    assert "skip_drive_mount_cells = true" in notebook_test_config_text
    assert "skip_credential_cells = true" in notebook_test_config_text
    assert "skip_network_cells = true" in notebook_test_config_text
    assert "skip_artifact_commands = true" in notebook_test_config_text
    assert "smoke_execution_enabled = false" in notebook_test_config_text


def test_generated_notebook_11_artifacts_are_not_committed() -> None:
    if not NOTEBOOK11_ARTIFACT_DIR.exists():
        return
    committed_payloads = [
        path
        for path in NOTEBOOK11_ARTIFACT_DIR.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]
    assert committed_payloads == []
