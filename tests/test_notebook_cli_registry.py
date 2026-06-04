from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_notebook_cli_registry as cli_registry  # noqa: E402

if sys.version_info < (3, 11):  # pragma: no cover - Python < 3.11
    pytest.skip(
        "Python 3.11+ is required for TOML-based CLI registry tests.",
        allow_module_level=True,
    )


CONFIG_PATH = REPO_ROOT / "config" / "notebook_cli_registry.toml"
CONFIG = cli_registry.load_toml(CONFIG_PATH)
SETTINGS = dict(CONFIG["notebook_cli_registry"])
REGISTRY_PATH = cli_registry.resolve_registry_path(CONFIG_PATH, SETTINGS)
REGISTRY = cli_registry.load_toml(REGISTRY_PATH)
MODEL = cli_registry.build_registry_model(REGISTRY)


def deep_contains_key(value: Any, target_key: str) -> bool:
    if isinstance(value, dict):
        if target_key in value:
            return True
        return any(deep_contains_key(item, target_key) for item in value.values())
    if isinstance(value, list):
        return any(deep_contains_key(item, target_key) for item in value)
    return False


def write_synthetic_notebook(tmp_path: Path, commands: list[str]) -> Path:
    cells = [
        {
            "cell_type": "code",
            "metadata": {},
            "source": [f"!{command}\n"],
            "outputs": [],
            "execution_count": None,
        }
        for command in commands
    ]
    notebook = {
        "cells": cells,
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = tmp_path / "synthetic.ipynb"
    path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    return path


def parse_example(command_text: str):
    parts = cli_registry.split_command(command_text)
    example = cli_registry.parse_parts(
        Path("synthetic.ipynb"),
        0,
        parts,
        "shell",
        MODEL,
    )
    assert example is not None
    return example


def validate_command_text(command_text: str, *, settings: dict[str, Any] | None = None):
    active_settings = dict(SETTINGS)
    if settings:
        active_settings.update(settings)
    return cli_registry.validate_example(parse_example(command_text), MODEL, active_settings)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()



def test_registry_toml_files_parse_successfully():
    command_registry = cli_registry.load_toml(REPO_ROOT / "config" / "cli_command_registry.toml")
    notebook_registry = cli_registry.load_toml(REPO_ROOT / "config" / "notebook_cli_registry.toml")

    assert "commands" in command_registry
    assert "notebook_cli_registry" in notebook_registry


def test_build_registry_model_contains_expected_commands_and_subcommands():
    assert isinstance(MODEL, cli_registry.RegistryModel)

    assert "fintech-init-project" in MODEL.commands
    assert "fintech-backfill-daily" in MODEL.commands
    assert "fintech-save-session" in MODEL.commands
    assert "fintech-backup-data" in MODEL.commands
    assert "stratlake-init-session" in MODEL.commands
    assert "stratlake-build-features" in MODEL.commands
    assert "stratlake-session-export" in MODEL.commands

    backup_entry = MODEL.commands["fintech-backup-data"]
    assert backup_entry.subcommands == ("pack", "validate", "inspect", "restore")
    assert ("fintech-backup-data", "pack") in MODEL.subcommands
    assert ("fintech-backup-data", "validate") in MODEL.subcommands
    assert ("fintech-backup-data", "inspect") in MODEL.subcommands
    assert ("fintech-backup-data", "restore") in MODEL.subcommands

    stratlake_entry = MODEL.commands["stratlake-init-session"]
    assert stratlake_entry.subcommands == ()
    assert "--root" in stratlake_entry.flags
    assert "--project-name" in stratlake_entry.flags
    assert "--marketlake-root" in stratlake_entry.flags
    assert "--drive-root" in stratlake_entry.flags
    assert "--enable-drive-persistence" in stratlake_entry.flags
    assert "--notebook-configs" in stratlake_entry.flags
    assert stratlake_entry.flags["--enable-drive-persistence"].kind == "boolean"
    assert stratlake_entry.flags["--notebook-configs"].kind == "boolean"
    assert stratlake_entry.flags["--marketlake-root"].notebook_contract_required is True


def test_registry_exclusions_and_stratlake_init_session_promoted():
    assert "fintech-restore-session" in MODEL.excluded
    assert "fintech-restore-session" not in MODEL.commands

    # stratlake-trade-engine commands placeholder still exists as excluded grouping
    assert "stratlake-trade-engine commands" in MODEL.excluded

    # stratlake-init-session is promoted to live NB04 scope (M7.3)
    assert "stratlake-init-session" in MODEL.commands
    assert "stratlake-init-session" not in MODEL.excluded

    # Notebook 05 promotes feature build and dry-run export; other StratLake commands remain deferred.
    assert "stratlake-build-features" in MODEL.commands
    assert "stratlake-session-export" in MODEL.commands

    excluded_stratlake = [
        "stratlake-session-import",
        "stratlake-session-archive-bootstrap",
        "stratlake-session-archive-restore-bootstrap",
    ]
    for command in excluded_stratlake:
        assert command not in MODEL.commands, f"{command} should not be in registry commands"


def test_required_flag_schema_and_restore_semantics():
    assert not deep_contains_key(REGISTRY, "required")

    for entry in REGISTRY.get("commands", []):
        for _flag_name, flag_data in entry.get("flags", {}).items():
            assert "argparse_required" in flag_data or "notebook_contract_required" in flag_data
    for entry in REGISTRY.get("command_subcommands", []):
        for _flag_name, flag_data in entry.get("flags", {}).items():
            assert "argparse_required" in flag_data or "notebook_contract_required" in flag_data

    restore_entry = MODEL.subcommands[("fintech-backup-data", "restore")]
    assert restore_entry.flags["--backup-pack-dir"].argparse_required is True
    assert restore_entry.flags["--restore-root"].argparse_required is True

    overwrite = restore_entry.flags["--overwrite-policy"]
    assert overwrite.argparse_required is False
    assert overwrite.allowed_values == ("fail", "replace", "merge")

    subcommands_raw = REGISTRY.get("command_subcommands", [])
    restore_raw = next(
        entry
        for entry in subcommands_raw
        if entry.get("command") == "fintech-backup-data" and entry.get("subcommand") == "restore"
    )
    assert restore_raw["flags"]["--overwrite-policy"]["default_value"] == "fail"

    init_entry = MODEL.commands["fintech-init-project"]
    assert init_entry.flags["--notebooks"].kind == "boolean"
    assert init_entry.flags["--notebooks"].argparse_required is False
    assert init_entry.flags["--with-session"].kind == "boolean"
    assert init_entry.flags["--with-session"].argparse_required is False

    backfill_entry = MODEL.commands["fintech-backfill-daily"]
    assert backfill_entry.flags["--start"].argparse_required is True
    assert backfill_entry.flags["--end"].argparse_required is True

    save_entry = MODEL.commands["fintech-save-session"]
    assert save_entry.flags["--session-id"].argparse_required is True
    assert save_entry.flags["--destination"].required_when == "not_dry_run"

    pack_entry = MODEL.subcommands[("fintech-backup-data", "pack")]
    assert pack_entry.flags["--dry-run"].argparse_required is False
    assert pack_entry.flags["--dry-run"].notebook_contract_required is False


@pytest.mark.parametrize(
    "command_text",
    [
        "fintech-init-project --root /content/fintech-market-ingestion-demo --notebooks --with-session --session-name extraction_daily_bars_demo",
        "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy fail",
        "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy replace",
        "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy merge",
        'fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy "fail"',
        "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy 'replace'",
        'fintech-backup-data restore --backup-pack-dir=/drive/pack --restore-root=/tmp/data --overwrite-policy="merge"',
        "fintech-backup-data restore --backup-pack-dir=/drive/pack --restore-root=/tmp/data --overwrite-policy=fail",
        "fintech-backup-data validate --backup-pack-dir /drive/pack",
        "fintech-backup-data validate --backup-pack-dir /drive/pack --raise-on-error",
        "fintech-backup-data inspect --backup-pack-dir /drive/pack",
        "fintech-backup-data restore --help",
        "fintech-backup-data validate --help",
        "fintech-backup-data inspect --help",
        "fintech-backup-data pack --workspace-root /content/demo --source-dataset-root /content/demo/data/curated --backup-root /drive/backups --backup-id archive-1 --shard-size-mb 512",
        "fintech-backup-data pack --workspace-root /content/demo --source-dataset-root /content/demo/data/curated --backup-root /drive/backups --backup-id archive-1 --shard-size-mb 512 --dry-run",
        "stratlake-build-features --timeframe 1D --start 2025-01-01 --end 2025-04-01 --tickers /content/tickers.txt --marketlake-root /content/fintech/data/curated",
        "stratlake-session-export --root /content/stratlake --drive-root /content/drive/MyDrive/demo --include-features --include-artifacts --include-configs --dry-run",
    ],
)
def test_validator_accepts_valid_command_examples(command_text):
    _example, findings, _warnings = validate_command_text(command_text)
    assert findings == []


@pytest.mark.parametrize(
    ("command_text", "expected_snippet"),
    [
        (
            'fintech-init-project --root /tmp/demo --notebooks "" --with-session --session-name demo',
            "boolean flag",
        ),
        (
            'fintech-init-project --root /tmp/demo --notebooks --with-session "" --session-name demo',
            "boolean flag",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy refuse",
            "invalid value",
        ),
        (
            'fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --overwrite-policy "refuse"',
            "invalid value",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir=/drive/pack --restore-root=/tmp/data --overwrite-policy=refuse",
            "invalid value",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir=/drive/pack --restore-root=/tmp/data --overwrite-policy='refuse'",
            "invalid value",
        ),
        (
            "fintech-backup-data restore --source /drive/pack --restore-root /tmp/data --overwrite-policy fail",
            "unsupported flag",
        ),
        (
            "fintech-backup-data restore --restore-root /tmp/data --overwrite-policy fail",
            "missing argparse-required flag",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir /drive/pack --overwrite-policy fail",
            "missing argparse-required flag",
        ),
        (
            "fintech-restore-session --root /tmp/demo --adapter google-drive --source /drive/session --overwrite-policy fail",
            "excluded from valid current notebook syntax",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir /drive/pack --restore-root /tmp/data --unknown-flag value",
            "unknown flag",
        ),
        (
            "fintech-backup-data restore --backup-pack-dir --restore-root /tmp/data --overwrite-policy fail",
            "value flag",
        ),
    ],
)
def test_validator_rejects_invalid_command_examples(command_text, expected_snippet):
    _example, findings, _warnings = validate_command_text(command_text)
    assert findings
    assert any(expected_snippet in finding.reason for finding in findings)


def test_boolean_flag_value_policy_can_be_disabled():
    _example, findings, _warnings = validate_command_text(
        'fintech-init-project --root /tmp/demo --notebooks "" --with-session --session-name demo',
        settings={"fail_on_boolean_flag_value": False},
    )
    assert findings
    assert not any("boolean flag" in finding.reason for finding in findings)


def test_split_command_preserves_windows_style_backslashes():
    parts = cli_registry.split_command(
        r"fintech-init-project --root C:\tmp\demo --notebooks --with-session --session-name demo"
    )
    assert parts[2] == r"C:\tmp\demo"


def test_help_examples_are_safe_help_and_skip_normal_required_flags():
    for command_text in [
        "fintech-backup-data restore --help",
        "fintech-backup-data validate --help",
        "fintech-backup-data inspect --help",
    ]:
        example, findings, _warnings = validate_command_text(command_text)
        assert findings == []
        assert example.classification == "safe_help"


def test_help_requires_known_command_or_subcommand():
    _example, findings, _warnings = validate_command_text(
        "fintech-backup-data unknown-subcommand --help"
    )
    assert findings
    assert any("unknown subcommand" in finding.reason for finding in findings)


def test_unknown_watched_command_warn_policy(tmp_path):
    notebook = write_synthetic_notebook(tmp_path, ["fintech-unlisted-command --help"])
    report = cli_registry.validate_targets([notebook], MODEL, dict(SETTINGS, unknown_command_policy="warn"))

    assert not report.findings
    assert any("unknown command: fintech-unlisted-command" in warning for warning in report.warnings)


def test_unknown_watched_command_fail_policy(tmp_path):
    notebook = write_synthetic_notebook(tmp_path, ["fintech-unlisted-command --help"])
    report = cli_registry.validate_targets([notebook], MODEL, dict(SETTINGS, unknown_command_policy="fail"))

    assert report.findings
    assert any("unknown command: fintech-unlisted-command" in finding.reason for finding in report.findings)


def test_ignored_setup_commands_do_not_fail_registry_validation(tmp_path):
    notebook = write_synthetic_notebook(
        tmp_path,
        [
            "pip install -q notebook",
            "python -m pip install -q notebook",
        ],
    )
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    payload["cells"].append(
        {
            "cell_type": "code",
            "metadata": {},
            "source": ["%pip install -q notebook\n"],
            "outputs": [],
            "execution_count": None,
        }
    )
    notebook.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    report = cli_registry.validate_targets([notebook], MODEL, SETTINGS)

    assert report.examples == []
    assert report.findings == []


def test_excluded_command_reports_unsupported_pattern():
    _example, findings, _warnings = validate_command_text(
        "fintech-restore-session --overwrite-policy fail"
    )

    assert findings
    assert any("excluded from valid current notebook syntax" in finding.reason for finding in findings)
    assert any("unsupported excluded-command pattern" in finding.reason for finding in findings)


def test_excluded_stratlake_placeholder_does_not_make_concrete_command_valid(tmp_path):
    notebook = write_synthetic_notebook(tmp_path, ["stratlake-train --help"])
    report = cli_registry.validate_targets([notebook], MODEL, dict(SETTINGS, unknown_command_policy="fail"))

    assert report.findings
    assert any("unknown command: stratlake-train" in finding.reason for finding in report.findings)


@pytest.mark.parametrize(
    "target",
    [
        REPO_ROOT / "notebooks" / "00_setup_and_storage_overview.ipynb",
        REPO_ROOT / "notebooks" / "01_fintech_daily_bars_extraction_backfill.ipynb",
        REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb",
        REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb",
        REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb",
        REPO_ROOT / "notebooks" / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb",
    ],
    ids=lambda path: path.name,
)
def test_current_notebooks_pass_registry_validation(target):
    report = cli_registry.validate_targets([target], MODEL, SETTINGS)

    assert report.examples
    assert not report.findings


def test_notebook_02_passes_with_zero_registry_failures():
    target = REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb"
    report = cli_registry.validate_targets([target], MODEL, SETTINGS)

    assert not report.findings


def test_notebook_03_passes_with_zero_registry_failures():
    target = REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb"
    report = cli_registry.validate_targets([target], MODEL, SETTINGS)

    assert report.examples
    assert not report.findings
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and example.classification == "dry_run"
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "pack"
        and "--dry-run" not in example.flag_names()
        and example.classification == "manual_only_live"
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backup-data"
        and example.subcommand == "restore"
        and {"--backup-pack-dir", "--restore-root", "--overwrite-policy"} <= example.flag_names()
        for example in report.examples
    )
    assert all(example.command != "fintech-save-session" for example in report.examples)
    assert all(example.command != "fintech-restore-session" for example in report.examples)


def test_notebook_04_passes_with_zero_registry_failures():
    target = REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb"
    report = cli_registry.validate_targets([target], MODEL, SETTINGS)

    assert report.examples
    assert not report.findings
    # fintech-init-project live shell is classified manual_only_live
    assert any(
        example.command == "fintech-init-project"
        and example.source_kind == "shell"
        and example.classification == "manual_only_live"
        and {"--root", "--notebooks", "--with-session", "--session-name"} <= example.flag_names()
        for example in report.examples
    )
    # stratlake-init-session live shell is classified manual_only_live
    assert any(
        example.command == "stratlake-init-session"
        and example.source_kind == "shell"
        and example.classification == "manual_only_live"
        and {"--root", "--project-name", "--marketlake-root", "--drive-root"} <= example.flag_names()
        and "--enable-drive-persistence" in example.flag_names()
        and "--notebook-configs" in example.flag_names()
        for example in report.examples
    )
    # availability-check-only commands are not treated as live NB04 commands
    availability_only = {
        "fintech-save-session",
        "stratlake-session-import",
        "stratlake-session-archive-bootstrap",
        "stratlake-session-archive-restore-bootstrap",
    }
    for command in availability_only:
        assert all(example.command != command for example in report.examples), (
            f"{command} should not appear as a live registry example in NB04"
        )
    # fintech-restore-session is not present
    assert all(example.command != "fintech-restore-session" for example in report.examples)


def test_config_includes_notebook_04_registry_target():
    targets = SETTINGS.get("default_targets", [])

    assert "notebooks/04_stratlake_feature_series_index_setup.ipynb" in targets


def test_config_includes_notebook_05_registry_target():
    targets = SETTINGS.get("default_targets", [])

    assert (
        "notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
        in targets
    )


def test_notebook_05_passes_with_zero_registry_failures():
    target = (
        REPO_ROOT
        / "notebooks"
        / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    )
    report = cli_registry.validate_targets([target], MODEL, SETTINGS)

    assert report.examples
    assert not report.findings
    assert any(
        example.command == "fintech-init-project"
        and example.classification == "manual_only_live"
        and {"--root", "--notebooks", "--with-session", "--session-name"} <= example.flag_names()
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-init-session"
        and example.classification == "manual_only_live"
        and {"--root", "--project-name", "--marketlake-root", "--drive-root"}
        <= example.flag_names()
        and "--enable-drive-persistence" in example.flag_names()
        and "--notebook-configs" in example.flag_names()
        for example in report.examples
    )
    assert any(
        example.command == "fintech-backfill-daily"
        and example.classification == "unsafe_live"
        and {"--symbols", "--start", "--end", "--out", "--feed", "--source", "--window"}
        <= example.flag_names()
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-build-features"
        and example.classification == "unsafe_live"
        and {"--timeframe", "--start", "--end", "--tickers", "--marketlake-root"}
        <= example.flag_names()
        for example in report.examples
    )
    assert any(
        example.command == "stratlake-session-export"
        and example.classification == "dry_run"
        and {
            "--root",
            "--drive-root",
            "--include-features",
            "--include-artifacts",
            "--include-configs",
            "--dry-run",
        }
        <= example.flag_names()
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


def test_notebook_05_command_source_values_are_pinned():
    target = (
        REPO_ROOT
        / "notebooks"
        / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    )
    source = target.read_text(encoding="utf-8")

    assert "--start 2025-01-01" in source
    assert "--end 2025-04-01" in source
    assert "--feed iex" in source
    assert "--source session_{FINTECH_SESSION_ID}" in source
    assert "--window month" in source
    assert "--timeframe 1D" in source
    assert "--marketlake-root {MARKETLAKE_ROOT_STR}" in source
    assert "!stratlake-session-export" in source
    assert "--dry-run" in source
    assert "FINTECH_SESSION_ID" in source
    assert "STRATLAKE_SESSION_ID" in source
    assert "MARKETLAKE_ROOT" in source


def test_registry_validation_does_not_mutate_source_notebooks():
    targets = [
        REPO_ROOT / "notebooks" / "00_setup_and_storage_overview.ipynb",
        REPO_ROOT / "notebooks" / "01_fintech_daily_bars_extraction_backfill.ipynb",
        REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb",
        REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb",
        REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb",
        REPO_ROOT / "notebooks" / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb",
    ]
    before = {path: file_digest(path) for path in targets}

    report = cli_registry.validate_targets(targets, MODEL, SETTINGS)

    assert report.targets_checked == 6
    after = {path: file_digest(path) for path in targets}
    assert before == after


def test_validate_notebook_cli_registry_subprocess_smoke_all_targets():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_notebook_cli_registry.py"),
            "--config",
            str(REPO_ROOT / "config" / "notebook_cli_registry.toml"),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_notebook_cli_registry_subprocess_smoke_notebook_02_only():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_notebook_cli_registry.py"),
            "notebooks/02_fintech_session_persistence_save_restore.ipynb",
            "--config",
            str(REPO_ROOT / "config" / "notebook_cli_registry.toml"),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_notebook_cli_registry_subprocess_smoke_notebook_05_only():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_notebook_cli_registry.py"),
            "notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb",
            "--config",
            str(REPO_ROOT / "config" / "notebook_cli_registry.toml"),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
