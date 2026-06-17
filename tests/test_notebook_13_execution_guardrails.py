"""
Static execution-guardrail tests for Notebook 13.

These tests assert command shape, restore gates, generated config provenance,
strategy/catalog blockers, and native execution blockers from committed source
text only. They intentionally do not execute Notebook 13 or require StratLake,
Drive, Colab, credentials, network, or native CLI availability.
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


def test_archive_restore_command_shape_is_guarded_and_current(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = notebook_source + "\n" + docs_text
    for token in [
        "stratlake-session-archive-restore-bootstrap",
        "--archive-root",
        "--target-root",
        "--validate-before-restore",
        "--inspect-before-restore",
        "--overwrite-policy",
        "overwrite_allowed",
    ]:
        assert token in combined
    normalized = _normalized(docs_text)
    assert "Restore is a guarded/manual runtime surface" in normalized
    assert "must not restore archives" in normalized
    assert "Google Drive" in normalized


def test_archive_restore_requires_profile_request_and_allow_flag(code_source: str) -> None:
    assert "archive_restore_requested = bool(globals().get(\"RUN_ARCHIVE_RESTORE\", False))" in code_source
    assert (
        "archive_restore_enabled = bool(archive_restore_requested and "
        "NOTEBOOK13_ALLOW_ARCHIVE_RESTORE)"
    ) in code_source
    assert "if archive_restore_requested and not NOTEBOOK13_ALLOW_ARCHIVE_RESTORE:" in code_source
    assert "archive_restore_blockers.append(\"NOTEBOOK13_ALLOW_ARCHIVE_RESTORE is not true\")" in code_source


def test_native_campaign_command_shape_and_execution_blockers(code_source: str) -> None:
    assert 'primary_campaign_command = "stratlake-run-research-campaign"' in code_source
    assert '"--config"' in code_source
    assert "campaign_execution_requested = bool(RUN_NATIVE_CAMPAIGN_EXECUTION)" in code_source
    assert (
        "campaign_execution_enabled = bool(RUN_NATIVE_CAMPAIGN_EXECUTION and "
        "NOTEBOOK13_ALLOW_NATIVE_EXECUTION)"
    ) in code_source
    for blocker in [
        "NOTEBOOK13_ALLOW_NATIVE_EXECUTION is not true",
        "campaign preflight did not succeed",
        "native campaign command build did not succeed",
        "native execution inputs are not ready",
        "selected campaign config is notebook-generated",
        "selected universe config is notebook-generated",
    ]:
        assert blocker in code_source
    assert "campaign_execution_succeeded\": completed.returncode == 0" in code_source
    assert "campaign_execution_status\": \"succeeded\" if completed.returncode == 0 else \"failed\"" in code_source


@pytest.mark.parametrize(
    "token",
    [
        "notebook13_generated_execution_candidate_config",
        "notebook13_generated_execution_candidate_universe",
        "notebook13_generated_empty_alpha_catalog",
        "notebook-generated",
        "execution-candidate",
        "native_template: false",
        "provenance: notebook-generated",
        "config_role: execution-candidate",
        "requires_user_review_before_execution: true",
        "requires_notebook_generated_config_execution_allow: true",
        "campaign_config_is_native_template = False",
    ],
)
def test_generated_config_provenance_labels_are_preserved(
    notebook_source: str,
    docs_text: str,
    token: str,
) -> None:
    assert token in notebook_source + "\n" + docs_text


def test_generated_configs_are_not_canonical_upstream_templates(docs_text: str) -> None:
    normalized = _normalized(docs_text)
    for token in [
        "Generated configs are review candidates, not canonical upstream templates.",
        "not a canonical upstream StratLake template",
        "They are not canonical upstream StratLake templates",
        "must not be documented as such",
    ]:
        assert token in normalized


def test_generated_config_execution_requires_review_and_allow_flag(
    code_source: str,
    docs_text: str,
) -> None:
    assert "NOTEBOOK13_MARK_INPUTS_USER_REVIEWED" in code_source
    assert "NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION" in code_source
    assert (
        "campaign_config_source == \"notebook13_generated_execution_candidate_config\"\n"
        "            and campaign_config_is_user_reviewed\n"
        "            and NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION"
    ) in code_source
    assert (
        "selected campaign config is notebook-generated; set "
        "NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION=true only after reviewing"
    ) in code_source
    normalized = _normalized(docs_text)
    assert "Executing a generated campaign or universe config requires:" in normalized
    assert "NOTEBOOK13_MARK_INPUTS_USER_REVIEWED=true" in normalized
    assert "NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION=true" in normalized


def test_strategy_and_catalog_guardrails_are_source_visible(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = notebook_source + "\n" + docs_text
    for token in [
        "/content/stratlake/configs/strategies.yml",
        "/content/stratlake/configs/portfolios.yml",
        "/content/stratlake/configs/alphas.yml",
        "NOTEBOOK13_NATIVE_STRATEGY_ALIASES",
        "resolve_notebook13_execution_strategies",
        "strategy_resolution_blocked",
        "strategy_resolution_blocker",
        "strategy_resolution_caveats",
        "default_strategy_used",
        "unknown_execution_candidate_strategies",
        "Unresolved requested strategies",
        "native alpha catalog path unavailable while alpha targets are requested",
        "generated an empty alpha catalog for a strategy-only campaign",
        "strategy-only fallback",
        "catalog_readiness_blocked",
    ]:
        assert token in combined


def test_empty_alpha_catalog_fallback_is_strategy_only(code_source: str) -> None:
    resolver = _function_block(code_source, "resolve_strategy_only_alpha_catalog_path")
    assert "alpha_names" in resolver
    assert '"source": "missing_required_alpha_catalog"' in resolver
    assert "native alpha catalog path unavailable while alpha targets are requested" in resolver
    assert "notebook13_generated_empty_alpha_catalog.yml" in resolver
    assert '"source": "notebook13_generated_empty_alpha_catalog_for_strategy_only_campaign"' in resolver
    assert '"generated": True' in resolver
    assert '"strategy_only_fallback": True' in resolver
    assert '"requires_real_alpha_catalog_for_requested_alpha_targets": True' in resolver
    assert "requires_real_alpha_catalog_for_requested_alpha_targets: true" in code_source


def test_native_execution_blockers_cover_config_catalog_strategy_and_inputs(
    code_source: str,
) -> None:
    for token in [
        "campaign config execution readiness is false",
        "universe config execution readiness is false",
        "feature input root is not marked reviewed for native execution",
        "feature input root is not ready for native execution",
        "catalog, strategy, or alpha readiness blockers are present",
        "campaign_execution_result[\"execution_blockers\"] = execution_blockers",
        "catalog_readiness_blocked",
        "strategy_resolution_blocker",
        "alpha_catalog_blocker",
    ]:
        assert token in code_source


def test_native_command_discovery_records_caveats_without_requiring_cli(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = notebook_source + "\n" + docs_text
    for token in [
        "command_available",
        "help_text",
        "import surface",
        "caveats",
        "command unavailable",
        "Missing commands/modules become caveats",
        "must not require installed native CLIs",
    ]:
        assert token in combined
