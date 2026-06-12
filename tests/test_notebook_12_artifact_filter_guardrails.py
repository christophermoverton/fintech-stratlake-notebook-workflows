"""
Static artifact-filter and campaign-context guardrail tests for Notebook 12.

Scope (M15.4):
- Parse committed notebook and classification docs source only.
- Verify native campaign artifacts, Notebook 11 review artifacts, Notebook 12
  review artifacts, strict campaign/run filters, and generated smoke config
  source classifications remain separated.
- Do not execute notebook cells, import notebook code, install packages, mount
  Drive, restore archives, run native StratLake commands, require generated
  runtime artifacts, or write review outputs.
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
def code_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    )


@pytest.fixture(scope="module")
def docs_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in [COMMAND_CLASSIFICATION_DOC, STAGING_CLASSIFICATION_DOC]
    )


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _function_block(code_source: str, function_name: str) -> str:
    pattern = rf"def {re.escape(function_name)}\(.*?(?=\n\n(?:def |if |[A-Z_]+ =)|\Z)"
    match = re.search(pattern, code_source, flags=re.DOTALL)
    assert match is not None, f"Expected function {function_name!r} in Notebook 12 source."
    return match.group(0)


def test_notebook_12_stays_output_free_and_source_safe(notebook: dict[str, Any]) -> None:
    assert set(notebook.get("metadata", {})) == {"kernelspec", "language_info"}
    for i, cell in enumerate(notebook.get("cells", [])):
        assert "id" not in cell, f"Cell {i} has a committed cell id."
        if cell.get("cell_type") == "code":
            assert cell.get("outputs", []) == [], f"Code cell {i} has committed outputs."
            assert cell.get("execution_count") is None, (
                f"Code cell {i} has non-null execution_count."
            )


def test_review_dirs_are_registered_but_classified_before_native_context(
    code_source: str,
) -> None:
    assert 'NOTEBOOK12_REVIEW_DIR = STRATLAKE_ROOT / "artifacts" / "notebook_12_campaign_evidence_gap_promotion_readiness"' in code_source
    assert 'NOTEBOOK11_REVIEW_DIR = STRATLAKE_ROOT / "artifacts" / "notebook_11_expanded_promotion_evidence_review"' in code_source
    assert "CAMPAIGN_ARTIFACT_DISCOVERY_ROOTS.append(NOTEBOOK11_REVIEW_DIR)" in code_source
    assert "CAMPAIGN_ARTIFACT_DISCOVERY_ROOTS.append(NOTEBOOK12_REVIEW_DIR)" in code_source

    origin_block = _function_block(code_source, "classify_artifact_origin")
    assert "path_is_relative_to(path, NOTEBOOK12_REVIEW_DIR)" in origin_block
    assert 'return "notebook12_review_artifact"' in origin_block
    assert "path_is_relative_to(path, NOTEBOOK11_REVIEW_DIR)" in origin_block
    assert 'return "notebook11_review_artifact"' in origin_block
    assert origin_block.index("NOTEBOOK12_REVIEW_DIR") < origin_block.index(
        'return "native_campaign_artifact"'
    )
    assert origin_block.index("NOTEBOOK11_REVIEW_DIR") < origin_block.index(
        'return "native_campaign_artifact"'
    )


def test_native_campaign_markers_require_native_artifact_origin(code_source: str) -> None:
    marker_block = _function_block(code_source, "is_native_campaign_marker")
    assert 'if artifact_origin != "native_campaign_artifact":' in marker_block
    assert "return False" in marker_block.split('if artifact_origin != "native_campaign_artifact":', 1)[1]
    assert "artifact_name in NATIVE_CAMPAIGN_MARKER_NAMES" in marker_block
    assert "artifact_has_native_identifier(path)" in marker_block


@pytest.mark.parametrize(
    "marker_name",
    [
        "campaign_manifest.json",
        "campaign_manifest.csv",
        "campaign_run_registry.json",
        "campaign_run_registry.csv",
        "campaign_summary.json",
        "campaign_summary.csv",
        "research_campaign_summary.json",
        "research_campaign_registry.csv",
    ],
)
def test_native_campaign_marker_names_include_registry_manifest_and_summary(
    code_source: str,
    marker_name: str,
) -> None:
    marker_set_block = code_source.split("NATIVE_CAMPAIGN_MARKER_NAMES = {", 1)[1]
    marker_set_block = marker_set_block.split("}", 1)[0]
    assert f'"{marker_name}"' in marker_set_block


@pytest.mark.parametrize(
    "review_name",
    [
        "campaign_artifact_inventory.csv",
        "campaign_evidence_review.csv",
        "summary.json",
        "final_handoff.json",
        "caveat_register.csv",
        "candidate_campaign_context_inventory.csv",
        "native_campaign_smoke_result.json",
    ],
)
def test_notebook12_generated_review_names_are_explicit(code_source: str, review_name: str) -> None:
    generated_set_block = code_source.split("NOTEBOOK12_GENERATED_REVIEW_NAMES = {", 1)[1]
    generated_set_block = generated_set_block.split("}", 1)[0]
    assert f'"{review_name}"' in generated_set_block


@pytest.mark.parametrize(
    "origin",
    [
        "native_campaign_artifact",
        "notebook12_review_artifact",
        "notebook11_review_artifact",
    ],
)
def test_artifact_origin_values_are_preserved(notebook_source: str, origin: str) -> None:
    assert origin in notebook_source


def test_notebook_review_artifacts_are_marked_non_native_and_generated(
    code_source: str,
) -> None:
    assert (
        '"notebook_generated_review_artifact": artifact_origin in '
        '{"notebook12_review_artifact", "notebook11_review_artifact"}'
    ) in code_source
    assert '"native_campaign_marker": native_marker' in code_source
    assert 'if artifact_origin != "native_campaign_artifact":\n        return False' in code_source
    assert "native_campaign_marker" in code_source
    assert "notebook_generated_review_artifact" in code_source


def test_inventory_dataframes_remain_distinct_and_native_only_for_downstream_loading(
    code_source: str,
) -> None:
    assert "campaign_artifact_inventory_all_df = discover_campaign_artifacts(CAMPAIGN_ARTIFACT_DISCOVERY_ROOTS)" in code_source
    assert "native_campaign_artifact_inventory_df = campaign_artifact_inventory_all_df.loc[" in code_source
    assert '.eq("native_campaign_artifact")' in code_source
    assert "notebook12_review_artifact_inventory_df = campaign_artifact_inventory_all_df.loc[" in code_source
    assert '.eq("notebook12_review_artifact")' in code_source
    assert "campaign_artifact_inventory_df = native_campaign_artifact_inventory_df.copy()" in code_source
    assert "candidate_campaign_context_df = build_campaign_context_candidates(campaign_artifact_inventory_all_df)" in code_source


def test_candidate_campaign_context_is_built_only_from_native_campaign_artifacts(
    code_source: str,
) -> None:
    candidate_block = _function_block(code_source, "build_campaign_context_candidates")
    assert "# Only native campaign artifacts can create candidate campaign context." in candidate_block
    assert (
        'native_df = inventory_df.loc[inventory_df.get("artifact_origin", '
        'pd.Series(dtype=str)).eq("native_campaign_artifact")].copy()'
    ) in candidate_block
    assert "if native_df.empty:" in candidate_block
    assert "return pd.DataFrame(columns=columns)" in candidate_block
    assert 'coherence_status = "candidate_context_missing_native_campaign_marker"' in candidate_block
    assert 'coherence_status = "candidate_context_sparse"' in candidate_block
    assert 'coherence_status = "candidate_context_reviewable"' in candidate_block


@pytest.mark.parametrize(
    "filter_token",
    [
        "RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY",
        "CAMPAIGN_ID_FILTER",
        "RUN_ID_FILTER",
        "REQUIRE_CAMPAIGN_OR_RUN_FILTER_FOR_RESTORED_REVIEW",
        "path_matches_strict_filters(path, CAMPAIGN_ID_FILTER, RUN_ID_FILTER)",
        "if RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY and (CAMPAIGN_ID_FILTER or RUN_ID_FILTER) and not strict_match:",
    ],
)
def test_strict_campaign_and_run_filters_remain_present(
    notebook_source: str,
    filter_token: str,
) -> None:
    assert filter_token in notebook_source


def test_missing_or_sparse_campaign_context_remains_caveated(
    notebook_source: str,
) -> None:
    for token in [
        "campaign_context_missing",
        "candidate_context_missing_native_campaign_marker",
        "candidate_context_sparse",
        "notebook_12_strict_discovery_blocked_missing_filter",
        "cold_smoke_4_strict_missing_filter_guardrail",
        "missing_campaign_context",
        "Excluded {len(notebook12_review_artifact_inventory_df)} Notebook 12-generated review artifact(s) from native campaign context.",
    ]:
        assert token in notebook_source
    assert "Missing campaign context or missing promotion evidence should be documented as caveats" in _normalized(
        notebook_source + "\n" + COMMAND_CLASSIFICATION_DOC.read_text(encoding="utf-8")
    )


def test_generated_smoke_configs_and_native_templates_are_separately_classified(
    code_source: str,
) -> None:
    smoke_source_block = _function_block(code_source, "smoke_config_source_for_path")
    assert '"config_source": "notebook12_generated_smoke_config" if is_notebook_generated else "native_campaign_template"' in smoke_source_block
    assert '"config_is_native_template": not is_notebook_generated' in smoke_source_block
    assert '"config_is_notebook_generated": is_notebook_generated' in smoke_source_block
    assert 'selected_campaign_smoke_config_source = "native_campaign_template"' in code_source
    assert "selected_campaign_smoke_config_is_native_template = True" in code_source
    assert "selected_campaign_smoke_config_is_notebook_generated = False" in code_source
    assert 'selected_campaign_smoke_config_source = "notebook12_generated_smoke_config"' in code_source
    assert "selected_campaign_smoke_config_is_native_template = False" in code_source
    assert "selected_campaign_smoke_config_is_notebook_generated = True" in code_source


@pytest.mark.parametrize(
    "field",
    [
        "config_source",
        "config_is_native_template",
        "config_is_notebook_generated",
        "native_campaign_smoke_config_source",
        "native_campaign_smoke_config_is_native_template",
        "native_campaign_smoke_config_is_notebook_generated",
    ],
)
def test_smoke_config_source_fields_are_preserved(notebook_source: str, field: str) -> None:
    assert field in notebook_source


def test_classification_docs_preserve_artifact_filter_boundaries(docs_text: str) -> None:
    normalized_docs_text = _normalized(docs_text)
    for token in [
        "Notebook 12 must not fabricate campaign context from its own review artifacts",
        "Generated smoke configs are useful for preview and explicitly guarded smoke tests, but their source remains `notebook12_generated_smoke_config`, not a native campaign template.",
        "Native campaign artifacts remain distinct from Notebook 12 review artifacts.",
        "`native_campaign_artifact_rows`, `notebook12_review_artifact_rows`, and `candidate_campaign_context_rows` should not be collapsed into a fabricated campaign context.",
        "Missing campaign context, missing split metrics, missing promotion gates, or missing promotion evidence are caveats and blockers.",
    ]:
        assert token in normalized_docs_text


@pytest.mark.parametrize(
    "forbidden_pattern",
    [
        r"\bapproved for promotion\b",
        r"\bstrategy approved\b",
        r"\balpha (?:validated|confirmed|ready)\b",
        r"\bproduction[- ]ready\b",
        r"\bstatistically significant\b",
        r"\bpromotion-grade readiness achieved\b",
    ],
)
def test_guardrail_coverage_introduces_no_positive_readiness_claims(
    notebook_source: str,
    docs_text: str,
    forbidden_pattern: str,
) -> None:
    assert re.search(forbidden_pattern, notebook_source + "\n" + docs_text, flags=re.IGNORECASE) is None
