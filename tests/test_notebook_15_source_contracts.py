"""
Static source-contract tests for Notebook 15.

Scope (M18.2):
- Parse committed Notebook 15 as source text only.
- Verify source-safe notebook shape, source-safe defaults, native portfolio
  command construction, archive/restore alignment, and conservative claim
  boundaries.
- Do not execute notebook cells, install packages, mount Drive, restore
  archives, run native strategies or portfolios, checkpoint archives, or write
  runtime artifacts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import nbformat

REPO_ROOT = Path(__file__).resolve().parents[1]
NB15_PATH = (
    REPO_ROOT / "notebooks" / "15_portfolio_workflow_review_and_case_study.ipynb"
)


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _active_lines(source: str, pattern: str) -> list[str]:
    compiled = re.compile(pattern)
    return [
        line
        for line in source.splitlines()
        if compiled.search(line) and not line.lstrip().startswith("#")
    ]


def _command_assignment(code_source: str, name: str) -> str:
    pattern = rf"{re.escape(name)}\s*=\s*\[(?P<body>.*?)\]\n"
    match = re.search(pattern, code_source, flags=re.DOTALL)
    assert match is not None, f"Expected command assignment for {name}."
    return match.group("body")


def _literal_after_flag(command_body: str, flag: str) -> str:
    pattern = rf'"{re.escape(flag)}",\s*(?P<value>[^,\n\]]+)'
    match = re.search(pattern, command_body)
    assert match is not None, f"Expected {flag} in command body."
    return match.group("value")


def _notebook() -> dict[str, Any]:
    return json.loads(NB15_PATH.read_text(encoding="utf-8"))


def _sources(notebook: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    code_cells = [
        cell
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    ]
    notebook_source = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if isinstance(cell, dict)
    )
    code_source = "\n".join("".join(cell.get("source", [])) for cell in code_cells)
    return notebook_source, code_source, code_cells


def test_notebook_15_is_valid_output_free_source_safe_notebook() -> None:
    assert NB15_PATH.exists()
    notebook = _notebook()
    nbformat.validate(nbformat.from_dict(notebook))
    notebook_source, _, code_cells = _sources(notebook)

    assert notebook.get("nbformat") == 4
    assert "Notebook 15 - Portfolio Workflow Review and Case Study" in notebook_source
    assert code_cells
    for index, cell in enumerate(code_cells):
        assert cell.get("outputs", []) == [], f"Code cell {index} has outputs."
        assert cell.get("execution_count") is None, (
            f"Code cell {index} has a committed execution count."
        )
        assert "id" not in cell
    assert "widgets" not in notebook.get("metadata", {})


def test_notebook_15_has_no_active_installs_or_runtime_overrides() -> None:
    notebook_source, code_source, _ = _sources(_notebook())
    assert _active_lines(code_source, r"^\s*!pip\s+install") == []
    assert _active_lines(notebook_source, r"os\.environ\[") == []
    assert _active_lines(code_source, r"userdata|getpass") == []
    assert 'NOTEBOOK15_PROFILE = os.environ.get("NOTEBOOK15_PROFILE", "portfolio_preview")' in code_source
    assert (
        'ALLOW_NATIVE_COMMAND_EXECUTION = os.environ.get("NOTEBOOK15_ALLOW_NATIVE_COMMAND_EXECUTION", "0").strip() == "1"'
        in code_source
    )


def test_notebook_15_uses_explicit_native_action_gates() -> None:
    _, code_source, _ = _sources(_notebook())
    for gate in [
        "NOTEBOOK15_ALLOW_FINTECH_INGESTION",
        "NOTEBOOK15_ALLOW_FINTECH_ARCHIVE_RESTORE",
        "NOTEBOOK15_ALLOW_FEATURE_GENERATION",
        "NOTEBOOK15_ALLOW_FEATURE_ARCHIVE_RESTORE",
        "NOTEBOOK15_ALLOW_STRATEGY_EXECUTION",
        "NOTEBOOK15_ALLOW_PORTFOLIO_EXECUTION",
        "NOTEBOOK15_ALLOW_PORTFOLIO_ARCHIVE_RESTORE",
        "NOTEBOOK15_ALLOW_WORKFLOW_ARCHIVE_CHECKPOINT",
        "NOTEBOOK15_ALLOW_WORKFLOW_ARCHIVE_RESTORE",
    ]:
        assert f'env_true("{gate}")' in code_source
    assert 'RUN_STRATEGIES_AFTER_RESTORE = env_true("NOTEBOOK15_RUN_STRATEGIES_AFTER_RESTORE", default=False)' in code_source
    assert 'RUN_PORTFOLIO_AFTER_RESTORE = env_true("NOTEBOOK15_RUN_PORTFOLIO_AFTER_RESTORE", default=False)' in code_source
    assert 'ARCHIVE_AFTER_PROFILE_RUN = env_true("NOTEBOOK15_ARCHIVE_AFTER_PROFILE_RUN", default=False)' in code_source


def test_notebook_15_portfolio_command_uses_required_native_surface() -> None:
    _, code_source, _ = _sources(_notebook())
    command_body = _command_assignment(code_source, "portfolio_execution_cmd")
    for token in [
        '"stratlake-run-portfolio"',
        '"--portfolio-config"',
        "PORTFOLIO_CONFIG_PATH.as_posix()",
        '"--portfolio-name"',
        "PORTFOLIO_NAME",
        '"--timeframe"',
        "PORTFOLIO_TIMEFRAME",
    ]:
        assert token in command_body
    assert "stratlake-run-research-campaign" not in code_source
    assert 'DEFAULT_NOTEBOOK15_STRATEGIES = "momentum_v1,mean_reversion_v1,buy_and_hold_v1"' in code_source
    assert "breakout" in code_source
    assert 'STRATEGY_REQUIRED_INPUT_COLUMNS = {"breakout": {"high", "low"}}' in code_source


def test_notebook_15_fintech_backup_restore_alignment_and_policy() -> None:
    _, code_source, _ = _sources(_notebook())
    restore_body = _command_assignment(code_source, "fintech_restore_cmd")
    backup_body = _command_assignment(code_source, "fintech_backup_cmd")

    assert "FINTECH_BACKUP_ROOT / FINTECH_BACKUP_ID" in code_source
    assert '"--backup-pack-dir", FINTECH_BACKUP_PACK_DIR.as_posix()' in restore_body
    assert '"--backup-root", FINTECH_BACKUP_ROOT.as_posix()' in backup_body
    assert '"--backup-id", fintech_backup_pack_id' in backup_body
    assert '"--restore-root", MARKETLAKE_ROOT.as_posix()' in restore_body
    assert '"overwrite_allowed"' not in restore_body
    assert '{"fail", "replace", "merge"}' in code_source
    assert 'FINTECH_BACKUP_COLLISION_POLICY = os.environ.get("NOTEBOOK15_FINTECH_BACKUP_COLLISION_POLICY", "reuse_existing")' in code_source
    assert "fintech_backup_validate_cmd" in code_source
    assert "fintech_backup_operation_cmd = fintech_backup_validate_cmd if fintech_backup_pack_exists and FINTECH_BACKUP_COLLISION_POLICY == \"reuse_existing\" else fintech_backup_cmd" in code_source


def test_notebook_15_stratlake_archive_restore_alignment_and_valid_flags() -> None:
    _, code_source, _ = _sources(_notebook())
    checkpoint_body = _command_assignment(code_source, "stratlake_checkpoint_cmd")
    feature_restore_body = _command_assignment(code_source, "feature_restore_cmd")
    portfolio_restore_body = _command_assignment(code_source, "portfolio_archive_restore_cmd")

    assert '"--include-market-data"' not in checkpoint_body
    for flag in ['"--include-features"', '"--include-artifacts"', '"--include-configs"']:
        assert flag in checkpoint_body
    assert '"--include-duckdb-snapshot"' in code_source
    assert '"--archive-collision-policy", STRATLAKE_ARCHIVE_COLLISION_POLICY' in checkpoint_body
    assert '"--copy-policy", STRATLAKE_ARCHIVE_COPY_POLICY' in checkpoint_body
    assert 'STRATLAKE_ARCHIVE_OUTPUT_ROOT = os.environ.get("NOTEBOOK15_STRATLAKE_ARCHIVE_OUTPUT_ROOT", "artifacts/_derived/session_archives")' in code_source
    assert _literal_after_flag(checkpoint_body, "--output-root") == "STRATLAKE_ARCHIVE_OUTPUT_ROOT"
    assert 'Path(STRATLAKE_ARCHIVE_OUTPUT_ROOT).is_absolute()' in code_source
    assert '"--archive-root", STRATLAKE_ARCHIVE_DRIVE_PACK_DIR.as_posix()' in feature_restore_body
    assert '"--archive-root", STRATLAKE_ARCHIVE_DRIVE_PACK_DIR.as_posix()' in portfolio_restore_body
    assert "STRATLAKE_ARCHIVE_DRIVE_ROOT / STRATLAKE_ARCHIVE_ID" in code_source


def test_notebook_15_has_no_real_runtime_identifiers_paths_or_secrets() -> None:
    notebook_source, _, _ = _sources(_notebook())
    for placeholder in [
        "<drive-root-placeholder>",
        "<reviewed-fintech-backup-root>",
        "<reviewed-stratlake-archive-drive-root>",
        "<reviewed-stratlake-archive-id>",
    ]:
        assert placeholder in notebook_source

    prohibited_patterns = [
        r"C:\\Users\\",
        r"Downloads",
        r"MyDrive/[A-Za-z0-9_-]+",
        r"notebook-session-\d+",
        r"manual-smoke-\d+",
        r"portfolio_[0-9a-f]{8,}",
        r"research_campaign_[0-9a-f]{8,}",
        r"\bsk-[A-Za-z0-9_-]{32,}",
        r"ghp_[A-Za-z0-9_]{20,}",
        r"Bearer\s+[A-Za-z0-9._-]{20,}",
    ]
    for pattern in prohibited_patterns:
        assert re.search(pattern, notebook_source) is None


def test_notebook_15_preserves_expected_sections_and_non_claims() -> None:
    notebook_source, _, _ = _sources(_notebook())
    normalized = _normalized(notebook_source).lower()
    for token in [
        "repository purpose",
        "workflow map",
        "ingestion",
        "session persistence",
        "feature generation",
        "validation",
        "strategy",
        "backtest",
        "portfolio workflow execution",
        "archive checkpoint and restore handoff",
        "evidence review",
        "governance",
        "promotion-evidence caveats",
        "portfolio artifact review is bounded and non-authoritative",
        "source-safe",
    ]:
        assert token in normalized
    for token in [
        "investment_recommendation",
        "strategy_approval",
        "positive_alpha",
        "promotion_readiness",
        "deployment_readiness",
        "production_readiness",
        "live_trading_suitability",
    ]:
        assert token in notebook_source
    for prohibited_claim in [
        "strategy is approved",
        "alpha is valid",
        "promotion ready",
        "production ready",
        "deployment ready",
        "live-trading suitable",
        "investment advice",
    ]:
        assert prohibited_claim not in normalized
