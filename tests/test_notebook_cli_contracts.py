from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_notebook_cli_contracts as cli_contracts  # noqa: E402

if sys.version_info < (3, 11):  # pragma: no cover - Python < 3.11
    pytest.skip("Python 3.11+ is required for TOML-based CLI contract tests.", allow_module_level=True)


CONFIG = cli_contracts.load_config(REPO_ROOT / "config" / "notebook_cli_contracts.toml")
CONTRACTS = cli_contracts.command_contracts(CONFIG)
KNOWN_COMMANDS = set(CONTRACTS)


def parse_shell(source: str):
    examples = cli_contracts.extract_shell_examples(
        Path("notebook.ipynb"),
        0,
        source,
        KNOWN_COMMANDS,
        CONTRACTS,
    )
    assert len(examples) == 1
    return examples[0]


def test_parser_extracts_fintech_save_session_flags():
    example = parse_shell(
        '!fintech-save-session --root "{LOCAL_WORKSPACE}" '
        '--session-id "{FINTECH_SESSION_NAME}" '
        "--policy artifacts_and_reports "
        "--adapter google-drive "
        '--destination "{DRIVE_SESSION_ROOT}" '
        "--dry-run"
    )

    assert example.command == "fintech-save-session"
    assert example.subcommand is None
    assert example.flags == {
        "--root",
        "--session-id",
        "--policy",
        "--adapter",
        "--destination",
        "--dry-run",
    }


def test_parser_extracts_fintech_backup_pack_subcommand_and_flags():
    example = parse_shell(
        '!fintech-backup-data pack --workspace-root "{LOCAL_WORKSPACE}" '
        '--source-dataset-root "{LOCAL_CURATED}" '
        '--backup-root "{DRIVE_BACKUP_ROOT}" '
        '--backup-id "{ARCHIVE_ID}" '
        "--shard-size-mb 512 --dry-run"
    )

    assert example.command == "fintech-backup-data"
    assert example.subcommand == "pack"
    assert "--workspace-root" in example.flags
    assert "--source-dataset-root" in example.flags
    assert "--dry-run" in example.flags


def test_parser_extracts_restore_preview_string_flags():
    source = """
restore_command = (
    "fintech-backup-data restore "
    f"--workspace-root {LOCAL_WORKSPACE} "
    f"--target-dataset-root {LOCAL_CURATED} "
    f"--backup-root {DRIVE_BACKUP_ROOT} "
    f"--backup-id {ARCHIVE_ID}"
)
"""

    examples = cli_contracts.extract_preview_examples(
        Path("notebook.ipynb"),
        0,
        source,
        KNOWN_COMMANDS,
        CONTRACTS,
    )

    assert len(examples) == 1
    example = examples[0]
    assert example.command == "fintech-backup-data"
    assert example.subcommand == "restore"
    assert example.flags == {
        "--workspace-root",
        "--target-dataset-root",
        "--backup-root",
        "--backup-id",
    }


def test_validator_accepts_notebook_00_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "00_setup_and_storage_overview.ipynb"],
        CONFIG,
    )

    assert report.examples
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings


def test_validator_rejects_missing_required_flag():
    example = cli_contracts.CommandExample(
        path=Path("notebook.ipynb"),
        cell_index=0,
        command="fintech-save-session",
        subcommand=None,
        flags={"--root", "--session-id"},
        source_kind="shell",
        is_help=False,
    )

    findings = cli_contracts.validate_example(
        example,
        cli_contracts.command_contracts(CONFIG),
        cli_contracts.subcommand_contracts(CONFIG),
    )

    assert any("--policy" in finding.reason for finding in findings)


def test_unknown_non_help_flag_fails_contract():
    example = cli_contracts.CommandExample(
        path=Path("notebook.ipynb"),
        cell_index=0,
        command="fintech-save-session",
        subcommand=None,
        flags={
            "--root",
            "--session-id",
            "--policy",
            "--adapter",
            "--destination",
            "--dry-run",
            "--surprise",
        },
        source_kind="shell",
        is_help=False,
    )

    findings = cli_contracts.validate_example(
        example,
        cli_contracts.command_contracts(CONFIG),
        cli_contracts.subcommand_contracts(CONFIG),
    )

    assert any("--surprise" in finding.reason for finding in findings)


def test_help_examples_do_not_require_workflow_flags():
    example = cli_contracts.CommandExample(
        path=Path("notebook.ipynb"),
        cell_index=0,
        command="fintech-save-session",
        subcommand=None,
        flags={"--help"},
        source_kind="shell",
        is_help=True,
    )

    findings = cli_contracts.validate_example(
        example,
        cli_contracts.command_contracts(CONFIG),
        cli_contracts.subcommand_contracts(CONFIG),
    )

    assert findings == []
