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


def test_notebook_05_is_in_readiness_and_execution_targets():
    notebook_05 = "notebooks/05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)

    assert notebook_05 in readiness["notebook_validation"]["default_targets"]
    assert notebook_05 in execution["notebook_execution"]["default_targets"]


def test_notebook_05_source_preserves_q1_feature_generation_workflow():
    source_notebook = (
        REPO_ROOT
        / "notebooks"
        / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    )
    notebook = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in notebook.cells)

    assert "FINTECH_SESSION_ID" in source
    assert "STRATLAKE_SESSION_ID" in source
    assert "MARKETLAKE_ROOT" in source
    assert "--marketlake-root {MARKETLAKE_ROOT_STR}" in source
    assert "--marketlake-root {MARKETLAKE_ROOT.as_posix()}" in source
    assert "--start 2025-01-01" in source
    assert "--end 2025-04-01" in source
    assert "fintech-init-project" in source
    assert "stratlake-init-session" in source
    assert "fintech-backfill-daily" in source
    assert "stratlake-build-features" in source
    assert "stratlake-session-export" in source
    assert "--dry-run" in source
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in source
    assert 'FINTECH_SESSION_ID = FINTECH_SESSION_MANIFEST["session_id"]' in source
    assert "STRATLAKE_SESSION_ID = (" in source


def test_notebook_05_sanitized_copy_removes_runtime_cells():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = (
        REPO_ROOT
        / "notebooks"
        / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    )

    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    assert kept_code > 0
    assert "!pip install" not in sanitized_sources
    assert "%pip" not in sanitized_sources
    assert "drive.mount(" not in sanitized_sources
    assert "google.colab" not in sanitized_sources
    assert "userdata.get(" not in sanitized_sources
    assert "getpass.getpass(" not in sanitized_sources
    assert "ALPACA_API_KEY_ID" not in sanitized_sources
    assert "ALPACA_API_SECRET_KEY" not in sanitized_sources
    assert "!fintech-init-project" not in sanitized_sources
    assert "!stratlake-init-session" not in sanitized_sources
    assert "!fintech-backfill-daily" not in sanitized_sources
    assert "!stratlake-build-features" not in sanitized_sources
    assert "!stratlake-session-export" not in sanitized_sources
    assert "!fintech-backup-data" not in sanitized_sources
    assert "!stratlake-session-archive-bootstrap" not in sanitized_sources
    assert "!stratlake-session-archive-restore-bootstrap" not in sanitized_sources
    assert ".mkdir(" not in sanitized_sources
    assert ".write_text(" not in sanitized_sources
    assert "os.chdir(" not in sanitized_sources
    assert 'rglob("*.parquet")' not in sanitized_sources
    assert "FINTECH_ROOT" not in sanitized_sources
    assert "STRATLAKE_ROOT" not in sanitized_sources
    assert "MARKETLAKE_ROOT" not in sanitized_sources
    assert "FINTECH_SESSION_MANIFEST" not in sanitized_sources
    assert "STRATLAKE_SESSION_FILE" not in sanitized_sources
    assert "feature_candidates" not in sanitized_sources


def test_notebook_05_sanitized_does_not_invoke_shell_drive_or_credentials():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = (
        REPO_ROOT
        / "notebooks"
        / "05_stratlake_q1_feature_data_generation_with_daily_bars_ingestion.ipynb"
    )

    sanitized, skipped, _ = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    for line in sanitized_sources.splitlines():
        stripped = line.lstrip()
        assert not stripped.startswith("!"), f"Shell command leaked into sanitized output: {line!r}"
        assert not stripped.startswith("%"), f"Magic command leaked into sanitized output: {line!r}"
        assert "drive.mount(" not in stripped
        assert "userdata.get(" not in stripped
        assert "getpass.getpass(" not in stripped
        assert "!fintech-" not in stripped
        assert "!stratlake-" not in stripped


def test_config_includes_notebook_06_readiness_target():
    notebook_06 = "notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    assert notebook_06 in readiness["notebook_validation"]["default_targets"]


def test_config_includes_notebook_06_sanitized_execution_target():
    notebook_06 = "notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb"
    execution = load_toml(EXECUTION_CONFIG)
    assert notebook_06 in execution["notebook_execution"]["default_targets"]


def test_notebook_06_is_in_readiness_and_execution_targets():
    notebook_06 = "notebooks/06_stratlake_feature_validation_archive_and_handoff.ipynb"
    readiness = load_toml(READINESS_CONFIG)
    execution = load_toml(EXECUTION_CONFIG)
    assert notebook_06 in readiness["notebook_validation"]["default_targets"]
    assert notebook_06 in execution["notebook_execution"]["default_targets"]


def test_notebook_06_source_hygiene():
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"
    assert_source_notebook_clean(source_notebook)


def test_notebook_06_execution_counts_and_outputs_are_clean():
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"
    nb = nbformat.read(source_notebook, as_version=4)
    for index, cell in enumerate(notebook_code_cells(nb)):
        assert cell.get("outputs", []) == [], f"cell {index} has outputs"
        assert cell.get("execution_count") is None, f"cell {index} has execution_count"


def test_notebook_06_source_invariants_are_pinned():
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"
    nb = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in nb.cells)

    # Session and workspace identifiers
    assert "FINTECH_SESSION_ID" in source
    assert "STRATLAKE_SESSION_ID" in source
    assert "MARKETLAKE_ROOT" in source

    # Drive placeholder guard
    assert 'DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"' in source

    # Q1 validation window
    assert 'START_DATE = "2025-01-01"' in source
    assert 'END_DATE = "2025-04-01"' in source

    # Compact ticker universe
    assert 'TICKERS = ["AAPL", "MSFT", "NVDA"]' in source

    # Command surface lists
    assert "required_workflow_commands" in source
    assert "optional_unverified_preview_commands" in source

    # Optional/unverified archive bootstrap commands remain source-visible
    assert "stratlake-session-archive-bootstrap" in source
    assert "stratlake-session-archive-restore-bootstrap" in source

    # Registry-current Fintech backup preview variables
    assert "FINTECH_PACK_COMMAND_TEXT" in source
    assert "FINTECH_RESTORE_COMMAND_TEXT" in source

    # Fintech pack CLI flags
    assert "--workspace-root {FINTECH_ROOT_STR}" in source
    assert "--source-dataset-root {MARKETLAKE_ROOT_STR}" in source
    assert "--backup-root {FINTECH_DRIVE_BACKUP_ROOT_STR}" in source
    assert "--backup-id {FINTECH_ARCHIVE_ID}" in source
    assert "--shard-size-mb 512" in source

    # Fintech restore CLI flags
    assert "--backup-pack-dir {RESTORE_FINTECH_BACKUP_PACK_DIR_STR}" in source
    assert "--restore-root {MARKETLAKE_ROOT_STR}" in source
    assert "--overwrite-policy fail" in source

    # StratLake export dry-run remains source-visible
    assert "!stratlake-session-export" in source
    assert "--dry-run" in source


def test_notebook_06_sanitized_execution_skips_runtime_surfaces():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"

    sanitized, skipped, kept_code = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    assert skipped + kept_code > 0

    # Package installs
    assert "!pip install" not in sanitized_sources
    assert "%pip" not in sanitized_sources

    # Drive and Colab surfaces
    assert "drive.mount(" not in sanitized_sources
    assert "google.colab" not in sanitized_sources
    assert "userdata.get(" not in sanitized_sources
    assert "getpass.getpass(" not in sanitized_sources

    # Session initialization
    assert "!fintech-init-project" not in sanitized_sources
    assert "!stratlake-init-session" not in sanitized_sources

    # Data generation and export
    assert "!fintech-backfill-daily" not in sanitized_sources
    assert "!stratlake-build-features" not in sanitized_sources
    assert "!stratlake-session-export" not in sanitized_sources

    # Archive/restore execution
    assert "!fintech-backup-data" not in sanitized_sources
    assert "subprocess.run(" not in sanitized_sources

    # Filesystem mutation
    assert ".mkdir(" not in sanitized_sources
    assert ".write_text(" not in sanitized_sources
    assert "os.chdir(" not in sanitized_sources

    # Generated data inspection
    assert 'rglob("*.parquet")' not in sanitized_sources
    assert "pd.read_parquet(" not in sanitized_sources
    assert "display(" not in sanitized_sources

    # Runtime path namespaces
    assert "FINTECH_ROOT" not in sanitized_sources
    assert "STRATLAKE_ROOT" not in sanitized_sources
    assert "MARKETLAKE_ROOT" not in sanitized_sources
    assert "DAILY_BARS_ROOT" not in sanitized_sources
    assert "FINTECH_DRIVE" not in sanitized_sources
    assert "STRATLAKE_DRIVE" not in sanitized_sources

    # Session/manifest artifacts
    assert "FINTECH_SESSION_MANIFEST" not in sanitized_sources
    assert "STRATLAKE_SESSION_FILE" not in sanitized_sources
    assert "feature_candidates" not in sanitized_sources


def test_notebook_06_sanitized_execution_does_not_require_colab_or_credentials():
    config = load_toml(EXECUTION_CONFIG)
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"

    sanitized, skipped, _ = build_sanitized_notebook(source_notebook, config)
    sanitized_sources = "\n".join(sanitized_code_sources(sanitized))

    assert skipped > 0
    for line in sanitized_sources.splitlines():
        stripped = line.lstrip()
        assert not stripped.startswith("!"), f"Shell command leaked into sanitized output: {line!r}"
        assert not stripped.startswith("%"), f"Magic command leaked into sanitized output: {line!r}"
        assert "drive.mount(" not in stripped
        assert "userdata.get(" not in stripped
        assert "getpass.getpass(" not in stripped
        assert "!fintech-" not in stripped
        assert "!stratlake-" not in stripped
        assert "ALPACA_API_KEY" not in stripped


def test_notebook_06_sanitized_execution_does_not_mutate_source():
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"
    nb = nbformat.read(source_notebook, as_version=4)
    source_before = "\n".join(cell_source(cell) for cell in nb.cells)

    config = load_toml(EXECUTION_CONFIG)
    build_sanitized_notebook(source_notebook, config)

    nb_after = nbformat.read(source_notebook, as_version=4)
    source_after = "\n".join(cell_source(cell) for cell in nb_after.cells)
    assert source_before == source_after, "Sanitized build mutated the source notebook"


def test_notebook_06_runtime_cells_remain_manual_only():
    source_notebook = REPO_ROOT / "notebooks" / "06_stratlake_feature_validation_archive_and_handoff.ipynb"
    nb = nbformat.read(source_notebook, as_version=4)
    source = "\n".join(cell_source(cell) for cell in nb.cells)

    # These runtime surfaces must be present in source (manual Colab-only)
    assert "!fintech-init-project" in source
    assert "!stratlake-init-session" in source
    assert "!fintech-backfill-daily" in source
    assert "!stratlake-build-features" in source
    assert "!stratlake-session-export" in source
    assert "subprocess.run(" in source
    assert "drive.mount(" in source
    assert "from google.colab import drive" in source
    assert "pd.read_parquet(" in source
    assert "display(" in source


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
        "ALPACA_API_KEY_ID",
        "ALPACA_API_SECRET_KEY",
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
        "!stratlake-session-export",
        "STRATLAKE_ROOT",
        "available_fintech_sessions",
        "MARKETLAKE_ROOT",
        ".write_text(",
        "os.chdir(",
        'rglob("*.parquet")',
        "feature_candidates",
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
