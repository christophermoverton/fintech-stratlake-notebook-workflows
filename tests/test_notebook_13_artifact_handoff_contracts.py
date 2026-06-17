"""
Static artifact and handoff contract tests for Notebook 13.

These tests parse committed source text only. They verify Notebook 13 preserves
artifact provenance boundaries, handoff fields, caveat registers, and
conservative non-claims without executing notebook/runtime code.
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
def docs_text() -> str:
    return CLASSIFICATION_DOC.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _function_block(code_source: str, function_name: str) -> str:
    pattern = rf"def {re.escape(function_name)}\(.*?(?=\n\n(?:def |[A-Z_][A-Z0-9_]*\s*=|if )|\Z)"
    match = re.search(pattern, code_source, flags=re.DOTALL)
    assert match is not None, f"Expected function {function_name!r} in Notebook 13."
    return match.group(0)


@pytest.mark.parametrize(
    "token",
    [
        "native_campaign_artifact",
        "native_campaign_artifact_candidate",
        "notebook13_summary_artifact",
        "generated execution-candidate configs",
        "restored session inputs",
        "campaign_caveat_register",
        "campaign_execution_summary",
        "campaign_execution_handoff",
        "notebook13_handoff_summary",
    ],
)
def test_artifact_and_handoff_surface_names_are_preserved(
    notebook_source: str,
    docs_text: str,
    token: str,
) -> None:
    assert token in notebook_source + "\n" + docs_text


def test_artifact_origin_classifier_separates_native_summary_and_prior_review(
    code_source: str,
) -> None:
    classifier = _function_block(code_source, "classify_artifact_origin")
    for token in [
        "notebook_13_native_campaign_execution_and_artifact_generation",
        'return "native_campaign_artifact_candidate"',
        'return "notebook13_summary_artifact"',
        'return "native_campaign_governance_artifact"',
        'return "native_campaign_artifact"',
        'return "prior_notebook_review_artifact"',
        'return "candidate_campaign_context"',
    ]:
        assert token in classifier


def test_runtime_artifacts_are_documented_outside_git_and_source_validation(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = _normalized(notebook_source + "\n" + docs_text)
    combined_lower = combined.lower()
    for token in [
        "Generated runtime artifacts are written outside Git",
        "runtime outputs belong under runtime artifact roots",
        "They must stay out of Git",
        "Committed notebook source must remain output-free and execution-count-null",
    ]:
        assert token in combined
    for token in [
        "must not execute notebook cells",
        "restore archives",
        "run native campaigns",
        "write runtime artifacts",
    ]:
        assert token in combined_lower


def test_artifact_discovery_is_not_current_session_execution_proof(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = _normalized(notebook_source + "\n" + docs_text)
    for token in [
        "Artifact discovery runs even when execution is skipped",
        "while still clearly recording whether Notebook 13 executed the campaign in the current session",
        "Artifact discovery is not itself proof of current-session execution",
        "artifact discovery alone proves current-session native execution",
    ]:
        assert token in combined


def test_campaign_success_requires_native_return_code_zero(code_source: str, docs_text: str) -> None:
    assert "campaign_execution_succeeded\": completed.returncode == 0" in code_source
    assert "campaign_execution_status\": \"succeeded\" if completed.returncode == 0 else \"failed\"" in code_source
    assert "Success is claimed only when return code is 0" in docs_text
    assert "success should be\nclaimed only when the native return code is 0" in docs_text


def test_caveat_register_preserves_missing_evidence_and_nonclaim_boundaries(
    notebook_source: str,
) -> None:
    for token in [
        "Caveats are evidence-preserving",
        "campaign_caveat_register_df",
        "promotion-grade readiness is not claimed because native campaign execution did not succeed in this session",
        "native promotion governance artifacts were not detected or generated",
        "native execution input readiness is false until campaign config, universe config, and feature input root are user-reviewed",
        "promotion_boundary",
    ]:
        assert token in notebook_source


def test_handoff_summary_preserves_reviewable_artifact_and_nonclaim_fields(
    code_source: str,
) -> None:
    for token in [
        "notebook_13_native_campaign_execution_smoke_passed_with_artifacts",
        "notebook_13_campaign_execution_completed_artifacts_not_detected",
        "notebook_13_native_campaign_execution_blocked_with_caveats",
        "notebook_13_native_campaign_execution_import_ready_runtime_execution_manual",
        "campaign_execution_succeeded",
        "native_campaign_artifact_rows",
        "campaign_report_available",
        "evidence_review_available",
        "promotion_governance_available",
        "promotion_grade_claim_made\": False",
        "production_readiness_claim_made\": False",
        "statistical_significance_claim_made\": False",
    ]:
        assert token in code_source


def test_optional_governance_reporting_and_checkpoint_remain_manual_guarded(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = notebook_source + "\n" + docs_text
    for token in [
        "stratlake-build-campaign-report",
        "stratlake-build-evidence-review",
        "stratlake-run-promotion-governance-report",
        "stratlake-session-archive-bootstrap",
        "RUN_OPTIONAL_REPORT_COMMANDS",
        "RUN_OPTIONAL_GOVERNANCE_COMMANDS",
        "NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT",
            "Optional report, evidence-review, governance, and archive checkpoint surfaces",
            "remain manual and guarded",
        "must not be converted into governance-readiness claims",
    ]:
        assert token in combined


def test_conservative_nonclaim_language_is_explicit(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = _normalized(notebook_source + "\n" + docs_text)
    for token in [
        "claim strategy approval, alpha validation, statistical significance, production readiness, or promotion-grade readiness unless native governance evidence supports those claims",
        "promotion_grade_claim_made",
        "production_readiness_claim_made",
        "statistical_significance_claim_made",
        "production readiness",
        "strategy approval",
        "promotion readiness",
        "governance readiness unless native governance evidence exists",
        "statistical significance",
        "generated configs are native upstream templates",
        "runtime smoke evidence is committed notebook output",
        "CI/source validation is equivalent to Colab/manual runtime validation",
    ]:
        assert token in combined


def test_classification_doc_completion_stance_is_present(docs_text: str) -> None:
    assert "notebook_13_runtime_surfaces_classified_source_safe" in docs_text
