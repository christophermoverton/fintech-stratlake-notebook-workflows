"""
Static source-contract tests for Notebook 14.

Scope (M45.N14.3):
- Parse committed Notebook 14 and its runtime-surface classification document
  as source text only.
- Verify source-safe notebook shape, preview defaults, runtime gates,
  review-only boundaries, M45 promotion-state ownership, artifact
  classifications, and native validation failure boundaries.
- Do not execute notebook cells, install packages, mount Drive, restore
  archives, initialize sessions, call native CLIs, build review packs, run
  governance, export catalog/lineage data, checkpoint archives, or write
  runtime artifacts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NB14_PATH = (
    REPO_ROOT
    / "notebooks"
    / "14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb"
)
CLASSIFICATION_DOC = REPO_ROOT / "docs" / "notebook_14_command_surface_classification.md"

PRIMARY_PROFILES = [
    "evidence_governance_preview",
    "campaign_feature_restore_and_generation_run",
    "existing_campaign_evidence_governance_review",
]

LEGACY_PROFILES = [
    "evidence_governance_preflight",
    "archive_restore_discovery",
    "campaign_artifact_generation_run",
    "campaign_evidence_governance_run",
    "evidence_review_pack_build",
    "governance_report_run",
    "catalog_lineage_review",
    "evidence_governance_full_review",
]

RUNTIME_ACTIONS = [
    "RUN_STRATLAKE_INIT",
    "RUN_ARCHIVE_RESTORE",
    "RUN_NATIVE_CAMPAIGN_GENERATION",
    "RUN_EVIDENCE_REVIEW_PACK_BUILD",
    "RUN_EVIDENCE_REVIEW_PACK_VALIDATE",
    "RUN_PROMOTION_GOVERNANCE_REPORT",
    "RUN_CATALOG_LINEAGE_EXPORT",
    "RUN_ARCHIVE_CHECKPOINT",
    "RUN_NOTEBOOK_RUNTIME_SUMMARY_WRITE",
]


@pytest.fixture(scope="module")
def notebook() -> dict[str, Any]:
    return json.loads(NB14_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def code_cells(notebook: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        cell
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    ]


@pytest.fixture(scope="module")
def notebook_source(notebook: dict[str, Any]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )


@pytest.fixture(scope="module")
def code_source(code_cells: list[dict[str, Any]]) -> str:
    return "\n".join("".join(cell.get("source", [])) for cell in code_cells)


@pytest.fixture(scope="module")
def docs_text() -> str:
    return CLASSIFICATION_DOC.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _profile_body(code_source: str, profile_name: str) -> str:
    pattern = rf'"{re.escape(profile_name)}":\s*dict\((?P<body>.*?)\)'
    match = re.search(pattern, code_source, flags=re.DOTALL)
    assert match is not None, f"Expected profile {profile_name!r} in Notebook 14."
    return match.group("body")


def _active_lines(source: str, pattern: str) -> list[str]:
    compiled = re.compile(pattern)
    return [
        line
        for line in source.splitlines()
        if compiled.search(line) and not line.lstrip().startswith("#")
    ]


def test_notebook_14_is_valid_output_free_notebook(
    notebook: dict[str, Any],
    code_cells: list[dict[str, Any]],
    notebook_source: str,
) -> None:
    assert NB14_PATH.exists()
    assert notebook.get("nbformat") == 4
    assert notebook.get("cells")
    assert "Notebook 14" in notebook_source
    assert code_cells
    for index, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {index} has committed outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {index} has non-null execution_count."
        )
    assert "widgets" not in notebook.get("metadata", {})


def test_notebook_14_has_no_active_runtime_overrides_or_installs(
    code_source: str,
) -> None:
    assert _active_lines(code_source, r"os\.environ\[") == []
    assert _active_lines(code_source, r"^\s*!") == []
    assert _active_lines(code_source, r"userdata|getpass") == []
    assert (
        "if DRIVE_NEEDED and IN_COLAB and ALLOW_DRIVE_MOUNT "
        "and drive is not None and not is_drive_mounted():"
    ) in code_source
    assert "drive.mount(DRIVE_MOUNT_POINT.as_posix())" in code_source


def test_notebook_14_has_no_real_runtime_identifiers_or_paths(
    notebook_source: str,
) -> None:
    allowed_placeholders = [
        "<reviewed-campaign-artifact-root>",
        "<reviewed-run-id>",
        "<reviewed-archive-id>",
        "<reviewed-drive-root>",
        "<temporary-restore-run-id>",
    ]
    for placeholder in allowed_placeholders:
        assert placeholder in notebook_source

    prohibited_patterns = [
        r"C:\\Users\\",
        r"Downloads",
        r"MyDrive/stratlake-colab",
        r"momentum_v1_single_[0-9a-f]+",
        r"research_campaign_[0-9a-f]{8,}",
        r"notebook-session-\d+",
        r"manual-smoke-\d+",
        r"feature-restore-smoke-\d+",
        r"sk-[A-Za-z0-9_-]{20,}",
        r"ghp_[A-Za-z0-9_]{20,}",
    ]
    for pattern in prohibited_patterns:
        assert re.search(pattern, notebook_source) is None


def test_notebook_14_defaults_to_evidence_governance_preview(
    code_source: str,
    docs_text: str,
) -> None:
    assert (
        'NOTEBOOK14_TEST_PROFILE = os.environ.get("NOTEBOOK14_TEST_PROFILE", '
        '"evidence_governance_preview").strip() or "evidence_governance_preview"'
    ) in code_source
    assert "Committed default profile | `evidence_governance_preview`" in docs_text
    assert "sole committed default" in _normalized(docs_text).lower()


def test_notebook_14_preview_profile_is_no_write_no_execution(code_source: str) -> None:
    preview = _profile_body(code_source, "evidence_governance_preview")
    for flag in [
        "init",
        "drive",
        "restore",
        "campaign",
        "review",
        "governance",
        "lineage",
        "checkpoint",
    ]:
        assert re.search(rf"\b{flag}=False\b", preview)


@pytest.mark.parametrize("runtime_action", RUNTIME_ACTIONS)
def test_notebook_14_runtime_actions_require_explicit_profile_and_gate(
    code_source: str,
    runtime_action: str,
) -> None:
    assert runtime_action in code_source
    if runtime_action == "RUN_NOTEBOOK_RUNTIME_SUMMARY_WRITE":
        assert (
            'RUN_NOTEBOOK_RUNTIME_SUMMARY_WRITE = env_true("NOTEBOOK14_WRITE_RUNTIME_SUMMARY") '
            "and any(["
        ) in code_source
        return

    expected = {
        "RUN_STRATLAKE_INIT": 'PROFILE["init"] and ALLOW_STRATLAKE_INIT and env_true("RUN_STRATLAKE_INIT")',
        "RUN_ARCHIVE_RESTORE": 'PROFILE["restore"] and ALLOW_ARCHIVE_RESTORE and env_true("RUN_ARCHIVE_RESTORE")',
        "RUN_NATIVE_CAMPAIGN_GENERATION": 'PROFILE["campaign"] and ALLOW_NATIVE_CAMPAIGN_RUN and env_true("RUN_NATIVE_CAMPAIGN_GENERATION")',
        "RUN_EVIDENCE_REVIEW_PACK_BUILD": 'PROFILE["review"] and ALLOW_EVIDENCE_REVIEW and env_true("RUN_EVIDENCE_REVIEW_PACK_BUILD")',
        "RUN_EVIDENCE_REVIEW_PACK_VALIDATE": 'PROFILE["review"] and ALLOW_EVIDENCE_REVIEW and env_true("RUN_EVIDENCE_REVIEW_PACK_VALIDATE")',
        "RUN_PROMOTION_GOVERNANCE_REPORT": 'PROFILE["governance"] and ALLOW_GOVERNANCE_REPORT and env_true("RUN_PROMOTION_GOVERNANCE_REPORT")',
        "RUN_CATALOG_LINEAGE_EXPORT": 'PROFILE["lineage"] and ALLOW_CATALOG_LINEAGE and env_true("RUN_CATALOG_LINEAGE_EXPORT")',
        "RUN_ARCHIVE_CHECKPOINT": 'PROFILE["checkpoint"] and ALLOW_ARCHIVE_CHECKPOINT and env_true("RUN_ARCHIVE_CHECKPOINT")',
    }
    assert expected[runtime_action] in code_source


def test_notebook_14_primary_profiles_are_documented(
    code_source: str,
    docs_text: str,
) -> None:
    for profile in PRIMARY_PROFILES:
        assert f'"{profile}"' in code_source
        assert f"`{profile}`" in docs_text
    normalized = _normalized(docs_text).lower()
    assert "recommended operational profile" in normalized
    assert "first-run temporary-runtime path" in normalized
    assert "review-only temporary-runtime path" in normalized


def test_notebook_14_legacy_profiles_are_classified_not_primary(
    code_source: str,
    docs_text: str,
) -> None:
    normalized = _normalized(docs_text).lower()
    for profile in LEGACY_PROFILES:
        assert f'"{profile}"' in code_source
        assert f"`{profile}`" in docs_text
    for label in [
        "retained compatibility mode",
        "historical/reference example",
        "deprecated alias",
        "remove in later cleanup issue",
        "not recommended for new operator use",
    ]:
        assert label in normalized
    assert "not equivalent to the three recommended workflows" in normalized


def test_notebook_14_runtime_override_examples_are_inactive(
    notebook_source: str,
    docs_text: str,
) -> None:
    assert "All committed override examples remain commented and inactive." in docs_text
    for token in [
        "current source-safe template",
        "temporary runtime-only example",
        "historical retained example",
        "deprecated example",
        "do not use for new runs",
    ]:
        assert token in docs_text
    assert _active_lines(notebook_source, r'os\.environ\["NOTEBOOK14_') == []


def test_notebook_14_review_only_profile_excludes_campaign_preparation(
    code_source: str,
    docs_text: str,
) -> None:
    review = _profile_body(code_source, "existing_campaign_evidence_governance_review")
    for disabled in ["drive", "restore", "campaign", "checkpoint"]:
        assert re.search(rf"\b{disabled}=False\b", review)
    for enabled in ["init", "review", "governance", "lineage"]:
        assert re.search(rf"\b{enabled}=True\b", review)

    assert (
        'RUN_CAMPAIGN_INPUT_PREPARATION = PROFILE["campaign"] and ('
        in code_source
    )
    assert "RUN_NATIVE_CAMPAIGN_GENERATION or ALLOW_CAMPAIGN_INPUT_PREPARATION" in code_source
    assert "A review-only profile must not create those runtime artifacts" in code_source

    normalized = _normalized(docs_text).lower()
    for token in [
        "archive restore",
        "drive mount for archive restoration",
        "campaign creation",
        "execution-candidate work",
        "campaign configuration generation",
        "feature discovery/adoption",
        "campaign-preparation caveats",
        "guessed run/review identities",
    ]:
        assert token in normalized


def test_notebook_14_preserves_m45_promotion_state_ownership(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = _normalized(notebook_source + "\n" + docs_text).lower()
    for token in [
        "review promotion state is review-owned",
        "campaign promotion state is campaign-owned",
        "canonical promotion-state construction, serialization, validation, and emission are engine-owned",
        "notebook governance is observational and read-only",
        "bounded, display-oriented, non-authoritative, and non-repairing",
        "must not create, backfill, repair, normalize, or rewrite canonical",
        "must not replay policy or gate evaluation",
        "must not borrow review promotion state as campaign promotion state",
        "must not borrow campaign promotion state as review promotion state",
    ]:
        assert token in combined


def test_notebook_14_preserves_exact_no_policy_wording(
    notebook_source: str,
    docs_text: str,
) -> None:
    required = "No promotion policy was configured; no promotion decision was made."
    assert required in notebook_source
    assert required in docs_text
    combined = _normalized(notebook_source + "\n" + docs_text).lower()
    assert "not_reviewed` as eligibility, approval, promotion" in combined
    for prohibited_claim in [
        "not_reviewed is eligible",
        "not_reviewed is approved",
        "not_reviewed is promoted",
        "not_reviewed is ready",
        "not_reviewed is deployment-ready",
        "not_reviewed is production-ready",
        "not_reviewed is live-trading-ready",
        "not_reviewed is live-trading-suitable",
    ]:
        assert prohibited_claim not in combined
    assert "missing and malformed canonical evidence remain integrity observations" in combined
    assert "no notebook fallback, repair, normalization, or reinterpretation may occur" in combined


def test_notebook_14_preserves_artifact_classification_boundaries(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = notebook_source + "\n" + docs_text
    for artifact_class in [
        "canonical_engine_owned_promotion_state_candidate",
        "native_governance_output_candidate",
        "derived_evidence_review_pack_non_authoritative",
        "catalog_or_lineage_observability_artifact",
        "restored_feature_or_qa_artifact_non_governance",
        "notebook_runtime_noncanonical_excluded",
        "unknown_or_unclassified_artifact",
    ]:
        assert artifact_class in combined

    normalized = _normalized(combined).lower()
    for token in [
        "exact-filename `promotion_gates.json` inspection remains bounded, read-only",
        "`_notebook_14_runtime` are noncanonical and excluded",
        "derived review packs",
        "do not become canonical governance evidence",
        "must not be copied, moved, rewritten, normalized, repaired",
        "catalog/lineage output",
        "restored feature/qa artifacts",
    ]:
        assert token in normalized


def test_notebook_14_preserves_evidence_review_root_containment(
    code_source: str,
    docs_text: str,
) -> None:
    assert "CAMPAIGN_ARTIFACT_ROOT.parent.as_posix()" in code_source
    assert "EVIDENCE_REVIEW_REPO_ROOT" in code_source
    assert "(EVIDENCE_REVIEW_REPO_ROOT / reported_root).resolve()" in code_source
    assert "path_is_within(candidate, CAMPAIGN_ARTIFACT_ROOT)" in code_source
    normalized = _normalized(docs_text)
    assert "EVIDENCE_REVIEW_REPO_ROOT = CAMPAIGN_ARTIFACT_ROOT.parent" in normalized
    assert "under the configured campaign artifact root" in normalized


def test_notebook_14_preserves_native_command_authority_boundaries(
    notebook_source: str,
    docs_text: str,
) -> None:
    combined = _normalized(notebook_source + "\n" + docs_text).lower()
    for token in [
        "native campaign preflight and campaign execution",
        "native evidence-review pack build",
        "native strict validation",
        "native read-only governance report",
        "optional catalog/lineage observation",
        "command text",
        "executed/skipped state",
        "return code",
        "bounded stdout/stderr tails",
        "selected run/catalog/review identity",
        "effective roots",
        "display-only observation of engine-written",
        "must not become replacement validation",
        "policy interpretation",
        "artifact repair",
        "workaround for native command failures",
    ]:
        assert token in combined


def test_notebook_14_preserves_native_validation_failure_boundary(
    docs_text: str,
) -> None:
    normalized = _normalized(docs_text).lower()
    for token in [
        "native evidence-review pack build may succeed while native strict validation reports invalid schema-governed review-pack json files",
        "engine-owned package, contract-resource, validator, or version-compatibility follow-up",
        "must not copy engine contract schemas",
        "rewrite or normalize review-pack json",
        "bypass strict validation",
        "replace native validation",
        "weaken native failure results",
        "assert an unverified root cause",
        "bounded operational caveat",
    ]:
        assert token in normalized
