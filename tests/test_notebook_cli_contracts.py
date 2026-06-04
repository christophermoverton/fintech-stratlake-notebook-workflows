from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

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


def test_parser_extracts_multiline_backfill_flags():
    example = parse_shell(
        "!fintech-backfill-daily \\\n"
        "  --symbols {TICKERS_FILE_STR} \\\n"
        "  --start 2024-10-01 \\\n"
        "  --end 2025-04-15 \\\n"
        "  --out {DAILY_BARS_ROOT_STR} \\\n"
        "  --feed iex \\\n"
        "  --source session_{SESSION_ID} \\\n"
        "  --window month"
    )

    assert example.command == "fintech-backfill-daily"
    assert example.subcommand is None
    assert example.flags == {
        "--symbols",
        "--start",
        "--end",
        "--out",
        "--feed",
        "--source",
        "--window",
    }


def test_parser_extracts_restore_preview_string_flags():
    source = """
restore_command = (
    "fintech-backup-data restore "
    f"--backup-pack-dir {DRIVE_BACKUP_ROOT} "
    f"--restore-root {RESTORE_ROOT} "
    f"--overwrite-policy {OVERWRITE_POLICY}"
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
        "--backup-pack-dir",
        "--restore-root",
        "--overwrite-policy",
    }


def test_parser_ignores_comment_occurrence_when_extracting_preview_flags():
    source = """
# fintech-backup-data restore --wrong-flag
restore_command = " ".join(
    [
        "fintech-backup-data restore",
        f"--backup-pack-dir {DRIVE_BACKUP_ROOT}",
        f"--restore-root {RESTORE_ROOT}",
        f"--overwrite-policy {OVERWRITE_POLICY}",
    ]
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
    assert "--wrong-flag" not in example.flags
    assert example.flags == {
        "--backup-pack-dir",
        "--restore-root",
        "--overwrite-policy",
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


def test_validator_accepts_notebook_01_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "01_fintech_daily_bars_extraction_backfill.ipynb"],
        CONFIG,
    )

    assert report.examples
    assert any(example.command == "fintech-backfill-daily" for example in report.examples)
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings


def test_config_includes_notebook_02_target():
    targets = CONFIG["notebook_cli_contracts"]["default_targets"]

    assert "notebooks/02_fintech_session_persistence_save_restore.ipynb" in targets


def test_config_includes_notebook_03_target():
    targets = CONFIG["notebook_cli_contracts"]["default_targets"]

    assert "notebooks/03_fintech_archive_backup_pack_and_restore.ipynb" in targets


def test_config_includes_notebook_04_target():
    targets = CONFIG["notebook_cli_contracts"]["default_targets"]

    assert "notebooks/04_stratlake_feature_series_index_setup.ipynb" in targets


def test_config_includes_notebook_05_target():
    targets = CONFIG["notebook_cli_contracts"]["default_targets"]

    assert (
        "notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
        in targets
    )


def test_config_includes_stratlake_init_session_contract():
    contracts = cli_contracts.command_contracts(CONFIG)

    assert "stratlake-init-session" in contracts
    nb04_contract = contracts["stratlake-init-session"]
    required = set(nb04_contract.get("required_flags", []))
    assert "--root" in required
    assert "--project-name" in required
    assert "--marketlake-root" in required
    assert "--drive-root" in required
    assert "--enable-drive-persistence" in required
    assert "--notebook-configs" in required


def test_validator_accepts_notebook_02_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb"],
        CONFIG,
    )

    assert report.examples
    assert any(
        example.command == "fintech-init-project"
        and example.source_kind == "preview"
        and "--root" in example.flags
        and "--notebooks" in example.flags
        and "--with-session" in example.flags
        and "--session-name" in example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "restore"
        and example.is_help
        and example.source_kind == "shell"
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "restore"
        and "--backup-pack-dir" in example.flags
        and "--restore-root" in example.flags
        and "--overwrite-policy" in example.flags
        and not example.is_help
        and example.source_kind == "preview"
        for example in report.examples
    )
    assert all(example.command != "fintech-save-session" for example in report.examples)
    assert all(example.command != "fintech-restore-session" for example in report.examples)
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings


def test_validator_accepts_notebook_05_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [
            REPO_ROOT
            / "notebooks"
            / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
        ],
        CONFIG,
    )

    assert report.examples
    assert any(
        example.command == "fintech-init-project"
        and example.source_kind == "shell"
        and {"--root", "--notebooks", "--with-session", "--session-name"} <= example.flags
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-init-session"
        and example.source_kind == "shell"
        and {
            "--root",
            "--project-name",
            "--marketlake-root",
            "--drive-root",
            "--enable-drive-persistence",
            "--notebook-configs",
        }
        <= example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backfill-daily"
        and example.source_kind == "shell"
        and {"--symbols", "--start", "--end", "--out", "--feed", "--source", "--window"}
        <= example.flags
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-build-features"
        and example.source_kind == "shell"
        and {"--timeframe", "--start", "--end", "--tickers", "--marketlake-root"}
        <= example.flags
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-session-export"
        and example.source_kind == "shell"
        and {
            "--root",
            "--drive-root",
            "--include-features",
            "--include-artifacts",
            "--include-configs",
            "--dry-run",
        }
        <= example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and example.source_kind == "preview"
        and {
            "--workspace-root",
            "--source-dataset-root",
            "--backup-root",
            "--backup-id",
            "--shard-size-mb",
        }
        <= example.flags
        for example in report.examples
    )
    availability_only = {
        "fintech-save-session",
        "fintech-restore-session",
        "stratlake-session-import",
        "stratlake-session-archive-bootstrap",
        "stratlake-session-archive-restore-bootstrap",
    }
    for command in availability_only:
        assert all(example.command != command for example in report.examples)
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings


def test_validator_accepts_notebook_03_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb"],
        CONFIG,
    )

    assert report.examples
    assert any(
        example.command == "fintech-init-project"
        and "--root" in example.flags
        and "--notebooks" in example.flags
        and "--with-session" in example.flags
        and "--session-name" in example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and "--dry-run" in example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and "--dry-run" not in example.flags
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "validate"
        and example.flags == {"--backup-pack-dir"}
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "inspect"
        and example.flags == {"--backup-pack-dir"}
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "restore"
        and "--backup-pack-dir" in example.flags
        and "--restore-root" in example.flags
        and "--overwrite-policy" in example.flags
        for example in report.examples
    )
    assert all(example.command != "fintech-save-session" for example in report.examples)
    assert all(example.command != "fintech-restore-session" for example in report.examples)
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings


def test_notebook_02_dry_run_examples_are_not_executed(monkeypatch):
    executed: list[tuple[str, ...]] = []

    def fake_run(args, **_kwargs):
        executed.append(tuple(args))
        assert args[-1] == "--help"
        assert "--dry-run" not in args
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "--root --session-id --policy --adapter --destination --dry-run "
                "--notebooks --with-session --session-name "
                "--symbols --start --end --out --feed --source --window "
                "--workspace-root --source-dataset-root --backup-root --backup-id "
                "--shard-size-mb --target-dataset-root --backup-pack-dir "
                "--restore-root --overwrite-policy inspect "
                "--project-name --marketlake-root --drive-root "
                "--enable-drive-persistence --notebook-configs "
                "--timeframe --tickers --include-features --include-artifacts "
                "--include-configs"
            ),
            stderr="",
        )

    monkeypatch.setattr(cli_contracts.shutil, "which", lambda command: command)
    monkeypatch.setattr(cli_contracts.subprocess, "run", fake_run)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb"],
        CONFIG,
    )

    assert executed
    assert report.help_checks == len(cli_contracts.help_commands(CONFIG))
    assert not report.warnings
    assert not report.findings
    assert all("--dry-run" not in args for args in executed)


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


def test_validator_accepts_notebook_04_contracts_without_installed_commands(monkeypatch):
    monkeypatch.setattr(cli_contracts.shutil, "which", lambda _command: None)

    report = cli_contracts.validate_targets(
        [REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb"],
        CONFIG,
    )

    assert report.examples
    # fintech-init-project live shell is validated
    assert any(
        example.command == "fintech-init-project"
        and example.source_kind == "shell"
        and "--root" in example.flags
        and "--notebooks" in example.flags
        and "--with-session" in example.flags
        and "--session-name" in example.flags
        for example in report.examples
    )
    # stratlake-init-session live shell is validated
    assert any(
        example.command == "stratlake-init-session"
        and example.source_kind == "shell"
        and "--root" in example.flags
        and "--project-name" in example.flags
        and "--marketlake-root" in example.flags
        and "--drive-root" in example.flags
        and "--enable-drive-persistence" in example.flags
        and "--notebook-configs" in example.flags
        for example in report.examples
    )
    # fintech-backup-data pack preview is validated with registry-confirmed flags
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and example.source_kind == "preview"
        and "--workspace-root" in example.flags
        and "--source-dataset-root" in example.flags
        and "--backup-root" in example.flags
        and "--backup-id" in example.flags
        and "--shard-size-mb" in example.flags
        for example in report.examples
    )
    # fintech-backup-data restore preview is validated with registry-confirmed flags
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "restore"
        and example.source_kind == "preview"
        and "--backup-pack-dir" in example.flags
        and "--restore-root" in example.flags
        and "--overwrite-policy" in example.flags
        for example in report.examples
    )
    # availability-check-only commands are not treated as live execution
    assert all(example.command != "fintech-save-session" for example in report.examples)
    assert all(example.command != "stratlake-build-features" for example in report.examples)
    assert all(example.command != "stratlake-session-export" for example in report.examples)
    assert all(example.command != "stratlake-session-import" for example in report.examples)
    assert all(example.command != "fintech-restore-session" for example in report.examples)
    assert report.help_checks == 0
    assert report.warnings
    assert not report.findings
