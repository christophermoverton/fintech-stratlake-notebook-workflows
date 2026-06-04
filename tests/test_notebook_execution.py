from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

if sys.version_info < (3, 11):  # pragma: no cover - Python < 3.11
    pytest.skip(
        "Python 3.11+ is required for TOML-based notebook execution tests.",
        allow_module_level=True,
    )

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[1]
EXECUTION_CONFIG = REPO_ROOT / "config" / "notebook_execution_test.toml"
READINESS_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_toml(path: Path) -> dict:
    if tomllib is None:
        raise AssertionError("Python 3.11 or newer is required for TOML parsing.")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def notebook_code_cells(nb) -> list:
    return [cell for cell in nb.cells if cell.get("cell_type") == "code"]


def cell_source(cell) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def assert_source_notebook_clean(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    for index, cell in enumerate(notebook_code_cells(nb)):
        assert cell.get("outputs", []) == [], f"cell {index} has outputs"
        assert cell.get("execution_count") is None, f"cell {index} has execution_count"


def configured_notebook_targets(config_path: Path, section: str) -> list[Path]:
    config = load_toml(config_path)
    return [REPO_ROOT / target for target in config[section]["default_targets"]]


def should_skip_cell(source: str, config: dict) -> bool:
    if any(line.lstrip().startswith(("!", "%")) for line in source.splitlines()):
        return True
    if ".mkdir" in source:
        return True
    if "RESTORE_ROOT" in source:
        return True
    patterns = config["skip_patterns"]["cell_source_contains"]
    return any(pattern in source for pattern in patterns)


def safe_prefix_lines(source: str) -> list[str]:
    if ".mkdir" in source:
        return []
    if any(
        pattern in source
        for pattern in (
            "!fintech-",
            "fintech-restore-session",
            "fintech-backup-data restore",
            "DRIVE_PROJECT_ROOT",
            "DRIVE_SESSION_ROOT",
            "DRIVE_BACKUP_ROOT",
            "BACKUP_PACK_DIR",
            "RESTORE_BACKUP_ROOT",
            "PREVIOUS_BACKUP_PACK_DIR",
            "FINTECH_ROOT",
            "RESTORE_ROOT",
            "STRATLAKE_ROOT",
            "MARKETLAKE_ROOT",
        )
    ):
        return []

    safe_lines: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("!", "%")):
            break
        if "import " in stripped or "from " in stripped:
            break
        if re.match(r"^[A-Z_][A-Z0-9_]*\s*=", stripped) and not any(
            token in line for token in ("os.environ", "userdata", "getpass")
        ):
            safe_lines.append(line)
            continue
        if stripped == "":
            safe_lines.append(line)
            continue
        break
    return safe_lines


def sanitized_code_cell(source: str):
    prefix = safe_prefix_lines(source)
    if prefix:
        cleaned_source = "\n".join(prefix).strip() + "\n"
    else:
        cleaned_source = "# Skipped by pytest sanitized notebook execution harness.\n"
    return nbformat.v4.new_code_cell(source=cleaned_source)


def build_sanitized_notebook(source_path: Path, config: dict):
    source_nb = nbformat.read(source_path, as_version=4)
    sanitized = nbformat.v4.new_notebook()
    sanitized.metadata = {
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    }

    skipped = 0
    kept_code = 0
    for cell in source_nb.cells:
        if cell.get("cell_type") == "markdown":
            sanitized.cells.append(nbformat.v4.new_markdown_cell(source=cell.get("source", "")))
            continue
        if cell.get("cell_type") != "code":
            continue

        source = cell_source(cell)
        if should_skip_cell(source, config):
            sanitized.cells.append(sanitized_code_cell(source))
            skipped += 1
        else:
            sanitized.cells.append(nbformat.v4.new_code_cell(source=source))
            kept_code += 1

    return sanitized, skipped, kept_code


def sanitized_code_sources(nb) -> list[str]:
    return [cell_source(cell) for cell in notebook_code_cells(nb)]


@pytest.mark.parametrize(
    "source_notebook",
    configured_notebook_targets(EXECUTION_CONFIG, "notebook_execution"),
    ids=lambda path: path.name,
)
def test_configured_notebooks_exist_and_load_with_nbformat(source_notebook):
    assert source_notebook.exists()
    nb = nbformat.read(source_notebook, as_version=4)
    assert nb.nbformat == 4
    assert nb.cells


@pytest.mark.parametrize(
    "source_notebook",
    configured_notebook_targets(EXECUTION_CONFIG, "notebook_execution"),
    ids=lambda path: path.name,
)
def test_configured_notebooks_are_output_free_and_unexecuted(source_notebook):
    assert_source_notebook_clean(source_notebook)


def test_notebook_01_is_in_readiness_and_execution_targets():
    notebook_01 = "notebooks/01_fintech_daily_bars_extraction_backfill.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)

    assert notebook_01 in readiness["notebook_validation"]["default_targets"]
    assert notebook_01 in execution["notebook_execution"]["default_targets"]


def test_notebook_02_is_in_readiness_and_execution_targets():
    notebook_02 = "notebooks/02_fintech_session_persistence_save_restore.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)

    assert notebook_02 in readiness["notebook_validation"]["default_targets"]
    assert notebook_02 in execution["notebook_execution"]["default_targets"]


def test_notebook_03_is_in_readiness_and_execution_targets():
    notebook_03 = "notebooks/03_fintech_archive_backup_pack_and_restore.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)

    assert notebook_03 in readiness["notebook_validation"]["default_targets"]
    assert notebook_03 in execution["notebook_execution"]["default_targets"]


def test_notebook_02_sanitized_copy_removes_runtime_restore_cells():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb"

    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    assert skipped + kept_code > 0
    assert "!fintech-save-session" not in sanitized_sources
    assert "!fintech-restore-session" not in sanitized_sources
    assert "RESTORE_COMMAND_CANDIDATE" not in sanitized_sources
    assert "drive.mount(" not in sanitized_sources
    assert ".mkdir(" not in sanitized_sources


def test_notebook_03_sanitized_copy_removes_archive_runtime_cells():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb"

    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    assert kept_code > 0
    assert "!python -m pip install" not in sanitized_sources
    assert "drive.mount(" not in sanitized_sources
    assert "!fintech-init-project" not in sanitized_sources
    assert "!fintech-backup-data" not in sanitized_sources
    assert "fintech-backup-data restore" not in sanitized_sources
    assert "SOURCE_DATASET_ROOT.mkdir" not in sanitized_sources
    assert "path.write_bytes" not in sanitized_sources
    assert "BACKUP_PACK_DIR" not in sanitized_sources
    assert "PREVIOUS_BACKUP_PACK_DIR" not in sanitized_sources
    assert "RESTORE_ROOT" not in sanitized_sources


def test_notebook_03_blocks_drive_directory_creation_until_preflight_is_ready():
    source_notebook = REPO_ROOT / "notebooks" / "03_fintech_archive_backup_pack_and_restore.ipynb"
    notebook = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in notebook.cells)

    assert "if DRIVE_FOLDER_NAME_IS_PLACEHOLDER:" in source
    assert "Update DRIVE_FOLDER_NAME before creating Drive archive directories." in source
    assert 'if not Path("/content/drive/MyDrive").is_dir():' in source
    assert "Mount Google Drive in Colab before creating Drive archive directories." in source


def test_notebook_02_has_archive_restore_preflight_guardrails():
    source_notebook = REPO_ROOT / "notebooks" / "02_fintech_session_persistence_save_restore.ipynb"
    notebook = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in notebook.cells)

    assert "Notebook 02 - Fintech Archive Restore and Session Readiness" in source
    assert "Initialize Local Restore Workspace" in source
    assert "ARCHIVE_RESTORE_PREFLIGHT_READY" in source
    assert "INIT_PROJECT_COMMAND" in source
    assert "fintech-init-project" in source
    assert "SESSION_NAME" in source
    assert '"--notebooks",' in source
    assert '"--notebooks", "REPLACE_WITH_NOTEBOOKS_ROOT"' not in source
    assert "REPLACE_WITH_NOTEBOOKS_ROOT" not in source
    assert "REPLACE_WITH_DRIVE_FOLDER_NAME" in source
    assert "REPLACE_WITH_SESSION_ID" in source
    assert "REPLACE_WITH_BACKUP_ID" in source
    assert "RESTORE_TARGET_READY" in source
    assert "EXPECTED_RESTORE_TARGET_PATHS" in source
    assert "RESTORE_ROOT" in source
    assert "Missing restore target path" in source
    assert "Local restore workspace initialization remains manual Colab-only." in source
    assert "DRIVE_BACKUP_ROOT" in source
    assert "DRIVE_BACKUP_MANIFEST" in source
    assert "Missing backup-pack source path" in source
    assert "Missing backup-pack manifest path" in source
    assert 'ARCHIVE_RESTORE_COMMAND_CANDIDATE = "fintech-backup-data"' in source
    assert "ARCHIVE_RESTORE_COMMAND" in source
    assert "fintech-backup-data" in source
    assert "fintech-backup-data restore" in source
    assert "--backup-pack-dir" in source
    assert "--restore-root" in source
    assert 'OVERWRITE_POLICY = "fail"' in source
    assert '"refuse"' not in source
    assert "--source" not in source
    assert '"fintech-restore-session"' not in source
    assert "RuntimeError" in source


def test_notebook_04_is_in_readiness_and_execution_targets():
    notebook_04 = "notebooks/04_stratlake_feature_series_index_setup.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)

    assert notebook_04 in readiness["notebook_validation"]["default_targets"]
    assert notebook_04 in execution["notebook_execution"]["default_targets"]


def test_notebook_04_source_preserves_dual_session_ids():
    source_notebook = REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb"
    notebook = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in notebook.cells)

    assert "FINTECH_SESSION_ID" in source
    assert "STRATLAKE_SESSION_ID" in source
    assert "MARKETLAKE_ROOT" in source
    assert "fintech-init-project" in source
    assert "stratlake-init-session" in source


def test_notebook_04_sanitized_copy_removes_runtime_cells():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb"

    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    assert skipped + kept_code > 0

    assert "!pip install" not in sanitized_sources
    assert "drive.mount(" not in sanitized_sources
    assert "google.colab" not in sanitized_sources
    assert "!fintech-init-project" not in sanitized_sources
    assert "!stratlake-init-session" not in sanitized_sources
    assert "!stratlake-build-features" not in sanitized_sources
    assert ".mkdir(" not in sanitized_sources
    assert "STRATLAKE_ROOT" not in sanitized_sources
    assert "MARKETLAKE_ROOT" not in sanitized_sources
    assert "available_fintech_sessions" not in sanitized_sources


def test_notebook_04_sanitized_does_not_invoke_shell_or_drive():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "04_stratlake_feature_series_index_setup.ipynb"

    sanitized, skipped, _ = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    for line in sanitized_sources.splitlines():
        stripped = line.lstrip()
        assert not stripped.startswith("!"), f"Shell command leaked into sanitized output: {line!r}"
        assert "drive.mount(" not in stripped
        assert "!pip install" not in stripped
        assert "!fintech-backup-data" not in stripped
        assert "!stratlake-" not in stripped


def test_issue_14_readiness_command_remains_compatible():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_notebook_execution_readiness.py"),
            "--config",
            str(READINESS_CONFIG),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "source_notebook",
    configured_notebook_targets(EXECUTION_CONFIG, "notebook_execution"),
    ids=lambda path: path.name,
)
def test_sanitized_execution_does_not_mutate_source(source_notebook, tmp_path):
    config = load_toml(EXECUTION_CONFIG)
    execution = config["notebook_execution"]
    assert execution["execute_sanitized_copy"] is True
    assert execution["full_notebook_execution_enabled"] is False
    assert execution["write_outputs_to_source"] is False

    before = file_digest(source_notebook)
    source_nb = nbformat.read(source_notebook, as_version=4)
    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)

    assert skipped > 0
    assert skipped + kept_code > 0

    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))
    unsafe_fragments = [
        "!python -m pip install",
        "drive.mount(",
        "userdata.get(",
        "getpass.getpass(",
        "!fintech-init-project",
        "!fintech-backfill",
        "!fintech-save-session",
        "!fintech-restore-session",
        "RESTORE_COMMAND_CANDIDATE",
        "RESTORE_ROOT",
        "BACKUP_PACK_DIR",
        "PREVIOUS_BACKUP_PACK_DIR",
        "DRIVE_BACKUP_ROOT",
        "RESTORE_BACKUP_ROOT",
        "SOURCE_DATASET_ROOT.mkdir",
        "path.write_bytes",
        "!fintech-backup-data",
        "fintech-backup-data restore",
        "session_manifest_paths",
        "available_drive_sessions",
        "DAILY_BARS_ROOT.rglob",
        ".mkdir(",
        "!stratlake-init-session",
        "!stratlake-build-features",
        "STRATLAKE_ROOT",
        "available_fintech_sessions",
        "MARKETLAKE_ROOT",
    ]
    for fragment in unsafe_fragments:
        assert fragment not in sanitized_sources

    sanitized_path = tmp_path / f"{source_notebook.stem}.sanitized.ipynb"
    nbformat.write(sanitized, sanitized_path)

    client = NotebookClient(
        sanitized,
        timeout=execution["timeout_seconds"],
        allow_errors=execution["allow_errors"],
        resources={"metadata": {"path": str(tmp_path)}},
    )
    executed = client.execute()

    executed_path = tmp_path / f"{source_notebook.stem}.executed.ipynb"
    nbformat.write(executed, executed_path)

    after = file_digest(source_notebook)
    assert before == after
    assert_source_notebook_clean(source_notebook)

    source_outputs = sum(len(cell.get("outputs", [])) for cell in notebook_code_cells(source_nb))
    assert source_outputs == 0
    assert sanitized_path.exists()
    assert executed_path.exists()
